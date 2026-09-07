"""
Section 48 Compounding Ledger & Treasury Reconciliation Subsystem
================================================================
Provides statutory compliance ledger, 3-year recidivism tracking,
e-Challan treasury reconciliation, and discharge order issuance under Section 48
and Section 48A of the Legal Metrology Act, 2009.

Statutory Provisions (Section 48, LM Act 2009):
-----------------------------------------------
1. Section 48(1): Any offence punishable under Section 25, Sections 27 to 39,
   Sections 45 to 47, or any rule made under sub-section (3) of Section 52 may,
   either before or after the institution of the prosecution, be compounded by
   the Director or Legal Metrology Officer authorized on payment of compounding fee.
   
2. Section 48(2) - Strict Recidivism Bar:
   "Nothing in sub-section (1) shall apply to a person who commits the same or
   similar offence within a period of three (3) years from the date on which the
   first offence, committed by him, was compounded."
   -> Second offence within 3 years is strictly NON-COMPOUNDABLE by law.
   -> Must be mandatorily escalated to the Judicial Magistrate for criminal prosecution.

3. Section 48(3) - Statutory Immunity & Discharge:
   "Where an offence has been compounded under sub-section (1), no proceeding or
   further proceeding, as the case may be, shall be taken against the offender
   in respect of the offence so compounded and the offender, if in custody,
   shall be discharged."
"""

from __future__ import annotations

import datetime
import enum
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("metrolens.judicial.compounding_ledger")


class CompoundingStatus(str, enum.Enum):
    """Lifecycle states of a statutory compounding proceeding."""
    NOTICE_ISSUED = "notice_issued"
    APPLICATION_RECEIVED = "application_received"
    FEE_ASSESSED = "fee_assessed"
    CHALLAN_GENERATED = "challan_generated"
    PAYMENT_VERIFIED = "payment_verified"
    DISCHARGE_ORDER_ISSUED = "discharge_order_issued"
    REJECTED_RECIDIVIST = "rejected_recidivist_non_compoundable"
    ESCALATED_TO_COURT = "escalated_to_court_prosecution"


class OffenceRecidivismLevel(str, enum.Enum):
    """Recidivism classification under the 3-year lookback rule."""
    FIRST_OFFENCE = "first_offence_eligible"
    REPEAT_WITHIN_3_YEARS = "repeat_within_3_years_strictly_non_compoundable"
    SUBSEQUENT_BEYOND_3_YEARS = "subsequent_beyond_3_years_eligible"


@dataclass
class TreasuryChallanReceipt:
    """State Government e-Challan / Cyber Treasury payment confirmation."""
    challan_number: str  # e.g. "MH-TR-2026-0098412"
    bank_reference_utr: str  # Bank UTR / Cyber Treasury reference
    major_head_account: str = "0435"  # Other Agricultural and Consumer Affairs Services
    minor_head_account: str = "102"  # Fees for Weights and Measures Regulation
    remitter_name: str = ""
    amount_inr: float = 0.0
    payment_mode: str = "NEFT/RTGS"  # "NetBanking", "UPI", "Treasury Counter"
    timestamp_verified: datetime.datetime = field(default_factory=datetime.datetime.now)
    cyber_treasury_auth_code: str = ""


@dataclass
class CompoundingRecord:
    """Complete statutory compounding docket entry."""
    case_number: str
    inspection_id: str
    offender_name: str
    gstin: str
    pan_number: str
    offence_type: str
    statutory_section: str
    date_of_commission: datetime.date
    recidivism_level: OffenceRecidivismLevel
    compounding_fee_inr: float
    status: CompoundingStatus
    notice_date: datetime.date
    treasury_challan: Optional[TreasuryChallanReceipt] = None
    discharge_order_number: Optional[str] = None
    discharge_date: Optional[datetime.date] = None
    authorized_officer: str = "Controller of Legal Metrology"
    remarks: str = ""
    prior_case_references: List[str] = field(default_factory=list)


@dataclass
class EligibilityAssessment:
    """Diagnostic outcome of Section 48 recidivism verification."""
    is_compoundable: bool
    recidivism_level: OffenceRecidivismLevel
    suggested_compounding_fee_inr: float
    prior_compounded_cases: List[CompoundingRecord] = field(default_factory=list)
    statutory_reasoning: str = ""


