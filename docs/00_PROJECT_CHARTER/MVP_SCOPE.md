# Minimum Viable Product (MVP) Scope Specification

## Purpose
Defines the strictly prioritized subset of capabilities delivered for the live Smart India Hackathon prototype demonstration.

## Scope
Focuses on demonstrating end-to-end defensibility: guided capture $\rightarrow$ image quality check $\rightarrow$ physical calibration $\rightarrow$ OCR & declaration extraction $\rightarrow$ deterministic rule check $\rightarrow$ human review $\rightarrow$ tamper-evident dossier export.

## Authoritative Inputs
- SIH evaluation rubric and 5-minute live judging format.
- Verified primary sources for Legal Metrology (Packaged Commodities) Rules, 2011.

## Assumptions
- The live demonstration will use physical consumer packages with varied packaging geometry (rectangular box and cylindrical container).
- Calibration will utilize a standardized physical reference target.

## Open Questions
- Offline inference latency on standard hackathon demonstration laptop without discrete GPU [TBD — MEASURE].

## Dependencies
- `apps/web/`
- `apps/api/`
- `packages/vision/`
- `packages/rules-engine/`

## Verification Requirements
- MVP inspection pipeline latency targets CPU execution (TARGET — NOT VALIDATED; Status: `TBD — MEASURE` via `benchmarks/protocols/PROTO_LATENCY_EVAL.md`).
- Must produce verifiable PDF inspection dossier with complete cryptographic hashes.

---

## MVP Deliverable Capabilities

| Component | MVP Scope Delivered | Deferred to Post-MVP / Production |
| :--- | :--- | :--- |
| **Capture Interface** | Web-based responsive guided capture with camera feed | Native Android/iOS native camera SDK bindings |
| **Quality Gate** | Laplacian variance blur detection & glare masking | Deep learning artifact segmentation network |
| **Calibration** | Reference object fiducial calibration ($\text{mm/px}$) | Stereoscopic depth camera & structured light sensors |
| **OCR Pipeline** | Multilingual OCR on rectangular and cylindrical packages | Arbitrary deformed pouch 3D mesh unrolling |
| **Field Extraction** | Rule-assisted regex and token parser for 7 mandatory fields | Zero-shot fine-tuned multilingual LLM extractor |
| **Rule Engine** | Rule 6 declarations & Rule 7 font height tables | State-specific local municipal market amendments |
| **Reporting** | Standalone cryptographic PDF & JSON dossier export | National server cloud sync & automated compounding memo |
