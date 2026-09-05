# NIRIKSHAK — FINAL REPOSITORY TRUTH CHECK

**Audit Standard:** Forensic Cross-Examination Against Physical Disk Reality (Truth > Appearance)  
**Audit Execution Date:** 2026-09-04  
**Audit Standard:** Strict Anti-Hallucination Policy  
**Mandate:** Direct, rigorous answers to the 14 core forensic questions.

---

## Question 1: Which datasets ACTUALLY exist?
**Answer: ZERO.**  
There are currently **0 physical datasets** committed to disk.  
All data subdirectories (`data/raw/`, `data/processed/`, `data/annotations/`, `data/synthetic/`, `data/benchmark/`) contain strictly `.gitkeep` placeholder files. No raw packaging photographs, no rectified crops, no polygon annotation files, and no caliper measurement sheets physically exist in the repository today.

---

## Question 2: Which datasets are only planned?
**Answer: ALL declared datasets are planned.**
1. **`DS-SYNTH-001`** (*Synthetic FMCG Packaging Benchmark Vector Set*): Planned target of 1,000 procedurally generated label configurations. Script and mathematical model specified; physical image files are `NOT_GENERATED`.
2. **`DS-RETAIL-PILOT-001`** (*Field Retail Packaged Commodities Ground-Truth Pilot*): Planned target of 50 physical retail SKU samples across dry food and personal care. Acquisition protocol specified; physical files are `DECLARED_BUT_MISSING`.

---

## Question 3: Which experiments ACTUALLY ran?
**Answer: ZERO.**  
All 8 experiment subdirectories (`experiments/calibration/`, `dewarping/`, `end_to_end/`, `extraction/`, `font_measurement/`, `ocr/`, `pdp_detection/`, `rules/`) contain strictly `.gitkeep` files.  
The experimental protocols, mathematical equations, and execution designs are fully documented in `docs/05_AI_VISION/`, but zero empirical trials have executed on physical hardware. All experiment directories are truthfully classified as **`SPECIFIED_ONLY`**.

---

## Question 4: Which benchmarks ACTUALLY ran?
**Answer: ZERO.**  
All 5 benchmark subdirectories (`benchmarks/datasets/`, `protocols/`, `reports/`, `results/`, `runs/`) contain strictly `.gitkeep` files.  
Zero benchmark scripts have been triggered, and zero latency or accuracy distribution logs exist on disk. Status is truthfully recorded as **`BENCHMARK_NOT_RUN`**.

---

## Question 5: Which models ACTUALLY exist?
**Answer: Zero model weights are committed locally in Git.**  
The `models/weights/` directory contains strictly `.gitkeep` because large deep learning weights are intentionally excluded from Git tracking.  
- Model architectures (PaddleOCR PP-OCRv4 DBNet, SVTR-LCNet, Tesseract 5 LSTM, RT-DETR) are formally specified with licensing audited (Apache 2.0).  
- Local availability status is **`WEIGHTS_NOT_TRACKED_IN_GIT`**, with acquisition and ONNX export scripts designated for Stage 2.

---

## Question 6: Which application code ACTUALLY exists?
**Answer: Only Governance & Verification Tooling exists as active executable Python code.**  
- **Active Executable Code:** Located in `scripts/verification/` (`verify_repository_integrity.py`, `verify_legal_sources.py`, `verify_rule_registry.py`, `verify_claims.py`, `verify_dataset_manifest.py`).
- **Scaffolds Only:** Application services (`apps/api/`, `apps/web/`, `apps/worker/`) and modular domain packages (`packages/calibration/`, `evidence/`, `extraction/`, `measurement/`, `ocr/`, `reporting/`, `rules-engine/`, `shared/`, `vision/`) contain strictly `.gitkeep` files and are classified as **`SCAFFOLD_ONLY`**.

---

## Question 7: Which tests ACTUALLY execute?
**Answer: Exactly 5 automated governance verification tests.**  
Executing `pytest -v` runs:
1. `tests/unit/test_verification_pipeline.py::test_verify_legal_sources` $ightarrow$ **PASSED**
2. `tests/unit/test_verification_pipeline.py::test_verify_rule_registry` $ightarrow$ **PASSED**
3. `tests/unit/test_verification_pipeline.py::test_verify_claims` $ightarrow$ **PASSED**
4. `tests/unit/test_verification_pipeline.py::test_verify_dataset_manifest` $ightarrow$ **PASSED**
5. `tests/unit/test_verification_pipeline.py::test_verify_repository_integrity` $ightarrow$ **PASSED**

**Active Test Scope & Execution Metrics:**  
The active governance verification suite is tested; runtime application, vision, rules-engine, integration and E2E tests remain pending implementation.

```text
[OBSERVED IN RUN:
duration=3.92s
python=3.12.7
os=Windows-11-10.0.26200-SP0
architecture=AMD64
commit=INITIAL_PRE_COMMIT_WORKING_TREE
tests_total=5
tests_passed=5
tests_failed=0
tests_skipped=0
]
```

