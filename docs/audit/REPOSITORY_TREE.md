# MetroLens AI — Comprehensive Repository Tree & Directory Map
**Audit Baseline Date:** 2026-09-05  
**Repository Root:** `c:\Users\kunal\Desktop\MetroLens`  
**Git Branch:** `kunal-member-1-work` (Commit `f25d15a`)

---

## 1. Directory Structure Map

```
MetroLens/
├── .github/                                # Repository management & GitHub templates
│   └── ISSUE_TEMPLATE/                     # Issue templates (bug, chore, config, doc, feature, legal, research)
│       └── [7 YAML template files]
│   # NOTE: .github/workflows/ DOES NOT EXIST (CI is planned, not implemented)
│
├── AI_CONTEXT/                             # AI session memory, chunk execution logs, experiments & handoffs
│   ├── AUDITS/                             # Audit summaries for AI agents
│   │   └── FULL_PROJECT_AUDIT.md
│   ├── EXPERIMENTS/                        # Experimental records across implementation chunks
│   │   ├── CHUNK_1_OCR_MODEL_SELECTION/    # OCR architecture spike (PaddleOCR vs EasyOCR vs Tesseract)
│   │   ├── CHUNK_2_OCR_ENGINE/             # Direct ONNX runtime engine design and model verification
│   │   ├── CHUNK_3_REAL_DATA/              # Real data provenance audit and OCR preprocessing evaluation
│   │   └── CHUNK_4_OCR_INTEGRATION/        # Service adapter, monorepo packaging, and shared contracts
│   ├── HANDOFFS/                           # Cross-chunk and cross-member formal handoff contracts
│   │   ├── CHUNK_1_TO_CHUNK_2.md ... CHUNK_4_TO_CHUNK_5.md
│   │   └── M1_TO_M2_CHUNK4.md ... M1_TO_M6_CHUNK3.md
│   ├── RUN_LOGS/                           # Granular execution step logs for Chunks 1–4
│   │   └── CHUNK_1_RUN_LOG.md ... CHUNK_4_RUN_LOG.md
│   └── PROJECT_CONTEXT.md                  # Comprehensive AI context baseline
│
├── ALL-IN-ONE context/                     # Generated context file repository
│   └── METROLENS_AI_ALL_IN_ONE_DOCS.md     # 720KB concatenated documentation dump
│
├── apps/                                   # Runnable application entrypoints (Scaffolds)
│   ├── api/                                # FastAPI backend service
│   │   ├── main.py                         # Application entrypoint with 3 mocked endpoints
│   │   ├── pyproject.toml                  # API packaging metadata
│   │   ├── README.md                       # API service documentation
│   │   └── tests/                          # API smoke tests
│   │       └── test_api_smoke.py           # 2 tests verifying /health and /api/v1/inspections
│   ├── web/                                # Next.js web application frontend
│   │   ├── src/app/                        # Next.js App Router files
│   │   │   ├── layout.tsx                  # Root HTML shell
│   │   │   └── page.tsx                    # 40-line static text homepage
│   │   ├── package.json                    # Frontend dependencies (Next 14, React 18, Tailwind 3)
│   │   ├── tsconfig.json                   # TypeScript compiler configuration
│   │   ├── next.config.mjs                 # Next.js build configuration
│   │   └── README.md                       # Web application documentation
│   │   # NOTE: node_modules does not exist on disk
│   └── worker/                             # Asynchronous pipeline worker
│       ├── main.py                         # 62-line stub worker class
│       ├── pyproject.toml                  # Worker packaging metadata
│       ├── README.md                       # Worker documentation
│       └── tests/                          # Worker smoke tests
│           └── test_worker_smoke.py        # 2 tests verifying worker instantiation
│
├── assets/                                 # Static project presentation assets (All subdirs empty .gitkeep)
│   ├── demo/                               # Empty placeholder for demo videos/scripts
│   ├── diagrams/                           # Empty placeholder for exported diagrams
│   ├── presentation/                       # Empty placeholder for pitch slide decks
│   ├── sample_packages/                    # Empty placeholder for sample product images
│   └── screenshots/                        # Empty placeholder for UI screenshots
│
├── benchmarks/                             # Performance, latency, and accuracy benchmark harnesses
│   ├── ocr/                                # OCR-specific empirical benchmarks
│   │   ├── chunk2/                         # Multi-thread CPU sweep & memory stability harness
│   │   │   ├── results.json, debug_visual.png, run_chunk2_benchmark.py
│   │   ├── chunk3/                         # Preprocessing evaluation on 8 synthetic specimens
│   │   │   ├── baseline_results.json, final_results.json, preprocessing_results.json
│   │   │   ├── dataset_manifest.json, run_chunk3_benchmark.py, visualize_errors.py
│   │   └── chunk4/                         # Service adapter latency & concurrency benchmarks
│   │       ├── integration_results.json, benchmark_config.json, run_chunk4_integration_benchmark.py
│   ├── datasets/                           # Empty placeholder directory (.gitkeep)
│   ├── protocols/                          # Empty placeholder directory (.gitkeep)
│   ├── reports/                            # Empty placeholder directory (.gitkeep)
│   ├── results/                            # Empty placeholder directory (.gitkeep)
│   └── runs/                               # Empty placeholder directory (.gitkeep)
│
├── CURRENT_STATE/                          # Active project status snapshots and baselines
│   ├── CHUNK_1_STATUS.md ... CHUNK_4_STATUS.md  # Status files for completed Chunks 1 to 4
│   ├── CHUNK_2_BASELINE.md ... CHUNK_4_BASELINE.md # Technical baseline parameters
│   ├── DEPENDENCY_SNAPSHOT.md              # Snapshot of installed Python packages
│   ├── ENVIRONMENT_SNAPSHOT.md             # Hardware and OS snapshot
│   ├── GIT_STATE.md                        # Branch and commit snapshot
│   └── PROJECT_SNAPSHOT.md                 # Current authoritative status summary
│
├── data/                                   # Datasets, ground-truth annotations, and manifests
│   ├── annotations/                        # Ground-truth annotations
│   │   └── ocr/                            # Empty directory (.gitkeep)
│   ├── manifests/                          # Machine-readable dataset manifests
│   │   ├── ground_truth_benchmark.json     # Ground-truth benchmark JSON schema & empty record list
│   │   ├── manifest.yaml                   # High-level dataset registry (declares DS-RETAIL-PILOT-001)
│   │   └── real_packaging_manifest.json    # Manifest declaring 35-SKU target (0 present on disk)
│   ├── processed/                          # Processed dataset derivatives
│   │   └── chunk3/                         # Empty directory (.gitkeep)
│   ├── raw/                                # Raw photographic images
│   │   └── real/                           # EMPTY DIRECTORY (0 authentic packaging images)
│   └── synthetic/                          # Procedural synthetic regression specimens
│       └── regression/                     # 8 synthetic packaging PNG images (SYNTH-01 to SYNTH-08)
│           └── manifest.json               # Metadata & ground truth for the 8 synthetic images
│
├── docs/                                   # Architectural, product, and legal documentation (123+ files)
│   ├── 00_PROJECT_CHARTER/                 # Scope, MVP definitions, non-goals, glossary
│   ├── 01_PROBLEM_STATEMENT/               # SIH26034 problem analysis & requirement traceability
│   ├── 02_LEGAL_AUTHORITY/                 # Source hierarchy, legal changelogs, verified rule catalogs
│   ├── 03_PRODUCT_REQUIREMENTS/            # Functional & non-functional requirements, user journeys
│   ├── 04_ARCHITECTURE/                    # System, AI pipeline, rule engine, and data flow architecture
│   ├── 05_AI_VISION/                       # OCR strategy, calibration, font measurement, quality gate
│   ├── 06_RULE_ENGINE/                     # Statutory rules, exceptions, and declaration schemas
│   ├── 07_DATA/                            # Data collection protocol, synthetic data generation, manifests
│   ├── 08_EVIDENCE/                        # Cryptographic DAG, chain-of-custody, evidence models
│   ├── 09_SECURITY_PRIVACY/                # Threat modeling, upload defenses, data lifecycle
│   ├── 10_TESTING/                         # Testing strategy, verification test plans
│   ├── 11_JUDGING/                         # Hackathon evaluation criteria, jury presentation guidelines
│   ├── 12_PRIOR_ART/                       # Competitive analysis and differentiation matrix
│   ├── 13_BUILD_PLAN/                      # Build sequences and milestones
│   ├── 14_SUBMISSION/                      # Implementation claim audits, artifact registries
│   ├── 15_DECISIONS/                       # Architectural Decision Records (ADR-001 to ADR-017)
│   ├── 16_LIMITATIONS/                     # Known technical and operational constraints
│   ├── 17_CLAIMS/                          # Anti-hallucination claims register
│   ├── audit/                              # Project ground-truth audit artifacts (This audit)
│   ├── legal_research/                     # Legal research dossiers and statutory analyses
│   ├── team/                               # 6-member work plans, checklists, and execution overviews
│   └── [25 standalone root markdown files] # ARCHITECTURE.md, PRODUCT_BLUEPRINT.md, etc.
│
├── experiments/                            # Scratch experimental directories (All subdirs empty .gitkeep)
│   ├── calibration/, dewarping/, end_to_end/, extraction/
│   ├── font_measurement/, ocr/, pdp_detection/, rules/
│
├── infra/                                  # Deployment, containerization, and infrastructure assets
│   ├── db/                                 # Database scripts
│   │   └── init.sql                        # PostgreSQL 16 table initialization DDL
│   ├── docker/                             # Docker build definitions
│   │   ├── Dockerfile.api                  # Python FastAPI container build definition
│   │   └── Dockerfile.web                  # Next.js Node container build definition
│   ├── deployment/                         # Empty directory (.gitkeep)
│   ├── monitoring/                         # Empty directory (.gitkeep)
│   └── storage/                            # Empty directory (.gitkeep)
│
├── METROLENS_LEGAL_SOURCE_PACK/            # 74 Authentic Sovereign Legal Documents (PDFs)
│   ├── 00_SOURCE_INDEX/                    # Indexes, checksums, coverage matrices, logs
│   ├── 01_PRIMARY_ACTS/                    # 5 PDFs (Legal Metrology Act 2009, Jan Vishwas 2023, 2026)
│   ├── 02_CURRENT_CONSOLIDATED_RULES/      # 1 PDF (Packaged Commodities Rules 2011 base)
│   ├── 03_PACKAGED_COMMODITIES_AMENDMENTS/ # 21 PDFs (Amendments 2011 through 2024 organized by year)
│   ├── 04_OFFICIAL_NOTIFICATIONS/          # 8 PDFs (Advisory notifications & gazette orders)
│   ├── 05_OFFICIAL_FAQ_GUIDANCE/           # 6 PDFs (Department of Consumer Affairs guidance)
│   ├── 06_OFFICIAL_ENFORCEMENT_INSPECTION/ # 7 PDFs (Inspection manuals, compounding orders)
│   ├── 07_E_MAAP/                          # 3 PDFs (National Portal circulars & user manuals)
│   ├── 08_STATE_LEGAL_METROLOGY/           # 12 PDFs (State-specific enforcement guidelines)
│   ├── 09_SUPPORTING_SECONDARY_SOURCES/    # 3 PDFs (Law commission & legal treatises)
│   └── 99_ARCHIVE/                         # 8 PDFs + scratch scripts from automated harvesting
│
├── models/                                 # ML model registry, configs, and ONNX weights
│   ├── cards/                              # Model metadata cards
│   ├── configs/                            # Model configuration files
│   ├── registry/                           # Model registry files
│   ├── manifest.yaml                       # Model manifest declaring SHA-256 and runtime settings
│   └── weights/ocr/                        # Production ONNX model files for OCR
│       ├── det/
│       │   └── ch_PP-OCRv3_det_infer.onnx  # DBNet++ text detector (2.43 MB, SHA: 3439588c...)
│       ├── rec_en/
│       │   └── ch_PP-OCRv3_rec_infer.onnx  # SVTR-EN Latin/English recognizer (10.69 MB, SHA: 897a3ede...)
│       └── rec_hi/
│           ├── rec.onnx                    # SVTR-HI Devanagari recognizer (8.98 MB, SHA: 43df175f...)
│           └── dict.txt                    # 167-character Devanagari dictionary
│
├── packages/                               # Modular Python application packages (Monorepo core)
│   ├── calibration/                        # Metric scale factor calculation (SCAFFOLD)
│   │   ├── src/nirikshak_calibration/      # __init__.py (compute_scale_factor stub, 67 lines)
│   │   └── tests/                          # test_calibration_smoke.py (2 tests)
│   ├── evidence/                           # Evidence graph and hashing (SCAFFOLD)
│   │   ├── src/nirikshak_evidence/         # __init__.py (create_evidence_item stub, 43 lines)
│   │   └── tests/                          # test_evidence_smoke.py (2 tests)
│   ├── extraction/                         # Semantic declaration parsing (SCAFFOLD)
│   │   ├── src/nirikshak_extraction/       # __init__.py (MRP regex extractor stub, 47 lines)
│   │   └── tests/                          # test_extraction_smoke.py (1 test)
│   ├── measurement/                        # Physical font & area dimensions (SCAFFOLD)
│   │   ├── src/nirikshak_measurement/      # __init__.py (calculate_font_height stub, 44 lines)
│   │   └── tests/                          # test_measurement_smoke.py (3 tests)
│   ├── ocr/                                # Perception OCR Subsystem (FULLY IMPLEMENTED)
│   │   ├── src/nirikshak_ocr/              # 11 modules (config, detector, engine, errors,
│   │   │                                   # evaluation, preprocessing, recognizer, router,
│   │   │                                   # service, types, utils)
│   │   └── tests/                          # test_ocr_smoke.py (1 test)
│   ├── reporting/                          # Inspection dossier PDF generation (SCAFFOLD)
│   │   ├── src/nirikshak_reporting/        # __init__.py (DossierGenerator stub, 41 lines)
│   │   └── tests/                          # test_reporting_smoke.py (1 test)
│   ├── rules-engine/                       # Statutory rule evaluation state machine (SCAFFOLD)
│   │   ├── src/nirikshak_rules_engine/     # __init__.py (MRP rule evaluator stub, 39 lines)
│   │   └── tests/                          # test_rules_engine_smoke.py (2 tests)
│   ├── shared/                             # Canonical domain contracts and primitives (IMPLEMENTED)
│   │   ├── src/nirikshak_shared/models/    # contracts.py (Pydantic DTOs), primitives.py (Enums)
│   │   └── tests/                          # test_contracts.py (5 tests)
│   └── vision/                             # Image quality gating & segmentation (SCAFFOLD)
│       ├── src/nirikshak_vision/           # __init__.py (check_image_quality stub, 71 lines)
│       └── tests/                          # test_vision_smoke.py (1 test)
│
├── pptx/                                   # SIH presentation slide templates
│   └── SIH2026-IDEA-Presentation-Format.pptx # 924KB PPTX template
│
├── problem statement #1/                   # Problem Statement SIH26034 reference dossier
│   ├── SIH26034_Dossier.html               # 126KB HTML rendered dossier
│   ├── SIH26034_Dossier.md                 # 91KB Markdown specification
│   ├── SIH26034_Dossier.pdf                # 805KB PDF document
│   └── scripts/generate_dossier.py         # 96KB Python dossier generator script
│
├── regulations/                            # Machine-readable legal registry & category folders
│   ├── source_registry.yaml                # Master legal source registry (1.2.0)
│   └── [10 empty categorised subdirectories] # amendments/, current/, exemptions/, etc.
│
├── research/                               # Background technical and statutory research
│   ├── datasets/PACK_E_DATASETS.md
│   ├── models/PACK_F_AI_STACK.md
│   ├── official_sources/PACK_A_OFFICIAL_PS.md ... PACK_C_MEASUREMENT_STANDARDS.md
│   ├── prior_art/PACK_D_PRIOR_ART.md
│   ├── research_gaps/RESEARCH_GAPS_REGISTER.md
│   ├── secondary_sources/SECONDARY_ANALYSIS.md
│   ├── sih/PACK_G_SIH_FRAMEWORK.md
│   └── [6 empty subdirectories]
│
├── rules/                                  # Machine-readable rule schemas and YAML proposals
│   ├── proposed/                           # Candidate rule YAMLs (Rule 6, Rule 7, templates)
│   └── schema/                             # JSON Schemas (rule, evidence, applicability)
│
├── scripts/                                # Verification and repository validation scripts
│   └── verification/                       # Subordinate integrity scripts invoked by pytest
│       ├── verify_claims.py                # Enforces anti-hallucination claims status
│       ├── verify_dataset_manifest.py      # Checks dataset manifests
│       ├── verify_legal_sources.py         # Validates legal source hashes
│       ├── verify_report_provenance.py     # Validates reporting integrity
│       ├── verify_repository_integrity.py  # Master invariant verification script
│       └── verify_rule_registry.py         # Checks rule schema references
│
├── tests/                                  # Root test suite (89 passing tests across repo)
│   ├── integration/                        # Integration tests
│   │   └── test_ocr_service_integration.py # 16 tests verifying OCRService adapter & contracts
│   ├── unit/                               # Unit test suite
│   │   ├── test_ocr_chunk3_hardening.py    # 5 tests
│   │   ├── test_ocr_chunk3_regression.py   # 4 tests
│   │   ├── test_ocr_engine_comprehensive.py# 15 tests
│   │   ├── test_ocr_evaluation.py          # 6 tests
│   │   ├── test_ocr_offline.py             # 1 test
│   │   ├── test_ocr_preprocessing.py       # 9 tests
│   │   ├── test_ocr_types_config.py        # 6 tests
│   │   └── test_verification_pipeline.py   # 5 tests (executes scripts/verification/*.py)
│   └── [empty dirs: e2e/, fixtures/, rules/, security/, vision/]
│
├── tools/                                  # Operational maintenance and verification CLI tools
│   ├── build_all_in_one_context.py         # Script that concatenates docs into ALL-IN-ONE
│   ├── validate_dataset_manifest.py        # CLI for checking dataset manifests
│   ├── verify_ocr_run.py                   # Ad-hoc verification script for OCR engine
│   ├── visualize_ocr_debug.py              # Visual bounding-box debugger for OCR outputs
│   └── legal_sources/
│       └── collect_official_legal_sources.py # Script used to download sovereign legal PDFs
│
├── .env.example                            # Template environment configuration
├── .gitignore                              # Git exclusion patterns
├── CONTRIBUTING.md                         # Contribution and code review guidelines
├── docker-compose.yml                      # Docker Compose orchestration definition
├── GLOBAL_TEAM_WORKFLOW.md                 # 72KB workflow specification for 6 members
├── LICENSE                                 # Apache 2.0 software license
├── Makefile                                # Development shortcuts
├── MVP_UNIFIED_WORKFLOW_GRAPH.md           # 34KB end-to-end mermaid architecture graph
├── pytest.ini                              # Pytest testpath, pythonpath, and marker settings
├── README.md                               # Primary project README
├── requirements.txt                        # Top-level Python dependencies
└── SECURITY.md                             # Security disclosure and vulnerability policy
```

