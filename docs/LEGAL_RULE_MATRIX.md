# STATUTORY LEGAL RULE MATRIX & REGULATORY FOUNDATION (V0.3)
## Legal Metrology (Packaged Commodities) Rules, 2011 (Consolidated as of September 2026)

**Governing Parent Statute:** The Legal Metrology Act, 2009 (Act No. 1 of 2010)  
**Enforcement Amendment:** Jan Vishwas (Amendment of Provisions) Act, 2026 — Legal Metrology provisions effective **1 May 2026** [PRIMARY RESEARCH FINDING — PIB PRID 2278745]  
**Nodal Ministry:** Ministry of Consumer Affairs, Food & Public Distribution (Department of Consumer Affairs)  
**System Role Definition:** Image-based compliance assessment tool that supports inspection workflows. Does NOT issue penalties, generate statutory notices, or claim legal standing independently. [ENGINEERING DECISION]

> **V0.3 CORRECTION:** V0.2 incorrectly attributed the Improvement Notice mechanism to "Jan Vishwas (Amendment of Provisions) Act, 2026". The operative enforcement mechanism is the **Jan Vishwas (Amendment of Provisions) Act, 2026**, effective 1 May 2026. See `LEGAL_CHANGELOG_2025_2026.md` for complete amendment chronology.

---

## 1. Current Enforcement Architecture (Jan Vishwas Act, 2026)

### Section 36(1) — Packaging Declaration Non-Compliances [PRIMARY RESEARCH FINDING]

```
INSPECTION by authorized officer (Section 15)
    ↓
DETECTION of potential Section 36(1) non-compliance
    ↓
FIRST OFFENCE?
    ├── YES → IMPROVEMENT NOTICE
    │         → Compliance window (prescribed period)
    │         → If rectified: MATTER CLOSED (no penalty)
    │         → If not rectified: ADJUDICATION (Section 48A)
    │
    └── NO (repeat offence) → DIRECT ADJUDICATION
         → 2nd offence: higher penalties
         → 3rd offence: ₹25 lakh to ₹50 lakh [SECONDARY RESEARCH]

SCOPE: Section 36(1) now explicitly includes e-commerce platforms,
       online marketplaces, and electronic service providers.
```

### Section 36(2) — Short Weight / Under-Measure
- Separate and stricter penalties remain (first offence up to ₹1,00,000; repeat up to ₹5,00,000)
- **MetroLens CANNOT verify net weight** — monocular camera cannot weigh objects
- Physical check-weighing under Rule 24 with certified scale is required

### MetroLens System Role — Precise Legal Positioning [ENGINEERING DECISION]
- MetroLens is designed to **support authorized inspection workflows**
- It provides image-based preliminary assessment and evidence packaging
- It does NOT: issue penalties, generate statutory notices, claim evidentiary standing independently, or make binding legal determinations
- A hash (SHA-256) provides **integrity verification** (tamper-evident record), NOT digital signature, authentication, or legal certification

> **V0.3 CORRECTIONS FROM V0.2:**
> - Removed: "supporting inspection evidence Audit Tool" → Replaced with: "image-based compliance assessment tool"
> - Removed: "cryptographically sealed" → Replaced with: "tamper-evident integrity record (SHA-256)"
> - Removed: "provides lawful justification under Section 15" → Replaced with: "designed to support authorized inspection workflows"
> - Removed: "Form 1" references → Form references removed pending verification of current statutory form numbering

---

## 2. Package Applicability Gate

Before checking individual rules, the system must determine whether a package falls within scope. [ENGINEERING DECISION]

