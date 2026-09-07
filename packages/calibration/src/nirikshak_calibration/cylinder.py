"""
Nirikshak Calibration: Constrained Cylindrical Packaging Measurement.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Responsibilities:
- Evaluates packaging surface geometry state (PLANAR, CYLINDRICAL, UNSUPPORTED_TAPERED, UNKNOWN).
- Strictly distinguishes:
    1. Axial/Vertical generator measurement (invariant under right-cylinder model when aligned)
    2. Circumferential/Horizontal measurement (foreshortened by cos(phi))
- Right-Cylinder Vertical Generator Principle:
    For a right cylinder whose axis is aligned with the measurement coordinate system
    and for a locally applicable calibrated scale, axial distance along the generator
    is preserved: h_axial_mm = h_vertical_px * S.
    The implementation does NOT assume this relationship for arbitrary unrectified or misaligned views.
- Central Vertical Strip Constraint:
    |phi| <= 20.0 deg (cos phi >= 0.9397).
    Circumferential correction 1/cos(20 deg) - 1 reaches approximately 6.42% at 20 deg.
    Classified as PROPOSED HEURISTIC / NOT PHYSICALLY VALIDATED.
- Explicit Graceful Degradation:
    - Planar surfaces receive NO cylindrical correction (factor = 1.0).
    - Tapered/conical and unknown packaging surfaces route to MANUAL_REVIEW_REQUIRED.
"""

import math
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Dict, Any

from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_shared.models.contracts import MeasurementResult
from . import CalibrationOutcome


class CylinderGeometryState(str, Enum):
    """Packaging surface geometric classification."""
    PLANAR = "PLANAR"
    CYLINDRICAL = "CYLINDRICAL"
    UNSUPPORTED_TAPERED = "UNSUPPORTED_TAPERED"
    UNKNOWN = "UNKNOWN"


class CylinderMeasurementStatus(str, Enum):
    """Status outcomes and error codes for cylindrical measurement."""
    SUCCESS = "SUCCESS"
    PLANAR_NO_CORRECTION = "PLANAR_NO_CORRECTION"
    UNSUPPORTED_TAPERED = "UNSUPPORTED_TAPERED"
    UNKNOWN_GEOMETRY = "UNKNOWN_GEOMETRY"
    EXCEEDS_ANGULAR_THRESHOLD = "EXCEEDS_ANGULAR_THRESHOLD"
    INVALID_INPUT = "INVALID_INPUT"
    UNCALIBRATED = "UNCALIBRATED"
    OUT_OF_CYLINDER_BOUNDS = "OUT_OF_CYLINDER_BOUNDS"
    MISALIGNED_AXIS = "MISALIGNED_AXIS"


@dataclass(frozen=True)
class CylinderModelConfig:
    """
    Configurable parameters and proposed heuristic thresholds for cylindrical measurement.

    Evidentiary Status:
        max_angular_displacement_deg (20.0 deg) and min_cos_phi (0.9397) represent
        PROPOSED HEURISTICS derived from theoretical 1/cos(phi) - 1 <= 6.42% distortion bounds.
        They must NOT be treated as validated statutory criteria.
    """
    max_angular_displacement_deg: float = 20.0   # Central strip boundary (PROPOSED HEURISTIC)
    min_cos_phi: float = 0.9397                 # cos(20 deg) ≈ 0.93969 (PROPOSED HEURISTIC)
    min_cylinder_radius_px: float = 20.0        # Minimum cylinder pixel radius
    strict_angular_cutoff: bool = False         # If True, rejects measurements beyond 20 deg; if False, flags warning


