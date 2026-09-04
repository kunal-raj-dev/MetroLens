# DATA STRATEGY & BENCHMARK VALIDATION PLAN (V0.3)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Document Status:** Empirical Scientific Evaluation Protocol | **Version:** 0.2 (Post-Audit Edition)  
**Date:** 4 September 2026 | **Governing Principle:** Zero Invented Metrics. Empirical Results Must Be Measured on Real Hardware.

---

## 1. Phased Data Strategy & Composition

To ensure absolute credibility during technical jury inspection while respecting the team's dual-project time constraint, dataset collection is organized into **three phased milestones**:

```
                              PHASED DATA ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Smoke-Test Calibration Suite (15–20 Physical SKUs) — By T+24h      │
│ • Purpose: Immediate validation of PaddleOCR CPU latency & scale recovery   │
│ • Composition: 15 compliant retail packs + 5 synthetic defect mockups       │
│ • Focus Categories: Biscuits, handwash, soap cartons, beverage cans         │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: Core Empirical Benchmark Dataset (35–40 Physical SKUs) — By Day 5  │
│ • Purpose: Formal measurement of CER, WER, font MAE, and Rule recall        │
│ • Ground Truth: Flatbed optical scan (1200 DPI) + dual-rater caliper check  │
│ • Composition: 25 compliant Indian retail packs + 12 synthetic defect SKUs  │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: Extended Evaluation Suite (Up to 60–75 SKUs) — Day 7 (Buffer Only) │
│ • Purpose: Robustness testing across secondary retail categories            │
│ • Execution: Undertaken ONLY if core software pipeline is stable and frozen │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Benchmark Composition by Retail Category (Phase 2 Target: 35–40 SKUs)

| Category | Target SKU Count | Packaging Types Represented | Representative Products |
| :--- | :---: | :--- | :--- |
| **Snacks & Packaged Food** | 10 | Flexible BOPP pouches, cardboard cartons | Parle-G, Lay's, Kurkure, Haldiram Bhujia, Tata Tea |
| **Personal Care & Cosmetics** | 8 | Cylindrical plastic bottles, cartons, squeeze tubes | Dettol Sanitizer, Nivea Lotion, Colgate Total, Dove Soap |
| **Beverages** | 6 | Aluminum cans, PET bottles, Tetra Paks | Coca-Cola Can, Red Bull, Real Juice Tetra Pak |
| **Home Care & Detergents** | 5 | Rigid HDPE containers, cartons | Surf Excel Bar, Harpic, Lizol Disinfectant |
| **Imported Commodities** | 3 | Confectionery, electronics (importer sticker check) | Lindt Chocolate, Korean Ramen |
| **Synthetic Defect Test Cases** | 8 | Custom printed mock sleeves with deliberate infractions | Controlled synthetic test labels representing 5 defect types |

### The 5 Synthetic Defect Modes (Controlled Testing Protocol):
> [!IMPORTANT]
> To prevent ethical and legal misrepresentation, all defect test cases MUST use custom printed mock sleeves or neutral package mockups clearly marked:  
> **"Synthetic Test Specimen — Not an Actual Manufacturer Violation."** Real commercial brand packaging must never be altered or displayed publicly as an accusation.

1. **Defect Mode A (Sub-Millimeter Font Deficit):** Net quantity numeral printed at $1.15\text{mm}$ on a package with $\text{PDP} = 75\text{ cm}^2$ (Rule 7 Table-I/II mandates minimum $1.50\text{mm}$).
2. **Defect Mode B (Missing Unit Sale Price):** Packaged commodity with Net Qty $> 100\text{g}$ omitting USP declaration (Rule 6(11) violation).
3. **Defect Mode C (USP Arithmetic Discrepancy):** Declared USP printed as ₹0.85/g when $\text{MRP} / \text{Net Qty} = ₹0.50/\text{g}$ (mathematical contradiction).
4. **Defect Mode D (Prohibited Unit Notation):** Net quantity declared as "50 Gms" or "100 ML" (violates Rule 6(1)(c) metric standard).
5. **Defect Mode E (Missing Mandatory Tax Qualifier):** MRP declared as "₹99/-" omitting statutory "inclusive of all taxes" qualifier (Rule 6(1)(e)).

---

## 3. Ground-Truth Measurement Protocol

Handheld digital calipers applied directly to tiny printed ink characters introduce human parallax, blade-angle tipping, and ink-bleed deformation of $\pm 0.10\text{–}0.15\text{mm}$. To provide an indisputable scientific standard for technical juries, ground truth is established via a **dual-instrument protocol**:

```
                       GROUND-TRUTH MEASUREMENT PROTOCOL
                       
  [ Physical Packaging Specimen ]
                 │
                 ├───────────────────────────────┐
                 ▼                               ▼
     [ 1200 DPI Optical Scan ]       [ Digital Vernier Caliper ]
   (Epson / Canon Flatbed Scanner)  (Mitutoyo 0.01mm Precision)
                 │                               │
                 ▼                               ▼
    [ Optical Pixel Measurement ]    [ Outer Package Dimensions ]
   (1 pixel = 0.02116 mm scale)     (Height x Width -> PDP Area)
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
         [ Dual-Rater Optical Measurement & Verification ]
         (Two independent raters measure 3 character heights)
                                 │
                                 ▼
         [ Ground Truth Benchmark Record: `benchmark.json` ]
