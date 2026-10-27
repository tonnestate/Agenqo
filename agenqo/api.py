"""Guarded Agenqo concierge prototype API; no external delivery or payment processing."""
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hmac
import json
import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import engine, get_db
from .domain import (RuleViolation, cents, commission_cents, gross_cents, move,
                     new_token, offer_fingerprint, require_valid_offer, token_digest, token_matches)
from .models import (Base, Company, ServiceRequest, Invitation, Quote, Booking,
                     CommissionEvent, AuditEvent)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Development only: production requires versioned Alembic migrations.
    if os.getenv("AGENQO_AUTO_CREATE_SCHEMA") == "1":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Agenqo Concierge Core", version="0.1.0", lifespan=lifespan)


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
        expires_at=aware(q.expires_at))


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


class InvitationIn(BaseModel):
    company_id: str


class QuoteIn(BaseModel):
    description: str = Field(min_length=8, max_length=20000)
    conditions: str = Field(default="", max_length=20000)
    price_net_eur: Decimal = Field(ge=0)
    vat_percent: Decimal = Field(default=Decimal("19.00"), ge=0, le=100)
    expires_at: datetime
    binding_declared_by_provider: bool = False


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
    request = ServiceRequest(**payload.model_dump(), customer_token_hash=token_digest(token))
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
    request = request_by_id(db, request_id)
    company = db.get(Company, payload.company_id)
    if company is None:
        raise HTTPException(404, "company_not_found")
    if request.status not in {"QUALIFIED", "INVITING", "COLLECTING"}:
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
    db.commit()
    return {"invitation_id": invitation.id, "status": invitation.status,
            "provider_token": token, "expires_at": aware(invitation.expires_at).isoformat(),
            "external_delivery": False}


@app.post("/v1/provider/invitations/{token}/quotes", status_code=201)
def submit_quote(token: str, payload: QuoteIn, db: Session = Depends(get_db)):
    invitation = invitation_by_token(db, token)
    if invitation.status != "READY":
        raise RuleViolation("invitation_not_open")
    if payload.expires_at.tzinfo is None or aware(payload.expires_at) <= now():
        raise RuleViolation("offer_expiry_must_be_future_and_timezone_aware")
    request = request_by_id(db, invitation.request_id)
    price = cents(payload.price_net_eur)
    total = gross_cents(price, payload.vat_percent)
    quote = Quote(invitation_id=invitation.id, description=payload.description,
                  conditions=payload.conditions, net_cents=price,
                  gross_cents=total, vat_percent=payload.vat_percent,
                  expires_at=payload.expires_at,
                  binding_declared_by_provider=payload.binding_declared_by_provider)
    db.add(quote)
    db.flush()
    quote.fingerprint = quote_hash(quote)
    invitation.status = move("invitation", invitation.status, "RESPONDED", "provider")
    if request.status == "INVITING":
        request.status = move("request", request.status, "COLLECTING", "provider")
    audit(db, "QUOTE_SUBMITTED", quote.id, "provider",
          {"request_id": request.id, "provider_binding_declaration": payload.binding_declared_by_provider})
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
    existing = db.query(Booking).filter_by(request_id=request.id).first()
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
    booking = Booking(request_id=request.id, quote_id=quote.id,
                      offer_fingerprint=quote.fingerprint)
    db.add(booking)
    quote.status = move("quote", quote.status, "ACCEPTED", "customer")
    request.status = move("request", request.status, "APPROVAL_PENDING", "customer")
    db.flush()
    audit(db, "CUSTOMER_APPROVED", booking.id, "customer", {"fingerprint": quote.fingerprint})
    db.commit()
    return {"booking_id": booking.id, "status": booking.status, "idempotent_replay": False}


@app.post("/v1/provider/invitations/{token}/bookings/{booking_id}/confirm")
def confirm_booking(token: str, booking_id: str, db: Session = Depends(get_db)):
    invitation = invitation_by_token(db, token)
    booking = db.get(Booking, booking_id)
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
    company = db.get(Company, invitation.company_id)
    commission = None
    if company.commission_agreement_reference and company.commission_rate_percent is not None:
        commission = CommissionEvent(booking_id=booking.id,
            agreement_reference=company.commission_agreement_reference,
            net_cents=commission_cents(quote.net_cents,
                         company.commission_rate_percent, company.commission_min_cents))
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
