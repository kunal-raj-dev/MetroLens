# CURRENT STATE: CHUNK 2 STATUS
**Document:** `CURRENT_STATE/CHUNK_2_STATUS.md`  
**Generated:** 2026-09-05T04:34:00+05:30  
**Phase:** Member 1 — Chunk 2 (OCR Engine Foundation)  
**Role:** Senior ML/OCR Engineer (Member 1 Lead)  
**Status:** COMPLETE  

---

## STATUS SUMMARY
- **STATUS:** COMPLETE
- **IMPLEMENTED:** Direct ONNX Runtime OCR engine (`packages/ocr/src/nirikshak_ocr/`), models in `models/weights/ocr/`, cryptographic manifest (`models/manifest.yaml`), visual debug tool (`tools/visualize_ocr_debug.py`), test suite (23 tests), benchmark harness (`benchmarks/ocr/chunk2/`).
- **VALIDATED:** 23 tests passing (1.91s), 100% offline execution verified, 4 CPU threads empirically confirmed optimal (107.29 ms median), memory stability bounded at ~305 MB RSS over 25 repeated calls, coordinate round-trip mapping confirmed within $\pm 0.05\text{px}$.
- **NOT VALIDATED:** Field-level Character Error Rate (CER) on authentic physical FMCG retail packaging.
- **REAL DATA:** PENDING (0 real packaging images in `data/raw/`; evaluations performed on controlled synthetic test fixtures).
- **DEPENDENCIES:** `onnxruntime==1.29.0`, `numpy==2.5.2`, `opencv-python==5.0.0.93`, `pyclipper==1.4.0`, `shapely==2.1.2`, `pydantic==2.13.4`. Zero dependency on `rapidocr-onnxruntime`.
- **RISKS:** Fragmented dot-matrix inkjet dates on metallic packaging crimps; awaiting authentic packaging dataset to calibrate domain-specific preprocessing in Chunk 3.
- **NEXT CHUNK:** Chunk 3 (Packaging Dataset Ingestion, Domain-Specific Preprocessing & Field-Level Robustness).

---

## 1. KNOWN
- `onnxruntime==1.29.0` with `CPUExecutionProvider` officially supports Python 3.14 on Windows 11.
- DBNet++ and SVTR-EN/HI run stably on CPU without third-party wrapper dependencies.
- 4 CPU intra-op threads provide the lowest inference latency on AMD Ryzen 8C/16T (107.29 ms median vs 168.22 ms on 1 thread; 8 threads suffer context switching penalty at 167.85 ms).
- Process RSS memory plateaus stably at ~305 MB across 25 repeated calls with zero unbounded memory growth.
- Coordinates unscale reversibly from resized DBNet input back to original image space.
- 4-point convex quadrilaterals preserve raw geometric stroke height without conflating it with statutory font height.
- The engine executes 100% offline with zero outbound network calls.

---

## 2. IMPLEMENTED
- `packages/ocr/src/nirikshak_ocr/config.py`: `OCRConfig` typed configuration.
- `packages/ocr/src/nirikshak_ocr/types.py`: `OCRToken`, `OCRResult`, `ScriptType`, and `to_observation()` adapter.
- `packages/ocr/src/nirikshak_ocr/errors.py`: Typed exception hierarchy (`OCRError`, `ModelLoadError`, `InvalidImageError`, etc.).
- `packages/ocr/src/nirikshak_ocr/preprocessing.py`: Multiples-of-32 resizing, ImageNet normalization, coordinate unscaling, and `ImagePreprocessHook`.
- `packages/ocr/src/nirikshak_ocr/detector.py`: Direct ONNX Runtime DBNet++ text detector.
- `packages/ocr/src/nirikshak_ocr/recognizer.py`: Direct ONNX Runtime SVTR recognizers with CTC greedy decoding.
- `packages/ocr/src/nirikshak_ocr/router.py`: Heuristic confidence-gated script router.
- `packages/ocr/src/nirikshak_ocr/utils.py`: Perspective cropping, clockwise quad ordering, deterministic reading order sorter.
- `packages/ocr/src/nirikshak_ocr/engine.py`: `OCREngine` public facade.
- `packages/ocr/src/nirikshak_ocr/__init__.py`: Public symbol exports and `NirikshakOCREngine` adapter.
- `packages/ocr/pyproject.toml`: Aligned dependencies (`onnxruntime`, `opencv-python`, `pyclipper`, `shapely`, `pydantic`).
- `models/manifest.yaml`: Cryptographic model manifest with SHA-256 hashes.
- `models/weights/ocr/`: Local ONNX weights for detection, Latin recognition, and Devanagari recognition.
- `tools/visualize_ocr_debug.py`: Visual debug polygon overlay tool.
- `tools/verify_ocr_run.py`: Runnable standalone verification script.
- `benchmarks/ocr/chunk2/run_chunk2_benchmark.py`: Benchmark harness for thread sweep, memory, and specimen sweep.

---

## 3. VALIDATED
- **Unit Test Suite:** 23 tests passing in 1.91s (`tests/unit/test_ocr_*.py` + `packages/ocr/tests/`).
- **Offline Execution:** Verified strictly offline under socket monkeypatch with zero network egress.
- **Runnable End-to-End Verification:** Verified on `SYNTH-01-ENG-FMCG.png` (97.84 ms, 6 tokens), `SYNTH-02-HIN-FMCG.png` (65.64 ms, 5 Devanagari tokens), `SYNTH-07-BLANK-FRAME.png` (22.66 ms, 0 tokens), and `None` invalid input (handled gracefully with warning, zero crash).
- **Visual Debug:** Verified `debug_visual.png` output.
- **Multi-thread Benchmark:** Sweep executed on 1, 2, 4, 8 threads; 4 threads optimal at 107.29 ms median.
- **Memory Trace:** 25 repeated calls logged; flat plateau at 305.04 MB - 305.06 MB (+0.02 MB delta).

---

## 4. NOT VALIDATED
- Performance and Character Error Rate (CER) on authentic physical retail packaging.
- Robustness on degraded dot-matrix inkjet expiration stamps without morphological preprocessing.
- Performance on curved metallic packaging surfaces.

---

## 5. UNKNOWN
- Empirical CER on authentic Indian commercial packaging across multiple regional lighting conditions.
- Degree of font stylization variation across regional FMCG brands.

---

## 6. BLOCKED
- **NONE.** Chunk 2 is 100% complete and unblocked. Chunk 3 execution awaits Member 6 dataset delivery.
