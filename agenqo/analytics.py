"""Embedded DuckDB analytics on de-identified slices from existing MySQL.

DuckDB is NOT a transaction store, deployed service, or secondary system of record.
No installing extensions, network calls, direct writes, persistent database file,
or exporting addresses/contact details. The caller needs a read-only DB session.
"""
from collections import defaultdict

def marketplace_liquidity_report(db):
    try:
        import duckdb
    except ImportError as exc:
        raise RuntimeError("DuckDB analytics not installed; install agenqo[analytics]") from exc

    from .models import Booking, RequestEconomicEvent, ServiceRequest

    requests = db.query(ServiceRequest.id, ServiceRequest.category,
                        ServiceRequest.postal_code).all()
    bookings = {request_id: status for request_id, status in
                db.query(Booking.request_id, Booking.status).all()}
    costs = defaultdict(int)
    receipts = defaultdict(int)
    for request_id, direction, amount in db.query(
            RequestEconomicEvent.request_id, RequestEconomicEvent.direction,
            RequestEconomicEvent.amount_cents).all():
        if direction == "COST":
            costs[request_id] += amount
        else:
            receipts[request_id] += amount

    # Only service and coarse postal prefix; never names, tokens, addresses, or raw requests.
    rows = [
        (category, str(postal_code)[:2],
         int(bookings.get(request_id) in {"PROVIDER_CONFIRMED", "COMPLETED", "DISPUTED"}),
         costs[request_id], receipts[request_id])
        for request_id, category, postal_code in requests
    ]
    with duckdb.connect(":memory:") as analytics:
        analytics.execute("""CREATE TABLE inquiries(
            service_category VARCHAR,
            region_prefix VARCHAR,
            confirmed_bookings INTEGER,
            cost_cents BIGINT,
            receipt_cents BIGINT)""")
        if rows:
            analytics.executemany("INSERT INTO inquiries VALUES (?,?,?,?,?)", rows)
        result = analytics.execute("""
            SELECT service_category,
                   COUNT(*) AS requests,
                   COALESCE(SUM(confirmed_bookings), 0) AS confirmed_bookings,
                   COALESCE(SUM(cost_cents), 0) AS recorded_cost_cents,
                   COALESCE(SUM(receipt_cents), 0) AS recorded_receipt_cents,
                   COALESCE(SUM(receipt_cents-cost_cents), 0) AS recorded_contribution_cents,
                   ROUND(100.0*SUM(confirmed_bookings)/COUNT(*),2) AS conversion_percent
            FROM inquiries
            GROUP BY service_category
            ORDER BY requests DESC, service_category
        """).fetchall()
        regions = analytics.execute("""
            SELECT region_prefix, COUNT(*) AS requests,
                   COALESCE(SUM(confirmed_bookings),0) AS confirmed_bookings
            FROM inquiries GROUP BY region_prefix ORDER BY requests DESC, region_prefix
        """).fetchall()
    return {
        "source": "existing_mysql_or_test_sqlite",
        "engine": "embedded_duckdb_in_memory",
        "data_scope": "service categories and 2-digit postal regions; no customer/provider personal details",
        "categories": [
            {"category":a, "requests":int(b), "confirmed_bookings":int(c),
             "recorded_cost_cents":int(d), "recorded_receipt_cents":int(e),
             "recorded_contribution_cents":int(f), "conversion_percent":float(g)}
            for a,b,c,d,e,f,g in result],
        "regions": [{"region_prefix":a, "requests":int(b), "confirmed_bookings":int(c)}
                    for a,b,c in regions],
        "warning": "Only operator-recorded costs and receipts; not audited income or profit."
    }
