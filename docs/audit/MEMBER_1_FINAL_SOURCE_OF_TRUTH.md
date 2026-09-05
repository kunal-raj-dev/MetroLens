# Member 1 Final Source of Truth: Subsystem Specification & Forensic Audit

**Project**: MetroLens AI™ (SIH26034)  
**Lead**: Member 1 — AI & Multilingual OCR Lead  
**Auditor**: Independent Principal Engineer  
**Audit Phase**: Phase B Independent Forensic Audit & Freeze Gate  
**Date**: 2026-09-05  
**Final Status**: **`M1 FINAL — READY WITH KNOWN LIMITATIONS`**  

---

## 1. Mission
Member 1 owns the scene text optical character recognition subsystem (`nirikshak_ocr`) within MetroLens AI.
Its fundamental mission is to deliver deterministic, low-latency, multilingual optical text detection and recognition on Indian retail packaging executing 100% locally on standard CPU hardware without cloud dependencies.

Member 1 produces strictly **optical observations** (`OCRObservation`, `OCRResult`). It localizes text bounding quadrilaterals, detects language/script, and decodes Unicode character sequences.
- **Architectural Seam Invariant**: Member 1 does NOT parse statutory rules (Rule 6, Rule 9), does NOT compute physical millimeter measurements, and does NOT evaluate legal compliance.

---

## 2. Final Architecture (`PP-OCRv3-ROUTED`)
Member 1 uses a modular, two-stage detector-recognizer pipeline optimized for multilingual Indian packaging:

1. **Input Normalization & Safety**: `OCRService.convert_image_input()` normalizes binary bytes, file paths, or numpy arrays into standard BGR ndarrays, enforces decompression bomb limits (<= 64 MP), and defensive copies memory to ensure caller input immutability.
2. **Text Detection (DBNet++)**: `DBNetDetector` runs lightweight DBNet++ Mobile to generate text probability maps, dilates probability contours, unclips character regions via `pyclipper`, orders vertices clockwise `[tl, tr, br, bl]`, and unscales coordinates back to original image space.
3. **Perspective Unwarping**: `get_rotate_crop_image()` crops quadrilateral regions and perspective-transforms them into upright horizontal rectangular text patches.
4. **Dynamic Script Routing**: `ScriptRouter` routes crops between Latin and Devanagari models using a confidence-gated heuristic:
   - Primary pass: Evaluates Latin recognizer (SVTR-EN).
   - High confidence (>= 0.70) and length >= 2: Accepts Latin immediately (`SVTR-EN`).
   - Ambiguous or low confidence: Evaluates Devanagari recognizer (`SVTR-HI`).
   - If Hindi confidence > English confidence + 0.15: Routes to Devanagari (`SVTR-HI`).
   - Otherwise routes to the model with higher confidence.
5. **Text Recognition (SVTR-LCNet / CTC)**: `SVTRRecognizer` resizes crops to 48x320 and executes greedy Connectionist Temporal Classification (CTC) sequence decoding via `CTCLabelDecoder`.
6. **Deterministic Reading Order**: `sort_tokens_reading_order()` clusters tokens into horizontal lines using vertical bounding box overlap and sorts lines top-to-bottom, left-to-right.

---

## 3. Runtime
- **Inference Runtime**: Direct `onnxruntime==1.29.0`
- **Execution Provider**: `CPUExecutionProvider` (intra-op threads: 4, inter-op threads: 1)
- **Dependency Invariant**: Zero PyTorch, zero TensorFlow, zero PaddlePaddle runtime, zero RapidOCR wrapper in production inference path.
- **Memory Management**: Pre-allocates execution provider buffers during warmup; stabilizes at ~190 MB for long-running inference workloads.

---

## 4. Models
All models are FP32 ONNX graphs stored locally in the repository:

1. **Detection Model**: `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx`
   - Architecture: DBNet++ Mobile (Lightweight scene text detector)
   - Input: `x` (`[1, 3, H, W]`, float32 normalized by ImageNet mean/std)
   - Output: `sigmoid_0.tmp_0` (`[1, 1, H, W]`, probability map)
   - Size: 2,432,880 bytes | SHA-256: `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526`
2. **Latin Recognizer**: `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx`
   - Architecture: SVTR-LCNet alphanumeric CTC recognizer
   - Classes: 6,625 output classes (embedded character dictionary in ONNX metadata)
   - Size: 10,690,752 bytes | SHA-256: `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615`
