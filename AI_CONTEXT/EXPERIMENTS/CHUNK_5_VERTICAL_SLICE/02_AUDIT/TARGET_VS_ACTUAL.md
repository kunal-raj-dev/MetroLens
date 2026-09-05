# Target Pipeline vs Actual Pipeline Matrix
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_5_VERTICAL_SLICE/02_AUDIT/TARGET_VS_ACTUAL.md`  
**Author:** Technical Lead & Systems Architect  
**Date:** 2026-09-05T15:38:00+05:30  
**Phase:** Chunk 5 — Vertical Slice 0  
**Status:** COMPLETE  

---

## 1. Pipeline Stage Comparison

| Stage | Target Specification | Actual Current State | Identified Gap | Owner | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Image Ingestion & Security** | Accept binary image (JPEG/PNG/WebP, $\le 15\text{ MB}$), validate magic bytes, compute SHA-256 digest, return unique inspection ID. | `apps/api` accepts JSON `InspectionRequest` and returns hardcoded mock. No multipart binary upload route. | Missing `POST /api/v1/inspect` multipart upload handler and byte-level validation. | Member 4 | **P0 (Blocker)** |
| **2. Quality Gate** | Pre-flight check computing edge sharpness (Laplacian variance $\ge 50.0$) and specular glare ratio ($\le 0.15$). Reject blurry/over-exposed frames with `REJECTED_QUALITY`. | Basic `check_image_quality` exists in `packages/vision` but is completely bypassed in API route. | Wire `check_image_quality` into the main inspection pipeline worker. | Member 2 | **P0 (Blocker)** |
| **3. Metric Calibration** | Detect reference coin or fiducial marker; compute mm/pixel scale factor with uncertainty; return `UNCALIBRATED` if absent. | Mathematical function `compute_scale_factor` exists in `packages/calibration`, but no image-level detector exists. | Implement automated fiducial/reference detection; safely fallback to `UNCALIBRATED` without inventing mm. | Member 2 | **P0 (Blocker)** |
| **4. OCR Perception** | Execute direct ONNX Runtime PP-OCRv3-ROUTED inference; generate 4-point quadrilateral polygons in original pixel coordinates. | Production `OCRService` implemented and hardened in `packages/ocr`, passing 81 tests. | None. OCR is fully ready; needs to be called by pipeline worker. | Member 1 | **Done** |
| **5. Semantic Extraction** | Parse mandatory Rule 6 declarations (MRP, Net Qty, Mfg Date, Consumer Care, Country of Origin) with contextual numeric normalization. | `DeclarationExtractor` in `packages/extraction` only parses MRP via simple regex. | Implement parsing for Net Qty, Mfg Date, Consumer Care, Origin; retain source token linkages and bounding boxes. | Member 3 | **P0 (Blocker)** |
| **6. Metric Measurement** | Calculate numeral font height in physical mm for Net Quantity declaration using calibration scale factor. | `calculate_font_height_mm` exists in `packages/measurement` but is not connected to extraction tokens. | Pass Net Quantity token pixel height to `calculate_font_height_mm`; leave `measured_mm=None` if uncalibrated. | Member 2 | **P0 (Blocker)** |
| **7. Legal Rule Engine** | Deterministically evaluate Rule 6 presence (MRP, Net Qty, Date, Care, Origin) and Rule 7 Table-I minimum numeral font height. | `NirikshakRulesEngine` in `packages/rules-engine` only evaluates Rule 6(1)(e) MRP presence. | Implement evaluation for Rule 6 declarations and Rule 7 Table-I font height (handling calibrated vs uncalibrated). | Member 3 | **P0 (Blocker)** |
| **8. Result & Evidence Assembly** | Compile master `InspectionResult` Pydantic model with cryptographic SHA-256 evidence nodes, stage latencies, and overall verdict. | Mocked static result generated with `COMPLIANT` verdict and empty evaluation lists. | Populate `InspectionResult` from actual stage outputs and telemetry timings; return HTTP 200 JSON. | Member 4 | **P0 (Blocker)** |

---

## 2. Remediation Strategy for Vertical Slice 0
The gaps identified above all stem from the lack of an orchestrated execution chain. In Chunk 5, we will:
1. Implement the missing parsing and rule evaluation logic in `packages/extraction` and `packages/rules-engine`.
2. Implement reference detection in `packages/calibration`.
3. Connect all stages in `apps/worker/main.py` (`InspectionPipelineWorker`).
4. Mount `POST /api/v1/inspect` in `apps/api/main.py`.
5. Verify end-to-end execution with comprehensive integration tests and benchmarks.
