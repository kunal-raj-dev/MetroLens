# LEGAL METROLOGY AMENDMENT CHRONOLOGY (V0.3)
## MetroLens AI — Regulatory Change Audit Trail
**Status:** Living Governance Document | **Last Updated:** 4 September 2026  
**Evidence Classification:** [PRIMARY RESEARCH FINDING] unless otherwise noted  
**Primary Sources:** Department of Consumer Affairs (consumeraffairs.gov.in), Gazette of India (egazette.gov.in), India Code (indiacode.nic.in), Indian Kanoon (indiankanoon.org), Press Information Bureau (pib.gov.in)

---

## Purpose

This document provides a verified chronological record of every Legal Metrology (Packaged Commodities) amendment relevant to MetroLens AI. It serves as the **legal audit trail** ensuring that no rule interpretation in the codebase is based on outdated or incorrectly dated law.

> **GOVERNING PRINCIPLE:** Every legal claim in the MetroLens documentation MUST trace back to an entry in this changelog. If a claim cannot be traced, it must be reclassified as [ENGINEERING DECISION] or [PRODUCT ASSUMPTION].

---

## Chronology

### 2011 — Baseline

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| S.O. 975(E) | 7 Mar 2011 | Legal Metrology (Packaged Commodities) Rules, 2011 — Baseline rules | 7 Mar 2011 | **FOUNDATIONAL** — Establishes Rules 3–26, the entire regulatory framework |

**Key provisions at baseline:**
- Rule 3: Application and scope
- Rule 6: Mandatory declarations (name, address, generic name, net qty, MRP, dates, consumer care)
- Rule 7: Principal Display Panel — area, size, font height tables (Table-I for weight/volume, Table-II for length/area/number), PDP area formulas, width requirements
- Rule 8: Placement and prominence of declarations, clear space requirements
- Rule 9: Manner of declaration — legibility, language (Hindi/English), contrast
- Rule 11: Unit sale price (original version)
- Rule 24: Verification of net contents
- Rule 26: Exemptions

---

### 2015

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 385(E) | 14 May 2015 | Substituted "ten cubic centimetre" in Rule 7(1) | 1 Jan 2016 | **AWARENESS** — Small-package PDP card/tape threshold is 10 cm³ (cubic centimetres), NOT 10 cm² |

---

### 2017

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 629(E) | 23 Jun 2017 | Major restructuring of Rule 7 — substituted sub-rules (2)–(5), replaced Tables, added Table-II for length/area/number, added PDP area calculation formulas, added width ≥ ⅓ height requirement | Retrospective to 7 Mar 2011 | **CRITICAL** — Current Table-I and Table-II structure, PDP formulas, and width rules all originate from this notification |

**Post-2017 Rule 7 structure (current):**
- 7(1): Packages ≤ 10 cm³ — card/tape permitted
- 7(2): Height requirements — Table-I for weight/volume, Table-II for length/area/number
- 7(3): Width ≥ ⅓ height (except "1", "i", "I", "l"); blown/formed/molded thresholds
- 7(4): PDP area determination: (a) rectangular H×W, (b) cylindrical 40% × H × circumference, (c) other 40% total surface
- 7(5): Exemption when information also required under another law (except net weight, MRP, expiry, consumer care sizes)

---

### 2021–2022 — Unit Sale Price

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 779(E) | 29 Oct 2021 | Introduced mandatory Unit Sale Price (Rule 6(11)), country-of-origin clause (Rule 6(1)(aa)) | 1 Apr 2022 (initial) | **CRITICAL** — USP becomes mandatory |
| G.S.R. 226(E) | 28 Mar 2022 | Revised USP denomination structure, corrected implementation details | 1 Oct 2022 (operative) | **CRITICAL** — Defines current USP rules |

**Current USP Rules (Rule 6(11)) per G.S.R. 226(E):** [PRIMARY RESEARCH FINDING]
- **Weight:** Net Qty < 1 kg → per gram; Net Qty ≥ 1 kg → per kilogram
- **Length:** Net Qty < 1 m → per centimetre; Net Qty ≥ 1 m → per metre
- **Volume:** Net Qty < 1 L → per millilitre; Net Qty ≥ 1 L → per litre
- **Count:** per number or per unit
- **Rounding:** to nearest two decimal places
- **Exemption:** Not required when MRP = USP
- **Exemption:** Not required for combination packages, group packages, multi-piece packages, and wholesale packages [SECONDARY RESEARCH — DCA FAQ]

