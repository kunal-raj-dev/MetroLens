# REST API CONTRACT & SCHEMA SPECIFICATION (V1.0)
# MetroLens AI™ — Web Inspection API Specification
### Document Status: Authoritative Interface Contract | Protocol: HTTP/REST (OpenAPI 3.1)
**Base URL:** `/api/v1` | **Content-Type:** `multipart/form-data` (Uploads) / `application/json` (Responses)

---

## 1. Executive Purpose & Contract Stability

This document defines the authoritative, frozen HTTP API contract connecting the **React Web Frontend (`apps/web`)** and the **FastAPI Backend Gateway (`apps/api`)**. 

To allow the frontend lead (M4) and backend leads (M1, M2, M3, M6) to build concurrently without interface churn, all endpoints, request parameters, JSON response schemas, and failure status codes defined here are binding.

---

## 2. API Endpoint Directory

| Method | Endpoint | Description | Consumes | Produces |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/inspect` | Uploads packaging image and returns synchronous compliance audit dossier. | `multipart/form-data` | `application/json` |
| `GET` | `/api/v1/health` | Service health, memory footprint, and ONNX model readiness probe. | None | `application/json` |
| `POST` | `/api/v1/report/pdf` | Generates a tamper-evident SHA-256 sealed assessment report PDF. | `application/json` | `application/pdf` |
| `POST` | `/api/v1/emaap/mock-sync` | Simulates e-Governance synchronization with national LM portal. | `application/json` | `application/json` |

---

## 3. Detailed Endpoint Specifications

### 3.1. `POST /api/v1/inspect` (Primary Inspection Endpoint)

Executes synchronous image ingestion, binary security validation, metric scale calibration, multilingual OCR, entity normalization, and statutory rule evaluation.

#### Request Headers
- `Content-Type`: `multipart/form-data`
- `X-Request-ID`: Optional client tracing UUID string.

#### Form-Data Parameters
| Field Name | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `file` | `Binary (File)` | **YES** | — | Packaging image payload (JPEG, PNG, or WebP; max 15MB). |
| `anchor_type` | `String (Enum)` | NO | `"INR_10_COIN"` | Calibration reference: `"INR_10_COIN"`, `"ISO_CARD"`, or `"NONE"`. |
| `panel_type` | `String (Enum)` | NO | `"FRONT_PDP"` | Panel view: `"FRONT_PDP"`, `"BACK_INFO"`, or `"ALL_IN_ONE"`. |
| `officer_id` | `String` | NO | `"WEB-GUEST"` | Identifier of inspecting officer or test session. |

---

#### Success Response (`HTTP 200 OK`)

```json
{
  "inspection_id": "INSP-20260905-8741",
  "timestamp": "2026-09-05T01:15:30.120Z",
  "state": "POTENTIAL_NON_COMPLIANCE",
  "summary_reason": "Rule 6(11) Unit Sale Price arithmetic discrepancy detected; font height for net quantity conforms to Rule 7 Table-I.",
  
  "image_metadata": {
    "filename": "cashew_pouch_front.jpg",
    "width_px": 2400,
    "height_px": 3200,
    "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "is_quality_valid": true,
    "blur_score": 245.8,
    "glare_percentage": 2.1
  },

  "calibration": {
    "is_calibrated": true,
    "anchor_type": "INR_10_COIN",
    "coin_detected": true,
    "scale_mm_per_px": 0.125,
    "pdp_width_mm": 95.0,
    "pdp_height_mm": 140.0,
    "pdp_area_cm2": 133.0,
    "calibration_confidence": 0.96
  },

  "declarations": {
    "commodity_name": "Premium Roasted Cashews",
    "mrp_inr": 240.0,
    "tax_qualifier_present": true,
    "net_quantity_value": 200.0,
    "net_quantity_unit": "g",
    "declared_usp_value": 1.20,
    "declared_usp_unit": "g",
    "mfg_month": 8,
    "mfg_year": 2026,
    "manufacturer_name": "MetroLens Foods Pvt Ltd",
    "manufacturer_pincode": "110001",
    "consumer_care_email": "support@metrolens.in",
    "consumer_care_phone": "1800-11-4000",
    "country_of_origin": "India"
  },

  "rule_evaluations": {
    "rule6_mandatory_status": {
      "overall_status": "PASS",
      "missing_declarations": [],
      "details": {
        "manufacturer_details": "PASS",
        "net_quantity": "PASS",
        "mrp": "PASS",
        "usp": "PASS",
        "mfg_date": "PASS",
        "consumer_care": "PASS"
      }
    },

    "usp_audit": {
      "is_compliant": false,
      "declared_usp": 1.20,
      "expected_usp": 1.20,
      "discrepancy_pct": 0.0,
      "standard_denominator": "g",
      "notes": "Unit declared as 'per gm' instead of statutory standard symbol 'per g' under Rule 6(11)"
    },

    "font_height_audit": {
      "is_compliant": true,
      "pdp_area_cm2": 133.0,
      "statutory_min_height_mm": 2.0,
      "measured_net_qty_height_mm": 2.24,
      "deficit_mm": 0.0,
      "benefit_of_doubt_applied": false
    },

    "exemption_status": {
      "is_exempt": false,
      "statutory_clause": null
    }
  },

  "improvement_notice": {
    "recommended": true,
    "act_provision": "Section 36(1) read with Jan Vishwas Act 2026",
    "cure_period_days": 15,
    "statutory_grounds": "Violation of Rule 6(11) of the Legal Metrology (Packaged Commodities) Rules, 2011: Use of non-standard unit symbol 'gm' for Unit Sale Price declaration."
  },

  "evidence_crops": [
    {
      "field_name": "net_quantity",
      "label": "Net Quantity & USP Crop",
      "bbox_px": [420, 1850, 680, 240],
      "measured_height_mm": 2.24,
      "confidence": 0.94,
      "crop_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
    },
    {
      "field_name": "mrp",
      "label": "MRP & Taxes Declaration",
      "bbox_px": [420, 1620, 550, 180],
      "measured_height_mm": 2.10,
      "confidence": 0.96,
      "crop_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
    }
  ],

  "telemetry": {
    "total_duration_ms": 1420,
    "stages_ms": {
      "quality_gate": 24,
      "metric_calibration": 86,
      "ocr_perception": 780,
      "normalization": 35,
      "rule_engine": 8,
      "evidence_packaging": 487
    }
  }
}
```

---

### 3.2. `GET /api/v1/health` (Readiness & Health Probe)

Reports system readiness, active worker threads, and local ONNX model runtime status.

#### Success Response (`HTTP 200 OK`)
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 14250,
  "system": {
    "cpu_percent": 12.4,
    "memory_used_mb": 284.5,
    "memory_total_mb": 8192.0
  },
  "models": {
    "paddleocr_onnx_det": "loaded_cpu_int8",
    "paddleocr_onnx_rec": "loaded_cpu_int8",
    "scale_calibrator": "ready"
  },
  "rules_engine": {
    "status": "active",
    "ruleset_version": "2026.09-JanVishwas-v1.0",
    "verified_rules_count": 4
  }
}
```

