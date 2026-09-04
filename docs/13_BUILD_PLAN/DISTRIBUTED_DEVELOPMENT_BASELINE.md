# Distributed Development Baseline

## Purpose
This document establishes the binding engineering baseline, code ownership boundaries, package interface contracts, branching strategy, and governance rules for distributed development across all teammates on the Nirikshak project.

---

## 1. Governance Principles & Invariants

1. **Zero Premature Code Without Interface Freezing**:
   No teammate may implement private internal data structures that cross package boundaries. All cross-package data flow must strictly use the frozen contracts in `packages/shared/src/nirikshak_shared/models/`.
2. **Statutory Source vs Machine-Readable Rule Separation**:
   `METROLENS_LEGAL_SOURCE_PACK/` is the primary statutory corpus of official Gazette notifications and Acts.
   > **Invariant**: Having an official PDF does NOT make it an active machine-readable rule.
   Rules in `rules/current/` must strictly possess `status: IN_FORCE` and `verification_status: VERIFIED_PRIMARY` with explicit statutory references and effective dates. Unverified or proposed changes belong exclusively in `rules/proposed/`.
3. **Historical / Research Snapshots**:
   Documents in `ALL-IN-ONE context/` or exploratory files are research snapshots and are **NOT** canonical. The structured directories under `docs/`, `rules/`, `regulations/`, and `packages/` constitute the sole source of truth.
4. **Deterministic Compliance Decision**:
   Generative AI / LLMs must never be used to decide legal compliance or penalties. Compliance is evaluated solely by deterministic code executing machine-readable rules against verified optical measurements and extracted text.

---

## 2. Directory Lifecycle Classification

| Category | Policy | Target Directories | Lifecycle Action |
| :--- | :--- | :--- | :--- |
| 🟢 **Empty by Design** | Keep `.gitkeep` | `experiments/*`, `benchmarks/results/`, `benchmarks/runs/`, `data/raw/`, `data/processed/`, `data/synthetic/`, `models/weights/`, `models/cards/`, `assets/demo/`, `assets/screenshots/` | Artifact directories populated only when experiments, runs, or benchmark executions produce physical files. |
| 🟡 **Runtime Packages** | Package Bootstrap | `packages/*`, `apps/api`, `apps/worker`, `apps/web` | Bootstrapped with package definitions (`pyproject.toml` / `package.json`), entry points, typed public interfaces, and automated tests. |
| 🔴 **Infrastructure** | Concrete Setup | `infra/db/`, `infra/docker/`, `infra/deployment/`, `infra/monitoring/`, `infra/storage/` | Contains concrete configuration, initialization scripts (`init.sql`), Dockerfiles, and environment templates. |

---

## 3. Subsystem & Repository Ownership Matrix

| Area | Package / Path | Technical Owner | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Shared Contracts** | `packages/shared/` | System Architect | Core domain models, schemas, shared exceptions, serialization contracts. |
| **Vision & Quality** | `packages/vision/` | Computer Vision Lead | Frame quality gate (blur/glare detection), panel segmentation (PDP polygon). |
| **Calibration** | `packages/calibration/` | CV / Measurement Lead | Optical fiducial detection (AruCo/coin/strip), pixel-to-mm scale factor $S$, uncertainty bounds. |
| **OCR Pipeline** | `packages/ocr/` | AI / OCR Lead | Multilingual text detection and recognition, bounding boxes, word/line tokenization. |
| **Field Extraction** | `packages/extraction/` | Extraction Lead | Mapping OCR tokens to Rule 6 mandatory declarations (MRP, Net Qty, Dates, Address). |
| **Measurement** | `packages/measurement/` | Metrology Lead | Metric font height computation ($H_{\text{font}} = H_{\text{px}} \times S$), PDP area computation ($A_{\text{pdp}}$). |
| **Rules Engine** | `packages/rules-engine/` | Legal / Rules Lead | Deterministic rule evaluation against `rules/current/`, rule applicability, verdict generation. |
| **Evidence System** | `packages/evidence/` | Evidence / Security Lead | Cryptographic hashing (SHA-256), immutable DAG evidence chain creation, chain-of-custody. |
| **Reporting** | `packages/reporting/` | Reporting Lead | Legal Metrology Inspection Dossier generation (ReportLab PDF and structured JSON). |
| **API Backend** | `apps/api/` | Backend Lead | REST endpoints, authentication, job orchestration, database persistence. |
| **Worker Service** | `apps/worker/` | Pipeline / Integration Lead | Asynchronous pipeline execution, queue consumption, multi-stage task runner. |
| **Web Frontend** | `apps/web/` | Frontend Lead | Inspector verification UI, bounding box overlays, manual review and sign-off workflow. |
| **Infrastructure** | `infra/` | DevOps / Infra Lead | Docker Compose, PostgreSQL schemas/migrations, storage layout, telemetry. |
| **Legal Regulations** | `regulations/`, `rules/` | Legal Engineering Lead | Gazette harvesting, rule authoring, statutory verification, regulatory lifecycle. |

