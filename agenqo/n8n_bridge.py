"""n8n integration: authenticated pull, MySQL lease, atomic review handoff, retries.

All business state transitions stay inside Agenqo. n8n may convert a durable
outbox event into an INTERNAL review task; this adapter never sends messages
to third parties, books orders, or executes arbitrary workflows.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hmac
import json
import os
from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

from .database import get_db
from .domain import new_token, token_digest
from .models import OutboxEvent, AutomationReviewTask
from .models import AuditEvent

def admin(x_admin_key: str | None = Header(default=None)) -> None:
    """Standalone internal admin authentication; no dependency on the API module."""
    configured = os.getenv("AGENQO_ADMIN_KEY", "")
    if not configured or not x_admin_key or not hmac.compare_digest(configured, x_admin_key):
        raise HTTPException(403, "admin_access_denied")

def audit(db: Session, kind: str, reference: str, actor: str,
          details: dict | None = None) -> None:
    db.add(AuditEvent(kind=kind, reference_id=reference, actor=actor,
                      details=json.dumps(details or {}, sort_keys=True, ensure_ascii=False)))

def aware(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)

router = APIRouter(prefix="/v1")
LEASE_SECONDS = 120
MAX_ATTEMPTS = 5
APPROVED_TYPES = frozenset({
    "invitation.review_requested", "quote.review_requested", "booking.confirmed"
})


def require_n8n_key(x_agenqo_bridge_key: str | None = Header(default=None)) -> None:
    configured = os.getenv("AGENQO_N8N_BRIDGE_KEY", "")
    if len(configured) < 32:
        raise HTTPException(503, "n8n_bridge_not_configured")
    if (not x_agenqo_bridge_key or len(x_agenqo_bridge_key) > 512
            or not hmac.compare_digest(configured, x_agenqo_bridge_key)):
        raise HTTPException(403, "n8n_bridge_access_denied")


def utcnow() -> datetime:
    # Second precision matches MySQL DATETIME(0); do not depend on microseconds.
    return datetime.now(timezone.utc).replace(microsecond=0)


def lease_is_valid(row: OutboxEvent, token: str) -> bool:
    return bool(row.lease_token_hash and token
                and hmac.compare_digest(row.lease_token_hash, token_digest(token)))


class LeaseResult(BaseModel):
    has_event: bool
    event: dict | None = None


class FinishIn(BaseModel):
    event_id: str = Field(min_length=36, max_length=36)
    lease_token: str = Field(min_length=32, max_length=256)
    execution_ref: str = Field(min_length=4, max_length=128)


class FailIn(BaseModel):
    event_id: str = Field(min_length=36, max_length=36)
    lease_token: str = Field(min_length=32, max_length=256)
    error_code: Literal["WORKFLOW_FAILED", "TEMPORARY_FAILURE", "OPERATOR_HOLD"]


class RetryIn(BaseModel):
    reason: str = Field(min_length=12, max_length=255)


@router.post("/integrations/n8n/claim", dependencies=[Depends(require_n8n_key)])
def claim_event(db: Session = Depends(get_db)):
    now = utcnow()
    # Expired fifth lease is dead-lettered. No permanently orphaned leased row.
    stale = (db.query(OutboxEvent)
        .filter(OutboxEvent.status == "LEASED",
                OutboxEvent.lease_until <= now,
                OutboxEvent.attempt_count >= MAX_ATTEMPTS)
        .order_by(OutboxEvent.created_at, OutboxEvent.id)
        .with_for_update(skip_locked=True).limit(20).all())
    for row in stale:
        row.status = "DEAD"
        row.last_failure_code = "LEASE_EXPIRED_MAX_ATTEMPTS"
        row.lease_token_hash = None
        row.lease_until = None
        audit(db, "N8N_OUTBOX_DEAD", row.id, "n8n")
    available = or_(OutboxEvent.available_at.is_(None), OutboxEvent.available_at <= now)
    candidates = or_(
        and_(OutboxEvent.status == "PENDING", available),
        and_(OutboxEvent.status == "LEASED", OutboxEvent.lease_until <= now)
    )
    row = (db.query(OutboxEvent)
        .filter(candidates, OutboxEvent.attempt_count < MAX_ATTEMPTS,
                OutboxEvent.event_type.in_(APPROVED_TYPES))
        .order_by(OutboxEvent.created_at, OutboxEvent.id)
        .with_for_update(skip_locked=True).first())
    if row is None:
        db.commit()
        return {"has_event": False, "event": None}
    lease_token = new_token()
    row.status = "LEASED"
    row.attempt_count = (row.attempt_count or 0) + 1
    row.lease_token_hash = token_digest(lease_token)
    row.lease_until = now + timedelta(seconds=LEASE_SECONDS)
    row.available_at = None
    row.last_failure_code = None
    # Explicit field allowlists: never expose credentials, contact addresses,
    # provider email, free-text RFQ, or unexpected future business fields.
    payload = json.loads(row.payload)
    fields = {
        "invitation.review_requested": ("invitation_id", "request_id", "company_id"),
        "quote.review_requested": ("quote_id", "request_id"),
        "booking.confirmed": ("booking_id", "request_id"),
    }[row.event_type]
    id_field = fields[0]
    is_legacy = row.event_type == "booking.confirmed" and isinstance(payload, dict) and "policy" not in payload
    valid = (
        isinstance(payload, dict)
        and set(payload).issubset(set(fields) | {"policy"})
        and all(isinstance(payload.get(field), str) and 1 <= len(payload[field]) <= 80
                for field in fields)
        and payload.get(id_field) == row.aggregate_id
        and (payload.get("policy") == "INTERNAL_REVIEW_ONLY" or is_legacy)
    )
    if not valid:
        row.status = "DEAD"
        row.last_failure_code = "INVALID_EVENT_POLICY"
        row.lease_until = None
        row.lease_token_hash = None
        audit(db, "N8N_OUTBOX_REJECTED", row.id, "n8n")
        db.commit()
        return {"has_event": False, "event": None}
    sanitized_payload = {field: payload[field] for field in fields}
    sanitized_payload["policy"] = "INTERNAL_REVIEW_ONLY"
    safe = {
        "event_id": row.id, "type": row.event_type,
        "aggregate_id": row.aggregate_id, "attempt": row.attempt_count,
        "lease_token": lease_token, "lease_seconds": LEASE_SECONDS,
        "payload": sanitized_payload,
    }
    audit(db, "N8N_EVENT_LEASED", row.id, "n8n",
          {"attempt": row.attempt_count})
    db.commit()
    return {"has_event": True, "event": safe}


@router.post("/integrations/n8n/complete", dependencies=[Depends(require_n8n_key)])
def complete_event(payload: FinishIn, db: Session = Depends(get_db)):
    row = (db.query(OutboxEvent)
           .filter_by(id=payload.event_id)
           .with_for_update().populate_existing().one_or_none())
    if not row:
        raise HTTPException(404, "event_not_found")
    if not lease_is_valid(row, payload.lease_token):
        raise HTTPException(403, "invalid_event_lease")
    if row.status == "DONE":
        if row.n8n_execution_ref == payload.execution_ref:
            return {"event_id": row.id, "status": row.status, "idempotent_replay": True}
        raise HTTPException(409, "completion_execution_mismatch")
    if row.status != "LEASED" or row.lease_until is None or aware(row.lease_until) <= utcnow():
        raise HTTPException(409, "lease_not_active")
    if row.event_type not in APPROVED_TYPES:
        raise HTTPException(409, "event_type_not_allowed")
    existing = db.query(AutomationReviewTask).filter_by(outbox_event_id=row.id).one_or_none()
    if existing is None:
        task = AutomationReviewTask(
            outbox_event_id=row.id, event_type=row.event_type,
            aggregate_id=row.aggregate_id)
        db.add(task)
    row.status = "DONE"
    row.completed_at = utcnow()
    row.n8n_execution_ref = payload.execution_ref
    row.lease_until = None
    audit(db, "N8N_INTERNAL_REVIEW_CREATED", row.id, "n8n",
          {"execution_ref": payload.execution_ref})
    db.commit()
    return {"event_id": row.id, "status": row.status,
            "action": "INTERNAL_REVIEW_TASK_CREATED", "idempotent_replay": False}


@router.post("/integrations/n8n/fail", dependencies=[Depends(require_n8n_key)])
def fail_event(payload: FailIn, db: Session = Depends(get_db)):
    row = (db.query(OutboxEvent).filter_by(id=payload.event_id)
           .with_for_update().populate_existing().one_or_none())
    if not row:
        raise HTTPException(404, "event_not_found")
    if not lease_is_valid(row, payload.lease_token):
        raise HTTPException(403, "invalid_event_lease")
    if row.status != "LEASED" or row.lease_until is None or aware(row.lease_until) <= utcnow():
        raise HTTPException(409, "lease_not_active")
    row.status = "DEAD" if row.attempt_count >= MAX_ATTEMPTS else "PENDING"
    row.available_at = (None if row.status == "DEAD"
                       else utcnow() + timedelta(seconds=min(60 * (2 ** (row.attempt_count - 1)), 3600)))
    row.lease_until = None
    row.lease_token_hash = None
    row.last_failure_code = payload.error_code
    audit(db, "N8N_EVENT_RETRY_SCHEDULED" if row.status == "PENDING" else "N8N_OUTBOX_DEAD",
          row.id, "n8n", {"attempt": row.attempt_count, "code": payload.error_code})
    db.commit()
    return {"event_id": row.id, "status": row.status, "attempt_count": row.attempt_count}


@router.get("/admin/automation/status", dependencies=[Depends(admin)])
def automation_status(db: Session = Depends(get_db)):
    stats = db.query(OutboxEvent.status, func.count(OutboxEvent.id)).group_by(OutboxEvent.status).all()
    open_tasks = db.query(AutomationReviewTask).filter_by(status="OPEN").count()
    return {"outbox": {status: count for status, count in stats},
            "open_review_tasks": open_tasks, "external_messages_sent": 0,
            "integration_mode": "INTERNAL_REVIEW_ONLY"}


@router.get("/admin/automation/review-tasks", dependencies=[Depends(admin)])
def list_automation_tasks(db: Session = Depends(get_db)):
    tasks = (db.query(AutomationReviewTask)
             .order_by(AutomationReviewTask.created_at.desc()).limit(100).all())
    return {"tasks": [{"task_id": t.id, "outbox_event_id": t.outbox_event_id,
                       "event_type": t.event_type, "aggregate_id": t.aggregate_id,
                       "status": t.status} for t in tasks]}


@router.post("/admin/automation/events/{event_id}/retry",
             dependencies=[Depends(admin)])
def manual_retry(event_id: str, body: RetryIn, db: Session = Depends(get_db)):
    row = (db.query(OutboxEvent).filter_by(id=event_id)
           .with_for_update().populate_existing().one_or_none())
    if not row:
        raise HTTPException(404, "event_not_found")
    if row.status != "DEAD" or row.event_type not in APPROVED_TYPES:
        raise HTTPException(409, "only_dead_allowed_events_can_be_retried")
    row.status = "PENDING"
    row.attempt_count = 0
    row.available_at = None
    row.lease_until = None
    row.lease_token_hash = None
    row.last_failure_code = None
    audit(db, "N8N_DEAD_EVENT_REQUEUED", row.id, "admin",
          {"review_reason": body.reason})
    db.commit()
    return {"event_id": row.id, "status": row.status}
