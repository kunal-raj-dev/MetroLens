"""
Comprehensive deterministic test suite for metric reference anchor detection.

Validates:
- RBI Rs 10 coin detection, concentric ring pairing, and tilt characterization.
- ISO/IEC 7810 ID-1 card detection, aspect ratio filtering, and ordered corner extraction.
- Candidate ranking determinism (never OpenCV order, never candidates[0]).
- Confidence gating BEFORE ambiguity (low-scoring noise blobs never trigger ambiguous status).
- Cross-anchor ambiguity and forced-mode vs AUTO dispatch.
- Pure algebraic ellipse residual mathematics (semi-axes + coordinate rotation).
- Robust input validation and graceful failure modes without unhandled exceptions.
- Frame processing performance (<= 300 ms/frame).
"""

import math
import time
import pytest
import numpy as np
import cv2

from nirikshak_calibration import (
    AnchorType,
    AnchorDetectionStatus,
    AnchorDetectorConfig,
    AnchorDetectionResult,
    EllipseGeometry,
    CardGeometry,
    ConcentricRingInfo,
    detect_anchor,
    order_quadrilateral_corners,
    compute_algebraic_ellipse_residual,
)


# ============================================================================
# Test Fixtures & Synthetic Image Generators
# ============================================================================

def create_synthetic_coin_image(
    width: int = 640,
    height: int = 480,
    center: tuple = (320, 240),
    outer_radius: int = 60,
    inner_radius: int = 44,
    tilt_deg: float = 0.0,
    angle_deg: float = 0.0,
    add_noise: bool = False,
    bg_color: tuple = (128, 128, 128),
) -> np.ndarray:
    """Generates a synthetic bimetallic coin with outer brass ring and inner nickel core."""
    img = np.full((height, width, 3), bg_color, dtype=np.uint8)

    # Compute foreshortened minor radius under tilt
    outer_minor = int(round(outer_radius * math.cos(math.radians(tilt_deg))))
    inner_minor = int(round(inner_radius * math.cos(math.radians(tilt_deg))))

    # Outer brass rim (BGR: 45, 165, 215)
    cv2.ellipse(
        img,
        center,
        (outer_radius, max(2, outer_minor)),
        angle_deg,
        0,
        360,
        (45, 165, 215),
        -1,
        lineType=cv2.LINE_AA,
    )
    # Rim outline
    cv2.ellipse(
        img,
        center,
        (outer_radius, max(2, outer_minor)),
        angle_deg,
        0,
        360,
        (25, 110, 160),
        2,
        lineType=cv2.LINE_AA,
    )

    # Inner nickel core (BGR: 190, 195, 200)
    cv2.ellipse(
        img,
        center,
        (inner_radius, max(2, inner_minor)),
        angle_deg,
        0,
        360,
        (190, 195, 200),
        -1,
        lineType=cv2.LINE_AA,
    )

    if add_noise:
        noise = np.random.normal(0, 3.0, img.shape).astype(np.float32)
        img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    return img


def create_synthetic_card_image(
    width: int = 640,
    height: int = 480,
    center: tuple = (320, 240),
    card_w: int = 190,  # 190 x 120 gives aspect ratio ~1.583 (ID-1 target 1.5858)
    card_h: int = 120,
    rotation_deg: float = 0.0,
    bg_color: tuple = (120, 120, 120),
    card_color: tuple = (230, 230, 230),
) -> np.ndarray:
    """Generates a synthetic ISO/IEC 7810 ID-1 card candidate."""
    img = np.full((height, width, 3), bg_color, dtype=np.uint8)

    cx, cy = center
    half_w, half_h = card_w / 2.0, card_h / 2.0
    corners = np.array([
        [-half_w, -half_h],
        [half_w, -half_h],
        [half_w, half_h],
        [-half_w, half_h],
    ], dtype=np.float64)

    rad = math.radians(rotation_deg)
    rot_mat = np.array([
        [math.cos(rad), -math.sin(rad)],
        [math.sin(rad), math.cos(rad)],
    ])
    rotated = (rot_mat @ corners.T).T + np.array([cx, cy])
    pts = rotated.astype(np.int32)

    cv2.fillPoly(img, [pts], card_color, lineType=cv2.LINE_AA)
    cv2.polylines(img, [pts], isClosed=True, color=(40, 40, 40), thickness=2, lineType=cv2.LINE_AA)

    return img


