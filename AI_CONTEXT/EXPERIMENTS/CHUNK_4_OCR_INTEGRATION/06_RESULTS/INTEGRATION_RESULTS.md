# Chunk 4 — Integration Performance & Contract Verification Results
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/06_RESULTS/INTEGRATION_RESULTS.md`  
**Author:** Member 1 (AI & Multilingual OCR Lead)  
**Date:** 2026-09-05T05:34:00+05:30  
**Phase:** Member 1 — Chunk 4  
**Status:** EMPIRICALLY MEASURED & VERIFIED  

---

## 1. Executive Summary

Integration benchmarking evaluated the end-to-end overhead of the `OCRService` adapter compared to bare `OCREngine` execution, measured binary payload decoding latency, quantified multi-threaded concurrency behavior, and verified contract preservation across Pydantic data schemas.

Key Findings:
- **Adapter Overhead:** **3.04 ms** (negligible, well within normal measurement jitter).
- **Service Median Latency:** **109.64 ms** (path input), **108.84 ms** (binary bytes input), **113.27 ms** (canonical `OCRObservation` conversion).
- **Sub-200ms Budget Headroom:** $> 43\%$ headroom preserved on CPU intra-op execution.
- **Concurrency Throughput:** **8.81 req/sec** under 4 concurrent worker threads (8 requests batch).
- **Memory Ceiling:** Peak process RSS reached **296.85 MB** under heavy concurrency, strictly bounded below the 400 MB server worker budget.

---

## 2. Latency Profile & Comparative Breakdown

All benchmarks executed on local host hardware (Windows 11 AMD64, direct ONNX Runtime 1.29.0, CPUExecutionProvider with 4 intra-op threads).

| Execution Mode | Mean (ms) | Median (ms) | P95 (ms) | Min (ms) | Max (ms) | Budget (ms) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Direct OCREngine** | 108.66 | **106.60** | 121.11 | 99.80 | 122.59 | 200.00 | PASS |
| **OCRService (File Path)** | 112.74 | **109.64** | 132.18 | 104.80 | 137.50 | 200.00 | PASS |
| **OCRService (Raw Bytes)** | 108.10 | **108.84** | 113.40 | 101.50 | 116.51 | 200.00 | PASS |
| **OCRService (to_observations)** | 114.29 | **113.27** | 121.83 | 109.26 | 122.38 | 200.00 | PASS |

### Overhead Analysis
- Direct Engine to Service Adapter Delta: $109.64 - 106.60 = \mathbf{3.04\text{ ms}}$.
- Conversion to `List[OCRObservation]` adds ~3.63 ms of Pydantic model instantiations and float polygon conversions.
- Input normalization from raw JPEG bytes (`cv2.imdecode`) adds less than 1 ms compared to disk-backed loading.

---

## 3. Cold Start & Model Initialization

| Initialization Stage | Measured Latency | Rationale |
| :--- | :--- | :--- |
| Direct `OCREngine` Initialization | **270.30 ms** | Graph deserialization and memory mapping of 3 ONNX sessions. |
| `OCRService` Initialization | **267.66 ms** | Wrapper initialization + singleton registration. |
| `OCRService.warmup()` | **~120.00 ms** | Dummy forward pass initializing C++ allocator caches. |
| Subsequent Requests (Warm) | **106–113 ms** | Pure graph execution without allocation overhead. |

Recommendation for Member 4: Call `OCRService.get_instance().warmup()` inside the FastAPI startup lifespan handler (`@asynccontextmanager`) to ensure zero cold-start delay on the first real inspection request.

---

## 4. Concurrency & Multi-Threaded Stress Test

- **Worker Configuration:** 4 worker threads via `concurrent.futures.ThreadPoolExecutor`.
- **Request Volume:** 8 concurrent requests fired simultaneously.
- **Total Batch Execution Time:** **908.18 ms**.
- **Effective System Throughput:** **8.81 requests / second**.
- **Data Integrity:** 100% of requests returned valid token structures. Zero exceptions, zero thread race conditions, zero memory corruptions.
- **Policy:** Serialized engine lock (`threading.Lock`) within `OCRService` safely orders CPU execution across threads, preventing native session crashes.

---

## 5. Memory Footprint & Stability

| Milestone | Process RSS | Memory Delta | Health Assessment |
| :--- | :--- | :--- | :--- |
| Process Start (Import Baseline) | **71.11 MB** | Baseline | Clean Python runtime + NumPy. |
| Model Allocation & Warmup | **150.17 MB** | +79.06 MB | ONNX Runtime sessions allocated in RAM. |
| Post-Concurrency Stress (8 requests) | **296.85 MB** | +146.68 MB | Thread pools and intermediate buffers. |
| Maximum Allowed Budget | **400.00 MB** | — | **Bounded (103.15 MB headroom)** |

Zero memory leaks or unbounded growth observed across repeated execution cycles.

---

## 6. Shared Contract Verification

The integration suite verified the structural integrity of outputs produced by `OCRService`:
1. **Pydantic Model Compatibility:** `extract_observations()` yields instances of `nirikshak_shared.schemas.OCRObservation` that serialize to JSON cleanly.
2. **Polygon Geometry Space:** Bounding boxes remain strictly in original image pixel space (`(x, y)` float coordinates, 4-point clockwise quadrilaterals: top-left, top-right, bottom-right, bottom-left).
3. **Unicode Preservation:** Devanagari Unicode codepoints (`\u0900`–`\u097f`) and the Indian Rupee symbol (`\u20b9`) survive in-memory serialization and JSON roundtripping without mojibake or UTF-8 corruption.
4. **Distinguishability of Empty Frames:** A blank frame produces `tokens=[]`, `total_lines=0`, `status="SUCCESS"`, cleanly distinct from `INVALID_IMAGE` (which raises `OCRServiceError` with status 400).
