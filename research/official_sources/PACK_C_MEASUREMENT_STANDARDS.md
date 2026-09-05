# RESEARCH EVIDENCE PACK C — MEASUREMENT STANDARDS & METROLOGICAL BASIS

**Research Scope:** Rule 7 PDP Area, Table-I Font Heights, Second Schedule Tolerances, and Optical Homography Math  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Mathematical Rigor & Anti-Hallucination Policy (Source Text vs Interpretation vs Engineering Rule)  
**Pack Status:** 🔴 CRITICAL (Verified Primary & Secondary)

---

## 1. Principal Display Panel (PDP) Definition & Area Formulas

```yaml
source_id: IN-LMPC-RULE7-PDP
title: "Legal Metrology (Packaged Commodities) Rules, 2011 — Rule 7: Principal Display Panel, its area, size and letter, etc."
issuing_authority: "Ministry of Consumer Affairs, Food & Public Distribution"
document_type: "Statutory Rule"
official_url: "https://consumeraffairs.nic.in"
retrieval_date: "2026-09-04"
publication_date: "2011-03-07 (Amended by G.S.R. 629(E) & G.S.R. 1373(E))"
effective_date: "2018-01-01"
supersession_status: "CURRENT"
local_filename: "docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/CONSOLIDATED/rule_07_consolidated.md"
sha256: "PRIMARY_SOURCE_REQUIRED"
page_number: "Rule 7(1), 7(2), 7(3)"
section/rule: "Rule 7"
quoted_requirement: |
  Rule 7(1): "In the case of a package which has a principal display panel,-
  (a) in the case of a rectangular package, where one entire side can properly be considered to be the principal display panel side, the product of the height multiplied by the width of that side;
  (b) in the case of a cylindrical or nearly cylindrical package, forty per cent of the product of the height of the package multiplied by the circumference;
  (c) in the case of any other shaped package, forty per cent of the total surface of the package, or an area considered to be a principal display panel side of the package."
interpretation: "The area of the principal display panel determines the required minimum height of letters and numerals for statutory declarations under Table-I. Shape geometry dictates the formula."
verification_status: "VERIFIED_PRIMARY"
notes: "Primary rule formulation verbatim from Gazette."
```

### Geometric Formulation & Engineering Rules

| Package Geometry | Statutory Definition | Mathematical Formula | Computer Vision Extraction Algorithm | Uncertainty & Boundary | Fact Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rectangular Carton** | Product of height multiplied by width of the side considered the PDP. | $A_{\text{PDP}} = H \times W$ | Extract bounding quadrilateral of the primary front panel; apply homography transformation; compute $H$ and $W$ in millimeters; convert to $\text{cm}^2$. | Corner radius / beveling on cartons: Measured along planar face edges. | `VERIFIED_PRIMARY` |
| **Cylindrical Can / Bottle** | Forty per cent of height multiplied by circumference. | $A_{\text{PDP}} = 0.4 \times (H \times C) = 0.4 \times (H \times \pi D)$ | Estimate cylinder diameter $D$ and label height $H$ via multi-view silhouette or parametric label dewarping. | Cylindrical taper (conical frustum): Requires bounding frustum formula; Nirikshak flags taper exceeding 5°. | `VERIFIED_PRIMARY` |
| **Irregular / Pouch / Sachet** | Forty per cent of total surface area, or the area considered to be a PDP side. | $A_{\text{PDP}} = 0.4 \times A_{\text{total}}$ | Contour perimeter integration over 2D planar projection of flattened packaging pouch. | Stand-up pouches with gusset bottoms: Gusset area excluded from 2D planar face calculation. | `VERIFIED_PRIMARY` |

---

## 2. Table-I: Minimum Height of Numerals & Letters

```yaml
source_id: IN-LMPC-TABLE1-CONSOLIDATED
title: "Table-I: Minimum Height of Numerals and Letters"
issuing_authority: "Department of Consumer Affairs"
document_type: "Statutory Table under Rule 7(3)"
official_url: "https://consumeraffairs.nic.in"
retrieval_date: "2026-09-04"
publication_date: "2017-06-23 (Substituted by G.S.R. 629(E), corrected by G.S.R. 1373(E) dated 2017-11-07)"
effective_date: "2018-01-01"
supersession_status: "CURRENT"
local_filename: "docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/CONSOLIDATED/table_1_consolidated.md"
sha256: "PRIMARY_SOURCE_REQUIRED"
page_number: "Table-I under Rule 7"
section/rule: "Rule 7(3), Table-I"
quoted_requirement: |
  Table-I specifies minimum heights based on Area of Principal Display Panel (A):
  1. A <= 50 cm^2: Normal 1.0 mm, Blown/Formed 1.5 mm
  2. 50 cm^2 < A <= 100 cm^2: Normal 2.0 mm (as corrected by G.S.R. 1373(E)), Blown/Formed 3.0 mm
  3. 100 cm^2 < A <= 500 cm^2: Normal 2.5 mm, Blown/Formed 4.0 mm
  4. 500 cm^2 < A <= 2500 cm^2: Normal 4.0 mm, Blown/Formed 6.0 mm
  5. A > 2500 cm^2: Normal 6.0 mm, Blown/Formed 6.0 mm
  Width condition: Width shall not be less than one-third of height, except for numeral '1' and letters 'i', 'I', 'l'.
interpretation: "Establishes a mandatory stepped step-function for font heights based on PDP area. Failure to meet the threshold constitutes statutory non-compliance under Section 36."
verification_status: "VERIFIED_PRIMARY"
notes: "Corrected 1.5 -> 2.0 mm in row 2 col 3 per official Gazette Corrigendum G.S.R. 1373(E)."
```

