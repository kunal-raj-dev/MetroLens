"""
Nirikshak Calibration: Optical reference fiducial detection, planar rectification,
physical font measurement, and constrained cylindrical packaging measurement.
"""

from typing import Optional, Dict, Any
from nirikshak_shared.models.primitives import CalibrationStatus


class CalibrationOutcome:
    """Represents the derived metric scale factor from optical calibration."""
    def __init__(
        self,
        status: CalibrationStatus,
        scale_factor_mm_per_pixel: Optional[float] = None,
        uncertainty_mm_per_pixel: Optional[float] = None,
        marker_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status = status
        self.scale_factor_mm_per_pixel = scale_factor_mm_per_pixel
        self.uncertainty_mm_per_pixel = uncertainty_mm_per_pixel
        self.marker_name = marker_name
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "scale_factor_mm_per_pixel": self.scale_factor_mm_per_pixel,
            "uncertainty_mm_per_pixel": self.uncertainty_mm_per_pixel,
            "marker_name": self.marker_name,
            "details": self.details,
        }


def compute_scale_factor(
    measured_marker_pixels: float,
    known_marker_mm: float,
    marker_name: str = "FIDUCIAL_REFERENCE",
    relative_uncertainty: float = 0.02,
) -> CalibrationOutcome:
    """
    Computes mm per pixel scale factor with formal uncertainty interval.
    Scale S = known_marker_mm / measured_marker_pixels.
    """
    if measured_marker_pixels <= 0 or known_marker_mm <= 0:
        return CalibrationOutcome(
            status=CalibrationStatus.UNCALIBRATED,
            details={"reason": "Invalid marker dimensions"},
        )

    scale = known_marker_mm / measured_marker_pixels
    uncertainty = scale * relative_uncertainty

    return CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=scale,
        uncertainty_mm_per_pixel=uncertainty,
        marker_name=marker_name,
        details={
            "measured_marker_pixels": measured_marker_pixels,
            "known_marker_mm": known_marker_mm,
        },
    )


# Phase 4 Exports
from .types import (
    AnchorType,
    AnchorDetectionStatus,
    EllipseGeometry,
    CardGeometry,
    ConcentricRingInfo,
    AnchorDetectorConfig,
    AnchorDetectionResult,
)
from .anchor_detector import (
    detect_anchor,
    order_quadrilateral_corners,
    compute_algebraic_ellipse_residual,
)

# Phase 5 Exports
from .homography import (
    RectificationStatus,
    HomographyConfig,
    RectificationResult,
    rectify_planar_quadrilateral,
    validate_quadrilateral_geometry,
)

# Phase 6 Exports
from .font_measurer import (
    FontMeasurementType,
    FontMeasurementStatus,
    FontMeasurementConfig,
    FontMeasurementResult,
    measure_font_height,
    measure_font_height_batch,
)

# Phase 7 Exports
from .cylinder import (
    CylinderGeometryState,
    CylinderMeasurementStatus,
    CylinderModelConfig,
    CylinderMeasurementResult,
    measure_cylindrical_feature,
)

# Phase 9 Exports
from .evaluation import (
    BenchmarkStatus,
    GroundTruthSample,
    EvaluationConfig,
    SampleEvaluation,
    CalibrationEvaluationResult,
    evaluate_calibration,
)

__all__ = [
    # Baseline
    "CalibrationOutcome",
    "compute_scale_factor",
    "CalibrationStatus",
    # Phase 4
    "AnchorType",
    "AnchorDetectionStatus",
    "EllipseGeometry",
    "CardGeometry",
    "ConcentricRingInfo",
    "AnchorDetectorConfig",
    "AnchorDetectionResult",
    "detect_anchor",
    "order_quadrilateral_corners",
    "compute_algebraic_ellipse_residual",
    # Phase 5
    "RectificationStatus",
    "HomographyConfig",
    "RectificationResult",
    "rectify_planar_quadrilateral",
    "validate_quadrilateral_geometry",
    # Phase 6
    "FontMeasurementType",
    "FontMeasurementStatus",
    "FontMeasurementConfig",
    "FontMeasurementResult",
    "measure_font_height",
    "measure_font_height_batch",
    # Phase 7
    "CylinderGeometryState",
    "CylinderMeasurementStatus",
    "CylinderModelConfig",
    "CylinderMeasurementResult",
    "measure_cylindrical_feature",
    # Phase 9
    "BenchmarkStatus",
    "GroundTruthSample",
    "EvaluationConfig",
    "SampleEvaluation",
    "CalibrationEvaluationResult",
    "evaluate_calibration",
]
