"""Deterministic, fail-closed contact policy; no communications are sent here.

A documented RFQ is NOT sufficient evidence to send commercial email to an
unregistered company. The pilot accepts only recorded, reviewed supplier
permissions for the exact channel, purpose and destination. Legal assessments
remain outside the software and must precede external sending.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib

POLICY_VERSION = "CONTACT_V1_OPT_IN_ONLY"
RFQ_EMAIL = "EMAIL"
RFQ_PURPOSE = "RFQ_INVITATION"
EVIDENCE_SIGNED = "SIGNED_PILOT_AGREEMENT"
DENIAL_NO_PERMISSION = "NO_RECORDED_OPT_IN"
DENIAL_OPT_OUT = "OPTED_OUT"
DENIAL_EMAIL_CHANGED = "RECIPIENT_CHANGED"
DENIAL_STATE = "INVITATION_NOT_READY"
DENIAL_EXPIRED = "INVITATION_EXPIRED"
DENIAL_CATEGORY = "CATEGORY_MISMATCH"
DENIAL_REQUEST = "REQUEST_NOT_QUALIFIED"
ALLOW = "RECORDED_OPT_IN"


def destination_digest(email: str) -> str:
    """Bind a supplier permission to a specific normalized destination."""
    return hashlib.sha256(email.strip().casefold().encode("utf-8")).hexdigest()


def utc_aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class ContactVerdict:
    decision: str
    reason_code: str


def evaluate_rfq_email(
    *,
    permission_enabled: bool | None,
    permission_destination_digest: str | None,
    destination_email: str,
    request_category: str,
    provider_category: str,
    request_status: str,
    invitation_status: str,
    invitation_expires_at: datetime,
    at: datetime | None = None,
) -> ContactVerdict:
    """Re-evaluate on EVERY preflight; a past ALLOW is never a send permit."""
    at = at or datetime.now(timezone.utc)
    if invitation_status != "READY":
        return ContactVerdict("DENY", DENIAL_STATE)
    if utc_aware(invitation_expires_at) <= utc_aware(at):
        return ContactVerdict("DENY", DENIAL_EXPIRED)
    if request_status not in {"QUALIFIED", "INVITING", "COLLECTING", "QUOTES_READY"}:
        return ContactVerdict("DENY", DENIAL_REQUEST)
    if request_category != provider_category:
        return ContactVerdict("DENY", DENIAL_CATEGORY)
    if permission_enabled is None:
        return ContactVerdict("DENY", DENIAL_NO_PERMISSION)
    if not permission_enabled:
        return ContactVerdict("DENY", DENIAL_OPT_OUT)
    if not permission_destination_digest or (
        permission_destination_digest != destination_digest(destination_email)
    ):
        return ContactVerdict("DENY", DENIAL_EMAIL_CHANGED)
    return ContactVerdict("ALLOW", ALLOW)
