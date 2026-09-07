"""
Prometheus Metrics Route
========================
Exposes operational telemetry at GET /metrics for scraping by Prometheus,
Grafana Agent, or Datadog.
"""

from fastapi import APIRouter, Response
from apps.api.telemetry.prometheus import metrics

router = APIRouter(tags=["Telemetry & Metrics"])


@router.get(
    "/metrics",
    summary="Prometheus Text Exposition Endpoint",
    description="Returns application-wide inspection counters, latency histograms, and resource gauges.",
    response_class=Response,
)
def prometheus_metrics() -> Response:
    content = metrics.render_prometheus_text()
    return Response(
        content=content,
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