> **V0.2 ERROR CORRECTED:** V0.2 docs stated "≥ 1 kg → per kg" and introduced "per 100g" as a valid denomination. The statutory text specifies "less than one kilogram → per gram" and "one kilogram or more → per kilogram". There is NO "per 100g" denomination in the statute.

---

### 2023 — Jan Vishwas Act (First)

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| Act No. 18 of 2023 | 11 Aug 2023 | Jan Vishwas (Amendment of Provisions) Act, 2023 — Decriminalized 42 offences across 183 provisions in various Acts | Various dates per section | **CONTEXTUAL** — Laid legislative groundwork for decriminalization approach |

**Note on Jan Vishwas 2023 vs 2026:** [PRIMARY RESEARCH FINDING]
The Jan Vishwas (Amendment of Provisions) Act, 2026, amended provisions across multiple Acts. However, the specific **Improvement Notice mechanism for Legal Metrology** was introduced through the **Jan Vishwas (Amendment of Provisions) Act, 2026**, with Legal Metrology provisions effective from **1 May 2026** (source: PIB PRID 2278745). The V0.2 documentation incorrectly attributed the Improvement Notice mechanism entirely to the 2023 Act.

---

### 2025 — Packaged Commodities Amendments

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 778(E) | 24 Oct 2025 | Medical Devices carved out — packaging governed by Medical Devices Rules, 2017 instead of LM(PC) Rules | Immediate (Oct 2025) | **CRITICAL** — Medical devices EXCLUDED from MetroLens supported categories |
| G.S.R. 881(E) | 2 Dec 2025 | Pan masala packs — all sizes must display full mandatory declarations and MRP; removes small-pack exemption under Rule 26(a) | 1 Feb 2026 | **MVP-RELEVANT** — Pan masala requires special handling if supported |

**Medical Devices (G.S.R. 778(E)):** [PRIMARY RESEARCH FINDING]
- Medical devices are now governed by Medical Devices Rules, 2017 for labelling/declaration requirements
- This is NOT merely "bypassing Rule 9 font height rules" — medical devices are carved out of the entire LM(PC) Rules framework for declarations
- For hackathon MVP: **medical devices should be excluded from supported categories entirely**

**Pan Masala (G.S.R. 881(E)):** [PRIMARY RESEARCH FINDING]
- The notification specifically addresses **pan masala** — do NOT automatically expand scope to "pan masala/gutkha" unless the notification text explicitly covers both
- Effect: removes the ≤10g/10ml exemption for pan masala, requiring full compliance
- For hackathon MVP: awareness only unless pan masala is a supported category

---

### 2026 — Current Year Amendments

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 128(E) | 13 Feb 2026 | E-commerce Rule 6(10A) — mandatory searchable/sortable country-of-origin filters for imported products on e-commerce platforms | 1 Jul 2026 | **FUTURE/POST-MVP** — E-commerce deferred |
| **Jan Vishwas (Amendment of Provisions) Act, 2026** | Enacted 2026 | Improvement Notice mechanism for Legal Metrology Act, including Section 36(1) | **1 May 2026** | **CRITICAL** — Defines current enforcement sequence |
| G.S.R. 418(E) | May 2026 | Importers may affix declarations at bonded warehouses (AEO Tier-2/3); companies must designate responsible Director for compliance | Immediate | **AWARENESS** — Procedural, does not affect image-based inspection |

**Jan Vishwas 2026 — Current Enforcement Flow:** [PRIMARY RESEARCH FINDING]

