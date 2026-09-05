"""
MetroLens AI™ API Latency & Throughput Benchmark Suite.
Audits:
1. Synchronous Pipeline Latency Budget (< 2.5s on CPU).
2. ReportLab PDF Generation Latency Budget (< 500ms on CPU).
3. P50, P90, P95, and P99 percentiles across 20 iterations.
4. Granular per-stage breakdown:
   - Stage 1: Quality Gate (< 30ms)
   - Stage 2: Metric Scale Calibration (< 100ms)
   - Stage 3: OCR Perception (< 1200ms)
   - Stage 4: Token Normalization (< 50ms)
   - Stage 5: Master Statutory Rules Engine (< 20ms)
   - Stage 6: Visual Evidence Packaging (< 500ms)
"""

import io
import json
import logging
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

# Ensure repository root and packages are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

for pkg_dir in (REPO_ROOT / "packages").glob("*/src"):
    if str(pkg_dir) not in sys.path:
        sys.path.insert(0, str(pkg_dir))

import numpy as np
from PIL import Image, ImageDraw

from apps.api.services.pipeline_orchestrator import pipeline_orchestrator
from nirikshak_reporting.pdf_compiler import pdf_compiler
from nirikshak_rules_engine.schemas import (
    ComplianceEvaluationResult,
    ComplianceState,
    VerdictBadgeColor,
    RuleEvaluationRecord,
    CanonicalDeclaration,
    MetricScaleResult,
    UnitType,
)

logging.basicConfig(level=logging.WARNING)


