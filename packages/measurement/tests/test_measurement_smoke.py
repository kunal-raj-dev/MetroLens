"""
Smoke test for nirikshak-measurement.
"""

from nirikshak_measurement import calculate_font_height_mm, calculate_pdp_area_cm2
from nirikshak_shared.models.primitives import CalibrationStatus


def test_calculate_font_height_calibrated():
    res = calculate_font_height_mm(pixel_height=40.0, scale_factor_mm_per_pixel=0.05)
    assert res.calibration_status == CalibrationStatus.CALIBRATED
    assert res.measured_mm == 2.0
    assert res.uncertainty_mm is not None


def test_calculate_font_height_uncalibrated():
    res = calculate_font_height_mm(pixel_height=40.0, scale_factor_mm_per_pixel=None)
    assert res.calibration_status == CalibrationStatus.UNCALIBRATED
    assert res.measured_mm is None


def test_calculate_pdp_area():
    area = calculate_pdp_area_cm2(width_mm=100.0, height_mm=200.0)
    assert area == 200.0  # 20,000 mm^2 / 100 = 200 cm^2