```
INSPECTION (Section 15)
    ↓
DETECTION of potential non-compliance
    ↓
IS THIS A FIRST OFFENCE under Section 36(1)?
    ├── YES → IMPROVEMENT NOTICE issued
    │         ↓
    │     COMPLIANCE WINDOW (typically 15–30 days)
    │         ↓
    │     RECTIFIED? 
    │         ├── YES → MATTER CLOSED (no penalty)
    │         └── NO  → ADJUDICATION by Adjudicating Officer (Section 48A)
    │                    → Financial penalties apply
    │
    └── NO (repeat offence) → DIRECT ADJUDICATION
         → Escalating penalties (2nd offence: higher; 3rd offence: ₹25L–₹50L for Section 36(1))

IMPORTANT: Section 36(2) (short weight/under-measure) remains separate and stricter.
           Software CANNOT determine net weight — requires physical check-weighing.
```

> **V0.2 ERROR CORRECTED:** V0.2 attributed the Improvement Notice mechanism to "Jan Vishwas (Amendment of Provisions) Act, 2026". The operative Act for Legal Metrology Improvement Notices is the **Jan Vishwas (Amendment of Provisions) Act, 2026**, effective 1 May 2026.

---

### Future-Effective (Not Yet Operative)

| Instrument | Date | Subject | Effective | MetroLens Impact |
|:---|:---|:---|:---|:---|
| G.S.R. 128(E) provisions | Feb 2026 | Additional e-commerce Rule 6(10A) requirements with 2027 effective dates | **2027** | **IGNORE FOR MVP** — Future-effective, do not implement |

> **GOVERNING RULE:** Do not implement a future-effective rule as though it is currently effective. If a notification contains both immediate and future-effective provisions, implement only the currently effective portions.

---

## Rule Number Reference (Current Consolidated State as of September 2026)

This is the authoritative quick reference for rule numbering. Every citation in the MetroLens codebase MUST use these correct references.

| What It Governs | Correct Rule | Common Incorrect Citation | Notes |
|:---|:---|:---|:---|
| Mandatory declarations (name, address, net qty, MRP, dates, consumer care, USP, country of origin) | **Rule 6** | — | Sub-clauses (1)(a) through (1)(h), (1)(aa), (10), (10A), (11) |
| **Font height tables** (Table-I and Table-II) | **Rule 7** | ~~"Rule 7 Table-I/II"~~ | Rule 7(2) references Tables; Rule 7(3) contains Tables |
| PDP area calculation formulas | **Rule 7(4)** | — | Rectangular, cylindrical, other shapes |
| Width ≥ ⅓ height requirement | **Rule 7(3)** | — | Except numeral "1" and letters i, I, l |
| Small package (≤10 cm³) card/tape provision | **Rule 7(1)** | ~~"10 cm²"~~ | 10 **cubic** centimetres, NOT square centimetres |
| Declaration **placement**, clear space, prominence | **Rule 8** | — | Net quantity clear space requirements |
| Declaration **manner**, legibility, contrast, language | **Rule 9** | ~~"Rule 7 Table-I/II"~~ | Rule 9 has NO table — it governs HOW declarations look, not their size |
| Unit Sale Price | **Rule 6(11)** | — | Added by 2021/2022 amendments |
| Net quantity verification (physical) | **Rule 24** | — | Physical check-weighing, NOT image-verifiable |
| Exemptions (small packs, industrial, fast food) | **Rule 26** | — | Scope exclusions (>25 kg, >25 L, industrial) may be Rule 3 or Rule 24, NOT all Rule 26 |
| Application and scope | **Rule 3** | — | Defines who/what the rules apply to |

---

## Evidence Classification Legend

| Tag | Meaning |
|:---|:---|
| [OFFICIAL FACT] | Directly quoted from or verified against official Gazette notification, Act text, or government circular |
| [PRIMARY RESEARCH FINDING] | Found via official government source (DCA, PIB, India Code, e-Gazette) and cross-verified |
| [SECONDARY RESEARCH] | Found via legal databases (Indian Kanoon), law firm articles, or DCA FAQ — needs primary verification |
| [ENGINEERING DECISION] | Technical choice made by the MetroLens team, not derived from statute |
| [PRODUCT ASSUMPTION] | Assumed to be true for product design but not verified against primary source |
| [UNKNOWN / UNVERIFIED] | Status unknown — must be verified before implementation |
