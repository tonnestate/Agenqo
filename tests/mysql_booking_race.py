"""Actual InnoDB regression test for two simultaneous customer approvals.

Run ONLY after applying Alembic migrations to a dedicated disposable MySQL database.
Uses Agenqo's production approve_offer business operation, not a mocked duplicate.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from threading import Barrier

from agenqo.api import ApprovalIn, approve_offer, quote_hash
from agenqo.database import SessionLocal, engine
from agenqo.domain import new_token, token_digest
from agenqo.models import (Company, ServiceRequest, Invitation, Quote, Booking, uid)


assert engine.dialect.name == "mysql", "Run against isolated MySQL test DB only"

customer_token = new_token()
with SessionLocal() as db:
    company = Company(id=uid(),legal_name="Concurrency Test GmbH",
        postal_code="20095",service_category="entruempelung",
        contact_email="qa@example.test",commission_rate_percent=Decimal("8.00"),
        commission_min_cents=4000,
        commission_agreement_reference="test-agreement-signed")
    request = ServiceRequest(id=uid(),customer_email="buyer@example.test",
        customer_token_hash=token_digest(customer_token),category="entruempelung",
        postal_code="20095",requirements="Wohnung ausraeumen und Abfall entsorgen",
        status="QUOTES_READY")
    invitation = Invitation(id=uid(),request_id=request.id,company_id=company.id,
        token_hash=token_digest(new_token()),status="RESPONDED",
        expires_at=datetime.now(timezone.utc)+timedelta(days=3))
    quote = Quote(id=uid(),invitation_id=invitation.id,revision=1,
        description="Komplettentsorgung",conditions="Besenrein",
        net_cents=100000,gross_cents=119000,vat_percent=Decimal("19.00"),
        expires_at=datetime.now(timezone.utc)+timedelta(days=2),
        binding_declared_by_provider=True,service_attributes_json="{}",
        status="BINDING",fingerprint="0"*64)
    quote.fingerprint=quote_hash(quote)
    company_id, request_id, quote_id, fingerprint = (company.id,request.id,quote.id,quote.fingerprint)
    # SQLAlchemy has no ORM relationships here: insert parents explicitly before FK children.
    db.add_all([company, request])
    db.flush()
    db.add(invitation)
    db.flush()
    db.add(quote)
    db.commit()

# Detect value canonicalization differences between ORM insert and MySQL round-trip.
with SessionLocal() as db:
    stored = db.get(Quote, quote_id)
    stored_hash = quote_hash(stored)
    if stored_hash != fingerprint:
        raise AssertionError({
            "pre_insert_hash":fingerprint,
            "mysql_roundtrip_hash":stored_hash,
            "expires_at":str(stored.expires_at),
            "vat_percent":str(stored.vat_percent),
            "revision":stored.revision,
            "conditions":stored.conditions,
            "attributes":stored.service_attributes_json,
            "description":stored.description,
            "net":stored.net_cents,
            "gross":stored.gross_cents
        })

start = Barrier(2)

def book(_):
    with SessionLocal() as db:
        start.wait(timeout=10)
        return approve_offer(
            request_id,
            ApprovalIn(quote_id=quote_id,offer_fingerprint=fingerprint),
            x_customer_key=customer_token,db=db)

with ThreadPoolExecutor(max_workers=2) as pool:
    outcomes=list(pool.map(book,range(2)))

assert len({x["booking_id"] for x in outcomes})==1,outcomes
assert sorted(x["idempotent_replay"] for x in outcomes)==[False,True],outcomes
with SessionLocal() as db:
    assert db.query(Booking).filter_by(request_id=request_id).count()==1
print("PASS: competing MySQL booking approvals serialized to one booking with idempotent replay")
