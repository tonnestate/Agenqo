"""n8n bridge contract: claim, ACK, failure, expired lease, DLQ and safety."""
from datetime import datetime, timedelta, timezone
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from agenqo.api import app
from agenqo.database import get_db
from agenqo.models import Base, OutboxEvent, AutomationReviewTask, AuditEvent

KEY = "n8n-only-bridge-key-with-very-high-entropy-123456789"
N8N = {"X-Agenqo-Bridge-Key": KEY}
ADMIN = {"X-Admin-Key": "n8n-test-admin-secret"}

@pytest.fixture
def context(monkeypatch):
    monkeypatch.setenv("AGENQO_N8N_BRIDGE_KEY",KEY)
    monkeypatch.setenv("AGENQO_ADMIN_KEY","n8n-test-admin-secret")
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,expire_on_commit=False)
    def fake_db():
        with Session() as db: yield db
    app.dependency_overrides[get_db]=fake_db
    with TestClient(app) as client:
        yield client,Session
    app.dependency_overrides.clear()
    engine.dispose()


def insert(Session,event_type="booking.confirmed",aggregate_id="book-demo",
           body=None):
    if body is None:
        body={"booking_id":"book-demo","request_id":"req-demo",
              "policy":"INTERNAL_REVIEW_ONLY"}
    with Session() as db:
        evt=OutboxEvent(event_type=event_type,aggregate_id=aggregate_id,
                        payload=json.dumps(body,sort_keys=True))
        db.add(evt)
        db.commit()
        return evt.id


def claim(c):
    response=c.post("/v1/integrations/n8n/claim",headers=N8N)
    assert response.status_code==200,response.text
    return response.json()


def complete(c,item,execution="n8n:1001"):
    return c.post("/v1/integrations/n8n/complete",headers=N8N,json={
        "event_id":item["event_id"],"lease_token":item["lease_token"],
        "execution_ref":execution})


def failed(c,item,code="WORKFLOW_FAILED"):
    return c.post("/v1/integrations/n8n/fail",headers=N8N,json={
        "event_id":item["event_id"],"lease_token":item["lease_token"],
        "error_code":code})


def test_bridge_requires_secret_and_is_disabled_by_default(context,monkeypatch):
    c,Session=context
    assert c.post("/v1/integrations/n8n/claim").status_code==403
    assert c.post("/v1/integrations/n8n/claim",
        headers={"X-Agenqo-Bridge-Key":"wrong"}).status_code==403
    monkeypatch.delenv("AGENQO_N8N_BRIDGE_KEY")
    assert c.post("/v1/integrations/n8n/claim",headers=N8N).status_code==503
    monkeypatch.setenv("AGENQO_N8N_BRIDGE_KEY",KEY)


def test_booking_event_creates_durable_internal_task_not_external_message(context):
    c,Session=context
    eid=insert(Session)
    first=claim(c)
    assert first["has_event"] is True
    evt=first["event"]
    assert evt["event_id"]==eid and evt["type"]=="booking.confirmed"
    assert evt["payload"]["policy"]=="INTERNAL_REVIEW_ONLY"
    assert "customer_email" not in first
    assert claim(c)["has_event"] is False
    assert c.get("/v1/admin/automation/status").status_code==403
    assert complete(c,{**evt,"lease_token":"short"}).status_code==422
    fake={**evt,"lease_token":"x"*40}
    assert complete(c,fake).status_code==403
    result=complete(c,evt)
    assert result.status_code==200,result.text
    assert result.json()["action"]=="INTERNAL_REVIEW_TASK_CREATED"
    replay=complete(c,evt)
    assert replay.status_code==200 and replay.json()["idempotent_replay"] is True
    assert complete(c,evt,execution="n8n:different").status_code==409
    assert failed(c,evt).status_code==409
    with Session() as db:
        row=db.get(OutboxEvent,eid)
        assert row.status=="DONE" and row.attempt_count==1
        assert db.query(AutomationReviewTask).filter_by(outbox_event_id=eid).count()==1
        assert db.query(AuditEvent).filter_by(kind="N8N_INTERNAL_REVIEW_CREATED").count()==1
    report=c.get("/v1/admin/automation/status",headers=ADMIN)
    assert report.status_code==200
    assert report.json()["open_review_tasks"]==1
    assert report.json()["external_messages_sent"]==0
    tasks=c.get("/v1/admin/automation/review-tasks",headers=ADMIN).json()["tasks"]
    assert tasks[0]["outbox_event_id"]==eid
    assert claim(c)["has_event"] is False


def test_failed_run_is_backoff_and_lease_token_rotates(context):
    c,Session=context
    eid=insert(Session)
    evt=claim(c)["event"]
    failed_response=failed(c,evt,code="TEMPORARY_FAILURE")
    assert failed_response.status_code==200
    assert failed_response.json()["status"]=="PENDING"
    assert claim(c)["has_event"] is False
    with Session() as db:
        row=db.get(OutboxEvent,eid)
        row.available_at=datetime.now(timezone.utc)-timedelta(seconds=1)
        db.commit()
    evt2=claim(c)["event"]
    assert evt2["attempt"]==2 and evt2["lease_token"]!=evt["lease_token"]
    assert complete(c,evt).status_code==403
    assert complete(c,evt2).status_code==200


def test_expired_leases_and_dead_letter_admin_retry(context):
    c,Session=context
    eid=insert(Session)
    for attempt in range(5):
        evt=claim(c)["event"]
        assert evt["attempt"]==attempt+1
        with Session() as db:
            row=db.get(OutboxEvent,eid)
            row.lease_until=datetime.now(timezone.utc)-timedelta(seconds=2)
            db.commit()
        assert complete(c,evt).status_code==409
        if attempt<4:
            # Lease expiry is reclaimed by a new claim.
            continue
    assert claim(c)["has_event"] is False
    with Session() as db:
        row=db.get(OutboxEvent,eid)
        assert row.status=="DEAD"
        assert row.last_failure_code=="LEASE_EXPIRED_MAX_ATTEMPTS"
    assert c.post(f"/v1/admin/automation/events/{eid}/retry",
        headers=ADMIN,json={"reason":"x"}).status_code==422
    recovered=c.post(f"/v1/admin/automation/events/{eid}/retry",
        headers=ADMIN,json={"reason":"Reviewed and approved by operator"},)
    assert recovered.status_code==200
    assert claim(c)["event"]["attempt"]==1


def test_bad_policy_not_orchestrated(context):
    c,Session=context
    eid=insert(Session,event_type="invitation.review_requested",
               body={"provider_token":"unsafe","policy":"EXTERNAL_EMAIL"},aggregate_id="bad-policy")
    assert claim(c)["has_event"] is False
    with Session() as db:
        assert db.get(OutboxEvent,eid).status=="DEAD"
        assert db.query(AutomationReviewTask).count()==0


def test_legacy_booking_event_without_policy_is_allowed_for_internal_review(context):
    c,Session=context
    eid=insert(Session,aggregate_id="legacy-id",body={"booking_id":"legacy-id","request_id":"legacy-rfq"})
    evt=claim(c)["event"]
    assert evt["event_id"]==eid
    assert complete(c,evt).status_code==200
