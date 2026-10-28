"""Admin-only RFQ contact permissions and auditable send preflight.

The API never sends mail. A positive preflight is a point-in-time assessment,
NOT an evergreen token. Any future dispatcher must re-evaluate immediately
before sending, in the same controlled workflow, including opt-out state.
"""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .contact_policy import (
    POLICY_VERSION, RFQ_EMAIL, RFQ_PURPOSE, EVIDENCE_SIGNED,
    destination_digest, evaluate_rfq_email,
)
from .domain import token_digest, token_matches
from .database import get_db
from .models import (
    Company, ServiceRequest, Invitation,
    ProviderContactPermission, ContactPolicyDecision,
)
from .n8n_bridge import admin, audit

router = APIRouter(prefix="/v1/admin", tags=["provider-contact-policy"],
                   dependencies=[Depends(admin)])


class PermissionUpdate(BaseModel):
    enabled: bool
    evidence_kind: Literal[
        "SIGNED_PILOT_AGREEMENT", "PROVIDER_OPTOUT_REQUEST", "OPERATOR_HOLD"
    ]
    evidence_reference: str = Field(min_length=8, max_length=1024)
    reviewer_reference: str = Field(min_length=8, max_length=255)


def latest_permission(db: Session, company_id: str) -> ProviderContactPermission | None:
    return (
        db.query(ProviderContactPermission)
        .filter_by(company_id=company_id, channel=RFQ_EMAIL, purpose=RFQ_PURPOSE)
        .order_by(ProviderContactPermission.revision.desc())
        .first()
    )


@router.post("/companies/{company_id}/contact-permissions", status_code=201)
def update_permission(
    company_id: str, payload: PermissionUpdate,
    db: Session = Depends(get_db),
):
    # Serialize concurrent decisions per company, including MySQL/InnoDB writes.
    company = (
        db.query(Company).filter_by(id=company_id)
        .with_for_update().populate_existing().one_or_none()
    )
    if company is None:
        raise HTTPException(404, "company_not_found")
    if payload.enabled and payload.evidence_kind != EVIDENCE_SIGNED:
        raise HTTPException(422, "opt_in_requires_signed_pilot_agreement_evidence")
    if not payload.enabled and payload.evidence_kind == EVIDENCE_SIGNED:
        raise HTTPException(422, "opt_out_requires_revocation_evidence")
    previous = latest_permission(db, company_id)
    dest_hash = destination_digest(company.contact_email)
    # Opt-out revokes the prior proof. Re-activation requires new evidence,
    # not reusing a signed document that predates the provider's withdrawal.
    if payload.enabled and previous is not None and not previous.enabled:
        reused = (db.query(ProviderContactPermission)
                  .filter_by(company_id=company_id, channel=RFQ_EMAIL,
                             purpose=RFQ_PURPOSE, enabled=True,
                             evidence_reference=payload.evidence_reference)
                  .first())
        if reused is not None:
            raise HTTPException(409, "fresh_opt_in_evidence_required_after_opt_out")
    if (
        previous is not None
        and previous.enabled == payload.enabled
        and previous.destination_hash == dest_hash
        and previous.evidence_kind == payload.evidence_kind
        and previous.evidence_reference == payload.evidence_reference
        and previous.reviewer_reference == payload.reviewer_reference
    ):
        return {
            "permission_id": previous.id,
            "revision": previous.revision,
            "enabled": previous.enabled,
            "idempotent_replay": True,
        }
    row = ProviderContactPermission(
        company_id=company_id, channel=RFQ_EMAIL, purpose=RFQ_PURPOSE,
        revision=(previous.revision + 1 if previous else 1),
        enabled=payload.enabled, destination_hash=dest_hash,
        evidence_kind=payload.evidence_kind,
        evidence_reference=payload.evidence_reference,
        reviewer_reference=payload.reviewer_reference,
    )
    db.add(row)
    db.flush()
    audit(db, "CONTACT_PERMISSION_RECORDED", row.id, "admin", {
        "company_id": company_id, "revision": row.revision,
        "channel": RFQ_EMAIL, "purpose": RFQ_PURPOSE, "enabled": payload.enabled,
        "evidence_kind": payload.evidence_kind,
        # No addresses or evidence URLs in general-purpose audit logs.
    })
    db.commit()
    return {
        "permission_id": row.id, "revision": row.revision,
        "enabled": row.enabled, "idempotent_replay": False,
    }


@router.get("/companies/{company_id}/contact-permissions")
def permission_history(company_id: str, db: Session = Depends(get_db)):
    if db.get(Company, company_id) is None:
        raise HTTPException(404, "company_not_found")
    records = (
        db.query(ProviderContactPermission)
        .filter_by(company_id=company_id, channel=RFQ_EMAIL, purpose=RFQ_PURPOSE)
        .order_by(ProviderContactPermission.revision.desc()).limit(100).all()
    )
    return {
        "company_id": company_id, "channel": RFQ_EMAIL, "purpose": RFQ_PURPOSE,
        "history": [
            {"permission_id": r.id, "revision": r.revision, "enabled": r.enabled,
             "evidence_kind": r.evidence_kind, "reviewer_reference": r.reviewer_reference,
             "created_at": r.created_at.isoformat()}
            for r in records
        ],
    }


