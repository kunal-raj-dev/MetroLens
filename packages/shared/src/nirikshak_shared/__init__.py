"""
Nirikshak Shared Package: Canonical domain models, contracts, and system primitives.
"""

from .models.primitives import (
    BoundingBox,
    CalibrationStatus,
    PanelName,
    RuleVerdict,
    OverallVerdict,
    InspectionStatus,
    ObservedValue,
    OperatorAnnotation,
)
from .models.contracts import (
    InspectionRequest,
    InspectionResult,
    OCRObservation,
    DeclarationField,
    MeasurementResult,
    RuleEvaluation,
    EvidenceItem,
    InspectionError,
)

__all__ = [
    "BoundingBox",
    "CalibrationStatus",
    "PanelName",
    "RuleVerdict",
    "OverallVerdict",
    "InspectionStatus",
    "ObservedValue",
    "OperatorAnnotation",
    "InspectionRequest",
    "InspectionResult",
    "OCRObservation",
    "DeclarationField",
    "MeasurementResult",
    "RuleEvaluation",
    "EvidenceItem",
    "InspectionError",
]
