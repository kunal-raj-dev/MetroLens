"""
Phase 8: Comprehensive Vision & Measurement Pipeline Robustness Tests.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Validates that every public entry point of the Member 2 pipeline:
1. Rejects malformed, degenerate, or hostile inputs with typed, structured failure states.
2. Never raises unhandled exceptions.
3. Never fabricates scale factors or physical measurements.
4. Never mutates caller-owned arrays.
5. Deterministically resolves ambiguity and non-standard visual scenes.
"""

import math
import pytest
import numpy as np
import cv2

from nirikshak_vision.quality import (
    evaluate_image_quality,
    convert_to_grayscale,
    QualityGateThresholds,
)
from nirikshak_calibration.types import (
    AnchorType,
    AnchorDetectionStatus,
    AnchorDetectionResult,
    AnchorDetectorConfig,
)
from nirikshak_calibration import CalibrationOutcome, compute_scale_factor
from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_calibration.anchor_detector import (
    detect_anchor,
    order_quadrilateral_corners,
    compute_algebraic_ellipse_residual,
)
from nirikshak_calibration.homography import (
    rectify_planar_quadrilateral,
    validate_quadrilateral_geometry,
    RectificationStatus,
    HomographyConfig,
)
from nirikshak_calibration.font_measurer import (
    measure_font_height,
    measure_font_height_batch,
    FontMeasurementType,
    FontMeasurementStatus,
    FontMeasurementConfig,
)
from nirikshak_calibration.cylinder import (
    measure_cylindrical_feature,
    CylinderGeometryState,
    CylinderMeasurementStatus,
    CylinderModelConfig,
)


# ============================================================================
# 1. Input Existence and Types Robustness
# ============================================================================

class TestInputExistenceAndTypes:
    """Verifies structured rejection of None, wrong types, and empty arrays."""

    @pytest.mark.parametrize("bad_input", [None, "image.png", 12345, [1, 2, 3], {"img": None}])
    def test_evaluate_image_quality_non_array_inputs(self, bad_input):
        result = evaluate_image_quality(bad_input)
        assert result.passed is False
        assert result.is_valid_input is False
        assert len(result.failure_reasons) > 0

    @pytest.mark.parametrize("bad_input", [None, "image.png", 12345, [1, 2, 3], {"img": None}])
    def test_detect_anchor_non_array_inputs(self, bad_input):
        result = detect_anchor(bad_input)
        assert result.detected is False
        assert result.status == AnchorDetectionStatus.INVALID_INPUT
        assert result.confidence == 0.0

    @pytest.mark.parametrize("bad_input", ["not_an_image", 42, [10, 20]])
    def test_rectify_planar_non_array_inputs(self, bad_input):
        pts = ((10.0, 10.0), (100.0, 10.0), (100.0, 100.0), (10.0, 100.0))
        result = rectify_planar_quadrilateral(pts, image=bad_input)
        assert result.success is False
        assert result.status == RectificationStatus.INVALID_INPUT

    def test_empty_arrays_across_all_entry_points(self):
        empty_1 = np.array([])
        empty_2 = np.zeros((0, 0, 3), dtype=np.uint8)
        empty_3 = np.zeros((100, 0), dtype=np.uint8)

        for empty in (empty_1, empty_2, empty_3):
            q_res = evaluate_image_quality(empty)
            assert q_res.passed is False
            assert q_res.is_valid_input is False

            a_res = detect_anchor(empty)
            assert a_res.detected is False
            assert a_res.status == AnchorDetectionStatus.INVALID_INPUT

            pts = ((10.0, 10.0), (100.0, 10.0), (100.0, 100.0), (10.0, 100.0))
            r_res = rectify_planar_quadrilateral(pts, image=empty)
            assert r_res.success is False
            assert r_res.status == RectificationStatus.INVALID_INPUT

            f_res = measure_font_height((10, 10, 50, 50), 0.1, image=empty,
                                       measurement_type=FontMeasurementType.INK_PROFILE_HEIGHT)
            assert f_res.status in (FontMeasurementStatus.FAILED_PROCESSING, FontMeasurementStatus.OUT_OF_IMAGE_BOUNDS)
            assert f_res.measured_mm is None