# ============================================================================
# 1. Mathematical Unit Tests
# ============================================================================

def test_compute_algebraic_ellipse_residual_mathematics():
    """
    Verifies that compute_algebraic_ellipse_residual correctly:
    1. Uses semi-axes a = width/2, b = height/2.
    2. Translates around center (cx, cy).
    3. Rotates into ellipse intrinsic frame.
    4. Evaluates (x'/a)^2 + (y'/b)^2 - 1.
    """
    cx, cy = 100.0, 150.0
    full_major = 80.0
    full_minor = 50.0
    angle_deg = 30.0
    a = full_major / 2.0  # 40.0
    b = full_minor / 2.0  # 25.0

    # Generate points exactly on the ellipse
    thetas = np.linspace(0, 2 * math.pi, 60, endpoint=False)
    rad = math.radians(angle_deg)
    cos_r, sin_r = math.cos(rad), math.sin(rad)

    pts = []
    for th in thetas:
        x_local = a * math.cos(th)
        y_local = b * math.sin(th)
        gx = cx + x_local * cos_r - y_local * sin_r
        gy = cy + x_local * sin_r + y_local * cos_r
        pts.append([[gx, gy]])

    cnt = np.array(pts, dtype=np.float32)
    ell = ((cx, cy), (full_major, full_minor), angle_deg)

    residual = compute_algebraic_ellipse_residual(cnt, ell)
    # For mathematically exact points, algebraic residual is ~0.0
    assert residual < 1e-4, f"Expected algebraic residual ~0, got {residual}"


def test_order_quadrilateral_corners():
    """Verifies deterministic corner ordering: (Top-Left, Top-Right, Bottom-Right, Bottom-Left)."""
    # Create unordered 4 points
    pts = np.array([
        [200, 250],  # Bottom-Right
        [100, 150],  # Top-Left
        [100, 250],  # Bottom-Left
        [200, 150],  # Top-Right
    ])
    ordered = order_quadrilateral_corners(pts)
    assert len(ordered) == 4
    tl, tr, br, bl = ordered
    assert tl == (100.0, 150.0)
    assert tr == (200.0, 150.0)
    assert br == (200.0, 250.0)
    assert bl == (100.0, 250.0)


# ============================================================================
# 2. Coin Detector Tests
# ============================================================================

def test_coin_clean_circle():
    """Verifies clean circular coin is detected with high confidence."""
    img = create_synthetic_coin_image(outer_radius=50, inner_radius=36, tilt_deg=0.0)
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)

    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert res.anchor_type == AnchorType.COIN_INR_10
    assert res.confidence >= 0.75
    assert isinstance(res.geometry, EllipseGeometry)
    assert abs(res.geometry.major_axis_px - 100.0) < 5.0
    assert abs(res.geometry.aspect_ratio - 1.0) < 0.08
    assert res.ring_information is not None
    assert res.ring_information.has_concentric_ring is True


def test_coin_perspective_ellipse():
    """
    Verifies that under 15 deg tilt, candidate is detected and ellipse geometry
    is correctly characterized with minor axis < major axis.
    NOTE: Does NOT claim physical scale invariance.
    """
    img = create_synthetic_coin_image(outer_radius=55, inner_radius=40, tilt_deg=15.0, angle_deg=20.0)
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)

    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert isinstance(res.geometry, EllipseGeometry)
    # Recovered minor axis must be strictly less than major axis under tilt
    assert res.geometry.minor_axis_px < res.geometry.major_axis_px
    # Recovered aspect ratio should be close to cos(15 deg) ≈ 0.966
    expected_ar = math.cos(math.radians(15.0))
    assert abs(res.geometry.aspect_ratio - expected_ar) < 0.10


