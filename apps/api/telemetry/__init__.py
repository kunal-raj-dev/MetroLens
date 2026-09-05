"""
MetroLens AI - Observability, Metrics & Tracing Package
======================================================
Provides Prometheus metrics exposition (/metrics) and OpenTelemetry W3C
trace context propagation across asynchronous and synchronous inspection stages.
"""

from .prometheus import PrometheusMetricsRegistry, metrics
from .tracing import TraceSpan, Tracer, tracer

__all__ = [
    "PrometheusMetricsRegistry",
    "metrics",
    "TraceSpan",
    "Tracer",
    "tracer",
]
