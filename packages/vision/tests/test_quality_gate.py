"""
Unit test suite for Nirikshak Vision pre-flight image quality gate.

Verifies deterministic behavior for:
- Progressive Gaussian blur monotonicity and rejection.
- Specular glare candidate isolation vs diffuse white label false-positive resilience.
- Illumination / exposure bounds (underexposure, normal, overexposure).
- Malformed, degenerate, and edge-case array handling without unhandled crashes.
- Execution latency adherence to NFR-01.1 (<= 300 ms per frame).
"""

import time
import cv2
import numpy as np
import pytest

from nirikshak_vision import check_image_quality
from nirikshak_vision.types import (
    QualityGateThresholds,
    QualityGateResult,
    ImageQualityResult,
    ImageQualityThresholds,
)
from nirikshak_vision.quality import (
    evaluate_image_quality,
    compute_laplacian_variance,
    compute_glare_candidate_ratio,
    compute_contrast,
    compute_mean_luminance,
    convert_to_grayscale,
)



# ============================================================================
# Deterministic Test Fixtures
# ============================================================================

def make_sharp_high_frequency_fixture(width: int = 400, height: int = 400) -> np.ndarray:
    """
    Generates a deterministic high-contrast pattern simulating packaging text/barcode grid.
    Uses high-contrast print intensities (30 for dark ink, 210 for light background),
    avoiding artificial saturation clipping while providing sharp step edges.
    """
    img = np.full((height, width, 3), 120, dtype=np.uint8)
    # High-frequency horizontal and vertical print grid
    for y in range(0, height, 10):
        img[y:y+2, :, :] = 210 if (y // 10) % 2 == 0 else 30
    for x in range(0, width, 10):
        img[:, x:x+2, :] = 210 if (x // 10) % 2 == 0 else 30
    # Sharp diagonal line transitions
    cv2.line(img, (0, 0), (width, height), (210, 210, 210), thickness=2)
    cv2.line(img, (width, 0), (0, height), (30, 30, 30), thickness=2)
    return img


def make_diffuse_white_label_fixture(width: int = 400, height: int = 400) -> np.ndarray:
    """
    Simulates a standard packaging surface with a large diffuse white paper label.
    The label is diffuse (intensity ~240-248 with subtle printed marks), NOT specular glare.
    """
    # Midtone packaging background (e.g. cardboard / pouch)
    img = np.full((height, width, 3), 100, dtype=np.uint8)
    # Centered white paper label covering ~40% of the image area
    label_x1, label_y1 = 80, 80
    label_x2, label_y2 = 320, 320
    img[label_y1:label_y2, label_x1:label_x2] = 245
    # Add simulated printed text markings on the label
    for y in range(100, 300, 20):
        cv2.putText(
            img,
            "NET QTY 500g",
            (100, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (20, 20, 20),
            1,
            cv2.LINE_AA,
        )
    return img


def make_specular_glare_fixture(
    width: int = 400,
    height: int = 400,
    glare_radius: int = 50,
) -> np.ndarray:
    """
    Simulates a packaging surface with a localized specular glare hotspot.
    Features a saturated core (255) with a steep intensity roll-off.
    """
    # Midtone packaging background
    img = np.full((height, width, 3), 80, dtype=np.uint8)
    center = (width // 2, height // 2)
    # Bright specular hotspot
    cv2.circle(img, center, glare_radius, (255, 255, 255), -1)
    return img


# ============================================================================
# 1. Blur Metric Tests
# ============================================================================

def test_blur_progressive_monotonicity():
    """Verifies that progressive Gaussian blurring monotonically degrades blur_score."""
    sharp = make_sharp_high_frequency_fixture()
    gray_sharp = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
    sharp_score = compute_laplacian_variance(gray_sharp)

    # Sharp fixture must have a high blur score
    assert sharp_score > 500.0

    sigmas = [1.0, 2.0, 4.0, 8.0]
    previous_score = sharp_score

    for sigma in sigmas:
        ksize = int(2 * round(3 * sigma) + 1)
        blurred = cv2.GaussianBlur(sharp, (ksize, ksize), sigmaX=sigma)
        gray_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        score = compute_laplacian_variance(gray_blurred)

        # Blur score must decrease meaningfully with increased blur
        assert score < previous_score * 0.85, f"Expected blur score to decrease meaningfully at sigma={sigma}"
        previous_score = score


def test_sharp_image_passes_quality_gate():
    """Verifies that a sharp, properly exposed packaging frame passes the gate."""
    sharp = make_sharp_high_frequency_fixture()
    res = evaluate_image_quality(sharp)

    assert res.passed is True
    assert res.is_blurry is False
    assert res.is_glared is False
    assert res.is_under_exposed is False
    assert res.is_over_exposed is False
    assert len(res.remediation_cues) == 0


def test_severely_blurred_image_is_rejected():
    """Verifies that heavily blurred images are rejected with actionable guidance."""
    sharp = make_sharp_high_frequency_fixture()
    blurred = cv2.GaussianBlur(sharp, (41, 41), sigmaX=15.0)
    res = evaluate_image_quality(blurred)

    assert res.passed is False
    assert res.is_blurry is True
    assert res.blur_score < 100.0
    assert any("blurry" in cue.lower() for cue in res.remediation_cues)


# ============================================================================
# 2. Glare Candidate Metric Tests
# ============================================================================

def test_diffuse_white_label_is_not_rejected_as_glare():
    """
    Verifies that a normal diffuse white label does NOT trigger false-positive
    glare rejection, even though it occupies a large portion of the frame.
    """
    diffuse_label = make_diffuse_white_label_fixture()
    res = evaluate_image_quality(diffuse_label)

    # Must NOT be classified as glared
    assert res.is_glared is False
    assert res.glare_candidate_ratio <= 0.15


def test_localized_specular_glare_is_detected():
    """Verifies that localized specular reflections are identified as glare candidates."""
    # Hotspot covering > 15% of the frame (radius 90 in 400x400 has area ~25,446 / 160,000 = ~16%)
    glare_frame = make_specular_glare_fixture(width=400, height=400, glare_radius=95)
    res = evaluate_image_quality(glare_frame)

    assert res.is_glared is True
    assert res.glare_candidate_ratio > 0.15
    assert res.passed is False
    assert any("glare" in cue.lower() for cue in res.remediation_cues)


def test_small_highlight_does_not_trigger_rejection():
    """Verifies that a tiny acceptable glint (e.g. radius 10) does not reject the frame."""
    small_glare = make_specular_glare_fixture(width=400, height=400, glare_radius=10)
    res = evaluate_image_quality(small_glare)

    assert res.is_glared is False
    assert res.glare_candidate_ratio < 0.05


def test_all_white_image_reports_complete_saturation():
    """Verifies that a completely white frame reports 1.0 glare candidate ratio."""
    all_white = np.full((200, 200, 3), 255, dtype=np.uint8)
    res = evaluate_image_quality(all_white)

    assert res.passed is False
    assert res.glare_candidate_ratio == 1.0
    assert res.is_over_exposed is True


# ============================================================================
# 3. Exposure Metric Tests
# ============================================================================

def test_underexposed_image_triggers_rejection():
    """Verifies that a dark, underexposed image (mean < 40) is rejected."""
    dark_image = np.full((200, 200, 3), 20, dtype=np.uint8)
    res = evaluate_image_quality(dark_image)

    assert res.passed is False
    assert res.is_under_exposed is True
    assert res.mean_luminance < 40.0
    assert any("underexposed" in cue.lower() for cue in res.remediation_cues)


def test_overexposed_image_triggers_rejection():
    """Verifies that a washed-out image (mean > 220) is rejected."""
    bright_image = np.full((200, 200, 3), 235, dtype=np.uint8)
    res = evaluate_image_quality(bright_image)

    assert res.passed is False
    assert res.is_over_exposed is True
    assert res.mean_luminance > 220.0
    assert any("overexposed" in cue.lower() for cue in res.remediation_cues)


def test_normally_exposed_image_passes_exposure():
    """Verifies that an image with midtone exposure (mean ~128) passes exposure bounds."""
    normal_image = np.full((200, 200, 3), 128, dtype=np.uint8)
    thresholds = QualityGateThresholds(min_blur_score=0.0)  # Ignore blur for exposure-only check
    res = evaluate_image_quality(normal_image, thresholds=thresholds)

    assert res.is_under_exposed is False
    assert res.is_over_exposed is False
    assert 40.0 <= res.mean_luminance <= 220.0


# ============================================================================
# 4. Input Validation & Degenerate Input Tests (No Crashes)
# ============================================================================

@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        np.array([]),
        np.zeros((0, 0, 3), dtype=np.uint8),
        np.zeros((1, 1), dtype=np.uint8),             # 1-pixel 2D
        np.zeros((1, 1, 3), dtype=np.uint8),          # 1-pixel 3D
        np.zeros((2, 2, 3), dtype=np.uint8),          # 2x2 below 3x3 minimum
        np.zeros((10, 10, 2), dtype=np.uint8),        # Invalid channel count (2)
        np.zeros((10, 10, 5), dtype=np.uint8),        # Invalid channel count (5)
        np.zeros((10, 10, 10, 10), dtype=np.uint8),   # 4D array
        "not_an_array",
        [1, 2, 3],
    ],
)
def test_invalid_inputs_return_structured_failure(invalid_input):
    """Verifies that all malformed or degenerate inputs return structured results without crashing."""
    res = evaluate_image_quality(invalid_input)
    assert isinstance(res, QualityGateResult)
    assert res.passed is False
    assert len(res.remediation_cues) > 0


def test_grayscale_2d_array_supported():
    """Verifies that single-channel 2D grayscale arrays are processed properly."""
    gray = np.full((200, 200), 120, dtype=np.uint8)
    res = evaluate_image_quality(gray)
    assert isinstance(res, QualityGateResult)
    assert res.mean_luminance == 120.0


def test_rgba_4channel_array_supported():
    """Verifies that 4-channel BGRA/RGBA arrays are processed without error."""
    rgba = np.full((200, 200, 4), 140, dtype=np.uint8)
    res = evaluate_image_quality(rgba)
    assert isinstance(res, QualityGateResult)
    assert res.mean_luminance == 140.0


def test_unusual_aspect_ratios_handled():
    """Verifies that extreme wide and tall aspect ratios do not crash."""
    wide = np.full((50, 1000, 3), 120, dtype=np.uint8)
    res_wide = evaluate_image_quality(wide)
    assert isinstance(res_wide, QualityGateResult)

    tall = np.full((1000, 50, 3), 120, dtype=np.uint8)
    res_tall = evaluate_image_quality(tall)
    assert isinstance(res_tall, QualityGateResult)


def test_float_arrays_normalized_without_mutation():
    """Verifies that floating-point image arrays are safely processed without in-place mutation."""
    float_img = np.full((100, 100, 3), 0.5, dtype=np.float32)
    original_val = float_img[0, 0, 0]

    res = evaluate_image_quality(float_img)
    assert isinstance(res, QualityGateResult)
    # Caller's array must remain completely untouched
    assert float_img[0, 0, 0] == original_val
    assert float_img.dtype == np.float32


# ============================================================================
# 5. Serialization & Contract Compatibility Tests
# ============================================================================

def test_quality_gate_result_to_dict():
    """Verifies that to_dict produces all keys expected by API_CONTRACT.md."""
    sharp = make_sharp_high_frequency_fixture()
    res = evaluate_image_quality(sharp)
    d = res.to_dict()

    assert "passed" in d
    assert "blur_score" in d
    assert "laplacian_variance" in d  # Backwards compatibility key
    assert "glare_candidate_ratio" in d
    assert "glare_ratio" in d        # Backwards compatibility key
    assert "mean_luminance" in d
    assert "remediation_cues" in d
    assert "details" in d


# ============================================================================
# 6. Performance Benchmark (Authoritative NFR-01.1: <= 300 ms per frame)
# ============================================================================

def test_quality_gate_execution_latency_nfr01():
    """
    Authoritative NFR-01.1 requirement:
    'Quality gate validation (blur & glare assessment) shall complete within <= 300 ms per frame.'
    """
    # Standard Full HD frame (1920 x 1080 x 3)
    full_hd_frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    # Measure execution time across 5 passes
    latencies_ms = []
    for _ in range(5):
        start = time.perf_counter()
        _ = evaluate_image_quality(full_hd_frame)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        latencies_ms.append(elapsed_ms)

    median_latency = np.median(latencies_ms)
    # Assert adherence to authoritative NFR-01.1
    assert median_latency <= 300.0, f"Quality gate took {median_latency:.2f} ms, exceeding 300 ms NFR."


# ============================================================================
# 7. Audit Regression Tests (F-01, F-02, F-03)
# ============================================================================

@pytest.mark.parametrize(
    "non_finite_val",
    [np.nan, np.inf, -np.inf],
)
def test_non_finite_float_inputs(non_finite_val):
    """
    F-01 Regression: Verifies that floating-point arrays with NaN, +Inf, or -Inf
    return structured failure without raising unhandled exceptions or NumPy RuntimeWarnings.
    """
    img = np.full((100, 100, 3), 0.5, dtype=np.float32)
    img[50, 50, :] = non_finite_val
    original_copy = img.copy()

    res = evaluate_image_quality(img)

    assert isinstance(res, QualityGateResult)
    assert res.passed is False
    assert res.details.get("error") == "NON_FINITE_VALUES"
    assert any("non-finite" in cue.lower() for cue in res.remediation_cues)
    # Verify caller array was not mutated
    np.testing.assert_array_equal(img, original_copy)


def test_configurable_glare_heuristics():
    """
    F-02 Regression: Verifies that global_blowout_ratio and local_neighborhood_ksize:
    1. Preserve defaults in QualityGateThresholds.
    2. Changing global_blowout_ratio adjusts the global saturation cutoff.
    3. Changing local_neighborhood_ksize is respected in the details and calculation.
    """
    default_th = QualityGateThresholds()
    assert default_th.global_blowout_ratio == 0.60
    assert default_th.local_neighborhood_ksize == 31

    # Frame with 70% saturated white pixels (area 70x100 on 100x100)
    frame = np.full((100, 100, 3), 100, dtype=np.uint8)
    frame[:70, :] = 255

    # With default blowout ratio 0.60, 70% exceeds 0.60 -> global blowout branch executes
    res_default = evaluate_image_quality(frame, default_th)
    assert res_default.glare_candidate_ratio >= 0.70

    # With high blowout ratio 0.85, 70% does NOT trigger global blowout
    custom_th = QualityGateThresholds(global_blowout_ratio=0.85, local_neighborhood_ksize=15)
    res_custom = evaluate_image_quality(frame, custom_th)
    assert res_custom.details["global_blowout_ratio"] == 0.85
    assert res_custom.details["local_neighborhood_ksize"] == 15


def test_legacy_check_image_quality_adapter():
    """
    F-03 Regression: Verifies backwards compatibility of check_image_quality():
    1. Positional invocation.
    2. Keyword invocation.
    3. Exposes legacy attributes: .passed, .laplacian_variance, .glare_ratio, .details.
    4. to_dict() contains both new and legacy keys.
    5. Positional and keyword calls produce equivalent results.
    """
    sharp = make_sharp_high_frequency_fixture()

    # 1. Positional call
    res_pos = check_image_quality(sharp, 50.0, 0.20)

    # 2. Keyword call
    res_kw = check_image_quality(sharp, min_laplacian_variance=50.0, max_glare_ratio=0.20)

    # 3. Verify legacy attributes exist
    assert hasattr(res_pos, "passed")
    assert hasattr(res_pos, "laplacian_variance")
    assert hasattr(res_pos, "glare_ratio")
    assert hasattr(res_pos, "details")

    assert res_pos.passed is True
    assert res_pos.laplacian_variance == res_pos.blur_score
    assert res_pos.glare_ratio == res_pos.glare_candidate_ratio

    # 4. Verify to_dict() contains both key sets
    d = res_pos.to_dict()
    assert "blur_score" in d
    assert "glare_candidate_ratio" in d
    assert "laplacian_variance" in d
    assert "glare_ratio" in d

    # 5. Positional and keyword equivalence
    assert res_pos.passed == res_kw.passed
    assert res_pos.laplacian_variance == res_kw.laplacian_variance
    assert res_pos.glare_ratio == res_kw.glare_ratio
    assert res_pos.details == res_kw.details


# ============================================================================
# Phase 2 — Comprehensive Image Quality Gate Tests
# ============================================================================

def test_phase2_sharp_image():
    """Verifies that a high-contrast sharp image passes all quality checks."""
    sharp = make_sharp_high_frequency_fixture()
    res = evaluate_image_quality(sharp)
    assert isinstance(res, ImageQualityResult)
    assert res.is_valid_input is True
    assert res.passed is True
    assert res.is_blurry is False
    assert res.is_glared is False
    assert res.is_low_contrast is False
    assert res.is_dark is False
    assert res.is_over_exposed is False
    assert res.blur_score > 100.0
    assert res.contrast_score >= 20.0
    assert len(res.failure_reasons) == 0


def test_phase2_blurred_image():
    """Verifies that a moderately blurred image is rejected with actionable reasons."""
    sharp = make_sharp_high_frequency_fixture()
    blurred = cv2.GaussianBlur(sharp, (15, 15), 4.0)
    res = evaluate_image_quality(blurred)
    assert res.is_valid_input is True
    assert res.passed is False
    assert res.is_blurry is True
    assert res.blur_score < 100.0
    assert any("blurry" in r.lower() for r in res.failure_reasons)


def test_phase2_heavily_blurred_image():
    """Verifies that heavily blurred images exhibit strictly lower scores than moderate blur."""
    sharp = make_sharp_high_frequency_fixture()
    blurred_mod = cv2.GaussianBlur(sharp, (15, 15), 4.0)
    blurred_heavy = cv2.GaussianBlur(sharp, (45, 45), 15.0)

    res_mod = evaluate_image_quality(blurred_mod)
    res_heavy = evaluate_image_quality(blurred_heavy)

    assert res_heavy.is_valid_input is True
    assert res_heavy.passed is False
    assert res_heavy.is_blurry is True
    assert res_heavy.blur_score < res_mod.blur_score
    assert any("blurry" in r.lower() for r in res_heavy.failure_reasons)


def test_phase2_glare():
    """Verifies that specular glare is detected and rejected with actionable advice."""
    glared = make_specular_glare_fixture(width=400, height=400, glare_radius=95)
    res = evaluate_image_quality(glared)
    assert res.is_valid_input is True
    assert res.passed is False
    assert res.is_glared is True
    assert res.glare_score > 0.15
    assert any("glare" in r.lower() for r in res.failure_reasons)



def test_phase2_low_contrast():
    """Verifies that an image with washed-out, narrow dynamic range is detected as low contrast."""
    low_contrast = np.full((200, 200, 3), 128, dtype=np.uint8)
    low_contrast[::2, ::2, :] = 127
    res = evaluate_image_quality(low_contrast)
    assert res.is_valid_input is True
    assert res.passed is False
    assert res.is_low_contrast is True
    assert res.contrast_score < 20.0
    assert any("contrast" in r.lower() for r in res.failure_reasons)


def test_phase2_dark_image():
    """Verifies that an underexposed dark frame is flagged with actionable failure reasons."""
    dark = np.full((200, 200, 3), 15, dtype=np.uint8)
    res = evaluate_image_quality(dark)
    assert res.is_valid_input is True
    assert res.passed is False
    assert res.is_dark is True
    assert res.is_under_exposed is True
    assert res.mean_luminance < 40.0
    assert any("dark" in r.lower() or "underexposed" in r.lower() for r in res.failure_reasons)


def test_phase2_grayscale_rgb_bgr_behavior():
    """Verifies consistent quality evaluation across grayscale, BGR, RGB, and RGBA formats without array mutation."""
    sharp = make_sharp_high_frequency_fixture()
    sharp_copy = sharp.copy()

    # BGR 3-channel
    res_bgr = evaluate_image_quality(sharp, color_format="BGR")
    assert res_bgr.is_valid_input is True
    assert np.array_equal(sharp, sharp_copy)

    # RGB 3-channel
    sharp_rgb = cv2.cvtColor(sharp, cv2.COLOR_BGR2RGB)
    res_rgb = evaluate_image_quality(sharp_rgb, color_format="RGB")
    assert res_rgb.is_valid_input is True
    assert abs(res_rgb.blur_score - res_bgr.blur_score) < 5.0

    # Grayscale 2D
    gray_2d = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
    res_gray = evaluate_image_quality(gray_2d)
    assert res_gray.is_valid_input is True
    assert res_gray.blur_score == res_bgr.blur_score

    # Grayscale 3D (H, W, 1)
    gray_3d = np.expand_dims(gray_2d, axis=2)
    res_gray_3d = evaluate_image_quality(gray_3d)
    assert res_gray_3d.is_valid_input is True
    assert res_gray_3d.blur_score == res_gray.blur_score

    # RGBA 4-channel
    rgba = cv2.cvtColor(sharp, cv2.COLOR_BGR2BGRA)
    res_rgba = evaluate_image_quality(rgba)
    assert res_rgba.is_valid_input is True
    assert abs(res_rgba.blur_score - res_bgr.blur_score) < 5.0


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        (np.zeros(100, dtype=np.uint8), "INVALID_DIMENSIONS"),
        (np.zeros((10, 10, 3, 3), dtype=np.uint8), "INVALID_DIMENSIONS"),
        (np.zeros((50, 50, 2), dtype=np.uint8), "INVALID_CHANNELS"),
        (np.zeros((50, 50, 5), dtype=np.uint8), "INVALID_CHANNELS"),
        (np.array([], dtype=np.uint8), "EMPTY_ARRAY"),
        (np.array([[np.nan, 100.0], [100.0, 100.0]], dtype=np.float32), "NON_FINITE_VALUES"),
        (np.array([[np.inf, 100.0], [100.0, 100.0]], dtype=np.float32), "NON_FINITE_VALUES"),
        (np.array([[-np.inf, 100.0], [100.0, 100.0]], dtype=np.float32), "NON_FINITE_VALUES"),
        ("invalid_string", "INVALID_TYPE"),
        (12345, "INVALID_TYPE"),
        ([1, 2, 3], "INVALID_TYPE"),
    ],
)
def test_phase2_invalid_ndarray(invalid_input, expected_error):
    """Verifies clear distinction between invalid input and poor-quality images."""
    res = evaluate_image_quality(invalid_input)
    assert res.is_valid_input is False
    assert res.passed is False
    assert res.is_blurry is False
    assert res.is_glared is False
    assert res.is_low_contrast is False
    assert res.is_dark is False
    assert res.is_over_exposed is False
    assert res.details["error"] == expected_error
    assert res.failure_reasons[0].startswith("INVALID_INPUT:")


