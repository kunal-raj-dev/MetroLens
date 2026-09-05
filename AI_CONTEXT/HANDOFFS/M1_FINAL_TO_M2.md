# Inter-Member Final Handoff: Member 1 (OCR) -> Member 2 (Legal Rule Engine)

**From**: Member 1 — AI & Multilingual OCR Lead  
**To**: Member 2 — Legal Metrology Rule Engine & Semantic Extraction Lead  
**Date**: September 2026  
**Status**: **FROZEN & PRODUCTION READY**

---

## 1. Executive Summary & Interface Contract

Member 1 has completed and permanently frozen the multilingual OCR subsystem (`nirikshak_ocr`). Member 2 is supplied with deterministic optical text observations extracted locally on CPU.

### How Member 2 Must Ingest OCR Data:
```python
from nirikshak_ocr import OCRService
from nirikshak_shared.ocr_contract import OCRObservation

service = OCRService()
service.warmup()

# Canonical observation ingestion (Immutable Tuple of OCRObservation)
observations = service.extract_observations(image_bytes)
```

Alternatively, for dictionary-based ingestion:
```python
ocr_dict = service.extract_dict(image_bytes)
# ocr_dict contains: {"status": "SUCCESS", "token_count": N, "tokens": [...]}
```

---

## 2. Token & Script Guarantees for Legal Rules

1. **Multilingual Text & Indian Rupee Symbol**:
   - English declarations: e.g., "MRP", "Rs.", "150.00", "NET QUANTITY:", "500g".
   - Hindi Devanagari declarations: e.g., "मूल्य", "₹150", "शुद्ध मात्रा:", "500 ग्राम".
   - Official Indian Rupee symbol (`₹`, U+20B9) is decoded natively.
2. **Language Script Tag**:
   - Each `OCRObservation` includes `language_script`: `"latin"`, `"devanagari"`, or `"mixed"`.
3. **Bounding Polygons & Bounding Boxes**:
   - `obs.polygon`: 4 clockwise vertices `[(x1, y1), (x2, y2), (x3, y3), (x4, y4)]`.
   - `obs.bounding_box`: `(xmin, ymin, xmax, ymax)` in pixel coordinates.

---

## 3. Strict Boundary Rules for Member 2

1. **Member 2 Owns**:
   - Semantic regex parsing and slot filling (extracting MRP numerical value, net content quantity, unit normalization).
   - Rule verification against Legal Metrology (Packaged Commodities) Rules, 2011 (e.g., Rule 6, Rule 7, Rule 8, First Schedule).
   - Generating violation findings and compliance scores.
2. **Member 2 Must NOT**:
   - Re-execute OCR or alter optical bounding boxes.
   - Modify or rebuild any code in `packages/ocr/` (permanently frozen per `MEMBER_1_DO_NOT_REBUILD.md`).