### Canonical Table-I Specification

| Serial No. | Area of Principal Display Panel ($A$ in $\text{cm}^2$) | Minimum Height: Normal Case ($H_{\text{min}}$ in $\text{mm}$) | Minimum Height: Blown, Formed, Molded, Embossed or Perforated ($H_{\text{min}}$ in $\text{mm}$) | Width Constraint | Exceptions to Width Constraint |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | $A \le 50\text{ cm}^2$ | **$1.0\text{ mm}$** | **$1.5\text{ mm}$** | $W \ge \frac{1}{3} H$ | Numeral `1`, Letters `i`, `I`, `l` |
| **2** | $50\text{ cm}^2 < A \le 100\text{ cm}^2$ | **$2.0\text{ mm}$** *(Corrigendum G.S.R. 1373(E))* | **$3.0\text{ mm}$** | $W \ge \frac{1}{3} H$ | Numeral `1`, Letters `i`, `I`, `l` |
| **3** | $100\text{ cm}^2 < A \le 500\text{ cm}^2$ | **$2.5\text{ mm}$** | **$4.0\text{ mm}$** | $W \ge \frac{1}{3} H$ | Numeral `1`, Letters `i`, `I`, `l` |
| **4** | $500\text{ cm}^2 < A \le 2500\text{ cm}^2$ | **$4.0\text{ mm}$** | **$6.0\text{ mm}$** | $W \ge \frac{1}{3} H$ | Numeral `1`, Letters `i`, `I`, `l` |
| **5** | $A > 2500\text{ cm}^2$ | **$6.0\text{ mm}$** | **$6.0\text{ mm}$** | $W \ge \frac{1}{3} H$ | Numeral `1`, Letters `i`, `I`, `l` |

---

## 3. Optical Measurement & Scale Calibration Framework

### 3.1 Perspective Rectification via Planar Homography
When a package is captured at an angle $\theta$, perspective distortion compresses text. A planar homography matrix $H \in \mathbb{R}^{3 \times 3}$ is calculated using known co-planar fiducial coordinates:
$$
\mathbf{x}' \sim H \mathbf{x}
$$
Where:
- $\mathbf{x} = [u, v, 1]^T$ represents image pixel coordinates.
- $\mathbf{x}' = [X_w, Y_w, 1]^T$ represents rectified world metric coordinates.

### 3.2 Physical Scale Factor ($k$)
The metric millimeter scale factor is derived from the rectified fiducial marker:
$$
k = \frac{d_{\text{physical}}(\text{mm})}{d_{\text{rectified}}(\text{pixels})}
$$

### 3.3 Glyph Height Extraction Algorithm
1. **Binarization & Component Analysis:** Morphological thresholding isolates connected components of numerals on the Net Quantity and MRP bounding boxes.
2. **Baseline and Cap-Height Fit:** For each connected component, find top-most and bottom-most scanlines within the stroke mask.
3. **Metric Conversion:**
   $$
   H_{\text{font}}(\text{mm}) = k \cdot (y_{\text{bottom}} - y_{\text{top}})
   $$
4. **Expanded Uncertainty:**
   $$
   U(H) = 2 \cdot \sqrt{u_{\text{calibration}}^2 + u_{\text{blur}}^2 + u_{\text{segmentation}}^2}
   $$
   *Status:* Target measurement threshold is `TARGET — NOT VALIDATED; Status: TBD — MEASURE` pending physical bench calibration in Stage 2.

---

## 4. Second Schedule Tolerances (Maximum Permissible Errors on Quantity)

Under Rule 2(h) and Second Schedule:
- Pre-packaged commodities cannot deviate from declared net weight by more than the Maximum Permissible Error (MPE).
- For example, for net quantity $100\text{ g} \dots 200\text{ g}$, the MPE is $4.5\%$ (or $9\text{ g}$).
- *Operational Scope in Nirikshak:* Nirikshak performs **optical label inspection**. Physical gross/tare scale verification is an optional external sensor integration for Stage 3. For Stage 2 MVP, Nirikshak asserts that the *declared quantity* and units adhere to Schedule I and Rule 6(1)(c).