3. **Devanagari Recognizer**: `models/weights/ocr/rec_hi/rec.onnx`
   - Architecture: SVTR Devanagari CTC recognizer
   - Classes: 169 output classes matching `dict.txt` (167 lines + blank + trailing space)
   - Size: 8,980,224 bytes | SHA-256: `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf`
4. **Devanagari Dictionary**: `models/weights/ocr/rec_hi/dict.txt`
   - Characters: 167 raw lines covering standard Devanagari glyphs, matras, numerals, and punctuation.
   - Size: 508 bytes | SHA-256: `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea`

---

## 5. Model Manifest
Model provenance is tracked in `models/manifest.yaml` (manifest version 1.0.0, license Apache-2.0). All disk file sizes and SHA-256 hashes match `models/manifest.yaml` with 100% cryptographic parity.

---

## 6. Package
- **Package Name**: `nirikshak-ocr` (version `0.1.0`)
- **Location**: `packages/ocr`
- **Installation**: `pip install -e packages/ocr --no-deps`
- **Public API**: `OCREngine`, `OCRService`, `OCRConfig`, `OCRToken`, `OCRResult`, `ScriptType`, `ScriptRouter`, `DBNetDetector`, `SVTRRecognizer`

---

## 7. Service
- **Adapter Class**: `nirikshak_ocr.OCRService`
- **Lifespan Management**: `OCRService.get_instance()` provides thread-safe singleton access for FastAPI application lifespan.
- **Warmup**: `OCRService.warmup()` primes CPU execution provider thread pools with a dummy frame (~15 ms).
- **Extraction Methods**:
  - `extract()`: Returns strongly-typed `OCRResult`.
  - `extract_observations()`: Returns `List[OCRObservation]` for Member 3 (Rule Engine).
  - `extract_dict()`: Returns JSON-serializable dictionary for Member 4 API and Member 5 Canvas.

---

## 8. Contract
- **Token Contract**: `OCRToken`
  - `token_id: str` (e.g. `tok_001`)
  - `text: str` (transcribed text, Unicode NFC normalized)
  - `confidence: float` (model CTC confidence score in `[0.0, 1.0]`)
  - `polygon: List[List[float]]` (4-point clockwise quad in unnormalized image pixels)
  - `bbox: List[float]` (`[xmin, ymin, xmax, ymax]`)
  - `script: ScriptType` (`latin`, `devanagari`, `unknown`)
  - `line_id: int` (top-to-bottom reading order line index)
  - `raw_pixel_height: float` (average side-edge height in pixels; NOT physical mm)
- **Shared Canonical Contract**: `nirikshak_shared.models.contracts.OCRObservation`

---

## 9. Preprocessing
- **Default Baseline**: `B0_BASELINE_RAW` (`preprocessing_mode="raw"`, `preprocess_target="crop"`).
- **Benchmark Evidence**: RAW achieved 111.0 ms mean latency vs 126.2 ms for ADAPTIVE on synthetic specimens with identical token yield (37 vs 37).
- **Provisional Pipeline**: `DomainPreprocessPipeline` supports CLAHE, bilateral filtering, unsharp masking, and polar-aware morphological dilation for low-contrast/dot-matrix text when explicitly configured.

---

## 10. Routing
- **Method**: Heuristic confidence gate (`ScriptRouter`).
- **Accuracy Metric**: Evaluated independently via `compute_routing_accuracy()` without mixing with CER or WER.
- **Behavior**: Directs Latin text to SVTR-EN and Devanagari text to SVTR-HI. Supports manual language override hints (`language_hint="en"` or `"hi"`).

---

## 11. Fallback
- **Mechanism**: Triggered when primary Latin evaluation yields confidence < 0.70 or length < 2.
- **Evaluation**: Hindi recognizer is evaluated; if Hindi confidence exceeds English by >= 0.15, Devanagari is selected.
- **Diagnostic Observability**: `fallback_used` boolean flag returned by router; fallback tokens recorded in `OCRResult.warnings`.

---

