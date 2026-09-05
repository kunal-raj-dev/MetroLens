"""
Unit tests for Phase 7: Constrained Cylindrical Packaging Measurement.
Verifies right-cylinder vertical generator invariance, central strip angular bounds,
circumferential foreshortening calculations, geometry classification safety, and error handling.
"""

import math
import numpy as np
import pytest

from nirikshak_shared.models.primitives import CalibrationStatus, BoundingBox
from nirikshak_shared.models.contracts import MeasurementResult
from nirikshak_calibration import CalibrationOutcome
from nirikshak_calibration.cylinder import (
    CylinderGeometryState,
    CylinderMeasurementStatus,
    CylinderModelConfig,
    CylinderMeasurementResult,
    measure_cylindrical_feature,
)


def test_central_vertical_strip_zero_displacement():
    """Feature centered directly on the cylinder axis (phi = 0 deg, cos(phi) = 1.0)."""
    # Cylinder: center_x = 200, R = 100
    # Feature: x = [190, 210] (center = 200), y = [50, 100] (height = 50px)
    box = (190.0, 50.0, 210.0, 100.0)
    cal = 0.1  # mm/px

    res = measure_cylindrical_feature(
        feature_box=box,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        cylinder_center_x=200.0,
        cylinder_radius_px=100.0,
        calibration=cal,
    )

    assert res.status == CylinderMeasurementStatus.SUCCESS
    assert res.geometry_state == CylinderGeometryState.CYLINDRICAL
    assert res.measured_axial_pixels == 50.0
    assert res.measured_axial_mm == 5.0
    assert res.angular_displacement_deg == pytest.approx(0.0, abs=1e-3)
    assert res.cos_phi == pytest.approx(1.0, abs=1e-4)
    assert res.circumferential_correction_factor == pytest.approx(1.0, abs=1e-4)
    assert res.measured_circumferential_pixels == 20.0
    assert res.corrected_circumferential_pixels == 20.0


def test_off_center_vertical_strip_within_central_boundary():
    """Feature at 15 degrees angular displacement (cos(15 deg) ≈ 0.9659)."""
    # R = 200, delta_x = 200 * sin(15 deg) ≈ 51.7638
    angle_rad = math.radians(15.0)
    delta_x = 200.0 * math.sin(angle_rad)

    center_x = 300.0
    feat_center = center_x + delta_x
    box = (feat_center - 15.0, 100.0, feat_center + 15.0, 160.0)  # h=60, w=30

    res = measure_cylindrical_feature(
        feature_box=box,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        cylinder_center_x=center_x,
        cylinder_radius_px=200.0,
        calibration=0.08,
    )

    assert res.status == CylinderMeasurementStatus.SUCCESS
    assert res.angular_displacement_deg == pytest.approx(15.0, abs=1e-2)
    assert res.cos_phi == pytest.approx(math.cos(angle_rad), abs=1e-4)
    expected_corr = 1.0 / math.cos(angle_rad)
    assert res.circumferential_correction_factor == pytest.approx(expected_corr, abs=1e-3)
    # Axial height remains invariant under vertical generator principle
    assert res.measured_axial_pixels == 60.0
    assert res.measured_axial_mm == pytest.approx(60.0 * 0.08, rel=1e-3)


