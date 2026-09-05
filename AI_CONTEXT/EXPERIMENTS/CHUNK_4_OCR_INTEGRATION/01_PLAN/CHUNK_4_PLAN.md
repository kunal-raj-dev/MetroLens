# CHUNK 4: OCR MONOREPO INTEGRATION & SERVICE ADAPTER PLAN
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/01_PLAN/CHUNK_4_PLAN.md`  
**Author:** Member 1 — AI & Multilingual OCR Lead  
**Date:** 2026-09-05T05:29:00+05:30  
**Phase:** Chunk 4  

---

## 1. Goal & Architectural Purpose
The goal of Chunk 4 is to transition the Nirikshak OCR subsystem from a standalone algorithm package into a production-grade, monorepo-integrated service component.

```
Incoming Request (HTTP / Service)
          │
          ▼
   [ apps/api ]  (Member 4 Owned)
          │
          ▼
   [ OCRService ]  (Member 1 Owned: packages/ocr/src/nirikshak_ocr/service.py)
   ├── Input Validation & Safe Array Conversion (JPEG, PNG, WebP, ndarray)
   ├── Lifecycle Management (Session Reuse, Lazy Initialization, Thread-safe execution)
   ├── Execution Instrumentation (Processing Time, Warnings, Diagnostic Stage Timings)
   └── Error Translation (Structured Service Exceptions)
          │
          ▼
   [ OCREngine ]  (PP-OCRv3-ROUTED Direct ONNX Runtime)
          │
          ▼
   [ OCRResult ]
          │
          ├──► to_observations() ──► List[OCRObservation]  (Member 3 / Rules Engine)
          └──► to_api_dict()     ──► JSON Transport DTO    (Member 4 / Member 5)
```

## 2. Strict Boundary Rules
1. **Member 1 (OCR):** Owns `packages/ocr/`, `OCRService`, `OCREngine`, `OCRConfig`, `OCRResult`, `OCRToken`, integration tests, performance benchmarks.
2. **Member 4 (API):** Owns `apps/api/`, HTTP routing, upload middleware, endpoint security.
3. **No Legal Logic:** Zero Rule 6/7/8/9/11/26 logic in OCR.
4. **No Calibration:** Zero millimeter conversion, zero font height compliance checks in OCR.
5. **Synchronous MVP:** Zero Celery, zero Redis, zero message queues. Synchronous execution only.
6. **Git Safety:** Zero git commits or pushes.

## 3. Microstep Execution Sequence
- **Step 1:** Model path resolution hardening (environment variable support, CWD-independence).
- **Step 2:** Implement `OCRService` in `packages/ocr/src/nirikshak_ocr/service.py` with singleton lifecycle management, input format conversion, and structured error handling.
- **Step 3:** Shared contract serialization verification (`OCRResult` $\rightarrow$ `OCRObservation` and JSON DTO).
- **Step 4:** Concurrency, memory, and offline isolation tests.
- **Step 5:** Integration test suite in `tests/integration/test_ocr_service_integration.py`.
- **Step 6:** Benchmark integration path (`benchmarks/ocr/chunk4/`).
- **Step 7:** Document handoffs and final report.