---

### 3.3. `POST /api/v1/report/pdf` (Tamper-Evident Report Generator)

Compiles an official, printable **Image-Based Compliance Assessment Report PDF** embedding SHA-256 hashes, Section 36(1) notice text, and visual evidence crops.

#### Request Body (`application/json`)
```json
{
  "inspection_id": "INSP-20260905-8741",
  "officer_notes": "First inspection during wholesale market surveillance in Chandni Chowk.",
  "include_raw_image": true
}
```

#### Response (`HTTP 200 OK`)
- `Content-Type`: `application/pdf`
- `Content-Disposition`: `attachment; filename="metrolens_report_INSP-20260905-8741.pdf"`
- Body: Binary PDF stream containing digital certificate and SHA-256 provenance footer.

---

### 3.4. `POST /api/v1/emaap/mock-sync` (e-Governance Mock Adapter)

Simulates the National eMaap Legal Metrology portal webhook synchronization.

#### Request Body (`application/json`)
```json
{
  "inspection_id": "INSP-20260905-8741",
  "jurisdiction_code": "DL-01-CENTRAL",
  "officer_id": "LMO-DELHI-42",
  "compliance_state": "POTENTIAL_NON_COMPLIANCE",
  "improvement_notice_issued": true,
  "dossier_sha256": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
}
```