def test_angular_displacement_boundary_and_heuristic_distortion():
    """
    Evaluates behavior at the proposed heuristic boundary of 20 degrees.
    At 20 deg, 1/cos(20 deg) - 1 ≈ 6.42%.
    """
    center_x = 500.0
    r_px = 300.0

    # Theoretical check on 20 deg
    cos_20 = math.cos(math.radians(20.0))
    expected_distortion_pct = (1.0 / cos_20 - 1.0) * 100.0
    assert expected_distortion_pct == pytest.approx(6.418, rel=1e-2)

    # 1. Just below threshold: 19.5 degrees -> SUCCESS
    dx_below = r_px * math.sin(math.radians(19.5))
    box_below = (center_x + dx_below - 10.0, 50.0, center_x + dx_below + 10.0, 90.0)
    res_below = measure_cylindrical_feature(
        feature_box=box_below,
        cylinder_center_x=center_x,
        cylinder_radius_px=r_px,
        calibration=0.1,
    )
    assert res_below.status == CylinderMeasurementStatus.SUCCESS

    # 2. Just above threshold: 20.5 degrees -> EXCEEDS_ANGULAR_THRESHOLD
    dx_above = r_px * math.sin(math.radians(20.5))
    box_above = (center_x + dx_above - 10.0, 50.0, center_x + dx_above + 10.0, 90.0)
    res_above = measure_cylindrical_feature(
        feature_box=box_above,
        cylinder_center_x=center_x,
        cylinder_radius_px=r_px,
        calibration=0.1,
    )
    assert res_above.status == CylinderMeasurementStatus.EXCEEDS_ANGULAR_THRESHOLD
    assert "exceeds proposed heuristic threshold" in res_above.message


def test_planar_geometry_receives_no_correction():
    """Planar surface receives NO cylindrical curvature correction (factor = 1.0)."""
    box = (50.0, 50.0, 100.0, 150.0)  # w=50, h=100
    res = measure_cylindrical_feature(
        feature_box=box,
        geometry_state=CylinderGeometryState.PLANAR,
        calibration=0.05,
    )
    assert res.status == CylinderMeasurementStatus.PLANAR_NO_CORRECTION
    assert res.geometry_state == CylinderGeometryState.PLANAR
    assert res.circumferential_correction_factor == 1.0
    assert res.cos_phi == 1.0
    assert res.angular_displacement_deg == 0.0
    assert res.measured_axial_pixels == 100.0
    assert res.measured_axial_mm == 5.0
    assert res.corrected_circumferential_pixels == 50.0


def test_unsupported_tapered_packaging_routes_to_manual_review():
    """Tapered packaging surfaces route to MANUAL_REVIEW_REQUIRED."""
    box = (40.0, 40.0, 80.0, 100.0)
    res = measure_cylindrical_feature(
        feature_box=box,
        geometry_state=CylinderGeometryState.UNSUPPORTED_TAPERED,
        calibration=0.1,
    )
    assert res.status == CylinderMeasurementStatus.UNSUPPORTED_TAPERED
    assert res.geometry_state == CylinderGeometryState.UNSUPPORTED_TAPERED
    assert "MANUAL_REVIEW_REQUIRED" in res.message


def test_unknown_geometry_routes_to_manual_review():
    """Unknown surface geometry routes to MANUAL_REVIEW_REQUIRED."""
    box = (40.0, 40.0, 80.0, 100.0)
    res = measure_cylindrical_feature(
        feature_box=box,
        geometry_state=CylinderGeometryState.UNKNOWN,
        calibration=0.1,
    )
    assert res.status == CylinderMeasurementStatus.UNKNOWN_GEOMETRY
    assert res.geometry_state == CylinderGeometryState.UNKNOWN
    assert "MANUAL_REVIEW_REQUIRED" in res.message


def test_axial_vs_circumferential_distinction():
    """
    CRITICAL TEST: Demonstrates that axial height along generator is unchanged
    while circumferential width is corrected by 1/cos(phi).
    """
    center_x = 400.0
    r_px = 250.0
    phi_target = math.radians(18.0)
    dx = r_px * math.sin(phi_target)

    # Box with raw width = 40px, raw height = 80px
    feat_x = center_x + dx
    box = (feat_x - 20.0, 100.0, feat_x + 20.0, 180.0)
    cal = 0.05

    res = measure_cylindrical_feature(
        box,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        cylinder_center_x=center_x,
        cylinder_radius_px=r_px,
        calibration=cal,
    )

    # 1. Axial measurement is NOT multiplied by 1/cos(phi)
    assert res.measured_axial_pixels == 80.0
    assert res.measured_axial_mm == 4.0

    # 2. Circumferential width IS corrected by 1/cos(phi)
    cos_phi = math.cos(phi_target)
    expected_corr_width = 40.0 / cos_phi
    assert res.corrected_circumferential_pixels == pytest.approx(expected_corr_width, rel=1e-3)
    assert res.corrected_circumferential_pixels > res.measured_circumferential_pixels


