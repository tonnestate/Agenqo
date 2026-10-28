"""RFQ contact permissions are fail-closed, auditable and revocable."""
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from agenqo.api import app
from agenqo.contact_policy import (
    POLICY_VERSION, destination_digest, evaluate_rfq_email,
)
from agenqo.database import get_db
from agenqo.models import (
    Base, Company, Invitation, ProviderContactPermission, ContactPolicyDecision,
    OutboxEvent,
)

ADMIN = {"X-Admin-Key": "contact-test-admin-strong-key"}


@pytest.fixture()
def client_and_session(monkeypatch):
    monkeypatch.setenv("AGENQO_ADMIN_KEY", ADMIN["X-Admin-Key"])
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    def db_override():
        with Session() as db:
            yield db
    app.dependency_overrides[get_db] = db_override
    with TestClient(app) as client:
        yield client, Session
    app.dependency_overrides.clear()
    engine.dispose()


def setup_rfq(client):
    company = client.post("/v1/admin/companies", headers=ADMIN, json={
        "legal_name": "Test Entrümpelung", "postal_code": "20095",
        "service_category": "entruempelung", "contact_email": "rfq@example.test",
    })
    assert company.status_code == 201, company.text
    cid = company.json()["company_id"]
    request = client.post("/v1/admin/requests", headers=ADMIN, json={
        "customer_email": "buyer@example.test", "postal_code": "20095",
        "category": "entruempelung", "requirements": "Wohnungsauflösung 80 qm",
    })
    assert request.status_code == 201, request.text
    rid = request.json()["request_id"]
    assert client.post(
        f"/v1/admin/requests/{rid}/qualify", headers=ADMIN, json={}
    ).status_code == 200
    invitation = client.post(
        f"/v1/admin/requests/{rid}/invitations",
        headers=ADMIN, json={"company_id": cid},
    )
    assert invitation.status_code == 201, invitation.text
    return cid, rid, invitation.json()["invitation_id"], invitation.json()["provider_token"]


def permission(client, cid, enabled, kind, reference):
    return client.post(
        f"/v1/admin/companies/{cid}/contact-permissions", headers=ADMIN,
        json={
            "enabled": enabled, "evidence_kind": kind,
            "evidence_reference": reference,
            "reviewer_reference": "human-operator-pilot-check",
        },
    )


def preflight(client, invite):
    return client.post(
        f"/v1/admin/invitations/{invite}/contact-preflight", headers=ADMIN,
        json={},
    )


def test_deny_opt_in_allow_revoke_deny_and_decision_history(client_and_session):
    client, Session = client_and_session
    cid, rid, invite, token = setup_rfq(client)
    assert client.post(f"/v1/admin/invitations/{invite}/contact-preflight").status_code == 403

    first = preflight(client, invite)
    assert first.status_code == 200, first.text
    assert first.json()["decision"] == "DENY"
    assert first.json()["reason_code"] == "NO_RECORDED_OPT_IN"

    # "Manual outreach" does not bypass an explicit documented contact policy.
    invalid = permission(client, cid, True, "OPERATOR_HOLD", "op-without-consent")
    assert invalid.status_code == 422
    yes = permission(client, cid, True, "SIGNED_PILOT_AGREEMENT", "signed-by-provider-2026")
    assert yes.status_code == 201, yes.text
    assert yes.json()["revision"] == 1
    repeat = permission(client, cid, True, "SIGNED_PILOT_AGREEMENT", "signed-by-provider-2026")
    assert repeat.status_code == 201
    assert repeat.json()["idempotent_replay"] is True
    second = preflight(client, invite)
    assert second.status_code == 200
    assert second.json()["decision"] == "ALLOW"
    assert second.json()["policy_version"] == POLICY_VERSION
    assert second.json()["external_delivery_performed"] is False

    # The invite token is enough for the provider to opt out even without an account.
    assert client.post("/v1/provider/contact/opt-out").status_code == 403
    optout = client.post(
        "/v1/provider/contact/opt-out", headers={"X-Invitation-Key": token}, json={},
    )
    assert optout.status_code == 200, optout.text
    assert optout.json()["status"] == "OPTED_OUT"
    repeated_optout = client.post(
        "/v1/provider/contact/opt-out", headers={"X-Invitation-Key": token}, json={},
    )
    assert repeated_optout.json()["idempotent_replay"] is True
    third = preflight(client, invite)
    assert third.json()["decision"] == "DENY"
    assert third.json()["reason_code"] == "OPTED_OUT"
    history = client.get(
        f"/v1/admin/invitations/{invite}/contact-decisions", headers=ADMIN,
    )
    assert history.status_code == 200
    assert sorted(d["decision"] for d in history.json()["decisions"]) == [
        "ALLOW", "DENY", "DENY"
    ]
    with Session() as db:
        versions = (
            db.query(ProviderContactPermission)
            .filter_by(company_id=cid)
            .order_by(ProviderContactPermission.revision).all()
        )
        assert [v.enabled for v in versions] == [True, False]
        assert db.query(ContactPolicyDecision).count() == 3
        # Contact decisions never generate a delivery outbox event.
        assert all(
            row.event_type == "invitation.review_requested"
            for row in db.query(OutboxEvent).all()
        )


