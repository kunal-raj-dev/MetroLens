"""
MetroLens AI™ / Nirikshak AI — Automated Benchmark Invariants & Release Gate Tests.
SIH 2026 Problem Statement 26034 — Member 6 Release Gate.

Enforces:
1. Benchmark summary schema validity.
2. Anti-hallucination / Anti-fabrication invariants (missing physical data -> BENCHMARK_BLOCKED).
3. Metric denominator accounting (no metric laundering).
4. Strict separation of synthetic test specimens from physical packaging.
5. Latency budget conformance (< 2500ms on CPU).
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SUMMARY_JSON_PATH = REPO_ROOT / "benchmarks" / "results" / "summary.json"


@pytest.fixture(scope="module")
def benchmark_data():
    """Loads the locked benchmark summary JSON."""
    if not SUMMARY_JSON_PATH.exists():
        # If not yet generated, invoke generator to ensure availability
        from scripts.benchmark.run_benchmark_suite import execute_master_benchmark
        return execute_master_benchmark()

    with open(SUMMARY_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestBenchmarkSchemaAndFidelity:
    """Validates structural schema and field definitions of the benchmark report."""

    def test_required_top_level_fields(self, benchmark_data):
        required_fields = [
            "benchmark_version",
            "generated_at",
            "git_commit",
            "environment",
            "dataset",
            "metrics",
            "per_sample",
        ]
        for field in required_fields:
            assert field in benchmark_data, f"Missing top-level benchmark field: {field}"

    def test_environment_metadata_completeness(self, benchmark_data):
        env = benchmark_data.get("environment", {})
        assert "python" in env and env["python"], "Python version missing in environment"
        assert "os" in env and env["os"], "OS info missing in environment"
        assert "hardware" in env, "Hardware metadata missing in environment"
        assert env["hardware"].get("cpu_count", 0) > 0, "CPU count must be positive"


class TestAntiHallucinationAndPhysicalDatasetGate:
    """Enforces non-negotiable physical metrology invariants."""

    def test_physical_dataset_status_is_blocked(self, benchmark_data):
        dataset_info = benchmark_data.get("dataset", {})
        # Invariant: 35 physical retail SKUs do not exist on disk in data/raw/
        raw_images = list((REPO_ROOT / "data" / "raw").glob("*.jpg")) + list((REPO_ROOT / "data" / "raw").glob("*.png"))
        if len(raw_images) == 0:
            assert dataset_info.get("status") == "BENCHMARK_BLOCKED", (
                "Anti-Hallucination Failure: Physical dataset is absent from disk, "
                "so dataset.status must be BENCHMARK_BLOCKED."
            )
            assert dataset_info.get("physical_skus_present") == 0

    def test_zero_scale_fabrication_on_uncalibrated_data(self, benchmark_data):
        scale_metric = benchmark_data.get("metrics", {}).get("optical_scale_factor", {})
        # When physical ground truth is absent, status must be BENCHMARK_BLOCKED and metric null
        assert scale_metric.get("status") == "BENCHMARK_BLOCKED"
        assert scale_metric.get("mean_relative_error") is None, (
            "Anti-Fabrication Invariant: mean_relative_error must not be populated without physical ground truth."
        )

    def test_font_height_mae_not_fabricated(self, benchmark_data):
        font_metric = benchmark_data.get("metrics", {}).get("font_height_metrology", {})
        assert font_metric.get("status") == "BENCHMARK_BLOCKED"
        assert font_metric.get("font_mae_mm") is None, (
            "Anti-Fabrication Invariant: font_mae_mm must remain null when physical caliper readings are missing."
        )

    def test_statutory_compliance_accuracy_not_fabricated(self, benchmark_data):
        comp_metric = benchmark_data.get("metrics", {}).get("statutory_compliance_accuracy", {})
        assert comp_metric.get("status") == "BENCHMARK_BLOCKED"
        assert comp_metric.get("accuracy") is None


class TestDenominatorIntegrity:
    """Guarantees denominator transparency and prevents metric laundering."""

    def test_explicit_denominators_reported(self, benchmark_data):
        scale_metric = benchmark_data.get("metrics", {}).get("optical_scale_factor", {})
        assert "eligible_count" in scale_metric
        assert "evaluated_count" in scale_metric
        assert "excluded_count" in scale_metric

        # Zero evaluated samples must not produce a zero error rate
        if scale_metric["evaluated_count"] == 0:
            assert scale_metric["mean_relative_error"] is None

    def test_synthetic_per_sample_integrity(self, benchmark_data):
        per_sample = benchmark_data.get("per_sample", [])
        assert len(per_sample) > 0, "Benchmark must record per-sample synthetic evaluations."

        for s in per_sample:
            assert s["sample_type"] == "SYNTHETIC_TEST_SPECIMEN", (
                f"Sample {s['sample_id']} must be labeled SYNTHETIC_TEST_SPECIMEN."
            )
            assert s["scale_status"] == "NULL", "Synthetic samples without calibration anchor must have scale NULL."
            assert s["predicted_font_height_mm"] is None, "Synthetic samples without physical scale must have null font height mm."


class TestLatencyBudgets:
    """Verifies latency targets are rigorously measured and pass budget."""

    def test_pipeline_latency_budget(self, benchmark_data):
        latency = benchmark_data.get("metrics", {}).get("system_latency", {})
        assert latency.get("target_budget_ms") == 2500.0
        mean_ms = latency.get("mean_pipeline_latency_ms")
        assert mean_ms is not None
        assert mean_ms < 2500.0, f"Pipeline mean latency ({mean_ms} ms) exceeded 2.5s budget!"

    def test_pdf_dossier_latency_budget(self, benchmark_data):
        latency = benchmark_data.get("metrics", {}).get("system_latency", {})
        pdf_ms = latency.get("pdf_generation_mean_ms")
        assert pdf_ms is not None
        assert pdf_ms < 500.0, f"PDF compilation ({pdf_ms} ms) exceeded 500ms budget!"