@dataclass(frozen=True)
class CylinderMeasurementResult:
    """
    Strongly-typed outcome of cylindrical packaging measurement.

    Attributes:
        status: Specific outcome or diagnostic status code.
        geometry_state: Surface geometry class (PLANAR, CYLINDRICAL, UNSUPPORTED_TAPERED, UNKNOWN).
        measured_axial_pixels: Raw vertical pixel extent (y_max - y_min).
        measured_axial_mm: Calibrated physical axial height in millimeters, or None if uncalibrated.
        scale_factor_mm_per_pixel: Applied optical scale factor, or None.
        uncertainty_mm: Uncertainty bound on axial measurement, or None if unavailable.
        calibration_status: Calibration state under which measurement was calculated.
        angular_displacement_deg: Angle phi between feature center and cylinder central meridian in degrees.
        cos_phi: Foreshortening cosine factor cos(phi).
        circumferential_correction_factor: Multiplicative factor 1.0 / cos(phi) to un-foreshorten horizontal width.
        measured_circumferential_pixels: Raw horizontal pixel width (x_max - x_min).
        corrected_circumferential_pixels: Un-foreshortened circumferential pixel width (w_px / cos(phi)).
        corrected_circumferential_mm: Un-foreshortened physical circumferential width in mm.
        is_axis_aligned: True if cylinder axis was validated/asserted parallel to measurement coordinate system.
        message: Optional human-readable diagnostic message.
    """
    status: CylinderMeasurementStatus
    geometry_state: CylinderGeometryState
    measured_axial_pixels: float
    measured_axial_mm: Optional[float] = None
    scale_factor_mm_per_pixel: Optional[float] = None
    uncertainty_mm: Optional[float] = None
    calibration_status: CalibrationStatus = CalibrationStatus.UNCALIBRATED
    angular_displacement_deg: Optional[float] = None
    cos_phi: Optional[float] = None
    circumferential_correction_factor: Optional[float] = None
    measured_circumferential_pixels: Optional[float] = None
    corrected_circumferential_pixels: Optional[float] = None
    corrected_circumferential_mm: Optional[float] = None
    is_axis_aligned: bool = True
    message: Optional[str] = None

    def to_measurement_result(self, feature_name: str = "numeral_height_mm") -> MeasurementResult:
        """Bridges to canonical nirikshak_shared.models.contracts.MeasurementResult for axial dimension."""
        return MeasurementResult(
            feature_name=feature_name,
            measured_pixels=self.measured_axial_pixels,
            scale_factor_mm_per_pixel=self.scale_factor_mm_per_pixel,
            measured_mm=self.measured_axial_mm,
            uncertainty_mm=self.uncertainty_mm,
            calibration_status=self.calibration_status,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into an inspectable dictionary."""
        return {
            "status": self.status.value,
            "geometry_state": self.geometry_state.value,
            "measured_axial_pixels": self.measured_axial_pixels,
            "measured_axial_mm": self.measured_axial_mm,
            "scale_factor_mm_per_pixel": self.scale_factor_mm_per_pixel,
            "uncertainty_mm": self.uncertainty_mm,
            "calibration_status": self.calibration_status.value,
            "angular_displacement_deg": self.angular_displacement_deg,
            "cos_phi": self.cos_phi,
            "circumferential_correction_factor": self.circumferential_correction_factor,
            "measured_circumferential_pixels": self.measured_circumferential_pixels,
            "corrected_circumferential_pixels": self.corrected_circumferential_pixels,
            "corrected_circumferential_mm": self.corrected_circumferential_mm,
            "is_axis_aligned": self.is_axis_aligned,
            "message": self.message,
        }


def _validate_box_coords(box: Any) -> Tuple[bool, str, Optional[Tuple[float, float, float, float]]]:
    """Validates raw bounding coordinates."""
    if box is None:
        return False, "Feature bounding box cannot be None.", None

    if isinstance(box, (str, bytes)):
        return False, "Feature bounding box cannot be a string or bytes.", None

    if isinstance(box, BoundingBox):
        coords = (box.x_min, box.y_min, box.x_max, box.y_max)
    elif hasattr(box, "__len__") and len(box) == 4:
        try:
            coords = (float(box[0]), float(box[1]), float(box[2]), float(box[3]))
        except (ValueError, TypeError):
            return False, f"Feature bounding box contains non-numeric values: {box}.", None
    else:
        return False, "Feature bounding box must be BoundingBox or 4-element (x_min, y_min, x_max, y_max) tuple.", None

    if not all(math.isfinite(c) for c in coords):
        return False, f"Feature bounding box contains non-finite coordinates: {coords}.", None

    xmin, ymin, xmax, ymax = coords
    if xmax <= xmin:
        return False, f"Feature bounding box width is zero or inverted: x_min={xmin} >= x_max={xmax}.", None
    if ymax <= ymin:
        return False, f"Feature bounding box height is zero or inverted: y_min={ymin} >= y_max={ymax}.", None

    return True, "Valid feature coordinates.", coords


def _validate_calibration_scale(
    calibration: Any,
) -> Tuple[bool, Optional[float], Optional[float], CalibrationStatus, str]:
    """Validates optical calibration scale without fabricating scale or uncertainty."""
    if calibration is None:
        return False, None, None, CalibrationStatus.UNCALIBRATED, "Calibration outcome is missing."

    scale = None
    unc = None
    status = CalibrationStatus.UNCALIBRATED

    if isinstance(calibration, CalibrationOutcome):
        status = calibration.status
        scale = calibration.scale_factor_mm_per_pixel
        unc = calibration.uncertainty_mm_per_pixel
    elif hasattr(calibration, "scale_factor_mm_per_pixel"):
        scale = getattr(calibration, "scale_factor_mm_per_pixel", None)
        unc = getattr(calibration, "uncertainty_mm_per_pixel", None)
        status = getattr(calibration, "status", CalibrationStatus.UNCALIBRATED)
    elif isinstance(calibration, (float, int)):
        scale = float(calibration)
        status = CalibrationStatus.CALIBRATED
    else:
        return False, None, None, CalibrationStatus.UNCALIBRATED, "Unrecognized calibration input type."

    if status != CalibrationStatus.CALIBRATED:
        return False, None, None, status, f"Calibration status is not CALIBRATED (received {status})."

    if scale is None or not math.isfinite(scale) or scale <= 0.0:
        return False, None, None, CalibrationStatus.UNCALIBRATED, f"Scale factor is invalid, non-finite, or <= 0: {scale}."

    if unc is not None and (not math.isfinite(unc) or unc < 0.0):
        unc = None

    return True, scale, unc, CalibrationStatus.CALIBRATED, "Valid optical calibration."


def measure_cylindrical_feature(
    feature_box: Any,
    geometry_state: CylinderGeometryState = CylinderGeometryState.CYLINDRICAL,
    cylinder_center_x: Optional[float] = None,
    cylinder_radius_px: Optional[float] = None,
    calibration: Any = None,
    is_axis_aligned: bool = True,
    config: Optional[CylinderModelConfig] = None,
) -> CylinderMeasurementResult:
    """
    Applies mathematically constrained measurement model for cylindrical packaging.

    Fundamental Model & Mathematical Principles:
    1. Planar surfaces (PLANAR):
       - No cylindrical curvature exists.
       - Returns PLANAR_NO_CORRECTION with curvature_correction_factor = 1.0.
    2. Unsupported / Unknown surfaces (UNSUPPORTED_TAPERED, UNKNOWN):
       - Non-cylindrical curvature violates right-cylinder generator invariance.
       - Returns UNSUPPORTED_TAPERED or UNKNOWN_GEOMETRY routing to MANUAL_REVIEW_REQUIRED.
    3. Right-Cylinder Vertical Generator Principle (CYLINDRICAL):
       - Conditioned on:
         a) Valid optical calibration.
         b) Cylinder axis aligned with measurement coordinate system (is_axis_aligned=True).
         c) Locally applicable scale at that generator.
       - Axial height along generator is invariant: h_axial_mm = h_vertical_px * S.
       - Circumferential width is foreshortened: w_true_px = w_measured_px / cos(phi).
    4. Central Vertical Strip Constraint:
       - Offset Delta x = x_feature - x_center.
       - sin(phi) = Delta x / R.
       - Central strip: |phi| <= 20.0 deg (cos phi >= 0.9397).
       - Circumferential distortion is <= 6.42% at 20 deg (PROPOSED HEURISTIC).
       - Features exceeding 20 deg are flagged with EXCEEDS_ANGULAR_THRESHOLD.

    Args:
        feature_box: BoundingBox or (x_min, y_min, x_max, y_max) tuple of feature.
        geometry_state: Surface classification (PLANAR, CYLINDRICAL, UNSUPPORTED_TAPERED, UNKNOWN).
        cylinder_center_x: Image x-coordinate of the vertical cylinder axis meridian.
        cylinder_radius_px: Apparent radius of the cylinder in pixels.
        calibration: CalibrationOutcome, scale factor float, or object with scale_factor_mm_per_pixel.
        is_axis_aligned: True if cylinder axis is verified parallel to image vertical axis.
        config: Optional CylinderModelConfig.

    Returns:
        CylinderMeasurementResult with axial and circumferential metrics and diagnostic status.
    """
    cfg = config if config is not None else CylinderModelConfig()

    # 1. Validate feature bounding coordinates
    box_ok, box_msg, coords = _validate_box_coords(feature_box)
    if not box_ok or coords is None:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.INVALID_INPUT,
            geometry_state=geometry_state,
            measured_axial_pixels=0.0,
            message=box_msg,
        )

    xmin, ymin, xmax, ymax = coords
    axial_px = float(ymax - ymin)
    circumferential_px = float(xmax - xmin)

    # 2. Validate optical calibration (without fabricating scale)
    is_cal, scale_val, unc_val, cal_status, cal_msg = _validate_calibration_scale(calibration)

    axial_mm = None
    unc_mm = None
    if is_cal and scale_val is not None:
        axial_mm = round(axial_px * scale_val, 4)
        if unc_val is not None and unc_val > 0.0:
            unc_mm = round(axial_px * unc_val, 4)

    # 3. Handle non-cylindrical geometry states
    if geometry_state == CylinderGeometryState.PLANAR:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.PLANAR_NO_CORRECTION,
            geometry_state=CylinderGeometryState.PLANAR,
            measured_axial_pixels=axial_px,
            measured_axial_mm=axial_mm,
            scale_factor_mm_per_pixel=scale_val,
            uncertainty_mm=unc_mm,
            calibration_status=cal_status,
            angular_displacement_deg=0.0,
            cos_phi=1.0,
            circumferential_correction_factor=1.0,
            measured_circumferential_pixels=circumferential_px,
            corrected_circumferential_pixels=circumferential_px,
            corrected_circumferential_mm=round(circumferential_px * scale_val, 4) if scale_val else None,
            is_axis_aligned=is_axis_aligned,
            message="Planar packaging panel: no cylindrical curvature correction applied.",
        )

    if geometry_state == CylinderGeometryState.UNSUPPORTED_TAPERED:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.UNSUPPORTED_TAPERED,
            geometry_state=CylinderGeometryState.UNSUPPORTED_TAPERED,
            measured_axial_pixels=axial_px,
            scale_factor_mm_per_pixel=scale_val,
            calibration_status=cal_status,
            is_axis_aligned=is_axis_aligned,
            message="MANUAL_REVIEW_REQUIRED: Tapered or conical packaging cannot be modeled with right-cylinder invariance.",
        )

    if geometry_state == CylinderGeometryState.UNKNOWN:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.UNKNOWN_GEOMETRY,
            geometry_state=CylinderGeometryState.UNKNOWN,
            measured_axial_pixels=axial_px,
            scale_factor_mm_per_pixel=scale_val,
            calibration_status=cal_status,
            is_axis_aligned=is_axis_aligned,
            message="MANUAL_REVIEW_REQUIRED: Surface geometry unknown.",
        )

    # 4. For CYLINDRICAL state: validate cylinder parameters
    try:
        if cylinder_center_x is None:
            raise ValueError()
        center_x = float(cylinder_center_x)
        if not math.isfinite(center_x):
            raise ValueError()
    except (TypeError, ValueError):
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.INVALID_INPUT,
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            measured_axial_pixels=axial_px,
            message=f"cylinder_center_x must be a finite numeric coordinate (received {cylinder_center_x}).",
        )

    try:
        if cylinder_radius_px is None:
            raise ValueError()
        radius_px = float(cylinder_radius_px)
        if not math.isfinite(radius_px) or radius_px < cfg.min_cylinder_radius_px:
            raise ValueError()
    except (TypeError, ValueError):
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.INVALID_INPUT,
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            measured_axial_pixels=axial_px,
            message=f"cylinder_radius_px must be a finite number >= {cfg.min_cylinder_radius_px}px (received {cylinder_radius_px}).",
        )

    # 5. Check axis alignment condition
    if not is_axis_aligned:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.MISALIGNED_AXIS,
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            measured_axial_pixels=axial_px,
            scale_factor_mm_per_pixel=scale_val,
            calibration_status=cal_status,
            is_axis_aligned=False,
            message="Right-cylinder axial invariance requires cylinder axis to be aligned with measurement coordinate system.",
        )

    # 6. Evaluate angular displacement phi
    feature_center_x = 0.5 * (xmin + xmax)
    delta_x = feature_center_x - center_x
    norm_sin = delta_x / radius_px

    if abs(norm_sin) > 1.0:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.OUT_OF_CYLINDER_BOUNDS,
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            measured_axial_pixels=axial_px,
            scale_factor_mm_per_pixel=scale_val,
            calibration_status=cal_status,
            is_axis_aligned=True,
            message=f"Feature center ({feature_center_x:.1f}) lies outside cylinder silhouette (center={center_x}, R={radius_px}).",
        )

    phi_rad = math.asin(norm_sin)
    phi_deg = math.degrees(phi_rad)
    cos_phi = math.cos(phi_rad)

    # Circumferential foreshortening correction factor = 1.0 / cos(phi)
    # Note: at 20 deg, cos(phi) ≈ 0.93969 -> factor ≈ 1.06418 -> correction ≈ 6.42% (PROPOSED HEURISTIC)
    corr_factor = 1.0 / cos_phi if cos_phi > 1e-6 else 1.0
    corr_circum_px = round(circumferential_px * corr_factor, 3)
    corr_circum_mm = round(corr_circum_px * scale_val, 4) if scale_val else None

    # 7. Check angular threshold and calibration condition
    abs_phi = abs(phi_deg)

    if (abs_phi > cfg.max_angular_displacement_deg or cos_phi < cfg.min_cos_phi) and cfg.strict_angular_cutoff:
        return CylinderMeasurementResult(
            status=CylinderMeasurementStatus.EXCEEDS_ANGULAR_THRESHOLD,
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            measured_axial_pixels=axial_px,
            scale_factor_mm_per_pixel=scale_val,
            calibration_status=cal_status,
            angular_displacement_deg=round(phi_deg, 3),
            cos_phi=round(cos_phi, 5),
            circumferential_correction_factor=round(corr_factor, 5),
            measured_circumferential_pixels=circumferential_px,
            is_axis_aligned=True,
            message=(
                f"Feature angular displacement (|phi|={abs_phi:.1f} deg) exceeds proposed heuristic threshold "
                f"({cfg.max_angular_displacement_deg:.1f} deg). Circumferential foreshortening reaches "
                f"{(corr_factor - 1.0) * 100:.1f}%. Reposition package closer to central strip for minimum distortion."
            ),
        )

    if not is_cal or scale_val is None:
        status = CylinderMeasurementStatus.UNCALIBRATED
        msg = cal_msg
    elif abs_phi > cfg.max_angular_displacement_deg or cos_phi < cfg.min_cos_phi:
        status = CylinderMeasurementStatus.EXCEEDS_ANGULAR_THRESHOLD
        msg = (
            f"Feature angular displacement (|phi|={abs_phi:.1f} deg) exceeds proposed heuristic threshold "
            f"({cfg.max_angular_displacement_deg:.1f} deg). Circumferential foreshortening reaches "
            f"{(corr_factor - 1.0) * 100:.1f}%. Reposition package closer to central strip for minimum distortion."
        )
    else:
        status = CylinderMeasurementStatus.SUCCESS
        msg = "Cylindrical vertical-generator measurement successful."

    return CylinderMeasurementResult(
        status=status,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        measured_axial_pixels=axial_px,
        measured_axial_mm=axial_mm,
        scale_factor_mm_per_pixel=scale_val,
        uncertainty_mm=unc_mm,
        calibration_status=cal_status,
        angular_displacement_deg=round(phi_deg, 3),
        cos_phi=round(cos_phi, 5),
        circumferential_correction_factor=round(corr_factor, 5),
        measured_circumferential_pixels=circumferential_px,
        corrected_circumferential_pixels=corr_circum_px,
        corrected_circumferential_mm=corr_circum_mm,
        is_axis_aligned=True,
        message=msg,
    )