---

## 2. Directory Classification Breakdown

| Category | Directories | Actual Role & Functional Reality |
| :--- | :--- | :--- |
| **Fully Implemented Source** | `packages/ocr/`, `packages/shared/` | Contains production-grade, tested Python source code. |
| **Scaffolded Source** | `packages/calibration/`, `packages/evidence/`, `packages/extraction/`, `packages/measurement/`, `packages/reporting/`, `packages/rules-engine/`, `packages/vision/`, `apps/api/`, `apps/worker/`, `apps/web/` | Skeletons containing minimal stubs (30–70 lines) or static HTML. Untested with real workloads. |
| **Test Suites** | `tests/unit/`, `tests/integration/`, `packages/*/tests/`, `apps/*/tests/` | 89 automated tests passing. 67 are OCR-focused; 22 are smoke stubs. |
| **Model Assets** | `models/weights/ocr/` | Contains 3 genuine ONNX weights files totaling 22.1 MB plus Devanagari dictionary. |
| **Data (Synthetic)** | `data/synthetic/regression/` | 8 valid synthetic FMCG test specimen images with ground truth. |
| **Data (Real Packaging)**| `data/raw/real/`, `data/annotations/ocr/` | Completely EMPTY. Zero authentic packaging images or annotations exist on disk. |
| **Legal Source Pack** | `METROLENS_LEGAL_SOURCE_PACK/` | 74 authentic sovereign Indian government legal PDFs, indexed and hashed. |
| **Documentation** | `docs/`, `research/`, `problem statement #1/` | 150+ markdown files detailing architecture, rules, user journeys, and claims. |
| **AI Session Context** | `AI_CONTEXT/`, `CURRENT_STATE/` | Complete history of Chunks 1–4 execution logs, handoffs, and baseline snapshots. |
| **Empty Scaffolding** | `assets/*/`, `experiments/*/`, `regulations/*/` (subdirs) | Empty directories containing only `.gitkeep` files. |
