# STATUTORY LEGAL RULE MATRIX & REGULATORY FOUNDATION (V0.2)
## Legal Metrology (Packaged Commodities) Rules, 2011 (As Amended up to September 2026)

**Governing Parent Statute:** The Legal Metrology Act, 2009 (Act No. 1 of 2010) as amended by the **Jan Vishwas (Amendment of Provisions) Act, 2023 (Act No. 18 of 2023)**  
**Nodal Ministry:** Ministry of Consumer Affairs, Food & Public Distribution (Department of Consumer Affairs)  
**System Role Definition:** Automated Regulatory Compliance Audit & Evidentiary Screening System (Assists Legal Metrology Officers under Section 15; does NOT issue unilateral penalties or judicial orders)

---

## 1. Statutory Architecture & Enforcement Reality (Jan Vishwas Act, 2023)

### Crucial Legal Clarification on Section 36 Enforcement & Improvement Notices
Competing proposals and outdated student projects frequently claim that software can "issue automated fines or compounding notices of ₹25,000 to ₹1,00,000". **Under current Indian law as of September 2026, this is legally false.**

1. **Decriminalization & The Improvement Notice Mechanism (Section 36(1)):**
   - The **Jan Vishwas (Amendment of Provisions) Act, 2023** fundamentally overhauled Section 36(1) of the Legal Metrology Act, 2009, removing criminal prosecution for first-time packaging declaration non-compliances (Rules 6, 7, 8, 9, 11).
   - For pre-packaged commodities not conforming to mandatory declarations or font sizes, the statute mandates an **Improvement Notice** for the **First Offence**.
   - The manufacturer, packer, or importer is granted a statutory compliance window (typically 15 to 30 days) to rectify the non-compliance. If rectified, proceedings are closed with **no financial penalty**.
   - Financial penalties apply only upon failure to comply with an Improvement Notice or for repeated offences, and these penalties must be formally adjudicated by a designated **Adjudicating Officer** appointed under Section 48A—**never via automated software summons**.
2. **Short-Weight / Under-Measure Distinction (Section 36(2)):**
   - For net quantity shortages (e.g., selling 82g in a container declared as 100g), penalties remain stringent under Section 36(2) (first offence up to ₹1,00,000; repeated up to ₹5,00,000).
   - **Critical Physical Boundary:** Monocular computer vision **cannot weigh an object**. Software must explicitly declare that Section 36(2) physical weight verification requires a physical check-weighing scale certified under Rule 24.
3. **Evidentiary Role of the System (Section 15 & Section 63 BSA / Section 65B IEA):**
   - Under **Section 15** of the Legal Metrology Act, 2009, a Legal Metrology Officer (LMO) has the power of inspection, entry, search, and seizure.
   - MetroLens AI functions as a **Prima Facie Evidentiary Audit Tool**: it captures tamper-evident proof (cryptographic SHA-256 hashes, GPS coordinates, ISO-8601 timestamps, calibrated optical measurements) providing lawful justification for an inspecting officer to issue an Improvement Notice or seize physical samples under Form 1.

---

## 2. Master Legal Rule Matrix (Amended up to September 2026)