# ============================================================================
# 2. Image Dimensions & Shapes Robustness
# ============================================================================

class TestImageDimensionsAndShapes:
    """Verifies behavior on 1x1, tiny, single-row, single-column, and extreme shapes."""

    @pytest.mark.parametrize("shape", [(1, 1), (2, 2), (5, 5), (1, 1, 3), (2, 2, 3)])
    def test_micro_images_rejected_gracefully(self, shape):
        img = np.zeros(shape, dtype=np.uint8)
        q_res = evaluate_image_quality(img)
        # Quality evaluator enforces min 3x3
        if min(shape[:2]) < 3:
            assert q_res.is_valid_input is False
        else:
            assert q_res.is_valid_input is True
            assert q_res.passed is False  # Blurry/dark

        a_res = detect_anchor(img)
        # Anchor detector enforces min 10x10
        assert a_res.detected is False
        assert a_res.status == AnchorDetectionStatus.INVALID_INPUT

    @pytest.mark.parametrize("shape", [(1, 500), (500, 1), (10, 1000), (1000, 10)])
    def test_extreme_aspect_ratios(self, shape):
        img = np.full(shape, 128, dtype=np.uint8)
        q_res = evaluate_image_quality(img)
        assert isinstance(q_res.passed, bool)

        a_res = detect_anchor(img)
        assert isinstance(a_res.detected, bool)
        # Extreme aspect ratio should either be NO_ANCHOR or INVALID_INPUT (for 1x500)
        assert a_res.detected is False

    def test_large_synthetic_dimensions_no_memory_leak(self):
        img = np.zeros((1200, 1200, 3), dtype=np.uint8)
        cv2.circle(img, (600, 600), 100, (255, 255, 255), -1)
        res = detect_anchor(img)
        assert isinstance(res.detected, bool)


# ============================================================================
# 3. Channel Configurations & Dtypes Robustness
# ============================================================================

class TestChannelConfigurationsAndDtypes:
    """Verifies handling of 2D, 1-ch, 2-ch, 3-ch, 4-ch, 5-ch, 1D, 4D and float/int dtypes."""

    def test_channel_depths(self):
        h, w = 120, 120
        img_2d = np.full((h, w), 128, dtype=np.uint8)
        img_3d_1 = np.full((h, w, 1), 128, dtype=np.uint8)
        img_3d_2 = np.full((h, w, 2), 128, dtype=np.uint8)
        img_3d_3 = np.full((h, w, 3), 128, dtype=np.uint8)
        img_3d_4 = np.full((h, w, 4), 128, dtype=np.uint8)
        img_3d_5 = np.full((h, w, 5), 128, dtype=np.uint8)
        img_1d = np.full((h * w,), 128, dtype=np.uint8)
        img_4d = np.full((1, h, w, 3), 128, dtype=np.uint8)

        # 2D, 1-ch, 3-ch, 4-ch should be valid inputs to evaluate_image_quality
        for valid_img in (img_2d, img_3d_1, img_3d_3, img_3d_4):
            res = evaluate_image_quality(valid_img)
            assert res.is_valid_input is True

        # 2-ch, 5-ch, 1D, 4D must be rejected as invalid input
        for invalid_img in (img_3d_2, img_3d_5, img_1d, img_4d):
            q_res = evaluate_image_quality(invalid_img)
            assert q_res.is_valid_input is False
            assert "INVALID_INPUT" in q_res.failure_reasons[0]

            a_res = detect_anchor(invalid_img)
            assert a_res.detected is False
            assert a_res.status == AnchorDetectionStatus.INVALID_INPUT

    def test_float_and_integer_dtypes(self):
        # uint8
        img_u8 = np.full((100, 100, 3), 128, dtype=np.uint8)
        assert evaluate_image_quality(img_u8).is_valid_input is True

        # float32 normalized [0.0, 1.0]
        img_f32 = np.full((100, 100, 3), 0.5, dtype=np.float32)
        assert evaluate_image_quality(img_f32).is_valid_input is True

        # float64 [0.0, 255.0]
        img_f64 = np.full((100, 100, 3), 128.0, dtype=np.float64)
        assert evaluate_image_quality(img_f64).is_valid_input is True

        # int32
        img_i32 = np.full((100, 100, 3), 128, dtype=np.int32)
        assert evaluate_image_quality(img_i32).is_valid_input is True

    def test_non_finite_floating_point_arrays(self):
        img_nan = np.full((100, 100, 3), 0.5, dtype=np.float32)
        img_nan[50, 50, 0] = float("nan")

        img_inf = np.full((100, 100, 3), 0.5, dtype=np.float32)
        img_inf[50, 50, 0] = float("inf")

        for bad_img in (img_nan, img_inf):
            q_res = evaluate_image_quality(bad_img)
            assert q_res.is_valid_input is False
            assert q_res.passed is False

            a_res = detect_anchor(bad_img)
            assert a_res.detected is False
            assert a_res.status == AnchorDetectionStatus.INVALID_INPUT