```

### Measurement Procedure:
1. **Outer Package Dimensions (PDP Area):** Measured using a calibrated digital vernier caliper ($0.01\text{mm}$ resolution) across three independent trials. Recorded as $H, W$ in millimeters; PDP Area $A = \frac{H \times W}{100}\text{ cm}^2$.
2. **Numeral & Character Heights (Rule 7):**
   - Package panel scanned on a flatbed optical scanner at **1200 DPI resolution** ($1\text{ pixel} \equiv 0.02116\text{mm}$).
   - Two independent team members (Rater 1 and Rater 2) measure the vertical pixel height of the Net Quantity numeral and MRP digits using an optical reticle tool.
   - Ground truth height $h_{\text{true}} = \text{pixels} \times 0.02116\text{mm}$.
   - Inter-rater variance must be $< 0.04\text{mm}$; recorded values are averaged.
3. **Data Logging Schema (`data/ground_truth_benchmark.json`):**
   ```json
   {
     "sku_id": "SKU-014-BISCUIT",
     "category": "Snacks",
     "brand_type": "Synthetic Mock",
     "true_pdp_area_sqcm": [DYNAMIC MEASURED VALUE],
     "true_numeral_height_mm": 1.15,
     "true_mrp": 20.0,
     "true_net_quantity": 50.0,
     "true_net_quantity_unit": "g",
     "true_usp": null,
     "expected_statutory_font_mm": 1.50,
     "expected_verdict": "POTENTIAL_NON_COMPLIANCE",
     "ground_truth_method": "1200_DPI_FLATBED_OPTICAL_SCAN"
   }
   ```

---

## 4. Benchmark Metrics & Mathematical Formulations

### A. Optical Character Recognition (OCR) Performance
1. **Character Error Rate (CER):**
   $$\text{CER} = \frac{S + D + I}{N_{\text{total\_chars}}}$$
   Where $S$ is substitutions, $D$ is deletions, $I$ is insertions, and $N_{\text{total\_chars}}$ is total ground-truth characters.
2. **Word Error Rate (WER):**
   $$\text{WER} = \frac{S_w + D_w + I_w}{N_{\text{total\_words}}}$$

### B. Entity Normalization Accuracy
1. **Field Extraction F1-Score:**
   $$\text{F1} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
   Evaluated independently across: `mrp`, `net_quantity`, `mfg_date`, `consumer_care_email`, `consumer_care_phone`, `declared_usp`.

### C. Physical Font-Height Measurement Accuracy
1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{M} \sum_{i=1}^{M} \left| h_{\text{measured}, i} - h_{\text{true}, i} \right|$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{M} \sum_{i=1}^{M} (h_{\text{measured}, i} - h_{\text{true}, i})^2}$$
3. **95th Percentile Maximum Error ($\epsilon_{95}$):**
   $$\text{P}_{95} \text{ of } |h_{\text{measured}} - h_{\text{true}}|$$

### D. Regulatory Compliance Classification
1. **Violation Detection Sensitivity (Recall):**
   $$\text{Recall}_{\text{violation}} = \frac{\text{True Defective Packages Flagged}}{\text{Total Ground-Truth Defective Packages}}$$
2. **False Positive Rate (FPR):**
   $$\text{FPR} = \frac{\text{Compliant Packages Erroneously Flagged as Non-Compliant}}{\text{Total Ground-Truth Compliant Packages}}$$

---

## 5. Formal Benchmark Matrix: Baseline vs. Target vs. Empirical Actuals

> [!NOTE]
> To preserve absolute scientific integrity, theoretical engineering targets are explicitly separated from empirical recorded results. All "Actual" columns remain unpopulated until the formal Day 7–8 benchmark execution on host hardware.

| Metric | Scientific Definition | Literature Baseline (Generic Tesseract / Zero-Shot LLM) | MetroLens AI Target (v0.3) | Empirical Result (Day 7–8 Benchmark) | Test Environment / Hardware |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **OCR CER** | Character Error Rate on declaration crops | $\sim 28\%$ | $< 6.0\%$ | *[To be recorded]* | Laptop CPU (quad-core, no GPU) |
| **OCR WER** | Word Error Rate on mandatory fields | $\sim 36\%$ | $< 10.0\%$ | *[To be recorded]* | Laptop CPU (quad-core, no GPU) |
| **MRP & Qty Extraction F1** | F1-score of numerical quantity & price | $0.70$ | $> 0.94$ | *[To be recorded]* | Python Regex + Normalizer |
| **Contact Details F1** | F1-score of email & telephone extraction | $0.72$ | $> 0.95$ | *[To be recorded]* | Python Regex (RFC 5322 / Telecom) |
| **Font Measurement MAE** | Mean Absolute Error vs optical scan | $0.85\text{ mm}$ (Uncalibrated) | $< 0.15\text{ mm}$ (Calibrated) | *[To be recorded]* | Planar surface, $<15^\circ$ tilt |
| **Measurement $\epsilon_{95}$** | 95th percentile worst-case error bound | $1.60\text{ mm}$ | $< 0.25\text{ mm}$ | *[To be recorded]* | Planar surface, $<15^\circ$ tilt |
| **Violation Recall** | Proportion of defective packages caught | $60.0\%$ | $> 95.0\%$ | *[To be recorded]* | Phase 2 Benchmark Set |
| **False Positive Rate (FPR)**| Compliant packages falsely penalized | $35.0\%$ | $< 5.0\%$ | *[To be recorded]* | Phase 2 Benchmark Set |
| **USP Math Accuracy** | Precision in catching calculation errors | $65.0\%$ (LLM float division) | **100%** (Deterministic math) | *[To be recorded]* | IEEE 754 Python unit tests |
| **End-to-End Latency** | Full scan-to-report processing time | $4.5\text{s}$ (Cloud APIs) | $< 2.5\text{s}$ (Local ONNX) | *[To be recorded]* | Demonstrator Laptop Localhost |

---

## 6. Optical Stress Testing Matrix

| Optical Stress Condition | Test Package Count | System Mitigation Strategy | Acceptance Criteria |
| :--- | :---: | :--- | :--- |
| **Specular Glare** | 6 SKUs (Glossy foil pouches) | Real-time HSV saturation check ($V > 250, S < 30$) | Viewfinder rejects capture if glare covers $>5\%$ of ROI |
| **Perspective Tilt ($15^\circ\text{–}30^\circ$)** | 8 SKUs (Tilted carton faces) | Viewfinder coplanarity guide + metric scale recovery | Font measurement error remains $< 0.20\text{mm}$ |
| **Right Cylindrical Curvature** | 6 SKUs (Beverage cans) | Vertical generator strip measurement within central $40^\circ$ | Vertical font height matches flat label scan |
| **Low Ambient Lighting ($<50\text{ lx}$)** | 4 SKUs | Adaptive local contrast normalization (CLAHE) | OCR CER increases by no more than $3.0\%$ |
| **Multilingual Text (Hindi)** | 6 SKUs (Bilingual FMCG) | PaddleOCR Devanagari model + Hindi dictionary mapping | MRP & Net Qty extracted with F1 $> 0.90$ |
| **Faded Dot-Matrix Inkjet Print**| 4 SKUs (Mfg dates) | Morphological dilation filter bridging dot gaps | Date extracted without human intervention |
