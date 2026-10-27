"""Deterministic business domain: no LLMs, network calls or database dependencies."""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import hashlib
import hmac
import json
import secrets

class RuleViolation(ValueError):
    pass

# Each state change explicitly identifies its permitted actor.
TRANSITIONS = {
    "request": {
        "DRAFT": {"QUALIFIED": {"admin"}, "CANCELLED": {"admin"}},
        "QUALIFIED": {"INVITING": {"admin"}, "CANCELLED": {"admin"}},
        "INVITING": {"COLLECTING": {"provider"}, "CANCELLED": {"admin"}},
        "COLLECTING": {"QUOTES_READY": {"admin"}, "CANCELLED": {"admin"}},
        "QUOTES_READY": {"APPROVAL_PENDING": {"customer"}, "COLLECTING": {"admin"}, "CANCELLED": {"admin"}},
        "APPROVAL_PENDING": {"BOOKED": {"provider"}, "CANCELLED": {"admin"}},
        "BOOKED": {"COMPLETED": {"admin"}, "DISPUTED": {"admin"}, "CANCELLED": {"admin"}},
        "DISPUTED": {"COMPLETED": {"admin"}, "CANCELLED": {"admin"}},
    },
    "invitation": {
        "READY": {"RESPONDED": {"provider"}, "EXPIRED": {"admin"}, "CANCELLED": {"admin"}},
        "RESPONDED": {"EXPIRED": {"admin"}, "CANCELLED": {"admin"}},
    },
    "quote": {
        "SUBMITTED": {"BINDING": {"admin"}, "CONDITIONAL": {"admin"}, "WITHDRAWN": {"provider"}},
        "BINDING": {"ACCEPTED": {"customer"}, "EXPIRED": {"admin"}, "WITHDRAWN": {"provider"}},
        "CONDITIONAL": {"BINDING": {"admin"}, "WITHDRAWN": {"provider"}},
    },
    "booking": {
        "CUSTOMER_APPROVED": {"PROVIDER_CONFIRMED": {"provider"}, "CANCELLED": {"admin"}},
        "PROVIDER_CONFIRMED": {"COMPLETED": {"admin"}, "DISPUTED": {"admin"}, "CANCELLED": {"admin"}},
        "DISPUTED": {"COMPLETED": {"admin"}, "CANCELLED": {"admin"}},
    },
    "commission": {"ELIGIBLE": {"INVOICED": {"admin"}, "VOID": {"admin"}},
                   "INVOICED": {"PAID": {"admin"}, "VOID": {"admin"}}},
}

def move(kind: str, current: str, target: str, actor: str) -> str:
    if actor not in TRANSITIONS.get(kind, {}).get(current, {}).get(target, set()):
        raise RuleViolation(f"forbidden_transition:{kind}:{current}:{target}:{actor}")
    return target

def cents(value: Decimal | str) -> int:
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            raise RuleViolation("invalid_amount")
        result = (amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        if result > 2_147_483_647:
            raise RuleViolation("amount_out_of_range")
        return int(result)
    except (InvalidOperation, ValueError) as exc:
        raise RuleViolation("invalid_amount") from exc

def gross_cents(net_cents: int, vat_percent: Decimal | str) -> int:
    rate = Decimal(str(vat_percent))
    if net_cents < 0 or not rate.is_finite() or not (Decimal("0") <= rate <= Decimal("100")):
        raise RuleViolation("invalid_vat_rate")
    return int((Decimal(net_cents) * (1 + rate / 100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def commission_cents(net_cents: int, rate_percent: Decimal | str, minimum_cents: int = 0) -> int:
    rate = Decimal(str(rate_percent))
    if net_cents < 0 or minimum_cents < 0 or not rate.is_finite() or not (0 <= rate <= 100):
        raise RuleViolation("invalid_commission_rule")
    return max(minimum_cents, int((Decimal(net_cents) * rate / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)))

def offer_fingerprint(*, quote_id: str, revision: int, description: str, conditions: str,
                      net_cents: int, gross_cents_value: int, vat_percent: str, expires_at: datetime) -> str:
    if expires_at.tzinfo is None:
        raise RuleViolation("expiry_timezone_required")
    canonical = {"quote_id": quote_id, "revision": revision, "description": description,
                 "conditions": conditions, "net_cents": net_cents, "gross_cents": gross_cents_value,
                 "vat_percent": vat_percent, "expires_at": expires_at.astimezone(timezone.utc).isoformat()}
    data = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def new_token() -> str:
    return secrets.token_urlsafe(32)

def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def token_matches(candidate: str, stored_sha256: str) -> bool:
    return hmac.compare_digest(token_digest(candidate), stored_sha256)

def require_valid_offer(status: str, expires_at: datetime, expected_hash: str, current_hash: str) -> None:
    if status != "BINDING":
        raise RuleViolation("offer_not_binding")
    expiry = expires_at if expires_at.tzinfo else expires_at.replace(tzinfo=timezone.utc)
    if expiry <= datetime.now(timezone.utc):
        raise RuleViolation("offer_expired")
    if not hmac.compare_digest(expected_hash, current_hash):
        raise RuleViolation("offer_changed")
