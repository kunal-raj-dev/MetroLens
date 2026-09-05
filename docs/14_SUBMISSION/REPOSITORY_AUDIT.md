# Comprehensive Repository Audit & Provenance Inventory — Project Nirikshak

**Audit Execution Date:** 2026-09-04T21:48:00+05:30  
**Target Repository:** `sih26034-nirikshak` (SIH 2026 — PS 26034)  
**Lead Auditor:** Principal Software Architect & QA Lead  
**Audit Mandate:** Anti-Hallucination, Legal Provenance, Traceability, and Implementation Discipline Audit.

---

## 1. Inventory of Files Found

A total of **135 tracked files** (excluding `.git/` internals) were surveyed across the repository:
- **Root Configuration & Metadata (7 files):** `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore`, `.env.example`, `docker-compose.yml`, `Makefile`.
- **CI/CD & GitHub Templates (3 files):** `.github/workflows/ci.yml`, `.github/workflows/verify-claims.yml`, `.github/pull_request_template.md`.
- **Regulatory Authority (`regulations/`, 1 file + 9 directory trees):** `regulations/source_registry.yaml`.
- **Machine-Readable Rules (`rules/`, 6 files):** `rules/README.md`, `rules/schema/rule.schema.json`, `rules/schema/evidence.schema.json`, `rules/schema/applicability.schema.json`, `rules/proposed/template_declarations_rule.yaml`, `rules/proposed/template_numeral_height_rule.yaml`.
- **Verification Scripts (`scripts/verification/`, 5 files):** `verify_legal_sources.py`, `verify_rule_registry.py`, `verify_claims.py`, `verify_dataset_manifest.py`, `verify_report_provenance.py`.
- **Data & Manifests (`data/`, 1 file):** `data/manifests/manifest.yaml`.
- **Tests (`tests/`, 2 files):** `tests/unit/test_verification_pipeline.py`, `tests/unit/__pycache__/...`.
- **Documentation Suite (`docs/`, 77 files across 18 subdirectories):** Covering charter, problem statement, legal authority, product requirements, architecture, AI vision, rule engine, data, evidence, security/privacy, testing, judging, prior art, build plan, submission, decisions, limitations, and claims.
- **Skeleton Directories with `.gitkeep` (71 directories):** Covering `apps/*`, `packages/*`, `experiments/*`, `benchmarks/*`, `models/*`, `assets/*`, `infra/*`, `research/*`.

---

## 2. Duplicate Files & Registry Audit

- **Duplicate Source Registries:**
  - **Audit Finding:** **NONE FOUND.** There is exactly one canonical regulatory registry: [`regulations/source_registry.yaml`](..\..\regulations\source_registry.yaml).
  - The documentation folder contains only [`docs/02_LEGAL_AUTHORITY/SOURCE_REGISTER_GUIDE.md`](..\02_LEGAL_AUTHORITY\SOURCE_REGISTER_GUIDE.md), which serves as an explanatory guide and points explicitly to `regulations/source_registry.yaml`.
- **Duplicate Documentation Files:**
  - [`docs/DATA_LICENSES.md`](..\DATA_LICENSES.md) vs. [`docs/07_DATA/DATA_LICENSES.md`](..\07_DATA\DATA_LICENSES.md).
  - **Issue:** Both files describe data licensing and permissions.
  - **Resolution Required:** Standardize `docs/07_DATA/DATA_LICENSES.md` as the detailed dataset licensing specification, and retain `docs/DATA_LICENSES.md` at root docs level as a high-level summary pointer, or consolidate cleanly.

---

## 3. Legal Claims Found & Source Provenance Audit

