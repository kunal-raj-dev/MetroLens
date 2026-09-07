"""
Performance Benchmark & Latency Telemetry Suite for Nirikshak Rules Engine.
Verifies that end-to-end statutory rule evaluation executes strictly in < 20ms on CPU
with zero generative LLM calls (ADR-001).
"""

import time
import statistics
import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    CanonicalDeclaration,
    MetricScaleResult,
    UnitType,
    ComplianceState,
)


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


def test_statutory_evaluation_latency_under_20ms(engine):
    """
    Measures CPU execution latency across 100 consecutive statutory evaluation cycles.
    Strict statutory budget: Sub-20ms latency per evaluation on CPU.
    """
    decl = CanonicalDeclaration(
        commodity_name="Premium Roasted Cashews",
        manufacturer_name="MetroLens Foods Pvt Ltd, Okhla Phase-III, New Delhi 110020",
        manufacturer_pincode="110020",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=240.0,
        tax_qualifier_present=True,
        consumer_care_email="care@metrolens.in",
        consumer_care_phone="1800-11-4000",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)

    # Warmup
    for _ in range(5):
        engine.evaluate(decl, scale=scale, measured_font_height_mm=1.65)

    latencies_ms = []
    iterations = 100

    for i in range(iterations):
        t0 = time.perf_counter()
        res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.65, inspection_id=f"BENCH-{i}")
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0
        latencies_ms.append(elapsed_ms)
        assert res.overall_verdict == ComplianceState.COMPLIANT

    avg_latency = statistics.mean(latencies_ms)
    p95_latency = statistics.quantiles(latencies_ms, n=20)[18]  # 95th percentile
    max_latency = max(latencies_ms)

    print(
        f"\n[RULES ENGINE LATENCY BENCHMARK] "
        f"Mean: {avg_latency:.3f}ms | P95: {p95_latency:.3f}ms | Max: {max_latency:.3f}ms | Budget: < 20.0ms"
    )

    # Assertions
    assert avg_latency < 5.0, f"Average latency {avg_latency:.3f}ms exceeded 5.0ms target"
    assert p95_latency < 15.0, f"P95 latency {p95_latency:.3f}ms exceeded 15.0ms target"
    assert max_latency < 20.0, f"Max latency {max_latency:.3f}ms exceeded 20.0ms budget"
