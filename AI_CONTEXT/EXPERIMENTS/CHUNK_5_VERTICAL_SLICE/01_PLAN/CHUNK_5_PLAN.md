# Chunk 5 Execution Plan: Vertical Slice 0 Core Inspection Pipeline
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_5_VERTICAL_SLICE/01_PLAN/CHUNK_5_PLAN.md`  
**Author:** Technical Lead & Senior Systems Architect  
**Date:** 2026-09-05T15:38:00+05:30  
**Phase:** Chunk 5 — Vertical Slice 0  
**Status:** APPROVED FOR EXECUTION  

---

## 1. Executive Objective
Construct **Vertical Slice 0**: the smallest authentic, end-to-end inspection flow operating on genuine code components:
$$\text{Image Upload} \longrightarrow \text{Input Validation} \longrightarrow \text{Quality Gate} \longrightarrow \text{Calibration} \longrightarrow \text{OCR Perception} \longrightarrow \text{Semantic Extraction} \longrightarrow \text{Rule Evaluation} \longrightarrow \text{Structured Result}$$

This phase eliminates mocked endpoints on the primary path, enforces real cross-subsystem contracts, connects the existing hardened `OCRService`, extracts a core statutory declaration subset (MRP, Net Qty, Date, Consumer Care, Country of Origin), and deterministically evaluates Legal Metrology Rules (Rule 6 and Rule 7 Table-I).

---

## 2. Architectural Boundaries & Scope Constraints

### 2.1 Scope Inclusions
1. Single uploaded image payload via `multipart/form-data` (`POST /api/v1/inspect`) and JSON payload (`POST /api/v1/inspections`).
2. Binary validation (magic bytes, max 15MB size, non-zero dimensions) and cryptographic SHA-256 computation.
3. Pre-flight image quality check (sharpness and glare rejection).
4. Scale calibration: fiducial reference detection resulting in either `CALIBRATED` or explicit `UNCALIBRATED` (no fabricated scales).
5. OCR execution using hardened `OCRService` (`PP-OCRv3-ROUTED` with direct ONNX Runtime on CPU).
6. Semantic extraction of core statutory fields from `OCRObservation` tokens with contextual numeric normalization.
7. Deterministic evaluation of Rule 6 mandatory declarations and Rule 7 Table-I numeral font height.
8. Structured `InspectionResult` containing observation coordinates, declarations, rule evaluations, and stage latencies.
9. Comprehensive integration test suite (`test_vertical_slice_0.py`) verifying valid images, defect images, quality rejection, uncalibrated handling, and offline execution.

### 2.2 Scope Exclusions (Strict Non-Goals)
- No Celery, Redis, or RabbitMQ background worker queues. Synchronous Web MVP execution only.
- No 3D pouch unwrapping, cylinder distortion rectification, or stereo vision. Planar/rectangular geometry only.
- No legal research rewrites. Strictly use verified PCR 2011 and Jan Vishwas Act 2026 rules.
- No full e-Maap live API integration (remains explicitly mocked/simulated).
- No frontend visual canvas redesign (provide stable API response contract for Member 5).
- No PDF dossier generation blocking the primary JSON flow.
- Zero Git commits or pushes.

---

## 3. Microstep Execution Roadmap

- **Microstep 1: Baseline Audit & Reality Alignment** (Capture baseline, author `ACTUAL_VS_DOCUMENTED.md` and `TARGET_VS_ACTUAL.md`).
- **Microstep 2: Subsystem Hardening for Vertical Slice**
  - Vision: Robust `check_image_quality`.
  - Calibration: Reference detection + `compute_scale_factor`. Safe `UNCALIBRATED` fallback.
  - Measurement: `calculate_font_height_mm` handling calibrated vs uncalibrated states.
  - Extraction: `DeclarationExtractor` for MRP, Net Qty, Date, Consumer Care, Country of Origin.
  - Rules Engine: `NirikshakRulesEngine` evaluating Rule 6 presence and Rule 7 Table-I font height.
- **Microstep 3: Pipeline Worker Implementation** (`apps/worker/main.py`)
  - Connect all 8 stages sequentially; record telemetry timings.
- **Microstep 4: API Endpoint Implementation** (`apps/api/main.py`)
  - Mount `POST /api/v1/inspect` and `POST /api/v1/inspections`; wire startup lifespan warmup.
- **Microstep 5: Verification & Benchmark Suite**
  - Author `tests/integration/test_vertical_slice_0.py`.
  - Run benchmark harness `benchmarks/vertical_slice_0/`.
- **Microstep 6: Documentation, Snapshots & Handoffs**
  - Author `FINAL_CHUNK_5_REPORT.md` (24 sections), `CHUNK_5_STATUS.md`, and member handoffs.