---

## 4. Package Interface Ownership & Seams

Every package is bound by the following interface contracts. All data transfer objects (DTOs) are imported from `nirikshak_shared.models`.

```
========================================================================================
                                 NIRIKSHAK PIPELINE SEAMS
========================================================================================

  [Raw Inspection Frame] (Image Bytes / Path)
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. packages/vision (Quality Gate)                            │
  │    • Input:  image_bytes: bytes, min_laplacian: float       │
  │    • Output: QualityGateResult (passed: bool, blur, glare)  │
  │    • Error:  ERR_IMAGE_BLUR, ERR_IMAGE_GLARE                │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 2. packages/calibration (Scale Computation)                 │
  │    • Input:  image: np.ndarray, marker_type: MarkerType     │
  │    • Output: CalibrationResult (scale_mm_per_px, status)    │
  │    • Error:  ERR_CALIBRATION_FAILED                         │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 3. packages/ocr (Text Observation)                          │
  │    • Input:  image: np.ndarray, languages: List[str]        │
  │    • Output: List[OCRObservation]                           │
  │    • Error:  ERR_OCR_EMPTY, ERR_OCR_ENGINE_FAULT            │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 4. packages/extraction (Mandatory Field Mapping)            │
  │    • Input:  observations: List[OCRObservation]             │
  │    • Output: Dict[str, DeclarationField]                    │
  │    • Error:  ERR_EXTRACTION_MISSING_MANDATORY               │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 5. packages/measurement (Metric Dimensions)                 │
  │    • Input:  declarations, observations, calibration        │
  │    • Output: Dict[str, MeasurementResult]                   │
  │    • Error:  ERR_MEASUREMENT_UNCALIBRATED                   │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 6. packages/rules-engine (Deterministic Compliance)         │
  │    • Input:  declarations, measurements, active_rules       │
  │    • Output: List[RuleEvaluation]                           │
  │    • Error:  ERR_RULE_SCHEMA_INVALID                        │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 7. packages/evidence (Cryptographic Chain of Custody)       │
  │    • Input:  image_sha256, evaluations, measurements        │
  │    • Output: List[EvidenceItem] (DAG nodes)                 │
  │    • Error:  ERR_EVIDENCE_HASH_MISMATCH                     │
  └─────────────────────────────────────────────────────────────┘
           │
           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 8. packages/reporting (Inspection Dossier Generation)       │
  │    • Input:  InspectionResult, officer_info, template       │
  │    • Output: DossierReport (pdf_bytes: bytes, json_payload) │
  │    • Error:  ERR_REPORT_GENERATION_FAILED                   │
  └─────────────────────────────────────────────────────────────┘
```

### Detailed Package Contracts

#### `packages/shared` (`nirikshak_shared`)
- **Input**: Domain primitives and external payloads.
- **Output**: Canonical Pydantic schemas (`InspectionRequest`, `InspectionResult`, `OCRObservation`, `DeclarationField`, `MeasurementResult`, `RuleEvaluation`, `EvidenceItem`, `InspectionError`).
- **Error States**: `ValidationError` on malformed schema inputs.
- **Dependencies**: `pydantic>=2.6.0`.
- **Test Contract**: Validates roundtrip serialization, JSON Schema compatibility with `rules/schema/evidence.schema.json`, and immutability invariants.

#### `packages/vision` (`nirikshak_vision`)
- **Input**: Raw image bytes or numpy array, variance thresholds.
- **Output**: `QualityGateResult` (Laplacian variance, glare pixel ratio, boolean pass/fail flag) and segmented PDP polygon.
- **Error States**: Raises `InspectionError(code="ERR_IMAGE_BLUR")` or `InspectionError(code="ERR_IMAGE_GLARE")` if unprocessable.
- **Dependencies**: `nirikshak_shared`, `opencv-python-headless`, `numpy`.
- **Test Contract**: Passes test fixtures for sharp image, blurry image, and high-glare image.

#### `packages/calibration` (`nirikshak_calibration`)
- **Input**: Preprocessed image frame and reference marker target parameters.
- **Output**: `CalibrationResult` containing `physical_scale_mm_per_pixel`, `uncertainty_mm_per_pixel`, and `calibration_status`.
- **Error States**: Returns `UNCALIBRATED` status if no valid marker detected; raises `InspectionError(code="ERR_CALIBRATION_FAILED")` in strict mode.
- **Dependencies**: `nirikshak_shared`, `opencv-python-headless`, `numpy`.
- **Test Contract**: Tested against synthetic marker images with known scale ground truths.

