# CHUNK 2: RUN LOG
**Project:** MetroLens AI (SIH26034)  
**Chunk:** Chunk 2 — OCR Engine Foundation  
**Start Timestamp:** 2026-09-05T04:02:00+05:30  
**Status:** RECONCILED, HARDENED & FROZEN  

| Timestamp (UTC/IST) | Action | Tool / Subsystem | Purpose | Result / Artifact Created |
| :--- | :--- | :--- | :--- | :--- |
| **04:02:00** | Chunk 2 Initialization | Filesystem inspection | Inspect baseline environment and repository state | `CURRENT_STATE/CHUNK_2_BASELINE.md` created. |
| **04:02:30** | Plan Formalization | Document generation | Establish Chunk 2 scope, constraints, and microstep protocol | `AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/01_PLAN/CHUNK_2_PLAN.md` created. |
| **04:07:22** | Runtime Compatibility Gate | Upstream PyPI & package audit | Evaluate RapidOCR (<3.13) vs Direct ONNX Runtime (3.14) | Selected Option B (Direct ONNX Runtime); created `02_RESEARCH/RUNTIME_DECISION.md`. |
| **04:07:28** | Model Currency Check | Hugging Face PP-OCRv5 audit | Investigate PP-OCRv5 vs PP-OCRv3 CTC | Retained PP-OCRv3 SVTR CTC for MVP; created `02_RESEARCH/MODEL_CURRENCY_CHECK.md`. |
| **04:10:39** | Model Assets & Manifest | Filesystem & YAML | Relocate ONNX weights to `models/weights/ocr/` with SHA-256 | Created `models/manifest.yaml`. |
| **04:12:12** | Types, Config & Errors | Code implementation | Implement `types.py`, `config.py`, `errors.py` with backward compatibility | Passed initial 6 unit tests. |
| **04:13:53** | Direct DBNet Detector | Code implementation | Implement `detector.py` with `pyclipper` polygon dilation | Verified 4-point convex polygon extraction and coordinate remapping. |
| **04:15:25** | Recognizers & Router | Code implementation | Implement `recognizer.py` (SVTR-EN & SVTR-HI) and `router.py` | Verified CTC decoding on English and Hindi text lines. |
| **04:15:35** | OCREngine Public Facade | Code implementation | Implement `engine.py` and `nirikshak_ocr/__init__.py` | Complete end-to-end extraction pipeline with `NirikshakOCREngine` adapter. |
| **04:16:00** | Comprehensive Test Suite | Pytest execution | Run unit and integration tests across synthetic fixtures | 21 tests passed in 1.39s. |
| **04:16:42** | Benchmark Harness Execution | `run_chunk2_benchmark.py` | Sweep threads (1,2,4,8), memory stability (25 inf), and specimens | Optimal threads=4 (110.47ms median); RSS stable at ~305MB; results in `benchmarks/ocr/chunk2/`. |
| **04:17:03** | Offline Network Isolation | Pytest execution with socket block | Prove zero network egress during OCR execution | 100% PASS in `tests/unit/test_ocr_offline.py`. |
| **04:17:17** | Visual Debugging Tool | Code implementation & run | Generate polygon overlay on test specimen | Created `tools/visualize_ocr_debug.py` and `debug_visual.png`. |
| **04:18:04** | Status & Handoff Formalization | Document generation | Finalize Chunk 2 review, status, and downstream contracts | Created `CHUNK_2_STATUS.md`, `CHUNK_2_TO_CHUNK_3.md`, and `FINAL_CHUNK_2_REPORT.md`. |
| **04:28:00** | Repository Audit & Claims Verification | Subsystem inspection & Pytest | Verify actual vs documented state; confirm tests and dependencies | Confirmed 23 OCR tests passing in 1.91s; 0 rapidocr imports in production. |
| **04:30:00** | Dependency Consistency Hardening | `pyproject.toml` edit | Align `packages/ocr/pyproject.toml` with actual imported runtime libraries | Added `onnxruntime`, `opencv-python`, `pyclipper`, `shapely`, `pydantic`. |
| **04:31:00** | Stale Documentation Reconciliation | Code & docs search & replace | Search and replace stale `PaddleOCR v4` and `char_height_px` references | Reconciled `MEMBER_1_WORK_PLAN.md`, `PROJECT_EXECUTION_OVERVIEW.md`, `INTEGRATION_CHECKLIST.md`. |
| **04:32:00** | Runnable Verification Execution | `tools/verify_ocr_run.py` | Run standalone verification on English, Hindi, and Blank specimens | Verified: English 97.84ms (6 tokens), Hindi 65.64ms (5 tokens), Blank 22.66ms (0 tokens), None handled safely. |
| **04:32:30** | Benchmark Re-run & Confirmation | Background task `task-920` | Empirical thread sweep, memory stability, and specimen latency | Confirmed: 4 threads optimal (107.29ms median); RSS plateau at 305.04MB (+0.02MB delta). |
| **04:33:00** | Inter-Member Handoff Specifications | Document generation | Formalize M1->M2, M1->M3, M1->M4, M1->M5, M1->M6 contracts | Created `M1_TO_M2_CHUNK2.md`, `M1_TO_M3_CHUNK2.md`, `M1_TO_M4_CHUNK2.md`, `M1_TO_M5_CHUNK2.md`, `M1_TO_M6_CHUNK2.md`. |
| **04:34:00** | Final Status, Report & Baseline Lock | Documentation updates | Update `FINAL_CHUNK_2_REPORT.md`, `CHUNK_2_TO_CHUNK_3.md`, `CHUNK_2_STATUS.md` | Frozen contract; zero git commits/pushes. |