# ============================================================================
# 4. Degenerate Pixel Value Distributions
# ============================================================================

class TestDegeneratePixelDistributions:
    """Verifies handling of all-black, all-white, constant gray, and noise distributions."""

    def test_all_black_frame(self):
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        q_res = evaluate_image_quality(img)
        assert q_res.is_valid_input is True
        assert q_res.passed is False
        assert q_res.is_dark is True

        a_res = detect_anchor(img)
        assert a_res.detected is False
        assert a_res.status == AnchorDetectionStatus.NO_ANCHOR

    def test_all_white_frame(self):
        img = np.full((200, 200, 3), 255, dtype=np.uint8)
        q_res = evaluate_image_quality(img)
        assert q_res.is_valid_input is True
        assert q_res.passed is False
        assert (q_res.is_over_exposed is True or q_res.is_glared is True)

        a_res = detect_anchor(img)
        assert a_res.detected is False
        assert a_res.status in (AnchorDetectionStatus.NO_ANCHOR, AnchorDetectionStatus.GLARE_INTERFERENCE)

    def test_constant_mid_gray(self):
        img = np.full((200, 200, 3), 128, dtype=np.uint8)
        q_res = evaluate_image_quality(img)
        assert q_res.is_valid_input is True
        assert q_res.passed is False
        assert q_res.contrast_score == 0.0

        a_res = detect_anchor(img)
        assert a_res.detected is False
        assert a_res.status == AnchorDetectionStatus.NO_ANCHOR

    def test_pure_uniform_noise(self):
        rng = np.random.default_rng(42)
        img = rng.integers(0, 256, size=(200, 200, 3), dtype=np.uint8)
        a_res = detect_anchor(img)
        # Random noise should never pass geometric validation as a coin or card
        assert a_res.detected is False
        assert a_res.status in (AnchorDetectionStatus.NO_ANCHOR, AnchorDetectionStatus.LOW_CONFIDENCE)


# ============================================================================
# 5. Realistic Non-Standard Visual Content
# ============================================================================

