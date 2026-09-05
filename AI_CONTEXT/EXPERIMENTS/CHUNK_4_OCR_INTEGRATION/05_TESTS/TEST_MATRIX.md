# Chunk 4 — OCR Integration Test Matrix & Verification Suite
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/05_TESTS/TEST_MATRIX.md`  
**Author:** Member 1 (AI & Multilingual OCR Lead)  
**Date:** 2026-09-05T05:33:00+05:30  
**Phase:** Member 1 — Chunk 4  
**Status:** 100% TESTS PASSING (89/89)  

---

## 1. Test Suite Architecture Overview

The test suite validates the OCR subsystem at two distinct levels:
1. **Low-Level Unit & Hardening Suite (73 Tests):** Tests the internal building blocks of `nirikshak_ocr` (direct ONNX sessions, DBNet++ detection, SVTR recognition, angle classification, CTC decoding, preprocessing filters, and error handlers).
2. **High-Level Service Integration Suite (16 Tests):** Tests the public application boundary (`OCRService`), lifecycle, contract compliance, concurrency, thread safety, input normalization, and offline isolation.

**Total Test Count:** **89 tests passing (0 failures, 0 skipped, 1 benign starlette warning)**  
**Execution Runtime:** ~12.93 seconds on AMD64 CPU.

---

## 2. Integration Test Matrix (`tests/integration/test_ocr_service_integration.py`)

| Test ID | Test Method | Scope & Scenario | Acceptance Criterion | Result |
| :--- | :--- | :--- | :--- | :--- |
| **INT-01** | `test_service_singleton_lifecycle` | Verify `get_instance()` returns identical object across calls; `reset_instance()` tears down and allows clean re-init. | `id(s1) == id(s2)`, `id(s1) != id(s3)` | **PASS** |
| **INT-02** | `test_service_warmup` | Execute `service.warmup()`. Verify graph initialization, memory allocation, and dummy inference. | `warmup_ms > 0`, `status == "READY"`, `device == "CPU"` | **PASS** |
| **INT-03** | `test_service_extract_path_english` | Pass image file path to `extract()`. Test English statutory token extraction (`MRP Rs 250`). | Tokens detected > 0, confidence > 0.5, text matches ground truth | **PASS** |
| **INT-04** | `test_service_extract_bytes_input` | Pass raw binary image bytes (via `cv2.imencode`) to `extract()`. | Tokens detected > 0, identical result to path loading | **PASS** |
| **INT-05** | `test_service_input_immutability` | Pass in-memory `np.ndarray` to `extract()`. Verify caller array is defensively copied and unchanged. | `np.array_equal(original, caller_array)` bit-for-bit exact | **PASS** |
| **INT-06** | `test_service_bytes_vs_path_equivalence` | Compare extraction from path vs extraction from bytes of same image. | Token counts identical; string transcripts identical | **PASS** |
| **INT-07** | `test_service_extract_devanagari_unicode` | Extract Hindi packaging with Devanagari text (`अधिकतम खुदरा मूल्य`). | Unicode codepoints survive intact without mojibake | **PASS** |
| **INT-08** | `test_service_extract_rupee_symbol` | Extract packaging bearing Indian Rupee symbol (`₹ 245.00`). | Unicode `\u20b9` correctly detected and encoded in UTF-8 | **PASS** |
| **INT-09** | `test_service_extract_bilingual_script_routing` | Extract bilingual image containing dual English/Hindi declarations. | Both English and Devanagari tokens extracted in single pass | **PASS** |
| **INT-10** | `test_service_extract_blank_frame_specificity` | Pass pure blank/uniform image to `extract()`. Test false positive rejection. | `tokens == []`, `total_lines == 0`, `status == "SUCCESS"` | **PASS** |
| **INT-11** | `test_service_corrupt_bytes_error_handling` | Pass corrupt random bytes (`os.urandom(1024)`) to `extract()`. | Raises `OCRServiceError` with `INVALID_IMAGE` / `status_code=400` | **PASS** |
| **INT-12** | `test_service_invalid_input_type_error` | Pass invalid type (`dict`, `int`, etc.) to `extract()`. | Raises `OCRServiceError` with `INVALID_IMAGE` / `status_code=400` | **PASS** |
| **INT-13** | `test_service_canonical_observation_contract` | Call `extract_observations()`. Verify returned list of `OCRObservation` instances. | Conforms to Pydantic schema; JSON serializable | **PASS** |
| **INT-14** | `test_service_polygon_geometry_and_invariance` | Verify polygon coordinates on extracted tokens and observations. | 4-point clockwise quadrilateral in original image pixel space | **PASS** |
| **INT-15** | `test_service_concurrency_thread_safety` | Execute 8 requests concurrently across 4 worker threads via `ThreadPoolExecutor`. | All requests succeed, tokens returned, zero race conditions | **PASS** |
| **INT-16** | `test_service_socket_isolation_offline` | Monkeypatch `socket.socket` to forbid network connections. Run full OCR. | Zero sockets opened; 100% strictly local offline execution | **PASS** |

---

## 3. Repository Test Suite Summary

```text
================================== test session starts ===================================
platform win32 -- Python 3.14.3, pytest-8.3.4
rootdir: c:\Users\kunal\Desktop\MetroLens
collected 89 items

tests/integration/test_ocr_service_integration.py ................                [ 17%]
tests/unit/test_ocr_chunk2.py ........................................             [ 62%]
tests/unit/test_ocr_chunk3_hardening.py .............                             [ 77%]
tests/unit/test_ocr_chunk3_regression.py ....................                      [100%]

============================= 89 passed, 1 warning in 12.93s ==============================
```
