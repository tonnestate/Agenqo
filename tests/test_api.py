from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest

from agenqo.api import app
from agenqo.database import get_db
from agenqo.models import Base, CommissionEvent, Company

ADMIN = {"X-Admin-Key": "test-admin-long-secret"}

@pytest.fixture()
def app_client(monkeypatch):
    monkeypatch.setenv("AGENQO_ADMIN_KEY", "test-admin-long-secret")
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    def override():
        with Session() as db:
            yield db
    app.dependency_overrides[get_db] = override
    with TestClient(app) as client:
        yield client, Session
    app.dependency_overrides.clear()
    engine.dispose()

def post(client, path, data, headers=ADMIN):
    return client.post(path, json=data, headers=headers)

def create_flow(client, partner=True):
    company = post(client, "/v1/admin/companies",
       {"legal_name": "Test Entruempelung GmbH", "postal_code": "20095",
        "service_category": "entruempelung", "contact_email": "offer@example.test",
        **({"commission_rate_percent": "8.00", "commission_min_cents": 4000,
            "commission_agreement_reference": "signed-pilot-2026-001"} if partner else {})})
    assert company.status_code == 201, company.text
    company_id = company.json()["company_id"]
    req = post(client, "/v1/admin/requests",
       {"customer_email": "buyer@example.test", "postal_code": "20095",
        "category": "entruempelung", "requirements": "Wohnungsaufloesung 80 qm, Stock 2"})
    assert req.status_code == 201, req.text
    request_id = req.json()["request_id"]
    customer_key = req.json()["customer_token"]
    assert post(client, f"/v1/admin/requests/{request_id}/qualify", {}).status_code == 200
    inv = post(client, f"/v1/admin/requests/{request_id}/invitations", {"company_id": company_id})
    assert inv.status_code == 201, inv.text
    token = inv.json()["provider_token"]
    assert inv.json()["external_delivery"] is False
    expiry = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    quote = post(client, "/v1/provider/quotes",
         {"description": "Wohnung komplett raeumen und fachgerecht entsorgen",
          "conditions": "Besenrein", "price_net_eur": "1260.50",
          "vat_percent": "19.00", "expires_at": expiry,
          "binding_declared_by_provider": True}, headers={"X-Invitation-Key": token})
    assert quote.status_code == 201, quote.text
    quote_id = quote.json()["quote_id"]
    assert post(client, f"/v1/admin/quotes/{quote_id}/validate", {}).status_code == 200
    return request_id, customer_key, token, quote_id

def test_guards_and_e2e_commission(app_client):
    client, Session = app_client
    assert post(client, "/v1/admin/requests", {}, headers={}).status_code == 403
    request_id, key, token, quote_id = create_flow(client)
    assert client.get(f"/v1/requests/{request_id}/offers").status_code == 403
    response = client.get(f"/v1/requests/{request_id}/offers", headers={"X-Customer-Key": key})
    assert response.status_code == 200
    offers = response.json()["offers"]
    assert len(offers) == 1 and offers[0]["gross_cents"] == 150000
    approval = post(client, f"/v1/requests/{request_id}/approve",
       {"quote_id": quote_id, "offer_fingerprint": "0"*64},
       headers={"X-Customer-Key": key})
    assert approval.status_code == 409
    payload = {"quote_id": quote_id, "offer_fingerprint": offers[0]["fingerprint"]}
    approval = post(client, f"/v1/requests/{request_id}/approve", payload,
       headers={"X-Customer-Key": key})
    assert approval.status_code == 201, approval.text
    booking_id = approval.json()["booking_id"]
    repeat = post(client, f"/v1/requests/{request_id}/approve", payload,
       headers={"X-Customer-Key": key})
    assert repeat.json()["idempotent_replay"] is True
    assert post(client, f"/v1/admin/bookings/{booking_id}/complete",
                {"completion_evidence": "Confirmed via signed completion document"}).status_code == 409
    confirmation = post(client, f"/v1/provider/bookings/{booking_id}/confirm",
                        {}, headers={"X-Invitation-Key": token})
    assert confirmation.status_code == 200
    # An agreement changed after booking must NOT change this booking's commission.
    with Session() as db:
        company = db.query(Company).one()
        company.commission_rate_percent = 20
        company.commission_agreement_reference = "future-agreement-999"
        db.commit()
    done = post(client, f"/v1/admin/bookings/{booking_id}/complete",
         {"completion_evidence": "Buyer confirmed work by email, manually checked"})
    assert done.status_code == 200, done.text
    assert done.json()["commission_eligible_cents"] == 10084
    assert post(client, f"/v1/admin/bookings/{booking_id}/complete",
         {"completion_evidence": "Second verified completion attempt"}).status_code == 409
    with Session() as db:
        assert db.query(CommissionEvent).count() == 1