def test_axis_misaligned_condition():
    """Rejects generator invariance calculation when cylinder axis is not aligned."""
    box = (100.0, 100.0, 150.0, 200.0)
    res = measure_cylindrical_feature(
        box,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        cylinder_center_x=125.0,
        cylinder_radius_px=100.0,
        calibration=0.1,
        is_axis_aligned=False,  # NOT aligned!
    )
    assert res.status == CylinderMeasurementStatus.MISALIGNED_AXIS
    assert "requires cylinder axis to be aligned" in res.message


def test_feature_outside_cylinder_silhouette():
    """Rejects features located beyond the apparent cylinder radius."""
    center_x = 200.0
    r_px = 80.0
    # Feature centered at x = 320 -> delta_x = 120 > R=80 -> sin(phi) = 1.5 > 1.0
    box = (310.0, 50.0, 330.0, 90.0)

    res = measure_cylindrical_feature(
        box,
        geometry_state=CylinderGeometryState.CYLINDRICAL,
        cylinder_center_x=center_x,
        cylinder_radius_px=r_px,
        calibration=0.1,
    )
    assert res.status == CylinderMeasurementStatus.OUT_OF_CYLINDER_BOUNDS


def test_malformed_feature_coordinates():
    """Rejects inverted, non-numeric, or NaN bounding coordinates."""
    # Inverted y (ymin > ymax)
    res_inv = measure_cylindrical_feature((10.0, 80.0, 40.0, 50.0), cylinder_center_x=20.0, cylinder_radius_px=50.0)
    assert res_inv.status == CylinderMeasurementStatus.INVALID_INPUT

    # NaN coordinates
    res_nan = measure_cylindrical_feature((float("nan"), 10.0, 40.0, 50.0), cylinder_center_x=20.0, cylinder_radius_px=50.0)
    assert res_nan.status == CylinderMeasurementStatus.INVALID_INPUT


def test_invalid_cylinder_radius():
    """Rejects zero, negative, or degenerate cylinder radius."""
    box = (10.0, 10.0, 40.0, 50.0)

    # Zero radius
    res_zero = measure_cylindrical_feature(box, cylinder_center_x=25.0, cylinder_radius_px=0.0)
    assert res_zero.status == CylinderMeasurementStatus.INVALID_INPUT

    # Radius smaller than minimum threshold (20px)
    res_small = measure_cylindrical_feature(box, cylinder_center_x=25.0, cylinder_radius_px=10.0)
    assert res_small.status == CylinderMeasurementStatus.INVALID_INPUT


def test_uncalibrated_scale_handling():
    """Handles missing or uncalibrated scale gracefully without fabricating scale."""
    box = (190.0, 50.0, 210.0, 100.0)
    res_none = measure_cylindrical_feature(
        box,
        cylinder_center_x=200.0,
        cylinder_radius_px=100.0,
        calibration=None,
    )
    assert res_none.status == CylinderMeasurementStatus.UNCALIBRATED
    assert res_none.measured_axial_pixels == 50.0
    assert res_none.measured_axial_mm is None  # Zero scale fabrication!
    assert res_none.calibration_status == CalibrationStatus.UNCALIBRATED


