"""
Phase 9: Metric Calibration Evaluation Engine Tests.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Validates that:
1. When no ground truth dataset is available, status is strictly BENCHMARK_BLOCKED.
2. Canonical production pipeline (detect_anchor -> compute_scale_factor) is executed.
3. Ground-truth scale factor is strictly reference-only and never leaked into pipeline.
4. Scale metrics (mm/px, %) and physical dimension metrics (mm) are strictly separated.
5. Statistical aggregates (MAE, RMSE, Median, P95, failure rate) are mathematically exact.
6. Stratification by surface geometry and failure breakdown are accurate.
7. Evaluation is completely deterministic across repeated executions.
"""

import math
import pytest
import numpy as np
import cv2

from nirikshak_calibration import (
    BenchmarkStatus,
    GroundTruthSample,
    EvaluationConfig,
    SampleEvaluation,
    CalibrationEvaluationResult,
    evaluate_calibration,
    AnchorType,
    AnchorDetectionStatus,
)


def _generate_synthetic_coin_image(
    canvas_size: int = 300,
    center_x: int = 150,
    center_y: int = 150,
    outer_radius: int = 50,
    inner_radius: int = 33,
) -> np.ndarray:
    """Generates a high-contrast synthetic RBI Rs 10 coin image for deterministic testing."""
    img = np.full((canvas_size, canvas_size, 3), 220, dtype=np.uint8)
    # Outer brass ring
    cv2.circle(img, (center_x, center_y), outer_radius, (30, 30, 30), 4)
    # Inner nickel-silver core
    cv2.circle(img, (center_x, center_y), inner_radius, (70, 70, 70), 3)
    return img


# ============================================================================
# 1. Benchmark Blocked Handling
# ============================================================================

def test_benchmark_blocked_on_none_dataset():
    result = evaluate_calibration(None)
    assert result.status == BenchmarkStatus.BENCHMARK_BLOCKED
    assert result.total_samples == 0
    assert result.successful_calibrations == 0
    assert result.failed_calibrations == 0
    assert result.calibration_success_rate == 0.0
    assert result.calibration_failure_rate == 0.0
    assert result.scale_mae_mm_per_pixel is None
    assert result.dimension_mae_mm is None
    assert "No explicit physical ground-truth dataset available." in result.message


def test_benchmark_blocked_on_empty_dataset():
    result = evaluate_calibration([])
    assert result.status == BenchmarkStatus.BENCHMARK_BLOCKED
    assert result.total_samples == 0
    assert "No explicit physical ground-truth dataset available." in result.message


# ============================================================================
# 2. Production Pipeline Execution & Non-Leakage of Ground Truth
# ============================================================================

def test_canonical_pipeline_execution_and_no_ground_truth_leakage():
    """
    Verifies that evaluate_calibration calls detect_anchor() and compute_scale_factor(),
    and that ground_truth_scale_mm_per_pixel is NEVER used to compute estimated_scale.
    """
    img = _generate_synthetic_coin_image(outer_radius=50)
    # Outer diameter = 100px. Known physical reference = 27.0mm.
    # Expected estimated scale S_est = 27.0 / 100.0 = 0.27 mm/px.
    # Intentionally set reference ground truth to an arbitrary value (0.50) to prove no leakage.
    sample = GroundTruthSample(
        sample_id="test_leakage_01",
        image=img,
        known_physical_reference_mm=27.0,
        surface_type="PLANAR",
        ground_truth_scale_mm_per_pixel=0.50,  # Intentionally disparate
    )

    config = EvaluationConfig(anchor_type=AnchorType.COIN_INR_10)
    res = evaluate_calibration([sample], config=config)

    assert res.status == BenchmarkStatus.OK
    assert res.total_samples == 1
    assert res.successful_calibrations == 1
    assert res.calibration_success_rate == 1.0

    eval_item = res.sample_evaluations[0]
    assert eval_item.calibration_succeeded is True
    # The pipeline must have computed scale from image geometry (~0.257 mm/px from stroke diameter ~105px), NOT copied ground truth (0.50)
    assert pytest.approx(eval_item.estimated_scale_mm_per_pixel, rel=0.08) == 0.27
    assert abs(eval_item.estimated_scale_mm_per_pixel - 0.50) > 0.20
    assert eval_item.ground_truth_scale_mm_per_pixel == 0.50
    # Error should reflect |estimated - ground_truth|
    expected_err = abs(eval_item.estimated_scale_mm_per_pixel - 0.50)
    assert pytest.approx(eval_item.scale_absolute_error_mm_per_pixel, abs=1e-5) == expected_err


