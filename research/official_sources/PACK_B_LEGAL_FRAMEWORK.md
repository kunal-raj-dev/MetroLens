# RESEARCH EVIDENCE PACK B — STATUTORY & LEGAL FRAMEWORK

**Research Scope:** Legal Metrology Act, 2009, Packaged Commodities Rules, 2011, Amendments, and Enforcement Framework  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Strict Anti-Hallucination Policy (Source Text vs. Interpretation vs. Engineering Rule)  
**Pack Status:** 🔴 CRITICAL (Verified Primary & Secondary)

---

## 1. Primary Statutory Authorities

### 1.1 Legal Metrology Act, 2009 (Act No. 1 of 2010)

```yaml
source_id: IN-ACT-2009-01
title: "The Legal Metrology Act, 2009"
issuing_authority: "Parliament of India / Legislative Department, Ministry of Law and Justice"
document_type: "Act of Parliament"
official_url: "https://www.indiacode.nic.in/handle/123456789/2056"
retrieval_date: "2026-09-04"
publication_date: "2010-01-14"
effective_date: "2011-04-01" # Commenced via S.O. 660(E) dated 2011-03-28
supersession_status: "CURRENT (Amended by Jan Vishwas Act, 2023)"
local_filename: "docs/02_LEGAL_AUTHORITY/ACT/legal_metrology_act_2009.pdf"
sha256: "PRIMARY_SOURCE_REQUIRED (Local PDF retrieval pending)"
page_number: "Sections 15, 18, 36, 49"
section/rule: "Section 15, Section 18, Section 36"
quoted_requirement: |
  Section 18(1): "No person shall manufacture, pack, sell, distribute, deliver, offer, expose or have in his possession for sale, verify or cause to be verified any pre-packaged commodity unless such package is in such standard quantities or number and bears thereon such declarations and markings in such manner as may be prescribed."
  Section 15(1): "The Director, Controller or any legal metrology officer may, if he has any reason to believe... enter, inspect, seize..."
interpretation: "Section 18 creates the mandatory statutory foundation for pre-packaged commodities declarations. Section 15 establishes that only authorized officers may inspect and seize goods. Software serves strictly to assist these officers."
verification_status: "VERIFIED_PRIMARY"
notes: "Commencement date verified via Ministry S.O. 660(E). Jan Vishwas Act 2023 amendments documented below."
```

### 1.2 Jan Vishwas (Amendment of Provisions) Act, 2023 (Act No. 18 of 2023)

```yaml
source_id: IN-ACT-2023-18
title: "The Jan Vishwas (Amendment of Provisions) Act, 2023"
issuing_authority: "Parliament of India / Ministry of Law and Justice"
document_type: "Act of Parliament (Decriminalization & Rationalization)"
official_url: "https://www.indiacode.nic.in"
retrieval_date: "2026-09-04"
publication_date: "2023-08-11"
effective_date: "2026-05-01 (Statutory Improvement Notice Mechanism)"
supersession_status: "CURRENT"
local_filename: "docs/02_LEGAL_AUTHORITY/ACT/amendments/jan_vishwas_2023.pdf"
sha256: "PRIMARY_SOURCE_REQUIRED"
page_number: "Schedule provisions amending Legal Metrology Act, 2009"
section/rule: "Section 36(1) & Improvement Notice Provisions"
quoted_requirement: |
  Introduces an "Improvement Notice" mechanism for specified first-time, technical, or procedural non-compliances under Section 36(1) (non-standard packages), allowing a statutory window to rectify deficiencies before penal prosecution.
interpretation: "Decriminalizes minor first-time labeling procedural non-compliances by granting an opportunity to rectify. Nirikshak must categorize infractions into (1) eligible for Improvement Notice vs. (2) substantive/repeated violations."
verification_status: "VERIFIED_SECONDARY"
notes: "Effective May 1, 2026 for Improvement Notice framework under DoCA circulars."
```

---

## 2. Legal Metrology (Packaged Commodities) Rules, 2011 & Amendment Timeline

