# INTER-MEMBER HANDOFF SPECIFICATION: M1 ──► M6
### Optical Character Recognition (M1) to Ground Truth & Benchmark Lead (M6)
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M6_CHUNK2.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 6 (Ground Truth Dataset, Benchmark Protocol, DevOps & QA Lead)  
**Status:** FROZEN CONTRACT (Chunk 2 Complete)  
**Timestamp:** 2026-09-05T04:33:00+05:30  

---

## 1. Executive Contract Summary
Member 6 is responsible for procuring the **35-SKU authentic Indian retail packaging ground-truth dataset** and conducting formal benchmarks.

This document delivers:
1. The automated benchmark runner tool.
2. The expected ground-truth annotation format for the 35-SKU dataset.
3. Instructions on how to drop real images into `data/raw/` and execute automated Character Error Rate (CER) and Word Error Rate (WER) evaluations.

---

## 2. Benchmark Runner Location & Usage

Member 1 has implemented and validated the multi-threaded CPU benchmark harness at:
`benchmarks/ocr/chunk2/run_chunk2_benchmark.py`

### How to Run:
```powershell
python benchmarks/ocr/chunk2/run_chunk2_benchmark.py
```

### Generated Artifacts:
- `benchmarks/ocr/chunk2/results.json`: Complete machine-readable JSON trace including CPU specs, thread sweep latency, memory RSS trace, and per-specimen performance.
- `benchmarks/ocr/chunk2/README.md`: Rendered markdown report of empirical metrics.
- `benchmarks/ocr/chunk2/debug_visual.png`: Visual debug polygon overlay.

---

## 3. Real-World 35-SKU Dataset Onboarding Guide (For Chunk 3)

### Current Data Gap Status:
- **`data/raw/`:** Currently contains **0 real physical packaging images** (`DATA INSUFFICIENT`).
- Existing tests run exclusively on controlled synthetic fixtures labeled:
  `SYNTHETIC TEST — NOT REAL PACKAGING`.

### Instructions for Member 6:
1. **Image Storage:** Drop real photographic captures into:
   `data/raw/` (or `AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/images/`).
2. **Ground Truth Schema (`manifest.json`):**
   Provide ground-truth annotations in standard JSON format:
   ```json
   {
     "specimens": [
       {
         "file_name": "SKU_01_PARLE_G.jpg",
         "commodity_name": "Biscuits",
         "ground_truth_declarations": {
           "mrp": "Rs. 10.00",
           "net_quantity": "100 g",
           "mfg_date": "04/2026",
           "unit_sale_price": "Rs. 0.10 / g",
           "consumer_care": "parle@parle.biz"
         },
         "ground_truth_lines": [
           "NET WT: 100g",
           "MRP Rs. 10.00 INCL. OF ALL TAXES",
           "MFD: 04/26"
         ]
       }
     ]
   }
   ```
3. **Automated CER / WER Calculation:**
   When Member 6 drops the ground truth lines, Member 1 will evaluate Levenshtein distance:
   $$\text{CER} = \frac{S + D + I}{N_{\text{reference characters}}}$$
   Target: $\text{CER} < 6.0\%$ across the 35 authentic retail SKUs.
