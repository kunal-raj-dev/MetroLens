# OPEN QUESTIONS REGISTER (V0.3)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Classification Framework:** Prioritized by Engineering Blocking Dependency  
- **P0 (Critical / Blocker):** Must be answered and experimentally resolved within the First 24 Hours before coding heavy pipelines.  
- **P1 (Integration / Refinement):** Must be resolved before Day 5 system integration and benchmark locking.  
- **P2 (Future / Post-Hackathon):** Documented as intentional architectural extensions; excluded from 8–9 day MVP.

---

## 1. Priority P0: Must Answer Before Heavy Coding (Hours 0 to 24)

### [P0-1] Metric Scale Recovery: Is a 10-Rupee Coin Alone Sufficient, or Is an ISO Card Required?
- **Context:** Previous documents assumed that a 10-Rupee coin provides complete planar homography ($H$) rectification up to $35^\circ$ tilt. Geometrically, an ellipse from an uncalibrated perspective projection leaves an unconstrained rotation around the surface normal without additional coplanar corner points.
- **Investigation Needed:** Day 1 Calibration Spike must test:
  1. *Coin Only:* Ellipse major-axis scale factor $S = 27.0\text{mm} / d_{\text{major}}$ under near-perpendicular capture ($<10^\circ$).
  2. *ISO Card (ATM / ID Card):* $85.60 \times 53.98\text{mm}$ rectangle providing 4 sharp corners for true 8-DOF planar homography.
  3. *Package Boundary + Coin:* Using segmented carton rectangle + coin diameter.
- **Resolution Criteria:** Measure physical scale error across 10 trials at $0^\circ, 15^\circ, 30^\circ$ tilt. If coin error at $>15^\circ$ exceeds $8\%$, mandate ISO Card or constrained capture guidelines in UI.
- **Owner:** Member 2 (Calibration Lead) | **Deadline:** Day 1, 6:00 PM (T+18h).

### [P0-2] Ground-Truth Font Height Methodology: What Is the Scientifically Defensible Standard?
- **Context:** Using handheld digital vernier caliper blades to measure a 1.0mm printed ink character introduces human parallax, blade-angle tipping, and ink-bleed crushing error of $\pm 0.10\text{–}0.15\text{mm}$—as large as the defect we are trying to detect!
- **Investigation Needed:** Establish whether our benchmark ground truth will be established via:
  - (A) High-resolution 1200 DPI flatbed optical scanning ($1\text{ pixel} = 0.021\text{mm}$), or
  - (B) Calibrated USB digital microscope with reticle scale, or
  - (C) Dual-rater digital caliper measurement averaged across 3 independent characters.
- **Resolution Criteria:** Formal protocol approved and tested on 5 sample packages with inter-rater variance $<0.05\text{mm}$.
- **Owner:** Member 5 (Data & Benchmark Lead) | **Deadline:** Day 1, 10:00 PM (T+22h).

### [P0-3] Local Inference Budget: Does PaddleOCR ONNX Meet CPU Latency & Accuracy on Target Hardware?
- **Context:** The system must run 100% offline on consumer laptops. If PaddleOCR ONNX CPU inference takes $>3\text{ seconds}$ or consumes $>2\text{GB}$ RAM, the live demonstration and user experience will fail.
- **Investigation Needed:** Benchmark quantized `ch_PP-OCRv4` ONNX models on the demonstrator's exact laptop across 15 real retail package images.
- **Resolution Criteria:** Total text detection + recognition latency must be $\le 1,200\text{ms}$ on CPU with Character Error Rate $<8\%$ on clear declaration panels.
- **Owner:** Member 1 (AI/CV Lead) | **Deadline:** Day 1, 8:00 PM (T+20h).

### [P0-4] Report Legal Architecture: How to Fully Eliminate "Image-Based Compliance Assessment Report" and False Penalty Wording?
- **Context:** Audit revealed that "Image-Based Compliance Assessment Report" is a statutory misnomer for inspection reports. Jan Vishwas (Amendment of Provisions) Act, 2026 mandates Improvement Notices for first-time Section 36(1) non-compliances.
- **Investigation Needed:** Draft exact schema and wording for the newly designated **"Image-Based Compliance Assessment Report"**.
- **Resolution Criteria:** Report schema includes: Inspection ID, SHA-256 raw image hash, GPS coordinates, detected declarations, calibrated measurements, rule check breakdown, recommended regulatory action (Improvement Notice / Section 15 sample seizure), and statutory disclaimer. Zero claims of automated penalties.
- **Owner:** Member 6 (Product Lead) | **Deadline:** Day 1, 4:00 PM (T+16h).

---

## 2. Priority P1: Must Answer Before Final Integration (Hours 24 to 72)

