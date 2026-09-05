# Non-Functional Requirements Specification

## Purpose
Establishes the performance, security, reliability, maintainability, and usability constraints governing the Nirikshak system.

## Scope
Applies to client applications, backend services, inference runtimes, and local data persistence.

## Authoritative Inputs
- SIH prototype operational standards.
- ISO/IEC 25010 Software Product Quality Standard.

## Assumptions
- Systems operate locally on standard field laptop or portable tablet hardware.

## Open Questions
- Target frame rate for real-time mobile camera preview processing [TBD — MEASURE].

## Dependencies
- `infra/`
- `benchmarks/protocols/`

## Verification Requirements
- Every non-functional requirement must be evaluated using benchmark protocols in `benchmarks/protocols/`.

---

## Non-Functional Requirements Matrix

### NFR-01: Latency & Performance
- **NFR-01.1:** Quality gate validation (blur & glare assessment) shall complete within $\le 300\text{ ms}$ per frame.
- **NFR-01.2:** End-to-end multi-panel inspection (capture $\rightarrow$ OCR $\rightarrow$ calibration $\rightarrow$ rule evaluation) shall complete within $\le 5.0\text{ s}$ per package on CPU.
- **NFR-01.3:** PDF inspection dossier generation shall complete within $\le 2.0\text{ s}$.

### NFR-02: Reliability & Offline Autonomy
- **NFR-02.1:** The core inspection engine must be capable of $100\%$ autonomous execution without internet access.
- **NFR-02.2:** Local SQLite/PostgreSQL storage must persist captured inspections across abrupt power loss without data corruption.

### NFR-03: Security & Cryptographic Integrity
- **NFR-03.1:** All raw captures must be hashed with SHA-256 immediately upon memory ingestion.
- **NFR-03.2:** Inspection audit logs must follow append-only semantics. Any alteration of historic inspection records must fail integrity validation.
- **NFR-03.3:** Role-Based Access Control (RBAC) must restrict administrative functions (updating rules, modifying thresholds) to authenticated administrators.

### NFR-04: Accuracy & Measurement Uncertainty
- **NFR-04.1:** Physical scale calibration error must not exceed $\pm 0.2\text{ mm}$ on calibrated planar surfaces.
- **NFR-04.2:** In all instances where measurement uncertainty overlaps with a statutory pass/fail boundary, the system must trigger a mandatory `REVIEW` verdict rather than false certainty.

### NFR-05: Usability & Ergonomics
- **NFR-05.1:** UI must provide high-contrast text and intuitive bounding box visualization for field use under sunlight or warehouse lighting.
- **NFR-05.2:** Operator action buttons must be touch-friendly with minimum touch target size of $48 \times 48\text{ dp}$.