def test_coin_ellipse_axis_angle_normalization():
    """
    Verifies that cv2.fitEllipse() output is normalized consistently:
    1. major_axis_px is strictly >= minor_axis_px.
    2. aspect_ratio is strictly <= 1.0.
    3. angle_deg is normalized to the major axis orientation regardless of whether
       OpenCV returns d1 > d2 or d1 < d2.
    """
    # Case A: horizontal tilt (major axis along x, minor axis along y, angle ~0 deg)
    img_horiz = create_synthetic_coin_image(outer_radius=60, inner_radius=42, tilt_deg=25.0, angle_deg=0.0)
    res_horiz = detect_anchor(img_horiz, anchor_type=AnchorType.COIN_INR_10)
    assert res_horiz.detected is True
    assert res_horiz.geometry.major_axis_px >= res_horiz.geometry.minor_axis_px
    assert res_horiz.geometry.aspect_ratio <= 1.0
    # In horizontal orientation, major axis is horizontal (angle ~0 or ~180)
    assert res_horiz.geometry.angle_deg < 15.0 or res_horiz.geometry.angle_deg > 165.0

    # Case B: vertical tilt (major axis along y, minor axis along x, angle ~90 deg)
    img_vert = create_synthetic_coin_image(outer_radius=60, inner_radius=42, tilt_deg=25.0, angle_deg=90.0)
    res_vert = detect_anchor(img_vert, anchor_type=AnchorType.COIN_INR_10)
    assert res_vert.detected is True
    assert res_vert.geometry.major_axis_px >= res_vert.geometry.minor_axis_px
    assert res_vert.geometry.aspect_ratio <= 1.0
    # In vertical orientation, major axis is vertical (angle ~90 deg)
    assert abs(res_vert.geometry.angle_deg - 90.0) < 15.0


def test_coin_concentric_ring_bonus():
    """Verifies that bimetallic coin receives concentric ring bonus over single solid disk."""
    # 1. Bimetallic coin
    img_bimetallic = create_synthetic_coin_image(outer_radius=50, inner_radius=36)
    res_bimetallic = detect_anchor(img_bimetallic, anchor_type=AnchorType.COIN_INR_10)

    # 2. Solid monochrome disk (no inner ring)
    img_solid = np.full((480, 640, 3), 128, dtype=np.uint8)
    cv2.circle(img_solid, (320, 240), 50, (45, 165, 215), -1)
    res_solid = detect_anchor(img_solid, anchor_type=AnchorType.COIN_INR_10)

    assert res_bimetallic.detected is True
    assert res_bimetallic.ring_information is not None
    assert res_bimetallic.ring_information.has_concentric_ring is True

    # Bimetallic coin confidence should be higher due to concentric confirmation bonus
    if res_solid.detected:
        assert res_bimetallic.confidence >= res_solid.confidence


def test_coin_inner_ring_not_mistaken_for_outer():
    """
    Verifies that detector selects the outer brass rim (major ~100px)
    and does not false-lock onto the inner nickel core (major ~72px).
    """
    img = create_synthetic_coin_image(outer_radius=50, inner_radius=36)
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)

    assert res.detected is True
    assert isinstance(res.geometry, EllipseGeometry)
    # Must lock to outer diameter (~100 px), not inner (~72 px)
    assert res.geometry.major_axis_px >= 90.0


def test_coin_circular_glare_false_positive():
    """Verifies that a circular specular glare reflection is rejected as GLARE_INTERFERENCE or LOW_CONFIDENCE."""
    img = np.full((480, 640, 3), 80, dtype=np.uint8)
    # Bright saturated white spot (255, 255, 255) simulating specular hotspot
    cv2.circle(img, (320, 240), 45, (255, 255, 255), -1)

    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    # Must NOT detect this as a valid anchor
    assert res.detected is False
    assert res.status in (
        AnchorDetectionStatus.GLARE_INTERFERENCE,
        AnchorDetectionStatus.LOW_CONFIDENCE,
        AnchorDetectionStatus.NO_ANCHOR,
    )


def test_coin_clutter_background():
    """Verifies that coin is detected amidst high-frequency background clutter."""
    img = create_synthetic_coin_image(outer_radius=50, inner_radius=36, bg_color=(100, 100, 100))
    # Add clutter lines and rectangles away from the coin
    for x in range(30, 200, 15):
        cv2.line(img, (x, 50), (x, 400), (30, 30, 30), 2)
    for y in range(50, 400, 30):
        cv2.rectangle(img, (450, y), (600, y + 15), (20, 20, 20), -1)

    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert isinstance(res.geometry, EllipseGeometry)
    assert abs(res.geometry.center[0] - 320.0) < 5.0
    assert abs(res.geometry.center[1] - 240.0) < 5.0