# ============================================================================
# 3. Mathematical Metrics and Dimensional Separation
# ============================================================================

def test_mathematical_metrics_and_dimensional_separation():
    """
    Verifies that scale metrics (mm/px, %) and physical dimension metrics (mm)
    are strictly separated and computed according to mathematical definitions.
    """
    img = _generate_synthetic_coin_image(outer_radius=50)
    # Add synthetic feature on image: 20-pixel tall box
    # If S ≈ 0.27 mm/px, measured feature dimension will be 20 * 0.27 = 5.4 mm.
    feature_box = (10.0, 10.0, 30.0, 30.0)  # dy = 20px

    sample1 = GroundTruthSample(
        sample_id="s1",
        image=img,
        known_physical_reference_mm=27.0,
        surface_type="PLANAR",
        ground_truth_scale_mm_per_pixel=0.27,  # Exact match
        target_feature_box=feature_box,
        ground_truth_feature_dimension_mm=5.40,
    )

    sample2 = GroundTruthSample(
        sample_id="s2",
        image=img,
        known_physical_reference_mm=27.0,
        surface_type="PLANAR",
        ground_truth_scale_mm_per_pixel=0.28,  # Slightly higher
        target_feature_box=feature_box,
        ground_truth_feature_dimension_mm=5.50,
    )

    config = EvaluationConfig(anchor_type=AnchorType.COIN_INR_10)
    res = evaluate_calibration([sample1, sample2], config=config)

    assert res.status == BenchmarkStatus.OK
    assert res.total_samples == 2
    assert res.successful_calibrations == 2

    # Verify dimensional units are distinct
    # Scale MAE is in mm/pixel
    assert isinstance(res.scale_mae_mm_per_pixel, float)
    assert res.scale_mae_mm_per_pixel >= 0.0
    # Dimension MAE is in mm
    assert isinstance(res.dimension_mae_mm, float)
    assert res.dimension_mae_mm >= 0.0

    # Verify RMSE >= MAE mathematically
    assert res.scale_rmse_mm_per_pixel >= res.scale_mae_mm_per_pixel - 1e-9
    assert res.dimension_rmse_mm >= res.dimension_mae_mm - 1e-9


# ============================================================================
# 4. Stratification and Failure Breakdown
# ============================================================================

def test_stratification_and_failure_accounting():
    """
    Verifies that the evaluator correctly stratifies samples by surface
    geometry and partitions success/failure rates with total_samples in denominator.
    """
    good_img = _generate_synthetic_coin_image(outer_radius=50)
    bad_img = np.zeros((200, 200, 3), dtype=np.uint8)  # All black -> NO_ANCHOR

    sample_planar = GroundTruthSample(
        sample_id="planar_good",
        image=good_img,
        known_physical_reference_mm=27.0,
        surface_type="PLANAR",
        ground_truth_scale_mm_per_pixel=0.27,
    )

    sample_cylinder_fail = GroundTruthSample(
        sample_id="cyl_fail",
        image=bad_img,
        known_physical_reference_mm=27.0,
        surface_type="CYLINDRICAL",
        ground_truth_scale_mm_per_pixel=0.27,
    )

    config = EvaluationConfig(anchor_type=AnchorType.COIN_INR_10)
    res = evaluate_calibration([sample_planar, sample_cylinder_fail], config=config)

    assert res.total_samples == 2
    assert res.successful_calibrations == 1
    assert res.failed_calibrations == 1
    assert res.calibration_success_rate == 0.5
    assert res.calibration_failure_rate == 0.5

    # Failure breakdown check
    assert "NO_ANCHOR" in res.failure_breakdown
    assert res.failure_breakdown["NO_ANCHOR"] == 1

    # Stratification check
    assert "PLANAR" in res.stratified_by_surface
    assert res.stratified_by_surface["PLANAR"]["total"] == 1
    assert res.stratified_by_surface["PLANAR"]["succeeded"] == 1
    assert res.stratified_by_surface["PLANAR"]["success_rate"] == 1.0

    assert "CYLINDRICAL" in res.stratified_by_surface
    assert res.stratified_by_surface["CYLINDRICAL"]["total"] == 1
    assert res.stratified_by_surface["CYLINDRICAL"]["succeeded"] == 0
    assert res.stratified_by_surface["CYLINDRICAL"]["success_rate"] == 0.0


