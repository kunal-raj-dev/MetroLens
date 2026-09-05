# CURRENT STATE: MEMBER 5 — BASELINE M5-4
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Timestamp:** 2026-09-05T17:56:00+05:30  
**Phase:** Chunk M5-4 Baseline Audit — Declaration Table, Evidence Linking & Inspector Review  

---

## 1. M5-3 Actual State Audit

| Area | Implementation State | Verification Evidence | Operational Reality |
| :--- | :--- | :--- | :--- |
| **Model Alignment** | `FrontendInspectionModel` with `OCRTokenModel` & `DeclarationModel` | `src/types/frontend.ts` | Complete (Minor fix needed for `imagePath` optional prop) |
| **Canvas Transform Engine** | Pure affine geometry: `imageToCanvas`, `canvasToImage`, `fitToScreen`, `zoomAt`, ray-casting | `src/features/inspection/canvasTransform.ts` | Verified & passing 20/20 unit tests |
| **Compliance Dashboard** | Multi-modal verdict visualizer, quality gate, calibration badge, telemetry, synthetic disclaimer | `src/features/inspection/ComplianceDashboard.tsx` | Complete & rendering |
| **Evidence Canvas** | HTML5 Canvas, High-DPI support, polygon outlines, zoom/pan/fit/reset, token selection, tooltip | `src/features/inspection/EvidenceCanvas.tsx` | Complete & interactive |
| **Accessible Evidence List** | Synchronized keyboard-navigable listbox exposing OCR text, confidence, script outside canvas | `EvidenceCanvas.tsx` DOM panel | Functional |
| **Workstation Integration** | Dual-column layout connecting upload dropzone to canvas & dashboard | `src/app/page.tsx` | Functional (Build regression fixed in M5-4 setup) |
| **M5-2 Verification Suite** | 34 automated unit tests for validation, normalizer, and adapters | `src/__tests__/m5_2_verification.test.ts` | 34/34 passing |
| **M5-3 Verification Suite** | 20 automated unit tests for canvas affine transforms and ray casting | `src/__tests__/canvas_transform.test.ts` | 20/20 passing |

---

## 2. Frontend Model & Available Fields

From `src/types/contract.ts` and `src/types/frontend.ts`:
- **Declarations Available:**
  - `fieldName` (e.g. `mrp`, `net_quantity`, `unit_sale_price`, `date_of_mfg`, `expiry_date`, `manufacturer`, `packer`, `consumer_care`, `country_of_origin`)
  - `label` (Human-readable title)
  - `rawText` (Transcribed OCR string)
  - `normalizedValue` (Parsed entity, e.g. `{ value: 65, unit: "g" }` or number)
  - `confidence` (Extraction confidence 0.0 - 1.0)
  - `isMandatory` (boolean)
  - `isPresent` (boolean)
  - `boundingBox` (`{ xMin, yMin, xMax, yMax }`)
  - `polygon` (`[number, number][]` 4-point coordinates)
  - `verdict` (`RuleVerdict`: `"PASS"` | `"FAIL"` | `"REVIEW"` | `"NOT_APPLICABLE"`)
  - `evaluationNotes` (Statutory rationale summary)
  - `sourceTokenIds` (`string[]` mapping to `OCRTokenModel.id`)
- **Rules Available:**
  - `rule_id`, `rule_title`, `verdict`, `statutory_reference`, `observed_summary`, `required_summary`, `evidence_ids`
- **Evidence Available:**
  - `evidence_id`, `image_sha256`, `panel_name`, `bounding_box`, `calibration_status`, `physical_scale_mm_per_pixel`, `observed_value`, `operator_annotation`
- **Measurements Available:**
  - `feature_name`, `measured_pixels`, `scale_factor_mm_per_pixel`, `measured_mm`, `uncertainty_mm`, `calibration_status`, `bounding_box`

---

## 3. Backend Review API Support Status

- **Actual Backend State:**
  - Inspecting `apps/api/main.py`: Currently provides `GET /health`, `POST /api/v1/inspect`, `POST /api/v1/inspections`, and `GET /api/v1/inspections/{id}`.
  - **No review submission endpoint exists on the backend yet.**
  - **Status:** `REVIEW API PENDING MEMBER 4`.
  - Frontend will implement the service boundary with clean adapter abstraction:
    - Mock Synthetic Adapter: Handles simulated review flow for demonstration and automated testing, labeled `SYNTHETIC DEMO`.
    - Live API Adapter: Defensively raises/reports that review submission is pending backend deployment. No fake network calls will be made.

---

## 4. Inviolable Invariant Verification Plan for M5-4
1. No legal calculation in client (no `if (mrp < x)` or verdict synthesis).
2. No physical measurement in client (no mm height math; only pixel coordinates mapped to original image space).
3. Explicit identifier linkage: Declarations link to OCR tokens via `sourceTokenIds`, not text heuristics.
4. Support for both single and multiple token evidence highlighting.
5. Review modal maintains strict state isolation (no state leakage between declarations).
6. 100% type-safe TypeScript with no `any` evasion.
7. Zero git commits, zero git pushes.
