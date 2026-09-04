# Data Flow Specification

## Purpose
Details the exact data transformations, ingestion pipelines, serialization formats, and state transitions from raw photographic capture to final PDF inspection dossier.

## Scope
Traces payload structures across UI, API, vision pipeline, rule engine, and database.

## Authoritative Inputs
- `rules/schema/evidence.schema.json`
- `rules/schema/rule.schema.json`

## Assumptions
- Data flows strictly in a forward-traceable, immutable graph sequence.

## Open Questions
- None.

## Dependencies
- `packages/`

## Verification Requirements
- Schema validation must pass at each stage of the data flow.

---

## End-to-End Data Pipeline

```
Raw Camera Frame (JPEG/PNG)
       │
       ▼ [Hash Stage]
Compute SHA-256 Checksum: H(I_raw)
       │
       ▼ [Quality Gate]
Check Laplacian Variance & Glare Histogram
       │  ├── Fails Threshold → Terminate & Return REQUEST_RETAKE
       │  └── Passes Threshold → Proceed
       ▼ [Calibration Stage]
Locate Fiducial / Reference Marker
       │  ├── Found → Calculate Scale: S (mm/px) ± delta
       │  └── Not Found → Set Calibration Status = UNCALIBRATED
       ▼ [Observation Layer]
Run Text Detection (Polygons) & Multilingual OCR (Tokens + Confidences)
Segment Principal Display Panel (PDP Polygon)
       │
       ▼ [Field Extraction]
Map OCR Tokens to Mandatory Rule 6 Fields:
  {mrp, net_qty, mfg_date, manufacturer, origin, generic_name, consumer_care}
       │
       ▼ [Measurement Engine]
Calculate:
  1. Area of PDP: A_pdp (cm^2)
  2. Font Height: H_font (mm) = H_pixel * S
       │
       ▼ [Regulatory Snapshot Loading]
Extract Mfg Date → Resolve Epoch → Load Active Machine Rules from rules/current/
       │
       ▼ [Deterministic Rule Evaluation]
Execute Evaluator(Observations, ActiveRules)
Output per Rule: PASS | FAIL | REVIEW | NOT_APPLICABLE
       │
       ▼ [Human Review Screen]
Inspector reviews overlays, overrides false positives/negatives if necessary,
enters justification notes.
       │
       ▼ [Dossier Generation]
Generate Immutable Dossier JSON & Signed PDF
Append entry to Audit Log with timestamp and officer ID.
```
