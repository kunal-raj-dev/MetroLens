# NIRIKSHAK — GITKEEP FORENSIC AUDIT

**Audit Standard:** Forensic Directory Scaffolding & Phantom Artifact Review (Truth > Appearance)  
**Audit Execution Date:** 2026-09-04  
**Total `.gitkeep` Files Audited:** 71  

---

## 1. Executive Summary

A `.gitkeep` file establishes an intentional directory reservation in Git. **A `.gitkeep` is NEVER evidence that an artifact, model, dataset, or implementation exists.**

This audit inspects every single `.gitkeep` file in the repository to determine whether each empty directory is a legitimate planned scaffold or unnecessary clutter (Category F).

### Classification Taxonomy
- **Class A:** Intentional Future Artifact Directory (e.g. model weights, benchmark results, demo assets)
- **Class B:** Required Now But Empty (Defect: Artifact claimed to exist today but missing)
- **Class C:** Experiment Not Yet Run (Physical calibration/dewarping/OCR trials)
- **Class D:** Dataset Not Yet Acquired (Physical retail SKUs or synthetic label renders)
- **Class E:** Implementation Not Yet Built (Application frontends, backends, modular packages)
- **Class F:** Unnecessary / Redundant / Recommend Removal (Clutter from early brainstorming without build plan backing)

### Summary Statistics

| Category | Meaning | Count | Governance Rationale |
| :--- | :--- | :---: | :--- |
| **Class A** | Intentional Future Artifact | 28 | Reserved for external weights, benchmark runs, and Level 1 Gazette PDFs |
| **Class B** | Required Now But Empty | 0 | Zero unacknowledged empty directories masquerading as complete |
| **Class C** | Experiment Not Yet Run | 8 | Pre-implementation experiment harnesses awaiting physical test bench |
| **Class D** | Dataset Not Yet Acquired | 6 | Planned image directories awaiting physical procurement or synthesis |
| **Class E** | Implementation Not Yet Built | 12 | Formal architectural scaffolds for apps (`apps/*`) and packages (`packages/*`) |
| **Class F** | Unnecessary / Recommend Removal | 17 | Redundant or duplicate directories with zero active role in build plan |
| **Total** | | **71** | |

---

## 2. Itemized Gitkeep Forensic Register

