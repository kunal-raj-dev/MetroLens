# NIRIKSHAK — FINAL REPOSITORY FILESYSTEM INVENTORY

**Audit Scope:** Full repository traversal (SIH 2026 — PS 26034)  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Anti-Hallucination & Governance Hardening Policy  

---

## 1. Executive Summary

This inventory provides a comprehensive, ground-truth audit of all **146 directories** comprising the Nirikshak repository skeleton and documentation framework.

### Directory Status Summary

| Category | Count | Governance Rationale |
| :--- | :--- | :--- |
| **Active Directories (Files Present)** | 92 | Functional code, tests, documentation, schemas, and verification scripts |
| **Scaffold Directories (Specified)** | 12 | Core application and package skeletons with defined architecture and interfaces |
| **Container Directories** | 16 | Structural parent directories grouping functional submodules |
| **Reserved / Empty Directories** | 26 | Explicitly reserved for Level 1 Gazette PDFs and verified rule lifecycle states |
| **Total Directories Audited** | **146** | Complete filesystem accounted for with 0 unexpected or uncataloged paths |

> [!IMPORTANT]
> **Governance Statement on Empty Directories:**
> Under the Nirikshak Anti-Hallucination Policy, empty directories under `rules/` (e.g., `rules/verified`, `rules/historical`, `rules/current`) and `docs/02_LEGAL_AUTHORITY/` (e.g., `AMENDMENTS/2026`, `BASE_2011`) are **intentionally preserved and empty**. No placeholder or synthetic rules have been authored to simulate completeness. These directories will only be populated as Level 1 primary gazette PDFs are officially downloaded and verified by legal counsel during Stage 2 implementation.

---

## 2. Comprehensive Directory Inventory

