"""
Unit tests for Phase 6: Physical Font Measurement & Optical Scale Conversion.
Verifies exact scaling math, uncertainty handling, bounding box vs ink profile distinctions,
and edge-case robustness.
"""

import math
import numpy as np
import pytest
import cv2

from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_calibration import CalibrationOutcome
from nirikshak_calibration.font_measurer import (
    FontMeasurementType,
    FontMeasurementStatus,
    FontMeasurementConfig,
    FontMeasurementResult,
    measure_font_height,
    measure_font_height_batch,
)


def test_exact_synthetic_scale_conversion():
    """h_px = 100.0, scale = 0.1 mm/px -> h_mm = 10.0 mm."""
    box = (10.0, 10.0, 50.0, 110.0)  # height = 100px
    cal = CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=0.10,
        uncertainty_mm_per_pixel=0.002,
    )
    res = measure_font_height(box, cal)

    assert res.status == FontMeasurementStatus.SUCCESS
    assert res.measurement_type == FontMeasurementType.BOUNDING_BOX_HEIGHT
    assert res.measured_pixels == 100.0
    assert res.measured_mm == 10.0
    assert res.uncertainty_mm == pytest.approx(100.0 * 0.002, rel=1e-3)
    assert res.calibration_status == CalibrationStatus.CALIBRATED


def test_multiple_scale_factors():
    """Evaluates various retail optical scale factors."""
    box = (0.0, 0.0, 20.0, 40.0)  # height = 40px

    # Scale 0.05 mm/px
    res1 = measure_font_height(box, 0.05)
    assert res1.measured_mm == 2.0

    # Scale 0.08 mm/px
    res2 = measure_font_height(box, 0.08)
    assert res2.measured_mm == 3.2

    # Scale 0.125 mm/px
    res3 = measure_font_height(box, 0.125)
    assert res3.measured_mm == 5.0


def test_zero_and_negative_dimensions():
    """Rejects zero-height and inverted bounding boxes."""
    # Zero height
    box_zero = (10.0, 50.0, 40.0, 50.0)
    res_zero = measure_font_height(box_zero, 0.1)
    assert res_zero.status == FontMeasurementStatus.INVALID_BOUNDING_BOX
    assert res_zero.measured_mm is None

    # Inverted height (ymin > ymax)
    box_inv = (10.0, 60.0, 40.0, 50.0)
    res_inv = measure_font_height(box_inv, 0.1)
    assert res_inv.status == FontMeasurementStatus.INVALID_BOUNDING_BOX

    # Inverted width (xmin > xmax)
    box_inv_w = (60.0, 10.0, 50.0, 40.0)
    res_inv_w = measure_font_height(box_inv_w, 0.1)
    assert res_inv_w.status == FontMeasurementStatus.INVALID_BOUNDING_BOX


def test_non_finite_coordinates():
    """Rejects NaN and Inf coordinates in bounding box."""
    box_nan = (float("nan"), 10.0, 50.0, 60.0)
    res_nan = measure_font_height(box_nan, 0.1)
    assert res_nan.status == FontMeasurementStatus.INVALID_BOUNDING_BOX

    box_inf = (10.0, 10.0, float("inf"), 60.0)
    res_inf = measure_font_height(box_inf, 0.1)
    assert res_inf.status == FontMeasurementStatus.INVALID_BOUNDING_BOX


