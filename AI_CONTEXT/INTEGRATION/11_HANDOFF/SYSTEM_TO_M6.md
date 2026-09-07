# System Integration Handoff -> Member 6 (Data & Ground-Truth Dataset)

**Auditor:** System Integration Lead  
**Recipient:** Member 6 Lead Engineer (Data & Testing Lead)  
**Status:** **CRITICAL BLOCKER ON PROJECT ROADMAP**  

---

## 1. Current State of Datasets
- Present in repository:
  - `data/synthetic/regression/` (SYNTH-01 to SYNTH-08): Clean, synthetic SVG/PNG test fixtures used for automated regression tests.
  - `data/real_world/dairy_milk_bubbly/`: Single FMCG packaging SKU with 6 active JPEG images.

## 2. The Core Blocker Explained
- **Why the System is Classified as "B: Partially Verified":**
  - Member 1 (OCR), Member 3 (Rules), Member 4 (API/PDF), and Member 5 (Web UX) are all 100% functional on both synthetic and real-world inputs.
  - Member 2 (Optical Calibration) is fully implemented algorithmically, BUT fails physical calibration on the real-world Dairy Milk images because **no physical reference object (coin or calibration card) was included in the photographs**.
  - As a result, real-world images execute in **Uncalibrated Mode**, which means Schedule II font height compliance cannot be validated against physical millimeter ground truth.

## 3. Urgent Action Items Required from Member 6
1. **Curate Physical Anchor Dataset:**
   - Capture 20+ real-world packaging specimens across FMCG, cosmetics, and electronics.
   - Every photograph MUST include a standard 27.0mm Indian 1-Rupee coin or ArUco reference marker placed directly on or adjacent to the Principal Display Panel.
2. **Provide Ground-Truth Annotations:**
   - Physical millimeter measurements of package dimensions (height, width, depth).
   - Physical font height measurements (in mm) measured via digital vernier calipers.
   - Ground-truth transcription of all mandatory declarations (MRP, Net Qty, Mfg Date, Packer).
3. **Diverse Lighting & Angles:**
   - Include slight specular glare, packaging wrinkles, and varying lighting conditions to stress-test Member 2's Laplacian blur filter and Hough circle detector.
