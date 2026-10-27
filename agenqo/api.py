"""Guarded Agenqo concierge prototype API; no external delivery or payment processing."""
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import hmac
import json
import os
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from .auth import require_provider_identity
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import engine, get_db
from .domain import (RuleViolation, cents, commission_cents, gross_cents, move,
                     new_token, offer_fingerprint, require_valid_offer, token_digest, token_matches)
from .models import (Base, Company, ServiceRequest, Invitation, Quote, Booking,
                     CommissionEvent, AuditEvent, OutboxEvent,
                     CompanyObservation, CompanyGoldenField, CompanyOwnershipClaim, CompanyMembership, RequestEconomicEvent)
from .company_records import (SOURCES, LICENSE_STATES, normalized_field,
                              observation_fingerprint, publishable)
from .service_catalog import (public_schema, quote_form_schema, validate_attributes)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Development only: production requires versioned Alembic migrations.
    if os.getenv("AGENQO_AUTO_CREATE_SCHEMA") == "1":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Agenqo Concierge Core", version="0.2.0", lifespan=lifespan)
_WEB_DIST = Path(__file__).resolve().parent.parent / "web_dist"
if (_WEB_DIST / "index.html").is_file():
    app.mount("/assets", StaticFiles(directory=_WEB_DIST / "assets"), name="quote-form-assets")
    @app.get("/quote", include_in_schema=False)
    @app.get("/provider", include_in_schema=False)
    @app.get("/provider/callback", include_in_schema=False)
    def quote_page():
        return FileResponse(_WEB_DIST / "index.html", headers={
            "Cache-Control": "no-store", "Referrer-Policy": "no-referrer",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; object-src 'none'"})



@app.exception_handler(RuleViolation)
async def domain_error(_, exc: RuleViolation):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=409, content={"error": str(exc)})


def admin(x_admin_key: str | None = Header(default=None)) -> None:
    configured = os.getenv("AGENQO_ADMIN_KEY", "")
    if not configured or not x_admin_key or not hmac.compare_digest(configured, x_admin_key):
        raise HTTPException(403, "admin_access_denied")


def now() -> datetime:
    return datetime.now(timezone.utc)


def aware(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def audit(db: Session, kind: str, reference: str, actor: str, details: dict | None = None):
    db.add(AuditEvent(kind=kind, reference_id=reference, actor=actor,
                      details=json.dumps(details or {}, sort_keys=True, ensure_ascii=False)))


def invitation_by_token(db: Session, token: str) -> Invitation:
    invitation = db.query(Invitation).filter_by(token_hash=token_digest(token)).one_or_none()
    if invitation is None or not token_matches(token, invitation.token_hash):
        raise HTTPException(404, "invitation_not_found")
    if aware(invitation.expires_at) <= now():
        raise HTTPException(410, "invitation_expired")
    return invitation


def validated_attributes(category: str, attributes: dict | None) -> dict:
    try:
        return validate_attributes(category, attributes)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

def request_by_id(db: Session, request_id: str) -> ServiceRequest:
    request = db.get(ServiceRequest, request_id)
    if request is None:
        raise HTTPException(404, "request_not_found")
    return request


def customer_request(db: Session, request_id: str, token: str | None) -> ServiceRequest:
    request = request_by_id(db, request_id)
    if not token or not token_matches(token, request.customer_token_hash):
        raise HTTPException(403, "customer_access_denied")
    return request


def quote_hash(q: Quote) -> str:
    return offer_fingerprint(quote_id=q.id, revision=q.revision,
        description=q.description, conditions=q.conditions, net_cents=q.net_cents,
        gross_cents_value=q.gross_cents, vat_percent=f"{q.vat_percent:.2f}",
        expires_at=aware(q.expires_at),
        service_attributes=json.loads(q.service_attributes_json or "{}"))


class CompanyIn(BaseModel):
    legal_name: str = Field(min_length=2, max_length=255)
    postal_code: str = Field(pattern=r"^[0-9]{5}$")
    service_category: str = Field(min_length=3, max_length=80)
    contact_email: str = Field(min_length=3, max_length=255)
    commission_rate_percent: Decimal | None = Field(default=None, ge=0, le=100)
    commission_min_cents: int = Field(default=0, ge=0)
    commission_agreement_reference: str | None = None


class RequestIn(BaseModel):
    customer_email: str = Field(min_length=3, max_length=255)
    postal_code: str = Field(pattern=r"^[0-9]{5}$")
    category: str = Field(min_length=3, max_length=80)
    requirements: str = Field(min_length=10, max_length=20000)
    structured_requirements: dict | None = None


class InvitationIn(BaseModel):
    company_id: str


class QuoteIn(BaseModel):
    description: str = Field(min_length=8, max_length=20000)
    conditions: str = Field(default="", max_length=20000)
    price_net_eur: Decimal = Field(ge=0)
    vat_percent: Decimal = Field(default=Decimal("19.00"), ge=0, le=100)
    expires_at: datetime
    binding_declared_by_provider: bool = False
    service_attributes: dict | None = None


class ApprovalIn(BaseModel):
    quote_id: str
    offer_fingerprint: str = Field(min_length=64, max_length=64)


class CompletionIn(BaseModel):
    completion_evidence: str = Field(min_length=8, max_length=4000)


@app.get("/health")
def health():
    return {"status": "ok", "stage": "prototype", "external_delivery": False}


@app.post("/v1/admin/companies", dependencies=[Depends(admin)], status_code=201)
def create_company(payload: CompanyIn, db: Session = Depends(get_db)):
    if (payload.commission_rate_percent is None) != (payload.commission_agreement_reference is None):
        raise HTTPException(422, "commission_rate_and_agreement_reference_required_together")
    if payload.commission_rate_percent is None and payload.commission_min_cents:
        raise HTTPException(422, "minimum_requires_agreement")
    company = Company(**payload.model_dump())
    db.add(company)
    db.flush()
    audit(db, "COMPANY_CREATED", company.id, "admin")
    db.commit()
    return {"company_id": company.id, "status": company.status}


@app.post("/v1/admin/requests", dependencies=[Depends(admin)], status_code=201)
def create_request(payload: RequestIn, db: Session = Depends(get_db)):
    token = new_token()
    attrs = validated_attributes(payload.category, payload.structured_requirements)
    request = ServiceRequest(customer_email=payload.customer_email,
        postal_code=payload.postal_code, category=payload.category,
        requirements=payload.requirements,
        structured_requirements_json=json.dumps(attrs, ensure_ascii=False, sort_keys=True),
        customer_token_hash=token_digest(token))
    db.add(request)
    db.flush()
    audit(db, "REQUEST_CREATED", request.id, "admin")
    db.commit()
    # The customer token is only returned to the authenticated admin, once.
    return {"request_id": request.id, "status": request.status, "customer_token": token}


@app.post("/v1/admin/requests/{request_id}/qualify", dependencies=[Depends(admin)])
def qualify_request(request_id: str, db: Session = Depends(get_db)):
    request = request_by_id(db, request_id)
    request.status = move("request", request.status, "QUALIFIED", "admin")
    audit(db, "REQUEST_QUALIFIED", request.id, "admin")
    db.commit()
    return {"request_id": request.id, "status": request.status}


@app.post("/v1/admin/requests/{request_id}/invitations", dependencies=[Depends(admin)], status_code=201)
def invite_provider(request_id: str, payload: InvitationIn, db: Session = Depends(get_db)):
    # Serialize provider invitations and enforce the cap under concurrent admin calls.
    request = db.query(ServiceRequest).filter_by(id=request_id).with_for_update().populate_existing().one_or_none()
    if request is None:
        raise HTTPException(404, "request_not_found")
    company = db.get(Company, payload.company_id)
    if company is None:
        raise HTTPException(404, "company_not_found")
    if request.status not in {"QUALIFIED", "INVITING", "COLLECTING", "QUOTES_READY"}:
        raise RuleViolation("request_not_invitable")
    if company.service_category != request.category:
        raise RuleViolation("provider_wrong_category")
    if db.query(Invitation).filter_by(request_id=request_id, company_id=company.id).first():
        raise RuleViolation("provider_already_invited")
    if db.query(Invitation).filter_by(request_id=request_id).count() >= 8:
        raise RuleViolation("invitation_limit")
    token = new_token()
    invitation = Invitation(request_id=request_id, company_id=company.id,
         token_hash=token_digest(token), expires_at=now() + timedelta(days=7))
    db.add(invitation)
    db.flush()
    if request.status == "QUALIFIED":
        request.status = move("request", request.status, "INVITING", "admin")
    # The status deliberately remains READY; no actual outbound delivery is implemented.
    audit(db, "INVITATION_READY", invitation.id, "admin",
          {"request_id": request_id, "company_id": company.id})
    # No email authorization is implied by an invitation record.
    db.add(OutboxEvent(event_type="invitation.review_requested", aggregate_id=invitation.id,
        payload=json.dumps({"invitation_id": invitation.id, "request_id": request_id,
                            "company_id": company.id, "policy": "INTERNAL_REVIEW_ONLY"},
                           sort_keys=True)))
    db.commit()
    return {"invitation_id": invitation.id, "status": invitation.status,
            "provider_token": token, "expires_at": aware(invitation.expires_at).isoformat(),
            "external_delivery": False}


def submit_quote(token: str, payload: QuoteIn, db: Session = Depends(get_db)):
    invitation = invitation_by_token(db, token)
    return submit_quote_for_invitation(invitation, payload, db)

def submit_quote_for_invitation(invitation: Invitation, payload: QuoteIn, db: Session):
    # MySQL/InnoDB row lock; a second concurrent offer cannot reuse this invitation.
    invitation = db.query(Invitation).filter_by(id=invitation.id).with_for_update().populate_existing().one()
    if aware(invitation.expires_at) <= now():
        raise HTTPException(410, "invitation_expired")
    if invitation.status != "READY":
        raise RuleViolation("invitation_not_open")
    if payload.expires_at.tzinfo is None or aware(payload.expires_at) <= now():
        raise RuleViolation("offer_expiry_must_be_future_and_timezone_aware")
    request = request_by_id(db, invitation.request_id)
    attrs = validated_attributes(request.category, payload.service_attributes)
    price = cents(payload.price_net_eur)
    total = gross_cents(price, payload.vat_percent)
    quote = Quote(invitation_id=invitation.id, revision=1, description=payload.description,
                  conditions=payload.conditions, net_cents=price,
                  gross_cents=total, vat_percent=payload.vat_percent,
                  expires_at=payload.expires_at.astimezone(timezone.utc).replace(microsecond=0),
                  binding_declared_by_provider=payload.binding_declared_by_provider,
                  service_attributes_json=json.dumps(attrs, ensure_ascii=False, sort_keys=True))
    # Materialize identifier and content hash before the NOT NULL database insert.
    from .models import uid
    quote.id = uid()
    quote.fingerprint = quote_hash(quote)
    db.add(quote)
    db.flush()
    invitation.status = move("invitation", invitation.status, "RESPONDED", "provider")
    if request.status == "INVITING":
        request.status = move("request", request.status, "COLLECTING", "provider")
    audit(db, "QUOTE_SUBMITTED", quote.id, "provider",
          {"request_id": request.id, "provider_binding_declaration": payload.binding_declared_by_provider})
    db.add(OutboxEvent(event_type="quote.review_requested", aggregate_id=quote.id,
        payload=json.dumps({"quote_id": quote.id, "request_id": request.id,
                            "policy": "INTERNAL_REVIEW_ONLY"}, sort_keys=True)))
    db.commit()
    return {"quote_id": quote.id, "status": quote.status,
            "gross_cents": total, "fingerprint": quote.fingerprint}


@app.post("/v1/admin/quotes/{quote_id}/validate", dependencies=[Depends(admin)])
def validate_quote(quote_id: str, db: Session = Depends(get_db)):
    quote = db.get(Quote, quote_id)
    if quote is None:
        raise HTTPException(404, "quote_not_found")
    if not quote.binding_declared_by_provider:
        raise RuleViolation("provider_has_not_declared_binding_offer")
    if aware(quote.expires_at) <= now():
        raise RuleViolation("offer_expired")
    quote.status = move("quote", quote.status, "BINDING", "admin")
    request = request_by_id(db, db.get(Invitation, quote.invitation_id).request_id)
    if request.status == "COLLECTING":
        request.status = move("request", request.status, "QUOTES_READY", "admin")
    audit(db, "QUOTE_VALIDATED", quote.id, "admin", {"fingerprint": quote.fingerprint})
    db.commit()
    return {"quote_id": quote.id, "status": quote.status}


@app.get("/v1/requests/{request_id}/offers")
def list_offers(request_id: str, x_customer_key: str | None = Header(default=None),
                db: Session = Depends(get_db)):
    request = customer_request(db, request_id, x_customer_key)
    result = []
    query = (db.query(Quote, Company)
            .join(Invitation, Invitation.id == Quote.invitation_id)
            .join(Company, Company.id == Invitation.company_id)
            .filter(Invitation.request_id == request.id, Quote.status == "BINDING"))
    for quote, company in query.all():
        if aware(quote.expires_at) <= now():
            continue
        result.append({"quote_id": quote.id, "company_name": company.legal_name,
                       "description": quote.description, "conditions": quote.conditions,
                       "net_cents": quote.net_cents, "gross_cents": quote.gross_cents,
                       "vat_percent": f"{quote.vat_percent:.2f}",
                       "valid_until": aware(quote.expires_at).isoformat(),
                       "fingerprint": quote.fingerprint})
    return {"request_id": request.id, "status": request.status,
            "offers": sorted(result, key=lambda item: item["gross_cents"])}


@app.post("/v1/requests/{request_id}/approve", status_code=201)
def approve_offer(request_id: str, payload: ApprovalIn,
                  x_customer_key: str | None = Header(default=None),
                  db: Session = Depends(get_db)):
    request = customer_request(db, request_id, x_customer_key)
    # Serialize all approval attempts for this RFQ before looking up existing bookings.
    request = db.query(ServiceRequest).filter_by(id=request.id).with_for_update().populate_existing().one()
    existing = db.query(Booking).filter_by(request_id=request.id).with_for_update().populate_existing().first()
    if existing:
        if existing.quote_id == payload.quote_id and hmac.compare_digest(
                existing.offer_fingerprint, payload.offer_fingerprint):
            return {"booking_id": existing.id, "status": existing.status,
                    "idempotent_replay": True}
        raise RuleViolation("request_already_has_another_booking")
    if request.status != "QUOTES_READY":
        raise RuleViolation("request_not_ready_for_approval")
    quote = db.get(Quote, payload.quote_id)
    if quote is None:
        raise HTTPException(404, "quote_not_found")
    invitation = db.get(Invitation, quote.invitation_id)
    if invitation.request_id != request_id:
        raise HTTPException(403, "quote_not_for_request")
    require_valid_offer(quote.status, aware(quote.expires_at),
                        payload.offer_fingerprint, quote_hash(quote))
    company = db.get(Company, invitation.company_id)
    booking = Booking(request_id=request.id, quote_id=quote.id,
                      offer_fingerprint=quote.fingerprint,
                      commission_agreement_reference=company.commission_agreement_reference,
                      commission_rate_percent=company.commission_rate_percent,
                      commission_min_cents=company.commission_min_cents)
    db.add(booking)
    quote.status = move("quote", quote.status, "ACCEPTED", "customer")
    request.status = move("request", request.status, "APPROVAL_PENDING", "customer")
    db.flush()
    audit(db, "CUSTOMER_APPROVED", booking.id, "customer", {"fingerprint": quote.fingerprint})
    db.commit()
    return {"booking_id": booking.id, "status": booking.status, "idempotent_replay": False}


def confirm_booking(token: str, booking_id: str, db: Session = Depends(get_db)):
    invitation = invitation_by_token(db, token)
    return confirm_booking_for_invitation(invitation, booking_id, db)

def confirm_booking_for_invitation(invitation: Invitation, booking_id: str, db: Session):
    booking = db.query(Booking).filter_by(id=booking_id).with_for_update().populate_existing().one_or_none()
    if booking is None:
        raise HTTPException(404, "booking_not_found")
    quote = db.get(Quote, booking.quote_id)
    if quote.invitation_id != invitation.id:
        raise HTTPException(403, "provider_not_authorized_for_booking")
    if booking.status == "PROVIDER_CONFIRMED":
        return {"booking_id": booking.id, "status": booking.status, "idempotent_replay": True}
    if not hmac.compare_digest(booking.offer_fingerprint, quote_hash(quote)):
        raise RuleViolation("offer_changed_before_confirmation")
    if aware(quote.expires_at) <= now():
        raise RuleViolation("offer_expired_before_confirmation")
    booking.status = move("booking", booking.status, "PROVIDER_CONFIRMED", "provider")
    request = request_by_id(db, booking.request_id)
    request.status = move("request", request.status, "BOOKED", "provider")
    audit(db, "BOOKING_CONFIRMED", booking.id, "provider")
    db.add(OutboxEvent(event_type="booking.confirmed", aggregate_id=booking.id,
        payload=json.dumps({"booking_id":booking.id,"request_id":request.id,
                            "policy":"INTERNAL_REVIEW_ONLY"},sort_keys=True)))
    db.commit()
    return {"booking_id": booking.id, "status": booking.status, "idempotent_replay": False}


@app.post("/v1/admin/bookings/{booking_id}/complete", dependencies=[Depends(admin)])
def complete_booking(booking_id: str, payload: CompletionIn, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(404, "booking_not_found")
    booking.status = move("booking", booking.status, "COMPLETED", "admin")
    booking.completion_evidence = payload.completion_evidence
    request = request_by_id(db, booking.request_id)
    request.status = move("request", request.status, "COMPLETED", "admin")
    quote = db.get(Quote, booking.quote_id)
    invitation = db.get(Invitation, quote.invitation_id)
    commission = None
    # Commission terms are frozen at customer approval, never read from mutable company settings.
    if booking.commission_agreement_reference and booking.commission_rate_percent is not None:
        commission = CommissionEvent(booking_id=booking.id,
            agreement_reference=booking.commission_agreement_reference,
            net_cents=commission_cents(quote.net_cents,
                         booking.commission_rate_percent, booking.commission_min_cents))
        db.add(commission)
    audit(db, "BOOKING_COMPLETED", booking.id, "admin",
          {"completion_evidence": payload.completion_evidence,
           "commission_agreement": bool(commission)})
    db.commit()
    return {"booking_id": booking.id, "status": booking.status,
            "commission_eligible_cents": commission.net_cents if commission else None,
            "commission_status": "ELIGIBLE" if commission else "NO_AGREEMENT"}


@app.get("/v1/admin/requests/{request_id}", dependencies=[Depends(admin)])
def admin_request(request_id: str, db: Session = Depends(get_db)):
    request = request_by_id(db, request_id)
    return {"request_id": request.id, "status": request.status,
            "invitations": db.query(Invitation).filter_by(request_id=request_id).count(),
            "booked": db.query(Booking).filter_by(request_id=request_id).count() > 0}


# ----- Donor adapters: JSON Schema, Golden Record provenance and ownership -----

class ObservationIn(BaseModel):
    field_name: str
    value: str
    source_kind: str
    source_ref: str = Field(min_length=8, max_length=2048)
    license_state: str = "UNKNOWN"

class OwnershipClaimIn(BaseModel):
    claimant_email: str = Field(min_length=5, max_length=255)
    proof_reference: str = Field(min_length=8, max_length=1024)

class OwnershipReviewIn(BaseModel):
    approved: bool
    reviewer_reference: str = Field(min_length=5, max_length=255)

@app.get("/v1/service-schemas/{category}")
def get_service_schema(category: str):
    try:
        return public_schema(category)
    except ValueError:
        raise HTTPException(404, "service_category_not_activated")

@app.get("/v1/quote-form-schema")
def get_quote_form_schema():
    return quote_form_schema()

@app.get("/v1/provider/invitation")
def provider_invitation(x_invitation_key: str | None = Header(default=None),
                        db: Session = Depends(get_db)):
    if not x_invitation_key:
        raise HTTPException(403, "invitation_access_denied")
    invitation = invitation_by_token(db, x_invitation_key)
    if invitation.status != "READY":
        raise HTTPException(409, "invitation_not_open")
    request = request_by_id(db, invitation.request_id)
    return {"category": request.category, "postal_code": request.postal_code,
            "requirements": request.requirements,
            "structured_requirements": json.loads(request.structured_requirements_json or "{}"),
            "expires_at": aware(invitation.expires_at).isoformat()}

@app.post("/v1/provider/quotes", status_code=201)
def submit_quote_header(payload: QuoteIn,
                        x_invitation_key: str | None = Header(default=None),
                        db: Session = Depends(get_db)):
    if not x_invitation_key:
        raise HTTPException(403, "invitation_access_denied")
    return submit_quote(x_invitation_key, payload, db)

@app.post("/v1/admin/companies/{company_id}/observations",
          dependencies=[Depends(admin)], status_code=201)
def record_observation(company_id: str, payload: ObservationIn, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if company is None:
        raise HTTPException(404, "company_not_found")
    if payload.source_kind not in SOURCES or payload.license_state not in LICENSE_STATES:
        raise HTTPException(422, "invalid_source_or_license_state")
    try:
        value = normalized_field(payload.field_name, payload.value)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    fingerprint = observation_fingerprint(
        field=payload.field_name, value=value,
        source_kind=payload.source_kind, source_ref=payload.source_ref)
    existing = db.query(CompanyObservation).filter_by(
        company_id=company_id, fingerprint=fingerprint).one_or_none()
    if existing:
        return {"observation_id":existing.id,"review_state":existing.review_state,
                "idempotent_replay":True}
    row = CompanyObservation(company_id=company_id, field_name=payload.field_name,
        value=value, source_kind=payload.source_kind, source_ref=payload.source_ref,
        license_state=payload.license_state, fingerprint=fingerprint)
    db.add(row); db.flush()
    audit(db,"COMPANY_OBSERVATION_RECORDED",row.id,"admin",{"company_id":company_id})
    db.commit()
    return {"observation_id":row.id,"review_state":row.review_state,"idempotent_replay":False}

@app.post("/v1/admin/observations/{observation_id}/verify", dependencies=[Depends(admin)])
def verify_observation(observation_id: str, db: Session = Depends(get_db)):
    observation = db.get(CompanyObservation, observation_id)
    if not observation:
        raise HTTPException(404, "observation_not_found")
    if observation.review_state != "PENDING":
        raise RuleViolation("observation_not_pending")
    observation.review_state = "VERIFIED"
    audit(db,"OBSERVATION_VERIFIED",observation_id,"admin")
    db.commit()
    return {"observation_id":observation_id,"review_state":observation.review_state}

@app.post("/v1/admin/observations/{observation_id}/publish", dependencies=[Depends(admin)])
def publish_observation(observation_id: str, db: Session = Depends(get_db)):
    observation = db.get(CompanyObservation, observation_id)
    if observation is None:
        raise HTTPException(404, "observation_not_found")
    if not publishable(license_state=observation.license_state,
                       review_state=observation.review_state):
        raise RuleViolation("observation_not_approved_for_public_reuse")
    company = db.get(Company, observation.company_id)
    field = db.query(CompanyGoldenField).filter_by(
        company_id=observation.company_id, field_name=observation.field_name).one_or_none()
    if field is None:
        field = CompanyGoldenField(company_id=observation.company_id,
            field_name=observation.field_name, value=observation.value,
            observation_id=observation.id)
        db.add(field)
    else:
        field.value = observation.value
        field.observation_id = observation.id
    setattr(company, observation.field_name, observation.value)
    audit(db,"GOLDEN_FIELD_PUBLISHED",observation.id,"admin",
          {"company_id":company.id,"field":observation.field_name})
    db.commit()
    return {"company_id":company.id,"field":observation.field_name,
            "value":observation.value,"source_observation_id":observation.id}

@app.post("/v1/admin/companies/{company_id}/ownership-claims",
          dependencies=[Depends(admin)], status_code=201)
def create_ownership_claim(company_id: str, payload: OwnershipClaimIn,
                           db: Session = Depends(get_db)):
    if db.get(Company, company_id) is None:
        raise HTTPException(404, "company_not_found")
    row=CompanyOwnershipClaim(company_id=company_id,
        claimant_email=payload.claimant_email, proof_reference=payload.proof_reference)
    db.add(row); db.flush()
    audit(db,"OWNERSHIP_CLAIM_STAGED",row.id,"admin",{"company_id":company_id})
    db.commit()
    return {"claim_id":row.id,"review_state":row.review_state}

@app.post("/v1/admin/ownership-claims/{claim_id}/review",dependencies=[Depends(admin)])
def review_ownership_claim(claim_id: str, payload: OwnershipReviewIn,
                           db: Session = Depends(get_db)):
    row=db.get(CompanyOwnershipClaim, claim_id)
    if not row:
        raise HTTPException(404, "claim_not_found")
    if row.review_state != "PENDING":
        raise RuleViolation("claim_already_reviewed")
    row.review_state="VERIFIED" if payload.approved else "REJECTED"
    row.reviewer_reference=payload.reviewer_reference
    access_enabled=False
    if payload.approved and row.claimant_subject:
        membership=db.query(CompanyMembership).filter_by(
            company_id=row.company_id, subject=row.claimant_subject).one_or_none()
        if membership is None:
            membership=CompanyMembership(company_id=row.company_id,
                subject=row.claimant_subject, verified_claim_id=row.id,
                role="OWNER", active=True)
            db.add(membership)
        else:
            # An explicit new verification is required to reactivate disabled members.
            membership.active=True
            membership.verified_claim_id=row.id
        access_enabled=True
    audit(db,"OWNERSHIP_CLAIM_REVIEWED",row.id,"admin",{
        "decision":row.review_state,"provider_access_enabled":access_enabled})
    db.commit()
    return {"claim_id":row.id,"review_state":row.review_state,
            "provider_access_enabled":access_enabled}

@app.get("/v1/admin/companies/{company_id}/golden-record",dependencies=[Depends(admin)])
def get_golden_record(company_id: str, db: Session = Depends(get_db)):
    company=db.get(Company,company_id)
    if not company:
        raise HTTPException(404,"company_not_found")
    observations=db.query(CompanyObservation).filter_by(company_id=company_id).all()
    golden=db.query(CompanyGoldenField).filter_by(company_id=company_id).all()
    ownership=db.query(CompanyOwnershipClaim).filter_by(company_id=company_id).all()
    return {"company_id":company_id,"legal_name":company.legal_name,
            "fields":[{"name":f.field_name,"value":f.value,
                       "observation_id":f.observation_id} for f in golden],
            "observations":[{"id":o.id,"field":o.field_name,"value":o.value,
                              "source":o.source_kind,"license_state":o.license_state,
                              "review_state":o.review_state} for o in observations],
            "ownership_claims":[{"id":c.id,"state":c.review_state} for c in ownership]}

@app.post("/v1/provider/bookings/{booking_id}/confirm")
def confirm_booking_header(booking_id: str, x_invitation_key: str | None = Header(default=None),
                           db: Session = Depends(get_db)):
    if not x_invitation_key:
        raise HTTPException(403, "invitation_access_denied")
    return confirm_booking(x_invitation_key, booking_id, db)


# ---- OIDC authenticated provider self-service; claims still require human review ----

class ProviderClaimRequest(BaseModel):
    claimant_email: str = Field(min_length=5, max_length=255)
    proof_reference: str = Field(min_length=8, max_length=1024)

class ProviderProposedUpdate(BaseModel):
    field_name: str
    value: str = Field(min_length=1, max_length=255)
    public_reuse_consent: bool = False

def authorized_membership(db: Session, company_id: str, subject: str):
    member = db.query(CompanyMembership).filter_by(
        company_id=company_id, subject=subject, active=True).one_or_none()
    if member is None or member.role not in {"OWNER", "EDITOR"}:
        raise HTTPException(403, "not_an_authorized_company_member")
    return member

@app.post("/v1/provider/companies/{company_id}/claim", status_code=201)
def provider_claim_company(company_id: str, payload: ProviderClaimRequest,
                           subject: str = Depends(require_provider_identity),
                           db: Session = Depends(get_db)):
    if db.get(Company, company_id) is None:
        raise HTTPException(404, "company_not_found")
    if db.query(CompanyMembership).filter_by(
            company_id=company_id, subject=subject, active=True).first():
        raise RuleViolation("already_an_authorized_company_member")
    if db.query(CompanyOwnershipClaim).filter_by(
            company_id=company_id, claimant_subject=subject,
            review_state="PENDING").first():
        raise RuleViolation("ownership_claim_already_pending")
    row = CompanyOwnershipClaim(company_id=company_id,
        claimant_subject=subject, claimant_email=payload.claimant_email,
        proof_reference=payload.proof_reference)
    db.add(row)
    db.flush()
    audit(db, "PROVIDER_CLAIM_SUBMITTED", row.id, "provider",
          {"company_id": company_id, "subject_digest": token_digest(subject)})
    db.commit()
    return {"claim_id": row.id, "review_state": row.review_state,
            "provider_access_enabled": False}

@app.get("/v1/provider/companies")
def provider_list_companies(subject: str = Depends(require_provider_identity),
                            db: Session = Depends(get_db)):
    memberships = db.query(CompanyMembership).filter_by(
        subject=subject, active=True).all()
    records = []
    for member in memberships:
        company = db.get(Company, member.company_id)
        if company is not None:
            records.append({"company_id":company.id, "legal_name":company.legal_name,
                            "service_category":company.service_category,
                            "postal_code":company.postal_code, "role":member.role})
    return {"companies":records}

@app.post("/v1/provider/companies/{company_id}/proposed-updates", status_code=201)
def provider_propose_company_update(company_id: str,
         payload: ProviderProposedUpdate,
         subject: str = Depends(require_provider_identity),
         db: Session = Depends(get_db)):
    authorized_membership(db, company_id, subject)
    try:
        value=normalized_field(payload.field_name,payload.value)
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc
    source_ref="oidc-subject-sha256:"+token_digest(subject)
    fingerprint=observation_fingerprint(field=payload.field_name, value=value,
        source_kind="PROVIDER_ASSERTION",source_ref=source_ref)
    existing=db.query(CompanyObservation).filter_by(
        company_id=company_id,fingerprint=fingerprint).one_or_none()
    if existing:
        return {"observation_id":existing.id,"review_state":existing.review_state,
                "idempotent_replay":True}
    row=CompanyObservation(company_id=company_id,field_name=payload.field_name,
        value=value,source_kind="PROVIDER_ASSERTION",source_ref=source_ref,
        license_state="PUBLIC_REUSE_APPROVED" if payload.public_reuse_consent else "INTERNAL_ONLY",
        fingerprint=fingerprint)
    db.add(row);db.flush()
    audit(db,"PROVIDER_PROFILE_UPDATE_PROPOSED",row.id,"provider",
          {"company_id":company_id,"subject_digest":token_digest(subject),
           "public_reuse_consent":payload.public_reuse_consent})
    db.commit()
    return {"observation_id":row.id,"review_state":row.review_state,
            "idempotent_replay":False,"published":False}


# ----- RFQ-level unit economics, including failed inquiries -----

COST_CATEGORIES = {"ACQUISITION", "MODEL", "COMMUNICATION", "SUPPORT",
                   "PROVIDER_ONBOARDING", "REFUND", "OTHER"}
RECEIPT_CATEGORIES = {"PROVIDER_COMMISSION", "BUYER_FEE", "OTHER"}

class EconomicEventIn(BaseModel):
    event_key: str = Field(min_length=6, max_length=128, pattern=r"^[a-zA-Z0-9_.:-]+$")
    direction: Literal["COST", "RECEIPT"]
    category: str
    amount_eur: Decimal = Field(gt=0)
    evidence_reference: str = Field(min_length=8, max_length=1024)

def _economic_totals(db: Session, request_id: str) -> dict:
    events=db.query(RequestEconomicEvent).filter_by(request_id=request_id).all()
    costs=sum(e.amount_cents for e in events if e.direction=="COST")
    receipts=sum(e.amount_cents for e in events if e.direction=="RECEIPT")
    return {"recorded_cost_cents":costs,"recorded_receipts_cents":receipts,
            "recorded_contribution_cents":receipts-costs, "economic_event_count":len(events)}

@app.post("/v1/admin/requests/{request_id}/economic-events",
          dependencies=[Depends(admin)], status_code=201)
def record_economic_event(request_id: str, payload: EconomicEventIn,
                          db: Session = Depends(get_db)):
    request_by_id(db,request_id)
    allowed=COST_CATEGORIES if payload.direction=="COST" else RECEIPT_CATEGORIES
    if payload.category not in allowed:
        raise HTTPException(422, "invalid_economic_category")
    amount=cents(payload.amount_eur)
    if amount <= 0:
        raise HTTPException(422,"economic_amount_too_small")
    existing=db.query(RequestEconomicEvent).filter_by(
        request_id=request_id,event_key=payload.event_key).one_or_none()
    if existing:
        if (existing.direction != payload.direction or existing.category != payload.category
            or existing.amount_cents != amount or
                existing.evidence_reference != payload.evidence_reference):
            raise RuleViolation("economic_event_key_payload_conflict")
        return {"economic_event_id":existing.id,"idempotent_replay":True}
    row=RequestEconomicEvent(request_id=request_id,event_key=payload.event_key,
        direction=payload.direction,category=payload.category,amount_cents=amount,
        evidence_reference=payload.evidence_reference)
    db.add(row)
    db.flush()
    audit(db,"RFQ_ECONOMIC_EVENT_RECORDED",row.id,"admin",{
        "request_id":request_id,"direction":payload.direction,"amount_cents":amount})
    db.commit()
    return {"economic_event_id":row.id,"idempotent_replay":False}

@app.get("/v1/admin/requests/{request_id}/economics",dependencies=[Depends(admin)])
def request_economics(request_id: str,db: Session = Depends(get_db)):
    request=request_by_id(db,request_id)
    booking=db.query(Booking).filter_by(request_id=request_id).one_or_none()
    commission=db.query(CommissionEvent).filter_by(booking_id=booking.id).one_or_none() if booking else None
    # Eligible commission is NOT recorded receipt. Payment must be separately evidenced.
    return {"request_id":request.id,"request_status":request.status,
            "booking_status":booking.status if booking else None,
            "commission_eligible_cents":commission.net_cents if commission else 0,
            **_economic_totals(db,request_id)}

@app.get("/v1/admin/economics/summary",dependencies=[Depends(admin)])
def economics_summary(db: Session = Depends(get_db)):
    requests=db.query(ServiceRequest).all()
    totals=[_economic_totals(db,r.id) for r in requests]
    n=len(requests)
    costs=sum(r["recorded_cost_cents"] for r in totals)
    receipts=sum(r["recorded_receipts_cents"] for r in totals)
    complete=sum(1 for r in requests if r.status=="COMPLETED")
    return {"total_requests":n,"completed_requests":complete,
            "booked_or_completed_requests":sum(
               1 for r in requests if r.status in {"BOOKED","COMPLETED","DISPUTED"}),
            "recorded_cost_cents":costs,"recorded_receipts_cents":receipts,
            "recorded_contribution_cents":receipts-costs,
            "recorded_contribution_per_request_cents":int(
                (Decimal(receipts-costs)/Decimal(n)).quantize(
                    Decimal("1"), rounding=ROUND_HALF_UP)) if n else None,
            "economic_event_count":sum(t["economic_event_count"] for t in totals),
            "warning":"Recorded events are operator-entered; not audited accounting or total company profit."}


# ---- Read-only analytics; DuckDB is embedded in-memory, never a transaction DB. ----
@app.get("/v1/admin/analytics/liquidity", dependencies=[Depends(admin)])
def get_liquidity_analytics(db: Session = Depends(get_db)):
    from .analytics import marketplace_liquidity_report
    try:
        return marketplace_liquidity_report(db)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc

# Register the OIDC-authenticated provider portal after core handlers are defined.
from .provider_portal import router as provider_portal_router
app.include_router(provider_portal_router)

# n8n is the operator-owned orchestration layer, not a second business state machine.
from .n8n_bridge import router as n8n_bridge_router
app.include_router(n8n_bridge_router)
