"""
Audit & Telemetry Logging Middleware
====================================
ASGI middleware intercepting incoming requests to inject W3C trace contexts,
measure sub-millisecond route latencies, and record Prometheus metric counters.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from apps.api.telemetry.prometheus import metrics
from apps.api.telemetry.tracing import SpanContext, tracer


class AuditTelemetryMiddleware(BaseHTTPMiddleware):
    """
    Measures endpoint latency, records telemetry, and injects distributed trace headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Extract or generate Request ID
        req_id = request.headers.get("x-request-id") or f"REQ-{uuid.uuid4().hex[:12].upper()}"

        # Extract or generate W3C traceparent
        traceparent = request.headers.get("traceparent")
        if traceparent:
            span_ctx = SpanContext.from_traceparent(traceparent) or SpanContext.generate()
        else:
            span_ctx = SpanContext.generate()

        # Process request within a traced span
        with tracer.start_span(f"http_{request.method}_{request.url.path}", parent_context=span_ctx) as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.path", request.url.path)
            span.set_attribute("http.client_ip", request.client.host if request.client else "unknown")

            try:
                response = await call_next(request)
            except Exception as exc:
                span.set_attribute("error.message", str(exc))
                raise exc

            duration_s = time.time() - start_time
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("http.duration_ms", round(duration_s * 1000.0, 3))

            # Record metrics
            if "/inspect" in request.url.path:
                metrics.inspection_latency_seconds.observe(duration_s, stage="pipeline_total")

            # Attach response headers
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Trace-ID"] = span_ctx.trace_id
            response.headers["traceparent"] = span_ctx.to_traceparent()
            response.headers["X-Response-Time-MS"] = str(round(duration_s * 1000.0, 2))

            return response
