# MetroLens AI — Comprehensive File Explanation Guide
**Audit Baseline Date:** 2026-09-05  
**Core Purpose:** Provide a clear, evidence-based reference detailing the purpose, status, ownership, and role of every significant file in the repository.

---

## 1. Core Source Files (`packages/`)

### `packages/ocr/src/nirikshak_ocr/engine.py`
- **Type:** Python Module (Core Implementation)
- **Purpose:** Central facade orchestrating DBNet++ text detection, perspective rectification, script routing, and SVTR text recognition.
- **Current Role:** Primary OCR inference orchestrator.
- **Status:** ACTIVE_IMPLEMENTATION (Verified passing 89 tests).
- **Owner:** Member 1.
- **Dependencies:** `detector.py`, `recognizer.py`, `router.py`, `preprocessing.py`, `types.py`, `errors.py`, `numpy`, `onnxruntime`.
- **Used By:** `service.py`, `tests/unit/test_ocr_*.py`, benchmark scripts.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Core production asset).
- **Notes:** Thread-safe execution managed via higher-level service lock.

### `packages/ocr/src/nirikshak_ocr/service.py`
- **Type:** Python Module (Service Adapter)
- **Purpose:** Production singleton adapter wrapping `OCREngine` to normalize inputs (path, bytes, ndarray), serialize outputs to `nirikshak_shared` contracts, and enforce thread serialization.
- **Current Role:** In-process service gateway for the API layer.
- **Status:** ACTIVE_IMPLEMENTATION (Delivered in Chunk 4).
- **Owner:** Member 1.
- **Dependencies:** `engine.py`, `config.py`, `types.py`, `errors.py`, `nirikshak_shared.models.contracts`.
- **Used By:** `tests/integration/test_ocr_service_integration.py`, `apps/api/` (planned).
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (This is the primary contract boundary for Backend).

### `packages/ocr/src/nirikshak_ocr/detector.py`
- **Type:** Python Module (ML Inference)
- **Purpose:** Executes DBNet++ ONNX model (`ch_PP-OCRv3_det_infer.onnx`), binarizes probability maps, and extracts 4-point quadrilateral polygons via contour analysis and Vatti clipping.
- **Current Role:** Text detection stage.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Member 1.
- **Dependencies:** `onnxruntime`, `opencv-python`, `pyclipper`, `shapely`, `numpy`.
- **Used By:** `engine.py`.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `packages/ocr/src/nirikshak_ocr/recognizer.py`
- **Type:** Python Module (ML Inference)
- **Purpose:** Executes SVTR-LCNet models with CTC greedy decoding for Latin (English) and Devanagari (Hindi) scripts.
- **Current Role:** Text recognition stage.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Member 1.
- **Dependencies:** `onnxruntime`, `numpy`, `dict.txt`.
- **Used By:** `engine.py`.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `packages/ocr/src/nirikshak_ocr/router.py`
- **Type:** Python Module (Script Routing)
- **Purpose:** Classifies cropped text regions by script (Devanagari vs Latin) using Unicode block density and heuristic character aspect ratios.
- **Current Role:** Routes text crops to the appropriate recognizer.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Member 1.
- **Dependencies:** Python `unicodedata`, `numpy`.
- **Used By:** `engine.py`.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `packages/ocr/src/nirikshak_ocr/config.py`
- **Type:** Python Module (Configuration)
- **Purpose:** Strongly typed Pydantic configuration (`OCRConfig`) managing model weights paths, ONNX threading parameters, thresholds, and preprocessing policies.
- **Current Role:** Subsystem configuration.
- **Status:** ACTIVE_CONFIGURATION.
- **Owner:** Member 1.
- **Dependencies:** `pydantic`, `pathlib`, `os`.
- **Used By:** Entire `nirikshak_ocr` package.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Automatically discovers project root using `METROLENS_ROOT` environment variable or parent directory traversal.

### `packages/ocr/src/nirikshak_ocr/preprocessing.py`
- **Type:** Python Module (Image Processing)
- **Purpose:** Implements CLAHE, bilateral filtering, unsharp masking, morphological dilation, and adaptive low-contrast enhancement hooks.
- **Current Role:** Per-crop and full-image preprocessing.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Member 1.
- **Dependencies:** `opencv-python`, `numpy`.
- **Used By:** `engine.py`, benchmark harnesses.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Default mode is `raw` (`B0_BASELINE_RAW`) based on empirical evaluation.

### `packages/shared/src/nirikshak_shared/models/contracts.py`
- **Type:** Python Module (Canonical Data Contracts)
- **Purpose:** Pydantic DTO definitions for inter-package communication: `InspectionRequest`, `InspectionResult`, `OCRObservation`, `DeclarationField`, `MeasurementResult`, `RuleEvaluation`, `EvidenceItem`, `InspectionError`.
- **Current Role:** Canonical contract boundary across all monorepo subsystems.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Architecture Lead / All Members.
- **Dependencies:** `pydantic`, `primitives.py`.
- **Used By:** `packages/ocr`, `packages/rules-engine`, `packages/calibration`, `apps/api`, `apps/worker`.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Crucial monorepo seam).

