# Member 1 Complete: All-Team Handoff & Subsystem Guidelines

**To**: All MetroLens AI Team Members (Members 2, 3, 4, 5, 6)  
**From**: Member 1 — AI & Multilingual OCR Lead  
**Date**: September 2026  
**Status**: **MEMBER 1 OFFICIALLY COMPLETED & FROZEN**

---

## 1. Team Announcement

Member 1 (AI & Multilingual OCR) has completed its planned engineering lifecycle (Chunks 1 through 7). The optical character recognition subsystem (`packages/ocr`) and its shared contracts (`packages/shared`) are permanently frozen and certified for production integration.

---

## 2. Quick Reference: How Each Team Member Uses OCR

```text
                               ┌────────────────────────┐
                               │ Packaging Image Source │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │   Member 1: OCRService │
                               │ (Direct ONNX CPU Core) │
                               └───────────┬────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
             ┌─────────────────────┐               ┌─────────────────────┐
             │ Member 2: Rules     │               │ Member 3: Vision    │
             │ Ingests: text,      │               │ Ingests: polygon    │
             │ confidence, script  │               │ coords, pixel bbox  │
             └──────────┬──────────┘               └──────────┬──────────┘
                        │                                     │
                        └──────────────────┬──────────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Member 4: Backend / API│
                               │ Ingests: OCRService    │
                               │ Exposes: /api/v1/ocr   │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Member 5: Frontend UI  │
                               │ Ingests: JSON tokens & │
                               │ polygon coordinates    │
                               └────────────────────────┘
```

- **Member 2 (Rules)**: Use `service.extract_observations(bytes)` to get structured `OCRObservation` tokens. Parse MRP and net quantity against Legal Metrology Rules.
- **Member 3 (Vision)**: Use `obs.polygon` and `obs.bounding_box` to compute physical millimeters from camera calibration scale factors.
- **Member 4 (Backend)**: Wrap `OCRService` in FastAPI lifespan and endpoints.
- **Member 5 (Frontend)**: Render bounding box overlays on SVG/Canvas from emitted token polygons.
- **Member 6 (QA)**: Run `python benchmarks/ocr/final/run_final_benchmark.py` to audit performance.

---

## 3. Golden Rules for Downstream Work

1. **Do NOT modify or rebuild OCR code**: `packages/ocr/` is permanently locked.
2. **Do NOT bypass OCRService**: Always use `OCRService` rather than instantiating raw ONNX sessions.
3. **Do NOT add rule logic to OCR**: Legal Metrology rules belong exclusively to Member 2.
4. **Remember Path B**: If you collect physical store packaging images, place them in `data/retail_samples/` for future team validation.
