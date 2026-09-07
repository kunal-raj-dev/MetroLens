"""
Phase 9: Metric Calibration Evaluation Engine & Rigorous Benchmarking Pipeline.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Responsibilities:
- Evaluates the canonical Member 2 calibration pipeline against ground-truth datasets.
- Dispatches each sample through the production detection and scale estimation path:
    detect_anchor() -> compute_scale_factor() -> S_estimated
- Strict separation of ground truth from pipeline inputs:
    known_physical_reference_mm is input; ground_truth_scale_mm_per_pixel is reference-only.
- Strict dimensional separation:
    Scale metrics: mm/pixel and % relative error.
    Physical dimension metrics: mm.
- Handles empty/missing dataset by emitting structured BENCHMARK_BLOCKED status.
- Zero scale fabrication; zero manufactured benchmark claims.
"""

import math
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
import numpy as np

from nirikshak_shared.models.primitives import CalibrationStatus
from .types import (
    AnchorType,
    AnchorDetectionStatus,
    AnchorDetectionResult,
    AnchorDetectorConfig,
    EllipseGeometry,
    CardGeometry,
)
from .anchor_detector import detect_anchor
from . import compute_scale_factor, CalibrationOutcome
from .font_measurer import measure_font_height, FontMeasurementType, FontMeasurementStatus
from .cylinder import measure_cylindrical_feature, CylinderGeometryState, CylinderMeasurementStatus


class BenchmarkStatus(str, Enum):
    """Taxonomy of calibration evaluation outcomes."""
    OK = "OK"
    BENCHMARK_BLOCKED = "BENCHMARK_BLOCKED"
    INVALID_DATASET = "INVALID_DATASET"


@dataclass(frozen=True)
class GroundTruthSample:
    """
    A single ground-truth test sample for calibration and physical measurement evaluation.

    Attributes:
        sample_id: Unique string identifier for the test sample.
        image: NumPy ndarray of the packaging frame.
        known_physical_reference_mm: True physical diameter/width of the fiducial marker in mm.
            Passed to calibration pipeline (e.g. 27.0mm for INR 10 coin, 85.60mm for ID-1 card).
        surface_type: Packaging surface geometry ("PLANAR", "CYLINDRICAL", etc.).
        ground_truth_scale_mm_per_pixel: Reference-only ground-truth optical scale factor.
            CRITICAL: Evaluator uses this ONLY to compute error; NEVER passed to pipeline.
        target_feature_box: Optional (xmin, ymin, xmax, ymax) coordinate box of a physical feature.
        ground_truth_feature_dimension_mm: Reference-only true physical height of target feature in mm.
        metadata: Optional dictionary with additional camera or scene metadata.
    """
    sample_id: str
    image: np.ndarray
    known_physical_reference_mm: float
    surface_type: str = "PLANAR"
    ground_truth_scale_mm_per_pixel: Optional[float] = None
    target_feature_box: Optional[Tuple[float, float, float, float]] = None
    ground_truth_feature_dimension_mm: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class EvaluationConfig:
    """
    Configuration and pass/fail thresholds for calibration benchmarking.

    Evidentiary Status:
        Thresholds represent proposed verification criteria for packaging metrology.
    """
    target_relative_scale_error: float = 0.05       # <= 5.0% relative scale error target
    target_dimension_mae_mm: float = 0.15           # <= 0.15 mm physical feature MAE target
    min_success_rate: float = 0.90                  # >= 90% anchor detection & calibration rate
    anchor_type: Optional[AnchorType] = None        # Default AUTO
    anchor_config: Optional[AnchorDetectorConfig] = None