### `packages/shared/src/nirikshak_shared/models/primitives.py`
- **Type:** Python Module (Domain Primitives)
- **Purpose:** Enumerations and geometric value objects: `CalibrationStatus`, `PanelName`, `RuleVerdict`, `OverallVerdict`, `InspectionStatus`, `BoundingBox`, `ObservedValue`.
- **Current Role:** Foundational types.
- **Status:** ACTIVE_IMPLEMENTATION.
- **Owner:** Architecture Lead / All Members.
- **Dependencies:** `pydantic`, Python `enum`.
- **Used By:** `contracts.py` and all packages.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `packages/vision/src/nirikshak_vision/__init__.py`
- **Type:** Python Module (Vision Scaffold)
- **Purpose:** Pre-inference quality gating (blur and specular glare detection).
- **Current Role:** Image quality filter stub.
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED (71 lines).
- **Owner:** Member 2.
- **Dependencies:** `numpy`.
- **Used By:** `apps/worker/main.py`, `packages/vision/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Needs full implementation by Member 2).
- **Notes:** Computes variance of raw gray array; does not use actual OpenCV Laplacian kernel or HSV glare mask yet.

### `packages/calibration/src/nirikshak_calibration/__init__.py`
- **Type:** Python Module (Calibration Scaffold)
- **Purpose:** Scale factor calculation ($S$ in mm/pixel).
- **Current Role:** Calibration stub (67 lines).
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED.
- **Owner:** Member 2.
- **Dependencies:** `nirikshak_shared.models.primitives`.
- **Used By:** `packages/calibration/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Contains math function `compute_scale_factor` that divides two numbers; does NOT detect coins or cards from an image.

### `packages/measurement/src/nirikshak_measurement/__init__.py`
- **Type:** Python Module (Measurement Scaffold)
- **Purpose:** Conversion of pixel heights to physical millimeters ($h_{\text{mm}} = h_{\text{px}} \times S$) and PDP area computation.
- **Current Role:** Measurement stub (44 lines).
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED.
- **Owner:** Member 2.
- **Dependencies:** `nirikshak_shared.models.contracts`.
- **Used By:** `packages/measurement/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `packages/extraction/src/nirikshak_extraction/__init__.py`
- **Type:** Python Module (Semantic Extraction Scaffold)
- **Purpose:** Regex and heuristic parsing of statutory fields from raw OCR observations.
- **Current Role:** Field extraction stub (47 lines).
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED.
- **Owner:** Member 3.
- **Dependencies:** `re`, `nirikshak_shared.models.contracts`.
- **Used By:** `packages/extraction/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Extracts only MRP via basic regex; net quantity, dates, manufacturer, and consumer care are unparsed.

