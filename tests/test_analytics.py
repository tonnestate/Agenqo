from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from agenqo.models import Base, ServiceRequest, Booking, RequestEconomicEvent
from agenqo.analytics import marketplace_liquidity_report

def test_duckdb_analyses_requests_without_new_server():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as db:
        a = ServiceRequest(customer_email="one@example.test", customer_token_hash="a"*64,
                           category="entruempelung", postal_code="20095",
                           requirements="Wohnungsaufloesung 80 qm")
        b = ServiceRequest(customer_email="two@example.test", customer_token_hash="b"*64,
                           category="entruempelung", postal_code="22111",
                           requirements="Entruempelung Dachboden")
        c = ServiceRequest(customer_email="three@example.test", customer_token_hash="c"*64,
                           category="reinigung", postal_code="50667", requirements="Grundreinigung")
        db.add_all([a,b,c])
        db.flush()
        db.add(Booking(request_id=a.id, quote_id="placeholder-test-quote",
                       offer_fingerprint="f"*64, status="PROVIDER_CONFIRMED"))
        db.add_all([
            RequestEconomicEvent(request_id=a.id,event_key="cost:one",direction="COST",
                                  category="ACQUISITION",amount_cents=3000,
                                  evidence_reference="manual-cost-2026-1"),
            RequestEconomicEvent(request_id=b.id,event_key="cost:two",direction="COST",
                                  category="MODEL",amount_cents=500,
                                  evidence_reference="manual-cost-2026-2"),
            RequestEconomicEvent(request_id=a.id,event_key="income:one",direction="RECEIPT",
                                  category="PROVIDER_COMMISSION",amount_cents=7000,
                                  evidence_reference="bank-receipt-2026-1")
        ])
        db.commit()
        report = marketplace_liquidity_report(db)
    engine.dispose()
    assert report["engine"] == "embedded_duckdb_in_memory"
    assert len(report["categories"]) == 2
    ent = next(row for row in report["categories"] if row["category"] == "entruempelung")
    assert ent["requests"] == 2
    assert ent["confirmed_bookings"] == 1
    assert ent["recorded_cost_cents"] == 3500
    assert ent["recorded_receipt_cents"] == 7000
    assert ent["recorded_contribution_cents"] == 3500
    assert ent["conversion_percent"] == 50.0
    assert {row["region_prefix"] for row in report["regions"]} == {"20", "22", "50"}
