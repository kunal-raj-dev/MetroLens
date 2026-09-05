# User Journeys & Operational Workflows

## Purpose
Maps the step-by-step user interactions across capture, quality gating, automated inspection, human review, and dossier generation.

## Scope
Defines end-to-end user workflows for field inspections and supervisory reviews.

## Authoritative Inputs
- Standard enforcement procedure under Section 15 (Power of inspection, seizure) of the Legal Metrology Act, 2009.

## Assumptions
- The user operates a tablet or mobile device with a rear-facing camera.

## Open Questions
- Departmental protocol for multi-officer joint inspections [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `apps/web/`
- `docs/03_PRODUCT_REQUIREMENTS/FUNCTIONAL_REQUIREMENTS.md`

## Verification Requirements
- Every workflow step must have corresponding UI states and error handlers.

---

## Primary Field Inspection Journey (Happy Path)

```
[Start Inspection]
       │
       ▼
[Select Commodity Type & Input Mfg Date]
       │
       ▼
[Guided Multi-Panel Capture: Front/PDP, Back, Sides]
       │
       ▼
[Automatic Image Quality Gate: Blur & Glare Check]
       │  ├── If Degraded: Prompt [Retake Panel X]
       │  └── If Clean: Proceed
       ▼
[Optical Calibration: Reference Marker Detection]
       │  ├── If Not Found: Default Physical Measurement to REVIEW
       │  └── If Found: Compute mm/px scale & uncertainty
       ▼
[Automated Observation & Extraction]
       │  ├── OCR Text Detection & Normalization
       │  ├── PDP Boundary Segmentation & Area Calculation
       │  └── Font Height Measurement of Numerals
       ▼
[Deterministic Rule Evaluation (Snapshot based on Mfg Date)]
       │  ├── PASS: All declarations present & verified
       │  ├── FAIL: Missing declaration or sub-threshold font
       │  └── REVIEW: Borderline font or ambiguous text
       ▼
[Officer Verification & Annotation]
       │  └── Officer confirms or adjusts bounding boxes/readings
       ▼
[Generate Signed Cryptographic Dossier (PDF & JSON)]
```
