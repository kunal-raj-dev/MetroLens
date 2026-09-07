"""
Nirikshak Rules Engine: Section 36(1) Jan Vishwas Improvement Notice Builder.
Statutory Authority: Section 36(1) of the Legal Metrology Act, 2009, as amended by
the Jan Vishwas (Amendment of Provisions) Act, 2026 (effective 01.05.2026).

Decriminalization Mandate:
- In force from May 1, 2026 (Act No. 18 of 2023 / 2026 amendments).
- Packaging declaration omissions under Section 36(1) require a statutory
  15-day Improvement Notice prior to compounding or financial adjudication.
- ZERO obsolete criminal penalty or imprisonment terminology is permitted.
"""

from typing import List, Optional, Dict, Any, Set
from datetime import datetime, timezone

from .schemas import (
    CanonicalDeclaration,
    RuleEvaluationRecord,
    ImprovementNoticePayload,
    ComplianceEvaluationResult,
)


class ImprovementNoticeBuilder:
    """
    Constructs statutory Improvement Notice payloads and eMaap sync records
    under Section 36(1) as amended by the Jan Vishwas (Amendment of Provisions) Act, 2026.
    """

    DEFAULT_CURE_PERIOD_DAYS: int = 15
    GOVERNING_PROVISION: str = "Section 36(1) read with Jan Vishwas (Amendment of Provisions) Act, 2026"
    COMPOUNDING_AUTHORITY: str = "Legal Metrology Compounding Officer"

    # Strictly prohibited obsolete criminal terminology under Jan Vishwas Act
    PROHIBITED_CRIMINAL_TERMS: Set[str] = {
        "imprisonment",
        "jail",
        "prison",
        "penal servitude",
        "arrest",
        "cognizable",
        "non-bailable",
        "custody",
    }

    @classmethod
    def audit_text_decriminalization(cls, text: str) -> None:
        """
        Guarantees that generated notice text contains zero criminal penalty terms.
        Raises ValueError if obsolete criminal terminology is detected.
        """
        lower_text = text.lower()
        for term in cls.PROHIBITED_CRIMINAL_TERMS:
            if term in lower_text:
                raise ValueError(
                    f"Statutory Decriminalization Violation: Prohibited criminal term '{term}' "
                    f"detected in notice text. The Jan Vishwas Act strictly decriminalized Section 36(1)."
                )

    def build_notice(
        self,
        decl: CanonicalDeclaration,
        rule_evaluations: List[RuleEvaluationRecord],
        inspection_id: str = "INSP-DEFAULT",
        officer_name: str = "Authorized Legal Metrology Officer",
        jurisdiction: str = "Central Jurisdiction, New Delhi",
    ) -> ImprovementNoticePayload:
        """
        Builds a Section 36(1) Improvement Notice for detected statutory non-compliances.
        Returns recommended=False if no non-compliances exist.
        """
        # Identify failing rules
        failing_records = [r for r in rule_evaluations if not r.is_compliant and r.status == "FAIL"]

        if not failing_records:
            return ImprovementNoticePayload(
                recommended=False,
                act_provision=self.GOVERNING_PROVISION,
                cure_period_days=self.DEFAULT_CURE_PERIOD_DAYS,
                statutory_grounds="No image-verifiable statutory non-compliance detected. Improvement Notice not recommended.",
                compounding_authority=self.COMPOUNDING_AUTHORITY,
                notice_title="STATUTORY IMPROVEMENT NOTICE",
                notice_text=None,
                itemized_violations=[],
                addressed_to=decl.manufacturer_name or "The Manufacturer / Packer / Importer",
            )

        # Build itemized grounds
        itemized_grounds: List[str] = []
        for idx, rec in enumerate(failing_records, 1):
            ground = (
                f"{idx}. {rec.statutory_reference} ({rec.rule_title}): "
                f"Observed: '{rec.observed_value}'. Required: '{rec.required_value}'. "
                f"Statutory Citation: {rec.statutory_citation}."
            )
            itemized_grounds.append(ground)

        grounds_summary = (
            f"Statutory non-compliance detected under {self.GOVERNING_PROVISION} across {len(failing_records)} requirement(s): "
            + "; ".join(f"{r.statutory_reference} ({r.rule_title})" for r in failing_records)
        )

        recipient = decl.manufacturer_name or "The Registered Manufacturer / Packer / Importer"
        commodity = decl.commodity_name or "Pre-Packaged Commodity"
        formatted_date = datetime.now(timezone.utc).strftime("%d-%m-%Y")

        # Draft formal legal notice text
        violations_block = "\n".join(f"  {g}" for g in itemized_grounds)
        notice_text = (
            f"GOVERNMENT OF INDIA\n"
            f"DEPARTMENT OF CONSUMER AFFAIRS\n"
            f"OFFICE OF THE CONTROLLER OF LEGAL METROLOGY\n"
            f"Jurisdiction: {jurisdiction}\n\n"
            f"STATUTORY IMPROVEMENT NOTICE UNDER SECTION 36(1)\n"
            f"(As amended by the Jan Vishwas (Amendment of Provisions) Act, 2026)\n\n"
            f"Notice Reference ID: NOT-{inspection_id}\n"
            f"Date of Notice: {formatted_date}\n\n"
            f"To:\n"
            f"{recipient}\n"
            f"{decl.manufacturer_address or ''}\n\n"
            f"SUBJECT: Improvement Notice under Section 36(1) of the Legal Metrology Act, 2009 "
            f"for packaging non-compliances observed on '{commodity}'.\n\n"
            f"1. WHEREAS an optical inspection of the pre-packaged commodity '{commodity}' was conducted "
            f"under the provisions of Section 15 of the Legal Metrology Act, 2009;\n\n"
            f"2. AND WHEREAS upon deterministic verification against Chapter II of the Legal Metrology "
            f"(Packaged Commodities) Rules, 2011, the following defect(s) and omission(s) were observed:\n"
            f"{violations_block}\n\n"
            f"3. NOW THEREFORE, in exercise of powers conferred under Section 36(1) of the Legal Metrology Act, "
            f"2009 as amended by the Jan Vishwas (Amendment of Provisions) Act, 2026, you are hereby called upon to:\n"
            f"   (a) Rectify the aforementioned packaging declaration defect(s) across all future production batches;\n"
            f"   (b) Furnish written confirmation and documentary evidence of corrective action to the undersigned "
            f"       Compounding Authority within fifteen (15) days from the receipt of this notice.\n\n"
            f"4. TAKE NOTICE that failure to rectify the defects within the prescribed statutory period of fifteen (15) "
            f"days may warrant administrative compounding proceedings under Section 48 / Section 48A of the Act.\n\n"
            f"Issued under seal by:\n"
            f"{officer_name}\n"
            f"{self.COMPOUNDING_AUTHORITY}\n"
            f"Department of Consumer Affairs\n"
        )

        # Audit notice text for zero criminal terminology
        self.audit_text_decriminalization(notice_text)

        return ImprovementNoticePayload(
            recommended=True,
            act_provision=self.GOVERNING_PROVISION,
            cure_period_days=self.DEFAULT_CURE_PERIOD_DAYS,
            statutory_grounds=grounds_summary,
            compounding_authority=self.COMPOUNDING_AUTHORITY,
            notice_title="STATUTORY IMPROVEMENT NOTICE UNDER SECTION 36(1)",
            notice_text=notice_text,
            itemized_violations=itemized_grounds,
            addressed_to=recipient,
        )

    def build_emaap_sync_payload(
        self,
        result: ComplianceEvaluationResult,
        officer_id: str = "LMO-DELHI-42",
        jurisdiction_code: str = "DL-01-CENTRAL",
    ) -> Dict[str, Any]:
        """
        Builds standardized eMaap mock sync webhook payload conforming to
        docs/API_CONTRACT.md Section 3.4.
        """
        notice_issued = bool(result.improvement_notice and result.improvement_notice.recommended)
        failing_rules = [r for r in result.rule_evaluations if not r.is_compliant]

        state_str = result.overall_verdict.value if hasattr(result.overall_verdict, "value") else str(result.overall_verdict)

        return {
            "inspection_id": result.inspection_id,
            "jurisdiction_code": jurisdiction_code,
            "officer_id": officer_id,
            "compliance_state": state_str,
            "improvement_notice_issued": notice_issued,
            "dossier_sha256": result.sha256_hash or "",
            "timestamp_utc": result.timestamp_utc,
            "statutory_grounds": (
                result.improvement_notice.statutory_grounds if result.improvement_notice else ""
            ),
            "cure_period_days": (
                result.improvement_notice.cure_period_days if result.improvement_notice else 15
            ),
            "defects_count": len(failing_rules),
        }
