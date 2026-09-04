# ARCHITECTURE DECISION RECORDS (ADRs) — V0.3
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Document Status:** Authoritative Architectural Single Source of Truth  
**Review Version:** 0.3 (Final Audit Edition) | **Date:** 4 September 2026

This document records the architectural, algorithmic, and engineering trade-offs governing the implementation of MetroLens AI for InnoHack 3.0 / Smart India Hackathon 2026. All decisions are categorized under strict validation states: **PROPOSED**, **VALIDATED**, **REJECTED**, or **DEFERRED**.

---

### ADR-001: Selection of Scene Text OCR Engine
- **Status:** **PROPOSED** (Inference Benchmark Scheduled Day 1, T+24h)
- **Context:** The system must accurately extract mandatory declarations (MRP, Net Qty, Dates, Address, USP) from diverse packaging surfaces including glossy foil, metallized pouches, cartons, and plastic bottles in English and Hindi (Devanagari). Latency must be $<1.2\text{s}$ on local CPU without requiring external internet.
- **Decision:** Use **PaddleOCR v4 Mobile (PP-OCRv4)** deployed via **ONNX Runtime (int8 quantized)** with OpenCV preprocessing (Adaptive CLAHE contrast enhancement).
- **Alternatives Considered:**
  1. *Tesseract 5:* Fast and local, but exhibits high Character Error Rate (CER $>25\%$) on decorative scene text, irregular packaging fonts, and low-contrast backgrounds.
  2. *Google Cloud Vision / AWS Textract:* Exceptional text extraction accuracy, but introduces external cloud latency ($>2.5\text{s}$), creates an active internet dependency fatal to rural inspections or venue Wi-Fi drops, and incurs per-call API costs.
  3. *TrOCR (HuggingFace Transformer):* High accuracy, but model footprint ($>1.2\text{GB}$) and inference latency ($>3.5\text{s}$ on CPU) exceed our edge latency budget.
- **Consequences:**
  - *Pros:* Native multilingual support (English + Devanagari), low memory footprint ($\sim 18\text{MB}$ weights), fast CPU inference ($\sim 400\text{–}650\text{ms}$ per crop), robust scene text detection (DBNet++).
  - *Cons:* Requires preprocessing for dot-matrix inkjet dates and specular glare masks.
  - *Fallback:* Tesseract 5 locally installed as a hot-swappable fallback engine if ONNX runtime initialization fails on host machine.
- **Validation Required:** First 24-Hour Technical Spike: Benchmark OCR latency and Character Error Rate on 15 real Indian retail packages on dual-core and quad-core CPUs.

---

### ADR-002: Metric Scale Reference Anchor for Physical Font-Height Measurement (Rule 7)
- **Status:** **PROPOSED** (Experiment-First Approach; Feasibility Spike Scheduled Day 1)
- **Context:** In monocular computer vision, absolute real-world dimensions cannot be recovered from pixel coordinates without a scale reference (scale ambiguity: $u = f \cdot \frac{X}{Z}$). Rule 7 Tables I and II mandate minimum numeral heights in millimeters ($1.0\text{mm}, 1.5\text{mm}, 2.0\text{mm}, 2.5\text{mm}, 4.0\text{mm}, 6.0\text{mm}$). Perspective tilt introduces foreshortening by $\cos(\theta)$.
- **Decision:** Implement metric scale calibration using a universally accessible physical anchor: a **standard Indian 10-Rupee coin** (official RBI outer diameter: $27.0\text{mm}$) under constrained near-normal capture ($\le 10^\circ$), with a standard **ISO/IEC 7810 ID-1 card / ATM card** ($85.60\text{mm} \times 53.98\text{mm}$) providing 4-corner planar homography ($H$) rectification as an advanced option.
- **Alternatives Considered:**
  1. *Monocular Depth Estimation (MiDaS / Depth-Anything):* Predicts relative depth maps, but lacks absolute metric scale without lidar and suffers from edge bleeding on thin text.
  2. *ArUco / AprilTag Fiducial Markers:* Mathematically precise ($<0.05\text{mm}$ error), but completely impractical for field inspectors who cannot carry or print synthetic markers in retail shops.
  3. *Smartphone LiDAR / ToF Sensors:* High precision, but restricted to high-end iPhones/iPads ($>₹80,000$), violating the requirement for inclusive accessibility on standard government Android smartphones.
  4. *Uncalibrated Pixel Counting:* Scientifically invalid; varies wildly whenever camera distance $Z$ changes.