@dataclass(frozen=True)
class SampleEvaluation:
    """Detailed evaluation result for an individual ground-truth sample."""
    sample_id: str
    surface_type: str
    calibration_succeeded: bool
    status: str
    estimated_scale_mm_per_pixel: Optional[float] = None
    ground_truth_scale_mm_per_pixel: Optional[float] = None
    scale_absolute_error_mm_per_pixel: Optional[float] = None
    scale_relative_error: Optional[float] = None
    measured_feature_mm: Optional[float] = None
    ground_truth_feature_mm: Optional[float] = None
    feature_dimension_absolute_error_mm: Optional[float] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "surface_type": self.surface_type,
            "calibration_succeeded": self.calibration_succeeded,
            "status": self.status,
            "estimated_scale_mm_per_pixel": self.estimated_scale_mm_per_pixel,
            "ground_truth_scale_mm_per_pixel": self.ground_truth_scale_mm_per_pixel,
            "scale_absolute_error_mm_per_pixel": self.scale_absolute_error_mm_per_pixel,
            "scale_relative_error": self.scale_relative_error,
            "measured_feature_mm": self.measured_feature_mm,
            "ground_truth_feature_mm": self.ground_truth_feature_mm,
            "feature_dimension_absolute_error_mm": self.feature_dimension_absolute_error_mm,
            "message": self.message,
        }