def test_address_rotation_and_expiration_always_fail_closed(client_and_session):
    client, Session = client_and_session
    cid, rid, invite, token = setup_rfq(client)
    assert permission(
        client, cid, True, "SIGNED_PILOT_AGREEMENT", "signed-original-email-2026"
    ).status_code == 201
    assert preflight(client, invite).json()["decision"] == "ALLOW"
    with Session() as db:
        company = db.get(Company, cid)
        company.contact_email = "changed@example.test"
        db.commit()
    changed = preflight(client, invite).json()
    assert changed["decision"] == "DENY"
    assert changed["reason_code"] == "RECIPIENT_CHANGED"
    assert permission(
        client, cid, True, "SIGNED_PILOT_AGREEMENT", "signed-new-email-2026"
    ).status_code == 201
    assert preflight(client, invite).json()["decision"] == "ALLOW"

    with Session() as db:
        row = db.get(Invitation, invite)
        row.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
        db.commit()
    expired = preflight(client, invite).json()
    assert expired["decision"] == "DENY"
    assert expired["reason_code"] == "INVITATION_EXPIRED"
    # Unsubscribe remains possible after an invitation expires.
    assert client.post(
        "/v1/provider/contact/opt-out", headers={"X-Invitation-Key": token},
        json={},
    ).status_code == 200


def test_opt_out_evidence_and_no_permission_are_not_interchangeable(client_and_session):
    client, _ = client_and_session
    cid, _, inv, _ = setup_rfq(client)
    assert permission(
        client, cid, False, "SIGNED_PILOT_AGREEMENT", "incorrect-document"
    ).status_code == 422
    denied = permission(client, cid, False, "OPERATOR_HOLD", "risk-control-001")
    assert denied.status_code == 201
    assert preflight(client, inv).json()["reason_code"] == "OPTED_OUT"
    assert client.get(
        f"/v1/admin/companies/{cid}/contact-permissions", headers=ADMIN
    ).json()["history"][0]["enabled"] is False
    assert client.get(
        f"/v1/admin/companies/{cid}/contact-permissions"
    ).status_code == 403


def test_pure_policy_checks_category_status_and_digest():
    now = datetime.now(timezone.utc)
    base = dict(
        permission_enabled=True,
        permission_destination_digest=destination_digest("Info@Example.test"),
        destination_email="info@example.test",
        request_category="entruempelung",
        provider_category="entruempelung",
        request_status="INVITING",
        invitation_status="READY",
        invitation_expires_at=now + timedelta(hours=1),
        at=now,
    )
    assert evaluate_rfq_email(**base).decision == "ALLOW"
    assert evaluate_rfq_email(**(base | {"request_category": "fotografie"})).reason_code == "CATEGORY_MISMATCH"
    assert evaluate_rfq_email(**(base | {"request_status": "DRAFT"})).reason_code == "REQUEST_NOT_QUALIFIED"
    assert evaluate_rfq_email(**(base | {"invitation_status": "RESPONDED"})).reason_code == "INVITATION_NOT_READY"
    assert evaluate_rfq_email(**(base | {"permission_enabled": None})).decision == "DENY"
