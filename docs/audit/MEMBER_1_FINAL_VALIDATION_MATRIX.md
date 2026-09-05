# MEMBER 1 — FINAL VALIDATION MATRIX

**Subsystem**: Member 1 — Multilingual OCR Engine & Service  
**Auditor**: Independent Principal Engineer  
**Date**: 2026-09-05  

| Test ID | Area | Expected | Actual | Evidence | Status | Severity if Failed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `VAL-01` | Smoke Check | OCREngine initializes and executes extraction | Initializes successfully, extracts tokens | `packages/ocr/tests/test_ocr_smoke.py` | PASS | CRITICAL |
| `VAL-02` | Detection Model Load | DBNet++ ONNX model loads via ONNX Runtime CPU | Session initialized with `CPUExecutionProvider` | `test_ocr_engine_comprehensive.py::test_missing_detector_model_raises_error` | PASS | CRITICAL |
| `VAL-03` | Latin Recognizer Load | SVTR-EN ONNX model loads with embedded 6625 classes | Session initialized, 6625 classes verified | `test_ocr_engine_comprehensive.py::test_extract_english_synthetic_specimen` | PASS | CRITICAL |
| `VAL-04` | Devanagari Recognizer Load | SVTR-HI ONNX model loads with 169 classes matching dict | Output dimension 169 matches decoder 169 classes | `test_ocr_phase_b_independent_audit.py::test_devanagari_dictionary_dimension_alignment` | PASS | CRITICAL |
| `VAL-05` | Model Hashes Integrity | Disk model SHA-256 matches manifest.yaml | All 4 assets match manifest 100% | `test_verification_pipeline.py::test_verify_dataset_manifest` | PASS | HIGH |
| `VAL-06` | Coordinate Remapping | Polygon coordinates accurately unscaled to original space | Remapping roundtrip error = 0.0000 px | `test_coordinates_and_geometry.py` | PASS | CRITICAL |
| `VAL-07` | Clockwise Ordering | 4 polygon vertices ordered clockwise `[tl, tr, br, bl]` | Vertex ordering invariant holds for all quads | `test_ocr_engine_comprehensive.py::test_order_points_clockwise` | PASS | HIGH |
| `VAL-08` | Bounding Box Enclosure | Derived bbox strictly encloses all polygon vertices | `xmin <= px <= xmax` and `ymin <= py <= ymax` | `test_ocr_phase_b_independent_audit.py::test_coordinate_invariance_and_bounding_envelope` | PASS | HIGH |
| `VAL-09` | Devanagari & ₹ Unicode | Hindi text and ₹ preserved across JSON roundtrip | Zero Mojibake; character strings match verbatim | `test_ocr_phase_b_independent_audit.py::test_unicode_nfc_and_currency_preservation` | PASS | CRITICAL |
| `VAL-10` | Heuristic Script Routing | Latin routed to SVTR-EN; Devanagari routed to SVTR-HI | English text routed to Latin, Hindi to Devanagari | `test_routing_and_fallback.py` | PASS | HIGH |
| `VAL-11` | Script Fallback | Ambiguous / low-confidence English triggers Devanagari | Fallback executes on noise and Devanagari crops | `test_routing_and_fallback.py` | PASS | HIGH |
| `VAL-12` | Routing Metric Independence | Routing accuracy computed independently of CER/WER | `compute_routing_accuracy` evaluates routing only | `test_ocr_chunk3_hardening.py::test_compute_routing_accuracy_independent_of_cer` | PASS | MEDIUM |
| `VAL-13` | RAW Preprocess Default | `OCRConfig.preprocessing_mode == "raw"` by default | Verified "raw" in config and service defaults | `test_ocr_chunk3_hardening.py::test_default_config_is_raw_baseline` | PASS | HIGH |
| `VAL-14` | Preprocessing Latency | RAW is faster than ADAPTIVE on standard specimens | RAW 111.0 ms vs ADAPTIVE 126.2 ms (+15.2 ms overhead) | `compare_preprocessing.py` | PASS | MEDIUM |
| `VAL-15` | Empty Frame Semantics | Blank image returns `status="SUCCESS"` with 0 tokens | Returns `OCRResult(tokens=[])`, status SUCCESS | `test_ocr_phase_b_independent_audit.py::test_empty_frame_vs_failure_semantics` | PASS | HIGH |
| `VAL-16` | Typed Error Hierarchy | Invalid and corrupt inputs raise typed exceptions | `InvalidImageError`, `UnsupportedImageError` raised | `test_error_semantics.py` | PASS | HIGH |
| `VAL-17` | Decompression Bomb Guard | Images exceeding 64 MP rejected immediately | Rejects >64 MP in < 0.1 ms with typed error | `test_ocr_service_integration.py::test_decompression_bomb_guard` | PASS | HIGH |
| `VAL-18` | Input Array Immutability | Caller numpy array is never mutated in-place | Before/after array equality verified | `test_ocr_service_integration.py::test_input_array_immutability` | PASS | HIGH |
| `VAL-19` | Offline Socket Isolation | Zero outbound network calls made during OCR | Socket connection monkeypatch verifies 0 calls | `test_ocr_offline.py::test_ocr_strictly_offline` | PASS | CRITICAL |
| `VAL-20` | Service Lifecycle | `get_instance()` provides thread-safe singleton session reuse | Singleton instance identical across callers | `test_ocr_phase_b_independent_audit.py::test_service_singleton_vs_fresh_instance` | PASS | HIGH |
| `VAL-21` | Concurrency Thread Safety | Multi-threaded callers execute safely without crashes | 2, 4, 8 threads execute with 0 errors and identical tokens | `test_ocr_service_integration.py::test_concurrency_thread_safety` | PASS | HIGH |
| `VAL-22` | Bounded Memory | Memory stabilizes after initial ONNX Runtime allocation | RSS stabilizes at ~190 MB; delta over 70 calls = +0.48 MB | `test_memory_and_concurrency.py` | PASS | MEDIUM |
| `VAL-23` | Determinism | Repeated inference on same specimen produces identical text | Token text, polygons, and scores match 100% | `test_ocr_chunk3_regression.py::test_determinism_under_repeated_runs` | PASS | HIGH |
| `VAL-24` | Reading Order Sorting | Tokens sorted top-to-bottom, left-to-right | Line grouping and reading order verified | `test_ocr_phase_b_independent_audit.py::test_reading_order_vertical_sorting` | PASS | MEDIUM |
| `VAL-25` | Seam Boundary Isolation | Zero legal rules or physical mm units inside Member 1 | Code grep and token inspection confirm 0 legal rules | `test_ocr_phase_b_independent_audit.py::test_no_semantic_or_legal_contamination_in_tokens` | PASS | CRITICAL |
| `VAL-26` | Downstream M2 Contract | Provides unnormalized polygons and raw pixel heights | `polygon`, `bbox`, `raw_pixel_height` present | `packages/shared/tests/test_contracts.py` | PASS | CRITICAL |
| `VAL-27` | Downstream M3 Contract | Provides canonical `OCRObservation` for Rule Engine | `OCRToken.to_observation()` conforms to shared DTO | `packages/shared/tests/test_contracts.py` | PASS | CRITICAL |
| `VAL-28` | Downstream M4 Contract | `OCRService` reusable by FastAPI application | FastAPI `/api/v1/inspect` returns 200 OK | `apps/api/tests/test_api_smoke.py` | PASS | CRITICAL |
| `VAL-29` | Downstream M5 Contract | `extract_dict()` provides tokens, bboxes, quads | JSON-ready dictionary output validated | `test_contracts_and_json.py` | PASS | HIGH |
| `VAL-30` | Real Data Honesty | 0 physical packaging images truthfully disclosed | Real-data validation status formally marked PENDING | `CURRENT_STATE/PHASE_B_BASELINE.md` | PASS | HIGH |