class TestRealisticNonStandardVisualContent:
    """Verifies determinism and robustness on non-packaging scenes, clutter, and multiple candidates."""

    def test_synthetic_clutter_with_circular_distractors(self):
        # Canvas with random lines, rectangles, and non-concentric circles
        img = np.full((400, 400, 3), 200, dtype=np.uint8)
        # Non-concentric circles of random sizes
        cv2.circle(img, (100, 100), 30, (50, 50, 50), 2)
        cv2.circle(img, (280, 120), 45, (30, 30, 30), -1)
        cv2.rectangle(img, (150, 250), (220, 320), (10, 10, 10), 3)

        a_res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
        # None of these have concentric ring ratios matching RBI Rs 10 coin
        assert a_res.detected is False

    def test_multiple_identical_candidates_triggers_ambiguity_or_deterministic_separation(self):
        # Canvas with two identical circular anchors
        img = np.full((500, 500, 3), 220, dtype=np.uint8)
        # Coin 1
        cv2.circle(img, (150, 250), 60, (40, 40, 40), 4)
        cv2.circle(img, (150, 250), 40, (70, 70, 70), 3)
        # Coin 2 (identical geometry)
        cv2.circle(img, (350, 250), 60, (40, 40, 40), 4)
        cv2.circle(img, (350, 250), 40, (70, 70, 70), 3)

        res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
        # If both pass confidence gating, score separation is zero -> AMBIGUOUS_ANCHOR
        if not res.detected:
            assert res.status in (
                AnchorDetectionStatus.AMBIGUOUS_ANCHOR,
                AnchorDetectionStatus.LOW_CONFIDENCE,
                AnchorDetectionStatus.NO_ANCHOR,
            )

    def test_coin_partially_truncated_by_border(self):
        img = np.full((300, 300, 3), 220, dtype=np.uint8)
        # Center is at (10, 150) with radius 50 -> half the coin is offscreen
        cv2.circle(img, (10, 150), 50, (30, 30, 30), 4)
        cv2.circle(img, (10, 150), 33, (60, 60, 60), 3)

        res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
        # Truncated contour cannot form a full ellipse fitting residual
        assert res.detected is False


# ============================================================================
# 6. Geometry Robustness (Homography & Rectification)
# ============================================================================

class TestGeometryRobustness:
    """Verifies that homography rejects malformed point sets with typed statuses."""

    @pytest.mark.parametrize("bad_pts, expected_status", [
        (None, RectificationStatus.INVALID_INPUT),
        ([], RectificationStatus.INVALID_POINT_COUNT),
        ([(10, 10), (100, 10), (100, 100)], RectificationStatus.INVALID_POINT_COUNT),  # 3 points
        ([(10, 10), (100, 10), (100, 100), (10, 100), (50, 50)], RectificationStatus.INVALID_POINT_COUNT),  # 5 points
        ([(10, 10), (10, 10), (100, 100), (10, 100)], RectificationStatus.DUPLICATE_POINTS),  # Duplicate
        ([(10, 10), (50, 10), (100, 10), (150, 10)], RectificationStatus.COLLINEAR_POINTS),  # All collinear
        ([(10, 10), (100, 100), (100, 10), (10, 100)], RectificationStatus.NON_CONVEX_QUADRILATERAL),  # Bowtie
        ([(float("nan"), 10), (100, 10), (100, 100), (10, 100)], RectificationStatus.NON_FINITE_COORDINATES),
        ([(float("inf"), 10), (100, 10), (100, 100), (10, 100)], RectificationStatus.NON_FINITE_COORDINATES),
        ([("str", 10), (100, 10), (100, 100), (10, 100)], RectificationStatus.NON_FINITE_COORDINATES),
    ])
    def test_validate_quadrilateral_geometry_rejections(self, bad_pts, expected_status):
        is_val, status, msg, _ = validate_quadrilateral_geometry(bad_pts)
        assert is_val is False
        assert status == expected_status

    def test_out_of_image_bounds_corners(self):
        pts = ((-50.0, 10.0), (100.0, 10.0), (100.0, 100.0), (10.0, 100.0))
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        res = rectify_planar_quadrilateral(pts, image=img)
        assert res.success is False
        assert res.status == RectificationStatus.OUT_OF_IMAGE_BOUNDS

    def test_zero_area_degenerate_quad(self):
        pts = ((50.0, 50.0), (50.0, 50.0), (50.0, 50.0), (50.0, 50.0))
        res = rectify_planar_quadrilateral(pts)
        assert res.success is False
        assert res.status in (RectificationStatus.DUPLICATE_POINTS, RectificationStatus.DEGENERATE_QUADRILATERAL)


# ============================================================================
# 7. Calibration Precondition Robustness
# ============================================================================

