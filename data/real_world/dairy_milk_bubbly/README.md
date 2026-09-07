# Real-World Packaging Dataset: Cadbury Dairy Milk Silk Bubbly

**Dataset ID:** `DS-REAL-PILOT-CADBURY-01`  
**Specimen:** Cadbury Dairy Milk Silk Bubbly Flexible Chocolate Foil Wrapper  
**Fiducial Standard:** RBI Standard ₹10 Bimetallic Coin ($27.0\text{ mm}$ physical outer diameter, configured specification)  
**Acquisition Instrument:** Smartphone Camera ($3072 \times 4080$ px, 24-bit BGR)  
**Organization Level:** Curation Phase (Down-selected to 6 core benchmarking images + 4 excluded robustness images)

---

## 1. Important Metrological Scope: NOT Ground Truth

> [!IMPORTANT]
> **Metrological Status:** This dataset contains **real-world test / optical robustness photographs**, NOT physical ground-truth measurements.
> 
> While the ₹10 coin provides a known reference anchor diameter ($27.0\text{ mm}$ outer diameter), physical dimensions of the specimen packaging (e.g. caliper-measured width/height, 1200 DPI flatbed optical comparator scans, or micrometric printed font heights) have **not yet been recorded**.
> 
> Therefore, in accordance with the Nirikshak Metrological Integrity Framework, physical accuracy benchmarks remain:
> $$\mathbf{BENCHMARK\_BLOCKED}$$
> 
> Pipeline-derived pixel scale factors (e.g. $\text{mm/px}$) are strictly **image-derived estimates**, never to be conflated with physical ground truth.

---

## 2. Core Evaluation Dataset (6 Recommended Images)

The following 6 images form the curated core evaluation set, providing controlled variation in distance, orientation, and panel face without redundant near-duplicates:

| Filename | Panel | Pose / Distance | Lighting / Condition | Curation Purpose |
| :--- | :---: | :--- | :--- | :--- |
| `front_near_01.jpg` | Front | Near orthogonal view, close framing | Controlled diffuse ambient | Baseline front-panel fiducial and trade dress test |
| `front_medium_01.jpg` | Front | Medium distance, slight pitch/yaw tilt | Diffuse ambient | Geometric tilt invariance and scale-at-distance |
| `front_far_01.jpg` | Front | Far/wide shot, expanded desk field of view | Diffuse ambient | Low-resolution anchor detection stress test |
| `back_flat_01.jpg` | Back | Horizontal, fairly flat orthogonal view | Controlled diffuse ambient | Back-of-pack statutory declaration readability & calibration |
| `back_diagonal_01.jpg` | Back | Moderate diagonal / oblique angle | Diffuse ambient | Perspective slant and declaration panel tilt handling |
| `back_far_01.jpg` | Back | Far/wide shot, desk and laptop background | Ambient with specular sheen | Wide-angle back panel detection under surface sheen |

---

## 3. Excluded Robustness Subset (`excluded/`)

The following 4 captures were removed from the primary benchmark set to eliminate near-duplicates and uncontrolled confounding variables, but are retained in `excluded/` for specialized defensive audits:

| Filename | Original Pose | Reason for Exclusion from Core Set | Audit Utility |
| :--- | :--- | :--- | :--- |
| `front_near_02.jpg` | Front, close-up with left tilt | Near-duplicate of `front_near_01.jpg` without significant geometric variation | Duplicate candidate stability & ranking tests |
| `back_diagonal_02.jpg` | Back, steep perspective angle | Redundant diagonal shot with extreme foreshortening | Steep perspective edge-case testing |
| `back_close_01.jpg` | Back, close macro framing | Edge defocus ($\sigma^2 = 94.06$) and slight framing occlusion | Quality-gate defocus rejection verification |
| `back_adverse_shadow_01.jpg` | Back, heavy cast shadow | Severe underexposure and motion blur ($\sigma^2 = 17.69$) | Severe adverse illumination rejection verification |

---

## 4. Upstream Interface & Downstream Integration

- **Member 1 (OCR):** Upstream token coordinates and bounding boxes are required before font height measurement can be physically evaluated.
- **Member 2 (Calibration & CV):** Anchor detection (`detect_anchor()`) and scale computation (`compute_scale_factor()`) run automatically on these images.
- **Member 3 (Legal Metrology):** If calibration fails or ambiguity is flagged (`AMBIGUOUS_ANCHOR`), measurements route safely to `MANUAL_REVIEW_REQUIRED` without fabricating millimeter figures.
