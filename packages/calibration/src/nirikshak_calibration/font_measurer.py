"""
Nirikshak Calibration: Physical Font Measurement & Optical Scale Conversion.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Responsibilities:
- Converts OCR bounding box observations to physical millimeters using validated optical calibration.
- Does NOT perform OCR text recognition (owned strictly by Member 1).
- Rigorously distinguishes between:
    1. OCR Bounding-Box Height (raw bounding box including whitespace padding)
    2. True Printed Glyph Ink Height (via vertical foreground ink projection profiles)
- Zero Scale Fabrication: returns explicit uncalibrated status if calibration is missing,
  invalid, ambiguous, or non-finite.
- Zero Manufactured Uncertainty: propagates uncertainty ONLY when explicitly supplied
  by upstream calibration; otherwise returns uncertainty as None (unavailable).
- Explicit coordinate validation, out-of-bounds detection, and clipping flags.
- Bridges cleanly to nirikshak_shared.models.contracts.MeasurementResult.
"""

import math
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union, Dict, Any
import numpy as np

from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_shared.models.contracts import MeasurementResult
from . import CalibrationOutcome


class FontMeasurementType(str, Enum):
    """Measurement methodology classification."""
    BOUNDING_BOX_HEIGHT = "BOUNDING_BOX_HEIGHT"
    INK_PROFILE_HEIGHT = "INK_PROFILE_HEIGHT"


class FontMeasurementStatus(str, Enum):
    """Taxonomy of font height measurement outcomes and failure modes."""
    SUCCESS = "SUCCESS"
    UNCALIBRATED = "UNCALIBRATED"
    INVALID_BOUNDING_BOX = "INVALID_BOUNDING_BOX"
    OUT_OF_IMAGE_BOUNDS = "OUT_OF_IMAGE_BOUNDS"
    NO_DETECTABLE_INK = "NO_DETECTABLE_INK"
    FAILED_PROCESSING = "FAILED_PROCESSING"


@dataclass(frozen=True)
class FontMeasurementConfig:
    """
    Configurable parameters for optical font measurement and ink profiling.

    Evidentiary Status:
        Thresholds represent PROPOSED HEURISTICS for ink boundary segmentation.
    """
    min_ink_row_occupancy_ratio: float = 0.02   # Fraction of box width required to consider row non-empty
    min_ink_contrast_delta: int = 15            # Minimum contrast between ink and background
    otsu_clip_limit: float = 2.0                # CLAHE clip limit if contrast enhancement needed


