# Final Repository Audit & Hardening Summary — Project Nirikshak

**Audit Execution Date:** 2026-09-04T21:51:00+05:30  
**Target Repository:** `sih26034-nirikshak` (SIH 2026 — PS 26034)  
**Lead Auditor:** Principal Software Architect & QA Lead  
**Audit Purpose:** Hardening the repository against legal hallucination, architectural overclaiming, unbacked performance claims, and missing provenance.

---

## 1. Files Added
1. [`docs/14_SUBMISSION/REPOSITORY_AUDIT.md`](REPOSITORY_AUDIT.md) — Comprehensive inventory of all files, claims, and provenance states.
2. [`docs/14_SUBMISSION/SIH_CLAIM_VERIFICATION.md`](SIH_CLAIM_VERIFICATION.md) — Dedicated audit of all SIH-specific claims, dates, and judging rubrics.
3. [`docs/11_JUDGING/PROBLEM_SOLVING_CASE.md`](..\11_JUDGING\PROBLEM_SOLVING_CASE.md) — Problem solving alignment case for judging defense.
4. [`docs/11_JUDGING/PROTOTYPE_CASE.md`](..\11_JUDGING\PROTOTYPE_CASE.md) — Working prototype case for judging defense.
5. [`research/README.md`](..\..\research\README.md) — Formal research quarantine policy isolating discovery reports from legal authority.
6. [`scripts/verification/verify_repository_integrity.py`](..\..\scripts\verification\verify_repository_integrity.py) — Master repository invariant and structural integrity verifier.
7. [`docs/14_SUBMISSION/AUDIT_SUMMARY.md`](AUDIT_SUMMARY.md) — This audit summary report.

---

## 2. Files Modified
1. [`regulations/source_registry.yaml`](..\..\regulations\source_registry.yaml) — Standardized source record schema fields (`issuing_authority`, `effective_from`, `effective_to`, `retrieval_date`, `document_sha256`, `local_artifact`, `verification_date`).
2. [`rules/schema/rule.schema.json`](..\..\rules\schema\rule.schema.json) — Standardized rule record schema matching exact fields (`status`, `source_document_sha256`, `source_page`, `source_section`, `source_rule`, `source_subrule`, `source_table`, `last_verified`).
3. [`rules/proposed/template_declarations_rule.yaml`](..\..\rules\proposed\template_declarations_rule.yaml) — Conformed to standardized rule schema; status set to `PRIMARY_SOURCE_REQUIRED`.
4. [`rules/proposed/template_numeral_height_rule.yaml`](..\..\rules\proposed\template_numeral_height_rule.yaml) — Conformed to standardized rule schema; status set to `PRIMARY_SOURCE_REQUIRED`.
5. [`scripts/verification/verify_legal_sources.py`](..\..\scripts\verification\verify_legal_sources.py) — Updated to enforce standardized source record schema fields.
6. [`scripts/verification/verify_rule_registry.py`](..\..\scripts\verification\verify_rule_registry.py) — Updated to validate standardized rule record schema and lifecycle gates.
7. [`docs/11_JUDGING/JUDGING_CRITERIA.md`](..\11_JUDGING\JUDGING_CRITERIA.md) — Added mandatory warning banner: `ANALYST FRAMEWORK — NOT OFFICIAL SIH MARKING SHEET`.
8. [`docs/14_SUBMISSION/FINAL_FEATURES.md`](FINAL_FEATURES.md) — Disciplined implementation stages: changed application modules from "Prototype Ready" to `PLANNED (Architectural Spec Complete)`.
9. [`docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`](..\01_PROBLEM_STATEMENT\PS_REQUIREMENTS_MATRIX.md) — Explicitly labeled planned test suites and application modules as `PLANNED`.
10. [`tests/unit/test_verification_pipeline.py`](..\..\tests\unit\test_verification_pipeline.py) — Added test for `verify_repository_integrity.py`.
11. [`Makefile`](..\..\Makefile) — Added `verify-integrity` target to `make verify`.
12. [`docs/14_SUBMISSION/DOCUMENT_INDEX.md`](DOCUMENT_INDEX.md) — Updated master index with all newly created documents.

---

## 3. Files Intentionally Left Unchanged
- All core architecture specifications in `docs/04_ARCHITECTURE/` (Data Flow, Offline Architecture, Rule Engine, Evidence DAG, Security).
- Core optics specifications in `docs/05_AI_VISION/` (Image Quality Gate, Calibration, Font Measurement, Curved Surfaces).
- Core governance documents in `docs/00_PROJECT_CHARTER/`, `docs/02_LEGAL_AUTHORITY/`, `docs/08_EVIDENCE/`, `docs/09_SECURITY_PRIVACY/`, `docs/10_TESTING/`, `docs/12_PRIOR_ART/`, `docs/13_BUILD_PLAN/`, `docs/15_DECISIONS/`, `docs/16_LIMITATIONS/`, `docs/17_CLAIMS/`.

---