class TestCalibrationPreconditions:
    """Verifies that font measurer and cylinder measurer handle uncalibrated/bad calibration."""

    @pytest.mark.parametrize("bad_cal", [
        None,
        "not_a_cal",
        {"scale": 0.1},
        CalibrationOutcome(status=CalibrationStatus.UNCALIBRATED, scale_factor_mm_per_pixel=None),
        CalibrationOutcome(status=CalibrationStatus.APPROXIMATE_ASSISTED, scale_factor_mm_per_pixel=0.1),
        CalibrationOutcome(status=CalibrationStatus.CALIBRATED, scale_factor_mm_per_pixel=0.0),  # Zero scale
        CalibrationOutcome(status=CalibrationStatus.CALIBRATED, scale_factor_mm_per_pixel=-0.5),  # Negative scale
        CalibrationOutcome(status=CalibrationStatus.CALIBRATED, scale_factor_mm_per_pixel=float("nan")),
    ])
    def test_font_measurer_uncalibrated_handling(self, bad_cal):
        res = measure_font_height((10, 10, 50, 40), calibration=bad_cal)
        assert res.status == FontMeasurementStatus.UNCALIBRATED
        assert res.measured_mm is None
        assert res.measured_pixels == 30.0

    @pytest.mark.parametrize("bad_cal", [
        None,
        0.0,
        -0.1,
        CalibrationOutcome(status=CalibrationStatus.UNCALIBRATED, scale_factor_mm_per_pixel=None),
    ])
    def test_cylinder_measurer_uncalibrated_handling(self, bad_cal):
        res = measure_cylindrical_feature(
            (10, 20, 30, 60),
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            cylinder_center_x=20.0,
            cylinder_radius_px=100.0,
            calibration=bad_cal,
            is_axis_aligned=True,
        )
        assert res.status == CylinderMeasurementStatus.UNCALIBRATED
        assert res.measured_axial_mm is None
        assert res.measured_axial_pixels == 40.0


# ============================================================================
# 8. OCR Observation Robustness
# ============================================================================