def test_phase2_none_input():
    """Verifies that None input returns structured failure with is_valid_input=False."""
    res = evaluate_image_quality(None)
    assert res.is_valid_input is False
    assert res.passed is False
    assert res.is_blurry is False
    assert res.details["error"] == "NULL_INPUT"
    assert res.failure_reasons == ["INVALID_INPUT: Input image is None."]


@pytest.mark.parametrize(
    "tiny_shape",
    [(1, 1), (1, 1, 3), (2, 2), (2, 2, 3), (2, 100), (100, 2)],
)
def test_phase2_tiny_image(tiny_shape):
    """Verifies that images below minimum 3x3 resolution are rejected as invalid input."""
    tiny = np.zeros(tiny_shape, dtype=np.uint8)
    res = evaluate_image_quality(tiny)
    assert res.is_valid_input is False
    assert res.passed is False
    assert res.details["error"] == "RESOLUTION_TOO_LOW"
    assert any("too small" in r for r in res.failure_reasons)


def test_phase2_extreme_aspect_ratio():
    """Verifies that extreme aspect ratios are handled gracefully without exceptions."""
    wide = np.full((10, 1000, 3), 120, dtype=np.uint8)
    wide[:, ::2, :] = 40

    # Without max_aspect_ratio threshold, evaluates purely on optical quality
    res_no_cap = evaluate_image_quality(wide)
    assert res_no_cap.is_valid_input is True
    assert res_no_cap.details["aspect_ratio"] == 100.0

    # With configured max_aspect_ratio threshold, rejects when ratio exceeded
    thresholds = QualityGateThresholds(max_aspect_ratio=20.0)
    res_capped = evaluate_image_quality(wide, thresholds=thresholds)
    assert res_capped.is_valid_input is True
    assert res_capped.passed is False
    assert res_capped.details["is_extreme_aspect_ratio"] is True
    assert any("Extreme image aspect ratio" in r for r in res_capped.failure_reasons)


