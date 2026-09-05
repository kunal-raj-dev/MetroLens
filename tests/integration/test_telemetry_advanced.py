"""
Integration Tests for Telemetry, Prometheus Exposition & W3C Tracing
=====================================================================
Verifies Prometheus plain-text exposition format, multi-dimensional metrics,
histogram bucket distributions, and W3C traceparent context propagation.
"""

import time
import pytest

from apps.api.telemetry.prometheus import PrometheusMetricsRegistry
from apps.api.telemetry.tracing import SpanContext, Tracer, TraceSpan


# ---------------------------------------------------------------------------
# 1. Prometheus Metrics Tests
# ---------------------------------------------------------------------------

def test_prometheus_metrics_registry_render():
    """Verify Prometheus exposition text structure and metric accumulation."""
    reg = PrometheusMetricsRegistry()

    # Counter with labels
    reg.inspections_total.inc(1, verdict="COMPLIANT", category="FMCG")
    reg.inspections_total.inc(2, verdict="NON_COMPLIANT", category="Cosmetics")

    # Rule violations
    reg.rule_violations_total.inc(1, rule_id="Rule_6_1_e", severity="HIGH")

    # Latency histogram
    reg.inspection_latency_seconds.observe(0.045, stage="ocr")
    reg.inspection_latency_seconds.observe(0.120, stage="ocr")

    # Gauges
    reg.active_workers_gauge.set(4)
    reg.spool_disk_usage_bytes.set(1048576)

    rendered = reg.render_prometheus_text()

    assert "# HELP metrolens_inspections_total" in rendered
    assert '# TYPE metrolens_inspections_total counter' in rendered
    assert 'metrolens_inspections_total{category="FMCG",verdict="COMPLIANT"} 1.0' in rendered
    assert 'metrolens_inspections_total{category="Cosmetics",verdict="NON_COMPLIANT"} 2.0' in rendered
    assert 'metrolens_active_workers 4' in rendered
    assert 'metrolens_spool_disk_usage_bytes 1048576' in rendered
    assert 'metrolens_inspection_duration_seconds_bucket' in rendered


# ---------------------------------------------------------------------------
# 2. W3C Tracing Tests
# ---------------------------------------------------------------------------

def test_w3c_traceparent_serialization_and_parsing():
    """Verify traceparent header creation and roundtrip decoding."""
    ctx = SpanContext(trace_id="4bf92f3577b34da6a3ce929d0e0e4736", span_id="00f067aa0ba902b7")
    tp_str = ctx.to_traceparent()
    assert tp_str == "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"

    parsed = SpanContext.from_traceparent(tp_str)
    assert parsed is not None
    assert parsed.trace_id == ctx.trace_id
    assert parsed.span_id == ctx.span_id


def test_tracer_span_context_manager_and_timing():
    """Verify tracer span lifecycle and error recording."""
    tracer = Tracer(service_name="test-service")

    with tracer.start_span("quality_gate") as span:
        span.set_attribute("resolution.width", 1920)
        span.set_attribute("resolution.height", 1080)
        time.sleep(0.01)

    assert span.status == "OK"
    assert span.duration_ms >= 8.0
    assert span.attributes["resolution.width"] == 1920

    # Test error handling inside span
    try:
        with tracer.start_span("failing_stage") as error_span:
            raise ValueError("Corrupted pixel buffer")
    except ValueError:
        pass

    assert error_span.status == "ERROR"
    assert error_span.attributes["error.type"] == "ValueError"
    assert "Corrupted pixel buffer" in error_span.attributes["error.message"]