class CompoundingLedger:
    """
    Centralized statewide registry for Section 48 Legal Metrology compounding.
    Maintains chronological offence history and enforces the strict 3-year recidivism bar.
    """

    STATUTORY_FEE_SCHEDULE: Dict[str, Tuple[float, float]] = {
        # (min_fee, max_fee)
        "Section 36(1)": (25000.0, 50000.0),
        "Section 36(2)": (50000.0, 100000.0),
        "Rule 6": (10000.0, 25000.0),
        "Rule 7": (10000.0, 20000.0),
        "Rule 18(2)": (15000.0, 30000.0),
        "Rule 26": (15000.0, 25000.0),
        "Section 24": (10000.0, 20000.0),
    }

    def __init__(self):
        # Key: case_number -> CompoundingRecord
        self._records: Dict[str, CompoundingRecord] = {}
        # Index: PAN -> List[case_number]
        self._pan_index: Dict[str, List[str]] = {}
        # Index: GSTIN -> List[case_number]
        self._gstin_index: Dict[str, List[str]] = {}

    # -------------------------------------------------------------------------
    # Recidivism & Eligibility Assessment
    # -------------------------------------------------------------------------

    def assess_eligibility(
        self,
        gstin: str,
        pan: str,
        statutory_section: str,
        date_of_commission: datetime.date,
    ) -> EligibilityAssessment:
        """
        Evaluates whether an accused entity is legally eligible for Section 48 compounding.
        Checks for prior compounded offences within a strict 3-year window (1095 days).
        """
        gstin_clean = gstin.strip().upper()
        pan_clean = pan.strip().upper()

        # Find all historical cases associated with PAN or GSTIN
        candidate_case_ids: Set[str] = set()
        if gstin_clean in self._gstin_index:
            candidate_case_ids.update(self._gstin_index[gstin_clean])
        if pan_clean in self._pan_index:
            candidate_case_ids.update(self._pan_index[pan_clean])

        # Filter to successfully compounded cases (where discharge order was issued or fee paid)
        prior_cases: List[CompoundingRecord] = []
        for cid in candidate_case_ids:
            rec = self._records[cid]
            if rec.status in (CompoundingStatus.PAYMENT_VERIFIED, CompoundingStatus.DISCHARGE_ORDER_ISSUED):
                # Check if same or similar statutory section
                if rec.statutory_section == statutory_section or "Rule" in statutory_section and "Rule" in rec.statutory_section:
                    prior_cases.append(rec)

        # Sort by date of commission / discharge
        prior_cases.sort(key=lambda r: r.discharge_date or r.date_of_commission, reverse=True)

        # Check 3-year statutory lookback window (1095 days)
        three_years_delta = datetime.timedelta(days=1095)
        recent_violations = [
            r for r in prior_cases
            if (date_of_commission - (r.discharge_date or r.date_of_commission)) <= three_years_delta
            and (date_of_commission >= (r.discharge_date or r.date_of_commission))
        ]

        if recent_violations:
            prior_ref = recent_violations[0]
            reason = (
                f"STRICTLY NON-COMPOUNDABLE under Section 48(2) of Legal Metrology Act, 2009. "
                f"Entity committed and compounded an identical/similar offence ({prior_ref.statutory_section}) "
                f"under Case #{prior_ref.case_number} on {prior_ref.discharge_date or prior_ref.date_of_commission}, "
                f"which falls within the statutory 3-year disqualification window. Mandatory Court prosecution required."
            )
            return EligibilityAssessment(
                is_compoundable=False,
                recidivism_level=OffenceRecidivismLevel.REPEAT_WITHIN_3_YEARS,
                suggested_compounding_fee_inr=0.0,
                prior_compounded_cases=recent_violations,
                statutory_reasoning=reason,
            )

        # Offence is compoundable
        fee_range = self.STATUTORY_FEE_SCHEDULE.get(statutory_section, (10000.0, 25000.0))
        if prior_cases:
            # Beyond 3 years: upper bracket
            recidivism = OffenceRecidivismLevel.SUBSEQUENT_BEYOND_3_YEARS
            suggested_fee = fee_range[1]
            reason = (
                f"Eligible for compounding as previous offence occurred > 3 years ago. "
                f"Assessed at upper statutory tier of ₹{suggested_fee:,.2f}."
            )
        else:
            recidivism = OffenceRecidivismLevel.FIRST_OFFENCE
            suggested_fee = fee_range[0]
            reason = (
                f"First-time offence under {statutory_section}. "
                f"Eligible for compounding at baseline statutory fee of ₹{suggested_fee:,.2f}."
            )

        return EligibilityAssessment(
            is_compoundable=True,
            recidivism_level=recidivism,
            suggested_compounding_fee_inr=suggested_fee,
            prior_compounded_cases=prior_cases,
            statutory_reasoning=reason,
        )

    # -------------------------------------------------------------------------
    # Compounding Lifecycle Management
    # -------------------------------------------------------------------------

    def create_compounding_notice(
        self,
        case_number: str,
        inspection_id: str,
        offender_name: str,
        gstin: str,
        pan_number: str,
        offence_type: str,
        statutory_section: str,
        date_of_commission: datetime.date,
        assessed_fee_inr: Optional[float] = None,
        authorized_officer: str = "Controller of Legal Metrology",
    ) -> CompoundingRecord:
        """Initializes compounding proceeding and issues statutory notice."""
        eligibility = self.assess_eligibility(gstin, pan_number, statutory_section, date_of_commission)

        if not eligibility.is_compoundable:
            record = CompoundingRecord(
                case_number=case_number,
                inspection_id=inspection_id,
                offender_name=offender_name,
                gstin=gstin.strip().upper(),
                pan_number=pan_number.strip().upper(),
                offence_type=offence_type,
                statutory_section=statutory_section,
                date_of_commission=date_of_commission,
                recidivism_level=eligibility.recidivism_level,
                compounding_fee_inr=0.0,
                status=CompoundingStatus.REJECTED_RECIDIVIST,
                notice_date=datetime.date.today(),
                authorized_officer=authorized_officer,
                remarks=eligibility.statutory_reasoning,
                prior_case_references=[c.case_number for c in eligibility.prior_compounded_cases],
            )
            self._save_record(record)
            return record

        fee = assessed_fee_inr if assessed_fee_inr is not None else eligibility.suggested_compounding_fee_inr
        record = CompoundingRecord(
            case_number=case_number,
            inspection_id=inspection_id,
            offender_name=offender_name,
            gstin=gstin.strip().upper(),
            pan_number=pan_number.strip().upper(),
            offence_type=offence_type,
            statutory_section=statutory_section,
            date_of_commission=date_of_commission,
            recidivism_level=eligibility.recidivism_level,
            compounding_fee_inr=fee,
            status=CompoundingStatus.NOTICE_ISSUED,
            notice_date=datetime.date.today(),
            authorized_officer=authorized_officer,
            remarks=eligibility.statutory_reasoning,
            prior_case_references=[c.case_number for c in eligibility.prior_compounded_cases],
        )
        self._save_record(record)
        return record

    def record_treasury_challan(
        self,
        case_number: str,
        challan: TreasuryChallanReceipt,
    ) -> CompoundingRecord:
        """Records e-Challan cyber treasury payment and verifies amount."""
        if case_number not in self._records:
            raise KeyError(f"Compounding case #{case_number} not found in ledger.")

        record = self._records[case_number]
        if record.status in (CompoundingStatus.REJECTED_RECIDIVIST, CompoundingStatus.ESCALATED_TO_COURT):
            raise ValueError(f"Cannot accept payment for case #{case_number} in status {record.status}.")

        if challan.amount_inr < record.compounding_fee_inr:
            raise ValueError(
                f"Challan amount (₹{challan.amount_inr:,.2f}) is less than assessed fee (₹{record.compounding_fee_inr:,.2f})."
            )

        record.treasury_challan = challan
        record.status = CompoundingStatus.PAYMENT_VERIFIED
        return record

    def issue_discharge_order(
        self,
        case_number: str,
        authorized_officer: Optional[str] = None,
    ) -> CompoundingRecord:
        """Issues Section 48(3) statutory discharge order upon verified treasury payment."""
        if case_number not in self._records:
            raise KeyError(f"Compounding case #{case_number} not found in ledger.")

        record = self._records[case_number]
        if record.status != CompoundingStatus.PAYMENT_VERIFIED:
            raise ValueError(
                f"Cannot issue discharge order for case #{case_number}: payment not verified (status: {record.status})."
            )

        order_no = f"DISCHARGE-SEC48-{case_number}-{datetime.date.today().strftime('%Y%m%d')}"
        record.discharge_order_number = order_no
        record.discharge_date = datetime.date.today()
        record.status = CompoundingStatus.DISCHARGE_ORDER_ISSUED
        if authorized_officer:
            record.authorized_officer = authorized_officer

        record.remarks += f" [Discharge order {order_no} granted under Section 48(3)]."
        return record

    def escalate_to_court_prosecution(
        self,
        case_number: str,
        reason: str,
    ) -> CompoundingRecord:
        """Escalates case to criminal court proceedings."""
        if case_number not in self._records:
            raise KeyError(f"Compounding case #{case_number} not found in ledger.")

        record = self._records[case_number]
        record.status = CompoundingStatus.ESCALATED_TO_COURT
        record.remarks += f" [Escalated to criminal prosecution: {reason}]."
        return record

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _save_record(self, record: CompoundingRecord) -> None:
        self._records[record.case_number] = record
        if record.pan_number:
            self._pan_index.setdefault(record.pan_number, []).append(record.case_number)
        if record.gstin:
            self._gstin_index.setdefault(record.gstin, []).append(record.case_number)

    def get_record(self, case_number: str) -> Optional[CompoundingRecord]:
        return self._records.get(case_number)

    def get_all_records(self) -> List[CompoundingRecord]:
        return list(self._records.values())
