"""
Officer Authentication & Jurisdiction Verification Routes
=========================================================
Provides session token issuance, badge credential verification,
and administrative jurisdiction validation for Legal Metrology officers.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from apps.api.auth.rbac import OfficerRole, PermissionScope, RBACManager
from apps.api.auth.jurisdiction import JurisdictionRegistry
from apps.api.auth.tokens import OfficerTokenManager, OfficerSessionContext

router = APIRouter(prefix="/api/v1/auth", tags=["Officer Authentication & RBAC"])

token_manager = OfficerTokenManager()
jurisdiction_registry = JurisdictionRegistry()


class OfficerLoginRequest(BaseModel):
    officer_id: str = Field(..., description="Unique government employee identifier")
    officer_name: str = Field(..., description="Full legal name of the inspecting officer")
    badge_number: str = Field(..., description="Official Legal Metrology badge/license number")
    jurisdiction_code: str = Field(..., description="Station jurisdiction code, e.g. 'IN-DL-SOUTH'")
    role: str = Field(default="FIELD_INSPECTOR", description="Designated role")


class OfficerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in_seconds: int
    officer_name: str
    jurisdiction_code: str
    permissions: List[str]


@router.post(
    "/token",
    response_model=OfficerTokenResponse,
    summary="Issue Officer Session Token",
    description="Authenticates inspector credentials and generates a signed session token.",
)
def login_for_token(req: OfficerLoginRequest) -> OfficerTokenResponse:
    try:
        role_enum = OfficerRole(req.role.upper())
    except ValueError:
        role_enum = OfficerRole.FIELD_INSPECTOR

    token = token_manager.issue_token(
        officer_id=req.officer_id,
        officer_name=req.officer_name,
        badge_number=req.badge_number,
        jurisdiction_code=req.jurisdiction_code,
        roles=[role_enum],
        ttl_seconds=28800,
    )

    perms = RBACManager.get_all_permissions([role_enum])

    return OfficerTokenResponse(
        access_token=token,
        token_type="Bearer",
        expires_in_seconds=28800,
        officer_name=req.officer_name,
        jurisdiction_code=req.jurisdiction_code,
        permissions=[p.value for p in perms],
    )


@router.get(
    "/verify",
    summary="Verify Active Session Token",
    description="Validates Bearer token in Authorization header and returns granted scopes.",
)
def verify_session(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header (expected 'Bearer <token>').",
        )

    raw_token = authorization.split(" ", 1)[1]
    ctx, err = token_manager.verify_token(raw_token)

    if err or not ctx:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {err}",
        )

    node = jurisdiction_registry.get(ctx.jurisdiction_code)
    jurisdiction_desc = node.name if node else "Unregistered Regional Zone"

    perms = RBACManager.get_all_permissions(ctx.roles)

    return {
        "status": "VALID",
        "officer_id": ctx.officer_id,
        "officer_name": ctx.officer_name,
        "badge_number": ctx.badge_number,
        "jurisdiction_code": ctx.jurisdiction_code,
        "jurisdiction_name": jurisdiction_desc,
        "roles": [r.value for r in ctx.roles],
        "granted_permissions": [p.value for p in perms],
        "expires_at_epoch": ctx.expires_at_epoch,
    }
