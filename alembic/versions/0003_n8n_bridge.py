"""n8n reliable MySQL outbox leases and internal review queue.

Revision ID: 0003_n8n
Revises: 0002_economics
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_n8n"
down_revision = "0002_economics"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("outbox_events", sa.Column("attempt_count", sa.Integer(),
                  nullable=False, server_default="0"))
    op.add_column("outbox_events", sa.Column("available_at", sa.DateTime(timezone=True)))
    op.add_column("outbox_events", sa.Column("lease_until", sa.DateTime(timezone=True)))
    op.add_column("outbox_events", sa.Column("lease_token_hash", sa.String(64)))
    op.add_column("outbox_events", sa.Column("completed_at", sa.DateTime(timezone=True)))
    op.add_column("outbox_events", sa.Column("n8n_execution_ref", sa.String(128)))
    op.add_column("outbox_events", sa.Column("last_failure_code", sa.String(48)))
    op.create_index("ix_outbox_claim_scan", "outbox_events",
                    ["status", "available_at", "lease_until"])
    op.create_table(
        "automation_review_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("outbox_event_id", sa.String(36),
                  sa.ForeignKey("outbox_events.id"), nullable=False, unique=True),
        sa.Column("event_type", sa.String(80), nullable=False),
        sa.Column("aggregate_id", sa.String(36), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="OPEN"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

def downgrade():
    op.drop_table("automation_review_tasks")
    op.drop_index("ix_outbox_claim_scan", table_name="outbox_events")
    for col in ("last_failure_code", "n8n_execution_ref", "completed_at",
                "lease_token_hash", "lease_until", "available_at", "attempt_count"):
        op.drop_column("outbox_events", col)
