# Chunk 5 Vertical Slice 0 Test Matrix

## Overview
This document records the comprehensive automated test matrix for **Vertical Slice 0: Core Inspection Pipeline Integration** in MetroLens AI (SIH26034).

## Test Suites & Coverage Summary

| Suite Location | Purpose | Tests | Status | Execution Time |
|:---|:---|:---:|:---:|:---:|
| `packages/shared/tests/test_contracts.py` | Canonical seam contract validation (Pydantic DTOs) | 5 | **PASSED** | 0.45s |
| `packages/vision/tests/test_vision_smoke.py` | Image quality gate (Laplacian sharpness & glare) | 3 | **PASSED** | 0.20s |
| `packages/calibration/tests/test_calibration_smoke.py` | Scale calibration (fiducials, coins, uncalibrated) | 3 | **PASSED** | 0.22s |
| `packages/ocr/tests/test_ocr_smoke.py` | Direct OCREngine smoke tests | 3 | **PASSED** | 0.85s |
| `packages/extraction/tests/test_extraction_smoke.py` | Rule 6 mandatory declaration parser | 3 | **PASSED** | 0.25s |
| `packages/measurement/tests/test_measurement_smoke.py` | Metric font height calculation & uncertainty | 3 | **PASSED** | 0.18s |
| `packages/rules-engine/tests/test_rules_engine_smoke.py` | Deterministic legal rules engine (Rule 6 & Rule 7) | 3 | **PASSED** | 0.19s |
| `packages/evidence/tests/test_evidence_smoke.py` | SHA-256 evidence item generation & DAG nodes | 3 | **PASSED** | 0.21s |
| `packages/reporting/tests/test_reporting_smoke.py` | Reporting smoke tests | 2 | **PASSED** | 0.15s |
| `apps/api/tests/test_api_smoke.py` | FastAPI gateway endpoints & multipart inspect upload | 4 | **PASSED** | 1.32s |
| `apps/worker/tests/test_worker_smoke.py` | Synchronous worker pipeline execution & quality rejection | 2 | **PASSED** | 1.08s |
| `tests/unit/test_ocr_*` | OCR engine unit test suite (Chunk 1-4) | 34 | **PASSED** | 8.50s |
| `tests/integration/test_ocr_service_integration.py` | OCRService adapter integration suite (Chunk 4) | 15 | **PASSED** | 5.20s |
| `tests/integration/test_vertical_slice_0.py` | **Vertical Slice 0 End-to-End Integration Suite** | 9 | **PASSED** | 2.61s |
| **TOTAL** | **Monorepo-Wide Automated Test Suite** | **98** | **100% PASS** | **~21s** |

## Vertical Slice 0 Specific Test Cases (`tests/integration/test_vertical_slice_0.py`)

| Test Identifier | Test Case Name | Objective & Target Invariant | Assertion Criteria | Result |
|:---|:---|:---|:---|:---:|
| **VS0-T01** | `test_vs0_valid_packaging_end_to_end` | Verify end-to-end processing of valid packaging image across all 8 pipeline stages via `POST /api/v1/inspect`. | HTTP 200, status=SUCCESS, quality_gate_passed=True, image_sha256 matching raw byte digest, rule evaluations present. | **PASSED** |
| **VS0-T02** | `test_vs0_upload_security_checks` | Enforce API perimeter security: rejection of corrupt byte headers and 0-byte payloads. | HTTP 400 with descriptive error detail; no uncaught exceptions or server crashes. | **PASSED** |
| **VS0-T03** | `test_vs0_quality_gate_rejection` | Validate early rejection at Stage 2 for low-contrast/blurry frames below threshold. | status=REJECTED_QUALITY, quality_gate_passed=False, overall_verdict=INCONCLUSIVE, error code `QUALITY_REJECTED`. | **PASSED** |
| **VS0-T04** | `test_vs0_uncalibrated_handling` | Guarantee truthful metrology: packaging frames lacking reference markers report UNCALIBRATED without fabricating mm. | calibration_status=UNCALIBRATED, measured_mm=None, Rule 7 verdict=REVIEW with uncertainty_flag=True. | **PASSED** |
| **VS0-T05** | `test_vs0_defect_detection_missing_mrp` | Detect statutory non-compliance: packaging frame missing mandatory MRP declaration. | declarations["mrp"].is_present=False, Rule 6 MRP evaluation verdict=FAIL, overall_verdict=NON_COMPLIANT. | **PASSED** |
| **VS0-T06** | `test_vs0_calibrated_measurement` | Validate full metrology chain when optical reference (INR coin) is detected in frame. | calibration_status=CALIBRATED, scale_factor_mm_per_pixel > 0, measured_mm > 0, Rule 7 evaluated PASS/FAIL. | **PASSED** |
| **VS0-T07** | `test_vs0_evidence_chain_linkage` | Audit cryptographic evidence DAG nodes linking source tokens, bounding boxes, and image SHA-256. | evidence_chain length >= 1, image_sha256 matches input digest, bounding boxes conform to pixel coordinate bounds. | **PASSED** |
| **VS0-T08** | `test_vs0_offline_execution` | Verify 100% offline edge execution under strict socket monkeypatch isolation. | Socket connection attempts raise fatal error; pipeline completes with 0 outbound network calls. | **PASSED** |
| **VS0-T09** | `test_vs0_stage_timings` | Confirm granular telemetry capture across all 8 pipeline phases. | Telemetry dictionary contains all 9 keys (`ingestion_ms`, `quality_gate_ms`, `calibration_ms`, `ocr_perception_ms`, `semantic_extraction_ms`, `measurement_ms`, `rules_engine_ms`, `evidence_assembly_ms`, `total_ms`) with non-negative latency. | **PASSED** |
