# SKU-LEVEL ZERO-LEAKAGE PARTITION PROTOCOL
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_DATA/SKU_SPLIT_PROTOCOL.md`  
**Purpose:** Ensure unbiased statistical benchmarking without packaging identity leakage  

---

## 1. The Data Leakage Vulnerability
In retail packaging OCR, multiple photographs taken of the same commercial product (e.g. front panel, back panel, angled view, differing lighting) share:
- Identical typographical fonts.
- Identical statutory text strings (MRP, net weight, ingredients).
- Identical color palettes and foil reflectance.

If photos of the same SKU are randomly assigned across training/tuning and testing sets:
- The evaluation measures **memorization of SKU brand aesthetics**, not generalization to unseen packaging.
- Character Error Rate (CER) results become artificially deflated and scientifically invalid.

## 2. Mandatory Partition Rule: Disjoint by SKU
The dataset must be partitioned strictly by `sku_id`:
$$\text{SKUs}_{\text{development}} \cap \text{SKUs}_{\text{holdout}} = \emptyset$$

### Target Distribution (35 SKUs Total):
1. **Development / Tuning Set (70% — 25 SKUs):**
   - Used for exploratory baseline analysis, failure taxonomy building, parameter tuning (CLAHE clip limits, dilation kernel size), and threshold calibration.
2. **Held-Out Evaluation Set (30% — 10 SKUs):**
   - Sealed during parameter tuning.
   - Evaluated only once for the final unbiased benchmark.
   - Any post-hoc parameter modifications after viewing holdout scores require invalidating the run and logging a new experimental cycle.

## 3. Stratified Diversity Constraints
Both development and holdout partitions must contain representative diversity across:
- **Product Categories:** Snacks, personal care, beverages, household products, packaged staples.
- **Surface Types:** Rigid flat cartons, flexible plastic pouches, reflective metallic foils, curved bottles/cans.
- **Scripts:** Latin-only, Devanagari-only, bilingual/mixed.
- **Special Conditions:** Standard clean print, degraded dot-matrix inkjet codes, low-contrast small print.
