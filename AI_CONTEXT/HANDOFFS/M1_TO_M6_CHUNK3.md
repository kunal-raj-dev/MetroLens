# MEMBER 1 TO MEMBER 6 HANDOFF: CHUNK 3
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M6_CHUNK3.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 6 (Dataset, Benchmarking & QA Lead)  
**Date:** 2026-09-05T05:04:00+05:30  

---

## 1. Dataset Ingestion Readiness
Member 1 has delivered the infrastructure required for Member 6 to deliver the authentic retail packaging dataset:
- **Image Directory:** `data/raw/real/`
- **Annotation Directory:** `data/annotations/ocr/`
- **Dataset Registry Manifest:** `data/manifests/real_packaging_manifest.json`
- **Ground Truth Benchmark Spec:** `data/manifests/ground_truth_benchmark.json`
- **Manifest Validator Script:** `tools/validate_dataset_manifest.py`

## 2. Dataset Requirements for Member 6
1. **Target:** 35 diverse FMCG retail packaging SKUs.
2. **Category Balance:** Snacks, beverages, personal care, household, staples.
3. **Packaging Types:** Rigid cartons, flexible pouches, foil crimps, bottles, cans.
4. **Script Balance:** English, Hindi/Devanagari, bilingual mixed.
5. **Zero Data Leakage:** Partition strictly by `sku_id` (70% development, 30% held-out test). Photos of the same SKU must never cross split boundaries.

## 3. Benchmark Reproduction Commands
Member 6 can execute and verify the benchmark harness using:
```powershell
# 1. Run full test suite (73 tests passing)
python -m pytest -v


# 2. Run dataset manifest validation
python tools/validate_dataset_manifest.py --manifest data/manifests/real_packaging_manifest.json

# 3. Run full Chunk 3 benchmark harness
python benchmarks/ocr/chunk3/run_chunk3_benchmark.py

# 4. Generate visual debug overlay
python benchmarks/ocr/chunk3/visualize_errors.py --image AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/SYNTH-01-ENG-FMCG.png --output benchmarks/ocr/chunk3/visual_debug_overlay.png --mode adaptive
```