def test_phase2_distinction_invalid_vs_poor_quality():
    """Explicitly tests the architectural boundary: invalid inputs vs poor-quality images."""
    # 1. Invalid input: array with NaN
    invalid_arr = np.full((100, 100), np.nan, dtype=np.float32)
    res_invalid = evaluate_image_quality(invalid_arr)
    assert res_invalid.is_valid_input is False
    assert res_invalid.passed is False
    assert res_invalid.is_blurry is False
    assert res_invalid.is_dark is False
    assert res_invalid.failure_reasons[0].startswith("INVALID_INPUT:")

    # 2. Poor-quality image: valid array, but severely blurred
    sharp = make_sharp_high_frequency_fixture()
    blurred = cv2.GaussianBlur(sharp, (31, 31), 10.0)
    res_poor = evaluate_image_quality(blurred)
    assert res_poor.is_valid_input is True
    assert res_poor.passed is False
    assert res_poor.is_blurry is True
    assert not res_poor.failure_reasons[0].startswith("INVALID_INPUT:")


def test_phase2_canonical_package_imports():
    """Verifies canonical imports from nirikshak_vision.quality and public exports from nirikshak_vision."""
    # 1. Direct submodule imports from nirikshak_vision.quality
    from nirikshak_vision.quality import (
        ImageQualityResult,
        QualityGateThresholds,
        evaluate_image_quality,
        compute_contrast,
    )
    sharp = make_sharp_high_frequency_fixture()
    res = evaluate_image_quality(sharp)
    assert isinstance(res, ImageQualityResult)
    assert res.passed is True
    assert compute_contrast(cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)) > 0.0

    # 2. Public package exports from top-level nirikshak_vision
    from nirikshak_vision import (
        ImageQualityResult as TopResult,
        QualityGateResult as TopGateResult,
        QualityGateThresholds as TopThresholds,
        evaluate_image_quality as top_evaluate,
        check_image_quality as top_check,
        compute_contrast as top_contrast,
        compute_laplacian_variance as top_blur,
        compute_glare_candidate_ratio as top_glare,
        compute_mean_luminance as top_luminance,
        convert_to_grayscale as top_convert,
    )
    assert TopResult is ImageQualityResult
    assert TopGateResult is ImageQualityResult
    assert TopThresholds is QualityGateThresholds
    assert top_evaluate is evaluate_image_quality
    assert top_contrast is compute_contrast
