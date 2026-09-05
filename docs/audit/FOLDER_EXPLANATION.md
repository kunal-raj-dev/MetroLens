# MetroLens AI — Comprehensive Folder Explanation Guide
**Audience:** Developers, new contributors, and engineers taking over or navigating the repository.  
**Audit Baseline Date:** 2026-09-05  
**Core Rule:** Every folder is explained based strictly on what is physically inside it today.

---

## 1. Top-Level Folder Inventory

### 1. `apps/`
- **Purpose:** Host the runnable application frontends, API services, and async workers for deployment.
- **Actual Content:** 
  - `apps/api/`: FastAPI web server with 3 mocked endpoints returning static JSON.
  - `apps/web/`: Next.js 14 frontend containing a single static text page; `node_modules` does not exist.
  - `apps/worker/`: Asynchronous execution worker stub (62 lines).
- **Status:** SCAFFOLD / PARTIALLY ACTIVE.
- **Who Uses It:** Member 4 (Backend API & Worker), Member 5 (Web UI).
- **Is It Currently Important?** YES for understanding integration endpoints, but DO NOT expect working end-to-end functionality. None of these apps currently invoke real OCR or rules.

### 2. `packages/`
- **Purpose:** House the reusable, decoupled domain subsystems of the MetroLens monorepo.
- **Actual Content:** 9 packages:
  - `packages/ocr/`: **FULLY IMPLEMENTED & TESTED**. Contains the DBNet++ and SVTR ONNX inference engine, script routing, preprocessing, and the `OCRService` adapter.
  - `packages/shared/`: **IMPLEMENTED**. Contains canonical Pydantic domain models (`InspectionResult`, `OCRObservation`, `RuleEvaluation`, etc.).
  - `packages/calibration/`, `evidence/`, `extraction/`, `measurement/`, `reporting/`, `rules-engine/`, `vision/`: **SCAFFOLDS**. Each contains only a minimal `__init__.py` (30–70 lines) with stub mathematical calculations and a basic smoke test.
- **Status:** MIXED (OCR & Shared: ACTIVE; 7 packages: SCAFFOLD).
- **Who Uses It:** All team members (M1 owns `ocr`, M2 owns `calibration/vision/measurement`, M3 owns `rules-engine/extraction`, M4 owns `reporting`, M6 tests across all).
- **Is It Currently Important?** CRITICAL. `packages/ocr` and `packages/shared` are the operational heart of the repository today.

### 3. `data/`
- **Purpose:** Store raw packaging photographs, annotations, benchmark datasets, and manifests.
- **Actual Content:**
  - `data/synthetic/regression/`: 8 synthetic test PNG images and a metadata manifest.
  - `data/manifests/`: JSON/YAML schemas declaring the 35-SKU retail target.
  - `data/raw/real/`: **COMPLETELY EMPTY**. Zero physical packaging photos.
  - `data/annotations/ocr/`: **COMPLETELY EMPTY**. Zero ground-truth annotation files.
- **Status:** MIXED (Synthetic: ACTIVE; Real Data: BLOCKED / EMPTY).
- **Who Uses It:** Member 1 (OCR validation), Member 6 (Data curation & benchmarking).
- **Is It Currently Important?** CRITICAL. The complete absence of real packaging data is the single largest empirical vulnerability of the project.

### 4. `models/`
- **Purpose:** Version-controlled storage for machine learning model weights, configs, and manifests.
- **Actual Content:** 
  - `models/weights/ocr/`: 3 genuine ONNX model weights files:
    1. `det/ch_PP-OCRv3_det_infer.onnx` (2.43 MB) — DBNet++ text detector.
    2. `rec_en/ch_PP-OCRv3_rec_infer.onnx` (10.69 MB) — SVTR Latin/English alphanumeric recognizer.
    3. `rec_hi/rec.onnx` (8.98 MB) — SVTR Devanagari Hindi recognizer.
    4. `rec_hi/dict.txt` (167 characters) — Devanagari character dictionary.
  - `models/manifest.yaml`: Machine-readable model manifest specifying file paths, SHA-256 hashes, and runtime settings.
- **Status:** ACTIVE / VERIFIED.
- **Who Uses It:** Member 1 (`packages/ocr`), Member 6 (Model deployment & caching).
- **Is It Currently Important?** CRITICAL. Without these files, OCR inference fails immediately.

### 5. `METROLENS_LEGAL_SOURCE_PACK/`
- **Purpose:** Primary repository of authoritative sovereign legal sources for Indian Legal Metrology.
- **Actual Content:** 74 authentic government legal PDFs (Legal Metrology Act 2009, Jan Vishwas Acts 2023 & 2026, Packaged Commodities Rules 2011 with 21 official amendments, advisories, and enforcement guidelines), plus SHA-256 checksum manifests and timelines in `00_SOURCE_INDEX/`.
- **Status:** ACTIVE / IMMUTABLE ARCHIVE.
- **Who Uses It:** Member 3 (Legal Rules Lead), statutory auditors, jury presentation reviewers.
- **Is It Currently Important?** HIGH. This is the unassailable legal foundation of the project proving that regulatory claims are rooted in sovereign gazettes.

