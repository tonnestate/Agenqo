"""Append-only RFQ cost and receipt events.

Revision ID: 0002_economics
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_economics"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "request_economic_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("request_id", sa.String(36),
                  sa.ForeignKey("service_requests.id"), nullable=False),
        sa.Column("event_key", sa.String(128), nullable=False),
        sa.Column("direction", sa.String(10), nullable=False),
        sa.Column("category", sa.String(40), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("evidence_reference", sa.String(1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("request_id", "event_key", name="uq_request_economic_event"),
        sa.CheckConstraint("amount_cents > 0", name="ck_economic_amount_positive"),
        sa.CheckConstraint("direction IN ('COST','RECEIPT')", name="ck_economic_direction"),
    )
    op.create_index("ix_request_economic_events_request_id",
                    "request_economic_events", ["request_id"])

def downgrade():
    op.drop_index("ix_request_economic_events_request_id",table_name="request_economic_events")
    op.drop_table("request_economic_events")
