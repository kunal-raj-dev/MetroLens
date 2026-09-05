# System Acceptance Criteria (Gherkin / Given-When-Then)

## Purpose
Defines the binary pass/fail criteria required for feature sign-off, staging deployment, and hackathon demonstration readiness.

## Scope
Covers guided capture, quality gate, calibration, declaration extraction, compliance evaluation, and dossier export.

## Authoritative Inputs
- `docs/03_PRODUCT_REQUIREMENTS/FUNCTIONAL_REQUIREMENTS.md`

## Assumptions
- Acceptance tests are executed against synthetic packages and validated physical test items.

## Open Questions
- None.

## Dependencies
- `tests/e2e/`
- `tests/rules/`

## Verification Requirements
- All acceptance scenarios must pass in automated CI or manual staging walk-throughs.

---

## Acceptance Test Scenarios

### Scenario AC-01: Blurry Capture Rejection
- **Given** an authorized inspector is capturing the Principal Display Panel,
- **When** the camera captures an image with Laplacian blur variance below threshold ($\sigma^2 < 100.0$),
- **Then** the system must reject the frame,
- **And** display a user-facing prompt: "Image too blurry. Please stabilize device and retake."
- **And** refuse to execute downstream OCR until a sharp image is acquired.

### Scenario AC-02: Missing Calibration Reference Handling
- **Given** a captured sharp image of a retail carton without any physical reference target,
- **When** the system runs the calibration module,
- **Then** the calibration status must evaluate to `UNCALIBRATED`,
- **And** the physical font height measurement rule must evaluate to `REVIEW`,
- **And** the UI must inform the officer: "Physical calibration reference not detected. Font height requires physical verification."

### Scenario AC-03: Mandatory Declaration Omission Detection
- **Given** a packaged commodity image missing the mandatory "Consumer Care" contact details,
- **When** the deterministic rule engine evaluates Rule 6(1)(n),
- **Then** the declaration extraction engine must flag consumer care details as `NOT_FOUND`,
- **And** the rule verdict must evaluate to `FAIL`,
- **And** the evidence dossier must highlight the missing field in red with statutory citation Rule 6(1)(n).

### Scenario AC-04: Regulatory Snapshot Time Machine
- **Given** a packaged commodity manufactured on `2015-06-15`,
- **When** the inspector enters `2015-06-15` as the date of manufacture,
- **Then** the system must load regulatory snapshot `EPOCH-2011-BASE`,
- **And** it must NOT evaluate against the Unit Sale Price (USP) mandate introduced in 2021 (G.S.R. 779(E)),
- **And** mark the USP check as `NOT_APPLICABLE` for that historical package.
