# M1 FINAL AUDITED HANDOFF TO MEMBER 3 (STATUTORY RULE ENGINE & EXTRACTION)

**From**: Member 1 (AI & Multilingual OCR Lead)  
**To**: Member 3 (Legal Metrology Rules & Entity Extraction Lead)  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Primary Ingestion Interface: Canonical `OCRObservation`
Member 3 should consume the canonical observation list directly:
```python
from nirikshak_ocr import OCRService

service = OCRService.get_instance()
observations: List[OCRObservation] = service.extract_observations(image_bytes, image_id="insp_001")
```

Each `OCRObservation` conforms to `nirikshak_shared.models.contracts.OCRObservation`:
- `token_id: str`: Unique token identifier (`tok_001`, `tok_002`, ...), sorted in reading order (top-to-bottom, left-to-right).
- `text: str`: Verbatim transcribed string, Unicode NFC normalized.
- `confidence: float`: Raw CTC / decoder confidence score in `[0.0, 1.0]`.
- `bounding_box: BoundingBox`: Enclosing envelope (`x_min`, `y_min`, `x_max`, `y_max`).
- `polygon: List[List[float]]`: 4-point quadrilateral in original pixel space.
- `language: str`: Detected language code (`"en"` for Latin, `"hi"` for Devanagari).

## 2. Inviolable Boundary between M1 and M3
- **M1 Role**: Pure character transcription and spatial localization.
- **M3 Role**: Semantic parsing (e.g. identifying which tokens constitute MRP, Net Quantity, Expiry, or Manufacturer Address) and evaluating Legal Metrology Rules (PCR 2011).
- **RULE**: M1 contains ZERO regexes for statutory fields and ZERO rule verdict logic. M3 must perform all entity extraction and legal compliance checks.

## 3. Numeric & Statutory OCR Caveats for Member 3
1. **Confidence Semantics**: M1 confidence represents neural CTC probability, NOT legal truth. Tokens with confidence < 0.60 trigger diagnostic warnings in `OCRResult.warnings`.
2. **Numeric Confusions**: On low-contrast or dot-matrix text, SVTR can occasionally exhibit character confusions:
   - `0` vs `O`
   - `1` vs `I` or `l`
   - `5` vs `S`
   - `8` vs `B`
   - Missing decimal points in currency / quantity (e.g. `25000` vs `250.00`).
   Member 3's extraction logic should implement fuzzy pattern validation and cross-check parsed numbers against standard statutory syntax.
3. **Currency Symbols**: Devanagari model preserves `₹` and Hindi numerals (`०, १, २, ३, ...`). Latin model preserves `Rs.`, `MRP`, and Arabic digits (`0-9`).