@dataclass(frozen=True)
class FontMeasurementResult:
    """
    Strongly-typed outcome of physical font height measurement.

    Attributes:
        status: Specific outcome or rejection status code.
        measurement_type: BOUNDING_BOX_HEIGHT or INK_PROFILE_HEIGHT.
        measured_pixels: Measured pixel height (either bbox height or ink height).
        scale_factor_mm_per_pixel: Applied optical scale factor, or None.
        measured_mm: Derived physical dimension in millimeters (h_px * S), or None.
        uncertainty_mm: Measurement uncertainty in millimeters, or None if unavailable.
        calibration_status: Calibration state under which the measurement was recorded.
        bounding_box: Final (possibly clipped) BoundingBox coordinates.
        original_bounding_box: Pre-clipping BoundingBox coordinates if clipped.
        is_clipped: True if bounding box extended outside image boundaries and was clipped.
        bbox_height_px: Full bounding box pixel height.
        ink_height_px: Measured foreground ink pixel height (if ink profile was evaluated).
        padding_px: Measured vertical whitespace padding pixels (bbox_height_px - ink_height_px).
        message: Optional human-readable diagnostic message.
    """
    status: FontMeasurementStatus
    measurement_type: FontMeasurementType
    measured_pixels: float
    scale_factor_mm_per_pixel: Optional[float] = None
    measured_mm: Optional[float] = None
    uncertainty_mm: Optional[float] = None
    calibration_status: CalibrationStatus = CalibrationStatus.UNCALIBRATED
    bounding_box: Optional[BoundingBox] = None
    original_bounding_box: Optional[BoundingBox] = None
    is_clipped: bool = False
    bbox_height_px: Optional[float] = None
    ink_height_px: Optional[float] = None
    padding_px: Optional[float] = None
    message: Optional[str] = None

    def to_measurement_result(self, feature_name: str = "numeral_height_mm") -> MeasurementResult:
        """Bridges to canonical nirikshak_shared.models.contracts.MeasurementResult."""
        return MeasurementResult(
            feature_name=feature_name,
            measured_pixels=self.measured_pixels,
            scale_factor_mm_per_pixel=self.scale_factor_mm_per_pixel,
            measured_mm=self.measured_mm,
            uncertainty_mm=self.uncertainty_mm,
            calibration_status=self.calibration_status,
            bounding_box=self.bounding_box,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into an inspectable dictionary."""
        bbox_dict = None
        if self.bounding_box is not None:
            bbox_dict = {
                "x_min": self.bounding_box.x_min,
                "y_min": self.bounding_box.y_min,
                "x_max": self.bounding_box.x_max,
                "y_max": self.bounding_box.y_max,
            }

        orig_bbox_dict = None
        if self.original_bounding_box is not None:
            orig_bbox_dict = {
                "x_min": self.original_bounding_box.x_min,
                "y_min": self.original_bounding_box.y_min,
                "x_max": self.original_bounding_box.x_max,
                "y_max": self.original_bounding_box.y_max,
            }

        return {
            "status": self.status.value,
            "measurement_type": self.measurement_type.value,
            "measured_pixels": self.measured_pixels,
            "scale_factor_mm_per_pixel": self.scale_factor_mm_per_pixel,
            "measured_mm": self.measured_mm,
            "uncertainty_mm": self.uncertainty_mm,
            "calibration_status": self.calibration_status.value,
            "bounding_box": bbox_dict,
            "original_bounding_box": orig_bbox_dict,
            "is_clipped": self.is_clipped,
            "bbox_height_px": self.bbox_height_px,
            "ink_height_px": self.ink_height_px,
            "padding_px": self.padding_px,
            "message": self.message,
        }


def _parse_bounding_box(
    box: Any,
) -> Tuple[bool, FontMeasurementStatus, str, Optional[BoundingBox]]:
    """Validates raw bounding box input and parses BoundingBox object."""
    if box is None:
        return False, FontMeasurementStatus.INVALID_BOUNDING_BOX, "Bounding box input cannot be None.", None

    if isinstance(box, BoundingBox):
        xmin, ymin, xmax, ymax = box.x_min, box.y_min, box.x_max, box.y_max
    elif hasattr(box, "__len__") and len(box) == 4:
        try:
            xmin, ymin, xmax, ymax = float(box[0]), float(box[1]), float(box[2]), float(box[3])
        except (ValueError, TypeError):
            return (
                False,
                FontMeasurementStatus.INVALID_BOUNDING_BOX,
                f"Bounding box contains non-numeric values: {box}.",
                None,
            )
    else:
        return (
            False,
            FontMeasurementStatus.INVALID_BOUNDING_BOX,
            "Bounding box must be BoundingBox instance or 4-element (x_min, y_min, x_max, y_max) tuple.",
            None,
        )

    # Check finite numbers (no NaN, Inf)
    coords = [xmin, ymin, xmax, ymax]
    if not all(math.isfinite(c) for c in coords):
        return (
            False,
            FontMeasurementStatus.INVALID_BOUNDING_BOX,
            f"Bounding box contains non-finite coordinates: ({xmin}, {ymin}, {xmax}, {ymax}).",
            None,
        )

    # Validate coordinate ordering and dimensions
    if xmax <= xmin:
        return (
            False,
            FontMeasurementStatus.INVALID_BOUNDING_BOX,
            f"Bounding box width is zero or inverted: x_min={xmin} >= x_max={xmax}.",
            None,
        )
    if ymax <= ymin:
        return (
            False,
            FontMeasurementStatus.INVALID_BOUNDING_BOX,
            f"Bounding box height is zero or inverted: y_min={ymin} >= y_max={ymax}.",
            None,
        )

    return True, FontMeasurementStatus.SUCCESS, "Valid bounding box.", BoundingBox(x_min=xmin, y_min=ymin, x_max=xmax, y_max=ymax)


def _validate_calibration(
    calibration: Any,
) -> Tuple[bool, Optional[float], Optional[float], CalibrationStatus, str]:
    """
    Validates calibration input without fabricating scale factor or uncertainty.

    Returns:
        (is_calibrated, scale_factor, uncertainty, calibration_status, message)
    """
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
        unc = None  # Invalidate bogus uncertainty rather than crashing

    return True, scale, unc, CalibrationStatus.CALIBRATED, "Valid optical calibration."


def _compute_ink_profile_height(
    image_crop: np.ndarray,
    config: FontMeasurementConfig,
) -> Tuple[bool, float, float, float, str]:
    """
    Analyzes token image crop via vertical projection profiling to isolate printed ink height.

    Returns:
        (ink_detected, ink_height_px, top_padding_px, bottom_padding_px, message)
    """
    if image_crop.size == 0 or image_crop.ndim < 2:
        return False, 0.0, 0.0, 0.0, "Empty or degenerate image crop."

    # Convert to grayscale
    if image_crop.ndim == 3:
        # Standard luminance weights
        gray = np.dot(image_crop[..., :3], [0.114, 0.587, 0.299]).astype(np.uint8)
    else:
        gray = image_crop.astype(np.uint8)

    crop_h, crop_w = gray.shape[:2]
    if crop_h < 2 or crop_w < 2:
        return True, float(crop_h), 0.0, 0.0, "Crop too small for profiling; returning crop height."

    # Determine background polarity using border pixels (top/bottom rows, left/right columns)
    border_pixels = np.concatenate([
        gray[0, :], gray[-1, :], gray[:, 0], gray[:, -1]
    ])
    border_median = float(np.median(border_pixels))

    # Otsu thresholding
    import cv2
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Determine foreground mask: foreground ink must contrast with border
    if border_median > 127.0:
        # Dark text on light background: ink pixels are 0 in thresh
        ink_mask = (thresh == 0).astype(np.uint8)
    else:
        # Light text on dark background: ink pixels are 255 in thresh
        ink_mask = (thresh == 255).astype(np.uint8)

    # Vertical projection profile: count ink pixels across each row y
    row_ink_counts = np.sum(ink_mask, axis=1)
    min_row_pixels = max(1, int(round(config.min_ink_row_occupancy_ratio * crop_w)))

    active_rows = np.where(row_ink_counts >= min_row_pixels)[0]
    if len(active_rows) == 0:
        return False, 0.0, 0.0, 0.0, "No foreground ink detected above noise threshold."

    y_top = int(active_rows[0])
    y_bottom = int(active_rows[-1])
    ink_height = float(y_bottom - y_top + 1)
    top_pad = float(y_top)
    bottom_pad = float(crop_h - 1 - y_bottom)

    return True, ink_height, top_pad, bottom_pad, "Ink profile successfully evaluated."


def measure_font_height(
    bounding_box: Any,
    calibration: Any,
    image: Optional[np.ndarray] = None,
    measurement_type: FontMeasurementType = FontMeasurementType.BOUNDING_BOX_HEIGHT,
    config: Optional[FontMeasurementConfig] = None,
) -> FontMeasurementResult:
    """
    Converts optical pixel measurements into physical millimeters with rigorous separation
    between OCR bounding-box height and true ink-profile glyph height.

    Mathematical Model:
    h_mm = h_px * scale_factor_mm_per_pixel

    Uncertainty Propagation Policy:
    - If calibration supplies uncertainty_scale: Delta h_mm = h_px * uncertainty_scale
    - If calibration does NOT supply uncertainty: uncertainty_mm = None (NEVER fabricated).

    Args:
        bounding_box: BoundingBox or (x_min, y_min, x_max, y_max) tuple.
        calibration: CalibrationOutcome, object with scale_factor_mm_per_pixel, or numeric scale.
        image: Optional image ndarray (required for INK_PROFILE_HEIGHT or out-of-bounds clipping).
        measurement_type: BOUNDING_BOX_HEIGHT (default) or INK_PROFILE_HEIGHT.
        config: Optional FontMeasurementConfig.

    Returns:
        FontMeasurementResult containing physical millimeters, pixel metrics, and diagnostic status.
    """
    cfg = config if config is not None else FontMeasurementConfig()

    # 1. Validate bounding box structure
    box_ok, box_status, box_msg, parsed_box = _parse_bounding_box(bounding_box)
    if not box_ok or parsed_box is None:
        return FontMeasurementResult(
            status=box_status,
            measurement_type=measurement_type,
            measured_pixels=0.0,
            message=box_msg,
        )

    orig_box = parsed_box
    is_clipped = False
    clipped_box = parsed_box

    # 2. Check and handle image boundary clipping if image is supplied
    if image is not None and isinstance(image, np.ndarray) and image.ndim >= 2:
        img_h, img_w = image.shape[:2]

        # Completely out of bounds check
        if (
            parsed_box.x_max <= 0.0
            or parsed_box.x_min >= img_w
            or parsed_box.y_max <= 0.0
            or parsed_box.y_min >= img_h
        ):
            return FontMeasurementResult(
                status=FontMeasurementStatus.OUT_OF_IMAGE_BOUNDS,
                measurement_type=measurement_type,
                measured_pixels=0.0,
                bounding_box=parsed_box,
                original_bounding_box=orig_box,
                is_clipped=False,
                message=f"Bounding box is completely outside image domain [0, {img_w}] x [0, {img_h}].",
            )

        # Coordinate clipping with explicit preservation of original box
        cx_min = max(0.0, min(float(img_w), parsed_box.x_min))
        cy_min = max(0.0, min(float(img_h), parsed_box.y_min))
        cx_max = max(0.0, min(float(img_w), parsed_box.x_max))
        cy_max = max(0.0, min(float(img_h), parsed_box.y_max))

        if cx_min != parsed_box.x_min or cy_min != parsed_box.y_min or cx_max != parsed_box.x_max or cy_max != parsed_box.y_max:
            is_clipped = True
            clipped_box = BoundingBox(x_min=cx_min, y_min=cy_min, x_max=cx_max, y_max=cy_max)

    bbox_h_px = float(clipped_box.y_max - clipped_box.y_min)

    # 3. Evaluate pixel height based on requested measurement type
    ink_h_px = None
    pad_px = None
    measured_px = bbox_h_px

    if measurement_type == FontMeasurementType.INK_PROFILE_HEIGHT:
        if image is None:
            return FontMeasurementResult(
                status=FontMeasurementStatus.FAILED_PROCESSING,
                measurement_type=measurement_type,
                measured_pixels=bbox_h_px,
                bounding_box=clipped_box,
                original_bounding_box=orig_box if is_clipped else None,
                is_clipped=is_clipped,
                bbox_height_px=bbox_h_px,
                message="INK_PROFILE_HEIGHT requires an image array to extract the glyph ink crop.",
            )

        # Extract integer crop window
        x0, y0 = int(math.floor(clipped_box.x_min)), int(math.floor(clipped_box.y_min))
        x1, y1 = int(math.ceil(clipped_box.x_max)), int(math.ceil(clipped_box.y_max))
        crop = image[y0:y1, x0:x1]

        ink_ok, extracted_ink_h, top_pad, bot_pad, ink_msg = _compute_ink_profile_height(crop, cfg)
        if not ink_ok:
            return FontMeasurementResult(
                status=FontMeasurementStatus.NO_DETECTABLE_INK,
                measurement_type=measurement_type,
                measured_pixels=0.0,
                bounding_box=clipped_box,
                original_bounding_box=orig_box if is_clipped else None,
                is_clipped=is_clipped,
                bbox_height_px=bbox_h_px,
                ink_height_px=0.0,
                padding_px=bbox_h_px,
                message=ink_msg,
            )

        ink_h_px = extracted_ink_h
        pad_px = top_pad + bot_pad
        measured_px = ink_h_px

    # 4. Validate calibration without fabricating scale
    is_cal, scale_val, unc_val, cal_status, cal_msg = _validate_calibration(calibration)

    if not is_cal or scale_val is None:
        return FontMeasurementResult(
            status=FontMeasurementStatus.UNCALIBRATED,
            measurement_type=measurement_type,
            measured_pixels=measured_px,
            scale_factor_mm_per_pixel=None,
            measured_mm=None,
            uncertainty_mm=None,
            calibration_status=cal_status,
            bounding_box=clipped_box,
            original_bounding_box=orig_box if is_clipped else None,
            is_clipped=is_clipped,
            bbox_height_px=bbox_h_px,
            ink_height_px=ink_h_px,
            padding_px=pad_px,
            message=cal_msg,
        )

    # 5. Compute physical millimeter height: h_mm = h_px * S
    h_mm = measured_px * scale_val

    # Uncertainty propagation: Delta h_mm = h_px * Delta S (if Delta S is supplied)
    h_unc_mm = None
    if unc_val is not None and unc_val > 0.0:
        h_unc_mm = round(measured_px * unc_val, 4)

    return FontMeasurementResult(
        status=FontMeasurementStatus.SUCCESS,
        measurement_type=measurement_type,
        measured_pixels=measured_px,
        scale_factor_mm_per_pixel=scale_val,
        measured_mm=round(h_mm, 4),
        uncertainty_mm=h_unc_mm,
        calibration_status=CalibrationStatus.CALIBRATED,
        bounding_box=clipped_box,
        original_bounding_box=orig_box if is_clipped else None,
        is_clipped=is_clipped,
        bbox_height_px=bbox_h_px,
        ink_height_px=ink_h_px,
        padding_px=pad_px,
        message="Font height physical measurement successful.",
    )


def measure_font_height_batch(
    boxes: List[Any],
    calibration: Any,
    image: Optional[np.ndarray] = None,
    measurement_type: FontMeasurementType = FontMeasurementType.BOUNDING_BOX_HEIGHT,
    config: Optional[FontMeasurementConfig] = None,
) -> List[FontMeasurementResult]:
    """Batch-evaluates a collection of OCR bounding boxes."""
    return [
        measure_font_height(
            bounding_box=box,
            calibration=calibration,
            image=image,
            measurement_type=measurement_type,
            config=config,
        )
        for box in boxes
    ]
