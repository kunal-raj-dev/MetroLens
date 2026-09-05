"""
Nirikshak Measurement: Physical dimension calculations, font height conversion, and PDP area computation.
"""

from typing import Optional, Dict
from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_shared.models.contracts import MeasurementResult


def calculate_font_height_mm(
    pixel_height: float,
    scale_factor_mm_per_pixel: Optional[float],
    uncertainty_scale: Optional[float] = None,
) -> MeasurementResult:
    """
    Converts font height from pixels to physical millimeters using optical calibration scale factor.
    """
    if scale_factor_mm_per_pixel is None or scale_factor_mm_per_pixel <= 0:
        return MeasurementResult(
            feature_name="font_height",
            measured_pixels=pixel_height,
            calibration_status=CalibrationStatus.UNCALIBRATED,
        )

    height_mm = pixel_height * scale_factor_mm_per_pixel
    unc_mm = (pixel_height * uncertainty_scale) if uncertainty_scale is not None else (height_mm * 0.05)

    return MeasurementResult(
        feature_name="font_height",
        measured_pixels=pixel_height,
        scale_factor_mm_per_pixel=scale_factor_mm_per_pixel,
        measured_mm=round(height_mm, 3),
        uncertainty_mm=round(unc_mm, 3),
        calibration_status=CalibrationStatus.CALIBRATED,
    )


def calculate_pdp_area_cm2(width_mm: float, height_mm: float) -> float:
    """Computes rectangular PDP area in square centimeters (cm^2)."""
    return (width_mm * height_mm) / 100.0


__all__ = ["calculate_font_height_mm", "calculate_pdp_area_cm2", "MeasurementResult"]
