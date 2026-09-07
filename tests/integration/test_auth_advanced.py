"""
Integration Tests for RBAC, Jurisdiction Boundaries & Token Authentication
==========================================================================
Verifies statutory role permissions, administrative hierarchy boundaries,
and cryptographic session token validation.
"""

import time
import pytest

from apps.api.auth.rbac import OfficerRole, PermissionScope, RBACManager
from apps.api.auth.jurisdiction import (
    JurisdictionLevel,
    JurisdictionRegistry,
)
from apps.api.auth.tokens import OfficerTokenManager, OfficerSessionContext


# ---------------------------------------------------------------------------
# 1. RBAC Tests
# ---------------------------------------------------------------------------

def test_rbac_permission_matrix():
    """Verify role privilege boundaries."""
    # Field inspector: can create inspection, cannot compound penalties
    inspector_roles = [OfficerRole.FIELD_INSPECTOR]
    assert RBACManager.has_permission(inspector_roles, PermissionScope.INSPECTION_CREATE) is True
    assert RBACManager.has_permission(inspector_roles, PermissionScope.PENALTY_COMPOUND) is False

    # Adjudicating officer: can compound penalties and read audit logs
    adjudicator_roles = [OfficerRole.ADJUDICATING_OFFICER]
    assert RBACManager.has_permission(adjudicator_roles, PermissionScope.PENALTY_COMPOUND) is True
    assert RBACManager.has_permission(adjudicator_roles, PermissionScope.AUDIT_LOG_READ) is True

    # Auditor: read-only access
    auditor_roles = [OfficerRole.SYSTEM_AUDITOR]
    assert RBACManager.has_permission(auditor_roles, PermissionScope.AUDIT_LOG_READ) is True
    assert RBACManager.has_permission(auditor_roles, PermissionScope.INSPECTION_CREATE) is False


# ---------------------------------------------------------------------------
# 2. Jurisdiction Boundary Tests
# ---------------------------------------------------------------------------

def test_jurisdiction_containment_rules():
    """Verify all-India, state-wide, and district-isolated authorities."""
    registry = JurisdictionRegistry()

    # 1. Central officer has jurisdiction everywhere
    assert registry.is_authorized("IN-CENTRAL", "IN-DL-SOUTH") is True
    assert registry.is_authorized("IN-CENTRAL", "IN-MH-MUMBAI-SUB") is True

    # 2. Maharashtra state controller has authority over all MH districts
    assert registry.is_authorized("IN-MH", "IN-MH-MUMBAI-CITY") is True
    assert registry.is_authorized("IN-MH", "IN-MH-PUNE") is True
    # But cannot enforce in Delhi
    assert registry.is_authorized("IN-MH", "IN-DL-SOUTH") is False

    # 3. South Delhi district inspector can only enforce in South Delhi
    assert registry.is_authorized("IN-DL-SOUTH", "IN-DL-SOUTH") is True
    assert registry.is_authorized("IN-DL-SOUTH", "IN-DL-CENTRAL") is False


# ---------------------------------------------------------------------------
# 3. Officer Token Tests
# ---------------------------------------------------------------------------

def test_officer_token_lifecycle_and_tamper_detection():
    """Verify cryptographic token issuance, verification, and signature tampering."""
    mgr = OfficerTokenManager()

    token = mgr.issue_token(
        officer_id="OFFICER-789",
        officer_name="Inspector Anjali Nair",
        badge_number="MH-LM-5021",
        jurisdiction_code="IN-MH-MUMBAI-SUB",
        roles=[OfficerRole.FIELD_INSPECTOR],
        ttl_seconds=3600,
    )

    assert isinstance(token, str)
    assert "." in token

    # Clean verification
    ctx, err = mgr.verify_token(token)
    assert err is None
    assert ctx is not None
    assert ctx.officer_id == "OFFICER-789"
    assert ctx.has_permission(PermissionScope.INSPECTION_CREATE) is True
    assert ctx.has_permission(PermissionScope.PENALTY_COMPOUND) is False

    # Tampered signature
    tampered_sig = token[:-4] + "0000"
    ctx_bad, err_bad = mgr.verify_token(tampered_sig)
    assert ctx_bad is None
    assert "verification failed" in err_bad.lower()


def test_officer_token_expiration():
    """Verify expired token rejection."""
    mgr = OfficerTokenManager()
    # Expired token with negative TTL
    expired_token = mgr.issue_token(
        officer_id="OFFICER-EXPIRED",
        officer_name="Inspector Test",
        badge_number="EX-01",
        jurisdiction_code="IN-CENTRAL",
        roles=[OfficerRole.FIELD_INSPECTOR],
        ttl_seconds=-10,
    )

    ctx, err = mgr.verify_token(expired_token)
    assert ctx is None
    assert "expired" in err.lower()
