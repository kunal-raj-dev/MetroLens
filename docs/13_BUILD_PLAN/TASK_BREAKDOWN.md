# Detailed Task Breakdown (WBS)

## Purpose
Provides an actionable Work Breakdown Structure (WBS) mapping discrete technical tasks, owners, dependencies, and verification criteria.

## Scope
Covers all work packages leading up to the SIH prototype submission.

## Authoritative Inputs
- `docs/13_BUILD_PLAN/ROADMAP.md`
- `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`

## Assumptions
- Tasks are completed iteratively and committed to feature branches.

## Dependencies
- `packages/`
- `apps/`

## Verification Requirements
- Every task must link to a tangible code or documentation deliverable.

---

## Work Breakdown Structure

### Track A: Computer Vision & Optics
- **TASK-A1:** Implement Laplacian variance blur filter and specular glare mask (`packages/vision/quality_gate.py`).
- **TASK-A2:** Implement fiducial target detector and $\text{mm/px}$ scale estimator (`packages/calibration/target_detector.py`).
- **TASK-A3:** Implement Principal Display Panel boundary segmenter and area calculator (`packages/vision/pdp_segmenter.py`).
- **TASK-A4:** Implement parametric cylinder dewarping unroller (`packages/vision/dewarping.py`).
- **TASK-A5:** Implement numeral font height bounding box estimator (`packages/measurement/font_estimator.py`).

### Track B: Optical Character Recognition & Extraction
- **TASK-B1:** Integrate local PaddleOCR/CRNN multilingual inference pipeline (`packages/ocr/engine.py`).
- **TASK-B2:** Author regex and token classification parsers for Rule 6(1) declarations (`packages/extraction/rule6_parser.py`).
- **TASK-B3:** Build unit conversion and metric normalization pipeline (`packages/extraction/normalizer.py`).

### Track C: Legal Informatics & Rule Engine
- **TASK-C1:** Author Pydantic validators matching `rule.schema.json` (`packages/rules-engine/models.py`).
- **TASK-C2:** Implement deterministic rule evaluator and 4-state state machine (`packages/rules-engine/evaluator.py`).
- **TASK-C3:** Implement Regulatory Snapshot Time-Machine manager (`packages/rules-engine/snapshot_manager.py`).
- **TASK-C4:** Build unit test suite covering 4-vector matrix for all rules (`tests/rules/`).

### Track D: Evidence, Security & Reporting
- **TASK-D1:** Implement SHA-256 stream hasher and crop graph builder (`packages/evidence/graph_builder.py`).
- **TASK-D2:** Implement append-only cryptographic audit logger (`packages/evidence/audit_log.py`).
- **TASK-D3:** Build PDF inspection dossier generator using ReportLab (`packages/reporting/pdf_generator.py`).

### Track E: Applications & User Interface
- **TASK-E1:** Build guided multi-panel camera capture workflow in React/Next.js (`apps/web/`).
- **TASK-E2:** Implement FastAPI ingestion endpoints and session controller (`apps/api/`).
- **TASK-E3:** Build interactive bounding box inspection and officer attestation UI (`apps/web/`).
