# Inter-Member Handoff: Member 1 (OCR) to Member 3 (Rule Engine) — Chunk 4
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M3_CHUNK4.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 3 (Legal Metrology Rule Engine & Statutory Logic Lead)  
**Date:** 2026-09-05T05:35:00+05:30  
**Phase:** Chunk 4 Delivery  
**Status:** READY FOR STATUTORY PARSING & RULE EVALUATION  

---

## 1. Handoff Summary
Member 1 delivers the canonical `List[OCRObservation]` output stream from `nirikshak_ocr.OCRService`. Member 3 consumes this stream to parse mandatory statutory declarations (MRP, Net Qty, Date, Manufacturer, Consumer Care) under the Legal Metrology (Packaged Commodities) Rules, 2011.

---

## 2. Statutory Parsing Contract

### 2.1 Input Data Structure
Member 3 receives a list of `OCRObservation` objects:
```python
@dataclass
class OCRObservation:
    text: str
    confidence: float
    bounding_box: List[List[float]]  # 4-point polygon in original image pixels
```

### 2.2 Preserved Text & Scripts
- **English Text:** Preserved in standard ASCII/UTF-8.
- **Hindi Text:** Preserved in Devanagari script (`अधिकतम खुदरा मूल्य`, `शुद्ध मात्रा`, `पैकिंग तिथि`, `उपभोक्ता सेवा`).
- **Currency Symbols:** Both `₹` (`\u20b9`) and `"Rs."`/`"INR"` appear in raw tokens. Regex parsers should support both prefixes.

---

## 3. Downstream Normalization Guidance for Member 3

As empirically documented in Chunk 3 and verified in Chunk 4, raw OCR tokens exhibit visual CTC character confusions on packaging fonts:
1. **Numeric Confusions:**
   - Visual `0` may be decoded as letter `O`.
   - Visual `1` may be decoded as letter `I` or lowercase `l`.
   - Visual `5` may occasionally be decoded as letter `S`.
   - *Recommendation:* In price, quantity, and date parsing regexes, apply contextual character substitution (e.g. `re.sub(r'(?<=\d)[OI](?=\d)', '0', text)`).
2. **Fractional & Unit Delimiters:**
   - Commas, periods, or spaces in decimal values (e.g. `₹ 245.00` vs `₹ 245 , 00`).
3. **Domain Separation:**
   - Member 1 guarantees text presence and spatial location.
   - Member 3 performs entity extraction, statutory rule validation (Rules 6, 8, 9, 11, 26), and Jan Vishwas Act penalty tier assignment.
