"""OIDC-authenticated provider portal API; delegates to the same transaction core.

The browser never receives legacy invitation access tokens, commission agreements,
customer email addresses or internal company source licensing metadata.
"""
from __future__ import annotations

import json
import os
import re
from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .auth import require_provider_identity
from .database import get_db
from .models import (Company, CompanyMembership, CompanyObservation,
                     CompanyOwnershipClaim, CompanyGoldenField,
                     Invitation, Quote, Booking, ServiceRequest)
from .api import (QuoteIn, admin, authorized_membership, submit_quote_for_invitation,
                  confirm_booking_for_invitation, aware, audit)

router = APIRouter()


@router.get("/v1/public/auth-config")
def public_auth_config():
    """Expose only non-secret OIDC SPA settings, never provider credentials."""
    issuer = os.environ.get("AGENQO_OIDC_ISSUER", "")
    client_id = os.environ.get("AGENQO_OIDC_CLIENT_ID", "")
    if (not issuer.startswith("https://") or not client_id
        or not re.fullmatch(r"[A-Za-z0-9._:-]{2,120}", client_id)):
        return {"enabled": False}
    return {"enabled": True, "authority": issuer,
            "client_id": client_id, "scope": "openid profile"}


@router.get("/v1/public/companies")
def search_companies(q: str = "", db: Session = Depends(get_db)):
    """Limited discovery for claim candidates; no contacts or personally identifying data."""
    query = q.strip()
    if len(query) < 3 or len(query) > 80:
        raise HTTPException(422, "search_query_length_3_to_80")
    # SQLAlchemy binds values; '%'/'_' are escaped as literal input for LIKE.
    esc = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    found = (db.query(Company)
        .filter(Company.legal_name.ilike("%" + esc + "%", escape="\\"))
        .order_by(Company.legal_name, Company.id)
        .limit(15).all())
    return {"companies": [{"company_id": c.id, "legal_name": c.legal_name,
             "postal_code": c.postal_code, "service_category": c.service_category}
             for c in found]}


@router.get("/v1/provider/claims")
def own_claims(subject: str = Depends(require_provider_identity),
               db: Session = Depends(get_db)):
    rows = (db.query(CompanyOwnershipClaim)
            .filter_by(claimant_subject=subject)
            .order_by(CompanyOwnershipClaim.created_at.desc()).limit(50).all())
    return {"claims": [{"claim_id": c.id, "company_id": c.company_id,
                        "review_state": c.review_state}
                       for c in rows]}


@router.get("/v1/provider/companies/{company_id}/profile")
def own_company_profile(company_id: str,
                        subject: str = Depends(require_provider_identity),
                        db: Session = Depends(get_db)):
    authorized_membership(db, company_id, subject)
    c = db.get(Company, company_id)
    if c is None:
        raise HTTPException(404, "company_not_found")
    golden = db.query(CompanyGoldenField).filter_by(company_id=company_id).all()
    # Only proposed edits, no internal observations from scraped/public data sources.
    proposals = (db.query(CompanyObservation)
                 .filter_by(company_id=company_id, source_kind="PROVIDER_ASSERTION")
                 .order_by(CompanyObservation.created_at.desc()).limit(50).all())
    return {
        "company_id": c.id, "legal_name": c.legal_name, "postal_code": c.postal_code,
        "service_category": c.service_category, "contact_email": c.contact_email,
        "company_status": c.status,
        "published_fields": {f.field_name: f.value for f in golden},
        "proposed_fields": [{"field": p.field_name, "value": p.value,
                             "review_state": p.review_state}
                            for p in proposals],
    }


@router.get("/v1/provider/companies/{company_id}/invitations")
def own_company_invitations(company_id: str,
                            subject: str = Depends(require_provider_identity),
                            db: Session = Depends(get_db)):
    authorized_membership(db, company_id, subject)
    invitations = (db.query(Invitation)
        .filter_by(company_id=company_id)
        .order_by(Invitation.created_at.desc()).limit(50).all())
    records = []
    for invite in invitations:
        req = db.get(ServiceRequest, invite.request_id)
        if req is None:
            continue
        quote = db.query(Quote).filter_by(invitation_id=invite.id).one_or_none()
        booking = db.query(Booking).filter_by(quote_id=quote.id).one_or_none() if quote else None
        records.append({
            "invitation_id": invite.id,
            "invitation_status": invite.status,
            "invitation_expires_at": aware(invite.expires_at).isoformat(),
            "request_category": req.category,
            "request_postal_code": req.postal_code,
            "request_description": req.requirements,
            "structured_requirements": json.loads(req.structured_requirements_json or "{}"),
            "quote": ({"quote_id": quote.id, "status": quote.status,
                       "gross_cents": quote.gross_cents,
                       "fingerprint": quote.fingerprint} if quote else None),
            "booking": ({"booking_id": booking.id, "status": booking.status} if booking else None),
        })
    return {"invitations": records}


@router.post("/v1/provider/companies/{company_id}/invitations/{invitation_id}/quotes",
             status_code=201)
def own_company_submit_quote(company_id: str, invitation_id: str, payload: QuoteIn,
                             subject: str = Depends(require_provider_identity),
                             db: Session = Depends(get_db)):
    authorized_membership(db, company_id, subject)
    invitation = (db.query(Invitation).filter_by(
        id=invitation_id, company_id=company_id).one_or_none())
    if invitation is None:
        raise HTTPException(404, "invitation_not_found")
    return submit_quote_for_invitation(invitation, payload, db)


@router.post("/v1/provider/companies/{company_id}/bookings/{booking_id}/confirm")
def own_company_confirm_booking(company_id: str, booking_id: str,
                                subject: str = Depends(require_provider_identity),
                                db: Session = Depends(get_db)):
    authorized_membership(db, company_id, subject)
    booking = db.get(Booking, booking_id)
    if booking is None:
        raise HTTPException(404, "booking_not_found")
    quote = db.get(Quote, booking.quote_id)
    invite = db.query(Invitation).filter_by(
        id=quote.invitation_id, company_id=company_id).one_or_none()
    if invite is None:
        raise HTTPException(403, "booking_not_owned_by_company")
    return confirm_booking_for_invitation(invite, booking_id, db)