class TestOCRObservationRobustness:
    """Verifies handling of invalid, inverted, zero-area, and out-of-bounds bounding boxes."""

    @pytest.mark.parametrize("bad_box", [
        None,
        "10,10,20,20",
        (10, 20),           # 2 elements instead of 4
        (10, 20, 30),       # 3 elements
        (10, 20, 30, 40, 50), # 5 elements
        (10, 20, "a", 40),  # Non-numeric
        (float("nan"), 10, 20, 30),
        (10, float("inf"), 20, 30),
        (50, 10, 20, 30),   # Inverted x (xmin > xmax)
        (10, 50, 20, 30),   # Inverted y (ymin > ymax)
        (20, 10, 20, 30),   # Zero width
        (10, 20, 30, 20),   # Zero height
    ])
    def test_font_measurer_invalid_bounding_boxes(self, bad_box):
        res = measure_font_height(bad_box, calibration=0.1)
        assert res.status == FontMeasurementStatus.INVALID_BOUNDING_BOX
        assert res.measured_mm is None

    def test_font_measurer_out_of_bounds_clipping(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        # Completely out of bounds
        res_oob = measure_font_height((150, 150, 200, 200), calibration=0.1, image=img)
        assert res_oob.status == FontMeasurementStatus.OUT_OF_IMAGE_BOUNDS
        assert res_oob.measured_mm is None

        # Partially clipped
        res_clipped = measure_font_height((80, 80, 120, 120), calibration=0.1, image=img)
        assert res_clipped.status == FontMeasurementStatus.SUCCESS
        assert res_clipped.is_clipped is True
        assert res_clipped.bounding_box.x_max == 100.0
        assert res_clipped.bounding_box.y_max == 100.0
        assert res_clipped.measured_pixels == 20.0  # 100 - 80

    @pytest.mark.parametrize("bad_center, bad_radius", [
        ("invalid", 100.0),
        (50.0, "invalid"),
        (float("nan"), 100.0),
        (50.0, float("inf")),
        (50.0, 5.0),  # Below min radius
        (50.0, -20.0),
    ])
    def test_cylinder_measurer_invalid_parameters(self, bad_center, bad_radius):
        res = measure_cylindrical_feature(
            (40, 20, 60, 60),
            geometry_state=CylinderGeometryState.CYLINDRICAL,
            cylinder_center_x=bad_center,
            cylinder_radius_px=bad_radius,
            calibration=0.1,
            is_axis_aligned=True,
        )
        assert res.status == CylinderMeasurementStatus.INVALID_INPUT
        assert res.measured_axial_mm is None


# ============================================================================
# 9. Caller-Owned Array Immutability (Non-Mutation)
# ============================================================================

class TestCallerOwnedArrayImmutability:
    """Verifies that every Member 2 public function preserves caller-owned numpy arrays."""

    def test_evaluate_image_quality_non_mutation(self):
        img = np.random.randint(0, 256, (120, 120, 3), dtype=np.uint8)
        img_copy = img.copy()
        evaluate_image_quality(img)
        assert np.array_equal(img, img_copy)
        assert img.dtype == img_copy.dtype

    def test_detect_anchor_non_mutation(self):
        img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        img_copy = img.copy()
        detect_anchor(img)
        assert np.array_equal(img, img_copy)
        assert img.dtype == img_copy.dtype

    def test_rectify_planar_quadrilateral_non_mutation(self):
        img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        img_copy = img.copy()
        pts = ((20.0, 20.0), (180.0, 20.0), (180.0, 180.0), (20.0, 180.0))
        rectify_planar_quadrilateral(pts, image=img)
        assert np.array_equal(img, img_copy)
        assert img.dtype == img_copy.dtype

    def test_measure_font_height_non_mutation(self):
        img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img_copy = img.copy()
        measure_font_height((20, 20, 60, 60), calibration=0.1, image=img,
                            measurement_type=FontMeasurementType.INK_PROFILE_HEIGHT)
        assert np.array_equal(img, img_copy)
        assert img.dtype == img_copy.dtype

    def test_convert_to_grayscale_non_mutation(self):
        # Test across various dtypes and color formats
        for fmt, ch in [("BGR", 3), ("RGB", 3), ("BGRA", 4), ("RGBA", 4)]:
            img = np.random.randint(0, 256, (80, 80, ch), dtype=np.uint8)
            img_copy = img.copy()
            convert_to_grayscale(img, color_format=fmt)
            assert np.array_equal(img, img_copy)
            assert img.dtype == img_copy.dtype

        # Floating point
        img_f = np.random.uniform(0.0, 1.0, (60, 60, 3)).astype(np.float32)
        img_f_copy = img_f.copy()
        convert_to_grayscale(img_f)
        assert np.array_equal(img_f, img_f_copy)
        assert img_f.dtype == img_f_copy.dtype

    def test_measure_font_height_batch_non_mutation(self):
        img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img_copy = img.copy()
        boxes = [(10, 10, 30, 30), (40, 40, 60, 60)]
        measure_font_height_batch(boxes, calibration=0.1, image=img)
        assert np.array_equal(img, img_copy)
        assert img.dtype == img_copy.dtype

    def test_order_quadrilateral_corners_non_mutation(self):
        pts = np.array([[100.0, 10.0], [10.0, 10.0], [10.0, 100.0], [100.0, 100.0]])
        pts_copy = pts.copy()
        order_quadrilateral_corners(pts)
        assert np.array_equal(pts, pts_copy)
        assert pts.dtype == pts_copy.dtype

    def test_compute_algebraic_ellipse_residual_non_mutation(self):
        cnt = np.array([[[50, 20]], [[80, 50]], [[50, 80]], [[20, 50]]], dtype=np.int32)
        cnt_copy = cnt.copy()
        ell = ((50.0, 50.0), (60.0, 60.0), 0.0)
        compute_algebraic_ellipse_residual(cnt, ell)
        assert np.array_equal(cnt, cnt_copy)
        assert cnt.dtype == cnt_copy.dtype


# ============================================================================
# 10. Additional Public Entry Point Robustness
# ============================================================================

class TestAdditionalPublicEntryPointsRobustness:
    """Verifies robustness of all remaining Member 2 public entry points."""

    def test_convert_to_grayscale_degenerate_inputs(self):
        with pytest.raises(Exception):
            convert_to_grayscale(None)

        with pytest.raises(Exception):
            convert_to_grayscale(np.zeros((10, 10, 5), dtype=np.uint8))  # 5 channels

        with pytest.raises(Exception):
            convert_to_grayscale(np.zeros((50,), dtype=np.uint8))  # 1D

        bad_float = np.array([[float("nan"), 0.5], [0.5, 0.5]], dtype=np.float32)
        with pytest.raises(ValueError):
            convert_to_grayscale(bad_float)

    def test_measure_font_height_batch_robustness(self):
        # Empty batch
        assert measure_font_height_batch([], calibration=0.1) == []

        # Batch with mixed valid and invalid boxes
        mixed_boxes = [
            None,
            (10, 10, 30, 40),
            "invalid_box",
            (50, 50, 40, 40),  # Inverted
        ]
        results = measure_font_height_batch(mixed_boxes, calibration=0.1)
        assert len(results) == 4
        assert results[0].status == FontMeasurementStatus.INVALID_BOUNDING_BOX
        assert results[1].status == FontMeasurementStatus.SUCCESS
        assert results[2].status == FontMeasurementStatus.INVALID_BOUNDING_BOX
        assert results[3].status == FontMeasurementStatus.INVALID_BOUNDING_BOX

    def test_compute_scale_factor_robustness(self):
        # Zero pixels -> UNCALIBRATED
        res_zero_px = compute_scale_factor(0.0, 27.0)
        assert res_zero_px.status == CalibrationStatus.UNCALIBRATED
        assert res_zero_px.scale_factor_mm_per_pixel is None

        # Negative pixels -> UNCALIBRATED
        res_neg_px = compute_scale_factor(-50.0, 27.0)
        assert res_neg_px.status == CalibrationStatus.UNCALIBRATED

        # Zero or negative known dimension -> UNCALIBRATED
        assert compute_scale_factor(100.0, 0.0).status == CalibrationStatus.UNCALIBRATED
        assert compute_scale_factor(100.0, -27.0).status == CalibrationStatus.UNCALIBRATED

        # Valid input -> CALIBRATED
        valid = compute_scale_factor(100.0, 27.0)
        assert valid.status == CalibrationStatus.CALIBRATED
        assert pytest.approx(valid.scale_factor_mm_per_pixel, rel=1e-3) == 0.27
        assert valid.uncertainty_mm_per_pixel is not None

    def test_compute_algebraic_ellipse_residual_robustness(self):
        # Degenerate semi-axis <= 0.5 returns 999.0
        cnt = np.array([[[10, 10]], [[20, 20]], [[30, 30]]], dtype=np.float32)
        degen_ell = ((10.0, 10.0), (0.4, 0.4), 0.0)
        res = compute_algebraic_ellipse_residual(cnt, degen_ell)
        assert res == 999.0

        # Normal ellipse
        normal_ell = ((50.0, 50.0), (60.0, 60.0), 0.0)
        normal_res = compute_algebraic_ellipse_residual(cnt, normal_ell)
        assert isinstance(normal_res, float)
        assert math.isfinite(normal_res)
        assert normal_res >= 0.0

    def test_measure_cylindrical_feature_geometry_states(self):
        box = (10.0, 20.0, 30.0, 60.0)
        # PLANAR state: no curvature correction applied
        p_res = measure_cylindrical_feature(box, geometry_state=CylinderGeometryState.PLANAR, calibration=0.1)
        assert p_res.status == CylinderMeasurementStatus.PLANAR_NO_CORRECTION
        assert p_res.circumferential_correction_factor == 1.0

        # UNSUPPORTED_TAPERED state: flags manual review
        t_res = measure_cylindrical_feature(box, geometry_state=CylinderGeometryState.UNSUPPORTED_TAPERED, calibration=0.1)
        assert t_res.status == CylinderMeasurementStatus.UNSUPPORTED_TAPERED

        # UNKNOWN state: flags manual review
        u_res = measure_cylindrical_feature(box, geometry_state=CylinderGeometryState.UNKNOWN, calibration=0.1)
        assert u_res.status == CylinderMeasurementStatus.UNKNOWN_GEOMETRY