## 12. Error Model
Hierarchical typed exceptions inheriting from `nirikshak_ocr.errors.OCRError`:
- `InvalidImageError`: None, empty array, or image < 8x8 px.
- `UnsupportedImageError`: Unsupported format, corrupted bytes, or > 64 MP.
- `ModelLoadError`: Missing weights or corrupt ONNX graph.
- `InferenceError`: ONNX Runtime session failure.
- `OCRServiceError`: High-level unexpected service failure.
- **Empty Result Invariant**: A blank frame returns `status="SUCCESS"` with 0 tokens. It is NOT an error.

---

## 13. Lifecycle
- `OCRService.get_instance()` reuses existing ONNX sessions across requests without reloading model weights.
- `OCRService()` direct constructor creates an independent instance with fresh sessions for testing isolation.
- `OCRService.reset_instance()` resets singleton state.

---

## 14. Concurrency
- **Thread Safety**: Mutex lock (`OCRService._engine_lock`) synchronizes concurrent callers.
- **Verification**: Tested under 2, 4, 8 concurrent threads (40 tasks, 0 errors, 100% token consistency).
- **Throughput Characteristic**: CPU throughput is ~5.2 - 5.6 req/s. Linear multi-core scalability requires multi-process workers.

---

## 15. Offline
- 100% air-gapped edge execution.
- Verified via socket connection blocker monkeypatch; zero network calls attempted.

---

## 16. Performance
Measured on AMD Ryzen Processor (8 physical cores, 16 logical cores, 15.31 GB RAM):
- **Cold Engine Load**: ~358 ms | **Cold Service Load**: ~350 ms
- **Warmup**: ~15 ms
- **English Specimen Median**: 124.19 ms (Engine) / 184.78 ms (Service Obs)
- **Hindi Specimen Median**: 144.22 ms (Engine) / 152.37 ms (Service Obs)
- **Bilingual Specimen Median**: 167.07 ms (Engine) / 175.21 ms (Service Obs)
- **Blank Control Frame Median**: 47.45 ms (Engine) / 46.44 ms (Service Obs)
- **Note**: 200 ms and 2.5 s are engineering targets, not legal requirements.

---

## 17. Testing
- **Test Suite**: 108 automated tests passing across monorepo (100% pass rate).
- **Execution Command**: `python -m pytest` (runtime: ~33 seconds).
- **Coverage**: Hardening, regression, engine comprehensive, evaluation metrics, offline isolation, types, preprocessing, and independent Phase B audit tests.

---

## 18. Benchmarking
- **Final Benchmark Suite**: `benchmarks/ocr/final/`
- **Runner**: `python benchmarks/ocr/final/run_final_benchmark.py`
- **Artifacts**: Machine-generated `results.json`, `environment.json`, `config.json`, `README.md`.

---

## 19. Real Data
- **Current Physical Images**: **0 (ZERO)**.
- **Validation Status**: **REAL DATA VALIDATION = PENDING / NOT VERIFIED** (Path B active).
- **Rule**: All current metrics reflect synthetic regression specimens. No real-world accuracy claims are fabricated.

---

## 20. Known Limitations
1. Real packaging accuracy is pending field dataset collection by Member 6.
2. Script routing is a heuristic gate, not a deep neural classifier.
3. Concurrency is safely serialized; parallel CPU scalability requires multi-process deployment.
4. Confidence scores represent raw model CTC probabilities, not calibrated legal certitude.

---

## 21. Downstream Interfaces
- **Member 2 (Vision/Calibration)**: Consumes raw pixel `polygon`, `bbox`, and `raw_pixel_height`.
- **Member 3 (Rule Engine)**: Consumes canonical `List[OCRObservation]` via `extract_observations()`.
- **Member 4 (FastAPI API)**: Consumes `OCRService.get_instance()` in `/api/v1/inspect`.
- **Member 5 (Web Canvas)**: Consumes JSON `tokens` via `extract_dict()`.
- **Member 6 (Validation)**: Executes `run_final_benchmark.py` and evaluates real datasets.

---

## 22. Reproducibility
A fresh developer can reproduce Member 1 with zero environment hacking:
```bash
# 1. Verify models
python -c "from nirikshak_ocr.config import OCRConfig; print(OCRConfig().resolve_paths())"

# 2. Run test suite
python -m pytest

# 3. Run final benchmark
python benchmarks/ocr/final/run_final_benchmark.py
```

---

## 23. Final Release Status
**`M1 FINAL — READY WITH KNOWN LIMITATIONS`**
