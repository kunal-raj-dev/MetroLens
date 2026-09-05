"""
Nirikshak Shared Models: Primitives and Contract DTOs.
"""

from .primitives import (
    BoundingBox,
    CalibrationStatus,
    PanelName,
    RuleVerdict,
    OverallVerdict,
    InspectionStatus,
    ObservedValue,
    OperatorAnnotation,
)
from .contracts import (
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
