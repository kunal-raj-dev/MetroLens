# MetroLens AI — "Where Is Everything?" Navigation Guide
**Audience:** Developers who need immediate, plain-English directions to files and folders without wading through hundreds of documentation pages.  
**Audit Baseline Date:** 2026-09-05

---

## Direct Navigation Answers

### 1. Where is the OCR?
- **Core Engine:** `packages/ocr/src/nirikshak_ocr/engine.py` (facade orchestrating detection & recognition).
- **Service Adapter:** `packages/ocr/src/nirikshak_ocr/service.py` (`OCRService` singleton for backend integration).
- **Detector:** `packages/ocr/src/nirikshak_ocr/detector.py` (DBNet++ text detector).
- **Recognizer:** `packages/ocr/src/nirikshak_ocr/recognizer.py` (SVTR English and Hindi text recognizers).
- **Script Router:** `packages/ocr/src/nirikshak_ocr/router.py` (directs crops to English vs Hindi models).
- **Preprocessing:** `packages/ocr/src/nirikshak_ocr/preprocessing.py` (CLAHE, bilateral, unsharp, dilation).
- **Config:** `packages/ocr/src/nirikshak_ocr/config.py` (`OCRConfig` Pydantic class).

### 2. Where are the models?
- **ONNX Weights:** `models/weights/ocr/`
  - Detector: `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` (2.43 MB)
  - English Recognizer: `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` (10.69 MB)
  - Hindi Recognizer: `models/weights/ocr/rec_hi/rec.onnx` (8.98 MB)
  - Hindi Dictionary: `models/weights/ocr/rec_hi/dict.txt` (167 characters)
- **Model Manifest:** `models/manifest.yaml` (specifies hashes, licenses, and sources).

### 3. Where are the OCR tests?
- **Unit Tests:** `tests/unit/` (`test_ocr_engine_comprehensive.py`, `test_ocr_types_config.py`, `test_ocr_preprocessing.py`, `test_ocr_evaluation.py`, `test_ocr_chunk3_hardening.py`, `test_ocr_chunk3_regression.py`, `test_ocr_offline.py`).
- **Integration Tests:** `tests/integration/test_ocr_service_integration.py` (16 tests verifying `OCRService` adapter and shared contracts).
- **Package Smoke Test:** `packages/ocr/tests/test_ocr_smoke.py`.

### 4. Where is calibration?
- **Code:** `packages/calibration/src/nirikshak_calibration/__init__.py` (currently a 67-line math stub; does not detect coins from images yet).
- **Measurement Logic:** `packages/measurement/src/nirikshak_measurement/__init__.py` (multiplies pixels by scale factor).
- **Documentation:** `docs/05_AI_VISION/CALIBRATION.md` and `docs/05_AI_VISION/FONT_MEASUREMENT.md`.

### 5. Where are the legal rules?
- **Rule Engine Code:** `packages/rules-engine/src/nirikshak_rules_engine/__init__.py` (currently a 39-line stub evaluating only MRP presence).
- **Proposed YAML Rules:** `rules/proposed/` (`rule_06_mandatory_declarations_candidate.yaml`, `rule_07_table1_font_height_candidate.yaml`).
- **Rule Schemas:** `rules/schema/` (`rule.schema.json`, `evidence.schema.json`, `applicability.schema.json`).
- **Legal Rule Matrix Doc:** `docs/LEGAL_RULE_MATRIX.md` and `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/`.

### 6. Where is the backend?
- **FastAPI Code:** `apps/api/main.py` (currently returns mock JSON).
- **Worker Code:** `apps/worker/main.py` (scaffold worker class).
- **Database Schema:** `infra/db/init.sql` (PostgreSQL 16 table creation script).

### 7. Where is the frontend?
- **Next.js Web Code:** `apps/web/src/app/page.tsx` (currently a static 40-line landing page).
- **Package Config:** `apps/web/package.json` (Next.js 14, React 18, Tailwind 3).
- **Layout:** `apps/web/src/app/layout.tsx`.

### 8. Where is the benchmark data?
- **OCR Benchmarks:** `benchmarks/ocr/`
  - Chunk 2 (CPU Thread Sweep): `benchmarks/ocr/chunk2/results.json`.
  - Chunk 3 (Preprocessing Filter Benchmark): `benchmarks/ocr/chunk3/final_results.json`.
  - Chunk 4 (Service Adapter Latency & Concurrency): `benchmarks/ocr/chunk4/integration_results.json`.

