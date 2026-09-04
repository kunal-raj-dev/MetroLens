# The Innovation Case for Nirikshak

## Purpose
Articulates the novel technical, scientific, and legal-informatics contributions of Nirikshak for judging panels.

## Scope
Defines the architectural and algorithmic advancements beyond off-the-shelf OCR scanners.

## Authoritative Inputs
- `docs/12_PRIOR_ART/DIFFERENTIATION.md`
- `docs/11_JUDGING/CRITERION_EVIDENCE_MATRIX.md`

## Assumptions
- Judges will challenge whether the project is merely an OCR wrapper around PaddleOCR or Tesseract.

## Dependencies
- `packages/calibration/`
- `packages/rules-engine/`

## Verification Requirements
- Team members must articulate the 4 core pillars of innovation during the 5-minute presentation.

---

## The 4 Pillars of Nirikshak Innovation

1. **Bridging the Physical-Digital Gap (Optical Scale Calibration):**
   Standard commercial computer vision operates in dimensionless pixel space. Nirikshak introduces optical scale calibration using planar reference fiducials, calculating font heights and package surface areas in physical millimetres ($\text{mm}$) with mathematically bounded uncertainty ($\pm \delta\text{ mm}$).

2. **The Regulatory Time-Machine (Multi-Epoch Legal Versioning):**
   Law is not static. Rules change across years (2011 base $\rightarrow$ 2017 e-commerce $\rightarrow$ 2021/2022 Unit Sale Price). Nirikshak solves the temporal audit problem by resolving and applying the exact statutory rules in force on the packaging manufacture date.

3. **Separation of Observation and Adjudication (Zero Hallucination Architecture):**
   AI models perform optical observation (text tokenization, edge localization, polygon segmentation). Compliance adjudication is executed entirely by deterministic, auditable code evaluated against verified declarative schemas.

4. **Multi-Panel Cross-View Correlation:**
   Packaged goods are 3D objects. Nirikshak correlates declarations across front, rear, and side panels to detect cross-panel contradictions (e.g. conflicting net weights or multiple conflicting MRPs).
