"""Prototype persistence schema; migrations are required before production."""
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def uid():
    return str(uuid4())

def utcnow():
    return datetime.now(timezone.utc)

class Company(Base):
    __tablename__ = "companies"
    id = Column(String(36), primary_key=True, default=uid)
    legal_name = Column(String(255), nullable=False)
    postal_code = Column(String(5), nullable=False)
    service_category = Column(String(80), nullable=False)
    contact_email = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default="IDENTIFIED")
    commission_rate_percent = Column(Numeric(5, 2))
    commission_min_cents = Column(Integer, nullable=False, default=0)
    commission_agreement_reference = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(String(36), primary_key=True, default=uid)
    customer_email = Column(String(255), nullable=False)
    customer_token_hash = Column(String(64), nullable=False)
    category = Column(String(80), nullable=False)
    postal_code = Column(String(5), nullable=False)
    requirements = Column(Text, nullable=False)
    structured_requirements_json = Column(Text, nullable=False, default="{}")
    status = Column(String(32), nullable=False, default="DRAFT")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = (UniqueConstraint("request_id", "company_id", name="uq_invitation_request_company"),)
    id = Column(String(36), primary_key=True, default=uid)
    request_id = Column(String(36), ForeignKey("service_requests.id"), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True)
    status = Column(String(32), nullable=False, default="READY")
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(String(36), primary_key=True, default=uid)
    invitation_id = Column(String(36), ForeignKey("invitations.id"), nullable=False, unique=True)
    revision = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=False)
    conditions = Column(Text, nullable=False, default="")
    net_cents = Column(Integer, nullable=False)
    gross_cents = Column(Integer, nullable=False)
    vat_percent = Column(Numeric(5, 2), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    binding_declared_by_provider = Column(Boolean, nullable=False, default=False)
    service_attributes_json = Column(Text, nullable=False, default="{}")
    status = Column(String(32), nullable=False, default="SUBMITTED")
    fingerprint = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String(36), primary_key=True, default=uid)
    request_id = Column(String(36), ForeignKey("service_requests.id"), nullable=False, unique=True)
    quote_id = Column(String(36), ForeignKey("quotes.id"), nullable=False, unique=True)
    offer_fingerprint = Column(String(64), nullable=False)
    # Snapshot of the agreement in force when the customer approved this quote.
    commission_agreement_reference = Column(String(255))
    commission_rate_percent = Column(Numeric(5, 2))
    commission_min_cents = Column(Integer, nullable=False, default=0)
    status = Column(String(32), nullable=False, default="CUSTOMER_APPROVED")
    completion_evidence = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class CommissionEvent(Base):
    __tablename__ = "commission_events"
    id = Column(String(36), primary_key=True, default=uid)
    booking_id = Column(String(36), ForeignKey("bookings.id"), nullable=False, unique=True)
    agreement_reference = Column(String(255), nullable=False)
    net_cents = Column(Integer, nullable=False)
    status = Column(String(32), nullable=False, default="ELIGIBLE")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(String(36), primary_key=True, default=uid)
    kind = Column(String(100), nullable=False)
    reference_id = Column(String(36), nullable=False)
    actor = Column(String(32), nullable=False)
    details = Column(Text, nullable=False, default="{}")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    __table_args__ = (UniqueConstraint("event_type","aggregate_id",name="uq_outbox_event_kind"),)
    id = Column(String(36), primary_key=True, default=uid)
    event_type = Column(String(80), nullable=False)
    aggregate_id = Column(String(36), nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class CompanyObservation(Base):
    """An observed value is never silently published or treated as a supplier assertion."""
    __tablename__ = "company_observations"
    __table_args__ = (UniqueConstraint("company_id", "fingerprint", name="uq_company_observation"),)
    id = Column(String(36), primary_key=True, default=uid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    field_name = Column(String(80), nullable=False)
    value = Column(String(255), nullable=False)
    source_kind = Column(String(40), nullable=False)
    source_ref = Column(String(2048), nullable=False)
    license_state = Column(String(35), nullable=False)
    review_state = Column(String(24), nullable=False, default="PENDING")
    fingerprint = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class CompanyGoldenField(Base):
    """A published company field preserves its winning source observation."""
    __tablename__ = "company_golden_fields"
    __table_args__ = (UniqueConstraint("company_id", "field_name", name="uq_company_golden_field"),)
    id = Column(String(36), primary_key=True, default=uid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    field_name = Column(String(80), nullable=False)
    value = Column(String(255), nullable=False)
    observation_id = Column(String(36), ForeignKey("company_observations.id"), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class CompanyOwnershipClaim(Base):
    """A claimed company remains untrusted pending manual verification."""
    __tablename__ = "company_ownership_claims"
    id = Column(String(36), primary_key=True, default=uid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    claimant_email = Column(String(255), nullable=False)
    claimant_subject = Column(String(255), nullable=True)
    proof_reference = Column(String(1024), nullable=False)
    review_state = Column(String(20), nullable=False, default="PENDING")
    reviewer_reference = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class CompanyMembership(Base):
    """Server-side source of truth: OIDC subject has permissions ONLY after verified claim."""
    __tablename__ = "company_memberships"
    __table_args__ = (UniqueConstraint("company_id", "subject", name="uq_company_member_subject"),)
    id = Column(String(36), primary_key=True, default=uid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    subject = Column(String(255), nullable=False, index=True)
    role = Column(String(20), nullable=False, default="OWNER")
    active = Column(Boolean, nullable=False, default=True)
    verified_claim_id = Column(String(36), ForeignKey("company_ownership_claims.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

class RequestEconomicEvent(Base):
    """Append-only operator-recorded costs and confirmed cash receipts per customer RFQ."""
    __tablename__ = "request_economic_events"
    __table_args__ = (UniqueConstraint("request_id", "event_key", name="uq_request_economic_event"),)
    id = Column(String(36), primary_key=True, default=uid)
    request_id = Column(String(36), ForeignKey("service_requests.id"), nullable=False, index=True)
    event_key = Column(String(128), nullable=False)
    direction = Column(String(10), nullable=False)  # COST or RECEIPT
    category = Column(String(40), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    evidence_reference = Column(String(1024), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
