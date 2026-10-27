"""Actual MySQL concurrent outbox lease test. Dedicated disposable CI database only."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import json
import os

from agenqo.database import engine, SessionLocal
from agenqo.models import OutboxEvent, AutomationReviewTask, uid
from agenqo.n8n_bridge import claim_event, complete_event, FinishIn

assert engine.dialect.name == "mysql", "Only run against disposable CI MySQL database"
event_id = uid()
with SessionLocal() as db:
    db.add(OutboxEvent(id=event_id,event_type="booking.confirmed",
                       aggregate_id="mysql-concurrency-test",
                       payload=json.dumps({"booking_id":"mysql-concurrency-test", "request_id":"ci-test-request",
                           "policy":"INTERNAL_REVIEW_ONLY"})))
    db.commit()

barrier=Barrier(2)

def worker(_):
    with SessionLocal() as db:
        barrier.wait(timeout=12)
        return claim_event(db=db)

with ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(worker,range(2)))
claimed=[r["event"] for r in results if r["has_event"]]
assert len(claimed)==1,results
assert claimed[0]["event_id"]==event_id,claimed
with SessionLocal() as db:
    confirmed=complete_event(
        FinishIn(event_id=event_id,lease_token=claimed[0]["lease_token"],
                 execution_ref="n8n:ci-parallel-001"),db=db)
    assert confirmed["status"]=="DONE"
    assert db.query(AutomationReviewTask).filter_by(outbox_event_id=event_id).count()==1
print("PASS: concurrent MySQL n8n claims lease exactly once and persist a single internal task")