```
STEP 1: Is this a pre-packaged commodity intended for retail sale?
    ├── NO → NOT APPLICABLE (Rules do not apply)
    └── YES ↓

STEP 2: Is the package within scope exclusions?
    ├── Rule 3: Industrial/institutional package? → EXCLUDED
    ├── Rule 3: Net Qty > 25 kg or > 25 L? → EXCLUDED (wholesale/bulk)
    ├── Rule 26(a): Net Qty ≤ 10g or ≤ 10ml? 
    │     ├── AND category is pan masala? → NOT EXEMPT (G.S.R. 881(E))
    │     ├── AND category is tobacco? → NOT EXEMPT
    │     └── OTHERWISE → EXEMPT from most declarations
    ├── Rule 26: Fast-food counter items? → EXEMPT
    ├── Rule 26: Scheduled formulations (Drugs Price Control)? → EXEMPT
    └── G.S.R. 778(E): Medical device? → GOVERNED BY Medical Devices Rules, 2017

STEP 3: What category does this package belong to?
    → Determines applicable regulatory profile (see Section 4)

STEP 4: Which Rule 6 declarations apply?
    → Category-specific checklist (see Section 3)
```

> **V0.3 CORRECTION:** V0.2 incorrectly placed all scope exclusions under Rule 26. Industrial/institutional and >25 kg/>25 L exclusions derive from Rule 3 (application scope). Rule 26 covers specific exemptions (small packs, fast food, scheduled drugs). The system must correctly attribute each exclusion.

---

## 3. Master Rule 6 Declaration Map (Current Consolidated)

### Rule 6(1) Clause Structure [PRIMARY RESEARCH FINDING — Indian Kanoon]

| Clause | Requirement | Image-Verifiable? | Notes |
|:---|:---|:---:|:---|
| **6(1)(a)** | Name and complete address of manufacturer/packer/importer | Partially | Cannot verify physical existence of address |
| **6(1)(aa)** | Country of origin (imported goods) | Yes | Added by G.S.R. 779(E) 2021 |
| **6(1)(b)** | Common or generic name of commodity | Yes | Brand/trademark alone insufficient |
| **6(1)(c)** | Net quantity in standard SI units | Yes | Deterministic SI validation |
| **6(1)(d)** | Month and year of manufacture/packing/import; best before/use by for perishables | Yes | Date parsing + temporal validation |
| **6(1)(da)** | [UNKNOWN / UNVERIFIED] — Verify whether clause (da) exists in current consolidated rules | — | Research required |
| **6(1)(e)** | Maximum Retail Price (MRP) inclusive of all taxes | Yes | Deterministic regex + qualifier check |
| **6(1)(f)** | [Verify current assignment — may relate to consumer care or other] | — | Cross-check against consolidated text |
| **6(1)(g)** | Consumer care details (name, address, phone, email) | Yes | Both phone AND email mandatory |
| **6(1)(h)** | [Verify current assignment — country of origin may have moved to (aa)] | — | Original (h) may have been re-assigned |
| **6(10)** | E-commerce marketplace listing declarations | Post-MVP | Currently deferred |
| **6(10A)** | E-commerce country-of-origin filters (G.S.R. 128(E), effective 1 Jul 2026) | Post-MVP | Currently deferred |
| **6(11)** | Unit Sale Price (USP) — added by G.S.R. 226(E), effective 1 Oct 2022 | Yes + Math | See USP section below |

> **V0.3 NOTE:** The exact current clause numbering of Rule 6(1) requires line-by-line verification against the latest consolidated text. Clauses (da), (f), and (h) need specific verification. The system should not hard-code clause references that may have shifted due to amendments. Mark as [UNKNOWN / UNVERIFIED] until confirmed.

---

## 4. Category Classification → Applicable Regulatory Profile [ENGINEERING DECISION]

The system must NOT apply a universal "every package → same checklist". Different commodity categories have different regulatory interactions.

### MVP Supported Categories (Recommended: 1–2 deeply defensible)

