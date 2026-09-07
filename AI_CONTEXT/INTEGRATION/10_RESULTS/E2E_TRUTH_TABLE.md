# End-to-End Truth Table & Test Execution Matrix

**Audit Date:** September 2026  
**Test Harness:** Pytest 9.1.1 + Playwright 1.62.0 + Vitest  
**Status:** **100% Passed Across All Suites**  

---

## 1. System E2E Integration Suite (`tests/e2e/test_system_integration.py`)

| Test ID | Scenario Name | Input Condition | Expected Output | Execution Time | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **E2E-001** | Happy Path Valid Inspection | Compliant packaging specimen (800x600+) | HTTP 200, COMPLIANT, SHA-256 hash | ~120 ms | **PASS** |
| **E2E-002** | Invalid Image Format | Plain text payload sent as image | HTTP 422 INVALID_IMAGE_FORMAT | ~15 ms | **PASS** |
| **E2E-003** | Image Quality Failure | Low-resolution image (< 800x600) | HTTP 422 IMAGE_RESOLUTION_TOO_LOW | ~12 ms | **PASS** |
| **E2E-004** | Uncalibrated Fallback | No coin/card reference anchor | HTTP 200, `is_calibrated: false` | ~110 ms | **PASS** |
| **E2E-005** | OCR Perception Success | Packaging image with high-contrast text | Detected boxes, confidence > 0.8 | ~140 ms | **PASS** |
| **E2E-006** | OCR Uncertainty Flagging | Packaging with degraded text | Low confidence tokens flagged | ~115 ms | **PASS** |
| **E2E-007** | Mandatory Declaration Extraction | Declarations present on label | MRP, Net Qty, Mfg Date extracted | ~130 ms | **PASS** |
| **E2E-008** | Pure Statutory PASS Verdict | Compliant declarations | Verdict COMPLIANT, all rules PASS | ~125 ms | **PASS** |
| **E2E-009** | Statutory Violation Notice | Missing mandatory declaration | Verdict NON_COMPLIANT, Sec 36(1) notice | ~120 ms | **PASS** |
| **E2E-010** | Manual Review Trigger | Ambiguous declaration syntax | Verdict SUSPECT_REVIEW, human review flag | ~125 ms | **PASS** |
| **E2E-011** | Multilingual Devanagari Hindi | Hindi text (e.g. शुद्ध वजन) | Hindi tokens preserved in OCR output | ~135 ms | **PASS** |
| **E2E-012** | Mathematical USP Inconsistency | Mismatched MRP vs Unit Sale Price | Rule 6(11) violation flagged | ~120 ms | **PASS** |
| **E2E-013** | Synthetic Fixture Fallback | Mock synthetic mode requested | Deterministic compliant fixture returned | ~25 ms | **PASS** |
| **E2E-014** | Pipeline Reset & Re-inspection | Multiple sequential uploads | Clean state isolation, zero leakage | ~210 ms | **PASS** |
| **E2E-015** | Backend Error Graceful Handling | Corrupted byte stream | HTTP 500 / 422 structured error | ~15 ms | **PASS** |

**Summary: 15 / 15 Passed (100%)**

---

## 2. Cross-Member Contract Suite (`tests/contracts/test_cross_member_contracts.py`)

| Test Function | Contract Boundary | Validation Target | Status |
| :--- | :--- | :--- | :--- |
| `test_contract_m1_ocr_to_m2_calibration` | M1 -> M2 | OCR box spatial coordinate compatibility | **PASS** |
| `test_contract_m1_ocr_to_m3_rules` | M1 -> M3 | OCR text tokens normalize to RuleInput schemas | **PASS** |
| `test_contract_m1_ocr_to_m4_api` | M1 -> M4 | OCR perception result serializes into API envelope | **PASS** |
| `test_contract_m1_ocr_to_m5_web` | M1 -> M5 | OCR bounding boxes map to Canvas coordinate system | **PASS** |
| `test_contract_m2_calibration_to_m3_rules` | M2 -> M3 | Metric scale & PDP area feed font height validator | **PASS** |
| `test_contract_m2_calibration_to_m4_api` | M2 -> M4 | Scale factor and anchor type serialize to API DTO | **PASS** |
| `test_contract_m2_calibration_to_m5_web` | M2 -> M5 | Millimeter scale factor maps to frontend visualizer | **PASS** |
| `test_contract_m3_rules_to_m4_api` | M3 -> M4 | Statutory evaluation records map to API response | **PASS** |
| `test_contract_m3_rules_to_m5_web` | M3 -> M5 | Rule statuses format for Frontend Verdict Matrix | **PASS** |
| `test_contract_m4_api_to_m5_web` | M4 -> M5 | Full API response parses against TS contract | **PASS** |
| `test_contract_m4_reporting_pdf` | M4 PDF Gen | Evidentiary PDF report generated with SHA-256 | **PASS** |
| `test_contract_uncalibrated_pipeline_flow` | M1-M5 Pipeline | End-to-end uncalibrated pipeline graceful degradation | **PASS** |

**Summary: 12 / 12 Passed (100%)**

---

## 3. Real-World Packaging Benchmark (`dairy_milk_bubbly/back_flat_01.jpg`)

- **Image Resolution:** 3072 × 4080 pixels (12.5 Megapixels)
- **File Size:** 4.2 MB
- **Pipeline Execution:** Live ONNX OCR + Quality Gate + Rules Engine + PDF Reporting
- **End-to-End Latency:** 1.49 seconds
- **Memory Growth:** Net +5.2 MB
- **OCR Perception:** 43 text lines extracted (MRP, Net Qty 50g, Mfg Date, Barcode, Veg Logo)
- **Calibration Result:** `is_calibrated: false` (no reference coin present in photo; graceful degradation)
- **Rules Verdict:** `NON_COMPLIANT` (due to missing Unit Sale Price declaration on legacy wrapper)
- **PDF Report:** 17.5 KB tamper-evident PDF generated in 4.12 ms with SHA-256 seal.
