# Final Features Summary & Implementation Discipline Register

## Purpose
Summarizes the complete catalog of features in Nirikshak, detailing their precise implementation lifecycle stage in accordance with the Architecture Claim Discipline Policy.

## Multi-Dimensional Feature Governance Taxonomy

In accordance with the Anti-Hallucination and Architecture Claim Discipline Policy, software features are NEVER described as `VERIFIED_PRIMARY`. Legal authority, software implementation maturity, and empirical evidence are evaluated across three distinct orthogonal dimensions:

### 1. Legal Basis Status (`legal_basis_status`)
- `VERIFIED_PRIMARY`: Directly mapped to an authenticated Level 1 primary government instrument verified on disk.
- `VERIFIED_SECONDARY`: Derived from official guidance, procedural manuals, or statutory time-of-manufacture principles.
- `PRIMARY_SOURCE_REQUIRED`: Mapped to a known regulatory clause whose primary gazette publication is pending retrieval.
- `NOT_APPLICABLE`: Engineering, optical, cryptographic, or system tooling capability without direct statutory mandate.

### 2. Implementation Status (`implementation_status`)
- `PLANNED`: Feature is architecturally specified in documentation; underlying production application code is not yet authored.
- `IMPLEMENTED`: Production-oriented code is complete on disk and passes static checks.
- `TESTED`: Unit and integration test suites exist on disk and pass automated regression runs.
- `BENCHMARKED`: Empirical benchmark runs executed against standardized datasets with logged results.

### 3. Evidence Status (`evidence_status`)
- `NONE`: Design-stage specification; no empirical measurement claim asserted.
- `EXPERIMENT_REQUIRED`: Technical or optical capability requiring empirical bench validation before quantitative claims are made.
- `VERIFIED`: Backed by an existing empirical report or executable automated test on disk.
- `PARTIALLY_VERIFIED`: Confirmed under limited test conditions; broader benchmark pending.
- `REJECTED`: Disproven or rejected.

> [!IMPORTANT]
> A feature is NEVER labeled `IMPLEMENTED` or `TESTED` merely because its design documentation exists.

---

## Feature Lifecycle & Multi-Dimensional Governance Register

| Feature ID | Feature Name | Architectural Domain | Legal Basis Status | Implementation Status | Evidence Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FEAT-01** | Guided Multi-Panel Capture | Frontend / Vision | VERIFIED_SECONDARY | PLANNED | NONE | Procedural multi-panel inspection requirement |
| **FEAT-02** | Image Quality Gate (Blur/Glare) | Vision Optics | NOT_APPLICABLE | PLANNED | NONE | Optical capture guardrail |
| **FEAT-03** | Planar Reference Calibration | Metrology / Calibration | NOT_APPLICABLE | PLANNED | EXPERIMENT_REQUIRED | Reference target homography pipeline |
| **FEAT-04** | Multilingual OCR Pipeline | AI Observation | VERIFIED_SECONDARY | PLANNED | EXPERIMENT_REQUIRED | Observational text extraction |
| **FEAT-05** | Rule 6(1) Declaration Extractor | Extraction & Normalization | PRIMARY_SOURCE_REQUIRED | PLANNED | NONE | Mapped to Rule 6(1) declaration list |
| **FEAT-06** | PDP Segmentation & Area Calc | Metrology Geometry | PRIMARY_SOURCE_REQUIRED | PLANNED | EXPERIMENT_REQUIRED | Rule 7(1) geometric explanations |
| **FEAT-07** | Calibrated Font Height Check | Measurement Engine | PRIMARY_SOURCE_REQUIRED | PLANNED | EXPERIMENT_REQUIRED | Table-I statutory numeral height checks |
| **FEAT-08** | Regulatory Time-Machine | Legal Metrology Engine | VERIFIED_SECONDARY | PLANNED | NONE | Non-retroactivity epoch resolution |
| **FEAT-09** | Cryptographic Evidence Graph | Systems & Evidence | VERIFIED_SECONDARY | PLANNED | NONE | Section 63 BSA 2023 provenance DAG |
| **FEAT-10** | Tamper-Evident PDF Dossier | Reporting | NOT_APPLICABLE | PLANNED | NONE | Inspection report generation |
| **FEAT-11** | Full Offline Execution | Edge Runtime | NOT_APPLICABLE | PLANNED | NONE | Offline SQLite/local engine |
| **FEAT-12** | Parametric Cylinder Dewarping | Vision Optics | NOT_APPLICABLE | PLANNED | EXPERIMENT_REQUIRED | Unwrapping cylindrical package labels |
| **VERIF-01** | Legal Source Verifier | CI Verification Script | NOT_APPLICABLE | TESTED | VERIFIED | `scripts/verification/verify_legal_sources.py` |
| **VERIF-02** | Rule Registry Verifier | CI Verification Script | NOT_APPLICABLE | TESTED | VERIFIED | `scripts/verification/verify_rule_registry.py` |
| **VERIF-03** | Claims Verifier | CI Verification Script | NOT_APPLICABLE | TESTED | VERIFIED | `scripts/verification/verify_claims.py` |
| **VERIF-04** | Dataset Manifest Verifier | CI Verification Script | NOT_APPLICABLE | TESTED | VERIFIED | `scripts/verification/verify_dataset_manifest.py` |
| **VERIF-05** | Repository Integrity Verifier | CI Verification Script | NOT_APPLICABLE | TESTED | VERIFIED | `scripts/verification/verify_repository_integrity.py` |