@dataclass(frozen=True)
class CalibrationEvaluationResult:
    """
    Complete summary report produced by the calibration evaluation pipeline.

    Metrics strictly separate:
    - Scale errors in mm/pixel and % relative error.
    - Physical feature dimension errors in mm.
    """
    status: BenchmarkStatus
    total_samples: int
    successful_calibrations: int
    failed_calibrations: int
    calibration_success_rate: float
    calibration_failure_rate: float

    # Denominator Accounting: Explicit sample counts
    scale_evaluated_samples: int = 0
    dimension_evaluated_samples: int = 0

    # Scale Error Metrics (Units: mm/pixel or ratio)
    scale_mae_mm_per_pixel: Optional[float] = None
    scale_median_ae_mm_per_pixel: Optional[float] = None
    scale_rmse_mm_per_pixel: Optional[float] = None
    scale_p95_ae_mm_per_pixel: Optional[float] = None
    scale_relative_error_mean: Optional[float] = None
    scale_relative_error_median: Optional[float] = None

    # Physical Feature Dimension Metrics (Units: mm)
    dimension_mae_mm: Optional[float] = None
    dimension_median_ae_mm: Optional[float] = None
    dimension_rmse_mm: Optional[float] = None
    dimension_p95_ae_mm: Optional[float] = None

    # Pass/Fail Verdicts
    scale_target_passed: Optional[bool] = None
    dimension_target_passed: Optional[bool] = None
    success_rate_passed: Optional[bool] = None

    # Stratification and diagnostics
    stratified_by_surface: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    failure_breakdown: Dict[str, int] = field(default_factory=dict)
    sample_evaluations: List[SampleEvaluation] = field(default_factory=list)
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into inspectable dictionary."""
        return {
            "status": self.status.value,
            "total_samples": self.total_samples,
            "successful_calibrations": self.successful_calibrations,
            "failed_calibrations": self.failed_calibrations,
            "calibration_success_rate": round(self.calibration_success_rate, 4),
            "calibration_failure_rate": round(self.calibration_failure_rate, 4),
            "scale_evaluated_samples": self.scale_evaluated_samples,
            "dimension_evaluated_samples": self.dimension_evaluated_samples,
            "scale_metrics_mm_per_pixel": {
                "evaluated_samples": self.scale_evaluated_samples,
                "mae": self.scale_mae_mm_per_pixel,
                "median_ae": self.scale_median_ae_mm_per_pixel,
                "rmse": self.scale_rmse_mm_per_pixel,
                "p95_ae": self.scale_p95_ae_mm_per_pixel,
                "relative_error_mean": self.scale_relative_error_mean,
                "relative_error_median": self.scale_relative_error_median,
            },
            "dimension_metrics_mm": {
                "evaluated_samples": self.dimension_evaluated_samples,
                "mae": self.dimension_mae_mm,
                "median_ae": self.dimension_median_ae_mm,
                "rmse": self.dimension_rmse_mm,
                "p95_ae": self.dimension_p95_ae_mm,
            },
            "verdicts": {
                "scale_target_passed": self.scale_target_passed,
                "dimension_target_passed": self.dimension_target_passed,
                "success_rate_passed": self.success_rate_passed,
            },
            "stratified_by_surface": self.stratified_by_surface,
            "failure_breakdown": self.failure_breakdown,
            "sample_evaluations": [s.to_dict() for s in self.sample_evaluations],
            "message": self.message,
        }

    def to_markdown_report(self) -> str:
        """Generates a structured GitHub-flavored markdown report."""
        status_icon = "🟢" if self.status == BenchmarkStatus.OK else "🟡"
        lines = [
            f"# Optical Calibration Evaluation Report",
            "",
            f"**Overall Benchmark Status:** {status_icon} `{self.status.value}`  ",
            f"**Diagnostic Message:** {self.message or 'N/A'}",
            "",
            "## 1. Executive Summary",
            "",
            "| Metric | Value | Target | Verdict |",
            "| :--- | :---: | :---: | :---: |",
            f"| Total Samples | {self.total_samples} | - | - |",
            f"| Successful Calibrations | {self.successful_calibrations} | - | - |",
            f"| Failed Calibrations | {self.failed_calibrations} | - | - |",
            f"| Calibration Success Rate | {self.calibration_success_rate:.1%} | >= 90.0% | {'✅ PASS' if self.success_rate_passed else ('⚠️ BLOCKED' if self.status == BenchmarkStatus.BENCHMARK_BLOCKED else '❌ FAIL')} |",
            f"| Calibration Failure Rate | {self.calibration_failure_rate:.1%} | - | - |",
            f"| Scale Evaluated Samples (N) | {self.scale_evaluated_samples} | - | - |",
            f"| Dimension Evaluated Samples (N) | {self.dimension_evaluated_samples} | - | - |",
        ]

        if self.scale_relative_error_mean is not None:
            v_scale = "✅ PASS" if self.scale_target_passed else "❌ FAIL"
            lines.append(f"| Scale Mean Relative Error | {self.scale_relative_error_mean:.2%} (N={self.scale_evaluated_samples}) | <= 5.0% | {v_scale} |")
        else:
            lines.append(f"| Scale Mean Relative Error | N/A | <= 5.0% | ⚠️ BLOCKED |")

        if self.dimension_mae_mm is not None:
            v_dim = "✅ PASS" if self.dimension_target_passed else "❌ FAIL"
            lines.append(f"| Feature Dimension MAE | {self.dimension_mae_mm:.4f} mm (N={self.dimension_evaluated_samples}) | <= 0.1500 mm | {v_dim} |")
        else:
            lines.append(f"| Feature Dimension MAE | N/A | <= 0.1500 mm | ⚠️ BLOCKED |")

        lines.extend([
            "",
            "## 2. Scale Estimation Metrics (Units: mm/pixel or %)",
            "",
            f"*Denominator Note: Metrics computed strictly over N = {self.scale_evaluated_samples} successfully calibrated samples with ground-truth scale. "
            f"Dataset-level calibration reliability is independently captured by the Calibration Failure Rate ({self.calibration_failure_rate:.1%} over all {self.total_samples} samples).*  ",
            "",
            "| Metric | Value | Unit |",
            "| :--- | :---: | :---: |",
            f"| Evaluated Sample Count (N) | {self.scale_evaluated_samples} | samples |",
            f"| Mean Absolute Error (MAE) | {self.scale_mae_mm_per_pixel if self.scale_mae_mm_per_pixel is not None else 'N/A'} | mm/px |",
            f"| Median Absolute Error | {self.scale_median_ae_mm_per_pixel if self.scale_median_ae_mm_per_pixel is not None else 'N/A'} | mm/px |",
            f"| Root Mean Square Error (RMSE) | {self.scale_rmse_mm_per_pixel if self.scale_rmse_mm_per_pixel is not None else 'N/A'} | mm/px |",
            f"| 95th Percentile Error (P95) | {self.scale_p95_ae_mm_per_pixel if self.scale_p95_ae_mm_per_pixel is not None else 'N/A'} | mm/px |",
            f"| Mean Relative Error | {f'{self.scale_relative_error_mean:.2%}' if self.scale_relative_error_mean is not None else 'N/A'} | % |",
            f"| Median Relative Error | {f'{self.scale_relative_error_median:.2%}' if self.scale_relative_error_median is not None else 'N/A'} | % |",
            "",
            "## 3. Physical Feature Dimension Metrics (Units: mm)",
            "",
            f"*Denominator Note: Metrics computed strictly over N = {self.dimension_evaluated_samples} samples with physical feature ground truth.*  ",
            "",
            "| Metric | Value | Unit |",
            "| :--- | :---: | :---: |",
            f"| Evaluated Sample Count (N) | {self.dimension_evaluated_samples} | samples |",
            f"| Dimension MAE | {f'{self.dimension_mae_mm:.4f}' if self.dimension_mae_mm is not None else 'N/A'} | mm |",
            f"| Dimension Median AE | {f'{self.dimension_median_ae_mm:.4f}' if self.dimension_median_ae_mm is not None else 'N/A'} | mm |",
            f"| Dimension RMSE | {f'{self.dimension_rmse_mm:.4f}' if self.dimension_rmse_mm is not None else 'N/A'} | mm |",
            f"| Dimension P95 AE | {f'{self.dimension_p95_ae_mm:.4f}' if self.dimension_p95_ae_mm is not None else 'N/A'} | mm |",
            "",
            "## 4. Failure Mode Breakdown",
            "",
        ])

        if self.failure_breakdown:
            lines.extend([
                "| Failure Reason Code | Count | Fraction |",
                "| :--- | :---: | :---: |",
            ])
            for reason, count in sorted(self.failure_breakdown.items()):
                frac = count / self.total_samples if self.total_samples > 0 else 0.0
                lines.append(f"| `{reason}` | {count} | {frac:.1%} |")
        else:
            lines.append("No failures recorded across evaluation dataset.")

        if self.stratified_by_surface:
            lines.extend([
                "",
                "## 5. Stratification by Surface Geometry",
                "",
                "| Surface Type | Total | Succeeded | Success Rate | Scale MAE (mm/px) | Dim MAE (mm) |",
                "| :--- | :---: | :---: | :---: | :---: | :---: |",
            ])
            for surf, data in sorted(self.stratified_by_surface.items()):
                s_rate = data["success_rate"]
                s_mae = data.get("scale_mae", "N/A")
                d_mae = data.get("dimension_mae", "N/A")
                lines.append(f"| `{surf}` | {data['total']} | {data['succeeded']} | {s_rate:.1%} | {s_mae} | {d_mae} |")

        lines.extend([
            "",
            "---",
            "*Evidentiary Note: Physical ground-truth verification requires physical calibration specimens. "
            "In accordance with Nirikshak metrological integrity constraints, when no physical ground-truth dataset "
            "is present in the repository, status is reported as BENCHMARK_BLOCKED without fabricating synthetic accuracy claims.*",
        ])

        return "\n".join(lines)


def _compute_statistical_aggregates(errors: List[float]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    Computes (MAE, Median AE, RMSE, P95 AE) deterministically.
    Returns (None, None, None, None) if errors list is empty.
    """
    if not errors:
        return None, None, None, None

    arr = np.array(errors, dtype=np.float64)
    mae = float(np.mean(arr))
    median_ae = float(np.median(arr))
    rmse = float(np.sqrt(np.mean(arr ** 2)))
    p95_ae = float(np.percentile(arr, 95))

    return (
        round(mae, 6),
        round(median_ae, 6),
        round(rmse, 6),
        round(p95_ae, 6),
    )


