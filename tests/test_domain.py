from datetime import datetime, timedelta, timezone
from decimal import Decimal
import pytest
from agenqo.domain import (RuleViolation, cents, gross_cents, commission_cents,
                           move, offer_fingerprint, new_token, token_digest, token_matches,
                           require_valid_offer)

def test_money_and_commission():
    assert cents("1500.00") == 150000
    assert gross_cents(126050, "19") == 150000
    assert commission_cents(126050, "8", 4000) == 10084
    assert commission_cents(20000, "8", 4000) == 4000
    assert cents(Decimal("2.225")) == 223
    with pytest.raises(RuleViolation):
        cents("-1")
    with pytest.raises(RuleViolation):
        gross_cents(100, "-10")
    with pytest.raises(RuleViolation):
        commission_cents(100, "NaN")

def test_transitions_are_actor_scoped():
    assert move("request", "DRAFT", "QUALIFIED", "admin") == "QUALIFIED"
    with pytest.raises(RuleViolation):
        move("request", "DRAFT", "QUALIFIED", "provider")
    with pytest.raises(RuleViolation):
        move("booking", "CUSTOMER_APPROVED", "COMPLETED", "admin")
    with pytest.raises(RuleViolation):
        move("booking", "PROVIDER_CONFIRMED", "COMPLETED", "customer")
    with pytest.raises(RuleViolation):
        move("request", "BOOKED", "COMPLETED", "provider")

def test_fingerprint_and_token():
    token = new_token()
    assert len(token) >= 32
    assert token_matches(token, token_digest(token))
    assert not token_matches("altered", token_digest(token))
    expiry = datetime.now(timezone.utc) + timedelta(days=1)
    args = dict(quote_id="quote-1", revision=1, description="Wohnung", conditions="",
                net_cents=50000, gross_cents_value=59500, vat_percent="19.00", expires_at=expiry)
    digest = offer_fingerprint(**args)
    assert digest == offer_fingerprint(**args)
    with pytest.raises(RuleViolation):
        require_valid_offer("SUBMITTED", expiry, digest, digest)
    with pytest.raises(RuleViolation):
        require_valid_offer("BINDING", expiry, "0" * 64, digest)
    require_valid_offer("BINDING", expiry, digest, digest)
    assert offer_fingerprint(**(args | {"net_cents": 50001})) != digest


def test_fingerprint_is_stable_across_mysql_datetime_second_precision():
    # MySQL's default DATETIME precision is seconds. SQLite retains fractions.
    # The same actual offer must not become invalid after a MySQL round-trip.
    from datetime import datetime, timedelta, timezone
    expiry = datetime.now(timezone.utc) + timedelta(days=2)
    details = dict(quote_id="q-mysql", revision=1, description="Raeumung",
                   conditions="Besenrein", net_cents=100000, gross_cents_value=119000,
                   vat_percent="19.00")
    digest = offer_fingerprint(**details, expires_at=expiry)
    assert digest == offer_fingerprint(**details,
        expires_at=expiry.replace(microsecond=0))
    assert digest != offer_fingerprint(**details,
        expires_at=expiry + timedelta(seconds=1))
