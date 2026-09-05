# Artificial Intelligence & OCR Systemic Limitations

## Purpose
Explicitly documents the technical boundaries, failure modes, and environmental constraints of the computer vision and OCR models utilized in Nirikshak.

## Documented AI Boundaries
1. **Low-Contrast & Debossed Text:** Highly degraded, translucent, or debossed plastic markings without ink fill suffer from elevated OCR character error rates.
2. **Severe Non-Planar Distortions:** Heavily crushed, crumpled, or torn packaging violates planar homography assumptions and routes to manual officer inspection.
3. **Multi-Lingual Dialects:** Optical character recognition is optimized for English and standard Hindi (Devanagari numerals and script). Rare regional dialect terms or unstandardized transliterations require officer review.
4. **Observation Only:** AI confidence scores are used solely to trigger human review routing. They are never converted into legal certainty.
