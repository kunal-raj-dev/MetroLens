# Actual Vertical Slice 0 Component Traceability
**Document:** `docs/audit/ACTUAL_VERTICAL_SLICE_0.md`  
**Author:** Technical Lead & Systems Architect  
**Date:** 2026-09-05T15:38:00+05:30  
**Phase:** Chunk 5 — Vertical Slice 0  
**Status:** CANONICAL REPOSITORY REALITY AUDIT  

---

## 1. Actual End-to-End Component Flow

This document traces each stage of the real, executing Vertical Slice 0 pipeline to its physical implementation file, output contract, and automated test suite.

```text
+-----------------------------------------------------------------------------------+
| 1. HTTP INGESTION & SECURITY VALIDATION                                           |
| File: apps/api/main.py -> /api/v1/inspect                                         |
| Action: Validates payload size (<=15MB), magic bytes (JPEG/PNG/WebP), computes    |
|         SHA-256 digest, decodes bytes into OpenCV BGR ndarray.                    |
| Output: (InspectionRequest, np.ndarray, image_sha256)                             |
| Test: tests/integration/test_vertical_slice_0.py::test_vs0_upload_security_checks |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. OPTICAL QUALITY GATE                                                           |
| File: packages/vision/src/nirikshak_vision/__init__.py                            |
| Action: Evaluates Laplacian edge variance and high-luminance specular glare.      |
| Output: QualityGateResult(passed=bool, laplacian_variance=float, glare_ratio=float)|
| Test: packages/vision/tests/test_vision_smoke.py                                  |
|       tests/integration/test_vertical_slice_0.py::test_vs0_quality_gate_rejection |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. OPTICAL REFERENCE CALIBRATION                                                  |
| File: packages/calibration/src/nirikshak_calibration/__init__.py                  |
| Action: Detects circular reference coin or fiducial marker; computes mm/pixel     |
|         scale factor. Safely returns UNCALIBRATED if no reference detected.       |
| Output: CalibrationOutcome(status=CalibrationStatus, scale_factor_mm_per_pixel)   |
| Test: packages/calibration/tests/test_calibration_smoke.py                        |
|       tests/integration/test_vertical_slice_0.py::test_vs0_uncalibrated_handling  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. MULTILINGUAL OCR PERCEPTION                                                    |
| File: packages/ocr/src/nirikshak_ocr/service.py (OCRService)                      |
| Action: Direct ONNX Runtime PP-OCRv3-ROUTED inference on local CPU.               |
| Output: List[OCRObservation] (tokens with 4-point polygon coordinates & text)     |
| Test: tests/integration/test_ocr_service_integration.py                           |
|       tests/integration/test_vertical_slice_0.py::test_vs0_ocr_perception_stage  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 5. STATUTORY SEMANTIC EXTRACTION                                                  |
| File: packages/extraction/src/nirikshak_extraction/__init__.py                    |
| Action: Parses Rule 6 declarations (MRP, Net Qty, Mfg Date, Consumer Care, Origin)|
|         with contextual numeric normalization. Retains source token IDs & boxes.  |
| Output: Dict[str, DeclarationField]                                               |
| Test: packages/extraction/tests/test_extraction_smoke.py                          |
|       tests/integration/test_vertical_slice_0.py::test_vs0_declaration_extraction |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 6. METRIC MEASUREMENT (Table-I Font Height)                                       |
| File: packages/measurement/src/nirikshak_measurement/__init__.py                  |
| Action: Measures Net Quantity numeral font height in pixels. If calibrated,       |
|         converts to physical mm; if uncalibrated, leaves measured_mm=None.         |
| Output: Dict[str, MeasurementResult]                                              |
| Test: packages/measurement/tests/test_measurement_smoke.py                        |
|       tests/integration/test_vertical_slice_0.py::test_vs0_font_measurement_stage |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 7. DETERMINISTIC STATUTORY RULE EVALUATION                                        |
| File: packages/rules-engine/src/nirikshak_rules_engine/__init__.py                |
| Action: Evaluates Rule 6 mandatory presence (MRP, Net Qty, Date, Care, Origin)    |
|         and Rule 7 Table-I font height (PASS, FAIL, or REVIEW/UNCALIBRATED).      |
| Output: List[RuleEvaluation]                                                      |
| Test: packages/rules-engine/tests/test_rules_engine_smoke.py                       |
|       tests/integration/test_vertical_slice_0.py::test_vs0_legal_rule_evaluation  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 8. RESULT & EVIDENCE COMPILATION                                                  |
| File: apps/worker/main.py (InspectionPipelineWorker)                              |
| Action: Assembles canonical InspectionResult with EvidenceItem DAG, overall       |
|         verdict, and stage latency telemetry.                                     |
| Output: InspectionResult (Pydantic model serialized to HTTP 200 JSON response)    |
| Test: apps/worker/tests/test_worker_smoke.py                                      |
|       tests/integration/test_vertical_slice_0.py::test_vs0_end_to_end_pipeline    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Components Intentionally Out of Scope (Vertical Slice 0)

| Component | Status | Rationale |
| :--- | :--- | :--- |
| **Asynchronous Worker Queue (Celery / Redis)** | **EXCLUDED (MVP Scope)** | ADR-011 through ADR-017 mandate synchronous in-process execution. |
| **3D Cylindrical Unwarping / Mesh Unrolling** | **DEFERRED (Chunk 6+)** | Vertical Slice 0 targets planar/rectangular packaging labels first. |
| **Full Legal Metrology Rules Matrix (Rules 8, 9, 11, 26)** | **DEFERRED (Chunk 6+)** | Vertical Slice 0 targets core P0 rules: Rule 6 presence & Rule 7 Table-I font height. |
| **Interactive Frontend Verification Canvas (`apps/web`)** | **PENDING CONSUMPTION** | Member 5 frontend will consume the stable JSON response from Vertical Slice 0. |
| **Cryptographically Signed PDF Dossier Generation** | **DEFERRED (Chunk 7)** | PDF dossier generation consumes the completed JSON `InspectionResult`. |
| **Live e-Maap API Synchronization** | **SIMULATED / MOCK** | National LM portal integration is strictly simulated. |
| **Real-World Physical Packaging Validation** | **BLOCKED (Path B Gate)** | 0 real physical images on disk; synthetic specimens used for pipeline verification. |
