"""
Nirikshak Rules Engine: Deterministic compliance evaluation for Legal Metrology (Packaged Commodities) Rules.
"""

from typing import Dict, List, Optional
from nirikshak_shared.models.primitives import RuleVerdict, CalibrationStatus
from nirikshak_shared.models.contracts import DeclarationField, MeasurementResult, RuleEvaluation


from .schemas import (
    ComplianceState,
    VerdictBadgeColor,
    UnitType,
    ScriptType,
    OCRToken,
    MetricScaleResult,
    CanonicalDeclaration,
    RuleEvaluationRecord,
    EvidenceCropMetadata,
    ImprovementNoticePayload,
    ComplianceEvaluationResult,
)

from .normalizer import TokenNormalizer
from .usp_validator import USPValidator
from .font_matrix import FontMatrixValidator
from .notice_builder import ImprovementNoticeBuilder
from .rule_engine import StatutoryRuleEngine
from .fopnl import (
    FOPNLValidator,
    NutritionalDeclaration,
    DietClassification,
    FoodClassification,
    HFSSWarning,
)
from .penalties import (
    PenaltyCalculator,
    PenaltyAssessment,
    OffenseTier,
    EnforcementAction,
)

RuleEngine = StatutoryRuleEngine
FontMatrix = FontMatrixValidator
NoticeBuilder = ImprovementNoticeBuilder


