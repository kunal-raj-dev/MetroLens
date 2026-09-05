"""
Prometheus Metrics Exposition Engine
====================================
Collects and formats application metrics into Prometheus plain-text format
(RFC 0001 / OpenMetrics) for enterprise monitoring and Grafana visualization.

Monitored Domains:
    - Inspection counts partitioned by verdict and commodity category.
    - Statutory rule failure counts partitioned by Rule ID (e.g. Rule 6(1)(e), Rule 26).
    - Security firewall rejection counts (decompression bomb, magic bytes, file cap).
    - Microsecond stage latency histograms.
    - Two-tier cache hit/miss distributions.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


class CounterMetric:
    """Thread-safe multi-dimensional counter."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self._counts: Dict[Tuple[Tuple[str, str], ...], float] = defaultdict(float)
        self._lock = threading.Lock()

    def inc(self, value: float = 1.0, **labels: str) -> None:
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._counts[label_key] += value

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.description}", f"# TYPE {self.name} counter"]
        with self._lock:
            for labels, count in sorted(self._counts.items()):
                if labels:
                    lbl_str = ",".join(f'{k}="{v}"' for k, v in labels)
                    lines.append(f"{self.name}{{{lbl_str}}} {count}")
                else:
                    lines.append(f"{self.name} {count}")
        return "\n".join(lines)


class GaugeMetric:
    """Thread-safe gauge metric."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = defaultdict(float)
        self._lock = threading.Lock()

    def set(self, value: float, **labels: str) -> None:
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] = value

    def inc(self, value: float = 1.0, **labels: str) -> None:
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] += value

    def dec(self, value: float = 1.0, **labels: str) -> None:
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] -= value

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.description}", f"# TYPE {self.name} gauge"]
        with self._lock:
            for labels, val in sorted(self._values.items()):
                if labels:
                    lbl_str = ",".join(f'{k}="{v}"' for k, v in labels)
                    lines.append(f"{self.name}{{{lbl_str}}} {val}")
                else:
                    lines.append(f"{self.name} {val}")
        return "\n".join(lines)


class HistogramMetric:
    """Thread-safe cumulative histogram with custom buckets."""

    DEFAULT_BUCKETS = (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, float("inf"))

    def __init__(
        self, name: str, description: str, buckets: Tuple[float, ...] = DEFAULT_BUCKETS
    ) -> None:
        self.name = name
        self.description = description
        self.buckets = buckets
        self._bucket_counts: Dict[Tuple[Tuple[str, str], ...], Dict[float, int]] = defaultdict(
            lambda: {b: 0 for b in self.buckets}
        )
        self._sums: Dict[Tuple[Tuple[str, str], ...], float] = defaultdict(float)
        self._totals: Dict[Tuple[Tuple[str, str], ...], int] = defaultdict(int)
        self._lock = threading.Lock()

    def observe(self, value: float, **labels: str) -> None:
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._sums[label_key] += value
            self._totals[label_key] += 1
            for b in self.buckets:
                if value <= b:
                    self._bucket_counts[label_key][b] += 1

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.description}", f"# TYPE {self.name} histogram"]
        with self._lock:
            for label_key in sorted(self._totals.keys()):
                lbl_dict = dict(label_key)
                # Render buckets
                for b in self.buckets:
                    b_str = "+Inf" if b == float("inf") else str(b)
                    lbl_with_le = dict(lbl_dict)
                    lbl_with_le["le"] = b_str
                    lbl_str = ",".join(f'{k}="{v}"' for k, v in sorted(lbl_with_le.items()))
                    cnt = self._bucket_counts[label_key][b]
                    lines.append(f"{self.name}_bucket{{{lbl_str}}} {cnt}")

                # Sum and count
                base_lbl = ",".join(f'{k}="{v}"' for k, v in sorted(lbl_dict.items()))
                base_bracket = f"{{{base_lbl}}}" if base_lbl else ""
                lines.append(f"{self.name}_sum{base_bracket} {self._sums[label_key]}")
                lines.append(f"{self.name}_count{base_bracket} {self._totals[label_key]}")

        return "\n".join(lines)


class PrometheusMetricsRegistry:
    """
    Central registry exposing standard MetroLens operational telemetry.
    """

    def __init__(self) -> None:
        self.inspections_total = CounterMetric(
            "metrolens_inspections_total",
            "Total packaging inspections processed partitioned by verdict and category.",
        )
        self.rule_violations_total = CounterMetric(
            "metrolens_rule_violations_total",
            "Total statutory violations identified partitioned by rule_id.",
        )
        self.security_blocks_total = CounterMetric(
            "metrolens_security_firewall_blocks_total",
            "Upload firewall rejections partitioned by security threat reason.",
        )
        self.rate_limit_rejections_total = CounterMetric(
            "metrolens_rate_limit_rejections_total",
            "Total requests rejected by leaky-bucket rate limiter.",
        )
        self.cache_events_total = CounterMetric(
            "metrolens_cache_events_total",
            "Perceptual and exact cache query outcomes.",
        )
        self.inspection_latency_seconds = HistogramMetric(
            "metrolens_inspection_duration_seconds",
            "Microsecond duration of inspection pipeline execution partitioned by stage.",
        )
        self.spool_disk_usage_bytes = GaugeMetric(
            "metrolens_spool_disk_usage_bytes",
            "Current disk bytes consumed by active ephemeral inspection spools.",
        )
        self.active_workers_gauge = GaugeMetric(
            "metrolens_active_workers",
            "Count of active thread pool background workers.",
        )

    def render_prometheus_text(self) -> str:
        """Render all metrics in compliant Prometheus text exposition format."""
        sections = [
            self.inspections_total.render(),
            self.rule_violations_total.render(),
            self.security_blocks_total.render(),
            self.rate_limit_rejections_total.render(),
            self.cache_events_total.render(),
            self.inspection_latency_seconds.render(),
            self.spool_disk_usage_bytes.render(),
            self.active_workers_gauge.render(),
        ]
        return "\n\n".join(sections) + "\n"


# Singleton instance for application-wide instrumentation
metrics = PrometheusMetricsRegistry()
