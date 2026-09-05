# Monorepo Reality Audit: Actual vs Documented Matrix
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_5_VERTICAL_SLICE/02_AUDIT/ACTUAL_VS_DOCUMENTED.md`  
**Author:** Technical Lead & Systems Architect  
**Date:** 2026-09-05T15:38:00+05:30  
**Phase:** Chunk 5 — Vertical Slice 0  
**Status:** COMPLETE & HONEST  

---

## 1. Subsystem Reality Matrix

| Component | Documentation Claims | Code Actually Does | Tests | Status | Action Required for Chunk 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend API Gateway (`apps/api`)** | "Fully functional inspection gateway orchestrating synchronous vision, OCR, and rules." | Returns hardcoded dummy `InspectionResult(overall_verdict=COMPLIANT)` regardless of input. Pipeline disconnected. | 2 smoke tests | **SCAFFOLD / MOCKED** | Implement `POST /api/v1/inspect` consuming `multipart/form-data`, decoding bytes, and invoking the real inspection pipeline. |
| **Pipeline Worker (`apps/worker`)** | "Asynchronous or multi-stage pipeline worker executing end-to-end inspection." | Evaluates quality gate and passes empty `{}` to rules engine; completely bypasses OCR, extraction, and calibration. | 2 smoke tests | **SCAFFOLD** | Rewire `InspectionPipelineWorker.process_inspection` to sequentially execute: Quality $\rightarrow$ Calibration $\rightarrow$ OCR $\rightarrow$ Extraction $\rightarrow$ Measurement $\rightarrow$ Rules $\rightarrow$ Result. |
| **OCR Perception (`packages/ocr`)** | "Production-ready direct ONNX Runtime PP-OCRv3-ROUTED engine with B0 raw default." | Fully implemented, hardened, and packaged as `nirikshak-ocr`. `OCRService` singleton operational with 3.04 ms adapter overhead. | 81 tests passing | **IMPLEMENTED & READY** | Consume existing `OCRService.get_instance().extract()` without modification. |
| **Shared Contracts (`packages/shared`)** | "Canonical Pydantic contracts for inter-package DTOs and data schemas." | Defines `OCRObservation`, `DeclarationField`, `MeasurementResult`, `RuleEvaluation`, `EvidenceItem`, `InspectionResult`. | 5 tests passing | **IMPLEMENTED & READY** | Align all subsystem inputs/outputs strictly to these contracts. |
| **Vision / Quality (`packages/vision`)** | "Optical Image Quality Gate & Pre-Flight Validation with Laplacian variance & glare detection." | Implements basic `check_image_quality(image)` returning `QualityGateResult`. Fast (< 15 ms). | 1 smoke test | **SCAFFOLD** | Ensure compatibility with OpenCV BGR images; integrate into pipeline before OCR. |
| **Calibration (`packages/calibration`)** | "Physical Scale Calibration & Reference Target Recovery via coin/ArUco." | Mathematical formula `compute_scale_factor` only; no automated marker detection from image. | 2 smoke tests | **SCAFFOLD** | Implement automated reference detection; return explicit `UNCALIBRATED` status when no fiducial reference is found. |
| **Measurement (`packages/measurement`)** | "Physical metrological dimension calculations and Rule 7 numeral font height measurement." | `calculate_font_height_mm` converts pixels to mm given a scale factor; returns `UNCALIBRATED` if scale is None. | 3 smoke tests | **SCAFFOLD** | Consume scale factor from calibration; measure font height of Net Quantity tokens in pixels and mm. |
| **Extraction (`packages/extraction`)** | "Statutory declaration extraction from OCR tokens under PCR 2011 Rule 6." | Simple regex matching MRP only. Other mandatory Rule 6 fields (Net Qty, Date, Consumer Care, Origin) absent. | 1 smoke test | **SCAFFOLD** | Enhance `DeclarationExtractor` to parse MRP, Net Qty, Date, Consumer Care, and Country of Origin from `OCRObservation` tokens. |
| **Rules Engine (`packages/rules-engine`)** | "Deterministic statutory compliance evaluation for PCR 2011 and Jan Vishwas Act 2026." | Evaluates single rule `LMPC-R06-MRP-001`. Does not evaluate Net Qty, Date, or Rule 7 Table-I font height. | 2 smoke tests | **SCAFFOLD** | Implement deterministic evaluations for Rule 6 presence and Rule 7 Table-I font height (contingent on calibration). |
| **Evidence (`packages/evidence`)** | "Cryptographic SHA-256 DAG linking pixels to legal verdicts." | Basic SHA-256 calculation and `EvidenceItem` factory function. | 2 smoke tests | **SCAFFOLD** | Generate `EvidenceItem` nodes linking observations and measurements to parent image SHA-256. |
| **Packaging Dataset (`data/raw`)** | "Comprehensive 35-SKU ground truth retail packaging dataset." | **0 physical packaging images exist on disk**. Path B Blocker active. | 0 real data tests | **BLOCKED (Path B)** | Maintain Path B Gate. Use synthetic regression specimens to verify pipeline wiring. |
| **Frontend UI (`apps/web`)** | "Interactive inspection dashboard and verification canvas." | Static UI scaffolding; disconnected from API. | 0 tests | **SCAFFOLD** | Provide stable, contract-compliant JSON response from API; mark frontend integration pending. |

---

## 2. Summary of Findings
The repository's perception layer (OCR) and data models (Shared) are mature, but the middle-tier processing pipeline (Vision, Calibration, Extraction, Rules) and the top-tier application layer (API) exist strictly as decoupled skeletons. 

Chunk 5 directly solves this by replacing the mocked execution paths with real deterministic logic, producing a genuinely functioning Vertical Slice 0.