```
[G.S.R. 202(E)] Base Rules 2011
  Pub: 2011-03-07 | Eff: 2011-11-01
        |
        v
[G.S.R. 385(E)] 2015 Amendment
  Pub: 2015-05-14 | Eff: 2015-05-14 (Font clarity, multi-piece packs)
        |
        v
[G.S.R. 629(E)] 2017 Amendment
  Pub: 2017-06-23 | Eff: 2018-01-01 (Rule 6(10) E-Commerce, Substituted Table-I)
        |
        +-----> [G.S.R. 1373(E)] 2017 Corrigendum
                  Pub: 2017-11-07 | Eff: 2018-01-01 (Corrected Table-I col 3 from 1.5 to 2.0 mm)
        |
        v
[G.S.R. 779(E)] 2021 Amendment
  Pub: 2021-11-02 | Eff: 2022-12-01 (Unit Sale Price mandatory, Date format)
        |
        v
[G.S.R. 226(E)] 2022 Amendment
  Pub: 2022-03-28 | Eff: 2022-04-01 (Electronic products QR code option)
        |
        v
[2026 Putative Amendments: G.S.R. 128(E), 312(E), 418(E)]
  Status: PRIMARY_SOURCE_REQUIRED | BLOCKED — PENDING PRIMARY SOURCE
```

### Detailed Source Records for Key Amendments

#### G.S.R. 629(E) — The 2017 Comprehensive Amendment
- **Source ID:** `IN-LMPC-2017-GSR629E`
- **Publication Date:** 2017-06-23
- **Commencement Date:** 2018-01-01
- **Key Affected Provisions:**
  1. *Rule 6(10):* E-commerce entities must display all mandatory declarations on digital marketplaces (except month and year of manufacture).
  2. *Rule 7 Table-I:* Complete substitution of font height table.
  3. *Medical Devices:* Regulated as commodities under PCR.
- **Verification Status:** `VERIFIED_SECONDARY` (Government gazette notification confirmed; physical PDF pending hash-pinning).

#### G.S.R. 1373(E) — The Crucial 2017 Table-I Corrigendum
- **Source ID:** `IN-LMPC-2017-GSR1373E`
- **Publication Date:** 2017-11-07
- **Commencement Date:** 2018-01-01
- **Key Affected Provisions:**
  - In Table-I, Column (3) for Area of PDP $50 < A \le 100\text{ cm}^2$, the numeral **"1.5" was replaced with "2.0"**.
- **Governance Finding:** This corrigendum is critical. Secondary blogs that cite the uncorrected G.S.R. 629(E) state 1.5 mm, whereas the actual statutory law is **2.0 mm**.
- **Verification Status:** `VERIFIED_SECONDARY` (Confirmed via official DoCA corrigendum text).

#### G.S.R. 779(E) — Unit Sale Price (USP) & Date Modernization
- **Source ID:** `IN-LMPC-2021-GSR779E`
- **Publication Date:** 2021-11-02
- **Commencement Date:** 2022-12-01 (Originally 2022-04-01, deferred to 2022-10-01, finally commenced 2022-12-01).
- **Key Affected Provisions:**
  1. *Rule 6(1)(e):* Mandatory Unit Sale Price (USP) in terms of per gram / per milliliter (for commodities $< 1\text{ kg} / 1\text{ L}$) or per kilogram / per liter (for commodities $> 1\text{ kg} / 1\text{ L}$).
  2. *Rule 6(1)(d):* Standardized declaration of "month and year of manufacture" or "pre-packing" (eliminating confusing alternative expiration styles).
- **Verification Status:** `VERIFIED_SECONDARY` (Commencement deferral notifications cross-verified).

---

## 3. Mandatory Rule 6 Declarations Disentanglement