### 9. Where is the synthetic data?
- **Synthetic Packaging Images:** `data/synthetic/regression/` (contains 8 PNG test specimens: `SYNTH-01-ENG-FMCG.png` through `SYNTH-08-LOW-CONTRAST-FADED.png`).
- **Synthetic Manifest:** `data/synthetic/regression/manifest.json`.

### 10. Where is the real packaging data?
- **Directory:** `data/raw/real/`.
- **Actual Status:** **COMPLETELY EMPTY (0 IMAGES)**. Real packaging data collection is formally BLOCKED awaiting delivery by Member 6.
- **Target Specification:** `data/manifests/real_packaging_manifest.json` (defines the 35-SKU target).

### 11. Where are the project plans?
- **Master Plans:** `docs/IMPLEMENTATION_PLAN.md`, `docs/PRODUCT_BLUEPRINT.md`, `docs/ARCHITECTURE.md`.
- **Individual Member Plans:** `docs/team/MEMBER_1_WORK_PLAN.md` through `docs/team/MEMBER_6_WORK_PLAN.md`.
- **Execution Overview:** `docs/team/PROJECT_EXECUTION_OVERVIEW.md`.

### 12. Where is the current state?
- **Authoritative Snapshot:** `CURRENT_STATE/PROJECT_SNAPSHOT.md`.
- **Latest Chunk Baseline:** `CURRENT_STATE/CHUNK_4_BASELINE.md` and `CURRENT_STATE/CHUNK_4_STATUS.md`.
- **Audit Dashboard:** `docs/audit/CURRENT_PROJECT_DASHBOARD.md`.

### 13. Where is AI context?
- **Execution Run Logs:** `AI_CONTEXT/RUN_LOGS/` (`CHUNK_1_RUN_LOG.md` to `CHUNK_4_RUN_LOG.md`).
- **Chunk Experiments:** `AI_CONTEXT/EXPERIMENTS/` (Spikes and research for Chunks 1 to 4).
- **Handoffs:** `AI_CONTEXT/HANDOFFS/` (Formal handoff notes between chunks and members).
- **Project Context Baseline:** `AI_CONTEXT/PROJECT_CONTEXT.md`.

### 14. Where are the legal sources?
- **Authoritative Sovereign PDFs:** `METROLENS_LEGAL_SOURCE_PACK/` (74 official Indian government Gazette PDFs).
- **Legal Source Index:** `METROLENS_LEGAL_SOURCE_PACK/00_SOURCE_INDEX/SOURCE_REGISTER.csv` and `CHECKSUM_MANIFEST.csv`.
- **Machine-Readable Metadata:** `regulations/source_registry.yaml`.

### 15. Where are APIs documented?
- **API Contract:** `docs/API_CONTRACT.md`.
- **FastAPI OpenAPI (Interactive Docs):** Automatically served at `http://localhost:8000/docs` when running `uvicorn apps.api.main:app`.

### 16. Where are experiments?
- **Historical Completed Experiments:** `AI_CONTEXT/EXPERIMENTS/` (Chunks 1 to 4).
- **Scratch Experiment Dirs:** `experiments/` (currently empty placeholder directories with `.gitkeep`).

### 17. Where are reports?
- **Inspection Dossier Generator:** `packages/reporting/src/nirikshak_reporting/__init__.py`.
- **Problem Statement Dossier:** `problem statement #1/SIH26034_Dossier.pdf`.
- **Benchmark Reports:** `benchmarks/ocr/chunk4/README.md` and `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/07_REVIEW/FINAL_CHUNK_4_REPORT.md`.

### 18. Where are handoffs?
- **Formal Handoff Folder:** `AI_CONTEXT/HANDOFFS/` (e.g., `M1_TO_M4_CHUNK4.md`, `CHUNK_3_TO_CHUNK_4.md`, `CHUNK_4_TO_CHUNK_5.md`).

### 19. Where are scripts?
- **Integrity Verification Scripts:** `scripts/verification/` (`verify_claims.py`, `verify_repository_integrity.py`, etc.).
- **Developer Utilities:** `tools/` (`verify_ocr_run.py`, `visualize_ocr_debug.py`, `build_all_in_one_context.py`).

### 20. Where are generated artifacts?
- **All-in-One Documentation Dump:** `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md` (720 KB).
- **Pytest Cache:** `.pytest_cache/`.
- **Python Bytecode:** `__pycache__/` folders across packages.