def generate_benchmark_specimen(width: int = 1200, height: int = 1600) -> bytes:
    """Generates realistic high-resolution packaging specimen."""
    img = Image.new("RGB", (width, height), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)

    draw.rectangle([40, 40, width - 40, height - 40], outline=(40, 60, 100), width=4)
    draw.text((80, 80), "METROLENS PREMIUM CASHEWS", fill=(10, 20, 50))
    draw.text((80, 140), "Net Quantity: 200 g", fill=(20, 20, 20))
    draw.text((80, 200), "MRP Rs. 240.00 (inclusive of all taxes)", fill=(20, 20, 20))
    draw.text((80, 260), "Unit Sale Price: Rs. 1.20 / g", fill=(20, 20, 20))
    draw.text((80, 320), "Mfg Date: 08/2026", fill=(20, 20, 20))
    draw.text((80, 380), "Manufactured By: MetroLens Foods Pvt Ltd, New Delhi 110020", fill=(20, 20, 20))
    draw.text((80, 440), "Consumer Care: 1800-11-4000, care@metrolens.in", fill=(20, 20, 20))
    draw.text((80, 500), "Country of Origin: India", fill=(20, 20, 20))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def run_pipeline_benchmark(iterations: int = 20) -> Dict[str, Any]:
    """Runs repeated end-to-end inspection pipeline iterations and collects percentiles."""
    print(f"\n[1/2] Benchmarking Synchronous Inspection Pipeline ({iterations} iterations)...")
    specimen = generate_benchmark_specimen()

    # Warmup
    _ = pipeline_orchestrator.orchestrate_inspection(
        image_bytes=specimen,
        filename="warmup.jpg",
    )

    latencies_ms: List[float] = []
    stages_breakdown: Dict[str, List[float]] = {
        "quality_gate": [],
        "metric_calibration": [],
        "ocr_perception": [],
        "normalization": [],
        "rule_engine": [],
        "evidence_packaging": [],
    }

    for i in range(iterations):
        t0 = time.perf_counter()
        resp = pipeline_orchestrator.orchestrate_inspection(
            image_bytes=specimen,
            filename=f"benchmark_{i}.jpg",
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(elapsed_ms)

        stages = resp.telemetry.stages_ms
        stages_breakdown["quality_gate"].append(stages.quality_gate)
        stages_breakdown["metric_calibration"].append(stages.metric_calibration)
        stages_breakdown["ocr_perception"].append(stages.ocr_perception)
        stages_breakdown["normalization"].append(stages.normalization)
        stages_breakdown["rule_engine"].append(stages.rule_engine)
        stages_breakdown["evidence_packaging"].append(stages.evidence_packaging)

    p50 = float(np.percentile(latencies_ms, 50))
    p90 = float(np.percentile(latencies_ms, 90))
    p95 = float(np.percentile(latencies_ms, 95))
    p99 = float(np.percentile(latencies_ms, 99))
    mean_lat = statistics.mean(latencies_ms)

    return {
        "iterations": iterations,
        "mean_ms": round(mean_lat, 2),
        "min_ms": round(min(latencies_ms), 2),
        "max_ms": round(max(latencies_ms), 2),
        "p50_ms": round(p50, 2),
        "p90_ms": round(p90, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "budget_limit_ms": 2500.0,
        "budget_passed": p95 < 2500.0,
        "stages_mean_ms": {k: round(statistics.mean(v), 2) for k, v in stages_breakdown.items()},
    }


def run_pdf_benchmark(iterations: int = 20) -> Dict[str, Any]:
    """Runs repeated PDF generation iterations and collects percentiles."""
    print(f"\n[2/2] Benchmarking Evidentiary PDF Report Compilation ({iterations} iterations)...")

    decl = CanonicalDeclaration(
        commodity_name="Fortified Wheat Flour",
        mrp_inr=210.0,
        tax_qualifier_present=True,
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.KILOGRAM,
        declared_usp_value=42.0,
        declared_usp_unit="kg",
        mfg_month=8,
        mfg_year=2026,
        manufacturer_name="Hindustan Grains Ltd",
        manufacturer_address="Phase 2, Udyog Vihar, Gurugram, Haryana",
        consumer_care_email="care@hindustangrains.com",
        consumer_care_phone="1800-111-9999",
        country_of_origin="India",
    )

    scale = MetricScaleResult(
        is_calibrated=True,
        scale_factor_mm_per_px=0.0825,
        pdp_area_sqcm=245.0,
        anchor_type_detected="coin_10rs",
        tilt_angle_deg=4.2,
        is_cylindrical=False,
    )

    evals = [
        RuleEvaluationRecord(
            rule_id="LMPC-R06-MFR-001",
            rule_title="Manufacturer Name & Address",
            statutory_reference="Rule 6(1)(a)",
            status="PASS",
            is_compliant=True,
            observed_value="Hindustan Grains Ltd, Gurugram",
            required_value="Complete manufacturer/packer name & address",
            statutory_citation="Rule 6(1)(a) of LM(PC) Rules, 2011",
        ),
        RuleEvaluationRecord(
            rule_id="LMPC-R06-MRP-001",
            rule_title="Retail Sale Price (MRP)",
            statutory_reference="Rule 6(1)(e)",
            status="PASS",
            is_compliant=True,
            observed_value="Rs. 210.00 (inclusive of all taxes)",
            required_value="MRP inclusive of all taxes",
            statutory_citation="Rule 6(1)(e) of LM(PC) Rules, 2011",
        ),
        RuleEvaluationRecord(
            rule_id="LMPC-R06-USP-001",
            rule_title="Unit Sale Price (USP)",
            statutory_reference="Rule 6(11)",
            status="PASS",
            is_compliant=True,
            observed_value="Rs. 42.00 / kg",
            required_value="Rs. 42.00 / kg (standard denominator)",
            statutory_citation="Rule 6(11) of LM(PC) Rules, 2011",
        ),
    ]

    comp_res = ComplianceEvaluationResult(
        inspection_id="INSP-BENCHMARK-001",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        overall_verdict=ComplianceState.COMPLIANT,
        verdict_badge_color=VerdictBadgeColor.GREEN,
        primary_legal_summary="Packaging satisfies all mandatory requirements.",
        rule_evaluations=evals,
        declarations=decl,
        calibrated_measurements=scale,
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )

    # Warmup
    _ = pdf_compiler.compile_report_pdf(comp_res)

    latencies_ms: List[float] = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _ = pdf_compiler.compile_report_pdf(comp_res)
        latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    p50 = float(np.percentile(latencies_ms, 50))
    p90 = float(np.percentile(latencies_ms, 90))
    p95 = float(np.percentile(latencies_ms, 95))
    p99 = float(np.percentile(latencies_ms, 99))
    mean_lat = statistics.mean(latencies_ms)

    return {
        "iterations": iterations,
        "mean_ms": round(mean_lat, 2),
        "min_ms": round(min(latencies_ms), 2),
        "max_ms": round(max(latencies_ms), 2),
        "p50_ms": round(p50, 2),
        "p90_ms": round(p90, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "budget_limit_ms": 500.0,
        "budget_passed": p95 < 500.0,
    }


def main():
    print("=" * 78)
    print(" MetroLens AI™ Gateway: Comprehensive Latency Benchmark Suite")
    print("=" * 78)

    pipeline_metrics = run_pipeline_benchmark(iterations=20)
    pdf_metrics = run_pdf_benchmark(iterations=20)

    print("\n" + "=" * 78)
    print(" BENCHMARK RESULTS SUMMARY")
    print("=" * 78)
    print(f"1. End-to-End Pipeline Latency (Target < 2500ms):")
    print(f"   Mean: {pipeline_metrics['mean_ms']}ms | P50: {pipeline_metrics['p50_ms']}ms | P95: {pipeline_metrics['p95_ms']}ms | P99: {pipeline_metrics['p99_ms']}ms")
    print(f"   Status: {'PASSED (Within Budget)' if pipeline_metrics['budget_passed'] else 'FAILED'}")
    print(f"   Per-Stage Breakdown (Mean ms):")
    for stg, dur in pipeline_metrics["stages_mean_ms"].items():
        print(f"     - {stg:<22}: {dur:>6.2f} ms")

    print(f"\n2. ReportLab PDF Generation (Target < 500ms):")
    print(f"   Mean: {pdf_metrics['mean_ms']}ms | P50: {pdf_metrics['p50_ms']}ms | P95: {pdf_metrics['p95_ms']}ms | P99: {pdf_metrics['p99_ms']}ms")
    print(f"   Status: {'PASSED (Within Budget)' if pdf_metrics['budget_passed'] else 'FAILED'}")
    print("=" * 78)

    # Save artifact
    out_dir = Path("benchmarks/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / "latency_benchmark_report.json"
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline": pipeline_metrics,
        "pdf_reporting": pdf_metrics,
    }
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved benchmark metrics artifact to: {report_file}")


if __name__ == "__main__":
    main()
