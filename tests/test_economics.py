"""Unit economics must include failed requests and exclude unpaid eligible commissions."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from agenqo.api import app
from agenqo.database import get_db
from agenqo.models import Base, RequestEconomicEvent

ADMIN={"X-Admin-Key":"economic-test-admin"}

@pytest.fixture
def setup_test(monkeypatch):
    monkeypatch.setenv("AGENQO_ADMIN_KEY","economic-test-admin")
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},
                         poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    def test_db():
        with Session() as db:
            yield db
    app.dependency_overrides[get_db]=test_db
    with TestClient(app) as client:
        yield client,Session
    app.dependency_overrides.clear()
    engine.dispose()

def make_request(client,email):
    res=client.post("/v1/admin/requests",headers=ADMIN,json={
        "customer_email":email,"postal_code":"20095","category":"entruempelung",
        "requirements":"Entruempelung von Keller und Garage"})
    assert res.status_code==201,res.text
    return res.json()["request_id"]

def record(c,request_id,key,direction,category,amount):
    return c.post(f"/v1/admin/requests/{request_id}/economic-events",headers=ADMIN,json={
        "event_key":key,"direction":direction,"category":category,
        "amount_eur":amount,"evidence_reference":"payment-or-cost-record-2026"})

def test_costs_for_nonconverting_requests_are_included(setup_test):
    c,Session=setup_test
    first=make_request(c,"one@example.test")
    second=make_request(c,"two@example.test")
    cost=record(c,first,"campaign-001","COST","ACQUISITION","25.00")
    assert cost.status_code==201,cost.text
    assert record(c,first,"campaign-001","COST","ACQUISITION","25.00").json()["idempotent_replay"]
    assert record(c,first,"campaign-001","COST","ACQUISITION","35.00").status_code==409
    assert record(c,first,"ai-001","COST","MODEL","1.25").status_code==201
    assert record(c,second,"support-001","COST","SUPPORT","10.00").status_code==201
    # Income requires separate evidence; mere RFQ creation has no recognized receipt.
    a=c.get(f"/v1/admin/requests/{first}/economics",headers=ADMIN).json()
    assert a["recorded_cost_cents"]==2625
    assert a["recorded_receipts_cents"]==0
    assert a["commission_eligible_cents"]==0
    assert record(c,first,"received-001","RECEIPT","BUYER_FEE","30.00").status_code==201
    summary=c.get("/v1/admin/economics/summary",headers=ADMIN).json()
    assert summary["total_requests"]==2
    assert summary["completed_requests"]==0
    assert summary["recorded_cost_cents"]==3625
    assert summary["recorded_receipts_cents"]==3000
    assert summary["recorded_contribution_cents"]==-625
    assert summary["recorded_contribution_per_request_cents"]==-313
    assert c.get("/v1/admin/economics/summary").status_code==403
    with Session() as db:
        assert db.query(RequestEconomicEvent).count()==4

def test_bad_economic_events_rejected(setup_test):
    c,_=setup_test
    rid=make_request(c,"one@example.test")
    assert record(c,rid,"key-111","RECEIPT","ACQUISITION","10").status_code==422
    assert record(c,rid,"key-112","COST","SUPPORT","0").status_code==422
    assert record(c,rid,"key-113","COST","SUPPORT","-5").status_code==422
    assert record(c,rid,"key-114","COST","SUPPORT","0.001").status_code==422
