# Member 1 Final Limitations & Boundary Specification

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Date**: September 2026  
**Status**: ACTIVE CONTRACTUAL BOUNDARY

---

## 1. Architectural Boundary Invariants

Member 1 (AI & Multilingual OCR Lead) owns optical text detection, script routing, optical character recognition, and canonical observation emission.

Member 1 **DOES NOT** own:
1. **Legal Rule Evaluation & Enforcement**: Owned strictly by Member 2 (Legal Rule Engine / LM Rules 2011). Member 1 does not decide whether a detected "MRP Rs. 150.00" violates Section 18.
2. **Semantic Extraction & Field Classification**: Owned strictly by Member 2 / Extraction Pipeline. Member 1 outputs raw optical tokens, bounding polygons, confidence scores, and script tags.
3. **Physical Optical Calibration & Measurement**: Owned strictly by Member 3 (Computer Vision & Physical Calibration Lead). Member 1 does not compute millimeters per pixel, minimum font height compliance in mm, or area proportions.
4. **Backend API Routing & Persistence**: Owned strictly by Member 4 (Backend / Infrastructure Lead).
5. **Frontend User Interface & Visual Presentation**: Owned strictly by Member 5 (Frontend / UX Lead).
6. **PDF Audit Generation & Digital Signatures**: Owned strictly by Member 4 / Member 6.

---

## 2. Technical & Operational Limitations

### Limitation 1: Dataset Reality (Path B Active)
- **Constraint**: Zero physical retail packaging images currently exist in local storage (`data/` or `AI_CONTEXT/`).
- **Implication**: All benchmark numbers and test verifications are conducted on synthetic, reproducible FMCG packaging specimens (`SYNTH-01` through `SYNTH-08`).
- **Honesty Mandate**: MetroLens makes **no claim** of having verified real-world physical packaging accuracy on store-shelf packaging until physical specimens are collected and evaluated under field conditions.
- **Contract Impact**: Core engine interfaces, bounding polygon mathematics, script routing, and service adapters are 100% verified and production-ready for real data ingestion as soon as images become available.

### Limitation 2: Script & Language Scope
- **Fully Supported**:
  - Latin script (English alphanumeric text, symbols, standard punctuation).
  - Devanagari script (Hindi characters, matras, conjuncts, numbers, and the Indian Rupee symbol `₹`).
- **Unsupported in MVP**:
  - Regional Indic scripts (e.g., Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Odia, Punjabi).
  - Future expansion will require adding language-specific recognition ONNX heads and character dictionaries mapped through the routing pipeline.

### Limitation 3: Physical Package Deformation & Optical Distortion
- **Tolerant To**:
  - Planar packaging labels (boxes, cartons, flat pouches).
  - Moderate illumination variations, contrast shifts, and blur up to baseline thresholds.
- **Challenged By**:
  - Extreme cylindrical wrap distortions (bottles, cans without cylindrical unrolling).
  - Highly crinkled metallic foils with severe specular reflections and specular blinding.
  - Sub-millimeter micro-text (< 6 pixels stroke width at capture resolution).

### Limitation 4: Hardware & Execution Environment
- **Target Platform**: Standard edge/server CPU (`CPUExecutionProvider`).
- **Threading Model**: Multi-threaded intra-op parallelism (configured to 4 CPU threads by default).
- **Latency Expectation**: 35 ms to 80 ms per frame on modern 12-core/8-core CPUs.
- **Resource Limits**: 64 Megapixel ceiling enforced per frame (ADR-014) to protect edge devices from memory exhaustion attacks or decompression bombs.

---

## 3. Maintenance & Extension Guidelines

1. **No Code Rebuilds**: The core OCR engine (`nirikshak_ocr`) is frozen. Any changes must be backwards-compatible extensions.
2. **Model Weight Immutability**: All model weights are cryptographically verified via `models/manifest.yaml`. Modifying model weights without updating the manifest and running full regression tests will fail CI/CD validation.
3. **Immutable Optical Observations**: Downstream consumers must treat `OCRObservation` and `OCRResult` as read-only observational data.