def evaluate_calibration(
    dataset: Optional[List[GroundTruthSample]],
    config: Optional[EvaluationConfig] = None,
) -> CalibrationEvaluationResult:
    """
    Evaluates the canonical Member 2 calibration pipeline against a ground-truth dataset.

    Pipeline Execution per Sample:
    1. Passes sample.image to detect_anchor(image, anchor_type, config).
    2. If anchor detected, invokes canonical compute_scale_factor(measured_px, sample.known_physical_reference_mm).
    3. Evaluates estimated scale S_est against sample.ground_truth_scale_mm_per_pixel (reference-only).
    4. If target feature box and ground-truth dimension are provided, measures feature height
       via measure_font_height / measure_cylindrical_feature and evaluates physical millimeter error.
    5. Aggregates metrics into CalibrationEvaluationResult.

    Empty / Missing Dataset Behavior:
    - Emits BENCHMARK_BLOCKED status with diagnostic explanation.
    - Never fabricates measurements or synthetic dataset benchmarks.
    """
    cfg = config if config is not None else EvaluationConfig()

    # 1. Dataset Pre-check: Detect absent or empty ground-truth dataset
    if dataset is None or len(dataset) == 0:
        return CalibrationEvaluationResult(
            status=BenchmarkStatus.BENCHMARK_BLOCKED,
            total_samples=0,
            successful_calibrations=0,
            failed_calibrations=0,
            calibration_success_rate=0.0,
            calibration_failure_rate=0.0,
            scale_evaluated_samples=0,
            dimension_evaluated_samples=0,
            message="No explicit physical ground-truth dataset available.",
        )

    sample_evals: List[SampleEvaluation] = []
    failure_counts: Dict[str, int] = {}
    surface_groups: Dict[str, List[SampleEvaluation]] = {}

    scale_abs_errors: List[float] = []
    scale_rel_errors: List[float] = []
    dimension_abs_errors: List[float] = []

    success_count = 0
    fail_count = 0

    for sample in dataset:
        surf = sample.surface_type or "PLANAR"
        if surf not in surface_groups:
            surface_groups[surf] = []

        # Validate basic sample properties
        if sample.image is None or not isinstance(sample.image, np.ndarray) or sample.image.size == 0:
            status_code = "INVALID_SAMPLE_IMAGE"
            failure_counts[status_code] = failure_counts.get(status_code, 0) + 1
            fail_count += 1
            eval_record = SampleEvaluation(
                sample_id=sample.sample_id,
                surface_type=surf,
                calibration_succeeded=False,
                status=status_code,
                message="Sample image is null, non-array, or empty.",
            )
            sample_evals.append(eval_record)
            surface_groups[surf].append(eval_record)
            continue

        if sample.known_physical_reference_mm <= 0.0 or not math.isfinite(sample.known_physical_reference_mm):
            status_code = "INVALID_PHYSICAL_REFERENCE"
            failure_counts[status_code] = failure_counts.get(status_code, 0) + 1
            fail_count += 1
            eval_record = SampleEvaluation(
                sample_id=sample.sample_id,
                surface_type=surf,
                calibration_succeeded=False,
                status=status_code,
                message=f"Known reference dimension is invalid: {sample.known_physical_reference_mm}.",
            )
            sample_evals.append(eval_record)
            surface_groups[surf].append(eval_record)
            continue

        # Canonical Step 1: Detect Anchor using production pipeline
        anchor_res: AnchorDetectionResult = detect_anchor(
            sample.image,
            anchor_type=cfg.anchor_type,
            config=cfg.anchor_config,
        )

        if not anchor_res.detected or anchor_res.geometry is None:
            status_code = anchor_res.status.value
            failure_counts[status_code] = failure_counts.get(status_code, 0) + 1
            fail_count += 1
            eval_record = SampleEvaluation(
                sample_id=sample.sample_id,
                surface_type=surf,
                calibration_succeeded=False,
                status=status_code,
                message=anchor_res.message,
            )
            sample_evals.append(eval_record)
            surface_groups[surf].append(eval_record)
            continue

        # Canonical Step 2: Scale estimation via production compute_scale_factor
        measured_px = 0.0
        marker_name = anchor_res.anchor_type.value if anchor_res.anchor_type else "ANCHOR"

        if isinstance(anchor_res.geometry, EllipseGeometry):
            measured_px = anchor_res.geometry.major_axis_px
        elif isinstance(anchor_res.geometry, CardGeometry):
            measured_px = anchor_res.geometry.width_px
        elif hasattr(anchor_res.geometry, "major_axis_px"):
            measured_px = getattr(anchor_res.geometry, "major_axis_px")
        elif hasattr(anchor_res.geometry, "width_px"):
            measured_px = getattr(anchor_res.geometry, "width_px")

        cal_outcome = compute_scale_factor(
            measured_marker_pixels=measured_px,
            known_marker_mm=sample.known_physical_reference_mm,
            marker_name=marker_name,
        )

        if cal_outcome.status != CalibrationStatus.CALIBRATED or cal_outcome.scale_factor_mm_per_pixel is None:
            status_code = cal_outcome.status.value
            failure_counts[status_code] = failure_counts.get(status_code, 0) + 1
            fail_count += 1
            eval_record = SampleEvaluation(
                sample_id=sample.sample_id,
                surface_type=surf,
                calibration_succeeded=False,
                status=status_code,
                message="Calibration outcome status is not CALIBRATED.",
            )
            sample_evals.append(eval_record)
            surface_groups[surf].append(eval_record)
            continue

        s_est = cal_outcome.scale_factor_mm_per_pixel
        success_count += 1

        # Evaluate Scale Error against reference-only ground truth
        scale_abs_err = None
        scale_rel_err = None
        if sample.ground_truth_scale_mm_per_pixel is not None and sample.ground_truth_scale_mm_per_pixel > 0.0:
            s_gt = sample.ground_truth_scale_mm_per_pixel
            scale_abs_err = abs(s_est - s_gt)
            scale_rel_err = scale_abs_err / s_gt
            scale_abs_errors.append(scale_abs_err)
            scale_rel_errors.append(scale_rel_err)

        # Evaluate Feature Measurement Error if requested
        feat_measured_mm = None
        feat_abs_err = None
        if sample.target_feature_box is not None and sample.ground_truth_feature_dimension_mm is not None:
            # Measure feature using calibrated scale
            if surf.upper() == "CYLINDRICAL" and sample.metadata and "cylinder_center_x" in sample.metadata:
                cyl_res = measure_cylindrical_feature(
                    feature_box=sample.target_feature_box,
                    geometry_state=CylinderGeometryState.CYLINDRICAL,
                    cylinder_center_x=sample.metadata["cylinder_center_x"],
                    cylinder_radius_px=sample.metadata["cylinder_radius_px"],
                    calibration=cal_outcome,
                    is_axis_aligned=sample.metadata.get("is_axis_aligned", True),
                )
                feat_measured_mm = cyl_res.measured_axial_mm
            else:
                font_res = measure_font_height(
                    bounding_box=sample.target_feature_box,
                    calibration=cal_outcome,
                    image=sample.image,
                    measurement_type=FontMeasurementType.BOUNDING_BOX_HEIGHT,
                )
                feat_measured_mm = font_res.measured_mm

            if feat_measured_mm is not None:
                feat_abs_err = abs(feat_measured_mm - sample.ground_truth_feature_dimension_mm)
                dimension_abs_errors.append(feat_abs_err)

        eval_record = SampleEvaluation(
            sample_id=sample.sample_id,
            surface_type=surf,
            calibration_succeeded=True,
            status="SUCCESS",
            estimated_scale_mm_per_pixel=round(s_est, 6),
            ground_truth_scale_mm_per_pixel=sample.ground_truth_scale_mm_per_pixel,
            scale_absolute_error_mm_per_pixel=round(scale_abs_err, 6) if scale_abs_err is not None else None,
            scale_relative_error=round(scale_rel_err, 6) if scale_rel_err is not None else None,
            measured_feature_mm=feat_measured_mm,
            ground_truth_feature_mm=sample.ground_truth_feature_dimension_mm,
            feature_dimension_absolute_error_mm=round(feat_abs_err, 4) if feat_abs_err is not None else None,
            message="Calibration succeeded.",
        )
        sample_evals.append(eval_record)
        surface_groups[surf].append(eval_record)

    total_count = len(dataset)
    success_rate = success_count / total_count if total_count > 0 else 0.0
    failure_rate = fail_count / total_count if total_count > 0 else 0.0

    # Scale aggregates
    s_mae, s_med, s_rmse, s_p95 = _compute_statistical_aggregates(scale_abs_errors)
    rel_mean = round(float(np.mean(scale_rel_errors)), 6) if scale_rel_errors else None
    rel_med = round(float(np.median(scale_rel_errors)), 6) if scale_rel_errors else None

    # Dimension aggregates
    d_mae, d_med, d_rmse, d_p95 = _compute_statistical_aggregates(dimension_abs_errors)

    # Verdicts
    s_passed = (rel_mean <= cfg.target_relative_scale_error) if rel_mean is not None else None
    d_passed = (d_mae <= cfg.target_dimension_mae_mm) if d_mae is not None else None
    rate_passed = (success_rate >= cfg.min_success_rate)

    # Stratification by surface
    stratified: Dict[str, Dict[str, Any]] = {}
    for surf, group in surface_groups.items():
        g_total = len(group)
        g_succ = sum(1 for g in group if g.calibration_succeeded)
        g_scale_errs = [g.scale_absolute_error_mm_per_pixel for g in group if g.scale_absolute_error_mm_per_pixel is not None]
        g_dim_errs = [g.feature_dimension_absolute_error_mm for g in group if g.feature_dimension_absolute_error_mm is not None]

        stratified[surf] = {
            "total": g_total,
            "succeeded": g_succ,
            "success_rate": round(g_succ / g_total, 4) if g_total > 0 else 0.0,
            "scale_mae": round(float(np.mean(g_scale_errs)), 6) if g_scale_errs else None,
            "dimension_mae": round(float(np.mean(g_dim_errs)), 4) if g_dim_errs else None,
        }

    return CalibrationEvaluationResult(
        status=BenchmarkStatus.OK,
        total_samples=total_count,
        successful_calibrations=success_count,
        failed_calibrations=fail_count,
        calibration_success_rate=round(success_rate, 4),
        calibration_failure_rate=round(failure_rate, 4),
        scale_evaluated_samples=len(scale_abs_errors),
        dimension_evaluated_samples=len(dimension_abs_errors),
        scale_mae_mm_per_pixel=s_mae,
        scale_median_ae_mm_per_pixel=s_med,
        scale_rmse_mm_per_pixel=s_rmse,
        scale_p95_ae_mm_per_pixel=s_p95,
        scale_relative_error_mean=rel_mean,
        scale_relative_error_median=rel_med,
        dimension_mae_mm=d_mae,
        dimension_median_ae_mm=d_med,
        dimension_rmse_mm=d_rmse,
        dimension_p95_ae_mm=d_p95,
        scale_target_passed=s_passed,
        dimension_target_passed=d_passed,
        success_rate_passed=rate_passed,
        stratified_by_surface=stratified,
        failure_breakdown=failure_counts,
        sample_evaluations=sample_evals,
        message=f"Evaluated {total_count} ground-truth samples.",
    )