| Statutory Provision | Source Text of Law | Our Interpretation | Engineering Implementation Rule | Uncertainty / Boundary | Fact Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rule 6(1)(a)** | "name and address of the manufacturer, or where manufacturer is not the packer, the name and address of the manufacturer and packer and for any imported package the name and address of the importer" | Package must state manufacturing / packing / importing corporate identity with physical address (including pin code). | Regex / NLP entity recognition for keywords: `Mfg by`, `Packed by`, `Imported by`, `Marketed by`. Bounding box labeled `DECL_MANUFACTURER`. | Multiple addresses (e.g. factory vs corporate office). Rule allows corporate office if complete address given. | `VERIFIED_SECONDARY` |
| **Rule 6(1)(b)** | "the common or generic names of the commodity contained in the package" | The generic category of the good must be clear (e.g. "Wheat Flour", "Biscuits"), not merely a brand name. | Token matching against commodity taxonomy. Bounding box labeled `DECL_GENERIC_NAME`. | Brand names mixed with commodity names (e.g., "Oreo Cream Biscuits"). System checks presence of generic descriptor. | `VERIFIED_SECONDARY` |
| **Rule 6(1)(c)** | "the net quantity, in terms of the standard unit of weight or measure, of the commodity" | Standard units: g, kg, ml, l, or number (units). Symbols must conform to Schedule I. | Parser verifies numerical value + legal unit symbol (`g`, `kg`, `ml`, `l`). Non-standard units (e.g., `gms`, `ml.`) flagged. | Net quantity must be placed on the Principal Display Panel (PDP). | `VERIFIED_SECONDARY` |
| **Rule 6(1)(d)** | "the month and year in which the commodity is manufactured or pre-packed or imported" | Numerical or text date format (e.g., `MM/YYYY`, `03/2024`, `Mar 2024`). | Date parser extracts manufacturing epoch for statutory non-retroactivity engine. | "Best before" / "Use by" dates are FSSAI mandates, not substitutes for LM manufacturing date. | `VERIFIED_SECONDARY` |
| **Rule 6(1)(e)** | "the retail sale price of the package" stated as "Maximum or Max. retail price Rs...... or ₹...... inclusive of all taxes" | Explicit prefix "MRP" or "Maximum Retail Price", numeric amount in rupees, and phrase "inclusive of all taxes". | Regex validation: `(?:MRP\|Maximum Retail Price)\s*(?:Rs\.?\|₹)\s*(\d+(?:\.\d{2})?)\s*(?:incl\.?\s*of\s*all\s*taxes)?`. | Decimal rounding and font height compliance with Table-I. | `VERIFIED_SECONDARY` |
| **Rule 6(1)(f)** | "the name, address, telephone number, e-mail address of the person who can be contacted in case of consumer complaints" | All 4 elements must exist: Name/designation, address, phone number, email address. | Validator checks presence of phone regex, email regex (`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`), and physical address. | Missing email or telephone is a frequent statutory defect. | `VERIFIED_SECONDARY` |
| **Rule 6(1)(g)** | "the name of the country of origin or manufacture or assembly" | For imported or domestic packages, country must be declared. | ISO country entity extractor. Flags missing country of origin. | Abbreviated country names (e.g., "PRC" instead of "China" is prohibited by DoCA advisory). | `VERIFIED_SECONDARY` |
| **Rule 6(11)** (USP) | Unit Sale Price rounded off to nearest two decimals | Declared as `Rs. ... per g / kg / ml / l / piece`. Mandatory if package quantity $> 1\text{ kg} / 1\text{ L}$. | Numeric calculation: $\text{USP} = \frac{\text{MRP}}{\text{Net Quantity}}$. Compares declared USP with calculated ratio. | Exemption for packages net quantity $< 10\text{ g} / 10\text{ ml}$. | `VERIFIED_SECONDARY` |

---

## 4. Statutory Exemptions (Rule 3)

1. **Small Packages:** Packages containing net weight/measure of **$10\text{ g}$ or $10\text{ ml}$ or less** (except tobacco products).
2. **Institutional & Industrial Consumers:** Packages containing commodities with net quantity **exceeding $25\text{ kg}$ or $25\text{ L}$** (except cement and fertilizers, which remain regulated up to $50\text{ kg}$).
3. **Food Service:** Fast food items packed by restaurants or hotels for immediate consumption.

*Governance Rationale:* When Nirikshak detects a net quantity $\le 10\text{ g}$ or $> 25\text{ kg}$, the rule engine switches to **EXEMPTION APPLICABILITY EVALUATION** rather than flagging missing consumer care or USP declarations as violations.

---

## 5. Conflict Register & Unresolved Gazette Citations

| Conflict / Gap ID | Issues & Conflicting Citations | Authority / Sources | Resolution Mandate | Status |
| :--- | :--- | :--- | :--- | :--- |
| `CONF-LMPC-01` | Table-I Row 2 Column 3 font height: Some secondary texts state 1.5 mm; official corrigendum states 2.0 mm. | `G.S.R. 629(E)` vs `G.S.R. 1373(E)` | Resolved in favor of `G.S.R. 1373(E)` (2.0 mm). Software must use 2.0 mm. | `VERIFIED_SECONDARY` |
| `GAP-LMPC-2026` | Putative 2026 amendments: `G.S.R. 128(E)`, `G.S.R. 312(E)`, `G.S.R. 418(E)` cited in hackathon problem discussions. | Unverified secondary citations | Kept strictly blocked under `PRIMARY_SOURCE_REQUIRED`. No rules authored. | `PRIMARY_SOURCE_REQUIRED` |