### [P1-1] What Is the Optimal Statutory Tolerance Buffer for Borderline Font Heights?
- **Context:** Rule 7 Table-I/II mandates minimum numeral heights ($1.0\text{mm}, 1.5\text{mm}, 2.5\text{mm}$, etc.). Optical edge binarization produces slight stroke jitter. If a true $1.50\text{mm}$ numeral measures $1.46\text{mm}$, flagging a definitive violation creates regulatory harassment.
- **Investigation Needed:** Test whether a Measurement Uncertainty Review Band buffer of $0.10\text{mm}$ or $0.15\text{mm}$ minimizes False Positive Rate (FPR) without degrading defect detection sensitivity.
- **Resolution Criteria:** FPR $<5.0\%$ on compliant benchmark packages; all packages within buffer flagged as `MANUAL_REVIEW_REQUIRED`.
- **Owner:** Member 3 (Rule Architect) & Member 5 (Benchmark Lead) | **Deadline:** Day 4, 2:00 PM (T+62h).

### [P1-2] How Should the Demo Stagecraft Handle Multi-Panel Packages Within 3 Minutes?
- **Context:** On many packages, the Net Quantity and MRP appear on the front Principal Display Panel (PDP), but the manufacturer address and consumer care details appear on the back or side panel. Capturing multiple panels takes precious seconds during a 3-minute pitch.
- **Investigation Needed:** Determine whether the live stage demonstration uses:
  - (A) Single-panel hero package (e.g., biscuit pouch where all declarations appear on the back face), or
  - (B) A two-shot multi-panel workflow (Front PDP scan $\rightarrow$ Back declaration scan), or
  - (C) A folded flat packaging carton.
- **Resolution Criteria:** Select 2 physical hero packages (1 compliant, 1 synthetic defect) where all primary declarations are visible in a single high-resolution capture or rapid 2-shot sequence under 30 seconds total.
- **Owner:** Member 6 (Demo Lead) & Member 4 (Frontend Lead) | **Deadline:** Day 3, 6:00 PM (T+54h).

### [P1-3] How to Structure the Mock eMaap Adapter to Ensure 100% Defensibility in Q&A?
- **Context:** The National Legal Metrology portal (eMaap) lacks a published public API. A judge may ask: *"How can you claim eMaap integration when eMaap has no open developer sandbox?"*
- **Investigation Needed:** Define the mock eMaap endpoint: `POST /api/v1/emaap/mock-sync` that ingests our standardized JSON schema and displays a synchronized status badge.
- **Resolution Criteria:** Answer script and UI clearly state: "eMaap-Inspired Architecture / Future Adapter Interface. We ingest our verified inspection payload into a standardized schema ready for direct ingestion when the Ministry exposes its secure gateway."
- **Owner:** Member 6 (Product Lead) | **Deadline:** Day 4, 6:00 PM (T+66h).

### [P1-4] What Is the Exact Boundary for Cylindrical Container Support?
- **Context:** Bottles and cans have curvature that compresses horizontal text. Right circular cylinders preserve vertical dimensions along the generator line, but real retail bottles are often tapered or conical.
- **Investigation Needed:** Test vertical font measurement on 5 standard cylindrical cans (e.g. Red Bull, Coca-Cola) vs 5 tapered shampoo bottles.
- **Resolution Criteria:** Formulate strict rule: System automatically measures font heights on cylindrical containers strictly within the central $40^\circ$ generator zone when held vertically upright. All tapered, conical, or irregular containers display: `MANUAL_REVIEW_REQUIRED — Non-Planar Curvature Detected`.
- **Owner:** Member 2 (Geometry Lead) | **Deadline:** Day 4, 12:00 PM (T+60h).

---

## 3. Priority P2: Documented Future Extensions (Post-Hackathon Roadmap)

### [P2-1] E-Commerce Rule 6(10) Marketplace Scraping
- **Decision:** Deferred to Post-Hackathon. Playwright scraping of Amazon/Blinkit listings introduces Cloudflare anti-bot blocks, DOM churn, and heavy latency that endanger hackathon stability.
- **Future Architecture:** Server-side asynchronous batch worker connecting via enterprise API feeds or authorized merchant developer keys.

### [P2-2] Native Android Camera Laser-Assisted Auto-Focus & LiDAR
- **Decision:** Deferred to Post-Hackathon. Responsive PWA is faster to build, test, and demonstrate across any device without app-store packaging.
- **Future Architecture:** Native Kotlin/Jetpack Compose Android APK leveraging CameraX API, ARCore depth API, and hardware hardware-accelerated NPU inference via TFLite/Qualcomm QNN.

### [P2-3] Full Regulatory Harmonization: CDSCO Medical Devices & FSSAI FOPNL
- **Decision:** Modularized in architecture; detailed legal codification deferred to post-hackathon.
- **Future Architecture:** Pluggable compliance modules for FSSAI Front-of-Pack Nutritional Labeling (Indian Nutrition Rating - INR) and CDSCO Medical Devices Rules, 2017.
