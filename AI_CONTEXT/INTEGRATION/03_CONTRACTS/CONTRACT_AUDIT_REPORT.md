# Cross-Member Contract Audit Report

**Date:** September 2026  
**Test Suite:** `tests/contracts/test_cross_member_contracts.py` (12 Tests Passed, 100%)  

---

## 1. Overview of Pairwise Boundaries

| Boundary | Producer -> Consumer | Contract Domain | Status | Key Findings / Drift |
| :--- | :--- | :--- | :--- | :--- |
| **M1 -> M2** | OCR -> Calibration / Measurement | Box coordinates for scale | **PASSED** | Boxes normalized in pixel space `[x, y, w, h]`; compliant. |
| **M1 -> M3** | OCR -> Rules Engine | Text tokens & confidence | **PASSED** | Field normalization bridges OCR text to statutory models. |
| **M1 -> M4** | OCR -> API Gateway | Perception payload | **PASSED** | `OCRPerceptionResult` integrates seamlessly into `InspectionResponse`. |
| **M1 -> M5** | OCR -> Web Frontend | Bounding box rendering | **PASSED** | Frontend converts `[x, y, w, h]` to canvas overlay coordinates. |
| **M2 -> M3** | Calibration -> Rules Engine | Metric scale & PDP area | **PASSED (ADAPTED)** | Field name drift: `pdp_area_sqcm` vs `pdp_area_sq_cm`. |
| **M2 -> M4** | Calibration -> API Gateway | Scale factor & anchor info | **PASSED (ADAPTED)** | Field name drift: `scale_mm_per_px` vs `scale_factor`. |
| **M2 -> M5** | Calibration -> Web Frontend | Scale & PDP overlay | **PASSED (ADAPTED)** | M5 normalizer defensively inspects snake_case and camelCase. |
| **M3 -> M4** | Rules Engine -> API Gateway | Statutory verdicts & notices | **PASSED** | Serialized into `RuleEvaluationsGroup` and `LegalNoticePayload`. |
| **M3 -> M5** | Rules Engine -> Web Frontend | Display verdicts & sections | **PASSED** | M5 strictly renders backend status with zero client-side logic. |
| **M4 -> M5** | API Gateway -> Web Frontend | Full inspection envelope | **PASSED** | REST JSON matches `InspectionResult` TypeScript interface. |

---

## 2. Forensic Analysis of Contract Drift

### 2.1 Calibration DTO Drift (M2 vs M3 vs M4 vs M5)
- **M2 Internal (`packages/calibration`):**
  ```python
  scale_factor: float  # mm per pixel
  pdp_area_sq_cm: float
  anchor_type: str
  ```
- **M3 Rules Engine (`nirikshak_rules_engine.schemas.MetricScaleResult`):**
  ```python
  scale_factor_mm_per_px: Optional[float]
  pdp_area_sqcm: Optional[float]
  anchor_type_detected: Optional[str]
  ```
- **M4 API Gateway (`apps/api/schemas.CalibrationInfo`):**
  ```python
  scale_mm_per_px: Optional[float]
  pdp_area_cm2: Optional[float]
  coin_detected: bool
  anchor_type: Optional[str]
  ```
- **M5 Frontend Adapter (`apps/web/src/lib/api/normalizer.ts`):**
  ```typescript
  scaleMmPerPx: raw.calibration?.scale_mm_per_px ?? raw.calibration?.scaleFactorMmPerPx ?? null
  pdpAreaCm2: raw.calibration?.pdp_area_cm2 ?? raw.calibration?.pdpAreaCm2 ?? null
  ```
- **Resolution:** M4's API gateway serves as the normalizing layer between M2/M3 domain models and M5 client schema. The contract test suite asserts bidirectional mapping stability.

### 2.2 Rule Evaluation Record Drift (M3 vs Shared vs M4)
- **`nirikshak_shared.models.contracts.RuleEvaluation`:**
  - `verdict: RuleVerdict` (`RuleVerdict.PASS`, `RuleVerdict.FAIL`, `RuleVerdict.REVIEW`)
- **`nirikshak_rules_engine.schemas.RuleEvaluationRecord`:**
  - `status: str` (`"PASS"`, `"FAIL"`, `"REVIEW"`)
  - `is_compliant: bool`
- **`apps/api/schemas.RuleEvaluationsGroup`:**
  - Explicit named fields: `rule6_mandatory_status`, `rule6_11_usp_status`, etc.
- **Resolution:** M4 maps `RuleEvaluationRecord` to the statutory grouped response expected by M5.

### 2.3 Review API Endpoint Drift (M4 vs M5)
- **M5 Expectation:** `POST /api/v1/inspections/{id}/review` to submit inspector manual override decisions.
- **M4 Implementation:** The endpoint is currently unmapped in `apps/api/routes/`.
- **M5 Handling:** `liveApiAdapter.ts` catches this and throws `REVIEW_API_NOT_IMPLEMENTED`, gracefully informing the user while maintaining full test coverage.
