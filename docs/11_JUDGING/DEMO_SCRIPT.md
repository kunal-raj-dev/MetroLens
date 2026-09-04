# Live Demonstration Runbook & Script

## Purpose
Provides the minute-by-minute execution steps, backup procedures, package setup instructions, and narrative cues for the live hackathon demonstration.

## Scope
Universal for the demonstration team during live jury evaluation.

## Authoritative Inputs
- `docs/11_JUDGING/CRITERION_EVIDENCE_MATRIX.md`
- `assets/sample_packages/`

## Assumptions
- The demonstration environment has a physical desk with 2 physical test packages and a standardized calibration card.

## Dependencies
- `apps/web/`
- `apps/api/`

## Verification Requirements
- Team must run a complete dry run before judges arrive.

---

## Live Demonstration Steps (2 Minutes 30 Seconds)

### Step 1: Quality Gate & Blur Detection (30 Seconds)
- **Action:** Open guided capture on `localhost:3000`. Aim camera at retail biscuit box while shaking the phone slightly.
- **Narrative:** *"Notice our real-time Image Quality Gate. The system instantly detects high Laplacian variance blur and refuses to waste compute or hallucinate on degraded pixels. Once the officer holds steady—green light!"*
- **Visual:** Instant transition from Red *"REQUEST_RETAKE: Blurry"* to Green *"SHARP"*.

### Step 2: Physical Scale Calibration & PDP Segmentation (40 Seconds)
- **Action:** Place standard calibration card adjacent to package face. Capture front panel.
- **Narrative:** *"Pixels are not millimetres. Watch how Nirikshak instantly detects the circular reference target, establishes exact physical scale in mm per pixel, segments the Principal Display Panel, and computes its statutory area as 124 cm²."*
- **Visual:** Blue bounding ellipse on marker; cyan polygon on PDP face with area readout.

### Step 3: Mandatory Declaration Extraction & Font Measurement (40 Seconds)
- **Action:** Ingest rear and side panels. Run rule evaluation.
- **Narrative:** *"In under 3 seconds [DESIGN TARGET: < 3 seconds — NOT EMPIRICALLY VALIDATED ON TARGET HARDWARE], all 7 mandatory declarations are extracted and normalized. Look at the Net Quantity: the OCR reads 'Net Wt: 200g', and our measurement engine calculates the numeral height as 2.15 mm. Checking Table-I for a 124 cm² PDP, the statutory minimum is 2.0 mm—verdict: PASS!"*
- **Visual:** Green bounding boxes around Manufacturer, Origin, Net Qty, MRP, and Consumer Care.

### Step 4: The Regulatory Time-Machine Demo (20 Seconds)
- **Action:** Toggle manufacturing date to `2016-05-10`.
- **Narrative:** *"Now watch our Regulatory Time-Machine. A package made in 2016 cannot be penalized under the 2021 Unit Sale Price amendment. Notice how the USP rule immediately toggles to NOT_APPLICABLE based on the historical regulatory snapshot!"*
- **Visual:** USP status badge dynamically switches from PASS to NOT_APPLICABLE.

### Step 5: Cryptographic Dossier Generation (20 Seconds)
- **Action:** Tap *"Finalize & Sign Dossier"*. Export PDF.
- **Narrative:** *"The officer signs off, and Nirikshak generates an immutable, tamper-evident inspection dossier embedding raw image SHA-256 hashes, exact Table-I citations, and measurement crops ready for supervisory review."*
- **Visual:** Downloaded PDF with embedded cryptographic hashes and side-by-side evidence crops.