| Category | LM(PC) Rules Apply? | Regulatory Interactions | MVP Recommendation |
|:---|:---:|:---|:---|
| **FMCG / Grocery** (biscuits, snacks, dry goods) | Yes | Food articles have special treatment under Rule 6 re: FSSAI labelling overlap. Rule 7(5) exempts certain provisions when information is required under another law. | PRIMARY — most common inspection target |
| **Household / Personal Care** (soap, sanitizer, detergent) | Yes | Fewer regulatory overlaps. BIS marking may apply separately. | SECONDARY — good fallback category |
| **Electronics accessories** (cables, batteries, chargers) | Yes | QR code circular permits partial electronic declaration. | OPTIONAL — if time permits |
| **Beverages** (water, juice, carbonated drinks) | Yes | FSSAI + LM overlap. Liquid-specific USP rules apply. | DEFER to v2 unless trivial |
| **Cosmetics** | Yes | Drugs & Cosmetics Act overlap for certain declarations | DEFER |
| **Medical Devices** | **NO** | Carved out by G.S.R. 778(E) Oct 2025 → Medical Devices Rules, 2017 | **EXCLUDED** |
| **Pan Masala** | Yes (enhanced) | G.S.R. 881(E) removes small-pack exemption | AWARENESS only |
| **Tobacco** | Yes (enhanced) | Never exempt from Rule 26(a) small-pack exemption | AWARENESS only |

> **V0.3 CORRECTION:** V0.2 stated medical devices "bypass Rule 9 font height rules". This is too narrow — G.S.R. 778(E) carves medical devices out of the entire LM(PC) Rules declaration framework, not just font heights.

---

## 5. Rule 7 — Font Height Tables & PDP (CORRECTED) [PRIMARY RESEARCH FINDING — Indian Kanoon doc/151004919]

> **CRITICAL V0.3 CORRECTION:** V0.2 repeatedly cited "Rule 7 Table-I/II" for font-size thresholds. The font-size tables are in **Rule 7**, NOT Rule 9. Rule 8 governs placement/space. Rule 9 governs manner/legibility/contrast. This is a P0 documentation correction.

### Table-I: Minimum Height — Net Quantity Declared by Weight or Volume [OFFICIAL FACT]

| # | PDP Area (A) in cm² | Min Height (normal, mm) | Min Height (blown/formed/molded, mm) |
|:---:|:---|:---:|:---:|
| 1 | A < 50 | 1.0 | 1.5 |
| 2 | 50 ≤ A < 100 | 1.5 | 3.0 |
| 3 | 100 ≤ A < 500 | 2.5 | 4.0 |
| 4 | 500 ≤ A < 2500 | 4.0 | 6.0 |
| 5 | A ≥ 2500 | 6.0 | 6.0 |

### Table-II: Minimum Height — Net Quantity Declared by Length, Area, or Number [OFFICIAL FACT]

| # | PDP Area (A) in cm² | Min Height (normal, mm) | Min Height (blown/formed/molded/embossed/perforated, mm) |
|:---:|:---|:---:|:---:|
| 1 | A ≤ 100 | 1 | 2 |
| 2 | 100 < A ≤ 500 | 2 | 4 |
| 3 | 500 < A ≤ 2500 | 4 | 6 |
| 4 | A > 2500 | 6 | 6 |

### Font Height Decision Matrix [ENGINEERING DECISION]

```
INPUT: Net Quantity Type + PDP Area
    ↓
Is net quantity declared by weight (g/kg) or volume (ml/L)?
    ├── YES → Use Table-I
    └── NO → Is net quantity declared by length, area, or number?
              ├── YES → Use Table-II
              └── UNKNOWN → MANUAL_REVIEW_REQUIRED
    ↓
Is the packaging blown, formed, molded, embossed, or perforated?
    ├── YES → Use Column (3) of applicable table
    └── NO  → Use Column (2) of applicable table
    ↓
COMPARE measured font height against threshold
    ↓
Result:
    • Height ≥ threshold → PASS
    • Height < threshold AND within MEASUREMENT UNCERTAINTY REVIEW BAND → MANUAL_REVIEW_REQUIRED
    • Height < threshold beyond uncertainty band → POTENTIAL_NON_COMPLIANCE
```

