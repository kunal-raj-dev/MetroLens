# Performance Claims Policy & Register

## Purpose
Governs all quantitative assertions regarding throughput, optical character recognition accuracy, bounding box precision, and inference latency.

## Anti-Hallucination Mandate
No performance numbers, accuracy percentages, or latency benchmarks may be committed to documentation or slides without an accompanying JSON/CSV test artifact in `benchmarks/results/`.

---

## Performance Targets vs. Verified Empirical Results

| Metric | Proposed Design Target | Empirical Benchmark Result | Benchmark Protocol Reference | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Character Error Rate (CER)** | $\le 2.5\%$ on clean flat panels (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_OCR_EVAL.md` | TBD_MEASURE |
| **Word Error Rate (WER)** | $\le 5.0\%$ on clean flat panels (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_OCR_EVAL.md` | TBD_MEASURE |
| **Font Height Measurement Error** | $\le \pm 0.2\text{ mm}$ with scale (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_CALIBRATION_EVAL.md` | TBD_MEASURE |
| **PDP Area Segmentation IoU** | $\ge 0.85$ IoU (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_PDP_EVAL.md` | TBD_MEASURE |
| **End-to-End Inspection Latency** | $\le 4.0\text{ s}$ per capture (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_LATENCY_EVAL.md` | TBD_MEASURE |
| **Offline Pipeline Capability** | $100\%$ local execution (`TARGET — NOT VALIDATED`) | TBD — MEASURE | `benchmarks/protocols/PROTO_OFFLINE_EVAL.md` | EXPERIMENT_REQUIRED |

> [!IMPORTANT]
> All figures above marked `TBD — MEASURE` are placeholders for planned benchmark runs. All design targets are strictly non-validated engineering goals (`TARGET — NOT VALIDATED`). Antigravity and contributors are strictly prohibited from replacing `TBD — MEASURE` with fabricated numbers.
