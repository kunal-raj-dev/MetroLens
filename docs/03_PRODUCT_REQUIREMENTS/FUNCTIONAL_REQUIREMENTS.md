# Functional Requirements Specification

## Purpose
Defines the functional requirements (FRs) for the Nirikshak automated inspection assistance system.

## Scope
Covers guided capture, computer vision, optical character recognition, physical calibration, deterministic rule checking, audit trails, and reporting.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rules 6, 7, 8, 9, 10, 11).
- `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`.

## Assumptions
- Functional features operate in both online and standalone offline modes.

## Open Questions
- Standard export format requirements for State Legal Metrology departmental management systems [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/`
- `apps/`

## Verification Requirements
- Every requirement must pass acceptance criteria detailed in `docs/03_PRODUCT_REQUIREMENTS/ACCEPTANCE_CRITERIA.md`.

---

## Functional Requirements Matrix

### FR-01: Guided Multi-Panel Capture
- **FR-01.1:** The system shall guide the operator to capture all visible exterior panels of a package (Principal Display Panel, Rear Panel, Top, Bottom, Sides).
- **FR-01.2:** The system shall support both rectangular cartons and cylindrical containers.
- **FR-01.3:** The capture interface shall display an overlay guide assisting the operator in positioning the calibration target within the camera plane.

### FR-02: Image Quality Gate
- **FR-02.1:** The system shall compute a blur score (e.g. Laplacian variance) on every captured image before downstream inference.
- **FR-02.2:** If blur score falls below threshold $\theta_{\text{blur}}$, the system shall reject the frame and prompt `REQUEST_RETAKE`.
- **FR-02.3:** The system shall detect severe specular reflection/glare across text regions and warn the operator.

### FR-03: Physical Scale Calibration
- **FR-03.1:** The system shall detect a standardized physical reference target within the image and calculate the real-world scale factor $S$ in $\text{mm/pixel}$.
- **FR-03.2:** If no reference target is detected, the system shall disable automatic millimeter-scale pass/fail evaluations and flag dimensional rules as `REVIEW`.
- **FR-03.3:** The system shall calculate an uncertainty bound ($\pm \delta\text{ mm}$) for all physical measurements.

### FR-04: Principal Display Panel (PDP) Segmentation & Area Computation
- **FR-04.1:** The system shall identify the Principal Display Panel bounding polygon.
- **FR-04.2:** For rectangular packages, PDP area shall be computed as $H \times W$.
- **FR-04.3:** For cylindrical packages, the system shall compute statutory PDP area as $40\%$ of total cylinder surface area ($0.40 \times \pi \times D \times H$).

### FR-05: Optical Character Recognition & Field Extraction
- **FR-05.1:** The system shall extract text tokens and character bounding polygons across all panels.
- **FR-05.2:** The system shall classify and extract the 7 mandatory declarations under Rule 6(1).
- **FR-05.3:** The system shall support multilingual numeral and text recognition (English and Devanagari numerals).

### FR-06: Deterministic Compliance Evaluation
- **FR-06.1:** The system shall evaluate extracted data against verified machine-readable rules.
- **FR-06.2:** The rule engine shall evaluate the package against the regulatory snapshot corresponding to the package manufacturing date.
- **FR-06.3:** Every rule check shall return strictly one of: `PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`.

### FR-07: Cryptographic Evidence & Dossier Generation
- **FR-07.1:** The system shall generate SHA-256 hashes of all raw captured images at ingestion.
- **FR-07.2:** The system shall assemble an immutable Evidence Graph linking raw photos, crops, OCR tokens, measurements, and rule verdicts.
- **FR-07.3:** The system shall export a tamper-evident PDF inspection dossier and machine-readable JSON summary.
