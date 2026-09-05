"""
Legal Metrology Prosecution Case Lifecycle Manager
==================================================
Coordinates the formal statutory case progression under Section 36(1) and
Section 48 / 48A of the Legal Metrology Act, 2009 (as amended by the Jan Vishwas Act).

Life Cycle:
    1. Inspection Assessment -> Non-Compliance Identified
    2. Section 36(1) Improvement Notice Served (15-Day Cure Period Triggered)
    3. Intermediate Verification -> Cured by Merchant (Case Closed without Penalty)
    4. Unremedied Expiration -> Compounding Escalation (Adjudicating Officer Determination)
    5. Repeat Offenses -> Multi-Year Compounding Escalation Ladder
"""

from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class CaseStage(str, enum.Enum):
    """Statutory stages of an enforcement case."""

    EVALUATED = "EVALUATED"
    NOTICE_SERVED = "NOTICE_SERVED"
    IN_CURE_PERIOD = "IN_CURE_PERIOD"
    CURED_CLOSED = "CURED_CLOSED"
    UNREMEDIED_EXPIRED = "UNREMEDIED_EXPIRED"
    COMPOUNDED = "COMPOUNDED"
    COURT_PROSECUTION_INITIATED = "COURT_PROSECUTION_INITIATED"


@dataclass
class ProsecutionCaseDossier:
    """Formal case docket tracking statutory progression against non-compliant packaging."""

    case_id: str
    inspection_id: str
    merchant_name: str
    manufacturer_name: str
    commodity_name: str
    jurisdiction_code: str
    stage: CaseStage = CaseStage.EVALUATED
    violation_rules: List[str] = field(default_factory=list)
    notice_reference: Optional[str] = None
    notice_issued_at_iso: Optional[str] = None
    cure_deadline_iso: Optional[str] = None
    cure_verified_at_iso: Optional[str] = None
    compounding_quantum_inr: Optional[int] = None
    compounding_receipt_ref: Optional[str] = None
    offense_count_for_entity: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "inspection_id": self.inspection_id,
            "merchant_name": self.merchant_name,
            "manufacturer_name": self.manufacturer_name,
            "commodity_name": self.commodity_name,
            "jurisdiction_code": self.jurisdiction_code,
            "stage": self.stage.value,
            "violation_rules": self.violation_rules,
            "notice_reference": self.notice_reference,
            "notice_issued_at_iso": self.notice_issued_at_iso,
            "cure_deadline_iso": self.cure_deadline_iso,
            "compounding_quantum_inr": self.compounding_quantum_inr,
            "offense_count_for_entity": self.offense_count_for_entity,
        }


class ProsecutionCaseManager:
    """
    Manages enforcement cases, statutory deadlines, and compounding ladders.
    """

    def __init__(self, default_cure_period_days: int = 15) -> None:
        self.default_cure_period_days = default_cure_period_days
        self._dockets: Dict[str, ProsecutionCaseDossier] = {}

    def create_case(
        self,
        inspection_id: str,
        merchant_name: str,
        manufacturer_name: str,
        commodity_name: str,
        jurisdiction_code: str,
        violation_rules: List[str],
        offense_count: int = 1,
    ) -> ProsecutionCaseDossier:
        """Initialize a new legal metrology docket."""
        case_id = f"CASE-{jurisdiction_code}-{inspection_id[:8].upper()}"
        dossier = ProsecutionCaseDossier(
            case_id=case_id,
            inspection_id=inspection_id,
            merchant_name=merchant_name,
            manufacturer_name=manufacturer_name,
            commodity_name=commodity_name,
            jurisdiction_code=jurisdiction_code,
            stage=CaseStage.EVALUATED,
            violation_rules=violation_rules,
            offense_count_for_entity=offense_count,
        )
        self._dockets[case_id] = dossier
        return dossier

    def issue_improvement_notice(self, case_id: str) -> ProsecutionCaseDossier:
        """Serve official Section 36(1) Improvement Notice and begin the 15-day cure clock."""
        dossier = self._dockets[case_id]
        now = datetime.datetime.now(datetime.timezone.utc)
        deadline = now + datetime.timedelta(days=self.default_cure_period_days)

        dossier.stage = CaseStage.NOTICE_SERVED
        dossier.notice_reference = f"IN/{dossier.jurisdiction_code}/{dossier.case_id[-6:]}"
        dossier.notice_issued_at_iso = now.isoformat()
        dossier.cure_deadline_iso = deadline.isoformat()
        return dossier

    def verify_merchant_cure(self, case_id: str, is_rectified: bool) -> ProsecutionCaseDossier:
        """Audit re-inspected packaging against notice."""
        dossier = self._dockets[case_id]
        now = datetime.datetime.now(datetime.timezone.utc)

        if is_rectified:
            dossier.stage = CaseStage.CURED_CLOSED
            dossier.cure_verified_at_iso = now.isoformat()
        else:
            dossier.stage = CaseStage.UNREMEDIED_EXPIRED
            # Calculate compounding fee according to repeat offense ladder
            dossier.compounding_quantum_inr = self._calculate_compounding_quantum(
                dossier.offense_count_for_entity
            )

        return dossier

    def compound_case(self, case_id: str, receipt_reference: str) -> ProsecutionCaseDossier:
        """Record receipt of compounding payment under Section 48."""
        dossier = self._dockets[case_id]
        dossier.stage = CaseStage.COMPOUNDED
        dossier.compounding_receipt_ref = receipt_reference
        return dossier

    def _calculate_compounding_quantum(self, offense_count: int) -> int:
        """Statutory compounding schedule under Jan Vishwas Act."""
        if offense_count <= 1:
            return 25000  # First non-compliance: up to Rs. 25,000
        elif offense_count == 2:
            return 50000  # Second offense: up to Rs. 50,000
        else:
            return 100000  # Subsequent: up to Rs. 1,00,000