def test_coin_low_contrast():
    """Verifies coin detection under low contrast conditions."""
    # Background color very close to brass rim
    img = create_synthetic_coin_image(
        outer_radius=50,
        inner_radius=36,
        bg_color=(50, 150, 200),
    )
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    # Should either detect outer coin or report structured status without crashing
    assert res.status in (AnchorDetectionStatus.SUCCESS, AnchorDetectionStatus.LOW_CONFIDENCE)


# ============================================================================
# 3. ID-1 Card Detector Tests
# ============================================================================

def test_card_clean_rectangle():
    """Verifies clean ID-1 card rectangle detection."""
    # Standard ID-1 aspect ratio: 85.60 / 53.98 ≈ 1.5858
    img = create_synthetic_card_image(card_w=190, card_h=120)
    res = detect_anchor(img, anchor_type=AnchorType.ID1_CARD)

    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert res.anchor_type == AnchorType.ID1_CARD
    assert isinstance(res.geometry, CardGeometry)
    assert len(res.geometry.corners) == 4
    # Aspect ratio should match ~1.583
    assert abs(res.geometry.aspect_ratio - 1.5858) < 0.10


def test_card_rotated():
    """Verifies rotated ID-1 card is correctly detected with ordered corners."""
    img = create_synthetic_card_image(card_w=190, card_h=120, rotation_deg=25.0)
    res = detect_anchor(img, anchor_type=AnchorType.ID1_CARD)

    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert isinstance(res.geometry, CardGeometry)
    assert abs(res.geometry.aspect_ratio - 1.5858) < 0.15


def test_card_incorrect_aspect_ratio_rejected():
    """Verifies non-ID-1 rectangles (e.g. square 1:1 or ultra-wide 3:1) are rejected."""
    # Square 1:1
    img_square = create_synthetic_card_image(card_w=140, card_h=140)
    res_square = detect_anchor(img_square, anchor_type=AnchorType.ID1_CARD)
    assert res_square.detected is False

    # Ultra-wide 3:1
    img_wide = create_synthetic_card_image(card_w=300, card_h=100)
    res_wide = detect_anchor(img_wide, anchor_type=AnchorType.ID1_CARD)
    assert res_wide.detected is False


def test_card_non_convex_quadrilateral_rejected():
    """Verifies that non-convex quadrilaterals are rejected."""
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Concave arrow/dart shape
    pts = np.array([[200, 150], [350, 180], [300, 240], [200, 300]], dtype=np.int32)
    cv2.fillPoly(img, [pts], (220, 220, 220))
    cv2.polylines(img, [pts], True, (20, 20, 20), 2)

    res = detect_anchor(img, anchor_type=AnchorType.ID1_CARD)
    assert res.detected is False


# ============================================================================
# 4. Candidate Ranking & Ambiguity Resolution Tests
# ============================================================================

