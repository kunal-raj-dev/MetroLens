# Member 1 Final Validation Matrix: Requirements vs. Validation Evidence

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Date**: September 2026  
**Status**: 100% SATISFIED & VALIDATED

---

## 1. Functional Requirements Matrix

| Req ID | Requirement Description | Implementation Location | Validation Method / Test | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Detect text regions in packaging images with arbitrary orientations. | `nirikshak_ocr.detector.DBDetector` | `test_detection_inference()` in `tests/unit/test_ocr_engine.py` | **VALIDATED** |
| **FR-02** | Recognize English alphanumeric text, packaging symbols, and units. | `nirikshak_ocr.recognizer.TextRecognizer` (Latin) | `test_extract_english_packaging_from_path()` in `test_ocr_service_integration.py` | **VALIDATED** |
| **FR-03** | Recognize Hindi Devanagari script including complex conjuncts and matras. | `nirikshak_ocr.recognizer.TextRecognizer` (Indic) | `test_extract_hindi_devanagari_and_currency_symbol()` in `test_ocr_service_integration.py` | **VALIDATED** |
| **FR-04** | Decode the official Indian Rupee currency symbol (`₹`, U+20B9). | `models/dict.txt` + Indic CTC Decoder | `test_extract_hindi_devanagari_and_currency_symbol()` in `test_ocr_service_integration.py` | **VALIDATED** |
| **FR-05** | Route mixed bilingual packaging crops dynamically without cross-script collisions. | `nirikshak_ocr.pipeline._route_script` | `test_extract_bilingual_mixed_script()` in `test_ocr_service_integration.py` | **VALIDATED** |
| **FR-06** | Gracefully handle blank or uninformative packaging frames with 0 tokens. | `nirikshak_ocr.engine.OCREngine` | `test_blank_frame_produces_zero_tokens_success_status()` in `test_ocr_service_integration.py` | **VALIDATED** |
| **FR-07** | Emit canonical shared observations conforming to monorepo contracts. | `nirikshak_ocr.service.OCRService.extract_observations` | `test_canonical_ocr_observations_contract()` in `test_ocr_service_integration.py` | **VALIDATED** |

---

## 2. Non-Functional Requirements Matrix

| Req ID | Non-Functional Requirement | Specification Target | Achieved Metric / Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **NFR-01** | Cold-start engine initialization latency. | < 1,000 ms on CPU | 481.14 ms (`results.json`) | **VALIDATED** |
| **NFR-02** | Warm session prime latency. | < 50 ms on CPU | 14.93 ms (`results.json`) | **VALIDATED** |
| **NFR-03** | Median warm frame inference latency. | < 250 ms on CPU | 115.79 ms (Hindi) / 139.18 ms (Eng) | **VALIDATED** |
| **NFR-04** | Multi-threaded inference throughput. | > 4.0 req/sec | 5.87 req/sec with 4 worker threads | **VALIDATED** |
| **NFR-05** | Complete air-gapped offline edge execution. | 0 socket network calls | `test_offline_execution_socket_guard()` | **VALIDATED** |
| **NFR-06** | Model weight cryptographic supply chain integrity. | 100% SHA-256 match | Bit-exact verification against `manifest.yaml` | **VALIDATED** |
| **NFR-07** | Thread safety across concurrent callers. | 0 race conditions | `test_concurrency_thread_safety()` (8 threads) | **VALIDATED** |
| **NFR-08** | Decompression bomb denial-of-service guard. | Reject >64MP in <10 ms | Rejects 67.1 MP array in 0.038 ms | **VALIDATED** |
| **NFR-09** | Memory RSS stability across repeated inferences. | Zero unbounded leak | 406 MB RSS after 250+ inferences | **VALIDATED** |

---

## 3. Boundary & Invariant Validation Matrix

| Invariant | Boundary Requirement | Verification Check | Status |
| :--- | :--- | :--- | :--- |
| **INV-01** | Zero Legal Metrology Act rule evaluation inside OCR. | Grep verification: 0 imports of rule engine | **VALIDATED (Strict Boundary)** |
| **INV-02** | Zero physical mm camera calibration inside OCR. | Grep verification: 0 camera matrices or mm math | **VALIDATED (Strict Boundary)** |
| **INV-03** | Zero web framework or HTTP transport coupling. | Grep verification: 0 fastapi/uvicorn imports in `packages/ocr` | **VALIDATED (Strict Boundary)** |
| **INV-04** | Zero unverified retail packaging claims (Path B Active). | Documentation audit: transparent disclaimers in all reports | **VALIDATED (Truth in Science)** |
