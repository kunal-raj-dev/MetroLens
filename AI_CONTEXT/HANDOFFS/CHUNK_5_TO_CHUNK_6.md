# HANDOFF: CHUNK 5 (VERTICAL SLICE 0) TO CHUNK 6 (INSPECTION UI & EVIDENCE VIEWER)

**From**: Member 1 (AI & Multilingual OCR Lead / System Architect)  
**To**: Member 4 (Frontend Lead) & Member 5 (Reporting & Integration Lead)  
**Date**: September 5, 2026  
**Artifact Status**: READY FOR FRONTEND BINDING  

---

## 1. What Is Delivered in Chunk 5
Vertical Slice 0 is complete, passing all 98 automated tests, and outperforming the Synchronous Web MVP latency SLA by 8.7x (214 ms actual vs 2000 ms limit).

The backend API is live and accepts packaging images directly:
- **Endpoint**: `POST /api/v1/inspect`
- **Method**: HTTP POST
- **Encoding**: `multipart/form-data`
- **Parameters**:
  - `file`: Packaging surface image file (JPEG, PNG, WebP) [Required, max 15MB]
  - `anchor_type`: Calibration hint (`"AUTO"`, `"COIN"`, `"ARUCO"`, `"NONE"`) [Default: `"AUTO"`]
  - `officer_id`: Badge/ID of inspecting officer [Default: `"INSP-OFFICER"`]
  - `brand_name`: Optional brand metadata string [Default: `null`]
  - `product_type`: Optional commodity category [Default: `null`]
- **Response**: HTTP 200 OK with fully populated canonical `InspectionResult` Pydantic model.

---

## 2. Canonical Contract Schema for Frontend Consumption

The response JSON conforms strictly to `nirikshak_shared.models.contracts.InspectionResult`:

```json
{
  "inspection_id": "insp_30662e0a6bcb",
  "status": "SUCCESS",
  "image_sha256": "a2d9be5d51ef95e0b4fc79eecc3fe3a5bf72c5d88012163113ff0af6c265af15",
  "overall_verdict": "NON_COMPLIANT",
  "quality_gate_passed": true,
  "calibration_status": "CALIBRATED",
  "declarations": {
    "mrp": {
      "field_name": "mrp",
      "raw_text": "MRP Rs 150.00 (Incl. of all taxes)",
      "normalized_value": "150.00",
      "confidence": 0.98,
      "bounding_box": { "x_min": 50.0, "y_min": 110.0, "x_max": 420.0, "y_max": 140.0 },
      "is_present": true,
      "source_token_ids": ["token_002"]
    },
    "net_quantity": {
      "field_name": "net_quantity",
      "raw_text": "Net Quantity: 500 g",
      "normalized_value": "500 g",
      "confidence": 0.99,
      "bounding_box": { "x_min": 50.0, "y_min": 170.0, "x_max": 300.0, "y_max": 200.0 },
      "is_present": true,
      "source_token_ids": ["token_003"]
    }
  },
  "measurements": {
    "net_quantity_font_height": {
      "feature_name": "net_quantity_font_height",
      "measured_pixels": 30.0,
      "measured_mm": 4.25,
      "uncertainty_mm": 0.08,
      "calibration_status": "CALIBRATED",
      "bounding_box": { "x_min": 50.0, "y_min": 170.0, "x_max": 300.0, "y_max": 200.0 }
    }
  },
  "rule_evaluations": [
    {
      "rule_id": "LMPC-R06-MRP-001",
      "rule_title": "Maximum Retail Price (MRP) Declaration",
      "verdict": "PASS",
      "statutory_reference": "Rule 6(1)(e)",
      "observed_summary": "MRP Rs 150.00 (Incl. of all taxes) declared",
      "required_summary": "Retail sale price inclusive of all taxes must be declared.",
      "uncertainty_flag": false
    },
    {
      "rule_id": "LMPC-R07-FONT-HEIGHT-001",
      "rule_title": "Minimum Numeral Height (Table-I)",
      "verdict": "PASS",
      "statutory_reference": "Rule 7, Table-I",
      "observed_summary": "Measured numeral height: 4.25 mm (Net Qty: 500 g)",
      "required_summary": "Net quantity 200g-1000g requires minimum 4.0 mm font height.",
      "uncertainty_flag": false
    }
  ],
  "evidence_chain": [
    {
      "evidence_id": "ev_decl_mrp_token_002",
      "image_sha256": "a2d9be5d51ef95e0b4fc79eecc3fe3a5bf72c5d88012163113ff0af6c265af15",
      "bounding_box": { "x_min": 50.0, "y_min": 110.0, "x_max": 420.0, "y_max": 140.0 },
      "calibration_status": "CALIBRATED",
      "physical_scale_mm_per_pixel": 0.1416,
      "observed_value": {
        "raw_text": "MRP Rs 150.00 (Incl. of all taxes)",
        "normalized_value": "150.00",
        "ocr_confidence": 0.98
      }
    }
  ],
  "telemetry": {
    "ingestion_ms": 5.79,
    "quality_gate_ms": 22.42,
    "calibration_ms": 16.05,
    "ocr_perception_ms": 169.55,
    "semantic_extraction_ms": 0.20,
    "measurement_ms": 0.02,
    "rules_engine_ms": 0.05,
    "evidence_assembly_ms": 0.06,
    "total_ms": 214.19
  },
  "errors": []
}
```

---

## 3. UI Requirements for Member 4 (Chunk 6)
1. **Inspection Submission Flow**:
   - Multi-format file drag-and-drop or camera frame capture (JPEG, PNG, WebP).
   - Display optical quality feedback immediately if `quality_gate_passed == false` (e.g. "Image blurry or excessive glare. Please retake.").
2. **5-State Status Badge**:
   - `COMPLIANT` (Green)
   - `NON_COMPLIANT` (Red)
   - `SUSPECT_REVIEW` (Amber)
   - `INCONCLUSIVE` (Gray)
3. **Side-by-Side Evidence Viewer**:
   - Render uploaded image with SVG/Canvas bounding box overlays using coordinates from `evidence_chain` (`x_min`, `y_min`, `x_max`, `y_max` in pixel space).
   - Clicking a rule evaluation highlights the corresponding evidence bounding box on the image.
4. **Statutory Rule Checklist**:
   - Display Rule 6 mandatory declaration statuses (MRP, Net Qty, Mfg Date, Consumer Care, Origin).
   - Display Rule 7 Table-I minimum font height measurement and required threshold.
5. **Officer Review & Audit Action**:
   - One-tap approval or override with audit justification notes.

---

## 4. Non-Blocking Gaps Deferred to Chunk 7
- **PDF Dossier Generation**: `dossier_pdf_path` is currently null. Member 5 will hook `packages/reporting` to generate signed PDF audit certificates in Chunk 7.