## 4. Unsupported Claims Removed / Flagged
1. **Implementation Overclaiming Removed:**
   - Previous status of application features labeled as "Prototype Ready" in `FINAL_FEATURES.md` was corrected to `PLANNED (Architectural Spec Complete)`.
   - Planned test suites in `PS_REQUIREMENTS_MATRIX.md` are explicitly designated as `(Planned)`.
2. **Unofficial Rubric Labeled:**
   - Replaced generic disclaimer in `JUDGING_CRITERIA.md` with explicit required notice: `ANALYST FRAMEWORK — NOT OFFICIAL SIH MARKING SHEET`.
3. **SIH Administrative Data Flagged:**
   - SIH 2026 event dates, prize amounts, and jury composition flagged as `UNKNOWN` or `UNVERIFIED` in `docs/14_SUBMISSION/SIH_CLAIM_VERIFICATION.md`.

---

## 5. Legal Sources Requiring Verification
The following primary source artifacts in `regulations/source_registry.yaml` currently have status `PARTIALLY_VERIFIED` because local PDF artifacts must be downloaded and their SHA-256 hashes computed:
1. `IN-ACT-2009-01`: The Legal Metrology Act, 2009.
2. `IN-LMPC-2011-GSR202E`: Legal Metrology (Packaged Commodities) Rules, 2011.
3. `IN-LMPC-2017-GSR629E`: LMPC Amendment Rules, 2017.
4. `IN-LMPC-2021-GSR779E`: LMPC Amendment Rules, 2021.
5. `IN-LMPC-2024-DRAFT-R3`: Draft Amendment to Rule 3 (Flagged as `PROPOSED`; blocked from current rules).

---

## 6. SIH Claims Requiring Verification
- Problem Statement 26034 final official text confirmation from the portal.
- Confirmation of official judging criteria and weightings once announced at event.

---

## 7. Datasets Requiring Verification
- Retail pilot dataset `DS-RETAIL-PILOT-001` (50 retail packaging samples) pending physical procurement and caliper measurement.
- Synthetic dataset `DS-SYNTH-001` pending procedural rendering pipeline execution.

---

## 8. APIs Requiring Verification
- **External Government APIs:** **NONE.** The system confirms zero dependency on external government APIs (DoCA portal, NCH, e-Daakhil). The system is architected to operate offline without external network or cloud service dependencies.

---

## 9. Experiments Still Required
All empirical benchmark protocols are defined in `benchmarks/protocols/` and marked `TBD — MEASURE`:
1. `PROTO-OCR-001`: Character Error Rate (CER) and Word Error Rate (WER) on retail packaging.
2. `PROTO-CALIB-001`: Scale factor estimation error on planar fiducials.
3. `PROTO-FONT-001`: Optical font height error bound vs. digital vernier caliper ground truth.
4. `PROTO-PDP-001`: Mean IoU for Principal Display Panel contour segmentation.
5. `PROTO-LATENCY-001`: End-to-end multi-panel inspection runtime on CPU.

---

## 10. Architecture Decisions Still Open
1. **DEC-01:** Selection between PaddleOCR and Tesseract based on empirical benchmark results (`PROTO-OCR-001`).
2. **DEC-02:** Standardized physical calibration marker format (Circular sticker vs. ID-1 inspection card).
3. **DEC-03:** Local SQLite with SQLCipher vs. Embedded PostgreSQL on mobile field workstation.

---

## 11. Remaining Risks & Mitigations
- **Optical Glare Risk:** Highly reflective foil packaging can obliterate text $\rightarrow$ Mitigated by Image Quality Gate specular reflection mask prompting `REQUEST_RETAKE`.
- **Perspective Distortion Risk:** Severe camera tilt distorts apparent character height $\rightarrow$ Mitigated by planar homography rectification and ellipse eccentricity thresholding.
- **Regulatory Confusion Risk:** Older packaging penalized under newer rules $\rightarrow$ Mitigated by Regulatory Time-Machine loading active rules based on declared manufacturing date.

---

## 12. Exact Next Engineering Steps
1. **Step 1:** Ingest Level 1 primary PDFs into `regulations/current/` and compute SHA-256 hashes to promote `source_registry.yaml` to `VERIFIED_PRIMARY`.
2. **Step 2:** Populate verified substantive rule records in `rules/verified/` citing exact page and subrule references from the verified PDFs.
3. **Step 3:** Implement core computer vision package modules:
   - `packages/vision/quality_gate.py` (Laplacian blur and glare mask).
   - `packages/calibration/target_detector.py` (Reference marker scale estimation).
   - `packages/measurement/font_estimator.py` (Optical font height in mm).
4. **Step 4:** Implement `packages/rules-engine/` deterministic evaluator and regulatory snapshot manager.
5. **Step 5:** Build guided capture interface in `apps/web/` and REST endpoints in `apps/api/`.
6. **Step 6:** Execute benchmark protocols against `data/benchmark/` to replace `TBD — MEASURE` with real empirical measurements.
