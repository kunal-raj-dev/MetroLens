# INTER-MEMBER HANDOFF SPECIFICATION: M1 ──► M3
### Optical Character Recognition (M1) to Legal Metrology Rule Engine (M3)
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M3_CHUNK2.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 3 (Legal Metrology Rule Engine & Statutory Logic Lead)  
**Status:** FROZEN CONTRACT (Chunk 2 Complete)  
**Timestamp:** 2026-09-05T04:33:00+05:30  

---

## 1. Executive Contract Summary
Member 1 provides **raw text observations** without semantic interpretation. Member 3 is strictly responsible for parsing, normalization, statutory keyword matching, and legal rule compliance verdicts.

```text
┌────────────────────────────────────────────────────────┐
│ MEMBER 1 (OCR PERCEPTION)                              │
│ • Transcribes character glyphs from image crops        │
│ • Emits raw tokens in deterministic reading order      │
│ • Assigns token confidence scores                      │
└───────────────────────────┬────────────────────────────┘
                            │ Handed off via List[OCRToken] / List[OCRObservation]
                            ▼
┌────────────────────────────────────────────────────────┐
│ MEMBER 3 (STATUTORY RULE ENGINE & SEMANTICS)           │
│ • Regex & semantic extraction of mandatory fields:     │
│   - Maximum Retail Price (MRP)                         │
│   - Net Quantity (Q) & Volume                          │
│   - Unit Sale Price (USP) under Rule 6(11)             │
│   - Manufacturing / Packing / Import Date              │
│   - Consumer Care Details & Country of Origin          │
│ • Statutory Rule Evaluation:                           │
│   - Rule 6 Declarations Check                          │
│   - Rule 7 Table-I Font Height Compliance              │
│   - Rule 3 & 26 Statutory Exemptions                  │
│   - Jan Vishwas Act 2026 Administrative Notice Verdict │
└────────────────────────────────────────────────────────┘
```

---

## 2. What Member 1 PROVIDES to Member 3

1. **Deterministic Reading-Order Text Tokens:**
   - Sequential list of `OCRToken` items sorted top-to-bottom, left-to-right.
   - Grouped by `line_id` for multiline declaration extraction (e.g. multi-line consumer care addresses).
2. **Raw Character Strings:**
   - Literal text as perceived by the neural models (e.g. `"Net Qty: 65 g"`, `"MRP Rs. 20 (incl. of all taxes)"`, `"अधिकतम खुदरा मूल्यः ₹24.0"`).
3. **Recognition Confidence:**
   - Float `confidence` $\in [0.0, 1.0]$. Member 3 can flag tokens with $c < 0.60$ for manual officer confirmation.
4. **Script Provenance:**
   - Script category (`'latin'`, `'devanagari'`, or `'unknown'`) to route tokens through English or Hindi keyword dictionaries.
5. **Canonical Adapter:**
   - `result.to_observations()` returns `List[nirikshak_shared.models.contracts.OCRObservation]` for direct ingestion into `packages/rules-engine/`.

---

## 3. What Member 1 DOES NOT Provide ("Not Member 1's Job")

Member 1 explicitly **does NOT contain semantic parsing or legal logic**:
- ❌ **NO MRP Parsing:** Member 1 does not extract currency symbols (`₹`, `Rs.`), tax inclusion phrases, or float price values.
- ❌ **NO Net Quantity Parsing:** Member 1 does not validate statutory units (`g`, `kg`, `ml`, `L`) or check prohibited symbols (`gms`, `grm`).
- ❌ **NO Unit Sale Price (USP) Calculation:** Member 1 does not calculate $\frac{\text{MRP}}{\text{Quantity}}$ or verify Rule 6(11) rounded unit rates.
- ❌ **NO Date Validation:** Member 1 does not parse month/year or compute shelf-life best-before intervals.
- ❌ **NO Legal Verdicts:** Member 1 never outputs `COMPLIANT`, `NON_COMPLIANT`, or `VIOLATION_DETECTED`.

---

## 4. Usage Example for Member 3

```python
from nirikshak_ocr import OCREngine

engine = OCREngine()
result = engine.extract(image_bgr)

# Option A: Ingest full text buffer for holistic regex search
raw_text_dossier = result.full_text

# Option B: Iterate tokens to correlate text with spatial position
for token in result.tokens:
    if "mrp" in token.text.lower() or "अधिकतम" in token.text:
        # Member 3 executes statutory price extraction:
        # parsed_mrp = parse_mrp_declaration(token.text)
        pass

# Option C: Use shared OCRObservation adapter
shared_observations = result.to_observations()
```
