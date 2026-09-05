# Nirikshak — Canonical Project Status Record

**Version:** 1.0.0  
**Audit Date:** 2026-09-04  
**Authority:** Master Repository Governance Lead  
**Governing Principle:** ONE FACT → ONE CANONICAL SOURCE → SAME STATUS EVERYWHERE (TRUTH > APPEARANCE)

---

## 1. Canonical State Vector

```yaml
PROJECT_STAGE: PRE_IMPLEMENTATION

DOCUMENTATION: READY
LEGAL_VERIFICATION: INCOMPLETE
DATA_VERIFICATION: INCOMPLETE
IMPLEMENTATION: NOT_STARTED
EXPERIMENTAL_VALIDATION: NOT_STARTED
BENCHMARKING: NOT_STARTED
SECURITY: HARDENED

DATASETS_EXISTING: 0
EXPERIMENTS_COMPLETED: 0
BENCHMARKS_COMPLETED: 0

DS-SYNTH-001:
  status: PLANNED
  artifact_status: NOT_GENERATED
  planned_target: 1000

DS-RETAIL-PILOT-001:
  status: PLANNED
  artifact_status: DECLARED_BUT_MISSING
  planned_target: 50
```

---

## 2. Definitive Subsystem Reality

### 2.1 Datasets
- **Physical Datasets on Disk:** Exactly **0**.
- **`DS-SYNTH-001`**: Procedural synthetic FMCG vector layout benchmark. Planned target is 1,000 configurations. `status: PLANNED`, `artifact_status: NOT_GENERATED`. Zero files exist in `data/synthetic/` (contains only `.gitkeep`).
- **`DS-RETAIL-PILOT-001`**: Physical retail FMCG packaging ground-truth pilot. Planned target is 50 physical SKUs (20 cartons, 15 cans/bottles, 15 pouches). `status: PLANNED`, `artifact_status: DECLARED_BUT_MISSING`. Zero photos, 0 annotation files, and 0 caliper measurement logs exist in `data/raw/` or `data/annotations/`.
- **Dataset Rights:** Commercial packaging photographs and annotations carry `RIGHTS_VERIFICATION_REQUIRED` across all 6 facets:
  1. Image Rights: `RIGHTS_VERIFICATION_REQUIRED`
  2. Annotation Rights: `RIGHTS_VERIFICATION_REQUIRED`
  3. Trademark / Trade Dress: Third-Party Trademark Owners
  4. Redistribution Rights: `RESTRICTED`
  5. Publication Rights: `RESTRICTED`
  6. Hackathon Demonstration Rights: `RIGHTS_VERIFICATION_REQUIRED`

### 2.2 Legal Metrology Rules & Authority
- **Primary Source Gazette PDFs:** Exactly **0** physical PDF files archived on disk (`regulations/sources/` contains only `.gitkeep`).
- **Canonical Registry:** `regulations/source_registry.yaml` lists 10 instruments, all explicitly marked `instrument_status: UNKNOWN` pending local checksum verification.
- **Production Rules (`rules/current/`):** Exactly **0** files. Intentionally gated.
- **Verified Rules (`rules/verified/`):** Exactly **0** files. Intentionally gated.
- **Candidate Rules (`rules/proposed/`):** Exactly **2** files (`rule_06_mandatory_declarations_candidate.yaml`, `rule_07_table1_font_height_candidate.yaml`). Both are non-executable (`executable: false`) and carry `verification_status: PRIMARY_SOURCE_REQUIRED`.

### 2.3 Experiments & Benchmarks
- **Empirical Experiments Executed:** Exactly **0**. All directories in `experiments/` are classified as `SPECIFIED_ONLY`.
- **Empirical Benchmarks Run:** Exactly **0**. All accuracy metrics and hardware latencies are classified as `DESIGN TARGET — NOT VALIDATED` or `TBD — MEASURE`.

### 2.4 Software & Applications
- **Active Code Executed:** Strictly limited to CI repository governance and validation scripts in `scripts/verification/`.
- **Application Services (`apps/api`, `apps/web`, `apps/worker`):** Architectural scaffolds (`SCAFFOLD_ONLY`), containing `.gitkeep` and Dockerfile configurations. Production application code is `PENDING_IMPLEMENTATION`.
- **Core ML Packages (`packages/`):** Module specifications and interface boundaries only (`SCAFFOLD_ONLY`). Implementation is `PENDING_IMPLEMENTATION`.

### 2.5 Active Test Suite (Dynamic Discovery)
- **Active Test File:** `tests/unit/test_verification_pipeline.py`
- **Scope:** Governance verification pipeline only (does not test runtime application or vision components).
- **Execution Metadata:**
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

## 3. Precedence Hierarchy for Cross-Document Facts

When any document in this repository conflicts with another, truth is resolved using the following strict hierarchy:

1. **Physical Reality on Disk:** Direct filesystem inventory (`PHYSICAL_ARTIFACT_INVENTORY.md`).
2. **Canonical Manifests & Registries:**
   - Datasets: `data/manifests/manifest.yaml`
   - Legal Sources: `regulations/source_registry.yaml`
   - Candidate Rules: `rules/proposed/`
3. **Canonical Project Status Record:** This file (`docs/14_SUBMISSION/CANONICAL_PROJECT_STATUS.md`).
4. **General Documentation & Research Dossiers:** Subordinate to items 1–3. Any claim in a research dossier or architecture guide that conflicts with items 1–3 is void and must be downgraded.