### 6. `benchmarks/`
- **Purpose:** Measure and record OCR latency, throughput, memory footprint, and character accuracy.
- **Actual Content:**
  - `benchmarks/ocr/chunk2/`: CPU sweep scripts and results across thread configurations.
  - `benchmarks/ocr/chunk3/`: Preprocessing filter benchmarks and error visualizations on synthetic specimens.
  - `benchmarks/ocr/chunk4/`: Service adapter latency, memory profiling (296 MB peak), and concurrency results (8.81 req/s).
  - Other subdirectories (`datasets`, `protocols`, `reports`, `results`, `runs`): Contain only `.gitkeep`.
- **Status:** ACTIVE (for OCR synthetic benchmarks); SCAFFOLD (for general benchmarking).
- **Who Uses It:** Member 1, Member 6.
- **Is It Currently Important?** HIGH for validating OCR CPU performance. Not yet applicable to real packaging accuracy.

### 7. `CURRENT_STATE/`
- **Purpose:** Provide machine-readable and human-readable baselines of what was achieved in each execution chunk.
- **Actual Content:** Status reports (`CHUNK_1_STATUS.md` to `CHUNK_4_STATUS.md`), technical baselines (`CHUNK_2_BASELINE.md` to `CHUNK_4_BASELINE.md`), hardware/dependency snapshots, and `PROJECT_SNAPSHOT.md`.
- **Status:** ACTIVE / CANONICAL FOR PROGRESS TRACKING.
- **Who Uses It:** AI agents, lead developers, orchestrator.
- **Is It Currently Important?** CRITICAL. Always read `PROJECT_SNAPSHOT.md` and `CHUNK_4_STATUS.md` to know where the project stands before writing new code.

### 8. `AI_CONTEXT/`
- **Purpose:** Context boundary memory for AI-assisted development across sprint chunks.
- **Actual Content:** Execution run logs (`RUN_LOGS/`), structured experiment folders (`EXPERIMENTS/`), and formal cross-member handoffs (`HANDOFFS/`) for Chunks 1, 2, 3, and 4.
- **Status:** ACTIVE / CANONICAL AUDIT TRAIL.
- **Who Uses It:** AI agents resuming context.
- **Is It Currently Important?** HIGH for AI agents; moderate for human developers. It documents why specific engineering decisions (like switching from RapidOCR to direct ONNX) were made.

### 9. `docs/`
- **Purpose:** Comprehensive repository architecture, legal rules matrix, requirements, and individual work plans.
- **Actual Content:** 123+ markdown files divided across 18 numbered thematic folders (`00_PROJECT_CHARTER` through `17_CLAIMS`), `team/` work plans, `audit/` reports, and 25 root-level documents.
- **Status:** ACTIVE DOCUMENTATION / PARTIALLY DIVERGENT.
- **Who Uses It:** Entire team, hackathon evaluators, AI agents.
- **Is It Currently Important?** HIGH for architecture guidance, but CAUTION: many documents describe the desired final state as if it already exists. Always cross-check against actual code in `packages/`.

### 10. `tests/`
- **Purpose:** Repository-level integration, regression, and verification test suites.
- **Actual Content:**
  - `tests/integration/test_ocr_service_integration.py`: 16 comprehensive service integration tests.
  - `tests/unit/`: 8 test files covering OCR components, preprocessing, types, offline execution, and repository verification scripts.
  - Subdirectories `e2e/`, `fixtures/`, `rules/`, `security/`, `vision/`: Empty placeholders (`.gitkeep`).
- **Status:** ACTIVE / PASSING (67 tests in `tests/`, 22 tests in packages/apps = 89 total).
- **Who Uses It:** Entire team, Member 6 (CI/QA).
- **Is It Currently Important?** CRITICAL. Running `python -m pytest` executes this suite and guarantees OCR regression safety.

### 11. `scripts/`
- **Purpose:** Automation and repository integrity verification scripts.
- **Actual Content:** `scripts/verification/` contains 6 Python scripts that check claims status, legal source hashes, rule schema integrity, dataset manifests, and repository invariants.
- **Status:** ACTIVE.
- **Who Uses It:** Pytest (`test_verification_pipeline.py`), Member 6.
- **Is It Currently Important?** HIGH. Ensures claims made in docs are not fabricated.

### 12. `tools/`
- **Purpose:** Ad-hoc developer utilities and maintenance scripts.
- **Actual Content:**
  - `tools/build_all_in_one_context.py`: Generates the massive `METROLENS_AI_ALL_IN_ONE_DOCS.md` file.
  - `tools/validate_dataset_manifest.py`: Validates dataset manifest syntax.
  - `tools/verify_ocr_run.py`: Runs OCR on a sample image.
  - `tools/visualize_ocr_debug.py`: Plots bounding boxes on images.
  - `tools/legal_sources/collect_official_legal_sources.py`: Downloader for government PDFs.