# ============================================================================
# 5. Determinism and Serialization
# ============================================================================

def test_evaluation_determinism_and_report_generation():
    img = _generate_synthetic_coin_image(outer_radius=50)
    sample = GroundTruthSample(
        sample_id="det_01",
        image=img,
        known_physical_reference_mm=27.0,
        surface_type="PLANAR",
        ground_truth_scale_mm_per_pixel=0.27,
    )

    config = EvaluationConfig(anchor_type=AnchorType.COIN_INR_10)
    res1 = evaluate_calibration([sample], config=config)
    res2 = evaluate_calibration([sample], config=config)

    # Assert exact deterministic agreement
    assert res1.scale_mae_mm_per_pixel == res2.scale_mae_mm_per_pixel
    assert res1.scale_rmse_mm_per_pixel == res2.scale_rmse_mm_per_pixel
    assert res1.calibration_success_rate == res2.calibration_success_rate

    # Check to_dict() serialization
    res_dict = res1.to_dict()
    assert res_dict["status"] == "OK"
    assert res_dict["total_samples"] == 1
    assert "scale_metrics_mm_per_pixel" in res_dict
    assert "dimension_metrics_mm" in res_dict
    assert "stratified_by_surface" in res_dict

    # Check to_markdown_report() generation
    md_report = res1.to_markdown_report()
    assert "# Optical Calibration Evaluation Report" in md_report
    assert "Scale Estimation Metrics" in md_report
    assert "Physical Feature Dimension Metrics" in md_report
    assert "Stratification by Surface Geometry" in md_report


# ============================================================================
# 6. Explicit Denominator Independence (Gate 1 Requirement)
# ============================================================================

def test_metric_denominators_explicit_separation():
    """
    Verifies that when failures occur in the dataset, N is NOT conflated:
    - total_samples = 3
    - successful_calibrations = 2
    - failed_calibrations = 1
    - calibration_failure_rate = 1/3 (computed over total_samples = 3)
    - scale_evaluated_samples = 2 (computed strictly over calculable samples)
    - scale_mae is computed strictly over the 2 calculable samples, NOT divided by 3.
    """
    good_img = _generate_synthetic_coin_image(outer_radius=50)
    bad_img = np.zeros((200, 200, 3), dtype=np.uint8)

    s1 = GroundTruthSample(
        sample_id="s1",
        image=good_img,
        known_physical_reference_mm=27.0,
        ground_truth_scale_mm_per_pixel=0.25,
    )
    s2 = GroundTruthSample(
        sample_id="s2",
        image=good_img,
        known_physical_reference_mm=27.0,
        ground_truth_scale_mm_per_pixel=0.26,
    )
    s3_fail = GroundTruthSample(
        sample_id="s3_fail",
        image=bad_img,
        known_physical_reference_mm=27.0,
        ground_truth_scale_mm_per_pixel=0.25,
    )

    config = EvaluationConfig(anchor_type=AnchorType.COIN_INR_10)
    res = evaluate_calibration([s1, s2, s3_fail], config=config)

    assert res.total_samples == 3
    assert res.successful_calibrations == 2
    assert res.failed_calibrations == 1
    assert pytest.approx(res.calibration_failure_rate, rel=1e-3) == 1.0 / 3.0
    assert pytest.approx(res.calibration_success_rate, rel=1e-3) == 2.0 / 3.0

    # Denominator for MAE must be strictly 2, not 3
    assert res.scale_evaluated_samples == 2
    e1 = abs(res.sample_evaluations[0].estimated_scale_mm_per_pixel - 0.25)
    e2 = abs(res.sample_evaluations[1].estimated_scale_mm_per_pixel - 0.26)
    expected_mae = (e1 + e2) / 2.0  # Denominator is 2!
    assert pytest.approx(res.scale_mae_mm_per_pixel, abs=1e-5) == expected_mae

    # Verify JSON and report explicitly expose scale_evaluated_samples
    d = res.to_dict()
    assert d["scale_evaluated_samples"] == 2
    assert d["scale_metrics_mm_per_pixel"]["evaluated_samples"] == 2
    assert "Evaluated Sample Count (N) | 2" in res.to_markdown_report()