- **Statutory Claims Audited:**
  1. *Rule 6(1) Mandatory Declarations:* Name/Address of Manufacturer, Country of Origin, Generic Name, Net Quantity, Mfg Date, MRP, Consumer Care.
     - *Provenance:* Cites `IN-LMPC-2011-GSR202E`.
     - *Status:* `PARTIALLY_VERIFIED` in `source_registry.yaml` because the physical Gazette PDF has not yet been fetched to `regulations/current/packaged_commodities_rules/rules_2011_base.pdf` and SHA-256 is marked `PRIMARY_SOURCE_REQUIRED`.
  2. *Rule 7 Table-I Font Heights:* Minimum numeral/letter heights (1.0 mm, 1.5 mm, 2.0 mm, 4.0 mm, 6.0 mm) based on PDP area ($A_{\text{PDP}} \le 50$, $50 < A \le 100$, etc.).
     - *Provenance:* Derived from published LMPC Rules 2011 Table-I.
     - *Status:* `PARTIALLY_VERIFIED` (Primary source PDF retrieval required before promotion to `rules/current/`).
  3. *Unit Sale Price (USP) Requirement:* Mandatory declaration of price per standard unit (g/ml/kg/l) for packages exceeding threshold quantities.
     - *Provenance:* Cites G.S.R. 779(E) dated 2021-11-02 (`IN-LMPC-2021-GSR779E`).
     - *Status:* `PARTIALLY_VERIFIED` (Commencement date verified as 2022-12-01; local PDF artifact pending download).
  4. *Chapter II Statutory Exemptions (Rule 3):* Net quantity $\le 10\text{ g}$ or $\le 10\text{ ml}$, fast food packed by hotels/restaurants, bulk agricultural $> 25\text{ kg} / 25\text{ L}$.
     - *Provenance:* Cites Rule 3 of LMPC Rules 2011.
     - *Status:* `PARTIALLY_VERIFIED`.
  5. *References to G.S.R. 128(E), G.S.R. 312(E), G.S.R. 418(E):*
     - *Status:* Explicitly labeled `BLOCKED — PENDING PRIMARY SOURCE` in `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/CHANGE_IMPACT_MATRIX.md` and `docs/14_SUBMISSION/SOURCE_GAPS.md`. No rules have been authored from them.

---

## 4. Smart India Hackathon (SIH) Claims Audit

- **Claims Audited in Documentation:**
  1. *Problem Statement Identity:* Problem Statement 26034 titled "Automated Compliance Checking and Verification of Declarations on Pre-Packaged Commodities under Legal Metrology".
     - *Status:* `PARTIALLY_VERIFIED` (Standard working draft transcript; requires verification against official portal PDF upload).
  2. *Evaluation Rubric / Judging Weights:*
     - In [`docs/11_JUDGING/JUDGING_CRITERIA.md`](..\11_JUDGING\JUDGING_CRITERIA.md), relative weights are listed (Innovation 25%, Feasibility 25%, Scalability 20%, UX 15%, Presentation 15%).
     - *Finding:* Although explicitly prefaced with *"INTERNAL STRATEGIC FRAMEWORK — NOT OFFICIAL"*, the prompt mandates the explicit labeling:
       `ANALYST FRAMEWORK — NOT OFFICIAL SIH MARKING SHEET`.
     - *Correction Required:* Update notice banner to verbatim text mandated by policy.
  3. *Missing Judging Cases Mandated by Prompt:*
     - The prompt mandates: `PROBLEM_SOLVING_CASE.md` and `PROTOTYPE_CASE.md` in `docs/11_JUDGING/`.
     - *Finding:* These two specific documents were missing and must be added.
  4. *SIH Claim Verification Register:*
     - Mandated document `docs/14_SUBMISSION/SIH_CLAIM_VERIFICATION.md` must be created with columns: `claim`, `source`, `source_type`, `verification_status`, `last_verified`, `notes`.

---

## 5. Technical & Performance Claims Audit

- **Performance Claims in `docs/17_CLAIMS/PERFORMANCE_CLAIMS.md`:**
  - Character Error Rate ($\le 2.5\%$), Word Error Rate ($\le 5.0\%$), Font Measurement Error ($\le \pm 0.2\text{ mm}$), PDP Area IoU ($\ge 0.85$), End-to-End Latency ($\le 5.0\text{ s}$).
  - *Audit Finding:* All quantitative figures are strictly labeled as `TBD — MEASURE` or `EXPERIMENT_REQUIRED`. Zero fabricated empirical results exist.
