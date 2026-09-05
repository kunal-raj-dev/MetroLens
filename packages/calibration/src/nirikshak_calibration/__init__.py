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


def detect_reference_and_calibrate(
    image: Any,
    reference_type: str = "AUTO",
    known_coin_diameter_mm: float = 27.0,
) -> CalibrationOutcome:
    """
    Detects physical scale reference (fiducial marker or reference coin) in image.
    If detected, computes optical scale factor (mm/pixel).
    If no valid reference detected, strictly returns UNCALIBRATED with scale_factor=None.
    """
    if image is None:
        return CalibrationOutcome(
            status=CalibrationStatus.UNCALIBRATED,
            details={"reason": "Empty image"},
        )

    import numpy as np
    if not isinstance(image, np.ndarray) or image.size == 0:
        return CalibrationOutcome(
            status=CalibrationStatus.UNCALIBRATED,
            details={"reason": "Invalid or empty image array"},
        )

    import cv2
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # 1. Detect ArUco marker if present
    try:
        if hasattr(cv2, "aruco"):
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
            corners, ids, _ = detector.detectMarkers(gray)
            if ids is not None and len(corners) > 0:
                pts = corners[0][0]
                side_px = float(np.linalg.norm(pts[0] - pts[1]))
                if side_px > 10.0:
                    return compute_scale_factor(
                        measured_marker_pixels=side_px,
                        known_marker_mm=50.0,
                        marker_name="ARUCO_4X4_50MM",
                    )
    except Exception:
        pass

    # 2. Detect circular reference coin via HoughCircles
    try:
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        h, w = gray.shape[:2]
        min_radius = int(min(h, w) * 0.03)
        max_radius = int(min(h, w) * 0.25)

        if min_radius > 0 and max_radius > min_radius:
            circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=min(h, w) * 0.1,
                param1=100,
                param2=60,
                minRadius=min_radius,
                maxRadius=max_radius,
            )
            if circles is not None and len(circles[0]) > 0:
                radius_px = float(circles[0][0][2])
                diameter_px = radius_px * 2.0
                if diameter_px > 10.0:
                    return compute_scale_factor(
                        measured_marker_pixels=diameter_px,
                        known_marker_mm=known_coin_diameter_mm,
                        marker_name="INR_10_COIN",
                    )
    except Exception:
        pass

    # 3. No valid reference found -> strictly return UNCALIBRATED
    return CalibrationOutcome(
        status=CalibrationStatus.UNCALIBRATED,
        scale_factor_mm_per_pixel=None,
        uncertainty_mm_per_pixel=None,
        marker_name=None,
        details={"reason": "No fiducial marker or reference coin detected in frame"},
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
    "detect_reference_and_calibrate",
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
