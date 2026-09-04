# ADR-006: Pre-Inference Image Quality Gate (Blur & Glare Detection)

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Computer Vision Lead, AI / OCR Lead

---

## Context & Problem Statement
Field inspections conducted with hand-held cameras often suffer from motion blur, defocus blur, or extreme specular reflection (glare) from glossy plastic films, laminates, and metallic pouches. Passing severely degraded images into downstream OCR and segmentation stages causes catastrophic OCR token hallucination, false missing declaration alarms, and wasted computational resources.

We must decide whether to process all images unconditionally through the heavy pipeline or enforce a fast pre-inference quality gate.

---

## Decision Drivers
- **Prevention of False Violations**: A blurry label where "Net Quantity" cannot be read must not trigger a false charge of "Missing Mandatory Net Quantity".
- **Compute Efficiency**: Heavy multilingual OCR and deep segmentation models should not execute on unusable inputs.
- **Immediate Field Feedback**: The inspector should receive real-time guidance (e.g. "Image too blurry: retake photo") within milliseconds.

---

## Considered Options
1. **Option 1: Fast Pre-Inference Image Quality Gate** (Chosen)
   - Evaluate Laplacian variance for sharpness and luminance histograms for specular glare. Terminate immediately with `REQUEST_RETAKE` if thresholds fail.
2. **Option 2: Blind End-to-End Execution**
   - Run OCR and rules regardless of input quality; rely on downstream confidence scores.
3. **Option 3: Generative Image Enhancement / Super-Resolution**
   - Attempt to deblur or hallucinate missing pixels using generative diffusion models before inspection.

---

## Decision Outcome
**Chosen Option:** Option 1: Fast Pre-Inference Image Quality Gate.
Raw frames must pass Laplacian variance and glare histogram thresholds before entering optical calibration and OCR. Generative image enhancement is explicitly rejected because modifying raw pixel evidence breaches chain-of-custody requirements.

### Positive Consequences
- Stops garbage-in / garbage-out processing at the earliest stage (< 15 ms).
- Protects merchants from false citations caused by camera handling mistakes.
- Preserves unaltered evidentiary fidelity.

### Negative Consequences / Trade-offs
- Requires fine-tuning blur/glare thresholds against diverse physical packaging materials (matte cardboard vs metallic polybags).

---

## References & Statutory Linkages
- Data Flow Specification (`docs/04_ARCHITECTURE/DATA_FLOW.md`).
- Anti-Hallucination Architectural Mandate (`docs/04_ARCHITECTURE/`).
