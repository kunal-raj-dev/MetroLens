"""
Nirikshak Reporting Package.
Provides statutory inspection dossier generation, court-admissible ReportLab PDF compilation,
Section 63 BSA 2023 legal affidavits, bilingual Devanagari typography, and multi-format exports.
"""

from .pdf_compiler import (
    PDFReportCompiler,
    NumberedCanvas,
    compile_inspection_pdf,
    pdf_compiler,
)
from .legal_affidavit import (
    LegalAffidavitCompiler,
    CertifyingOfficerInfo,
    ElectronicRecordEvidenceDetails,
)
from .bilingual_typography import (
    BilingualTypographyEngine,
    BilingualTerm,
)
from .multi_page_dossier import (
    MultiPageDossierCompiler,
    MultiPageDossierPayload,
    DossierEvidenceExhibit,
)
from .digital_signature import (
    DigitalSignatureManager,
    DigitalSignatureSeal,
    TimestampToken,
)
from .export_formats import ComplianceDossierExporter

# Legacy compatibility
from nirikshak_shared.models.contracts import InspectionResult
from typing import Dict, Any


class DossierGenerator:
    """Renders standardized inspection dossiers into PDF and structured JSON formats."""

    def __init__(self):
        self.compiler = PDFReportCompiler()

    def generate_json_summary(self, result: InspectionResult) -> Dict[str, Any]:
        """Exports the immutable inspection result into a standardized summary dictionary."""
        return result.model_dump(mode="json", exclude_none=True)

    def generate_pdf_bytes(self, result: InspectionResult) -> bytes:
        """Generates a standardized PDF dossier using ReportLab."""
        from nirikshak_rules_engine.schemas import (
            ComplianceEvaluationResult,
            ComplianceState,
            VerdictBadgeColor,
            RuleEvaluationRecord,
        )

        rule_records = []
        for re in result.rule_evaluations:
            rule_records.append(
                RuleEvaluationRecord(
                    rule_id=re.rule_id,
                    rule_title=re.rule_title,
                    statutory_reference=re.statutory_reference,
                    status="PASS" if re.verdict.value == "PASS" else "FAIL",
                    is_compliant=re.verdict.value == "PASS",
                    observed_value=re.observed_summary,
                    required_value=re.required_summary,
                    notes=re.evaluation_notes,
                    statutory_citation=getattr(
                        re,
                        "statutory_citation",
                        re.statutory_reference or "Legal Metrology (Packaged Commodities) Rules, 2011",
                    ),
                )
            )

        comp_res = ComplianceEvaluationResult(
            inspection_id=result.inspection_id,
            timestamp_utc=result.created_at.isoformat(),
            overall_verdict=result.overall_verdict.value,
            verdict_badge_color="green" if result.overall_verdict.value == "COMPLIANT" else "red",
            primary_legal_summary=f"Automated legal metrology inspection outcome: {result.overall_verdict.value}",
            rule_evaluations=rule_records,
            sha256_hash=result.image_sha256,
        )
        return self.compiler.compile_report_pdf(comp_res)


__all__ = [
    "DossierGenerator",
    "PDFReportCompiler",
    "NumberedCanvas",
    "compile_inspection_pdf",
    "pdf_compiler",
    "LegalAffidavitCompiler",
    "CertifyingOfficerInfo",
    "ElectronicRecordEvidenceDetails",
    "BilingualTypographyEngine",
    "BilingualTerm",
    "MultiPageDossierCompiler",
    "MultiPageDossierPayload",
    "DossierEvidenceExhibit",
    "DigitalSignatureManager",
    "DigitalSignatureSeal",
    "TimestampToken",
    "ComplianceDossierExporter",
]