- **Consequences:**
  - *Pros:* 100% field practicality (10-Rupee coins exist in every Indian pocket); solves the monocular scale ambiguity without special hardware.
  - *Cons:* A circular coin contour alone does not uniquely constrain surface normal azimuth under large tilt angles; requires coplanar placement and viewfinder plane alignment guides.
  - *Fallback:* UI manual scale override mode (tap 2 reference points of known distance or enter physical carton height from a standard ruler).
- **Validation Required:** Day 1 Calibration Feasibility Experiment measuring scale error across 10 trials at $0^\circ, 15^\circ, 30^\circ$ tilt against a printed millimeter calibration grid.

---

### ADR-003: Deterministic Statutory Compliance Rule Engine vs. LLM Authority
- **Status:** **VALIDATED** (Architectural Pattern Mandated)
- **Context:** The system must evaluate mandatory declarations against the Legal Metrology (Packaged Commodities) Rules, 2011 (amended through 2026).
- **Decision:** Compliance decisions **MUST be evaluated strictly by a deterministic Python Statutory State Machine** organized as versioned rule classes. LLMs are strictly forbidden from acting as compliance authorities or determining whether an item violates the law.
- **Alternatives Considered:**
  1. *Prompting an LLM (e.g., GPT-4V or Gemini) with raw images or OCR text to ask "Is this compliant?":* LLMs hallucinate non-existent statutory clauses, miss subtle arithmetic errors, fail to reproduce decisions across runs, cannot guarantee legal auditability, and generate unexplainable conclusions.
- **Consequences:**
  - *Pros:* 100% mathematical auditability; deterministic regression test suite; versioned rule definitions; exact statutory citations; zero legal hallucination risk.
  - *Cons:* Edge cases and new amendments must be codified in code rules rather than zero-shot prompts.
  - *Division of Responsibility:*
    - **AI Perceives:** OCR detects text and bounding boxes.
    - **Math Validates:** Homography converts pixels to mm; floating-point division verifies USP.
    - **Rules Decide:** Deterministic state machine checks Rule 6, 7, 8, 9, 11 clauses.
    - **Humans Handle Uncertainty:** Low-confidence edge cases flagged for manual officer verification.

---

### ADR-004: Curved Surface Packaging (Bottles/Cans) Handling Strategy
- **Status:** **PROPOSED** (Scoped with Strict Boundary Conditions)
- **Context:** Retail packaging includes cylindrical containers (soft drink cans, shampoo bottles, jars). Curvature compresses horizontal text as it approaches cylinder silhouettes, potentially distorting OCR and measurement.
- **Decision:** 
  1. Primary MVP Focus: Planar and near-planar packaging faces (cartons, flat pouches, box faces).
  2. Cylindrical Containers: Apply the **Right Cylinder Vertical Generator Invariance Principle**:
     - Surface parameterization: $\mathbf{P}(\phi, y) = (R\cos\phi, y, R\sin\phi)$.
     - Along the horizontal circumferential axis, text is foreshortened by $\cos\phi$.
     - Along the vertical generator line parallel to the cylinder axis: $y_{\text{proj}} = y_{\text{actual}}$.
     - Restrict automated measurement strictly to the **central $40^\circ$ generator strip** ($\cos\phi \ge 0.94$) on upright right circular cylinders.
  3. All tapered bottles, conical necks, spherical jars, and crumpled pouches are routed to `MANUAL_REVIEW_REQUIRED`.
- **Alternatives Considered:**
  1. *Full 3D Mesh Reconstruction (Structure-from-Motion):* Far too computationally heavy and fragile for an 8–9 day hackathon timeline.
  2. *Ignoring Curvature Completely:* Produces severe measurement errors and false-positive violations.
- **Consequences:**
  - *Pros:* Mathematically defensible in jury Q&A; avoids complex 3D unwarping algorithms.
  - *Cons:* Requires the user to hold cylindrical cans vertically upright.
- **Validation Required:** Test vertical font measurements on 5 cylindrical cans (e.g. Red Bull, Coca-Cola) to confirm vertical height invariance under controlled capture.

---

### ADR-005: LLM Role Boundary — Constrained Normalization vs. Legal Decision
- **Status:** **VALIDATED** (Architectural Guardrail Enforced)
- **Context:** OCR text outputs are frequently noisy, fragmented, or present in varied semantic orderings (e.g., "Mktg by:", "Manufactured and Packed at:").
- **Decision:** Utilize an LLM (Gemini 1.5 Flash / local quantized SLM) **strictly as an Entity Normalizer & Key-Value Structuring Parser**, constrained by a strict Pydantic JSON schema (`CanonicalPackagingDeclaration`).
- **Input to LLM:** Raw OCR text bounding boxes and extracted text lines.
- **Output of LLM:** Structured JSON object matching schema keys.
- **Prohibited LLM Prompts:** Never ask the LLM: *"Did this brand commit an infraction?"* or *"What penalty should be imposed?"*
- **Offline Fallback:** If offline or API unavailable, a deterministic regex-based rule parser parses standard patterns.