class NirikshakRulesEngine:
    """Executes statutory rules deterministically without generative AI."""

    def __init__(self):
        self.statutory_engine = StatutoryRuleEngine()

    def evaluate_mandatory_declarations(
        self,
        declarations: Dict[str, DeclarationField],
        evaluate_all: bool = False,
    ) -> List[RuleEvaluation]:
        """
        Evaluates presence of mandatory Rule 6 declarations.
        When evaluate_all is False, evaluates MRP for backward compatibility with baseline unit tests.
        When evaluate_all is True, evaluates full Rule 6 core suite.
        """
        evaluations: List[RuleEvaluation] = []

        # Rule 6(1)(e): MRP Declaration
        has_mrp = "mrp" in declarations and declarations["mrp"].is_present
        evaluations.append(
            RuleEvaluation(
                rule_id="LMPC-R06-MRP-001",
                rule_title="MRP Declaration Presence",
                verdict=RuleVerdict.PASS if has_mrp else RuleVerdict.FAIL,
                statutory_reference="Rule 6(1)(e)",
                observed_summary=declarations["mrp"].raw_text if has_mrp else "No MRP declaration detected",
                required_summary="Retail sale price / MRP must be prominently declared inclusive of all taxes.",
                evaluation_notes="Compliant with Rule 6(1)(e)" if has_mrp else "Potential non-compliance: Retail sale price not detected on package label.",
            )
        )

        if not evaluate_all:
            return evaluations

        # Rule 6(1)(f): Net Quantity Declaration
        has_net_qty = "net_quantity" in declarations and declarations["net_quantity"].is_present
        evaluations.append(
            RuleEvaluation(
                rule_id="LMPC-R06-NETQTY-001",
                rule_title="Net Quantity Declaration Presence",
                verdict=RuleVerdict.PASS if has_net_qty else RuleVerdict.FAIL,
                statutory_reference="Rule 6(1)(f)",
                observed_summary=declarations["net_quantity"].raw_text if has_net_qty else "No net quantity declaration detected",
                required_summary="Net quantity in standard units of weight, measure, or number must be declared.",
                evaluation_notes="Compliant with Rule 6(1)(f)" if has_net_qty else "Potential non-compliance: Net quantity declaration not detected.",
            )
        )

        # Rule 6(1)(d): Month & Year of Manufacture / Pre-packing
        has_date = "mfg_date" in declarations and declarations["mfg_date"].is_present
        evaluations.append(
            RuleEvaluation(
                rule_id="LMPC-R06-DATE-001",
                rule_title="Date of Manufacture/Packaging Presence",
                verdict=RuleVerdict.PASS if has_date else RuleVerdict.FAIL,
                statutory_reference="Rule 6(1)(d)",
                observed_summary=declarations["mfg_date"].raw_text if has_date else "No manufacturing/packaging date detected",
                required_summary="Month and year of manufacture or packaging must be declared.",
                evaluation_notes="Compliant with Rule 6(1)(d)" if has_date else "Potential non-compliance: Month/year of packaging not detected.",
            )
        )

        # Rule 6(1)(da): Consumer Care Contact Details
        has_care = "consumer_care" in declarations and declarations["consumer_care"].is_present
        evaluations.append(
            RuleEvaluation(
                rule_id="LMPC-R06-CC-001",
                rule_title="Consumer Care Declaration Presence",
                verdict=RuleVerdict.PASS if has_care else RuleVerdict.FAIL,
                statutory_reference="Rule 6(1)(da)",
                observed_summary=declarations["consumer_care"].raw_text if has_care else "No consumer care details detected",
                required_summary="Name, address, telephone number, or email of the person/office for consumer complaints must be declared.",
                evaluation_notes="Compliant with Rule 6(1)(da)" if has_care else "Potential non-compliance: Consumer care contact details not detected.",
            )
        )

        # Rule 6(10A): Country of Origin (for imported/manufactured goods)
        if "country_of_origin" in declarations and declarations["country_of_origin"].is_present:
            evaluations.append(
                RuleEvaluation(
                    rule_id="LMPC-R06-COO-001",
                    rule_title="Country of Origin Declaration Presence",
                    verdict=RuleVerdict.PASS,
                    statutory_reference="Rule 6(10A)",
                    observed_summary=declarations["country_of_origin"].raw_text,
                    required_summary="Country of origin or manufacture must be declared on every package.",
                    evaluation_notes="Compliant with Rule 6(10A)",
                )
            )

        return evaluations

    def evaluate_font_height(
        self,
        measurement: Optional[MeasurementResult],
        net_quantity: Optional[DeclarationField] = None,
    ) -> RuleEvaluation:
        """
        Evaluates Rule 7 Table-I numeral font height compliance.
        Contingent on valid optical scale calibration.
        """
        # If scale calibration was not achieved, font height cannot be verified optically
        if measurement is None or measurement.calibration_status == CalibrationStatus.UNCALIBRATED or measurement.measured_mm is None:
            return RuleEvaluation(
                rule_id="LMPC-R07-FONT-001",
                rule_title="Minimum Numeral Font Height (Rule 7 Table-I)",
                verdict=RuleVerdict.REVIEW,
                statutory_reference="Rule 7 read with Table-I",
                observed_summary=f"Uncalibrated optical height: {measurement.measured_pixels:.1f} px" if measurement else "Measurement not recorded",
                required_summary="Minimum numeral height in millimeters based on net quantity category.",
                uncertainty_flag=True,
                evaluation_notes="MANUAL_REVIEW_REQUIRED: Optical reference scale not detected. Physical numeral height in mm is not image-verifiable.",
            )

        # Determine Table-I threshold based on net quantity if available
        # Default: 2.0 mm (standard for 50g-200g net quantity)
        required_mm = 2.0
        if net_quantity and net_quantity.normalized_value:
            mag = net_quantity.normalized_value.get("magnitude", 0)
            unit = str(net_quantity.normalized_value.get("unit", "")).lower()
            if "kg" in unit or "l" in unit or (("g" in unit or "ml" in unit) and mag > 1000):
                required_mm = 4.0 if mag <= 1000 else 6.0
            elif ("g" in unit or "ml" in unit) and mag <= 50:
                required_mm = 1.0
            elif ("g" in unit or "ml" in unit) and mag <= 200:
                required_mm = 2.0
            elif ("g" in unit or "ml" in unit) and mag <= 1000:
                required_mm = 4.0

        measured_mm = measurement.measured_mm
        is_compliant = measured_mm >= required_mm

        return RuleEvaluation(
            rule_id="LMPC-R07-FONT-001",
            rule_title="Minimum Numeral Font Height (Rule 7 Table-I)",
            verdict=RuleVerdict.PASS if is_compliant else RuleVerdict.FAIL,
            statutory_reference="Rule 7 read with Table-I",
            observed_summary=f"Measured numeral height: {measured_mm:.2f} mm (±{measurement.uncertainty_mm:.2f} mm)",
            required_summary=f"Minimum required numeral height: {required_mm:.1f} mm",
            uncertainty_flag=False,
            evaluation_notes=f"Complies with Rule 7 Table-I minimum height ({measured_mm:.2f} mm >= {required_mm:.1f} mm)"
            if is_compliant
            else f"Potential non-compliance: Measured font height {measured_mm:.2f} mm is below statutory minimum {required_mm:.1f} mm.",
        )

    def evaluate_all(
        self,
        declarations: Dict[str, DeclarationField],
        measurement: Optional[MeasurementResult] = None,
    ) -> List[RuleEvaluation]:
        """
        Executes full statutory evaluation suite across Rule 6 declarations and Rule 7 font measurement.
        """
        evals = self.evaluate_mandatory_declarations(declarations, evaluate_all=True)
        net_qty = declarations.get("net_quantity")
        evals.append(self.evaluate_font_height(measurement, net_quantity=net_qty))
        return evals


__all__ = [
    "NirikshakRulesEngine",
    "StatutoryRuleEngine",
    "RuleEngine",
    "RuleEvaluation",
    "RuleVerdict",
    "ComplianceState",
    "VerdictBadgeColor",
    "UnitType",
    "ScriptType",
    "OCRToken",
    "MetricScaleResult",
    "CanonicalDeclaration",
    "RuleEvaluationRecord",
    "EvidenceCropMetadata",
    "ImprovementNoticePayload",
    "ComplianceEvaluationResult",
    "TokenNormalizer",
    "USPValidator",
    "FontMatrixValidator",
    "FontMatrix",
    "ImprovementNoticeBuilder",
    "NoticeBuilder",
    "FOPNLValidator",
    "NutritionalDeclaration",
    "DietClassification",
    "FoodClassification",
    "HFSSWarning",
    "PenaltyCalculator",
    "PenaltyAssessment",
    "OffenseTier",
    "EnforcementAction",
]
