# System Integration Handoff -> Member 1 (OCR Perception)

**Auditor:** System Integration Lead  
**Recipient:** Member 1 Lead Engineer  
**Status:** Subsystem Production-Ready on Local CPU  

---

## 1. Verified Strengths
- Your local RapidOCR ONNX inference engine is rock-solid. All models (`det`, `rec_en`, `rec_hi`) are present, self-contained, and require zero cloud API calls.
- Devanagari Hindi text recognition works reliably in end-to-end tests.
- Execution speed is well within budget: ~1.04s for full OCR perception on a 12.5 Megapixel (3072x4080) image.

## 2. Identified Contract Gaps & Requirements
1. **Low-Confidence Character Normalization:** Ensure character-level confidences below 0.60 are flagged with an explicit `uncertain: true` attribute in the returned token structure so Member 3 and Member 5 can highlight them for manual inspector review.
2. **Text Bounding Box Consistency:** Maintain strict integer coordinates `[x, y, w, h]` normalized relative to original image dimensions, avoiding floating-point or relative 0.0-1.0 coords without documentation.

## 3. High-Priority Action Items
- [x] CPU inference verified with ONNX runtime.
- [ ] Add explicit language tag (`hi` vs `en`) in token metadata to assist downstream phonetic normalizers.
- [ ] Ensure non-ASCII Unicode strings do not get corrupted during JSON serialization.