---

## Question 8: Which legal sources ACTUALLY exist locally?
**Answer: Canonical registry exists; primary Gazette PDF artifacts are pending on disk.**  
- `regulations/source_registry.yaml` physically exists and tracks 10 legal authorities.
- Candidate machine-readable rules exist in `rules/proposed/` (`rule_06_mandatory_declarations_candidate.yaml`, `rule_07_table1_font_height_candidate.yaml`).
- Physical Gazette of India PDFs on disk (`regulations/sources/*.pdf`): **0 files** (Status: `PRIMARY_SOURCE_REQUIRED`).
- `rules/current/` and `rules/verified/`: **0 files** (Intentionally preserved empty).

---

## Question 9: Which assets ACTUALLY exist?
**Answer: Zero binary media assets exist on disk.**  
All subdirectories under `assets/` (`demo/`, `diagrams/`, `presentation/`, `sample_packages/`, `screenshots/`) contain strictly `.gitkeep` files.  
All mockups, diagrams, and demo workflows are documented in Markdown/Mermaid specifications, and physical screenshots are truthfully marked `PLANNED`.

---

## Question 10: Which claims were downgraded?
**Answer:**
1. **Dataset Claims in `manifest.yaml`:** Downgraded from implying completed collection on 2026-09-04 to `status: PLANNED`, `artifact_status: NOT_GENERATED` (`DS-SYNTH-001`) and `artifact_status: DECLARED_BUT_MISSING` (`DS-RETAIL-PILOT-001`).
2. **Test Coverage Phrasing:** Replaced claims of "100% test coverage" with "100% pass rate on active governance CI verification test suite (5/5 tests in tests/unit/)".
3. **Application Maturity:** Replaced any implication of "production-ready" with "Development Infrastructure Scaffold" and `PRE_IMPLEMENTATION`.
4. **Optical Precision:** Replaced hardcoded numbers ($\le 0.2	ext{ mm}$, $< 5	ext{ s}$) with `TARGET — NOT VALIDATED; Status: TBD — MEASURE`.

---

## Question 11: Which artifacts remain missing?
**Answer:**
1. Physical retail packaging photographs (50 SKUs) in `data/raw/`.
2. Digital caliper measurement sheets in `data/benchmark/caliper_measurements.csv`.
3. Annotation JSON files in `data/annotations/`.
4. Level 1 Gazette of India PDFs in `regulations/sources/`.
5. Pre-trained OCR/vision model weights in `models/weights/`.
6. Runtime application source code in `apps/` and `packages/`.
7. Empirical benchmark execution logs in `benchmarks/results/`.

---

## Question 12: Which directories are intentionally empty?
**Answer: 26 directories are intentionally preserved empty under the Anti-Hallucination Policy:**
- `rules/current/`, `rules/verified/`, `rules/historical/`, `rules/superseded/`, `rules/fixtures/`, `rules/tests/`
- `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2012/` through `2026/`
- `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/BASE_2011/`, `CONSOLIDATED/`
- `docs/02_LEGAL_AUTHORITY/ACT/amendments/`, `legal_metrology_act_2009/`
- `docs/02_LEGAL_AUTHORITY/GUIDELINES/FAQs/`, `implementation_guidelines/`, `official_advisories/`

---

## Question 13: Which `.gitkeep` files should be removed?
**Answer: 17 Category F `.gitkeep` files are recommended for removal during Stage 2 refactoring:**
1. `infra/db/.gitkeep`, `infra/monitoring/.gitkeep`, `infra/storage/.gitkeep`, `infra/deployment/.gitkeep` (Superseded by `docker-compose.yml` and `infra/docker/`).
2. `research/academic_papers/.gitkeep`, `research/competitors/.gitkeep`, `research/hackathon_winners/.gitkeep`, `research/research_notes/.gitkeep` (Superseded by canonical 7-pack structure in `research/`).
3. `regulations/interpretations/.gitkeep`, `regulations/exemptions/.gitkeep`, `regulations/applicability/.gitkeep` (Superseded by `source_registry.yaml` and schema definitions).
4. `scripts/benchmark/.gitkeep`, `scripts/dataset/.gitkeep`, `scripts/legal/.gitkeep`, `scripts/reports/.gitkeep` (Consolidated under `scripts/verification/`).
5. `tests/rules/.gitkeep`, `tests/vision/.gitkeep` (Consolidated under `tests/unit/`, `tests/integration/`).

---

## Question 14: Which claims have no corresponding physical artifact?
**Answer:**
- **Zero claims remain active without explicit disclosure.**
- Every capability that lacks physical code, images, or Gazette PDFs has been explicitly classified as `PLANNED`, `PENDING_IMPLEMENTATION`, `PENDING_EXPERIMENT`, or `PENDING_PRIMARY_SOURCE` in `docs/14_SUBMISSION/CLAIM_ARTIFACT_TRACEABILITY.md`.

---

**Truth Check Verdict:** **`VERIFIED CONSISTENT WITH DISK REALITY`**
