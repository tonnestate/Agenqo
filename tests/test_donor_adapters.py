from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest
from agenqo.api import app
from agenqo.database import get_db
from agenqo.domain import offer_fingerprint
from agenqo.models import Base, Company, CompanyGoldenField, CompanyObservation, OutboxEvent
from agenqo.service_catalog import validate_attributes

ADMIN={"X-Admin-Key":"test-admin-key"}

@pytest.fixture()
def setup_db(monkeypatch):
    monkeypatch.setenv("AGENQO_ADMIN_KEY","test-admin-key")
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,expire_on_commit=False)
    def get_test_db():
        with Session() as db:
            yield db
    app.dependency_overrides[get_db]=get_test_db
    with TestClient(app) as client:
        yield client,Session
    app.dependency_overrides.clear()
    engine.dispose()

def test_schema_enforcement(setup_db):
    c,_=setup_db
    schema=c.get("/v1/service-schemas/entruempelung")
    assert schema.status_code==200
    assert schema.json()["additionalProperties"] is False
    assert c.get("/v1/service-schemas/unknown").status_code==404
    assert "price_net_eur" in c.get("/v1/quote-form-schema").json()["required"]
    with pytest.raises(ValueError):
        validate_attributes("entruempelung",{"volume_m3":-10})
    with pytest.raises(ValueError):
        validate_attributes("entruempelung",{"password":"x"})

def test_golden_record_and_ownership_gate(setup_db):
    c,Session=setup_db
    comp=c.post("/v1/admin/companies",headers=ADMIN,json={
        "legal_name":"Muster GmbH","postal_code":"20095",
        "service_category":"entruempelung","contact_email":"a@example.test"})
    assert comp.status_code==201
    cid=comp.json()["company_id"]
    url=f"/v1/admin/companies/{cid}/observations"
    src={"field_name":"legal_name","value":"Muster Nord GmbH","source_kind":"OFFICIAL_REGISTER",
         "source_ref":"https://register.example.test/1","license_state":"INTERNAL_ONLY"}
    obs=c.post(url,headers=ADMIN,json=src)
    assert obs.status_code==201
    oid=obs.json()["observation_id"]
    assert c.post(url,headers=ADMIN,json=src).json()["idempotent_replay"] is True
    assert c.post(f"/v1/admin/observations/{oid}/publish",headers=ADMIN).status_code==409
    assert c.post(f"/v1/admin/observations/{oid}/verify",headers=ADMIN).status_code==200
    assert c.post(f"/v1/admin/observations/{oid}/publish",headers=ADMIN).status_code==409
    pub=c.post(url,headers=ADMIN,json={**src,"value":"Muster Nord 2 GmbH",
                                       "license_state":"PUBLIC_REUSE_APPROVED"})
    oid2=pub.json()["observation_id"]
    assert c.post(f"/v1/admin/observations/{oid2}/verify",headers=ADMIN).status_code==200
    assert c.post(f"/v1/admin/observations/{oid2}/publish",headers=ADMIN).status_code==200
    claim=c.post(f"/v1/admin/companies/{cid}/ownership-claims",headers=ADMIN,json={
        "claimant_email":"owner@example.test","proof_reference":"inperson-reviewed-2026"})
    assert claim.status_code==201
    review=c.post(f"/v1/admin/ownership-claims/{claim.json()['claim_id']}/review",
        headers=ADMIN,json={"approved":True,"reviewer_reference":"operator-verification-ref"})
    assert review.json()["provider_access_enabled"] is False
    rec=c.get(f"/v1/admin/companies/{cid}/golden-record",headers=ADMIN).json()
    assert rec["legal_name"]=="Muster Nord 2 GmbH"
    with Session() as db:
        assert db.query(CompanyObservation).count()==2
        assert db.query(CompanyGoldenField).count()==1
        assert db.get(Company,cid).legal_name=="Muster Nord 2 GmbH"

def test_quote_header_flow_and_safe_outbox(setup_db):
    c,Session=setup_db
    comp=c.post("/v1/admin/companies",headers=ADMIN,json={"legal_name":"Entruempelung Nord",
        "postal_code":"20095","service_category":"entruempelung",
        "contact_email":"anbieter@example.test"}).json()
    req=c.post("/v1/admin/requests",headers=ADMIN,json={
        "customer_email":"kunde@example.test","postal_code":"20095",
        "category":"entruempelung","requirements":"Keller fachgerecht komplett ausraeumen",
        "structured_requirements":{"object_type":"keller","volume_m3":13.5}})
    assert req.status_code==201,req.text
    rid=req.json()["request_id"]
    assert c.post(f"/v1/admin/requests/{rid}/qualify",headers=ADMIN).status_code==200
    inv=c.post(f"/v1/admin/requests/{rid}/invitations",headers=ADMIN,
        json={"company_id":comp["company_id"]}).json()
    key=inv["provider_token"]
    assert c.get("/v1/provider/invitation").status_code==403
    detail=c.get("/v1/provider/invitation",headers={"X-Invitation-Key":key})
    assert detail.json()["structured_requirements"]["volume_m3"]==13.5
    assert "customer_email" not in detail.json()
    data={"description":"Raeumung mit Entsorgung","price_net_eur":"400",
          "vat_percent":"19","binding_declared_by_provider":True,
          "expires_at":(datetime.now(timezone.utc)+timedelta(days=2)).isoformat(),
          "service_attributes":{"volume_m3":14}}
    quote=c.post("/v1/provider/quotes",headers={"X-Invitation-Key":key},json=data)
    assert quote.status_code==201,quote.text
    qid=quote.json()["quote_id"]
    assert c.post(f"/v1/admin/quotes/{qid}/validate",headers=ADMIN).status_code==200
    offers=c.get(f"/v1/requests/{rid}/offers",
        headers={"X-Customer-Key":req.json()["customer_token"]}).json()["offers"]
    assert len(offers)==1
    approved=c.post(f"/v1/requests/{rid}/approve",headers={
        "X-Customer-Key":req.json()["customer_token"]},json={
        "quote_id":qid,"offer_fingerprint":offers[0]["fingerprint"]})
    assert approved.status_code==201
    bid=approved.json()["booking_id"]
    assert c.post(f"/v1/provider/invitations/{key}/bookings/{bid}/confirm").status_code==200
    with Session() as db:
        event=db.query(OutboxEvent).filter_by(event_type="booking.confirmed").one()
        assert event.status=="PENDING"
        assert key not in event.payload and "kunde@example.test" not in event.payload

def test_service_fingerprint_binds_attributes():
    expiry=datetime.now(timezone.utc)+timedelta(days=1)
    kw={"quote_id":"q","revision":1,"description":"Leistung","conditions":"",
        "net_cents":10000,"gross_cents_value":11900,"vat_percent":"19.00",
        "expires_at":expiry}
    assert offer_fingerprint(**kw,service_attributes={"volume_m3":5}) != offer_fingerprint(
        **kw,service_attributes={"volume_m3":10})
