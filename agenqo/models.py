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
    id = Column(String(36), primary_key=True, default=uid)
    event_type = Column(String(80), nullable=False)
    aggregate_id = Column(String(36), nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