| # | Gitkeep Path | Parent Directory | Documented Purpose | Expected Future Artifact | Referenced in Plan? | Required? | Class | Audit Recommendation |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | `apps/api/.gitkeep` | `apps/api` | Storage for api | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 2 | `apps/web/.gitkeep` | `apps/web` | Storage for web | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 3 | `apps/worker/.gitkeep` | `apps/worker` | Storage for worker | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 4 | `assets/demo/.gitkeep` | `assets/demo` | Storage for demo | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 5 | `assets/diagrams/.gitkeep` | `assets/diagrams` | Storage for diagrams | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 6 | `assets/presentation/.gitkeep` | `assets/presentation` | Storage for presentation | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 7 | `assets/sample_packages/.gitkeep` | `assets/sample_packages` | Storage for sample_packages | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 8 | `assets/screenshots/.gitkeep` | `assets/screenshots` | Storage for screenshots | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 9 | `benchmarks/datasets/.gitkeep` | `benchmarks/datasets` | Storage for datasets | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 10 | `benchmarks/protocols/.gitkeep` | `benchmarks/protocols` | Storage for protocols | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 11 | `benchmarks/reports/.gitkeep` | `benchmarks/reports` | Storage for reports | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 12 | `benchmarks/results/.gitkeep` | `benchmarks/results` | Storage for results | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 13 | `benchmarks/runs/.gitkeep` | `benchmarks/runs` | Storage for runs | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 14 | `data/annotations/.gitkeep` | `data/annotations` | Storage for annotations | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 15 | `data/benchmark/.gitkeep` | `data/benchmark` | Storage for benchmark | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 16 | `data/processed/.gitkeep` | `data/processed` | Storage for processed | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 17 | `data/raw/.gitkeep` | `data/raw` | Storage for raw | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 18 | `data/synthetic/.gitkeep` | `data/synthetic` | Storage for synthetic | Raw/processed packaging imagery, synthetic renders, or annotation labels | Yes (data/manifests/manifest.yaml, docs/07_DATA/) | YES | `D` | RETAIN (Populate upon physical SKU acquisition in Stage 2) |
| 19 | `experiments/calibration/.gitkeep` | `experiments/calibration` | Storage for calibration | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 20 | `experiments/dewarping/.gitkeep` | `experiments/dewarping` | Storage for dewarping | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 21 | `experiments/end_to_end/.gitkeep` | `experiments/end_to_end` | Storage for end_to_end | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 22 | `experiments/extraction/.gitkeep` | `experiments/extraction` | Storage for extraction | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 23 | `experiments/font_measurement/.gitkeep` | `experiments/font_measurement` | Storage for font_measurement | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 24 | `experiments/ocr/.gitkeep` | `experiments/ocr` | Storage for ocr | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 25 | `experiments/pdp_detection/.gitkeep` | `experiments/pdp_detection` | Storage for pdp_detection | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 26 | `experiments/rules/.gitkeep` | `experiments/rules` | Storage for rules | Physical laboratory trial script, raw input image set, and measurement log | Yes (docs/05_AI_VISION/, docs/10_TESTING/PERFORMANCE_TESTS.md) | YES | `C` | RETAIN (Execute during Stage 2 Physical Benchmarking) |
| 27 | `infra/db/.gitkeep` | `infra/db` | Storage for db | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 28 | `infra/deployment/.gitkeep` | `infra/deployment` | Storage for deployment | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 29 | `infra/docker/.gitkeep` | `infra/docker` | Storage for docker | Future project artifact | Referenced in architecture | YES | `A` | RETAIN |
| 30 | `infra/monitoring/.gitkeep` | `infra/monitoring` | Storage for monitoring | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 31 | `infra/storage/.gitkeep` | `infra/storage` | Storage for storage | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 32 | `models/cards/.gitkeep` | `models/cards` | Storage for cards | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 33 | `models/configs/.gitkeep` | `models/configs` | Storage for configs | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 34 | `models/registry/.gitkeep` | `models/registry` | Storage for registry | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 35 | `models/weights/.gitkeep` | `models/weights` | Storage for weights | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 36 | `packages/calibration/.gitkeep` | `packages/calibration` | Storage for calibration | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 37 | `packages/evidence/.gitkeep` | `packages/evidence` | Storage for evidence | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 38 | `packages/extraction/.gitkeep` | `packages/extraction` | Storage for extraction | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 39 | `packages/measurement/.gitkeep` | `packages/measurement` | Storage for measurement | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 40 | `packages/ocr/.gitkeep` | `packages/ocr` | Storage for ocr | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 41 | `packages/reporting/.gitkeep` | `packages/reporting` | Storage for reporting | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 42 | `packages/rules-engine/.gitkeep` | `packages/rules-engine` | Storage for rules-engine | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 43 | `packages/shared/.gitkeep` | `packages/shared` | Storage for shared | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 44 | `packages/vision/.gitkeep` | `packages/vision` | Storage for vision | Production Python/TypeScript application or modular package code | Yes (docs/04_ARCHITECTURE/, docs/13_BUILD_PLAN/TASK_BREAKDOWN.md) | YES | `E` | RETAIN AS SCAFFOLD (Populate during Stage 2 Implementation) |
| 45 | `regulations/amendments/packaged_commodities/.gitkeep` | `regulations/amendments/packaged_commodities` | Storage for packaged_commodities | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 46 | `regulations/applicability/.gitkeep` | `regulations/applicability` | Storage for applicability | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 47 | `regulations/current/legal_metrology_act_2009/.gitkeep` | `regulations/current/legal_metrology_act_2009` | Storage for legal_metrology_act_2009 | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 48 | `regulations/current/packaged_commodities_rules/.gitkeep` | `regulations/current/packaged_commodities_rules` | Storage for packaged_commodities_rules | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 49 | `regulations/exemptions/.gitkeep` | `regulations/exemptions` | Storage for exemptions | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 50 | `regulations/historical/.gitkeep` | `regulations/historical` | Storage for historical | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 51 | `regulations/interpretations/.gitkeep` | `regulations/interpretations` | Storage for interpretations | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 52 | `regulations/proposed/.gitkeep` | `regulations/proposed` | Storage for proposed | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 53 | `regulations/superseded/.gitkeep` | `regulations/superseded` | Storage for superseded | Primary legal Gazette of India PDFs | Yes (regulations/source_registry.yaml) | YES | `A` | RETAIN (Deposit Gazette PDFs during Stage 2 Legal Verification) |
| 54 | `research/academic_papers/.gitkeep` | `research/academic_papers` | Storage for academic_papers | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 55 | `research/competitors/.gitkeep` | `research/competitors` | Storage for competitors | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 56 | `research/hackathon_winners/.gitkeep` | `research/hackathon_winners` | Storage for hackathon_winners | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 57 | `research/official_sources/.gitkeep` | `research/official_sources` | Storage for official_sources | Regulatory archive or research evidence pack | Yes (docs/02_LEGAL_AUTHORITY/SOURCE_REGISTER_GUIDE.md) | YES | `A` | RETAIN (.gitkeep can be removed as directory contains active markdown/YAML) |
| 58 | `research/prior_art/.gitkeep` | `research/prior_art` | Storage for prior_art | Regulatory archive or research evidence pack | Yes (docs/02_LEGAL_AUTHORITY/SOURCE_REGISTER_GUIDE.md) | YES | `A` | RETAIN (.gitkeep can be removed as directory contains active markdown/YAML) |
| 59 | `research/research_notes/.gitkeep` | `research/research_notes` | Storage for research_notes | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 60 | `research/secondary_sources/.gitkeep` | `research/secondary_sources` | Storage for secondary_sources | Regulatory archive or research evidence pack | Yes (docs/02_LEGAL_AUTHORITY/SOURCE_REGISTER_GUIDE.md) | YES | `A` | RETAIN (.gitkeep can be removed as directory contains active markdown/YAML) |
| 61 | `scripts/benchmark/.gitkeep` | `scripts/benchmark` | Storage for benchmark | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 62 | `scripts/dataset/.gitkeep` | `scripts/dataset` | Storage for dataset | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 63 | `scripts/legal/.gitkeep` | `scripts/legal` | Storage for legal | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 64 | `scripts/reports/.gitkeep` | `scripts/reports` | Storage for reports | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 65 | `tests/e2e/.gitkeep` | `tests/e2e` | Storage for e2e | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 66 | `tests/fixtures/.gitkeep` | `tests/fixtures` | Storage for fixtures | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 67 | `tests/integration/.gitkeep` | `tests/integration` | Storage for integration | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 68 | `tests/rules/.gitkeep` | `tests/rules` | Storage for rules | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |
| 69 | `tests/security/.gitkeep` | `tests/security` | Storage for security | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 70 | `tests/unit/.gitkeep` | `tests/unit` | Storage for unit | Benchmark logs, model weights, demo assets, or integration test suites | Yes (specs/, docs/11_JUDGING/, docs/13_BUILD_PLAN/) | YES | `A` | RETAIN AS INTENTIONAL SCAFFOLD |
| 71 | `tests/vision/.gitkeep` | `tests/vision` | Storage for vision | Redundant or premature structural scaffold | No direct build plan dependency; duplicate of standardized modular folders | NO | `F` | RECOMMEND REMOVAL (Clean directory clutter; consolidated elsewhere) |

