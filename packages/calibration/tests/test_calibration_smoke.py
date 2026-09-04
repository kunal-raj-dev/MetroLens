"""
Smoke test for nirikshak-calibration.
"""

from nirikshak_calibration import compute_scale_factor, CalibrationStatus


def test_compute_scale_factor_valid():
    # 25.0 mm reference coin measured at 500 pixels in image
    res = compute_scale_factor(measured_marker_pixels=500.0, known_marker_mm=25.0)
    assert res.status == CalibrationStatus.CALIBRATED
    assert res.scale_factor_mm_per_pixel == 0.05
    assert res.uncertainty_mm_per_pixel is not None
    assert res.uncertainty_mm_per_pixel > 0


def test_compute_scale_factor_invalid():
    res = compute_scale_factor(measured_marker_pixels=0.0, known_marker_mm=25.0)
    assert res.status == CalibrationStatus.UNCALIBRATED
    assert res.scale_factor_mm_per_pixel is None
