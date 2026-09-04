# DATA STRATEGY & BENCHMARK VALIDATION PLAN
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)

This document establishes the empirical evaluation framework, ground-truth dataset collection protocol, and mathematical benchmarking formulas for validating MetroLens AI during InnoHack 3.0 / SIH 2026.

---

## 1. Data Strategy & Composition

To ensure absolute credibility during technical jury inspection, the system is evaluated on a **three-tier data architecture**:

```
                              DATA ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Public External Datasets (OpenFoodFacts India, Kaggle FMCG Packshots)    │
│    • Used for: Initial OCR syntax stress-testing and regex rule validation  │
│    • Size: ~5,000 package crop images                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Curated 100-Product Physical Benchmark Dataset (Indian Retail SKUs)      │
│    • Used for: Core metric calibration and font height benchmarking         │
│    • Ground Truth: Measured with digital vernier calipers (0.01mm precision)│
│    • Composition: 85 compliant retail SKUs + 15 intentional defect SKUs     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. 10-Product Deliberate Stress-Test Suite (Live Jury Stagecraft)           │
│    • Used for: Interactive live demonstration on jury table                 │
│    • High-contrast defect archetypes (missing USP, sub-1.5mm font, etc.)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 100-Product Ground-Truth Physical Dataset Specification

Within the first 36 hours of the hackathon, the team will assemble and physically measure **100 diverse Indian packaged commodities** across 6 retail categories:

| Category | Target SKU Count | Packaging Types Represented | Representative Brands / Products |
| :--- | :---: | :--- | :--- |
| **Snacks & Packaged Food** | 25 | Flexible BOPP pouches, cardboard cartons, laminates | Parle-G, Lay's, Kurkure, Haldiram Bhujia, Knorr Soup, Tata Tea |
| **Personal Care & Cosmetics** | 20 | Cylindrical plastic bottles, squeeze tubes, glass jars | Dettol Handwash, Nivea Lotion, Colgate Total, Head & Shoulders |
| **Beverages** | 15 | Metallized aluminum cans, PET bottles, Tetra Paks | Coca-Cola Can, Red Bull, Kinley Water, Real Juice Tetra Pak |
| **Home Care & Detergents** | 15 | Rigid HDPE containers, heavy LDPE bags | Surf Excel Liquid, Lizol Disinfectant, Harpic, Tide Bar |
| **Imported Commodities** | 10 | Confectionery, sauces, electronics (importer sticker check) | Lindt Chocolate, Tabasco Sauce, Korean Ramen, Bluetooth Earbuds |
| **Intentional Defect Test Cases** | 15 | Customized labels with deliberate statutory infractions | Printed defect labels representing 5 statutory non-compliance types |

### The 5 Intentional Defect Modes:
1. **Defect Type A (Sub-Millimeter Font Size):** Net quantity font printed at $1.1\text{mm}$ on a package with $\text{PDP} = 120\text{ cm}^2$ (Rule 9 Table 1 requires $\ge 2.5\text{mm}$).
2. **Defect Type B (Missing Unit Sale Price):** Packaged food with Net Qty $> 100\text{g}$ omitting USP (Rule 6(11) violation).
3. **Defect Type C (Mathematical USP Discrepancy):** Declared USP printed as ₹0.90/g when $\text{MRP} / \text{Net Qty} = ₹0.50/\text{g}$ (arithmetic fraud).
4. **Defect Type D (Illegal Metric Notation):** Net quantity declared as "50 Gms" or "100 ML" (prohibited under Rule 6(1)(c)).
5. **Defect Type E (Missing Statutory Qualifier):** MRP declared as "₹99/-" omitting mandatory "inclusive of all taxes" (Rule 6(1)(e)).

---

## 3. Physical Ground Truth Measurement Protocol

Every package in the benchmark dataset must undergo rigorous physical ground-truth recording:
1. **Instrument:** Digital Vernier Caliper (Mitutoyo / Baker style, $0.01\text{mm}$ resolution, calibrated).
2. **Recorded Parameters:**
   - Physical height and width of the Principal Display Panel ($H, W$ in millimeters).
   - Calculated physical PDP area: $A = \frac{H \times W}{100}\text{ cm}^2$.
   - Physical capital letter / numeral height of Net Quantity, MRP, and USP ($h_{\text{caliper}}$ in mm, measured across 3 distinct characters and averaged).
   - True Net Quantity, True MRP, True Declared USP, True Mfg Date.
3. **Storage:** Ground truth values stored in structured CSV/JSON: `data/ground_truth_benchmark_100.json`.

---

## 4. Benchmark Metrics & Mathematical Formulas

The system separates evaluation into four distinct analytical domains:

### A. Optical Character Recognition (OCR) Performance
1. **Character Error Rate (CER):**
   $$\text{CER} = \frac{S + D + I}{N_{\text{total\_chars}}}$$
   Where $S$ is character substitutions, $D$ is deletions, $I$ is insertions, and $N_{\text{total\_chars}}$ is ground-truth character count.
2. **Word Error Rate (WER):**
   $$\text{WER} = \frac{S_w + D_w + I_w}{N_{\text{total\_words}}}$$

### B. Entity Extraction & Normalization
1. **Extraction Precision, Recall, and F1-Score:**
   $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{F1} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
   Evaluated independently across: `mrp`, `net_quantity`, `mfg_date`, `consumer_care_email`, `consumer_care_phone`, `usp`.

### C. Physical Font-Height Measurement Accuracy
1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{M} \sum_{i=1}^{M} \left| h_{\text{measured}, i} - h_{\text{caliper}, i} \right|$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{M} \sum_{i=1}^{M} (h_{\text{measured}, i} - h_{\text{caliper}, i})^2}$$
3. **95th Percentile Maximum Error Bound ($\epsilon_{95}$):**
   $$\text{P}_{95} \text{ of } |h_{\text{measured}} - h_{\text{caliper}}|$$

### D. Statutory Compliance Classification
1. **Violation Detection Recall (Sensitivity):**
   $$\text{Recall}_{\text{violation}} = \frac{\text{True Defective Packages Flagged}}{\text{Total Ground Truth Defective Packages}}$$
   *Statutory Goal: Must be near 100% (Zero illegal packages overlooked).*
2. **False Positive Rate (FPR):**
   $$\text{FPR} = \frac{\text{Compliant Packages Erroneously Flagged as Non-Compliant}}{\text{Total Compliant Packages}}$$
   *Statutory Goal: Must be minimized to prevent regulatory harassment of legitimate brands.*

---

## 5. Performance Baselines vs. Engineering Targets vs. Empirical Actuals

> [!IMPORTANT]
> To preserve scientific integrity, theoretical performance goals are explicitly separated from empirical recorded results. Below is the official benchmark tracking matrix to be populated during testing.

| Metric | Historical Baseline (Uncalibrated Tesseract / Generic LLM) | MetroLens AI Engineering Target | Empirical Benchmark Result (To be measured Day 7–8) |
| :--- | :---: | :---: | :---: |
| **OCR Character Error Rate (CER)** | $28.4\%$ | $< 4.0\%$ | *[Recorded on Day 8]* |
| **OCR Word Error Rate (WER)** | $36.1\%$ | $< 6.5\%$ | *[Recorded on Day 8]* |
| **MRP & Net Qty Extraction F1** | $0.68$ | $> 0.95$ | *[Recorded on Day 8]* |
| **Consumer Care Email/Phone F1** | $0.72$ | $> 0.96$ | *[Recorded on Day 8]* |
| **Font Height Measurement MAE** | $0.85\text{ mm}$ (Uncalibrated) | $< 0.12\text{ mm}$ (Planar Homography) | *[Recorded on Day 8]* |
| **Measurement 95th Pct Error ($\epsilon_{95}$)** | $1.60\text{ mm}$ | $< 0.18\text{ mm}$ | *[Recorded on Day 8]* |
| **Violation Detection Recall** | $55.0\%$ | $> 96.0\%$ | *[Recorded on Day 8]* |
| **False Positive Rate (FPR)** | $38.0\%$ | $< 5.0\%$ | *[Recorded on Day 8]* |
| **USP Arithmetic Verification Accuracy** | $62.0\%$ (LLM division) | **100%** (Deterministic math) | *[Recorded on Day 8]* |
| **End-to-End Processing Latency** | $4.2\text{s}$ (Cloud API) | $< 2.0\text{s}$ (Local ONNX) | *[Recorded on Day 8]* |

---

## 6. Real-World Optical Stress Matrix

The benchmark dataset incorporates deliberate real-world optical degradation to evaluate robustness:

```
                            OPTICAL STRESS MATRIX
┌──────────────────────┬──────────────────────┬───────────────────────────────┐
│ Stress Condition     │ Test Package Count   │ System Mitigation Technique   │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ Specular Glare       │ 15 SKUs (Foil packs) │ HSV Saturation mask warning   │
│ Perspective Tilt     │ 20 SKUs (15° to 35°) │ Planar homography warping (H) │
│ Curved Cylinders     │ 15 SKUs (Cans/bottles│ Central generator invariance  │
│ Low Lighting (<50lx) │ 10 SKUs              │ CLAHE contrast normalization  │
│ Multilingual Text    │ 15 SKUs (Hindi/Eng)  │ PaddleOCR Devanagari model    │
│ Faded Dot-Matrix Ink │ 10 SKUs (Mfg dates)  │ Morphological character bridge│
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```