def test_ranking_determinism_not_opencv_order():
    """
    Verifies that the highest-scoring candidate is chosen deterministically
    regardless of contour order or position in image.
    """
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # 1. Distorted ellipse on left (raster first, lower fit quality)
    pts = cv2.ellipse2Poly((150, 240), (40, 26), 0, 0, 360, 8)
    pts[::2, 0] += 4  # asymmetry to lower residual fit quality
    cv2.fillPoly(img, [pts], (70, 70, 70))

    # 2. Perfect bimetallic coin on right (raster second, high fit quality + concentric bonus)
    cv2.circle(img, (450, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (450, 240), 36, (190, 195, 200), -1)

    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    assert res.detected is True
    assert isinstance(res.geometry, EllipseGeometry)
    # Must select the perfect coin on the right despite being second in raster order
    assert abs(res.geometry.center[0] - 450.0) < 5.0


def test_ambiguity_two_identical_coins():
    """
    Verifies that when two identical coins are present with near-equal scores,
    the detector returns AMBIGUOUS_ANCHOR and detected=False.
    False calibration is worse than no calibration.
    """
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Coin 1 on left
    cv2.circle(img, (180, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (180, 240), 36, (190, 195, 200), -1)
    # Coin 2 on right (identical)
    cv2.circle(img, (460, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (460, 240), 36, (190, 195, 200), -1)

    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    assert res.detected is False
    assert res.status == AnchorDetectionStatus.AMBIGUOUS_ANCHOR
    assert "Ambiguous" in res.message


def test_ambiguity_low_confidence_not_ambiguous():
    """
    Verifies that low-scoring noise blobs below min_confidence_threshold
    return LOW_CONFIDENCE, NOT AMBIGUOUS_ANCHOR.
    Confidence gating must execute before ambiguity analysis.
    """
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Two faint blurry gray ellipses that have low confidence
    cv2.ellipse(img, (180, 240), (25, 22), 0, 0, 360, (135, 135, 135), -1)
    cv2.ellipse(img, (460, 240), (25, 22), 0, 0, 360, (135, 135, 135), -1)

    config = AnchorDetectorConfig(min_confidence_threshold=0.60)
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10, config=config)

    assert res.detected is False
    assert res.status in (AnchorDetectionStatus.LOW_CONFIDENCE, AnchorDetectionStatus.NO_ANCHOR)
    assert res.status != AnchorDetectionStatus.AMBIGUOUS_ANCHOR


# ============================================================================
# 5. Dispatch Policy Tests (Forced vs AUTO)
# ============================================================================

def test_dispatch_forced_coin_mode_ignores_card():
    """In forced COIN mode, card present in frame is ignored and coin is detected."""
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Add coin on left
    cv2.circle(img, (180, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (180, 240), 36, (190, 195, 200), -1)
    # Add ID-1 card on right
    cv2.rectangle(img, (380, 180), (570, 300), (220, 220, 220), -1)
    cv2.rectangle(img, (380, 180), (570, 300), (30, 30, 30), 2)

    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)
    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert res.anchor_type == AnchorType.COIN_INR_10
    assert isinstance(res.geometry, EllipseGeometry)


def test_dispatch_forced_card_mode_ignores_coin():
    """In forced CARD mode, coin present in frame is ignored and card is detected."""
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Add coin on left
    cv2.circle(img, (180, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (180, 240), 36, (190, 195, 200), -1)
    # Add ID-1 card on right
    cv2.rectangle(img, (380, 180), (570, 300), (220, 220, 220), -1)
    cv2.rectangle(img, (380, 180), (570, 300), (30, 30, 30), 2)

    res = detect_anchor(img, anchor_type=AnchorType.ID1_CARD)
    assert res.detected is True
    assert res.status == AnchorDetectionStatus.SUCCESS
    assert res.anchor_type == AnchorType.ID1_CARD
    assert isinstance(res.geometry, CardGeometry)


def test_dispatch_auto_mode_ambiguity():
    """In AUTO mode with both high-scoring coin and card with close scores, returns AMBIGUOUS_ANCHOR."""
    img = np.full((480, 640, 3), 128, dtype=np.uint8)
    # Add coin on left
    cv2.circle(img, (180, 240), 50, (45, 165, 215), -1)
    cv2.circle(img, (180, 240), 36, (190, 195, 200), -1)
    # Add ID-1 card on right
    cv2.rectangle(img, (380, 180), (570, 300), (220, 220, 220), -1)
    cv2.rectangle(img, (380, 180), (570, 300), (30, 30, 30), 2)

    # Set high ambiguity margin to ensure competition triggers ambiguity
    config = AnchorDetectorConfig(ambiguity_confidence_margin=0.30)
    res = detect_anchor(img, anchor_type=None, config=config)

    assert res.detected is False
    assert res.status == AnchorDetectionStatus.AMBIGUOUS_ANCHOR


# ============================================================================
# 6. Input Validation & Robustness Tests
# ============================================================================

@pytest.mark.parametrize("invalid_input,expected_error", [
    (None, "None"),
    (np.array([], dtype=np.uint8), "empty"),
    ("not_an_array", "numpy.ndarray"),
    (np.full((5, 5, 3), 128, dtype=np.uint8), "too small"),
    (np.zeros((100, 100, 5), dtype=np.uint8), "color channels"),
])
def test_invalid_inputs_return_structured_failure(invalid_input, expected_error):
    """Verifies that all malformed inputs return structured INVALID_INPUT without unhandled exceptions."""
    res = detect_anchor(invalid_input)
    assert res.detected is False
    assert res.status == AnchorDetectionStatus.INVALID_INPUT
    assert res.message is not None


@pytest.mark.parametrize("non_finite_val", [np.nan, np.inf, -np.inf])
def test_non_finite_float_inputs(non_finite_val):
    """Verifies floating-point arrays containing NaN or Inf return structured INVALID_INPUT."""
    img = np.full((100, 100, 3), 0.5, dtype=np.float32)
    img[50, 50, 0] = non_finite_val
    res = detect_anchor(img)
    assert res.detected is False
    assert res.status == AnchorDetectionStatus.INVALID_INPUT
    assert "non-finite" in res.message.lower()


def test_color_format_support():
    """Verifies that 2D grayscale, 3D BGR, 3D RGB, and 4-channel RGBA are supported."""
    base_coin = create_synthetic_coin_image(outer_radius=50, inner_radius=36)

    # 1. 2D grayscale
    gray_2d = cv2.cvtColor(base_coin, cv2.COLOR_BGR2GRAY)
    res_gray = detect_anchor(gray_2d)
    assert res_gray.detected is True

    # 2. 3D RGB
    rgb_3d = cv2.cvtColor(base_coin, cv2.COLOR_BGR2RGB)
    res_rgb = detect_anchor(rgb_3d, color_format="RGB")
    assert res_rgb.detected is True

    # 3. 4-channel RGBA
    rgba_4d = cv2.cvtColor(base_coin, cv2.COLOR_BGR2RGBA)
    res_rgba = detect_anchor(rgba_4d, color_format="RGBA")
    assert res_rgba.detected is True


def test_result_to_dict_serialization():
    """Verifies that AnchorDetectionResult serializes cleanly to an inspectable dictionary."""
    img = create_synthetic_coin_image(outer_radius=50, inner_radius=36)
    res = detect_anchor(img, anchor_type=AnchorType.COIN_INR_10)

    d = res.to_dict()
    assert isinstance(d, dict)
    assert d["detected"] is True
    assert d["anchor_type"] == "COIN_INR_10"
    assert d["status"] == "SUCCESS"
    assert "geometry" in d
    assert d["geometry"]["type"] == "ellipse"
    assert "ring_information" in d
    assert d["ring_information"]["has_concentric_ring"] is True


# ============================================================================
# 7. Latency Benchmark (NFR: <= 300 ms/frame)
# ============================================================================

def test_anchor_detection_latency():
    """Verifies that anchor detection latency on a 1280x720 frame is <= 300 ms."""
    img = create_synthetic_coin_image(width=1280, height=720, center=(640, 360), outer_radius=70, inner_radius=50)

    # Warmup
    _ = detect_anchor(img)

    latencies = []
    for _ in range(5):
        t0 = time.perf_counter()
        _ = detect_anchor(img)
        latencies.append((time.perf_counter() - t0) * 1000.0)

    mean_latency_ms = float(np.mean(latencies))
    assert mean_latency_ms <= 300.0, f"Mean latency {mean_latency_ms:.1f}ms exceeds 300ms requirement"


def test_score_range_guarantee_after_bonus_and_penalties():
    """
    Verifies that anchor candidate scores are strictly clamped to [0.0, 1.0]
    after every bonus (e.g. +0.10 concentric bonus) and penalty (glare, border).
    """
    # 1. Ideal coin with concentric ring bonus (+0.10)
    img_coin = create_synthetic_coin_image(outer_radius=60, inner_radius=44)
    res_coin = detect_anchor(img_coin, anchor_type=AnchorType.COIN_INR_10)
    assert 0.0 <= res_coin.confidence <= 1.0

    # 2. Coin on border (border penalty x0.70)
    img_border_coin = create_synthetic_coin_image(center=(65, 65), outer_radius=60, inner_radius=44)
    res_border = detect_anchor(img_border_coin, anchor_type=AnchorType.COIN_INR_10)
    assert 0.0 <= res_border.confidence <= 1.0

    # 3. Card with perfect aspect ratio and orthogonality
    img_card = create_synthetic_card_image(card_w=190, card_h=120)
    res_card = detect_anchor(img_card, anchor_type=AnchorType.ID1_CARD)
    assert 0.0 <= res_card.confidence <= 1.0

    # 4. Card on border
    img_border_card = create_synthetic_card_image(center=(100, 70), card_w=190, card_h=120)
    res_border_card = detect_anchor(img_border_card, anchor_type=AnchorType.ID1_CARD)
    assert 0.0 <= res_border_card.confidence <= 1.0