#### `packages/ocr` (`nirikshak_ocr`)
- **Input**: Preprocessed image or cropped region of interest (ROI).
- **Output**: `List[OCRObservation]` with normalized bounding boxes, confidence score, text string, and detected language.
- **Error States**: Raises `InspectionError(code="ERR_OCR_EMPTY")` when no text is detected.
- **Dependencies**: `nirikshak_shared`, `rapidocr-onnxruntime` or `paddleocr`.
- **Test Contract**: Tested with standardized package label test images.

#### `packages/extraction` (`nirikshak_extraction`)
- **Input**: `List[OCRObservation]`.
- **Output**: `Dict[str, DeclarationField]` containing normalized fields for: `mrp`, `net_quantity`, `mfg_date`, `expiry_date`, `manufacturer_name`, `country_of_origin`, `consumer_care`.
- **Error States**: Flags absent mandatory fields with `is_present=False` without raising fatal runtime crashes.
- **Dependencies**: `nirikshak_shared`.
- **Test Contract**: Tested against sample label token streams with known ground truth extractions.

#### `packages/measurement` (`nirikshak_measurement`)
- **Input**: `DeclarationField`, `List[OCRObservation]`, and `CalibrationResult`.
- **Output**: `Dict[str, MeasurementResult]` including numeral font height (mm), PDP area ($\text{cm}^2$), and line spacing.
- **Error States**: If calibration is missing, records pixel measurements with `calibration_status=UNCALIBRATED`.
- **Dependencies**: `nirikshak_shared`, `numpy`, `shapely`.
- **Test Contract**: Verifies correct mathematical scaling $H_{\text{font}} = H_{\text{px}} \times S$ and tolerance calculations.

#### `packages/rules-engine` (`nirikshak_rules_engine`)
- **Input**: `Dict[str, DeclarationField]`, `Dict[str, MeasurementResult]`, and active rules loaded from `rules/current/`.
- **Output**: `List[RuleEvaluation]` with verdicts (`PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`), statutory citations, and reasoning notes.
- **Error States**: Raises `InspectionError(code="ERR_RULE_SCHEMA_INVALID")` if a rule file violates schema.
- **Dependencies**: `nirikshak_shared`, `pyyaml`, `jsonschema`.
- **Test Contract**: Tested against verified test fixtures in `rules/tests/`.

#### `packages/evidence` (`nirikshak_evidence`)
- **Input**: Raw image bytes, `List[RuleEvaluation]`, `Dict[str, MeasurementResult]`.
- **Output**: `List[EvidenceItem]` conforming to `rules/schema/evidence.schema.json` with SHA-256 hash digests.
- **Error States**: Raises `InspectionError(code="ERR_EVIDENCE_HASH_MISMATCH")` if integrity checks fail.
- **Dependencies**: `nirikshak_shared`.
- **Test Contract**: Verifies that every evidence node is cryptographically linked and schema-compliant.

#### `packages/reporting` (`nirikshak_reporting`)
- **Input**: `InspectionResult`, officer signature/ID, issuing authority metadata.
- **Output**: PDF inspection dossier bytes and structured JSON summary.
- **Error States**: Raises `InspectionError(code="ERR_REPORT_GENERATION_FAILED")`.
- **Dependencies**: `nirikshak_shared`, `reportlab`.
- **Test Contract**: Generates a valid, readable PDF document and validates provenance checksums.

---

## 5. Development Workflow & Git Rules

### Branch Naming Standard
Every pull request must originate from an isolated feature branch named according to:
- Feature: `feat/<issue-id>-<short-description>` (e.g. `feat/12-aruco-calibration`)
- Bug fix: `fix/<issue-id>-<short-description>` (e.g. `fix/24-mrp-currency-regex`)
- Test addition: `test/<issue-id>-<short-description>` (e.g. `test/30-rule-6-fixtures`)
- Documentation: `docs/<issue-id>-<short-description>` (e.g. `docs/45-adr-007-storage`)

### Main Branch Rule
- **Direct commits to `main` are strictly forbidden.**
- All code enters `main` exclusively through Pull Requests with at least 1 peer approval and passing CI.

### Issue-to-Merge Lifecycle
```
[Issue / User Story]
         │
         ▼
[Definition of Ready (DoR) Validated]
         │
         ▼
[Create Branch: feat/<id>-<desc>]
         │
         ▼
[Local Implementation & Unit Tests]
         │
         ▼
[Pass Local Verification: pytest + verify_repository_integrity.py]
         │
         ▼
[Open Pull Request against main]
         │
         ▼
[Automated CI & Code Review Approval]
         │
         ▼
[Squash & Merge into main]
```

---

## 6. Verification Checklist Before Opening a PR

Prior to requesting code review, each teammate must execute:
1. `python -m pytest` (all unit and contract tests must pass with 0 errors).
2. `python scripts/verification/verify_repository_integrity.py` (master repository integrity must pass 100%).
3. Check that no mock files or temporary artifacts were committed into green artifact directories.