### Width Requirement — Rule 7(3) [OFFICIAL FACT]
- Width of letter or numeral ≥ ⅓ of its height
- Exception: numeral "1" and letters (i), (I), (l)

### PDP Area Calculation — Rule 7(4) [OFFICIAL FACT]
- **Rectangular package:** H × W of the principal display panel side
- **Cylindrical or nearly cylindrical:** 40% × (H × circumference)
- **Other shapes:** 40% of total surface area, or the area of the principal display panel
- **Exclusions from area calculation:** top, bottom, flange at top and bottom of cans, shoulders and neck of bottles and jars

> **V0.3 CORRECTION:** V0.2 mixed Legal Metrology PDP formulas with FSSAI food-labelling PDP rules. The above are the ONLY PDP formulas from Rule 7(4) of LM(PC) Rules. Do NOT import FSSAI formulas into the Legal Metrology rules engine.

### Small Package Provision — Rule 7(1) [OFFICIAL FACT]
- Package with capacity ≤ **10 cubic centimetres** (NOT 10 square centimetres)
- May use a card or tape affixed firmly to the package bearing required information

> **V0.3 CORRECTION:** V0.2 contained references to "10 cm²" (square centimetres). The legal threshold is **10 cm³** (cubic centimetres / capacity).

---

## 6. Rule 8 — Placement & Prominence [SECONDARY RESEARCH]

- All mandatory declarations must appear on the **Principal Display Panel**
- Clear blank space required around net quantity numeral: height of numeral above/below, twice width left/right
- If package has outside container/wrapper: must also carry declarations unless wrapper is transparent and inner declarations readable
- Declarations must NOT be placed where they must be read through liquid in the package

---

## 7. Rule 9 — Manner of Declaration (Legibility, Language, Contrast) [SECONDARY RESEARCH]

- Declarations must be **legible and prominent**
- Language: Hindi or English; may also appear in regional language
- MRP and Net Quantity numerals must be in a color that **contrasts conspicuously** with background
- Exception: contrast requirement does not apply to blown/molded/formed/embossed text on glass or plastic containers

> **Rule 9 does NOT contain any font-size table.** It governs HOW declarations appear (legible, prominent, contrasting), not their minimum physical dimensions.

---

## 8. Unit Sale Price (USP) — Rule 6(11) (CORRECTED) [PRIMARY RESEARCH FINDING]

### Current Statutory Logic (G.S.R. 226(E), effective 1 Oct 2022)

| Net Quantity Type | Threshold | USP Denomination |
|:---|:---|:---|
| Weight | < 1 kg | Per gram (₹/g) |
| Weight | ≥ 1 kg | Per kilogram (₹/kg) |
| Length | < 1 m | Per centimetre (₹/cm) |
| Length | ≥ 1 m | Per metre (₹/m) |
| Volume | < 1 L | Per millilitre (₹/ml) |
| Volume | ≥ 1 L | Per litre (₹/L) |
| Count | Any | Per number or per unit |

**Rounding:** To nearest two decimal places  
**Exemption:** Not required when MRP equals USP  
**Exemption:** Not required for combination, group, multi-piece, and wholesale packages [SECONDARY RESEARCH — DCA FAQ]

> **V0.3 CORRECTIONS FROM V0.2:**
> - Removed: "per g or kg" — this denomination does NOT exist in the statute
> - Corrected: "≥ 1 kg" boundary — statute says "less than one kilogram → per gram" and "one kilogram or more → per kilogram"
> - Removed: "±1% tolerance" as though it were a statutory tolerance — if used, it must be labeled as [ENGINEERING COMPARISON TOLERANCE], not a legal requirement
> - Added: exemptions for combination/group/multi-piece/wholesale packages

### USP Verification Architecture [ENGINEERING DECISION]

