# Master Criterion-to-Evidence Matrix (Judge Defense Specifications)

## Purpose
Transforms SIH judging criteria into an actionable, data-driven defense matrix for every major engineering capability of Nirikshak.

## Scope
Provides complete technical justifications, proof points, benchmark references, and Q&A answers.

## Authoritative Inputs
- `docs/11_JUDGING/JUDGING_CRITERIA.md`
- `docs/17_CLAIMS/`

## Assumptions
- Judges will probe edge cases, legal authority, optical accuracy, and differentiation from generic mobile scanner apps.

## Dependencies
- `benchmarks/`
- `docs/11_JUDGING/DEMO_SCRIPT.md`

## Verification Requirements
- Team members must master the question-and-answer defenses detailed below.

---

## Executable Feature Defense Profiles

### Feature Profile: FEAT-01 (Physical Millimetre Calibration)
- **Feature ID:** `FEAT-01`
- **Feature:** Physical Reference-Object Scale Calibration ($\text{mm/pixel}$)
- **Problem:** Generic smartphone cameras output pixels, not millimetres. Distance and focal length variations make raw pixel counts legally useless for Rule 7 font compliance.
- **Innovation:** Sub-pixel fiducial ellipse detection combined with planar homography rectification to calculate exact optical scale factor $S$ ($\text{mm/px}$) with bounded uncertainty $\pm \delta\text{ mm}$.
- **Implementation:** `packages/calibration/target_detector.py`, `packages/measurement/font_estimator.py`
- **Evidence:** `experiments/calibration/`, `tests/vision/test_calibration.py`
- **Benchmark:** Protocol PROTO-CALIB-001 (Determine achievable measurement error experimentally; Acceptance threshold: `TBD — MEASURE`; Status: `TBD_MEASURE`)
- **Live Demo:** Live placement of calibrated reference card adjacent to package; system visualizes detected scale and calculated physical height.
- **Failure Case:** Marker missing or occluded $\rightarrow$ system automatically defaults dimensional rules to `REVIEW`.
- **Scalability:** Standardized printed calibration fiducials (production cost estimate: TARGET — NOT VALIDATED; Status: `TBD — MEASURE`).
- **UX:** Real-time green bounding circle highlighting detected reference target on camera preview.
- **Judge Question:** *"Why can't you just use depth sensors or ArCore without a physical sticker?"*
- **Answer:** *"Depth sensors on consumer smartphones exhibit significant depth uncertainty at close inspection ranges (under 30 cm), which can exceed statutory font height thresholds. In legal metrology, physical planar reference calibration provides mathematically provable optical scale required for evidentiary scrutiny."*

---

### Feature Profile: FEAT-02 (Regulatory Time-Machine Versioning)
- **Feature ID:** `FEAT-02`
- **Feature:** Regulatory Snapshot Engine (Time-Machine)
- **Problem:** Packaged goods have multi-year shelf lives. Enforcing the newest 2022 rules on an inventory unit packed lawfully in 2018 is a statutory violation.
- **Innovation:** Deterministic snapshot resolution mapping declared manufacturing date to active statutory epochs.
- **Implementation:** `packages/rules-engine/snapshot_manager.py`, `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/effective_dates.yaml`
- **Evidence:** `tests/rules/test_time_machine.py`
- **Benchmark:** Unit test coverage across 3 historical regulatory epochs.
- **Live Demo:** Inspector toggles date from 2016 to 2024; system activates/deactivates Unit Sale Price (USP) check dynamically.
- **Failure Case:** Date unreadable $\rightarrow$ UI prompts officer to enter declared date manually or flags `REVIEW`.
- **Scalability:** New Gazette amendments ingested via YAML schemas without modifying core Python codebase.
- **UX:** Clear badge showing *"Active Legal Epoch: G.S.R. 779(E) (2022-Present)"*.
- **Judge Question:** *"Why not just use an LLM to read the latest law from the web?"*
- **Answer:** *"LLMs hallucinate subsection numbers, confuse proposed draft rules with gazetted law, and invent exemptions. Our system uses versioned, human-verified declarative schemas with exact Gazette SHA-256 hashes, ensuring zero hallucination."*

---

### Feature Profile: FEAT-03 (Tamper-Evident Evidence Graph)
- **Feature ID:** `FEAT-03`
- **Feature:** Cryptographic Provenance DAG & Dossier Generation
- **Problem:** Blurry photos and subjective inspection memos get thrown out during judicial compounding hearings.
- **Innovation:** Directed Acyclic Graph linking raw camera SHA-256 hashes, crop polygons, OCR token scores, calibrated measurements, and officer sign-offs into a tamper-evident PDF dossier.
- **Implementation:** `packages/evidence/graph_builder.py`, `packages/reporting/pdf_generator.py`
- **Evidence:** `tests/unit/test_dossier.py`, `scripts/verification/verify_report_provenance.py`
- **Benchmark:** Dossier generation latency $\le 2.0\text{ s}$ (Status: `TBD — MEASURE`).
- **Live Demo:** Officer reviews side-by-side crop, enters digital signature, and exports verifiable PDF with embedded QR checksum.
- **Failure Case:** Byte tampering with stored image breaks SHA-256 validation immediately on audit.
- **Scalability:** Generates lightweight standalone PDF/JSON files distributable via email, WhatsApp, or departmental portals.
- **UX:** Side-by-side visual comparison showing the physical crop alongside the statutory requirement.
- **Judge Question:** *"Is this report automatically admissible in an Indian court?"*
- **Answer:** *"No, and we deliberately do not claim that. Admissibility of electronic records is governed by the competent court under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023. Our system provides complete cryptographic provenance and chain-of-custody to assist the authorized officer in establishing authenticity."*