- **Status:** ACTIVE UTILITIES.
- **Who Uses It:** Developers, Member 1, Member 6.
- **Is It Currently Important?** MODERATE. Useful for local debugging and maintenance.

### 13. `infra/`
- **Purpose:** Infrastructure as code, containerization, and database scripts.
- **Actual Content:** 
  - `infra/db/init.sql`: PostgreSQL 16 table creation schema.
  - `infra/docker/Dockerfile.api` & `Dockerfile.web`: Docker build specifications.
  - `infra/deployment/`, `monitoring/`, `storage/`: Empty directories (`.gitkeep`).
- **Status:** SCAFFOLD.
- **Who Uses It:** Member 4 (DB/API), Member 6 (Docker/Hosting).
- **Is It Currently Important?** MODERATE. Required when standing up containers or PostgreSQL.

### 14. `regulations/`
- **Purpose:** Machine-readable regulatory definitions and categorized statutory archives.
- **Actual Content:** `source_registry.yaml` (canonical YAML metadata for legal acts and amendments). The 10 subdirectories (`amendments`, `current`, `exemptions`, etc.) are currently empty.
- **Status:** ACTIVE REGISTRY / SCAFFOLD FOLDERS.
- **Who Uses It:** Member 3, verification scripts.
- **Is It Currently Important?** HIGH. `source_registry.yaml` is validated by integrity tests.

### 15. `rules/`
- **Purpose:** Formal JSON schemas and proposed machine-readable rule files.
- **Actual Content:** 
  - `rules/schema/`: `rule.schema.json`, `evidence.schema.json`, `applicability.schema.json`.
  - `rules/proposed/`: Candidate YAML rules for Rule 6 and Rule 7.
- **Status:** SPECIFICATION / CANDIDATE RULES.
- **Who Uses It:** Member 3.
- **Is It Currently Important?** HIGH for designing the rules engine logic.

### 16. `research/`
- **Purpose:** Background statutory analyses, academic paper notes, and prior art research.
- **Actual Content:** 9 markdown synthesis packs (`PACK_A_OFFICIAL_PS.md` through `PACK_G_SIH_FRAMEWORK.md`).
- **Status:** HISTORICAL RESEARCH / BACKGROUND.
- **Who Uses It:** All members during initial concept design.
- **Is It Currently Important?** LOW for active coding; MODERATE for jury question preparation.

### 17. `experiments/`
- **Purpose:** Intended scratchpad for experimental scripts across CV, dewarping, and extraction.
- **Actual Content:** 8 empty subdirectories (`calibration`, `dewarping`, `end_to_end`, etc.), each containing only `.gitkeep`.
- **Status:** EMPTY SCAFFOLD.
- **Who Uses It:** Nobody currently.
- **Is It Currently Important?** NO. Safe to ignore.

### 18. `assets/`
- **Purpose:** Intended storage for pitch decks, demo media, and diagrams.
- **Actual Content:** 5 empty subdirectories (`demo`, `diagrams`, `presentation`, etc.), each containing only `.gitkeep`.
- **Status:** EMPTY SCAFFOLD.
- **Who Uses It:** Member 5, Member 6.
- **Is It Currently Important?** NO. Safe to ignore until presentation materials are created.

### 19. `pptx/`
- **Purpose:** SIH official presentation deck template.
- **Actual Content:** `SIH2026-IDEA-Presentation-Format.pptx` (924 KB).
- **Status:** ASSET / TEMPLATE.
- **Who Uses It:** Pitch presenter / team lead.
- **Is It Currently Important?** LOW for software engineering; HIGH for competition submission.

### 20. `problem statement #1/`
- **Purpose:** Historical problem analysis dossier generated at project inception.
- **Actual Content:** `SIH26034_Dossier.md`, `SIH26034_Dossier.html`, `SIH26034_Dossier.pdf`, and `generate_dossier.py`.
- **Status:** HISTORICAL REFERENCE.
- **Who Uses It:** Historical archive.
- **Is It Currently Important?** LOW. Superseded by `docs/01_PROBLEM_STATEMENT/`. Safe to ignore.

### 21. `ALL-IN-ONE context/`
- **Purpose:** Concatenated mega-file containing full documentation for ingestion by LLMs with large context windows.
- **Actual Content:** `METROLENS_AI_ALL_IN_ONE_DOCS.md` (720 KB).
- **Status:** GENERATED ARTIFACT / CLUTTER.
- **Who Uses It:** External AI prompts.
- **Is It Currently Important?** LOW. Prone to becoming stale whenever individual docs change. Regenerable via `tools/build_all_in_one_context.py`.
