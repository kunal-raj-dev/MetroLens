"""
Unit tests for Phase 5: Planar Homography & Perspective Rectification.
Evaluates numerical geometry, coordinate transformations, error handling, and stability.
"""

import math
import numpy as np
import pytest
import cv2

from nirikshak_calibration.types import CardGeometry
from nirikshak_calibration.homography import (
    RectificationStatus,
    HomographyConfig,
    RectificationResult,
    rectify_planar_quadrilateral,
    validate_quadrilateral_geometry,
)


def test_identity_transformation():
    """Identity rectangle: source points match destination rectangle. H must be ~identity."""
    w, h = 400, 300
    corners = ((0.0, 0.0), (float(w - 1), 0.0), (float(w - 1), float(h - 1)), (0.0, float(h - 1)))
    res = rectify_planar_quadrilateral(corners, target_dimensions=(w, h))

    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.homography_matrix is not None
    assert res.reprojection_error_px is not None
    assert res.reprojection_error_px < 1e-4

    h_mat = np.array(res.homography_matrix)
    # Normalize by h_mat[2, 2]
    h_norm = h_mat / h_mat[2, 2]
    identity = np.eye(3)
    np.testing.assert_allclose(h_norm, identity, atol=1e-3)


def test_known_synthetic_perspective_transformation():
    """Applies a known perspective warp to an image, rectifies back, and verifies numerical error."""
    w, h = 500, 350
    # Destination rectangle
    dst_corners = ((0.0, 0.0), (float(w - 1), 0.0), (float(w - 1), float(h - 1)), (0.0, float(h - 1)))

    # Distorted source corners (perspective foreshortening)
    src_corners = (
        (50.0, 40.0),    # Top-Left shifted right and down
        (460.0, 20.0),   # Top-Right
        (490.0, 340.0),  # Bottom-Right
        (20.0, 320.0),   # Bottom-Left
    )

    # Generate synthetic checkerboard image
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    img[::20, :, :] = 255
    img[:, ::20, :] = 255

    res = rectify_planar_quadrilateral(src_corners, image=img, target_dimensions=(w, h))

    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.reprojection_error_px is not None
    assert res.reprojection_error_px < 1e-3
    assert res.rectified_image is not None
    assert res.rectified_image.shape == (h, w, 3)


def test_rotated_rectangle():
    """Quadrilateral rotated by 30 degrees in 2D plane."""
    center_x, center_y = 250.0, 250.0
    w, h = 200.0, 100.0
    angle = math.radians(30.0)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    raw_offsets = [
        (-w / 2, -h / 2),
        (w / 2, -h / 2),
        (w / 2, h / 2),
        (-w / 2, h / 2),
    ]
    corners = tuple(
        (center_x + dx * cos_a - dy * sin_a, center_y + dx * sin_a + dy * cos_a)
        for dx, dy in raw_offsets
    )

    res = rectify_planar_quadrilateral(corners, target_dimensions=(int(w), int(h)))
    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.reprojection_error_px < 1e-3


def test_skewed_parallelogram():
    """Quadrilateral with sheer / skew."""
    corners = (
        (100.0, 100.0),
        (350.0, 100.0),
        (390.0, 250.0),
        (140.0, 250.0),
    )
    res = rectify_planar_quadrilateral(corners, target_dimensions=(250, 150))
    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.reprojection_error_px < 1e-3


def test_card_geometry_integration():
    """Accepts Phase 4 CardGeometry instance directly as corners."""
    card = CardGeometry(
        corners=((10.0, 10.0), (210.0, 10.0), (210.0, 136.0), (10.0, 136.0)),
        width_px=200.0,
        height_px=126.0,
        aspect_ratio=1.587,
    )
    res = rectify_planar_quadrilateral(card)
    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.output_dimensions == (200, 126)


