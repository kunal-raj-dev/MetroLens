"""Service access status. Individual officer login is intentionally unavailable."""

from fastapi import APIRouter, Depends, HTTPException

from apps.api.auth.dependencies import ServicePrincipal, require_api_access


router = APIRouter(prefix="/api/v1/auth", tags=["Service Access"])


@router.post("/token")
def login_for_token():
    raise HTTPException(501, "Officer token issuance is disabled until a trusted identity provider is configured.")


@router.get("/verify")
def verify_session(principal: ServicePrincipal = Depends(require_api_access)):
    return {
        "status": "VALID", "identity_type": "shared_service_access",
        "officer_identity_verified": False,
    }
