# System Integration Handoff -> Member 2 (Computer Vision & Optical Calibration)

**Auditor:** System Integration Lead  
**Recipient:** Member 2 Lead Engineer  
**Status:** Algorithmic Pipeline Complete; Field Calibration Blocked on M6 Real Data  

---

## 1. Verified Strengths
- Mathematical scale recovery algorithms (Laplacian blur score, Hough circle coin detection, ArUco card tracking) are well-crafted and pass all synthetic regression suites.
- Graceful degradation works cleanly: when no reference anchor is found, the system smoothly returns `is_calibrated: false` and enables uncalibrated processing without crashing the pipeline.

## 2. Identified Contract Gaps & Blockers
1. **Contract Field Drift:**
   - Your package exports `scale_factor` (mm/px) and `pdp_area_sq_cm`.
   - Member 3 expects `scale_factor_mm_per_px` and `pdp_area_sqcm`.
   - Member 4 expects `scale_mm_per_px` and `pdp_area_cm2`.
   - **Action:** Standardize on `scale_mm_per_px` and `pdp_area_sqcm` across all models or implement an explicit DTO adapter.
2. **Real-World Calibration Anchor Failure:**
   - Tested against real Dairy Milk Bubbly specimens: coin detection failed because no coin was placed in the frame.
   - **Critical Dependency:** You cannot certify real-world physical calibration without Member 6 providing packaging photos that include a physical reference target (e.g. 27.0mm Indian 1-Rupee coin or standard calibration card).

## 3. High-Priority Action Items
- [ ] Align naming of calibration fields with Member 3 and Member 4.
- [ ] Implement Hough circle parameter auto-tuning for varying lighting conditions.
- [ ] Await Member 6 calibration test dataset.
