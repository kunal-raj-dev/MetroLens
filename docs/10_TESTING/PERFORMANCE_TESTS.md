# Performance & Load Testing Specification

## Purpose
Specifies automated load tests, CPU thread concurrency benchmarks, and latency regression checks.

## Scope
Covers local mobile/laptop inference performance and backend API ingestion under multi-officer batch uploads.

## Authoritative Inputs
- `docs/03_PRODUCT_REQUIREMENTS/NON_FUNCTIONAL_REQUIREMENTS.md`

## Assumptions
- Performance testing isolates hardware specifications to guarantee reproducible measurements.

## Open Questions
- Target throughput on multi-core ARM servers for centralized departmental batch audits [TBD — MEASURE].

## Dependencies
- `benchmarks/protocols/`

## Verification Requirements
- All performance benchmarks must produce machine-readable JSON metrics stored in `benchmarks/results/`.

---

## Performance Test Scenarios

1. **Scenario PERF-01: Single-Thread Field Latency**
   - Ingestion of 4-panel package (front, back, 2 sides) on single CPU core.
   - Target: End-to-end processing $\le 5.0\text{ s}$.
   - Metric: `TBD — MEASURE`.

2. **Scenario PERF-02: Peak Memory Consumption**
   - Memory footprint during simultaneous OCR text detection and polygon dewarping.
   - Target: Resident Set Size (RSS) $\le 1.8\text{ GB}$.
   - Metric: `TBD — MEASURE`.

3. **Scenario PERF-03: Concurrent API Ingestion**
   - 20 concurrent simulated field inspectors submitting dossiers via `apps/api/`.
   - Target: 0 dropped requests; $p95$ response time $\le 1.5\text{ s}$.
   - Metric: `TBD — MEASURE`.