def test_monotonic_increasing_displacement_gradient():
    """Verifies that increasing phi causes monotonic increase in circumferential correction."""
    center_x = 500.0
    r_px = 400.0
    angles_deg = [0.0, 5.0, 10.0, 15.0, 20.0]

    factors = []
    cos_values = []
    for deg in angles_deg:
        dx = r_px * math.sin(math.radians(deg))
        box = (center_x + dx - 10.0, 50.0, center_x + dx + 10.0, 90.0)
        res = measure_cylindrical_feature(
            box,
            cylinder_center_x=center_x,
            cylinder_radius_px=r_px,
            calibration=0.1,
        )
        factors.append(res.circumferential_correction_factor)
        cos_values.append(res.cos_phi)

    # Check monotonic decrease in cos(phi)
    for i in range(len(cos_values) - 1):
        assert cos_values[i] >= cos_values[i + 1]

    # Check monotonic increase in correction factor 1/cos(phi)
    for i in range(len(factors) - 1):
        assert factors[i] <= factors[i + 1]


def test_deterministic_repeated_execution():
    """Repeated calls produce identical results."""
    box = (212.4, 45.2, 235.1, 98.7)
    res1 = measure_cylindrical_feature(box, cylinder_center_x=200.0, cylinder_radius_px=150.0, calibration=0.08)
    res2 = measure_cylindrical_feature(box, cylinder_center_x=200.0, cylinder_radius_px=150.0, calibration=0.08)

    assert res1.status == res2.status
    assert res1.measured_axial_pixels == res2.measured_axial_pixels
    assert res1.circumferential_correction_factor == res2.circumferential_correction_factor
    assert res1.angular_displacement_deg == res2.angular_displacement_deg


def test_to_dict_serialization():
    """Serializes result into an inspectable dictionary."""
    box = (190.0, 50.0, 210.0, 100.0)
    res = measure_cylindrical_feature(box, cylinder_center_x=200.0, cylinder_radius_px=100.0, calibration=0.1)
    d = res.to_dict()

    assert d["status"] == "SUCCESS"
    assert d["geometry_state"] == "CYLINDRICAL"
    assert d["measured_axial_pixels"] == 50.0
    assert d["measured_axial_mm"] == 5.0
    assert d["angular_displacement_deg"] == 0.0
    assert d["cos_phi"] == 1.0


def test_cylinder_measurement_result_bridge_to_contracts():
    """Verifies that to_measurement_result() converts directly into nirikshak_shared.models.contracts.MeasurementResult."""
    box = (190.0, 50.0, 210.0, 100.0)
    cal = CalibrationOutcome(
        status=CalibrationStatus.CALIBRATED,
        scale_factor_mm_per_pixel=0.1,
        uncertainty_mm_per_pixel=0.002,
    )
    res = measure_cylindrical_feature(
        box,
        cylinder_center_x=200.0,
        cylinder_radius_px=100.0,
        calibration=cal,
    )
    mr = res.to_measurement_result(feature_name="numeral_height_mm")
    assert isinstance(mr, MeasurementResult)
    assert mr.feature_name == "numeral_height_mm"
    assert mr.measured_pixels == 50.0
    assert mr.scale_factor_mm_per_pixel == 0.1
    assert mr.measured_mm == 5.0
    assert mr.uncertainty_mm == pytest.approx(50.0 * 0.002, rel=1e-3)
    assert mr.calibration_status == CalibrationStatus.CALIBRATED
    assert mr.bounding_box is None  # default None

    # Uncalibrated bridge test
    res_uncal = measure_cylindrical_feature(
        box,
        cylinder_center_x=200.0,
        cylinder_radius_px=100.0,
        calibration=None,
    )
    mr_uncal = res_uncal.to_measurement_result()
    assert isinstance(mr_uncal, MeasurementResult)
    assert mr_uncal.measured_pixels == 50.0
    assert mr_uncal.scale_factor_mm_per_pixel is None
    assert mr_uncal.measured_mm is None
    assert mr_uncal.uncertainty_mm is None
    assert mr_uncal.calibration_status == CalibrationStatus.UNCALIBRATED

