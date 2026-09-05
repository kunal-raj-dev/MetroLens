# Evidence Model Specification

## Purpose
Specifies the entity-relationship model, JSON schemas, and graph linkages used to construct an immutable inspection evidence dossier.

## Scope
Covers raw captures, crops, visual overlays, OCR tokens, calibration records, rule evaluations, and officer review actions.

## Authoritative Inputs
- `rules/schema/evidence.schema.json`
- Bharatiya Sakshya Adhiniyam, 2023 principles.

## Assumptions
- An evidence model must enable complete backward and forward auditability: any finding can be traced to the exact raw pixels that generated it.

## Open Questions
- None.

## Dependencies
- `packages/evidence/`

## Verification Requirements
- All generated dossiers must validate against `scripts/verification/verify_report_provenance.py`.

---

## Evidence Graph Structure (DAG Entities)

```
                       ┌──────────────────────┐
                       │ InspectionSession    │
                       │ - session_id         │
                       │ - officer_id         │
                       │ - timestamp_utc      │
                       └──────────┬───────────┘
                                  │ 1..n
                                  ▼
                       ┌──────────────────────┐
                       │ CapturedPanelImage   │
                       │ - panel_name         │
                       │ - raw_image_sha256   │
                       │ - calibration_record │
                       └──────────┬───────────┘
                                  │ 1..n
                                  ▼
                       ┌──────────────────────┐
                       │ EvidenceCrop         │
                       │ - bounding_box       │
                       │ - crop_sha256        │
                       │ - optical_confidence │
                       └──────────┬───────────┘
                                  │ 1..n
                                  ▼
                       ┌──────────────────────┐
                       │ RuleEvaluationRecord │
                       │ - rule_id            │
                       │ - verdict (PASS/FAIL)│
                       │ - measured_value     │
                       │ - statutory_limit    │
                       └──────────┬───────────┘
                                  │ 1..1
                                  ▼
                       ┌──────────────────────┐
                       │ OfficerAttestation   │
                       │ - confirmed (Y/N)    │
                       │ - officer_signature  │
                       │ - notes              │
                       └──────────────────────┘
```
