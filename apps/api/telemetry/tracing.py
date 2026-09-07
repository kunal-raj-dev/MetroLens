"""
W3C Distributed Tracing & Span Context Engine
=============================================
Provides W3C Trace Context compliant distributed tracing instrumentation
(traceparent / tracestate) across asynchronous background tasks and pipeline stages.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class SpanContext:
    """W3C compliant trace identification context."""

    trace_id: str  # 32 hex chars
    span_id: str   # 16 hex chars
    trace_flags: str = "01"  # Sampled

    @classmethod
    def generate(cls) -> SpanContext:
        return cls(
            trace_id=os.urandom(16).hex(),
            span_id=os.urandom(8).hex(),
            trace_flags="01",
        )

    def to_traceparent(self) -> str:
        """Format as W3C traceparent header: 00-{trace_id}-{span_id}-{flags}"""
        return f"00-{self.trace_id}-{self.span_id}-{self.trace_flags}"

    @classmethod
    def from_traceparent(cls, header_val: str) -> Optional[SpanContext]:
        """Parse incoming W3C traceparent header."""
        parts = header_val.strip().split("-")
        if len(parts) == 4 and parts[0] == "00":
            return cls(trace_id=parts[1], span_id=parts[2], trace_flags=parts[3])
        return None


@dataclass
class TraceSpan:
    """Represents a discrete timed execution segment within the inspection pipeline."""

    name: str
    context: SpanContext
    parent_span_id: Optional[str] = None
    start_time_epoch_ns: int = field(default_factory=time.time_ns)
    end_time_epoch_ns: Optional[int] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "OK"  # 'OK' | 'ERROR'

    @property
    def duration_ms(self) -> float:
        if self.end_time_epoch_ns is None:
            return (time.time_ns() - self.start_time_epoch_ns) / 1_000_000.0
        return (self.end_time_epoch_ns - self.start_time_epoch_ns) / 1_000_000.0

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        self.events.append(
            {
                "name": name,
                "timestamp_ns": time.time_ns(),
                "attributes": attributes or {},
            }
        )

    def end(self, status: str = "OK") -> None:
        self.end_time_epoch_ns = time.time_ns()
        self.status = status

    def __enter__(self) -> TraceSpan:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.set_attribute("error.type", exc_type.__name__)
            self.set_attribute("error.message", str(exc_val))
            self.end(status="ERROR")
        else:
            self.end(status="OK")


class Tracer:
    """Manages creation and lifecycle of active spans."""

    def __init__(self, service_name: str = "metrolens-api") -> None:
        self.service_name = service_name
        self._completed_spans: List[TraceSpan] = []

    def start_span(
        self,
        name: str,
        parent_context: Optional[SpanContext] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> TraceSpan:
        """Begin a new timed trace span."""
        if parent_context:
            ctx = SpanContext(
                trace_id=parent_context.trace_id,
                span_id=os.urandom(8).hex(),
                trace_flags=parent_context.trace_flags,
            )
            parent_id = parent_context.span_id
        else:
            ctx = SpanContext.generate()
            parent_id = None

        span = TraceSpan(
            name=name,
            context=ctx,
            parent_span_id=parent_id,
            attributes=attributes or {},
        )
        span.set_attribute("service.name", self.service_name)
        return span


tracer = Tracer()
