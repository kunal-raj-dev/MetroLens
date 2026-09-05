"""
Stateful eMaap Mock Server & Portal Simulator
=============================================
Provides a deterministic, stateful simulation of the national Legal Metrology
eMaap / e-Pramit portal for integration testing, fuzzing, and failure injection.

Capabilities:
    - Maintains in-memory case database.
    - Simulates notice issuance, merchant cure periods, and compounding fines.
    - Injects transient faults (503 Service Unavailable, 504 Timeout, 401 Bad HMAC).
"""

from __future__ import annotations

import datetime
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class EMaapCaseRecord:
    """Represents a case dossier filed within the national registry."""

    case_reference: str
    inspection_id: str
    jurisdiction_code: str
    status: str  # 'FILED', 'NOTICE_DISPATCHED', 'CURE_PENDING', 'CURED', 'COMPOUNDED', 'ESCALATED'
    raw_image_sha256: str
    violations_count: int
    cure_deadline_iso: Optional[str] = None
    compounding_fee_inr: Optional[int] = None
    created_at_iso: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    last_updated_iso: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )


class StatefulEMaapMockServer:
    """
    Simulates the National Legal Metrology portal backend.
    """

    def __init__(self, authorized_api_key: str = "METROLENS_PROD_KEY") -> None:
        self.authorized_api_key = authorized_api_key
        self._cases: Dict[str, EMaapCaseRecord] = {}
        # Fault injection controls
        self.simulate_down = False
        self.simulate_latency_ms = 0
        self.fail_next_n_requests = 0

    def file_inspection_case(
        self,
        api_key: str,
        inspection_id: str,
        jurisdiction_code: str,
        raw_image_sha256: str,
        violations: List[Dict[str, Any]],
        overall_verdict: str,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Handle POST /api/v1/cases/file
        """
        if self.simulate_down or self.fail_next_n_requests > 0:
            if self.fail_next_n_requests > 0:
                self.fail_next_n_requests -= 1
            return 503, {"error": "eMaap National Portal Database Unavailable for Maintenance."}

        if api_key != self.authorized_api_key:
            return 401, {"error": "Invalid or expired eMaap API authentication credentials."}

        case_ref = f"EMAAP-{jurisdiction_code}-2026-{uuid.uuid4().hex[:6].upper()}"
        has_violations = len(violations) > 0 or overall_verdict != "COMPLIANT"

        status = "NOTICE_DISPATCHED" if has_violations else "FILED"
        deadline = None
        fee = None

        if has_violations:
            cure_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=15)
            deadline = cure_dt.isoformat()
            fee = 25000  # Standard Section 36(1) compounding benchmark

        record = EMaapCaseRecord(
            case_reference=case_ref,
            inspection_id=inspection_id,
            jurisdiction_code=jurisdiction_code,
            status=status,
            raw_image_sha256=raw_image_sha256,
            violations_count=len(violations),
            cure_deadline_iso=deadline,
            compounding_fee_inr=fee,
        )

        self._cases[case_ref] = record
        return 201, {
            "status": "SUCCESS",
            "case_reference": case_ref,
            "lifecycle_status": status,
            "cure_deadline": deadline,
            "compounding_fee_inr": fee,
        }

    def get_case(self, case_ref: str) -> Optional[EMaapCaseRecord]:
        """Retrieve case record by reference code."""
        return self._cases.get(case_ref)

    def record_merchant_cure(self, case_ref: str) -> bool:
        """Mark case as rectified by merchant within 15-day window."""
        record = self._cases.get(case_ref)
        if record and record.status in ("NOTICE_DISPATCHED", "CURE_PENDING"):
            record.status = "CURED"
            record.last_updated_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return True
        return False

    def escalate_for_prosecution(self, case_ref: str) -> bool:
        """Escalate case for judicial magistrate proceedings."""
        record = self._cases.get(case_ref)
        if record:
            record.status = "ESCALATED"
            record.last_updated_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return True
        return False
