# CURRENT STATE: PROJECT SNAPSHOT
**Project:** MetroLens AI (SIH26034)
**Snapshot Date:** 2026-09-05T17:00:00+05:30
**Active Workstreams:** Member 1 (OCR) & Member 2 (Computer Vision & Optical Calibration)
**Governing Architecture:** Online Web Application MVP (ADR-011 through ADR-015)

---

## 1. High-Level Status Across Workstreams

- **Legal Source Base:** 74 authentic government legal documents cataloged and verified under `METROLENS_LEGAL_SOURCE_PACK/`.
- **Legal Rule Matrix:** PCR 2011 (Rules 6, 6(11), 7, 8, 26) and Jan Vishwas Act 2026 Section 36(1) codified in documentation.
- **System Architecture:** Decoupled Web Delivery (React + FastAPI) from Deterministic Processing Engine (Local CPU execution, zero cloud AI APIs).
- **Monorepo Test Suite:** **119 passed in 3.89s** with zero regressions.

### Workstream Status Summary:
1. **Member 1 (OCR Lead):**
   - Completed **Chunk 1: OCR Model Feasibility Spike**.
   - Selected `PP-OCRv3-ROUTED` (DBNet++ shared det + script-routed SVTR-EN / SVTR-HI ONNX), median warm latency ~710ms, memory footprint ~157MB.
2. **Member 2 (Computer Vision & Optical Calibration Lead):**
   - **Phase 0 (Repo Audit & Boundaries):** Clean package seams and dependency isolation.
   - **Phase 1 (Interface Seams & Foundation):** Minimal typed contracts established across packages.
   - **Phase 2 (Pre-Flight Image Quality Gate):** Delivered `packages/vision/src/nirikshak_vision/quality.py` (Laplacian blur $<100$, HSV glare $>15\%$, contrast $\sigma < 20$, $<25\text{ms}$ CPU).
   - **Phase 3 (Calibration Spike Benchmark):** Delivered `scripts/benchmark/spike_calibration.py` across 288 controlled factorial scenes; empirically evaluated ellipse major vs minor axis, partitioned errors ($3.03\%$ nominal, $7.98\%$ overall $0^\circ\text{--}15^\circ$), and characterized minor-axis foreshortening physics ($1/\cos\theta - 1$).
   - **Phase 4 (Metric Anchor Detection):** Delivered `packages/calibration/src/nirikshak_calibration/anchor_detector.py` for RBI ₹10 coin and ISO ID-1 card (normalized algebraic ellipse residuals, canonical major-axis orientation normalization, concentric ring pairing, spatial NMS deduplication, ambiguity resolution, 32 unit tests passing).
3. **Members 3, 4, 5, 6:** Upstream foundation and contracts ready for integration.

---

## 2. Immediate Active Objectives

- **Member 2 Next Phase:** Proceed to **Phase 5 — Planar Homography & Perspective Rectification** (`packages/calibration/homography.py`).
  - Consume Phase 4 metric anchor geometries.
  - Compute $3 \times 3$ homography transformation matrix $H$.
  - Generate top-down orthorectified declaration panel crops for Member 1 OCR ingestion.
