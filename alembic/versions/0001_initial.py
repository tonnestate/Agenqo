"""Initial Agenqo transaction, evidence and provider-identity schema.

Revision ID: 0001_initial
Revises: None
This revision is frozen: edit schema in future migrations only.
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def pk():
    return sa.Column("id", sa.String(36), primary_key=True)

def created():
    return sa.Column("created_at", sa.DateTime(timezone=True), nullable=False)

def ref(name, table):
    return sa.Column(name, sa.String(36), sa.ForeignKey(table + ".id"), nullable=False)

def upgrade():
    op.create_table("companies",
        pk(), sa.Column("legal_name",sa.String(255),nullable=False),
        sa.Column("postal_code",sa.String(5),nullable=False),
        sa.Column("service_category",sa.String(80),nullable=False),
        sa.Column("contact_email",sa.String(255),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        sa.Column("commission_rate_percent",sa.Numeric(5,2)),
        sa.Column("commission_min_cents",sa.Integer(),nullable=False),
        sa.Column("commission_agreement_reference",sa.String(255)),
        created())

    op.create_table("service_requests",
        pk(), sa.Column("customer_email",sa.String(255),nullable=False),
        sa.Column("customer_token_hash",sa.String(64),nullable=False),
        sa.Column("category",sa.String(80),nullable=False),
        sa.Column("postal_code",sa.String(5),nullable=False),
        sa.Column("requirements",sa.Text(),nullable=False),
        sa.Column("structured_requirements_json",sa.Text(),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        created())

    op.create_table("audit_events",
        pk(),sa.Column("kind",sa.String(100),nullable=False),
        sa.Column("reference_id",sa.String(36),nullable=False),
        sa.Column("actor",sa.String(32),nullable=False),
        sa.Column("details",sa.Text(),nullable=False),
        created())

    op.create_table("outbox_events",
        pk(),sa.Column("event_type",sa.String(80),nullable=False),
        sa.Column("aggregate_id",sa.String(36),nullable=False),
        sa.Column("payload",sa.Text(),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        created(),
        sa.UniqueConstraint("event_type","aggregate_id",name="uq_outbox_event_kind"))

    op.create_table("company_ownership_claims",
        pk(),ref("company_id","companies"),
        sa.Column("claimant_email",sa.String(255),nullable=False),
        sa.Column("claimant_subject",sa.String(255)),
        sa.Column("proof_reference",sa.String(1024),nullable=False),
        sa.Column("review_state",sa.String(20),nullable=False),
        sa.Column("reviewer_reference",sa.String(255)),
        created())
    op.create_index("ix_company_ownership_claims_company_id","company_ownership_claims",["company_id"])

    op.create_table("company_observations",
        pk(),ref("company_id","companies"),
        sa.Column("field_name",sa.String(80),nullable=False),
        sa.Column("value",sa.String(255),nullable=False),
        sa.Column("source_kind",sa.String(40),nullable=False),
        sa.Column("source_ref",sa.String(2048),nullable=False),
        sa.Column("license_state",sa.String(35),nullable=False),
        sa.Column("review_state",sa.String(24),nullable=False),
        sa.Column("fingerprint",sa.String(64),nullable=False),
        created(),sa.UniqueConstraint("company_id","fingerprint",name="uq_company_observation"))
    op.create_index("ix_company_observations_company_id","company_observations",["company_id"])

    op.create_table("company_golden_fields",
        pk(),ref("company_id","companies"),
        sa.Column("field_name",sa.String(80),nullable=False),
        sa.Column("value",sa.String(255),nullable=False),
        ref("observation_id","company_observations"),
        sa.Column("published_at",sa.DateTime(timezone=True),nullable=False),
        sa.UniqueConstraint("company_id","field_name",name="uq_company_golden_field"))
    op.create_index("ix_company_golden_fields_company_id","company_golden_fields",["company_id"])

    op.create_table("company_memberships",
        pk(),ref("company_id","companies"),
        sa.Column("subject",sa.String(255),nullable=False),
        sa.Column("role",sa.String(20),nullable=False),
        sa.Column("active",sa.Boolean(),nullable=False),
        ref("verified_claim_id","company_ownership_claims"),
        created(),sa.UniqueConstraint("company_id","subject",name="uq_company_member_subject"))
    op.create_index("ix_company_memberships_company_id","company_memberships",["company_id"])
    op.create_index("ix_company_memberships_subject","company_memberships",["subject"])

    op.create_table("invitations",
        pk(),ref("request_id","service_requests"),ref("company_id","companies"),
        sa.Column("token_hash",sa.String(64),nullable=False,unique=True),
        sa.Column("status",sa.String(32),nullable=False),
        sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),
        created(),sa.UniqueConstraint("request_id","company_id",name="uq_invitation_request_company"))
    op.create_index("ix_invitations_request_id","invitations",["request_id"])
    op.create_index("ix_invitations_company_id","invitations",["company_id"])

    op.create_table("quotes",
        pk(),ref("invitation_id","invitations"),
        sa.Column("revision",sa.Integer(),nullable=False),
        sa.Column("description",sa.Text(),nullable=False),
        sa.Column("conditions",sa.Text(),nullable=False),
        sa.Column("net_cents",sa.Integer(),nullable=False),
        sa.Column("gross_cents",sa.Integer(),nullable=False),
        sa.Column("vat_percent",sa.Numeric(5,2),nullable=False),
        sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("binding_declared_by_provider",sa.Boolean(),nullable=False),
        sa.Column("service_attributes_json",sa.Text(),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        sa.Column("fingerprint",sa.String(64),nullable=False),
        created(),sa.UniqueConstraint("invitation_id",name="uq_quote_invitation"))

    op.create_table("bookings",
        pk(),ref("request_id","service_requests"),ref("quote_id","quotes"),
        sa.Column("offer_fingerprint",sa.String(64),nullable=False),
        sa.Column("commission_agreement_reference",sa.String(255)),
        sa.Column("commission_rate_percent",sa.Numeric(5,2)),
        sa.Column("commission_min_cents",sa.Integer(),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        sa.Column("completion_evidence",sa.Text()),
        created(),
        sa.UniqueConstraint("request_id",name="uq_booking_request"),
        sa.UniqueConstraint("quote_id",name="uq_booking_quote"))

    op.create_table("commission_events",
        pk(),ref("booking_id","bookings"),
        sa.Column("agreement_reference",sa.String(255),nullable=False),
        sa.Column("net_cents",sa.Integer(),nullable=False),
        sa.Column("status",sa.String(32),nullable=False),
        created(),sa.UniqueConstraint("booking_id",name="uq_commission_booking"))

def downgrade():
    # Development-only destructive downgrade, never run against production records.
    for idx in ("commission_events","bookings","quotes","invitations",
                "company_memberships","company_golden_fields","company_observations",
                "company_ownership_claims","outbox_events","audit_events",
                "service_requests","companies"):
        op.drop_table(idx)
