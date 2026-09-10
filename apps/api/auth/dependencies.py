"""Deployment access control for the MVP's single trusted service principal.

This shared key is an API access boundary, not officer authentication or RBAC.
Individual officer identities and statutory authorizations are not implemented.
"""

import hashlib
import hmac
import os
from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class ServicePrincipal:
    subject: str
    display_name: str = "Authenticated service operator (individual officer unverified)"


def require_api_access(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> ServicePrincipal:
    configured_key = os.environ.get("METROLENS_API_KEY", "")
    if len(configured_key.encode("utf-8")) < 32:
        raise HTTPException(503, "API access is not configured. Contact the service administrator.")
    supplied = credentials.credentials if credentials and credentials.scheme.lower() == "bearer" else ""
    if not supplied or not hmac.compare_digest(supplied.encode("utf-8"), configured_key.encode("utf-8")):
        raise HTTPException(401, "A valid API access key is required.", headers={"WWW-Authenticate": "Bearer"})
    # Binding records to this key also invalidates access to old sessions on rotation.
    subject = hashlib.sha256(configured_key.encode("utf-8")).hexdigest()
    return ServicePrincipal(subject=subject)