| Rule Reference | Current Legal Source | Statutory Requirement | Verifiability Classification | Required Extracted Data | Automation & Verification Method | Verifiability Tier & Confidence | Statutory Exceptions & Nuances |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **Rule 6(1)(a)** | LM(PC) Rules 2011; GSR 779(E) | Name and complete address of manufacturer. If packer is distinct, both names and addresses. For imported goods, name and address of importer. | **Partially Verifiable** | Manufacturer / Packer / Importer block, Street/Area, City, State, PIN code. | OCR text detection $\rightarrow$ Entity extraction $\rightarrow$ Syntactic validation (checks presence of 6-digit Indian PIN code regex, keywords "Mfg by", "Packed by", "Mkt by"). | **High Syntactic (>95%)**<br>*Semantic truth unverified* | Abbreviated address permitted if package surface area $< 10\text{ cm}^2$. Cannot verify physical existence of factory without MCA21 / GSTN API or physical officer visit. |
| **Rule 6(1)(b)** | LM(PC) Rules 2011 | Generic or common name of the commodity contained in the package. Brand/trademark alone does not satisfy this requirement. | **Image-Verifiable** | Generic commodity descriptor (e.g., "Potato Chips", "Refined Sunflower Oil"). | Multilingual OCR $\rightarrow$ String normalization against National Product Catalog / Food Safety Category taxonomy. | **High (>90%)** | For combo packs containing distinct commodities, each generic name must appear. Lab chemical testing required to confirm contents match label. |
| **Rule 6(1)(c)** | LM(PC) Rules 2011; GSR 779(E) | Net quantity in standard units of weight or measure (mass, volume, length, area, or count). Non-metric units prohibited. | **Image-Verifiable** | Numerical quantity + approved SI unit symbol (`g`, `kg`, `ml`, `l`, `m`, `N`, `U`, `pieces`). | Deterministic Regex parser validating approved SI symbols. Flags illegal notations: `Gms`, `gms`, `Kgs`, `k.g.`, `ML`, `ltrs`. Enforces decimal notation over vulgar fractions. | **Deterministic (100% logic, >98% OCR)** | Rule 26 exemption: Packages with net quantity $\le 10\text{g}$ or $\le 10\text{ml}$ exempt (except tobacco/pan masala). Fast-food counter items exempt. |
| **Rule 6(1)(d)** | LM(PC) Rules 2011; FSSAI Harmonization | Month and year of manufacture, packing, or import (e.g., "08/2026", "Aug 2026", "Packed: 08/26"). Best Before / Use By required for perishable items. | **Image-Verifiable** | Date tokens, month/year qualifiers, expiry / shelf-life text. | Multilingual date regex pattern matching + temporal sanity check (flags future dates $>30$ days or expired shelf-life). | **High (>95%)** | Faded dot-matrix inkjet printing on crimped edges requires adaptive contrast enhancement (CLAHE). Electronic items may declare via QR code under circular. |
| **Rule 6(1)(e)** | LM(PC) Rules 2011 | Maximum Retail Price (MRP) in mandatory format including retail sale price and tax inclusivity qualifier. | **Image-Verifiable** | Currency symbol (`₹`, `Rs.`), price value (float), tax inclusivity qualifier string. | Deterministic Regex extracting price value and validating presence of semantic qualifier: "inclusive of all taxes", "incl. of all taxes", or "कर सहित". | **Deterministic (100% logic, >97% OCR)** | Rounding rules: fraction of a rupee rounded to nearest 50 paise or whole rupee. Overwriting or pasting a sticker over original MRP is a violation under Section 36. |
| **Rule 6(1)(f) & Rule 6(11)** | GSR 779(E) (2021); Enforced Oct 1, 2022 | Mandatory Unit Sale Price (USP) where package contains $>1$ unit or $>1\text{kg/L}$. Must follow standardized denominations. | **Image-Verifiable & Mathematically Auditable** | Declared USP float + unit denomination, extracted MRP, extracted Net Quantity. | Deterministic Arithmetic Validator: Computes expected USP in standard denomination. Flags discrepancies exceeding $\pm 1\%$ rounding tolerance and non-standard units. | **Deterministic (100% mathematical audit)** | Denomination mapping:<br>• Net Qty $< 1\text{kg}$: ₹/g or ₹/100g<br>• Net Qty $\ge 1\text{kg}$: ₹/kg<br>• Net Qty $< 1\text{L}$: ₹/ml or ₹/100ml<br>• Net Qty $\ge 1\text{L}$: ₹/L<br>• Sold by count: ₹/item or ₹/piece.<br>Exemption: Packages where net quantity = 1 or where package price = unit sale price. |
| **Rule 6(1)(g)** | LM(PC) Rules 2011 | Consumer Care details: Name, physical address, telephone number, and official email address of person/office handling consumer complaints. | **Image-Verifiable** | Contact name/designation, physical address, 10-digit/toll-free phone number, email address. | RFC 5322 regex for email validation + Indian telecom regex (toll-free 1800/1860, STD landlines, +91 mobile). | **High (>96%)** | Statute mandates BOTH phone AND email. Omission of either channel constitutes a non-compliance. |
| **Rule 6(1)(h)** | LM(PC) Rules 2011 | Country of origin on all imported commodities: "Country of Origin: [Name]" or "Made in [Country]". | **Image-Verifiable** | Country name token, origin phrasing. | ISO 3166-1 country lookup dictionary + phrase regex ("Made in", "Country of Origin", "Product of"). | **High (>95%)** | Mandatory on all imported commodities. On domestic products, absence is permitted if manufacturer address in India is clearly stated. |
| **Rule 6(10)** | LM(PC) Amendment 2017 & 2021 | E-Commerce Marketplace Listings: Digital listing must display mandatory declarations except mfg date. | **Web/Platform Verifiable** *(Post-Hackathon)* | Listing attributes and packshot images (Amazon, Blinkit, Zepto, Flipkart). | Headless DOM inspection / packshot OCR verifying presence of generic name, net qty, MRP, USP, manufacturer, origin. | **High (>90%)** | INTERMEDIARY LIABILITY: Marketplaces liable under Section 36(1) for non-compliant listings. Scoped out of hackathon MVP to protect team bandwidth. |
| **Rule 7 & Rule 2(h)** | LM(PC) Rules 2011 | Principal Display Panel (PDP) dimensions: part of package likely to be displayed. Rectangular: $H \times W$; Cylindrical: $40\% \times (H \times \text{Circumference})$; Other: $20\%$ total surface. | **Partially Verifiable (Requires Coplanar Reference)** | Packaging outer boundary bounding box, scale factor from metric reference. | Package boundary segmentation $\rightarrow$ metric homography transformation to metric centimeters $\rightarrow$ PDP area calculation ($A\text{ cm}^2$). | **Medium-High (85–90%)** | Monocular camera requires known planar scale anchor (standard 10-Rupee coin or ISO card) to calculate physical area in $\text{cm}^2$. |
| **Rule 8** | LM(PC) Rules 2011 | Prominence, Placement & Clear Space: Declarations must be legible, conspicuous, and maintain clear blank space around net quantity numeral (equal to numeral height above/below, twice width left/right). | **Image-Verifiable** | Numeral bounding box, neighboring text/graphic bounding boxes, stroke clarity. | Spatial intersection query on OCR bounding boxes + background uniformity check around the net quantity numeral. | **Medium-High (85–90%)** | Decorative artwork or graphic splashes overlapping quantity numeral violate Rule 8. Declarations permitted in Hindi or English. |
| **Rule 9 & Table 1** | LM(PC) Rules 2011 | Statutory Minimum Font Height: Minimum numeral and letter heights based on PDP area $A$ and Net Quantity:<br>• $A \le 50\text{ cm}^2 \rightarrow \ge 1.0\text{ mm}$<br>• $50 < A \le 100\text{ cm}^2 \rightarrow \ge 1.5\text{ mm}$<br>• $100 < A \le 500\text{ cm}^2 \rightarrow \ge 2.5\text{ mm}$<br>• $500 < A \le 2500\text{ cm}^2 \rightarrow \ge 4.0\text{ mm}$<br>• $A > 2500\text{ cm}^2 \rightarrow \ge 6.0\text{ mm}$<br>Width must be $\ge \frac{1}{3}\text{ Height}$ (except numeral "1"). | **Partially Verifiable (Strict Calibration Required)** | PDP Area $A$, Bounding box of numerals in Net Quantity, USP, and MRP, metric pixel-to-mm scale. | Metric calibration via reference anchor $\rightarrow$ character contour extraction $\rightarrow$ vertical stroke height measurement (x-height in mm) $\rightarrow$ Table 1 lookup. | **Target MAE: $\pm 0.12\text{ mm}$**<br>*Borderline cases: Manual Review* | Blown, formed, or molded packaging has higher thresholds (2.0mm, 3.0mm, 4.0mm, 6.0mm, 8.0mm). Software implements a $0.10\text{ mm}$ statutory benefit-of-doubt buffer. |
| **Rule 26** | LM(PC) Rules 2011 | Statutory Exemptions: Packages $\le 10\text{g}$ or $\le 10\text{ml}$ (except tobacco); industrial packages $> 25\text{kg}$ or $> 25\text{L}$; fast-food counter items; LPG cylinders. | **Image-Verifiable** | Extracted Net Quantity number and unit, product category. | Conditional rule switch: If Net Qty $\le 10\text{g}$ or $\le 10\text{ml}$ and category is NOT tobacco/pan masala, engine flags `STATUTORY_EXEMPTION_APPLIED`. | **Deterministic (100%)** | Prevents false-positive violations on miniature hotel soaps, ketchup sachets, or single chewing gum packs. |
| **Medical Devices (2025)** | GSR 778(E) (Oct 24, 2025) | Medical Devices Rule Harmonization: Packaging of medical devices governed under Medical Devices Rules, 2017 supersedes LM(PC) font size rules. | **Categorical Exception** | Product category classification. | If product is identified as Medical Device (CDSCO licensed), Rule 9 font height checks are bypassed in favor of MDR 2017 standards. | **High (>95%)** | Prevents erroneous notices against syringes, IV sets, or diagnostic kits. |
| **Pan Masala (2025/2026)** | GSR 881(E) (Dec 2, 2025; in force Feb 1, 2026) | Revocation of Pan Masala packaging exemptions: Full declaration sizes and font heights mandatory on all pouch sizes. | **Categorical Inclusion** | Product category classification ("Pan Masala", "Gutkha"). | Engine strictly enforces standard Rule 9 Table 1 thresholds with zero miniature pouch exemptions. | **Deterministic (100%)** | High government enforcement priority area. |
| **QR Code Circular (2022/2023)** | DCA Circulars on Electronic Products | Electronic Products QR Code Exemption: Electronic items permitted to declare address, consumer care, and specs via external QR code, provided MRP, Net Qty, Mfg Date, and Country are physical. | **Image-Verifiable** | Barcode / QR code detector + physical declaration presence. | QR code detection + payload URL verification. If electronic commodity, missing address on carton is permitted if valid QR code is present. | **High (>92%)** | Restricted strictly to electronic products; food and cosmetics cannot substitute physical declarations with QR codes. |

