"""
Nirikshak Metric Calibration Evaluation CLI Runner.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Usage:
    python scripts/benchmark/run_calibration_evaluation.py [OPTIONS]

Outputs:
    benchmarks/results/calibration_evaluation_results.json
    benchmarks/reports/calibration_evaluation_report.md
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List
import cv2

# Ensure workspace packages are importable
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root / "packages" / "calibration" / "src"))
sys.path.insert(0, str(repo_root / "packages" / "vision" / "src"))
sys.path.insert(0, str(repo_root / "packages" / "shared" / "src"))

from nirikshak_calibration import (
    BenchmarkStatus,
    GroundTruthSample,
    EvaluationConfig,
    CalibrationEvaluationResult,
    evaluate_calibration,
    AnchorType,
)


def load_dataset_from_directory(dataset_dir: Path) -> Optional[List[GroundTruthSample]]:
    """
    Attempts to load ground-truth packaging samples from specified directory.
    Expects manifest.json or metadata.json containing sample annotations.
    """
    if not dataset_dir.exists() or not dataset_dir.is_dir():
        return None

    manifest_file = dataset_dir / "manifest.json"
    if not manifest_file.exists():
        manifest_file = dataset_dir / "metadata.json"
    if not manifest_file.exists():
        return None

    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as exc:
        print(f"Warning: Failed to parse dataset manifest at {manifest_file}: {exc}")
        return None

    samples: List[GroundTruthSample] = []
    for entry in manifest.get("samples", []):
        img_rel_path = entry.get("image_path")
        if not img_rel_path:
            continue
        img_full_path = dataset_dir / img_rel_path
        if not img_full_path.exists():
            continue

        img = cv2.imread(str(img_full_path))
        if img is None:
            continue

        known_ref = float(entry.get("known_physical_reference_mm", 27.0))
        surf = entry.get("surface_type", "PLANAR")
        gt_scale = entry.get("ground_truth_scale_mm_per_pixel")
        if gt_scale is not None:
            gt_scale = float(gt_scale)

        box = entry.get("target_feature_box")
        if box is not None and len(box) == 4:
            box = (float(box[0]), float(box[1]), float(box[2]), float(box[3]))
        else:
            box = None

        gt_dim = entry.get("ground_truth_feature_dimension_mm")
        if gt_dim is not None:
            gt_dim = float(gt_dim)

        samples.append(
            GroundTruthSample(
                sample_id=entry.get("sample_id", img_full_path.stem),
                image=img,
                known_physical_reference_mm=known_ref,
                surface_type=surf,
                ground_truth_scale_mm_per_pixel=gt_scale,
                target_feature_box=box,
                ground_truth_feature_dimension_mm=gt_dim,
                metadata=entry.get("metadata"),
            )
        )

    return samples if len(samples) > 0 else None


def main():
    parser = argparse.ArgumentParser(
        description="Run Nirikshak calibration evaluation pipeline against physical ground-truth dataset."
    )
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default=str(repo_root / "data" / "calibration_ground_truth"),
        help="Path to dataset directory containing ground-truth images and manifest.json",
    )
    parser.add_argument(
        "--results-path",
        type=str,
        default=str(repo_root / "benchmarks" / "results" / "calibration_evaluation_results.json"),
        help="Path to write structured JSON evaluation metrics",
    )
    parser.add_argument(
        "--report-path",
        type=str,
        default=str(repo_root / "benchmarks" / "reports" / "calibration_evaluation_report.md"),
        help="Path to write Markdown summary report",
    )
    parser.add_argument(
        "--target-scale-err",
        type=float,
        default=0.05,
        help="Target maximum relative scale error (default: 0.05 = 5%%)",
    )
    parser.add_argument(
        "--target-dim-mae",
        type=float,
        default=0.15,
        help="Target maximum physical dimension MAE in mm (default: 0.15mm)",
    )
    parser.add_argument(
        "--anchor-type",
        type=str,
        default="AUTO",
        choices=["AUTO", "COIN_INR_10", "ID1_CARD"],
        help="Forced anchor detection mode (default: AUTO)",
    )

    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir)
    results_path = Path(args.results_path)
    report_path = Path(args.report_path)

    print(f"Checking dataset at: {dataset_dir}")
    dataset = load_dataset_from_directory(dataset_dir)

    anchor_mode = None
    if args.anchor_type == "COIN_INR_10":
        anchor_mode = AnchorType.COIN_INR_10
    elif args.anchor_type == "ID1_CARD":
        anchor_mode = AnchorType.ID1_CARD

    config = EvaluationConfig(
        target_relative_scale_error=args.target_scale_err,
        target_dimension_mae_mm=args.target_dim_mae,
        anchor_type=anchor_mode,
    )

    print("Running evaluate_calibration()...")
    result: CalibrationEvaluationResult = evaluate_calibration(dataset, config=config)

    print(f"\n========================================================")
    print(f"Evaluation Complete. Status: {result.status.value}")
    print(f"Total Samples: {result.total_samples}")
    print(f"Message: {result.message}")
    print(f"========================================================\n")

    # Ensure parent directories exist
    results_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON results
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)
    print(f"Saved evaluation JSON to: {results_path}")

    # Write Markdown report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(result.to_markdown_report())
    print(f"Saved evaluation report to: {report_path}")


if __name__ == "__main__":
    main()
