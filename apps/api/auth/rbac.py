"""
Role-Based Access Control (RBAC) Engine
======================================
Defines statutory roles, granular permission scopes, and access verification
logic for officers, inspectors, and adjudicators in MetroLens AI.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class OfficerRole(str, enum.Enum):
    """Statutory and operational roles within the Legal Metrology hierarchy."""

    FIELD_INSPECTOR = "FIELD_INSPECTOR"                    # Field inspections, camera capture, notice serving
    LEGAL_METROLOGY_OFFICER = "LEGAL_METROLOGY_OFFICER"    # Dossier review, statutory verification, notice approval
    ADJUDICATING_OFFICER = "ADJUDICATING_OFFICER"          # Jan Vishwas civil compounding, fine determination
    DIRECTORATE_ADMIN = "DIRECTORATE_ADMIN"                # User management, portal sync, quota settings
    SYSTEM_AUDITOR = "SYSTEM_AUDITOR"                      # Read-only audit logs, Section 63 BSA verification


class PermissionScope(str, enum.Enum):
    """Granular operational privileges."""

    INSPECTION_READ = "inspection:read"
    INSPECTION_CREATE = "inspection:create"
    INSPECTION_DELETE = "inspection:delete"
    NOTICE_ISSUE = "notice:issue"
    NOTICE_EXTEND = "notice:extend"
    PENALTY_COMPOUND = "penalty:compound"
    PROSECUTION_ESCALATE = "prosecution:escalate"
    REPORT_EXPORT_PDF = "report:export_pdf"
    AFFIDAVIT_EXPORT_BSA = "affidavit:export_bsa"
    AUDIT_LOG_READ = "audit_log:read"
    SYSTEM_CONFIG_MANAGE = "system_config:manage"
    PORTAL_SYNC_EMAAP = "portal_sync:emaap"


class RBACManager:
    """
    Manages role-to-permission mappings and evaluates access grants.
    """

    ROLE_PERMISSIONS: Dict[OfficerRole, Set[PermissionScope]] = {
        OfficerRole.FIELD_INSPECTOR: {
            PermissionScope.INSPECTION_READ,
            PermissionScope.INSPECTION_CREATE,
            PermissionScope.REPORT_EXPORT_PDF,
            PermissionScope.NOTICE_ISSUE,
        },
        OfficerRole.LEGAL_METROLOGY_OFFICER: {
            PermissionScope.INSPECTION_READ,
            PermissionScope.INSPECTION_CREATE,
            PermissionScope.NOTICE_ISSUE,
            PermissionScope.NOTICE_EXTEND,
            PermissionScope.REPORT_EXPORT_PDF,
            PermissionScope.AFFIDAVIT_EXPORT_BSA,
            PermissionScope.PORTAL_SYNC_EMAAP,
        },
        OfficerRole.ADJUDICATING_OFFICER: {
            PermissionScope.INSPECTION_READ,
            PermissionScope.NOTICE_ISSUE,
            PermissionScope.NOTICE_EXTEND,
            PermissionScope.PENALTY_COMPOUND,
            PermissionScope.PROSECUTION_ESCALATE,
            PermissionScope.REPORT_EXPORT_PDF,
            PermissionScope.AFFIDAVIT_EXPORT_BSA,
            PermissionScope.AUDIT_LOG_READ,
            PermissionScope.PORTAL_SYNC_EMAAP,
        },
        OfficerRole.DIRECTORATE_ADMIN: {
            PermissionScope.INSPECTION_READ,
            PermissionScope.INSPECTION_CREATE,
            PermissionScope.INSPECTION_DELETE,
            PermissionScope.NOTICE_ISSUE,
            PermissionScope.NOTICE_EXTEND,
            PermissionScope.PENALTY_COMPOUND,
            PermissionScope.PROSECUTION_ESCALATE,
            PermissionScope.REPORT_EXPORT_PDF,
            PermissionScope.AFFIDAVIT_EXPORT_BSA,
            PermissionScope.AUDIT_LOG_READ,
            PermissionScope.SYSTEM_CONFIG_MANAGE,
            PermissionScope.PORTAL_SYNC_EMAAP,
        },
        OfficerRole.SYSTEM_AUDITOR: {
            PermissionScope.INSPECTION_READ,
            PermissionScope.REPORT_EXPORT_PDF,
            PermissionScope.AFFIDAVIT_EXPORT_BSA,
            PermissionScope.AUDIT_LOG_READ,
        },
    }

    @classmethod
    def has_permission(
        cls, roles: List[OfficerRole], required_permission: PermissionScope
    ) -> bool:
        """Evaluate whether any of the assigned roles grants the required permission."""
        for role in roles:
            granted_scopes = cls.ROLE_PERMISSIONS.get(role, set())
            if required_permission in granted_scopes:
                return True
        return False

    @classmethod
    def get_all_permissions(cls, roles: List[OfficerRole]) -> Set[PermissionScope]:
        """Aggregate all unique permissions granted by assigned roles."""
        all_perms: Set[PermissionScope] = set()
        for role in roles:
            all_perms.update(cls.ROLE_PERMISSIONS.get(role, set()))
        return all_perms