---

### ADR-006: Local Edge Architecture & 100% Offline Hackathon Resilience
- **Status:** **VALIDATED** (Core Strategic Mandate)
- **Context:** Hackathon demonstration venues suffer notoriously from network congestion, captive portal dropouts, and cellular dead zones. A cloud-dependent prototype creates existential demonstration failure risk.
- **Decision:** The primary runtime architecture must be **100% Localhost / Offline Capable**.
  - Backend: Python FastAPI running locally on the demonstrator's laptop (`localhost:8000`).
  - OCR: Local ONNX runtime loading quantized PaddleOCR weights from local disk cache.
  - Rule Engine: Local Python modules.
  - Storage: Local SQLite database for inspection records and audit logs.
  - Frontend: Responsive web application (Vite/React or PWA) served locally over localhost.
- **Cloud Extension (Optional Secondary Mode):** A cloud deployment on Vercel/Render may exist for judges to test on their own phones, but the live stage demonstration must run 100% offline.

---

### ADR-007: Evidentiary Integrity, Chain of Custody & Tamper Evidence
- **Status:** **VALIDATED** (Legally Grounded Realism)
- **Context:** Under Section 63 of Bharatiya Sakshya Adhiniyam, 2023 / Section 65B of Indian Evidence Act, electronic records submitted in regulatory proceedings require proof of authenticity, integrity, and origin.
- **Decision:** Generate an **Image-Based Compliance Assessment Report PDF** embedding:
  1. Raw uncompressed capture image hash (SHA-256).
  2. Bounding box overlay and calibrated crop image hash (SHA-256).
  3. System metadata (UTC ISO-8601 timestamp, GPS coordinates, device identifier, model version hash, rule-engine commit SHA).
  4. Composite inspection certificate checksum signing the entire record.
- **Explicit Rejection of Blockchain:** Reject blockchain smart contracts or distributed ledger technology. Blockchain adds zero legal standing in Indian district courts, wastes engineering bandwidth, and represents hackathon buzzword distraction.
- **Statutory Language Guardrail:** System outputs are described as **tamper-evident supporting inspection packages**, not unilateral judicial decrees.

---

### ADR-008: Interoperability with Government Infrastructure (eMaap Mock Adapter)
- **Status:** **PROPOSED** (Re-framed as Mock Adapter Interface)
- **Context:** The Ministry of Consumer Affairs operates **eMaap** (National Legal Metrology Portal). eMaap does not currently provide a public third-party REST API. Claiming live official integration is misleading.
- **Decision:** Design MetroLens AI as an **eMaap-Ready Field Perception Microservice**.
  - Expose a mock REST API webhook endpoint: `POST /api/v1/emaap/mock-sync`.
  - Provide a dedicated UI tab: "eMaap Inspector Sync Portal", demonstrating standardized JSON export of inspection cases into national compliance schemas.

---

### ADR-009: E-Commerce Listing Web Scraper (Playwright)
- **Status:** **REJECTED** (Post-Hackathon Roadmap)
- **Context:** V0.1 scheduled building an automated scraper for Amazon/Blinkit listings under Rule 6(10).
- **Decision:** **Excise e-commerce scraping from the 8–9 day MVP.** 
- **Rationale:** Anti-bot protections (Cloudflare, CAPTCHAs), dynamic DOM changes, and scraping failures introduce high demonstration risk and consume 15+ engineering hours needed for core vision, rules, and physical benchmarks.
- **Post-Hackathon Vision:** Server-side batch scraper utilizing official merchant feeds and partner APIs.

---

### ADR-010: Inspection Report Redesign & Removal of "Image-Based Compliance Assessment Report"
- **Status:** **VALIDATED** (Legal Correction Implemented)
- **Context:** V0.1 named the generated PDF "Image-Based Compliance Assessment Report", which is a statutory misnomer under the LM(PC) Rules, 2011.
- **Decision:** Rename the document to **"MetroLens AI — Image-Based Compliance Assessment Report"**.
  - Frame the report as an objective evidentiary screening tool under Section 15.
  - Cite Improvement Notices under Section 36(1) as amended by Jan Vishwas (Amendment of Provisions) Act, 2026.
  - Include explicit statutory disclaimer: *"Automated image-based assessment. Final legal determination remains with the authorized officer."*