- **Overclaiming of Implementation Status in Documentation:**
  - In [`docs/14_SUBMISSION/FINAL_FEATURES.md`](FINAL_FEATURES.md), the column "Implementation Stage" lists `Prototype Ready` for FEAT-01 through FEAT-11.
  - In [`docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`](..\01_PROBLEM_STATEMENT\PS_REQUIREMENTS_MATRIX.md), test files like `tests/e2e/test_capture.py` and `tests/vision/test_ocr.py` are listed as if they are currently implemented test suites.
  - In [`docs/01_PROBLEM_STATEMENT/REQUIREMENT_TRACEABILITY.md`](..\01_PROBLEM_STATEMENT\REQUIREMENT_TRACEABILITY.md), source files like `packages/extraction/address_parser.py` are mapped as active modules.
  - **CRITICAL AUDIT DEFECT:** The repository skeleton is currently in Phase 1 (Documentation + Governance + Schemas + Verification Scripts). The underlying application code in `packages/` and `apps/` is **PLANNED / ARCHITECTURALLY SPECIFIED**, not yet implemented.
  - **Correction Required:** Correct `FINAL_FEATURES.md`, `PS_REQUIREMENTS_MATRIX.md`, and `REQUIREMENT_TRACEABILITY.md` to clearly indicate:
    - Status: `PLANNED / ARCHITECTURAL SPECIFICATION COMPLETE`
    - Distinguish between implemented verification tests (`tests/unit/test_verification_pipeline.py`) and planned feature test suites.

---

## 6. Missing Provenance & Empty Placeholders

- **Primary Source Documents Pending Ingestion:**
  - `regulations/current/legal_metrology_act_2009/legal_metrology_act_2009.pdf` (Pending download)
  - `regulations/current/packaged_commodities_rules/rules_2011_base.pdf` (Pending download)
  - `regulations/amendments/packaged_commodities/gsr_629_e_2017.pdf` (Pending download)
  - `regulations/amendments/packaged_commodities/gsr_779_e_2021.pdf` (Pending download)
- **Empty Directories Tracked via `.gitkeep`:**
  - All subdirectories under `apps/`, `packages/`, `experiments/`, `benchmarks/`, `models/`, `assets/`, `infra/`, and `research/` currently contain `.gitkeep`.
  - *Recommendation:* Add foundational README files in `research/` establishing that research papers, blogs, and secondary reports (such as `ch-deep-research-report.md`) constitute research discovery input only and never legal authority.

---

## 7. Verification Tooling Audit

- **Existing Verification Scripts:**
  - `verify_legal_sources.py` (Functional, passes)
  - `verify_rule_registry.py` (Functional, passes)
  - `verify_claims.py` (Functional, passes)
  - `verify_dataset_manifest.py` (Functional, passes)
  - `verify_report_provenance.py` (Functional, passes)
- **Missing Tooling Mandated by Policy (Section Z):**
  - Prompt Section Z explicitly requires:
    `scripts/verification/verify_repository_integrity.py`
  - *Correction Required:* Author `scripts/verification/verify_repository_integrity.py` to enforce overall repository structural invariants, rule placement safety, duplicate registry checks, and claim evidence validation in one master CI command.

---

## 8. Summary of Corrective Action Plan

1. **Create `docs/14_SUBMISSION/SIH_CLAIM_VERIFICATION.md`** auditing all SIH-related claims.
2. **Create `docs/11_JUDGING/PROBLEM_SOLVING_CASE.md`** and `docs/11_JUDGING/PROTOTYPE_CASE.md`.
3. **Update `docs/11_JUDGING/JUDGING_CRITERIA.md`** to prominently display `ANALYST FRAMEWORK — NOT OFFICIAL SIH MARKING SHEET`.
4. **Correct Implementation Overclaiming** in `docs/14_SUBMISSION/FINAL_FEATURES.md`, `PS_REQUIREMENTS_MATRIX.md`, and `REQUIREMENT_TRACEABILITY.md` by explicitly designating application components as `PLANNED` / `SPECIFIED`.
5. **Align Source Registry Field Names** in `regulations/source_registry.yaml` and `scripts/verification/verify_legal_sources.py` to support exact schema fields (`issuing_authority`, `document_sha256`, `local_artifact`, `retrieval_date`, `verification_date`, `effective_from`, `effective_to`).
6. **Implement `scripts/verification/verify_repository_integrity.py`** and integrate into Makefile / CI.
7. **Add `research/README.md`** establishing the research quarantine policy.
8. **Generate `docs/14_SUBMISSION/AUDIT_SUMMARY.md`** detailing all modifications.
