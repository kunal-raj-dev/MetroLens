"""
Officer Session Token & Identity Validator
==========================================
Issues and validates cryptographically signed session tokens for Legal
Metrology Officers carrying out field and administrative inspections.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from .jurisdiction import JurisdictionRegistry
from .rbac import OfficerRole, PermissionScope, RBACManager


@dataclass(frozen=True)
class OfficerSessionContext:
    """Authenticated context of a Legal Metrology officer session."""

    officer_id: str
    officer_name: str
    badge_number: str
    jurisdiction_code: str
    roles: List[OfficerRole]
    issued_at_epoch: float
    expires_at_epoch: float

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at_epoch

    def has_permission(self, permission: PermissionScope) -> bool:
        return RBACManager.has_permission(self.roles, permission)

    def is_authorized_for_zone(self, target_jurisdiction_code: str, registry: JurisdictionRegistry) -> bool:
        return registry.is_authorized(self.jurisdiction_code, target_jurisdiction_code)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "officer_id": self.officer_id,
            "officer_name": self.officer_name,
            "badge_number": self.badge_number,
            "jurisdiction_code": self.jurisdiction_code,
            "roles": [r.value for r in self.roles],
            "issued_at_epoch": self.issued_at_epoch,
            "expires_at_epoch": self.expires_at_epoch,
        }


class OfficerTokenManager:
    """
    Signs and validates tamper-evident session tokens.
    """

    def __init__(self, signing_secret_key: Optional[bytes] = None) -> None:
        configured = os.environ.get("METROLENS_AUTH_SECRET")
        key = signing_secret_key if signing_secret_key is not None else (
            configured.encode("utf-8") if configured is not None else secrets.token_bytes(32)
        )
        if len(key) < 32:
            raise ValueError("Token signing keys must contain at least 32 bytes.")
        self.signing_secret_key = key

    def issue_token(
        self,
        officer_id: str,
        officer_name: str,
        badge_number: str,
        jurisdiction_code: str,
        roles: List[OfficerRole],
        ttl_seconds: int = 28800,  # 8 hours standard shift
    ) -> str:
        """Issue a signed base64 session token."""
        now = time.time()
        payload = {
            "sub": officer_id,
            "name": officer_name,
            "badge": badge_number,
            "jurisdiction": jurisdiction_code,
            "roles": [r.value for r in roles],
            "iat": now,
            "exp": now + ttl_seconds,
        }

        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")

        sig = hmac.new(self.signing_secret_key, payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
        return f"{payload_b64}.{sig}"

    def verify_token(self, token_str: str) -> Tuple[Optional[OfficerSessionContext], Optional[str]]:
        """
        Verify signature and expiration of session token.

        Returns:
            Tuple of (Optional[OfficerSessionContext], Optional[error_reason])
        """
        if len(token_str) > 8192 or not token_str.isascii():
            return None, "Invalid token encoding or length."
        parts = token_str.strip().split(".")
        if len(parts) != 2:
            return None, "Invalid token structure (expected payload.signature)."

        payload_b64, signature_hex = parts

        # Verify HMAC signature
        expected_sig = hmac.new(
            self.signing_secret_key, payload_b64.encode("ascii"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, signature_hex):
            return None, "Cryptographic signature verification failed (token forged or corrupted)."

        # Decode payload
        try:
            # Re-pad base64
            rem = len(payload_b64) % 4
            padded = payload_b64 + ("=" * (4 - rem) if rem else "")
            payload_bytes = base64.urlsafe_b64decode(padded)
            data = json.loads(payload_bytes.decode("utf-8"))
        except Exception as exc:
            return None, f"Failed to parse token payload: {str(exc)}"

        try:
            if not isinstance(data, dict):
                return None, "Invalid token payload."
            exp = float(data.get("exp", 0))
            issued_at = float(data.get("iat", 0))
            import math
            if not math.isfinite(exp) or not math.isfinite(issued_at) or not isinstance(data.get("roles", []), list):
                return None, "Invalid token claims."
        except (TypeError, ValueError):
            return None, "Invalid token claims."
        if time.time() > exp:
            return None, "Officer session token has expired."

        role_objs = [OfficerRole(r) for r in data.get("roles", []) if isinstance(r, str) and r in OfficerRole._value2member_map_]

        context = OfficerSessionContext(
            officer_id=data.get("sub", ""),
            officer_name=data.get("name", ""),
            badge_number=data.get("badge", ""),
            jurisdiction_code=data.get("jurisdiction", ""),
            roles=role_objs,
            issued_at_epoch=issued_at,
            expires_at_epoch=exp,
        )

        return context, None