---

## 3. Category F (Unnecessary / Recommend Removal) Action Plan

The audit identified **17 directories** classified as **Category F**. These directories represent early brainstorming scaffolds that have been superseded by standardized project directories:

1. **Redundant Infra Directories:** `infra/db`, `infra/monitoring`, `infra/storage`, `infra/deployment` are superseded by root `docker-compose.yml` and `infra/docker/`.
2. **Superseded Research Directories:** `research/academic_papers`, `research/competitors`, `research/hackathon_winners`, `research/research_notes` are superseded by the canonical 7-pack structure in `research/official_sources/`, `research/prior_art/`, `research/datasets/`, `research/models/`, `research/sih/`, and `research/research_gaps/`.
3. **Redundant Rule Folders:** `regulations/interpretations`, `regulations/exemptions`, `regulations/applicability` are superseded by `regulations/source_registry.yaml` and schema definitions in `rules/schema/`.
4. **Redundant Script & Test Folders:** `scripts/benchmark`, `scripts/dataset`, `scripts/legal`, `scripts/reports`, `tests/rules`, `tests/vision` are consolidated under `scripts/verification/` and `tests/unit/`, `tests/integration/`, `tests/compliance/`.

> [!NOTE]
> These Category F directories can be safely purged or left as dormant scaffolds during Stage 2 refactoring, without any impact on repository build or verification integrity.