### `packages/rules-engine/src/nirikshak_rules_engine/__init__.py`
- **Type:** Python Module (Rule Engine Scaffold)
- **Purpose:** Deterministic statutory rule evaluation.
- **Current Role:** Compliance engine stub (39 lines).
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED.
- **Owner:** Member 3.
- **Dependencies:** `nirikshak_shared.models.contracts`, `primitives.py`.
- **Used By:** `apps/worker/main.py`, `packages/rules-engine/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Implements only 1 rule: `LMPC-R06-MRP-001` (MRP Presence).

### `packages/reporting/src/nirikshak_reporting/__init__.py`
- **Type:** Python Module (Reporting Scaffold)
- **Purpose:** PDF inspection dossier generation.
- **Current Role:** Reporting stub (41 lines).
- **Status:** SCAFFOLD / PARTIALLY IMPLEMENTED.
- **Owner:** Member 4.
- **Dependencies:** `reportlab`, `nirikshak_shared.models.contracts`.
- **Used By:** `apps/worker/main.py`, `packages/reporting/tests/`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.
- **Notes:** Renders a 5-line plain text PDF; Section 36(1) notices and image crops are not implemented.

---

## 2. Application Entrypoints (`apps/`)

### `apps/api/main.py`
- **Type:** Python Application (FastAPI)
- **Purpose:** API gateway entrypoint providing endpoints for health check, inspection submission, and result retrieval.
- **Current Role:** Mocked API server (67 lines).
- **Status:** SCAFFOLD (Returns static mock JSON).
- **Owner:** Member 4.
- **Dependencies:** `fastapi`, `uvicorn`, `nirikshak_shared.models.contracts`.
- **Used By:** `apps/api/tests/test_api_smoke.py`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Needs integration with `OCRService` and rules).
- **Notes:** Does NOT invoke OCR or rules; returns hardcoded `COMPLIANT` result immediately.

### `apps/web/src/app/page.tsx`
- **Type:** TypeScript React Component
- **Purpose:** Web interface home page for regulatory officers to upload photos and view compliance verdicts.
- **Current Role:** Static landing page (40 lines).
- **Status:** SCAFFOLD.
- **Owner:** Member 5.
- **Dependencies:** Next.js App Router, React.
- **Used By:** Web browser.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Needs interactive upload and bounding-box canvas).
- **Notes:** Contains zero interactive components or API calls; `node_modules` not installed.

### `apps/worker/main.py`
- **Type:** Python Application
- **Purpose:** Background worker executing end-to-end inspection pipeline asynchronously.
- **Current Role:** Orchestrator stub (62 lines).
- **Status:** SCAFFOLD.
- **Owner:** Member 4.
- **Dependencies:** `nirikshak_vision`, `nirikshak_rules_engine`, `nirikshak_reporting`, `nirikshak_shared`.
- **Used By:** `apps/worker/tests/test_worker_smoke.py`.
- **Is Active?** ACTIVE SCAFFOLD.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

---

## 3. Configuration & Infrastructure Files

### `pytest.ini`
- **Type:** Configuration File
- **Purpose:** Configures root pytest execution, Python module paths (`testpaths = tests packages apps`, `pythonpath = packages/shared/src packages/ocr/src ...`), and custom markers.
- **Current Role:** Test discovery runner.
- **Status:** ACTIVE_CONFIGURATION.
- **Owner:** Member 6 / All Members.
- **Dependencies:** `pytest`.
- **Used By:** `pytest`, `python -m pytest`.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `models/manifest.yaml`
- **Type:** YAML Manifest
- **Purpose:** Machine-readable catalog of ML model weights, specifying file paths, SHA-256 hashes, licenses, and runtime requirements.
- **Current Role:** Model provenance authority.
- **Status:** ACTIVE_CONFIGURATION.
- **Owner:** Member 1 / Member 6.
- **Dependencies:** ONNX weights in `models/weights/ocr/`.
- **Used By:** Verification scripts.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `infra/db/init.sql`
- **Type:** SQL DDL Script
- **Purpose:** PostgreSQL 16 schema definition creating tables for `inspections`, `declarations`, `measurements`, `rule_evaluations`, `evidence_items`, and `audit_log`.
- **Current Role:** Database schema definition.
- **Status:** ACTIVE_CONFIGURATION / DDL ONLY.
- **Owner:** Member 4.
- **Dependencies:** PostgreSQL 16.
- **Used By:** `docker-compose.yml`.
- **Is Active?** ACTIVE SCHEMA (No ORM connection exists in code yet).
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

### `docker-compose.yml`
- **Type:** YAML Configuration
- **Purpose:** Multi-container orchestration definition for PostgreSQL, FastAPI, and Next.js services.
- **Current Role:** Local containerized runtime config.
- **Status:** ACTIVE_CONFIGURATION.
- **Owner:** Member 6.
- **Dependencies:** Docker Engine.
- **Used By:** `docker compose up`.
- **Is Active?** YES (Configured, but container builds unverified in audit).
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO.

---

## 4. Key Documentation & Context Files

### `CURRENT_STATE/PROJECT_SNAPSHOT.md`
- **Type:** Markdown Status Document
- **Purpose:** Authoritative single-page summary of current technical achievements, active chunk, and blockers.
- **Current Role:** Primary ground-truth status reference.
- **Status:** CURRENT_STATE (Authoritative).
- **Owner:** Orchestrator / Lead Engineer.
- **Dependencies:** None.
- **Used By:** AI agents and developers.
- **Is Active?** YES.
- **Is Duplicated?** NO.
- **Is Historical?** NO.
- **Safe to Ignore?** NO (Always read first).

### `docs/PRODUCT_BLUEPRINT.md`
- **Type:** Markdown Specification
- **Purpose:** Comprehensive product requirements, user journeys, 5-state compliance taxonomy, and system design.
- **Current Role:** Target product vision.
- **Status:** ACTIVE_DOCUMENTATION (Describes target state).
- **Owner:** Product Lead / Member 6.
- **Dependencies:** None.
- **Used By:** All team members.
- **Is Active?** YES.
- **Is Duplicated?** PARTIALLY DUPLICATED by `docs/ARCHITECTURE.md`.
- **Is Historical?** NO.
- **Safe to Ignore?** NO, but treat as TARGET architecture, not CURRENT reality.

### `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`
- **Type:** Generated Markdown Artifact (720 KB)
- **Purpose:** Single concatenated file containing full documentation for ingestion into LLM context windows.
- **Current Role:** External AI prompt context.
- **Status:** GENERATED_ARTIFACT.
- **Owner:** Generated by `tools/build_all_in_one_context.py`.
- **Dependencies:** Individual markdown files in `docs/`.
- **Used By:** External AI chats.
- **Is Active?** GENERATED / DERIVATIVE.
- **Is Duplicated?** YES (100% duplicate of underlying docs).
- **Is Historical?** NO.
- **Safe to Ignore?** YES for codebase work; can be regenerated on demand.

### `problem statement #1/SIH26034_Dossier.md`
- **Type:** Markdown Reference Document (91 KB)
- **Purpose:** In-depth initial domain analysis of problem statement SIH26034.
- **Current Role:** Historical reference dossier.
- **Status:** HISTORICAL.
- **Owner:** Initial research team.
- **Dependencies:** None.
- **Used By:** Background research.
- **Is Active?** NO (Superseded by `docs/01_PROBLEM_STATEMENT/`).
- **Is Duplicated?** PARTIALLY.
- **Is Historical?** YES.
- **Safe to Ignore?** YES.
