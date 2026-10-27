"""Evidence-first golden record rules, adapted from TonnEstate's
catalog quality/survivorship approach; independent of its ORM and runtime.

Observation != verified claim != canonical published field.
"""
from __future__ import annotations
import hashlib
import json
import re

FIELDS = {"legal_name", "postal_code", "contact_email", "service_category"}
SOURCES = {"OFFICIAL_REGISTER", "COMPANY_WEBSITE", "PROVIDER_ASSERTION", "THIRD_PARTY_DIRECTORY"}
LICENSE_STATES = {"UNKNOWN", "INTERNAL_ONLY", "PUBLIC_REUSE_APPROVED", "RESTRICTED"}

def normalized_field(field: str, value: str) -> str:
    if field not in FIELDS or not isinstance(value, str):
        raise ValueError("field_not_allowed")
    value = value.strip()
    if not value or len(value) > 255:
        raise ValueError("invalid_field_value")
    if field == "postal_code" and not re.fullmatch(r"\d{5}", value):
        raise ValueError("invalid_postal_code")
    if field == "contact_email" and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise ValueError("invalid_contact_email")
    if field == "service_category" and not re.fullmatch(r"[a-z0-9_-]{3,80}", value):
        raise ValueError("invalid_category")
    return value

def observation_fingerprint(*, field: str, value: str, source_kind: str,
                            source_ref: str) -> str:
    canonical = json.dumps({"field": field, "value": normalized_field(field, value),
                            "source_kind": source_kind, "source_ref": source_ref},
                           sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def publishable(*, license_state: str, review_state: str) -> bool:
    return license_state == "PUBLIC_REUSE_APPROVED" and review_state == "VERIFIED"