---

## 3. Strict Boundary: Image-Verifiable vs. Laboratory/Physical Testing

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     STATUTORY VERIFICATION BOUNDARIES                    │
├──────────────────────────────────┬───────────────────────────────────────┤
│    IMAGE-VERIFIABLE BY SYSTEM    │      PHYSICAL / EXTERNAL REALITY      │
│  (What MetroLens AI evaluates)   │   (Requires physical tools or labs)   │
├──────────────────────────────────┼───────────────────────────────────────┤
│ • Presence of mandatory fields   │ • Actual physical net weight inside   │
│ • SI unit syntax (g vs Gms)      │   (Requires certified weighing scale) │
│ • Tax inclusivity text on MRP    │ • Chemical / nutritional purity       │
│ • Mathematical USP correctness   │   (Requires FSSAI chemical lab test)  │
│ • Valid email and phone syntax   │ • Physical factory existence at PIN   │
│ • Area-proportional font height  │   (Requires physical officer visit)   │
│ • Clear blank space prominence   │ • Sub-surface tamper/re-sealing       │
│ • Rule 26 miniature exemption    │ • Dynamic wholesale invoice pricing   │
└──────────────────────────────────┴───────────────────────────────────────┘
```

---

## 4. Statutory Language Guidelines for Software Output
1. **Never Output:** *"This package is 100% legally compliant under Indian Law."*
2. **Always Output:** *"Image-Based Compliance Assessment: No image-verifiable non-compliances detected under Rules 6, 7, 8, 9, 11 of LM(PC) Rules, 2011."*
3. **Never Output:** *"Penalty of ₹25,000 imposed."*
4. **Always Output:** *"Potential Non-Compliance Flagged. Recommended Regulatory Action: Issue Improvement Notice under Section 36(1) (as amended by Jan Vishwas Act, 2023) or verify physical sample under Section 15."*