def test_out_of_image_bounds_and_clipping():
    """Tests complete out-of-bounds rejection and boundary coordinate clipping."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    # Completely outside image domain [0, 100] x [0, 100]
    box_out = (120.0, 120.0, 150.0, 180.0)
    res_out = measure_font_height(box_out, 0.1, image=img)
    assert res_out.status == FontMeasurementStatus.OUT_OF_IMAGE_BOUNDS

    # Partially outside: x extends to 120, y extends to 110
    box_partial = (80.0, 80.0, 120.0, 110.0)
    res_partial = measure_font_height(box_partial, 0.1, image=img)
    assert res_partial.status == FontMeasurementStatus.SUCCESS
    assert res_partial.is_clipped is True
    assert res_partial.original_bounding_box is not None
    assert res_partial.bounding_box.x_max == 100.0
    assert res_partial.bounding_box.y_max == 100.0
    assert res_partial.measured_pixels == 20.0  # 100.0 - 80.0


def test_missing_and_invalid_calibration():
    """Ensures zero scale fabrication when calibration is absent, non-finite, or <= 0."""
    box = (10.0, 10.0, 50.0, 60.0)

    # Missing calibration (None)
    res_none = measure_font_height(box, None)
    assert res_none.status == FontMeasurementStatus.UNCALIBRATED
    assert res_none.measured_mm is None
    assert res_none.uncertainty_mm is None

    # Uncalibrated outcome
    uncal = CalibrationOutcome(status=CalibrationStatus.UNCALIBRATED)
    res_uncal = measure_font_height(box, uncal)
    assert res_uncal.status == FontMeasurementStatus.UNCALIBRATED
    assert res_uncal.measured_mm is None

    # Zero scale
    res_zero = measure_font_height(box, 0.0)
    assert res_zero.status == FontMeasurementStatus.UNCALIBRATED

    # Negative scale
    res_neg = measure_font_height(box, -0.05)
    assert res_neg.status == FontMeasurementStatus.UNCALIBRATED

    # NaN scale
    res_nan = measure_font_height(box, float("nan"))
    assert res_nan.status == FontMeasurementStatus.UNCALIBRATED


def test_zero_manufactured_uncertainty():
    """Verifies that uncertainty is None when calibration outcome does NOT supply uncertainty."""
    box = (0.0, 0.0, 20.0, 50.0)
    cal_no_unc = CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=0.10,
        uncertainty_mm_per_pixel=None,  # No uncertainty supplied!
    )
    res = measure_font_height(box, cal_no_unc)
    assert res.status == FontMeasurementStatus.SUCCESS
    assert res.measured_mm == 5.0
    assert res.uncertainty_mm is None  # MUST NOT fabricate 5%!


def test_uncertainty_propagation_when_available():
    """Verifies uncertainty propagation when upstream calibration supplies uncertainty."""
    box = (0.0, 0.0, 20.0, 50.0)  # height = 50px
    cal = CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=0.10,
        uncertainty_mm_per_pixel=0.005,  # 50px * 0.005 = 0.25 mm
    )
    res = measure_font_height(box, cal)
    assert res.status == FontMeasurementStatus.SUCCESS
    assert res.measured_mm == 5.0
    assert res.uncertainty_mm == 0.25


def test_padding_sensitive_behavior_bbox_vs_ink():
    """
    CRITICAL TEST: Demonstrates that OCR bbox height differs from true ink height
    when bounding box padding exists.
    """
    # Create white canvas with a black horizontal bar (glyph) of height 30px
    # surrounded by 10px white padding on top and bottom -> bbox height = 50px
    img = np.ones((100, 100), dtype=np.uint8) * 255
    # Ink occupies y = 20 to y = 49 (height = 30px), x = 20 to 60
    img[20:50, 20:60] = 0

    ocr_box = BoundingBox(x_min=10.0, y_min=10.0, x_max=70.0, y_max=60.0)  # bbox height = 50px
    cal = CalibrationOutcome(status=CalibrationStatus.CALIBRATED, scale_factor_mm_per_pixel=0.1)

    # 1. Bounding-Box Height measurement
    res_bbox = measure_font_height(ocr_box, cal, image=img, measurement_type=FontMeasurementType.BOUNDING_BOX_HEIGHT)
    assert res_bbox.status == FontMeasurementStatus.SUCCESS
    assert res_bbox.measurement_type == FontMeasurementType.BOUNDING_BOX_HEIGHT
    assert res_bbox.measured_pixels == 50.0
    assert res_bbox.measured_mm == 5.0

    # 2. Ink-Profile Height measurement
    res_ink = measure_font_height(ocr_box, cal, image=img, measurement_type=FontMeasurementType.INK_PROFILE_HEIGHT)
    assert res_ink.status == FontMeasurementStatus.SUCCESS
    assert res_ink.measurement_type == FontMeasurementType.INK_PROFILE_HEIGHT
    assert res_ink.measured_pixels == 30.0
    assert res_ink.measured_mm == 3.0
    assert res_ink.padding_px == 20.0  # 10px top + 10px bottom

    # Crucial assertion: bbox height != ink height
    assert res_bbox.measured_pixels != res_ink.measured_pixels
    assert res_bbox.measured_mm != res_ink.measured_mm


def test_clean_synthetic_numeral_ink_profile():
    """Renders a synthetic numeral '1' and tests ink profile height."""
    img = np.ones((80, 80), dtype=np.uint8) * 255
    # Draw vertical stroke from y=25 to y=55 (height=31)
    cv2.rectangle(img, (38, 25), (42, 55), 0, thickness=-1)

    box = BoundingBox(x_min=20.0, y_min=10.0, x_max=60.0, y_max=70.0)  # bbox height = 60px
    cal = 0.05  # mm/px

    res = measure_font_height(box, cal, image=img, measurement_type=FontMeasurementType.INK_PROFILE_HEIGHT)
    assert res.status == FontMeasurementStatus.SUCCESS
    assert res.measured_pixels == 31.0
    assert res.measured_mm == pytest.approx(31.0 * 0.05, rel=1e-3)
    assert res.bbox_height_px == 60.0


def test_no_detectable_ink_in_blank_box():
    """Completely blank/uniform white box yields NO_DETECTABLE_INK."""
    img = np.ones((60, 60), dtype=np.uint8) * 255  # All white, no text
    box = (10.0, 10.0, 50.0, 50.0)
    cal = 0.1

    res = measure_font_height(box, cal, image=img, measurement_type=FontMeasurementType.INK_PROFILE_HEIGHT)
    assert res.status == FontMeasurementStatus.NO_DETECTABLE_INK
    assert res.measured_pixels == 0.0
    assert res.measured_mm is None


def test_batch_font_height_measurement():
    """Batch processes multiple bounding boxes."""
    boxes = [
        (0.0, 0.0, 20.0, 30.0),   # 30px
        (0.0, 0.0, 20.0, 50.0),   # 50px
        (0.0, 0.0, 20.0, 80.0),   # 80px
    ]
    cal = 0.1
    results = measure_font_height_batch(boxes, cal)

    assert len(results) == 3
    assert [r.measured_mm for r in results] == [3.0, 5.0, 8.0]


def test_bridge_to_shared_measurement_result():
    """Verifies that .to_measurement_result() creates valid nirikshak_shared MeasurementResult."""
    box = (10.0, 10.0, 40.0, 50.0)
    cal = CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=0.08,
        uncertainty_mm_per_pixel=0.002,
    )
    res = measure_font_height(box, cal)
    shared_res = res.to_measurement_result(feature_name="numeral_height_mm")

    assert shared_res.feature_name == "numeral_height_mm"
    assert shared_res.measured_pixels == 40.0
    assert shared_res.measured_mm == pytest.approx(40.0 * 0.08, rel=1e-3)
    assert shared_res.calibration_status == CalibrationStatus.CALIBRATED
    assert shared_res.uncertainty_mm == pytest.approx(40.0 * 0.002, rel=1e-3)


def test_deterministic_repeated_execution():
    """Bitwise identical results on repeated calls."""
    box = (12.4, 18.9, 45.1, 78.6)
    cal = CalibrationOutcome(status=CalibrationStatus.CALIBRATED, scale_factor_mm_per_pixel=0.075)

    res1 = measure_font_height(box, cal)
    res2 = measure_font_height(box, cal)

    assert res1.measured_pixels == res2.measured_pixels
    assert res1.measured_mm == res2.measured_mm
    assert res1.status == res2.status