def test_no_agreement_no_commission(app_client):
    client, Session = app_client
    request_id, key, token, quote_id = create_flow(client, partner=False)
    offer = client.get(f"/v1/requests/{request_id}/offers",
                       headers={"X-Customer-Key": key}).json()["offers"][0]
    booked = post(client, f"/v1/requests/{request_id}/approve",
        {"quote_id": quote_id, "offer_fingerprint": offer["fingerprint"]},
        headers={"X-Customer-Key": key}).json()
    assert post(client, f"/v1/provider/bookings/{booked['booking_id']}/confirm",
                {}, headers={"X-Invitation-Key": token}).status_code == 200
    # A retroactively added agreement must not create a commission.
    with Session() as db:
        company = db.query(Company).one()
        company.commission_rate_percent = 8
        company.commission_agreement_reference = "agreement-after-booking"
        db.commit()
    done = post(client, f"/v1/admin/bookings/{booked['booking_id']}/complete",
        {"completion_evidence": "Manually verified completed work"})
    assert done.status_code == 200
    assert done.json()["commission_status"] == "NO_AGREEMENT"

def test_provider_isolation_and_quote_auth(app_client):
    client, _ = app_client
    request_id, key, token, quote_id = create_flow(client)
    other_company = post(client, "/v1/admin/companies",
        {"legal_name": "Other Provider", "postal_code": "20095",
         "service_category": "entruempelung", "contact_email": "other@example.test"}).json()
    inv = post(client, f"/v1/admin/requests/{request_id}/invitations",
        {"company_id": other_company["company_id"]}).json()
    other_token = inv["provider_token"]
    offer = client.get(f"/v1/requests/{request_id}/offers",
        headers={"X-Customer-Key": key}).json()["offers"][0]
    booking = post(client, f"/v1/requests/{request_id}/approve",
        {"quote_id": quote_id, "offer_fingerprint": offer["fingerprint"]},
        headers={"X-Customer-Key": key}).json()
    cross = post(client, f"/v1/provider/bookings/{booking['booking_id']}/confirm",
        {}, headers={"X-Invitation-Key": other_token})
    assert cross.status_code == 403
    assert post(client, "/v1/provider/quotes",
        {"description": "unallowed repeat", "price_net_eur": "10",
         "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()},
        headers={"X-Invitation-Key": token}).status_code == 409



def test_buyer_status_requires_own_token_and_never_exposes_email(app_client):
    client, _ = app_client
    request_id, key, token, quote_id = create_flow(client)
    endpoint = f"/v1/requests/{request_id}/status"
    assert client.get(endpoint).status_code == 403
    assert client.get(endpoint, headers={"X-Customer-Key": "wrong"}).status_code == 403
    status = client.get(endpoint, headers={"X-Customer-Key": key})
    assert status.status_code == 200, status.text
    data = status.json()
    assert data["request_id"] == request_id
    assert data["status"] == "QUOTES_READY"
    assert data["category"] == "entruempelung"
    assert data["booking_status"] is None
    assert "buyer@example.test" not in status.text
    assert "customer_token" not in status.text
    assert "offer" not in status.text
    offers = client.get(
        f"/v1/requests/{request_id}/offers", headers={"X-Customer-Key": key}
    ).json()["offers"]
    booking = post(
        client, f"/v1/requests/{request_id}/approve",
        {"quote_id": quote_id, "offer_fingerprint": offers[0]["fingerprint"]},
        headers={"X-Customer-Key": key},
    )
    assert booking.status_code == 201, booking.text
    after = client.get(endpoint, headers={"X-Customer-Key": key}).json()
    assert after["status"] == "APPROVAL_PENDING"
    assert after["booking_status"] == "CUSTOMER_APPROVED"
    assert after["booking_id"] == booking.json()["booking_id"]


def test_buyers_cannot_read_other_buyers_requests(app_client):
    client, _ = app_client
    rid_a, key_a, _, _ = create_flow(client)
    rid_b, key_b, _, _ = create_flow(client)
    assert client.get(
        f"/v1/requests/{rid_b}/status",
        headers={"X-Customer-Key": key_a},
    ).status_code == 403
    assert client.get(
        f"/v1/requests/{rid_a}/offers",
        headers={"X-Customer-Key": key_b},
    ).status_code == 403
