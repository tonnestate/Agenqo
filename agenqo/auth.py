"""Fail-closed OAuth 2.0 JWT access-token verification for provider-facing APIs.

Agenqo never issues an access token and does not trust self-asserted company IDs.
Configure a trusted issuer, API audience, and issuer-controlled HTTPS JWKS URI.
Only RS256-signed at+jwt access tokens are accepted.
"""
from __future__ import annotations

from functools import lru_cache
import os
from urllib.parse import urlparse

from fastapi import Header, HTTPException
import jwt
from jwt import InvalidTokenError, PyJWKClient


@lru_cache(maxsize=4)
def _jwks_client(jwks_uri: str):
    return PyJWKClient(jwks_uri, cache_jwk_set=True, lifespan=300, timeout=5)


def require_provider_identity(authorization: str | None = Header(default=None)) -> str:
    issuer = os.getenv("AGENQO_OIDC_ISSUER", "")
    audience = os.getenv("AGENQO_OIDC_AUDIENCE", "")
    jwks_uri = os.getenv("AGENQO_OIDC_JWKS_URL", "")
    parsed = urlparse(jwks_uri)
    # No silent insecure local mode. No discovery URLs derived from untrusted requests.
    if not issuer or not audience or parsed.scheme != "https" or not parsed.netloc:
        raise HTTPException(503, "identity_provider_not_configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "bearer_token_required", headers={"WWW-Authenticate": "Bearer"})
    token = authorization[7:]
    if not token or len(token) > 8192:
        raise HTTPException(401, "invalid_access_token")
    try:
        header = jwt.get_unverified_header(token)
        if header.get("typ", "").lower() not in {"at+jwt", "application/at+jwt"}:
            raise InvalidTokenError("not_an_access_token")
        if header.get("alg") != "RS256":
            raise InvalidTokenError("unsupported_algorithm")
        signing_key = _jwks_client(jwks_uri).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token, signing_key.key, algorithms=["RS256"],
            issuer=issuer, audience=audience,
            options={"require": ["iss", "aud", "sub", "exp", "iat"]},
            leeway=30,
        )
        subject = claims["sub"]
        if not isinstance(subject, str) or not (1 <= len(subject) <= 255):
            raise InvalidTokenError("invalid_subject")
        return subject
    except (jwt.PyJWTError, ValueError, TypeError, OSError) as exc:
        raise HTTPException(401, "invalid_access_token",
                            headers={"WWW-Authenticate": "Bearer"}) from exc