```
EXTRACT: MRP (₹), Net Quantity (value + unit), Declared USP (₹/unit)
    ↓
DETERMINE: USP denomination from table above
    ↓
COMPUTE: Expected USP = MRP / Net Quantity (in standard denomination)
    ↓
ROUND: to 2 decimal places
    ↓
COMPARE: |Declared USP - Computed USP|
    ↓
Result:
    • Match (within ENGINEERING COMPARISON TOLERANCE) → PASS
    • Mismatch → POTENTIAL_NON_COMPLIANCE
    • Cannot extract reliably → INPUT_INSUFFICIENT
    • Package is combination/group/multi-piece → USP_NOT_REQUIRED
```

> **IMPORTANT DISTINCTION:**
> - **ARITHMETIC CORRECTNESS** = Does declared USP match computed USP? (Engineering check)
> - **STATUTORY DECLARATION COMPLIANCE** = Is USP declared in the correct denomination? Is it present when required?
> - These are separate checks. Do NOT say "USP differs by >1% therefore illegal" unless the law creates such a tolerance. The ±tolerance is our engineering comparison buffer for OCR/rounding variance.

---

## 9. Customary Units (2026 Advisory) [PRODUCT ASSUMPTION — NEEDS VERIFICATION]

A 2026 DCA advisory addressed customary units as supplementary statements alongside standard SI units.

**System must distinguish:**
- ✅ VALID: Standard SI declaration + supplementary customary information (e.g., "500 g (approx. 1.1 lbs)")
- ❌ NON-COMPLIANT: Customary unit used as substitute for SI declaration (e.g., "1.1 lbs" without "500 g")
- ❌ NON-COMPLIANT: Non-standard abbreviations used as the primary declaration (e.g., "500 Gms" instead of "500 g")

> **V0.3 NOTE:** The exact advisory text must be verified. The rule engine must NOT flag a customary unit merely because it exists alongside a valid SI declaration. It must flag only: (a) customary unit used as substitute, or (b) non-standard SI abbreviation used as primary declaration.

---

## 10. Compliance Status Model [ENGINEERING DECISION]

The system must NOT output binary PASS/FAIL for legal compliance. The following status model reflects uncertainty honestly:

| Status | Meaning | When Used |
|:---|:---|:---|
| `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` | All image-checkable rules passed | All checks pass within confidence |
| `POTENTIAL_NON_COMPLIANCE` | Rule violation detected with high confidence | Clear discrepancy found |
| `MANUAL_REVIEW_REQUIRED` | System cannot determine with sufficient confidence | Borderline measurement, low OCR confidence, ambiguous category |
| `NOT_APPLICABLE` | Rule does not apply to this package/category | Exemption or scope exclusion applies |
| `NOT_IMAGE_VERIFIABLE` | Cannot be checked from image alone | Weight verification, factory existence, etc. |
| `INPUT_INSUFFICIENT` | Image quality or OCR too poor to assess | Blurry, occluded, or unreadable |
| `RULE_APPLICABILITY_UNCERTAIN` | Cannot determine which rules apply | Unknown category, ambiguous package type |

> **CRITICAL PRINCIPLE:** `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` ≠ "legally compliant in every respect". The system assesses what the camera can see. It cannot verify physical weight, chemical composition, factory existence, or declarations on unseen panels.

---

## 11. Statutory Language Guidelines for System Output [ENGINEERING DECISION]

| ❌ NEVER Output | ✅ ALWAYS Output Instead |
|:---|:---|
| "This package is 100% legally compliant" | "No image-verifiable non-compliances detected for the assessed declarations" |
| "Penalty of ₹X imposed" | "Potential non-compliance flagged. Recommended: review by authorized officer" |
| "Improvement Notice issued" | "Assessment suggests Improvement Notice may be applicable under current enforcement framework" |
| "supporting inspection evidence evidence" | "Tamper-evident inspection record with integrity metadata" |
| "Chain of custody established" | "Image integrity verified via SHA-256 hash" |
| "Certified inspection report" | "Image-based compliance assessment report" |
