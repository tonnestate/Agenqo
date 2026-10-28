"""Append-only, channel-specific supplier permissions and preflight decisions.

Revision ID: 0004_contact_policy
Revises: 0003_n8n
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_contact_policy"
down_revision = "0003_n8n"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "provider_contact_permissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("company_id", sa.String(36),
                  sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("purpose", sa.String(40), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("destination_hash", sa.String(64), nullable=False),
        sa.Column("evidence_kind", sa.String(40), nullable=False),
        sa.Column("evidence_reference", sa.String(1024), nullable=False),
        sa.Column("reviewer_reference", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("company_id", "channel", "purpose", "revision",
                            name="uq_contact_permission_revision"),
    )
    op.create_index("ix_provider_contact_permissions_company_id",
                    "provider_contact_permissions", ["company_id"])
    op.create_table(
        "contact_policy_decisions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("invitation_id", sa.String(36),
                  sa.ForeignKey("invitations.id"), nullable=False),
        sa.Column("request_id", sa.String(36),
                  sa.ForeignKey("service_requests.id"), nullable=False),
        sa.Column("company_id", sa.String(36),
                  sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("permission_id", sa.String(36),
                  sa.ForeignKey("provider_contact_permissions.id")),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("purpose", sa.String(40), nullable=False),
        sa.Column("policy_version", sa.String(50), nullable=False),
        sa.Column("decision", sa.String(10), nullable=False),
        sa.Column("reason_code", sa.String(48), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_contact_policy_decisions_invitation_id",
                    "contact_policy_decisions", ["invitation_id"])


def downgrade():
    op.drop_index("ix_contact_policy_decisions_invitation_id",
                  table_name="contact_policy_decisions")
    op.drop_table("contact_policy_decisions")
    op.drop_index("ix_provider_contact_permissions_company_id",
                  table_name="provider_contact_permissions")
    op.drop_table("provider_contact_permissions")
