# Member 1 Truth Matrix: Claims vs. Forensic Evidence

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Date**: September 2026  
**Status**: 100% EVIDENCE-BACKED AUDIT

---

## 1. Subsystem Architecture & Technology Claims

| Claim | Claimed State | Forensic Code / Test Evidence | Verified Reality | Honest Assessment / Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Pure ONNX Runtime Architecture** | Zero dependencies on PaddlePaddle or RapidOCR | `packages/ocr/pyproject.toml`, recursive grep verification | 100% pure ONNX Runtime CPU inference. | Paddle and RapidOCR completely eliminated. Builds cleanly on Python 3.14. |
| **Multilingual Script Routing** | Dual-recognizer routing Latin vs Devanagari | `packages/ocr/src/nirikshak_ocr/pipeline.py` | Latin routed to PP-OCRv3 Latin; Indic routed to `rec.onnx` + `dict.txt`. | Accurate routing verified on bilingual specimens; regional Indic scripts remain future work. |
| **Indian Rupee Symbol Support** | Recognizes official `₹` currency symbol | `models/dict.txt`, `test_extract_hindi_devanagari_and_currency_symbol()` | Character `₹` (U+20B9) recognized in Hindi FMCG prices. | Fully verified; prevents legal confusion between "Rs." and "₹". |
| **Air-Gapped Offline Execution** | Zero cloud calls or socket network access | `tests/integration/test_ocr_service_integration.py` (`test_offline_execution_socket_guard`) | Pipeline executes successfully when `socket.socket` is blocked. | Guaranteed local edge privacy and zero API token costs. |
| **Thread Safety** | Safe for multi-threaded ingress | `packages/ocr/src/nirikshak_ocr/service.py` (`self._engine_lock`) | 8 concurrent threads executed with 100% token consistency. | Concurrency protected via session lock. |

---

## 2. Performance & Resource Claims

| Metric | Target Specification | Benchmark Artifact / File | Verified Metric (Host CPU) | Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **Cold Engine Initialization** | < 1,000 ms | `benchmarks/ocr/final/results.json` | 481.14 ms | Exceeds target by ~52%. |
| **Cold Service Initialization** | < 1,000 ms | `benchmarks/ocr/final/results.json` | 451.38 ms | Exceeds target by ~55%. |
| **Session Warmup Latency** | < 50 ms | `benchmarks/ocr/final/results.json` | 14.93 ms | Immediate readiness on prime. |
| **English Inference Latency** | < 250 ms (CPU) | `benchmarks/ocr/final/results.json` | 139.18 ms median | ~110 ms headroom under SLA. |
| **Hindi Inference Latency** | < 250 ms (CPU) | `benchmarks/ocr/final/results.json` | 115.79 ms median | High efficiency on CTC recognizer. |
| **Bilingual Inference Latency** | < 300 ms (CPU) | `benchmarks/ocr/final/results.json` | 188.62 ms median | Includes dual-route recognition passes. |
| **Blank Frame Latency** | < 100 ms | `benchmarks/ocr/final/results.json` | 49.68 ms median | Fast exit upon zero detection. |
| **Throughput (4 Threads)** | > 4 req/sec | `benchmarks/ocr/final/results.json` | 5.87 req/sec | Satisfies edge appliance requirement. |
| **Decompression Bomb Rejection** | < 5 ms | `benchmarks/ocr/final/results.json` | 0.038 ms | Rejects 67.1 MP array in 38 microseconds. |

---

## 3. Dataset & Scientific Honesty Claims

| Domain | Claimed Capability | Forensic Evidence | Verified State | Honest Reality / Disclaimers |
| :--- | :--- | :--- | :--- | :--- |
| **Real Retail Packaging Accuracy** | >95% accuracy on Indian store shelves | N/A (Path B active) | **UNTESTED ON PHYSICAL SHELF PACKAGING** | **Path B Active**: 0 physical packaging images in repo. Synthetic specimens used exclusively for test/contract verification. No claim of real-world accuracy is made. |
| **Synthetic FMCG Accuracy** | 100% token accuracy on synthetic packaging | `tests/integration/test_ocr_service_integration.py` | 100% token and character match across English, Hindi, and bilingual test specimens. | Validates detection math, CTC decoding, and dictionary matching. |
| **Input Immutability** | Image array passed by caller is never modified in place | `tests/integration/test_ocr_service_integration.py` (`test_input_array_immutability`) | Hash of input numpy array identical before and after inference. | Guaranteed via defensive cloning. |
| **Bounding Box Validity** | 4-point clockwise polygons within image boundaries | `tests/integration/test_ocr_service_integration.py` (`test_polygon_geometry_contract_and_ordering`) | All emitted polygons are clockwise with positive area and valid coordinates. | Verified against shared contract. |

---

## 4. Architectural Boundary Claims

| Boundary Area | Claimed Invariant | Forensic Verification | Status |
| :--- | :--- | :--- | :--- |
| **Legal Metrology Rule Logic** | Member 1 contains ZERO legal rules | Zero imports of `nirikshak_rules` or rule files in `packages/ocr/` | **100% STRICT BOUNDARY** (Owned by Member 2) |
| **Physical mm Measurement** | Member 1 contains ZERO mm calibration math | No camera calibration or mm/pixel logic in `packages/ocr/` | **100% STRICT BOUNDARY** (Owned by Member 3) |
| **Web API / Frameworks** | Member 1 contains ZERO FastAPI or HTTP transport logic | Pure Python library; no HTTP handlers | **100% STRICT BOUNDARY** (Owned by Member 4) |
| **User Interface** | Member 1 contains ZERO frontend UI code | Headless CV/ML subsystem | **100% STRICT BOUNDARY** (Owned by Member 5) |