#### Response (`HTTP 200 OK`)
```json
{
  "sync_status": "ACCEPTED_FOR_RECORD",
  "emaap_reference_no": "EMAAP-DL-2026-009182",
  "received_at": "2026-09-05T01:15:35.402Z",
  "tamper_verification": "VERIFIED_VALID"
}
```

---

## 4. Standardized Error Contract & Taxonomy

When an operation fails, the API strictly returns a uniform error structure:

```json
{
  "error": {
    "code": "IMAGE_TOO_LARGE",
    "message": "The uploaded packaging image exceeds the 15.0 MB file size limit.",
    "details": {
      "file_size_bytes": 18450120,
      "max_allowed_bytes": 15728640
    },
    "remediation": "Please resize or compress your image and try again.",
    "timestamp": "2026-09-05T01:15:31.005Z"
  }
}
```

### Complete Error Code Taxonomy

| HTTP Status | Error Code (`code`) | Trigger Condition | Recommended User Remediation |
| :--- | :--- | :--- | :--- |
| `400` | `INVALID_IMAGE_PAYLOAD` | Missing file stream or corrupted multipart form data. | Select a valid image file. |
| `413` | `IMAGE_TOO_LARGE` | Upload exceeds 15.0 MB size limit. | Compress or downsample image under 15MB. |
| `415` | `UNSUPPORTED_MEDIA_TYPE` | Magic bytes do not match JPEG, PNG, or WebP. | Upload a genuine JPEG, PNG, or WebP photo. |
| `422` | `DECOMPRESSION_BOMB_DETECTED` | Image exceeds 64 Megapixels (`MAX_IMAGE_PIXELS`). | Upload a standard camera resolution image. |
| `422` | `IMAGE_CORRUPTED` | PIL or OpenCV decoder fails to parse raster pixels. | Re-take photograph or export from graphics tool. |
| `422` | `IMAGE_RESOLUTION_TOO_LOW` | Image resolution is below $800 \times 600$ pixels. | Capture at higher resolution to allow text reading. |
| `429` | `RATE_LIMIT_EXCEEDED` | Client IP exceeded 10 inspection requests per minute. | Please wait 60 seconds before submitting again. |
| `500` | `PIPELINE_EXECUTION_ERROR` | Internal Python runtime exception during processing. | Contact technical team with inspection ID. |
| `504` | `PROCESSING_TIMEOUT` | CPU inference exceeded 5.0-second watchdog limit. | Upload a sharper, single-panel crop. |

---

## 5. Pydantic Python Schema Definitions (Backend Reference)

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class ComplianceState(str, Enum):
    GREEN = "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED"
    RED = "POTENTIAL_NON_COMPLIANCE"
    AMBER = "MANUAL_REVIEW_REQUIRED"
    BLUE = "STATUTORY_EXEMPTION_APPLIED"
    GRAY = "NOT_IMAGE_VERIFIABLE"

class UnitType(str, Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    METER = "m"
    NUMBER = "N"
    PIECE = "piece"

class EvidenceCrop(BaseModel):
    field_name: str
    label: str
    bbox_px: List[int] = Field(..., description="[x, y, width, height]")
    measured_height_mm: Optional[float] = None
    confidence: float
    crop_base64: str

class CanonicalDeclaration(BaseModel):
    commodity_name: Optional[str] = None
    mrp_inr: Optional[float] = None
    tax_qualifier_present: bool = False
    net_quantity_value: Optional[float] = None
    net_quantity_unit: Optional[UnitType] = None
    declared_usp_value: Optional[float] = None
    declared_usp_unit: Optional[str] = None
    mfg_month: Optional[int] = None
    mfg_year: Optional[int] = None
    manufacturer_name: Optional[str] = None
    manufacturer_pincode: Optional[str] = None
    consumer_care_email: Optional[str] = None
    consumer_care_phone: Optional[str] = None
    country_of_origin: Optional[str] = None

class InspectionResponse(BaseModel):
    inspection_id: str
    timestamp: str
    state: ComplianceState
    summary_reason: str
    image_metadata: Dict[str, Any]
    calibration: Dict[str, Any]
    declarations: CanonicalDeclaration
    rule_evaluations: Dict[str, Any]
    improvement_notice: Dict[str, Any]
    evidence_crops: List[EvidenceCrop]
    telemetry: Dict[str, Any]
```
