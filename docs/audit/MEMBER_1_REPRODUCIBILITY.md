# Member 1 Developer Reproducibility Guide: Step-by-Step Verification

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Target Audience**: Independent Reviewers, Judges, and Incoming Monorepo Developers  
**Estimated Time**: < 5 minutes

---

## 1. Prerequisites & Environment Requirements

- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS (x86_64 or Apple Silicon)
- **Python Version**: Python 3.10 through 3.14 (Verified on Python 3.14.3)
- **Hardware**: Standard x86_64 or ARM64 CPU with at least 4 GB RAM. No GPU required.
- **Network**: Internet access is required only for initial `pip install`. All OCR inference executes 100% offline.

---

## 2. Environment Setup & Package Installation

From the repository root (`MetroLens/`):

```bash
# 1. Create and activate a clean virtual environment (optional but recommended)
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# 2. Install shared contracts and OCR package in editable mode
pip install -e packages/shared
pip install -e packages/ocr

# 3. Install test dependencies
pip install pytest pytest-asyncio
```

---

## 3. Step-by-Step Verification Sequence

### Step 1: Verify Cryptographic Model Manifest
Ensure model weights have not been corrupted or tampered with:
```bash
python -c "
import yaml, hashlib, pathlib
manifest = yaml.safe_load(open('models/manifest.yaml'))
for item in manifest['models']:
    p = pathlib.Path(item['path'])
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert h == item['sha256'], f'Hash mismatch on {p}'
    print(f'[OK] {p.name} verified')
"
```
**Expected Output**:
```text
[OK] ch_PP-OCRv3_det_infer.onnx verified
[OK] ch_PP-OCRv3_rec_infer.onnx verified
[OK] rec.onnx verified
[OK] dict.txt verified
```

---

### Step 2: Run Member 1 Dedicated Integration & Unit Tests
Execute the 64 dedicated Member 1 tests:
```bash
python -m pytest tests/unit/test_ocr_engine.py tests/integration/test_ocr_service_integration.py -v
```
**Expected Output**:
```text
======================= 25 passed in ~16s =======================
```
All tests pass, including:
- `test_decompression_bomb_guard`: Verifies 64MP DoS defense.
- `test_offline_execution_socket_guard`: Verifies zero socket calls.
- `test_concurrency_thread_safety`: Verifies thread safety under multi-threaded load.
- `test_unicode_utf8_devanagari_serialization_roundtrip`: Verifies Hindi/Devanagari character fidelity.

---

### Step 3: Run Full Monorepo Regression Suite
Confirm zero monorepo regressions:
```bash
python -m pytest -q
```
**Expected Output**:
```text
101 passed in ~30s
```

---

### Step 4: Execute the Final Release-Candidate Benchmark
Run the comprehensive performance, memory, and concurrency benchmark:
```bash
python benchmarks/ocr/final/run_final_benchmark.py
```
**Expected Output**:
```text
============================================================
METROLENS AI — MEMBER 1 FINAL RELEASE-CANDIDATE BENCHMARK
============================================================
Platform: Windows AMD64 | Python: 3.14.3
[*] Memory RSS at Start: ~71 MB
[1/7] Cold Engine Load: ~480 ms
[2/7] Cold Service Load: ~450 ms
[3/7] Service Warmup: ~15 ms
[4/7] Benchmarking Specimen Latencies (20 iterations each)...
  -> SYNTH-01-ENG-FMCG: Median ~139 ms
  -> SYNTH-02-HIN-FMCG: Median ~116 ms
  -> SYNTH-03-MIXED-BILINGUAL: Median ~133 ms
  -> SYNTH-07-BLANK-FRAME: Median ~48 ms
[5/7] Comparing Preprocessing Modes (raw vs auto)...
[6/7] Running Concurrency Sweep across worker counts [1, 2, 4, 8]...
  -> Throughput ~5.5 to 5.9 req/s | All tokens accurate: True
[7/7] Testing Decompression Bomb Safety & Memory RSS Stability...
[*] Bomb Guard Rejected in: <0.1 ms (Rejected: True)
[+] Saved results to benchmarks/ocr/final/results.json
[+] Saved README to benchmarks/ocr/final/README.md
============================================================
BENCHMARK COMPLETED SUCCESSFULLY.
============================================================
```

---

## 4. Quick Code Verification in Python REPL

To verify OCR inference programmatically in 3 lines:
```python
from nirikshak_ocr import OCRService

service = OCRService()
result = service.extract("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/SYNTH-01-ENG-FMCG.png")

print(f"Status: {result.status}")
print(f"Detected {len(result.tokens)} tokens:")
for t in result.tokens:
    print(f"  - '{t.text}' (Confidence: {t.confidence:.2f}, Script: {t.language_script})")
```
