"""
Nirikshak Rules Engine: Deterministic compliance evaluation for Legal Metrology (Packaged Commodities) Rules.
"""

from typing import Dict, List, Optional
from nirikshak_shared.models.primitives import RuleVerdict
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
    ) -> List[RuleEvaluation]:
        """
        Evaluates presence of mandatory Rule 6 declarations (MRP, Net Qty, etc.).
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
            )
        )

        return evaluations


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