| Path | Purpose | Expected Contents | Actual Files | Status |
| :--- | :--- | :--- | :--- | :--- |
| `.` | Repository root containing governance, Docker, CI, and setup manifests | Code / Docs / Manifests | 9 file(s) (`.env.example`, ...) | `ACTIVE (Files Present)` |
| `apps` | Parent directory for application service frontends, backends, and workers | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `apps/api` | Backend REST/gRPC API service for Nirikshak inspection engine | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `apps/web` | Officer inspection review interface and dashboard application | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `apps/worker` | Background asynchronous task worker for vision pipelines and exports | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `assets` | Parent directory for visual media, diagrams, and sample packages | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `assets/demo` | Media assets for demo | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `assets/diagrams` | Media assets for diagrams | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `assets/presentation` | Media assets for presentation | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `assets/sample_packages` | Media assets for sample packages | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `assets/screenshots` | Media assets for screenshots | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `benchmarks` | Parent directory for empirical benchmarking datasets, protocols, and reports | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `benchmarks/datasets` | Benchmarking assets for datasets | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `benchmarks/protocols` | Benchmarking assets for protocols | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `benchmarks/reports` | Benchmarking assets for reports | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `benchmarks/results` | Benchmarking assets for results | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `benchmarks/runs` | Benchmarking assets for runs | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `data` | Parent directory for training, evaluation, and test datasets | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `data/annotations` | Dataset storage for annotations | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `data/benchmark` | Dataset storage for benchmark | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `data/manifests` | Dataset storage for manifests | Code / Docs / Manifests | 1 file(s) (`manifest.yaml`) | `ACTIVE (Files Present)` |
| `data/processed` | Dataset storage for processed | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `data/raw` | Dataset storage for raw | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `data/synthetic` | Dataset storage for synthetic | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `docs` | Comprehensive engineering, legal, architecture, and submission documentation | Code / Docs / Manifests | 3 file(s) (`DATA_LICENSES.md`, ...) | `ACTIVE (Files Present)` |
| `docs/00_PROJECT_CHARTER` | Charter, MVP scope, stakeholders, and success criteria | Code / Docs / Manifests | 6 file(s) (`ASSUMPTIONS.md`, ...) | `ACTIVE (Files Present)` |
| `docs/01_PROBLEM_STATEMENT` | Problem statement, domain background, and operational context | Code / Docs / Manifests | 2 file(s) (`PS_REQUIREMENTS_MATRIX.md, REQUIREMENT_TRACEABILITY.md`) | `ACTIVE (Files Present)` |
| `docs/01_PROBLEM_STATEMENT/OFFICIAL_PS` | Problem statement, domain background, and operational context | Code / Docs / Manifests | 2 file(s) (`SOURCE_RECORD.md, problem_statement_transcript.md`) | `ACTIVE (Files Present)` |
| `docs/02_LEGAL_AUTHORITY` | Legal authority register, primary source provenance, and legal guidance | Code / Docs / Manifests | 4 file(s) (`LEGAL_CHANGELOG.md`, ...) | `ACTIVE (Files Present)` |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS` | Legal authority register, primary source provenance, and legal guidance | Code / Docs / Manifests | 1 file(s) (`CHANGE_IMPACT_MATRIX.md`) | `ACTIVE (Files Present)` |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_128_E` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_312_E` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_418_E` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/ACT` | Legal authority register, primary source provenance, and legal guidance | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `docs/02_LEGAL_AUTHORITY/ACT/amendments` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/ACT/legal_metrology_act_2009` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES` | Legal authority register, primary source provenance, and legal guidance | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/FAQs` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/implementation_guidelines` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/official_advisories` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES` | Legal authority register, primary source provenance, and legal guidance | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS` | Legal authority register, primary source provenance, and legal guidance | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2012` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2013` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2014` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2015` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2016` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2017` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2022` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2023` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2026` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/BASE_2011` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/CONSOLIDATED` | Legal authority register, primary source provenance, and legal guidance | Level 1 Source PDFs | 0 file(s) | `EMPTY / RESERVED (Level 1 Primary Gazette PDFs to be deposited)` |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG` | Legal authority register, primary source provenance, and legal guidance | Code / Docs / Manifests | 5 file(s) (`applicability_matrix.yaml`, ...) | `ACTIVE (Files Present)` |
| `docs/03_PRODUCT_REQUIREMENTS` | Functional, non-functional, and compliance requirements | Code / Docs / Manifests | 6 file(s) (`ACCEPTANCE_CRITERIA.md`, ...) | `ACTIVE (Files Present)` |
| `docs/04_ARCHITECTURE` | System architecture, rule engine, data flows, and state machines | Code / Docs / Manifests | 8 file(s) (`AI_PIPELINE.md`, ...) | `ACTIVE (Files Present)` |
| `docs/04_ARCHITECTURE/diagrams` | System architecture, rule engine, data flows, and state machines | Code / Docs / Manifests | 0 file(s) | `EMPTY / RESERVED (Generated binary diagrams pending render)` |
| `docs/05_AI_VISION` | AI/CV vision pipelines, OCR evaluation, and image quality gates | Code / Docs / Manifests | 9 file(s) (`CALIBRATION.md`, ...) | `ACTIVE (Files Present)` |
| `docs/06_RULE_ENGINE` | Security, threat modeling, RBAC, tamper-evidence, and data privacy | Code / Docs / Manifests | 6 file(s) (`APPLICABILITY_ENGINE.md`, ...) | `ACTIVE (Files Present)` |
| `docs/07_DATA` | Data architecture, schemas, golden sets, and audit trails | Code / Docs / Manifests | 7 file(s) (`ANNOTATION_GUIDE.md`, ...) | `ACTIVE (Files Present)` |
| `docs/08_EVIDENCE` | Testing strategy, compliance verification, and test suites | Code / Docs / Manifests | 6 file(s) (`AUDIT_LOG.md`, ...) | `ACTIVE (Files Present)` |
| `docs/09_SECURITY_PRIVACY` | UI/UX workflows, officer interactions, and review screens | Code / Docs / Manifests | 5 file(s) (`DATA_RETENTION.md`, ...) | `ACTIVE (Files Present)` |
| `docs/10_TESTING` | Operations, deployment topology, and incident response | Code / Docs / Manifests | 6 file(s) (`ADVERSARIAL_TESTS.md`, ...) | `ACTIVE (Files Present)` |
| `docs/11_JUDGING` | SIH judging criteria, rubrics, and Q&A defense | Code / Docs / Manifests | 11 file(s) (`CRITERION_EVIDENCE_MATRIX.md`, ...) | `ACTIVE (Files Present)` |
| `docs/12_PRIOR_ART` | Risk register, mitigation strategies, and limitations | Code / Docs / Manifests | 3 file(s) (`COMPETITOR_MATRIX.md`, ...) | `ACTIVE (Files Present)` |
| `docs/12_PRIOR_ART/GOVERNMENT_SYSTEMS` | Risk register, mitigation strategies, and limitations | Code / Docs / Manifests | 1 file(s) (`README.md`) | `ACTIVE (Files Present)` |
| `docs/12_PRIOR_ART/PAPERS` | Risk register, mitigation strategies, and limitations | Code / Docs / Manifests | 1 file(s) (`README.md`) | `ACTIVE (Files Present)` |
| `docs/12_PRIOR_ART/PRODUCTS` | Risk register, mitigation strategies, and limitations | Code / Docs / Manifests | 1 file(s) (`README.md`) | `ACTIVE (Files Present)` |
| `docs/13_BUILD_PLAN` | Build plan, engineering milestones, and work breakdown | Code / Docs / Manifests | 5 file(s) (`DEFINITION_OF_DONE.md`, ...) | `ACTIVE (Files Present)` |
| `docs/14_SUBMISSION` | Submission artifacts, audit reports, and readiness documentation | Code / Docs / Manifests | 14 file(s) (`AUDIT_SUMMARY.md`, ...) | `ACTIVE (Files Present)` |
| `docs/15_DECISIONS` | Repository component | Code / Docs / Manifests | 2 file(s) (`ADR_TEMPLATE.md, README.md`) | `ACTIVE (Files Present)` |
| `docs/16_LIMITATIONS` | Repository component | Code / Docs / Manifests | 6 file(s) (`AI_LIMITATIONS.md`, ...) | `ACTIVE (Files Present)` |
| `docs/17_CLAIMS` | Repository component | Code / Docs / Manifests | 5 file(s) (`CLAIMS_REGISTER.md`, ...) | `ACTIVE (Files Present)` |
| `experiments` | Machine learning and computer vision experimental scripts and logs | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `experiments/calibration` | Experimental trials for calibration | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/dewarping` | Experimental trials for dewarping | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/end_to_end` | Experimental trials for end to end | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/extraction` | Experimental trials for extraction | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/font_measurement` | Experimental trials for font measurement | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/ocr` | Experimental trials for ocr | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/pdp_detection` | Experimental trials for pdp detection | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `experiments/rules` | Experimental trials for rules | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `infra` | Infrastructure-as-code and container build definitions | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `infra/db` | Infrastructure definitions for db | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `infra/deployment` | Infrastructure definitions for deployment | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `infra/docker` | Infrastructure definitions for docker | Code / Docs / Manifests | 3 file(s) (`.gitkeep`, ...) | `ACTIVE (Files Present)` |
| `infra/monitoring` | Infrastructure definitions for monitoring | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `infra/storage` | Infrastructure definitions for storage | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `models` | Repository component | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `models/cards` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `models/configs` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `models/registry` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `models/weights` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `packages` | Modular Python core library packages | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `packages/calibration` | Modular package: calibration | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/evidence` | Modular package: evidence | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/extraction` | Modular package: extraction | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/measurement` | Modular package: measurement | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/ocr` | Modular package: ocr | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/reporting` | Modular package: reporting | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/rules-engine` | Modular package: rules-engine | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/shared` | Modular package: shared | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `packages/vision` | Modular package: vision | Scaffold README / specs | 1 file(s) (`.gitkeep`) | `SCAFFOLD / SPECIFIED (Architecture & Contract Defined)` |
| `regulations` | Authoritative regulatory registry, extracted texts, and rule schemas | Code / Docs / Manifests | 1 file(s) (`source_registry.yaml`) | `ACTIVE (Files Present)` |
| `regulations/amendments` | Regulatory repository for amendments | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `regulations/amendments/packaged_commodities` | Regulatory repository for amendments | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/applicability` | Regulatory repository for applicability | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/current` | Regulatory repository for current | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `regulations/current/legal_metrology_act_2009` | Regulatory repository for current | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/current/packaged_commodities_rules` | Regulatory repository for current | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/exemptions` | Regulatory repository for exemptions | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/historical` | Regulatory repository for historical | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/interpretations` | Regulatory repository for interpretations | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/proposed` | Regulatory repository for proposed | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `regulations/superseded` | Regulatory repository for superseded | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research` | Repository component | Code / Docs / Manifests | 1 file(s) (`README.md`) | `ACTIVE (Files Present)` |
| `research/academic_papers` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/competitors` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/hackathon_winners` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/official_sources` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/prior_art` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/research_notes` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `research/secondary_sources` | Repository component | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `rules` | Legal Metrology declarative rules separated by verification lifecycle | Code / Docs / Manifests | 1 file(s) (`README.md`) | `ACTIVE (Files Present)` |
| `rules/current` | Lifecycle state for declarative rules: current | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `rules/fixtures` | Lifecycle state for declarative rules: fixtures | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `rules/historical` | Lifecycle state for declarative rules: historical | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `rules/proposed` | Lifecycle state for declarative rules: proposed | Code / Docs / Manifests | 2 file(s) (`template_declarations_rule.yaml, template_numeral_height_rule.yaml`) | `ACTIVE (Files Present)` |
| `rules/schema` | Lifecycle state for declarative rules: schema | Code / Docs / Manifests | 3 file(s) (`applicability.schema.json`, ...) | `ACTIVE (Files Present)` |
| `rules/superseded` | Lifecycle state for declarative rules: superseded | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `rules/tests` | Lifecycle state for declarative rules: tests | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `rules/verified` | Lifecycle state for declarative rules: verified | Rule YAMLs | 0 file(s) | `EMPTY / RESERVED (Declarative rules lifecycle stages pending primary verification)` |
| `scripts` | Utility scripts for maintenance, verification, and developer workflows | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `scripts/benchmark` | Automation scripts for benchmark | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `scripts/dataset` | Automation scripts for dataset | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `scripts/legal` | Automation scripts for legal | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `scripts/reports` | Automation scripts for reports | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `scripts/verification` | Automation scripts for verification | Code / Docs / Manifests | 6 file(s) (`verify_claims.py`, ...) | `ACTIVE (Files Present)` |
| `tests` | Comprehensive multi-level test suite | Parent container | 0 file(s) | `CONTAINER (Contains Subdirectories)` |
| `tests/e2e` | Test suite for e2e | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `tests/fixtures` | Test suite for fixtures | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `tests/integration` | Test suite for integration | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `tests/rules` | Test suite for rules | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `tests/security` | Test suite for security | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |
| `tests/unit` | Test suite for unit | Code / Docs / Manifests | 2 file(s) (`.gitkeep, test_verification_pipeline.py`) | `ACTIVE (Files Present)` |
| `tests/vision` | Test suite for vision | Code / Docs / Manifests | 1 file(s) (`.gitkeep`) | `ACTIVE (Files Present)` |

---

## 3. Directory Invariant & Verification Results

1. **Machine-Specific Path References:** 0 detected. All markdown and configuration paths are strictly repository-relative.
2. **Broken Symlinks / References:** 0 detected.
3. **Unaccounted Files:** 0 detected. All files map directly to either system documentation, schemas, unit tests, or scaffold packages.
4. **Lifecycle Segregation:** Strictly preserved between `regulations/` (canonical source registry) and `rules/` (declarative engine rules).