def test_derived_dimensions_when_target_not_specified():
    """Derives output width and height from average edge lengths."""
    corners = (
        (0.0, 0.0),
        (200.0, 0.0),
        (220.0, 100.0),
        (0.0, 100.0),
    )
    res = rectify_planar_quadrilateral(corners)
    assert res.success is True
    assert res.output_dimensions is not None
    out_w, out_h = res.output_dimensions
    assert abs(out_w - 210) <= 2  # avg(200, 220)
    assert abs(out_h - 100) <= 2  # avg(100, 100)


def test_invalid_point_count():
    """Rejects inputs with fewer or more than 4 points."""
    # 3 points
    res3 = rectify_planar_quadrilateral(((0.0, 0.0), (100.0, 0.0), (100.0, 100.0)))
    assert res3.success is False
    assert res3.status == RectificationStatus.INVALID_POINT_COUNT

    # 5 points
    res5 = rectify_planar_quadrilateral(((0.0, 0.0), (100.0, 0.0), (100.0, 50.0), (100.0, 100.0), (0.0, 100.0)))
    assert res5.success is False
    assert res5.status == RectificationStatus.INVALID_POINT_COUNT


def test_duplicate_points():
    """Rejects quadrilateral where two corners are coincident."""
    corners = (
        (100.0, 100.0),
        (100.0, 100.5),  # Coincident with first point (< 2px)
        (300.0, 300.0),
        (100.0, 300.0),
    )
    res = rectify_planar_quadrilateral(corners)
    assert res.success is False
    assert res.status == RectificationStatus.DUPLICATE_POINTS


def test_degenerate_quadrilateral_small_area():
    """Rejects quadrilateral with area below threshold."""
    corners = (
        (10.0, 10.0),
        (12.0, 10.0),
        (12.0, 12.0),
        (10.0, 12.0),
    )  # Area = 4 px^2 < 400 px^2
    res = rectify_planar_quadrilateral(corners)
    assert res.success is False
    assert res.status == RectificationStatus.DEGENERATE_QUADRILATERAL


def test_collinear_points():
    """Rejects quadrilateral where 3 consecutive points lie on the same straight line."""
    corners = (
        (100.0, 100.0),
        (200.0, 100.0),
        (300.0, 100.0),  # Collinear with previous two points
        (200.0, 300.0),
    )
    res = rectify_planar_quadrilateral(corners)
    assert res.success is False
    assert res.status == RectificationStatus.COLLINEAR_POINTS


def test_non_convex_quadrilateral():
    """Rejects self-intersecting (bow-tie) or concave quadrilateral."""
    # Bow-tie / twisted corners
    twisted_corners = (
        (100.0, 100.0),
        (300.0, 300.0),  # Crossed diagonal
        (300.0, 100.0),
        (100.0, 300.0),
    )
    res = rectify_planar_quadrilateral(twisted_corners)
    assert res.success is False
    assert res.status == RectificationStatus.NON_CONVEX_QUADRILATERAL


def test_non_finite_coordinates():
    """Rejects NaN and Inf coordinates."""
    nan_corners = (
        (float("nan"), 0.0),
        (100.0, 0.0),
        (100.0, 100.0),
        (0.0, 100.0),
    )
    res_nan = rectify_planar_quadrilateral(nan_corners)
    assert res_nan.success is False
    assert res_nan.status == RectificationStatus.NON_FINITE_COORDINATES

    inf_corners = (
        (0.0, 0.0),
        (float("inf"), 0.0),
        (100.0, 100.0),
        (0.0, 100.0),
    )
    res_inf = rectify_planar_quadrilateral(inf_corners)
    assert res_inf.success is False
    assert res_inf.status == RectificationStatus.NON_FINITE_COORDINATES


def test_out_of_image_bounds():
    """Rejects corners extending significantly outside the image boundary."""
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    corners = (
        (-50.0, 10.0),  # Well outside [0, 200]
        (100.0, 10.0),
        (100.0, 100.0),
        (10.0, 100.0),
    )
    res = rectify_planar_quadrilateral(corners, image=img)
    assert res.success is False
    assert res.status == RectificationStatus.OUT_OF_IMAGE_BOUNDS


