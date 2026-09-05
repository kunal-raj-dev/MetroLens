# MEMBER 1 — FINAL CLUTTER CLEANUP PLAN

**Subsystem**: Member 1 — Multilingual OCR Engine & Service  
**Auditor**: Independent Principal Engineer  
**Date**: 2026-09-05  
**Policy**: Safe classification without premature deletion. No code or asset deletion performed during freeze.  

---

## 1. Classification Taxonomy
- **KEEP**: Active production code, active tests, active verified benchmarks, and models required for freeze handoff.
- **ARCHIVE**: Historical documentation, design logs, and experimental records from Chunks 1–5 that provide audit trail but are superseded by Phase B Final Source of Truth.
- **REMOVE LATER**: Transitional scripts, obsolete temporary outputs, or redundant test files scheduled for cleanup after full multi-member monorepo integration.
- **REVIEW**: Items requiring cross-team consensus before modification.

---

## 2. Classified Inventory

| File / Path | Category | Classification | Rationale | Action for Freeze |
| :--- | :--- | :--- | :--- | :--- |
| `packages/ocr/src/nirikshak_ocr/*.py` | Production Code | **KEEP** | Core OCR engine, service, detector, recognizer, router, config, types, errors, preprocessing. | Frozen |
| `packages/ocr/tests/test_ocr_smoke.py` | Package Test | **KEEP** | Basic package health check. | Frozen |
| `tests/unit/test_ocr_*.py` | Monorepo Unit Tests | **KEEP** | Comprehensive unit test suite (chunk 3 hardening, regression, engine comprehensive, evaluation, preprocessing, offline, types, Phase B independent audit). | Frozen |
| `tests/integration/test_ocr_service_integration.py` | Integration Tests | **KEEP** | Verifies OCRService singleton, contract compliance, thread safety, socket guard. | Frozen |
| `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` | Model Asset | **KEEP** | DBNet++ detection ONNX model. | Frozen |
| `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx`| Model Asset | **KEEP** | SVTR-EN alphanumeric recognition ONNX model. | Frozen |
| `models/weights/ocr/rec_hi/rec.onnx` | Model Asset | **KEEP** | SVTR-HI Devanagari recognition ONNX model. | Frozen |
| `models/weights/ocr/rec_hi/dict.txt` | Model Asset | **KEEP** | 167-character Devanagari dictionary. | Frozen |
| `models/manifest.yaml` | Model Manifest | **KEEP** | Single source of truth for model hashes, licenses, versions. | Frozen |
| `benchmarks/ocr/final/*` | Final Benchmarks | **KEEP** | Machine-generated benchmark results, config, environment, runner. | Frozen |
| `data/synthetic/regression/*.png` | Test Data | **KEEP** | 8 synthetic regression specimens used for deterministic tests. | Frozen |
| `CURRENT_STATE/PHASE_B_BASELINE.md` | Baseline State | **KEEP** | Official Phase B audit baseline. | Frozen |
| `docs/audit/MEMBER_1_FINAL_SOURCE_OF_TRUTH.md` | Documentation | **KEEP** | Single source of truth for Member 1 subsystem. | Frozen |
| `docs/audit/MEMBER_1_DO_NOT_REBUILD.md` | Documentation | **KEEP** | Invariant freeze boundary specification for other members. | Frozen |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/` | Experiment Logs | **ARCHIVE** | Historical model evaluation between RapidOCR, Paddle, Tesseract, EasyOCR. Superseded by direct ONNX runtime. | Retain as historical audit record |
| `benchmarks/ocr/chunk2/` | Benchmark | **ARCHIVE** | Legacy RapidOCR benchmark baseline. Superseded by final benchmark suite. | Retain as historical comparison |
| `benchmarks/ocr/chunk3/` | Benchmark | **ARCHIVE** | Chunk 3 intermediate ONNX benchmark results. | Retain as historical evidence |
| `benchmarks/ocr/chunk4/` | Benchmark | **ARCHIVE** | Chunk 4 intermediate service integration results. | Retain as historical evidence |
| `tools/visualize_ocr_debug.py` | Diagnostic Utility | **REMOVE LATER** | Debug script for drawing bounding boxes on synthetic images. Useful for visual inspection, not needed in production. | Mark for post-integration cleanup |
| `tools/verify_ocr_run.py` | Verification Utility | **REMOVE LATER** | Standalone run verifier. Redundant with automated pytest suite. | Mark for post-integration cleanup |
| `packages/ocr/README.md` (Legacy mentions) | Docs | **REVIEW** | Contains minor legacy RapidOCR reference; update to reflect pure ONNX Runtime. | Keep updated |
