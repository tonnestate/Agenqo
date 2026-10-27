"""Provider account isolation and versioned schema regression tests."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import jwt
from alembic import command
from alembic.config import Config
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from agenqo.api import app
from agenqo.database import get_db
from agenqo.models import Base, CompanyMembership, CompanyObservation, CompanyGoldenField
import agenqo.auth as auth

ADMIN={"X-Admin-Key":"admin-qa-token"}
ISSUER="https://identity.example.test/realms/agenqo"
AUDIENCE="agenqo-api"
JWKS_URI="https://identity.example.test/realms/agenqo/protocol/openid-connect/certs"


@pytest.fixture
def oidc_client(monkeypatch):
    monkeypatch.setenv("AGENQO_ADMIN_KEY","admin-qa-token")
    monkeypatch.setenv("AGENQO_OIDC_ISSUER",ISSUER)
    monkeypatch.setenv("AGENQO_OIDC_AUDIENCE",AUDIENCE)
    monkeypatch.setenv("AGENQO_OIDC_JWKS_URL",JWKS_URI)
    private=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    key=private.public_key()
    monkeypatch.setattr(auth,"_jwks_client",lambda url:SimpleNamespace(
        get_signing_key_from_jwt=lambda token:SimpleNamespace(key=key)))
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},
                         poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,expire_on_commit=False)
    def db_override():
        with Session() as db:
            yield db
    app.dependency_overrides[get_db]=db_override
    def make_token(sub="provider-1",typ="at+jwt",aud=AUDIENCE,exp=3600):
        ts=int(datetime.now(timezone.utc).timestamp())
        payload={"iss":ISSUER,"aud":aud,"sub":sub,"exp":ts+exp,"iat":ts}
        return jwt.encode(payload,private,algorithm="RS256",
                          headers={"typ":typ,"kid":"testing-key"})
    with TestClient(app) as client:
        yield client,Session,make_token
    app.dependency_overrides.clear()
    engine.dispose()


def test_claim_review_membership_and_profile_mutation(oidc_client):
    client,Session,token=oidc_client
    res=client.post("/v1/admin/companies",headers=ADMIN,json={
        "legal_name":"Nord GmbH","postal_code":"20095","service_category":"entruempelung",
        "contact_email":"post@example.test"})
    assert res.status_code==201
    cid=res.json()["company_id"]
    member={"Authorization":"Bearer "+token()}
    outsider={"Authorization":"Bearer "+token(sub="other-subject")}
    path=f"/v1/provider/companies/{cid}/proposed-updates"
    assert client.post(path,headers=member,json={"field_name":"legal_name","value":"Wrong Name"}).status_code==403
    assert client.post(f"/v1/provider/companies/{cid}/claim",
        json={"claimant_email":"owner@example.test","proof_reference":"signed-ownership-proof"},
        headers={}).status_code==401
    claim=client.post(f"/v1/provider/companies/{cid}/claim",
        json={"claimant_email":"owner@example.test","proof_reference":"signed-ownership-proof"},
        headers=member)
    assert claim.status_code==201,claim.text
    claimid=claim.json()["claim_id"]
    assert claim.json()["provider_access_enabled"] is False
    assert client.post(f"/v1/provider/companies/{cid}/claim",
        json={"claimant_email":"owner@example.test","proof_reference":"signed-ownership-proof"},
        headers=member).status_code==409
    assert client.get("/v1/provider/companies",headers=member).json()["companies"]==[]
    approval=client.post(f"/v1/admin/ownership-claims/{claimid}/review",headers=ADMIN,
        json={"approved":True,"reviewer_reference":"manual-check-2026"})
    assert approval.status_code==200 and approval.json()["provider_access_enabled"] is True
    names=client.get("/v1/provider/companies",headers=member).json()["companies"]
    assert len(names)==1 and names[0]["company_id"]==cid
    assert client.get("/v1/provider/companies",headers=outsider).json()["companies"]==[]
    assert client.post(path,headers=outsider,json={
        "field_name":"legal_name","value":"Stolen Company","public_reuse_consent":True}).status_code==403
    update=client.post(path,headers=member,json={
        "field_name":"legal_name","value":"Nord Entsorgung GmbH",
        "public_reuse_consent":True})
    assert update.status_code==201,update.text
    observation_id=update.json()["observation_id"]
    assert update.json()["published"] is False
    # No automatic supplier-authored modification of the canonical identity.
    with Session() as db:
        assert db.query(CompanyGoldenField).count()==0
        assert db.query(CompanyMembership).count()==1
        observation=db.get(CompanyObservation,observation_id)
        assert observation.source_kind=="PROVIDER_ASSERTION"
    assert client.post(f"/v1/admin/observations/{observation_id}/publish",
                       headers=ADMIN).status_code==409
    assert client.post(f"/v1/admin/observations/{observation_id}/verify",
                       headers=ADMIN).status_code==200
    assert client.post(f"/v1/admin/observations/{observation_id}/publish",
                       headers=ADMIN).status_code==200


def test_jwt_fail_closed(oidc_client,monkeypatch):
    client,_,token=oidc_client
    route="/v1/provider/companies"
    assert client.get(route).status_code==401
    assert client.get(route,headers={"Authorization":"Bearer "+token(typ="JWT")}).status_code==401
    assert client.get(route,headers={"Authorization":"Bearer "+token(aud="wrong-audience")}).status_code==401
    assert client.get(route,headers={"Authorization":"Bearer "+token(exp=-30_000)}).status_code==401
    assert client.get(route,headers={"Authorization":"Bearer nonsensical-token"}).status_code==401
    monkeypatch.delenv("AGENQO_OIDC_JWKS_URL")
    assert client.get(route,headers={"Authorization":"Bearer "+token()}).status_code==503


def test_migration_creates_fresh_schema(tmp_path,monkeypatch):
    url="sqlite:///"+str(tmp_path/"agenqo_schema.db")
    monkeypatch.setenv("AGENQO_DATABASE_URL",url)
    cfg=Config(str(Path(__file__).resolve().parents[1]/"alembic.ini"))
    command.upgrade(cfg,"head")
    engine=create_engine(url)
    try:
        tables=set(inspect(engine).get_table_names())
        expected=set(Base.metadata.tables.keys()) | {"alembic_version"}
        assert tables==expected,expected ^ tables
        assert "claimant_subject" in {
            c["name"] for c in inspect(engine).get_columns("company_ownership_claims")}
        assert inspect(engine).get_unique_constraints("company_memberships")
        command.upgrade(cfg,"head")
    finally:
        engine.dispose()