@router.post("/invitations/{invitation_id}/contact-preflight")
def preflight_invitation(invitation_id: str, db: Session = Depends(get_db)):
    invitation = (
        db.query(Invitation).filter_by(id=invitation_id)
        .with_for_update().populate_existing().one_or_none()
    )
    if invitation is None:
        raise HTTPException(404, "invitation_not_found")
    company = (db.query(Company).filter_by(id=invitation.company_id)
               .with_for_update().populate_existing().one_or_none())
    request = db.get(ServiceRequest, invitation.request_id)
    if not company or not request:
        raise HTTPException(409, "invitation_data_incomplete")
    permission = latest_permission(db, invitation.company_id)
    verdict = evaluate_rfq_email(
        permission_enabled=permission.enabled if permission else None,
        permission_destination_digest=permission.destination_hash if permission else None,
        destination_email=company.contact_email,
        request_category=request.category,
        provider_category=company.service_category,
        request_status=request.status,
        invitation_status=invitation.status,
        invitation_expires_at=invitation.expires_at,
    )
    record = ContactPolicyDecision(
        invitation_id=invitation.id, company_id=company.id,
        request_id=request.id, permission_id=permission.id if permission else None,
        channel=RFQ_EMAIL, purpose=RFQ_PURPOSE,
        policy_version=POLICY_VERSION,
        decision=verdict.decision, reason_code=verdict.reason_code,
    )
    db.add(record)
    db.flush()
    audit(db, "CONTACT_PREFLIGHT_EVALUATED", record.id, "admin", {
        "invitation_id": invitation.id, "decision": verdict.decision,
        "reason_code": verdict.reason_code, "policy_version": POLICY_VERSION,
    })
    db.commit()
    return {
        "decision_id": record.id, "invitation_id": invitation.id,
        "decision": verdict.decision, "reason_code": verdict.reason_code,
        "policy_version": POLICY_VERSION, "channel": RFQ_EMAIL,
        "purpose": RFQ_PURPOSE,
        "external_delivery_performed": False,
        "warning": "Preflight only. Recheck policy and opt-out immediately before actual delivery.",
    }


@router.get("/invitations/{invitation_id}/contact-decisions")
def decision_history(invitation_id: str, db: Session = Depends(get_db)):
    if db.get(Invitation, invitation_id) is None:
        raise HTTPException(404, "invitation_not_found")
    records = (
        db.query(ContactPolicyDecision).filter_by(invitation_id=invitation_id)
        .order_by(ContactPolicyDecision.created_at.desc(),
                  ContactPolicyDecision.id.desc()).limit(100).all()
    )
    return {
        "invitation_id": invitation_id,
        "decisions": [
            {"decision_id": r.id, "decision": r.decision, "reason_code": r.reason_code,
             "policy_version": r.policy_version, "permission_id": r.permission_id,
             "created_at": r.created_at.isoformat()}
            for r in records
        ],
    }



# A supplier may withdraw an RFQ opt-in directly through an invitation token.
# Opt-out remains available after the quote deadline; an expired invitation
# must not trap suppliers in a marketing/notification list.
optout_router = APIRouter(prefix="/v1/provider", tags=["provider-contact-policy"])


@optout_router.post("/contact/opt-out")
def invitation_token_opt_out(
    x_invitation_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_invitation_key or len(x_invitation_key) > 256:
        raise HTTPException(403, "invitation_access_denied")
    invitation = (
        db.query(Invitation).filter_by(token_hash=token_digest(x_invitation_key))
        .one_or_none()
    )
    if invitation is None or not token_matches(x_invitation_key, invitation.token_hash):
        raise HTTPException(403, "invitation_access_denied")
    company = (
        db.query(Company).filter_by(id=invitation.company_id)
        .with_for_update().populate_existing().one_or_none()
    )
    if company is None:
        raise HTTPException(404, "company_not_found")
    previous = latest_permission(db, company.id)
    if previous is not None and not previous.enabled:
        return {"status": "OPTED_OUT", "idempotent_replay": True}
    row = ProviderContactPermission(
        company_id=company.id, channel=RFQ_EMAIL, purpose=RFQ_PURPOSE,
        revision=(previous.revision + 1 if previous else 1),
        enabled=False, destination_hash=destination_digest(company.contact_email),
        evidence_kind="PROVIDER_OPTOUT_REQUEST",
        evidence_reference="invitation:" + invitation.id,
        reviewer_reference="SELF_SERVICE_INVITATION_TOKEN",
    )
    db.add(row)
    db.flush()
    audit(db, "PROVIDER_RFQ_EMAIL_OPT_OUT", row.id, "provider", {
        "company_id": company.id, "invitation_id": invitation.id,
        "revision": row.revision,
    })
    db.commit()
    return {"status": "OPTED_OUT", "idempotent_replay": False}