def test_invalid_image_inputs():
    """Rejects empty, non-array, or 1D image inputs gracefully."""
    valid_corners = ((10.0, 10.0), (100.0, 10.0), (100.0, 100.0), (10.0, 100.0))

    # Empty array
    empty_arr = np.array([])
    res_empty = rectify_planar_quadrilateral(valid_corners, image=empty_arr)
    assert res_empty.success is False
    assert res_empty.status == RectificationStatus.INVALID_INPUT

    # Non-array input
    res_str = rectify_planar_quadrilateral(valid_corners, image="not an image")
    assert res_str.success is False
    assert res_str.status == RectificationStatus.INVALID_INPUT


def test_invalid_target_dimensions():
    """Rejects invalid explicit target dimensions."""
    valid_corners = ((10.0, 10.0), (100.0, 10.0), (100.0, 100.0), (10.0, 100.0))

    res_neg = rectify_planar_quadrilateral(valid_corners, target_dimensions=(-10, 100))
    assert res_neg.success is False
    assert res_neg.status == RectificationStatus.INVALID_TARGET_DIMENSIONS

    res_zero = rectify_planar_quadrilateral(valid_corners, target_dimensions=(0, 0))
    assert res_zero.success is False
    assert res_zero.status == RectificationStatus.INVALID_TARGET_DIMENSIONS


def test_extreme_perspective():
    """Validates behavior under steep perspective angles."""
    # Steep perspective trapezoid
    corners = (
        (150.0, 100.0),
        (250.0, 100.0),
        (350.0, 300.0),
        (50.0, 300.0),
    )
    res = rectify_planar_quadrilateral(corners, target_dimensions=(200, 200))
    assert res.success is True
    assert res.status == RectificationStatus.SUCCESS
    assert res.reprojection_error_px < 1e-2


def test_deterministic_repeated_execution():
    """Verifies that multiple runs produce bitwise identical matrices and errors."""
    corners = (
        (25.3, 14.7),
        (312.4, 28.1),
        (295.6, 210.9),
        (18.2, 195.4),
    )
    res1 = rectify_planar_quadrilateral(corners, target_dimensions=(300, 200))
    res2 = rectify_planar_quadrilateral(corners, target_dimensions=(300, 200))

    assert res1.status == res2.status
    assert res1.homography_matrix == res2.homography_matrix
    assert res1.reprojection_error_px == res2.reprojection_error_px


def test_result_to_dict_serialization():
    """Verifies JSON-compatible dictionary serialization."""
    corners = ((0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0))
    res = rectify_planar_quadrilateral(corners, target_dimensions=(100, 100))
    d = res.to_dict()

    assert d["status"] == "SUCCESS"
    assert d["success"] is True
    assert len(d["homography_matrix"]) == 3
    assert len(d["source_corners"]) == 4
    assert len(d["destination_corners"]) == 4
    assert d["output_dimensions"] == [100, 100]


def test_reprojection_error_tolerance_enforced():
    """Confirms rejection when mean reprojection error exceeds configured threshold."""
    corners = (
        (10.0, 10.0),
        (205.0, 12.0),
        (198.0, 150.0),
        (8.0, 145.0),
    )
    # Zero tolerance (0.0 px) enforces strict failure on any floating point residual
    strict_cfg = HomographyConfig(max_reprojection_error_px=0.0)
    res = rectify_planar_quadrilateral(corners, target_dimensions=(200, 150), config=strict_cfg)
    assert res.success is False
    assert res.status == RectificationStatus.TRANSFORMATION_FAILED
    assert "exceeds tolerance" in res.message
    assert res.reprojection_error_px is not None
    assert res.reprojection_error_px >= 0.0

    # Default tolerance (5.0 px) allows numerically valid planar quadrilateral to pass cleanly
    res_default = rectify_planar_quadrilateral(corners, target_dimensions=(200, 150))
    assert res_default.success is True
    assert res_default.status == RectificationStatus.SUCCESS
