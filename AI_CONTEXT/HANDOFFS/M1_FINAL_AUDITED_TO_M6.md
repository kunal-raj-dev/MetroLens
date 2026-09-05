# M1 FINAL AUDITED HANDOFF TO MEMBER 6 (VALIDATION, DATASETS & BENCHMARK REPRODUCIBILITY)

**From**: Member 1 (AI & Multilingual OCR Lead)  
**To**: Member 6 (Validation Lead, Datasets & Quality Assurance)  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Current Benchmark Reality: SYNTHETIC FIXTURES ONLY
- **Physical Retail Images on Disk**: **0 (ZERO)**.
- **Current Test Fixtures**: 8 synthetic packaging specimens under `data/synthetic/regression/`:
  - `SYNTH-01-ENG-FMCG.png`: English FMCG nutrition and statutory declaration panel.
  - `SYNTH-02-HIN-FMCG.png`: Hindi Devanagari FMCG label with `₹` currency symbol.
  - `SYNTH-03-MIXED-BILINGUAL.png`: Bilingual Hindi-English retail packaging.
  - `SYNTH-04-MICRO-FONT.png`: Micro-font statutory declarations (<10px text).
  - `SYNTH-05-LIQUID-VOLUME.png`: Liquid commodity volume packaging.
  - `SYNTH-06-PROHIBITED-UNITS.png`: Non-standard units.
  - `SYNTH-07-BLANK-FRAME.png`: Negative control (pure blank white frame).
  - `SYNTH-08-LOW-CONTRAST-FADED.png`: Low-contrast faded text stress specimen.

## 2. Requirements for Real-Data Collection (Path B Handoff)
To validate Member 1 on physical retail packaging, Member 6 must collect:
1. **Packaging Categories**: FMCG, cosmetics, pharmaceuticals, electronics, food grains.
2. **Surface Variations**: Flat cardboard cartons, flexible pouches, cylindrical bottles/cans, metallic foil wrappers.
3. **Lighting Conditions**: Diffuse retail lighting, slight shadows, reflective glare.
4. **Script Stratification**: Latin (English), Devanagari (Hindi), and Bilingual packaging.
5. **Annotation Schema**: Ground truth JSON files with:
   - `image_id`: Unique SKU identifier.
   - `ground_truth_tokens`: Array of `{"text": str, "polygon": List[List[float]], "script": str, "is_numeric": bool}`.
   - **SKU-Disjoint Split**: Partition test/eval sets such that the same SKU never appears across evaluation splits.

## 3. Benchmark Execution Commands
To reproduce Member 1 performance and regression benchmarks:
```bash
# 1. Full automated unit & integration test suite (108 tests)
python -m pytest

# 2. Comprehensive 7-stage release benchmark
python benchmarks/ocr/final/run_final_benchmark.py

# 3. Preprocessing mode comparison (RAW vs ADAPTIVE)
python AI_CONTEXT/EXPERIMENTS/MEMBER_1_PHASE_B_AUDIT/06_PERFORMANCE_AUDIT/compare_preprocessing.py

# 4. Memory & Concurrency Stress Audit
python AI_CONTEXT/EXPERIMENTS/MEMBER_1_PHASE_B_AUDIT/06_PERFORMANCE_AUDIT/test_memory_and_concurrency.py
```

## 4. Expected Machine-Generated Outputs
- `benchmarks/ocr/final/results.json`: Complete JSON summary of cold load, specimen latencies, concurrency sweeps, and memory delta.
- `benchmarks/ocr/final/README.md`: Markdown summary table.
- **Reference Latencies (AMD Ryzen CPU)**:
  - Cold engine load: ~350 ms
  - English specimen median: ~124 ms
  - Hindi specimen median: ~144 ms
  - Control blank frame: ~47 ms
  - Concurrency throughput: ~5.2 - 5.6 req/s
