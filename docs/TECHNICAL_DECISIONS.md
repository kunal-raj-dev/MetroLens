# ARCHITECTURE DECISION RECORDS (ADRs)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)

This document records the architectural, algorithmic, and engineering trade-offs governing the implementation of MetroLens AI for InnoHack 3.0 / Smart India Hackathon 2026.

---

### ADR-001: Selection of Scene Text OCR Engine
- **Status:** APPROVED / MANDATED
- **Context:** The system must accurately extract mandatory declarations (MRP, Net Qty, Dates, Address, USP) from diverse packaging surfaces including glossy foil, metallized pouches, cartons, and plastic bottles in English and Hindi (Devanagari). Latency must be $<1.5\text{s}$ on local CPU/Edge hardware without requiring external internet.
- **Decision:** Use **PaddleOCR v4 Mobile (PP-OCRv4)** deployed via **ONNX Runtime (int8 quantized)** with OpenCV preprocessing (Adaptive CLAHE contrast enhancement).
- **Alternatives Considered:**
  1. *Tesseract 5:* Fast and local, but exhibits high Character Error Rate (CER $>25\%$) on decorative scene text, irregular packaging fonts, and low-contrast backgrounds.
  2. *Google Cloud Vision / AWS Textract:* Exceptional text extraction accuracy, but introduces external cloud latency ($>2.5\text{s}$), creates an active internet dependency fatal to rural inspections or venue Wi-Fi drops, and incurs per-call API costs.
  3. *TrOCR (HuggingFace Transformer):* High accuracy, but model footprint ($>1.2\text{GB}$) and inference latency ($>3.5\text{s}$ on CPU) exceed our edge latency budget.
- **Consequences:**
  - *Pros:* Native multilingual support (English + Devanagari), low memory footprint ($\sim 18\text{MB}$ weights), fast CPU inference ($\sim 400\text{–}650\text{ms}$ per crop), robust scene text detection (DBNet++).
  - *Cons:* Requires preprocessing for dot-matrix inkjet dates and specular glare masks.
  - *Fallback:* Tesseract 5 locally installed as a hot-swappable fallback engine if ONNX runtime initialization fails on host machine.

---

### ADR-002: Metric Calibration Anchor for Physical Font-Height Measurement (Rule 9)
- **Status:** APPROVED / MANDATED
- **Context:** In monocular computer vision, absolute real-world dimensions cannot be recovered from pixel coordinates without a scale reference (scale ambiguity: $u = f \cdot \frac{X}{Z}$). Rule 9 Table 1 mandates minimum numeral heights in millimeters ($1.0\text{mm}, 1.5\text{mm}, 2.5\text{mm}, 4.0\text{mm}, 6.0\text{mm}$). Perspective tilt introduces foreshortening by $\cos(\theta)$.
- **Decision:** Implement **Planar Homography Rectification** using a universally accessible physical metric anchor: a **standard Indian 10-Rupee coin** (official RBI diameter: exactly $27.0\text{mm}$) or a standard **ISO/IEC 7810 ID-1 card / ATM card** ($85.60\text{mm} \times 53.98\text{mm}$).
- **Alternatives Considered:**
  1. *Monocular Depth Estimation (MiDaS / Depth-Anything):* Predicts relative depth maps, but lacks absolute metric scale without lidar and suffers from edge bleeding on thin text.
  2. *ArUco / AprilTag Fiducial Markers:* Mathematically precise ($<0.05\text{mm}$ error), but completely impractical for field inspectors who cannot carry or print synthetic markers in retail shops.
  3. *Smartphone LiDAR / ToF Sensors:* High precision, but restricted to high-end iPhones/iPads ($>₹80,000$), violating the requirement for inclusive accessibility on standard government Android smartphones.
  4. *Uncalibrated Pixel Counting:* Disastrous scientific flaw used by weak hackathon projects; yields false positives whenever distance $Z$ changes.
- **Consequences:**
  - *Pros:* 100% field practicality (10-Rupee coins exist in every Indian pocket); official RBI minting tolerance $\pm 0.05\text{mm}$; eliminates perspective tilt up to $35^\circ$ via $H^{-1}$ inverse warping.
  - *Cons:* User must place coin coplanar with packaging panel.
  - *Fallback:* UI manual calibration mode (tap 2 reference points of known distance or enter physical pack height from ruler).

---

### ADR-003: Deterministic Statutory Compliance Rule Engine vs. LLM Authority
- **Status:** APPROVED / MANDATED
- **Context:** The system must evaluate mandatory declarations against the Legal Metrology (Packaged Commodities) Rules, 2011 (amended up to 2026). 
- **Decision:** Compliance decisions **MUST be evaluated strictly by a deterministic, hardcoded Python Statutory State Machine**. LLMs are strictly forbidden from acting as compliance authorities or determining whether an item violates the law.
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
- **Status:** APPROVED / MANDATED
- **Context:** Retail packaging includes cylindrical containers (soft drink cans, shampoo bottles, jars). Curvature compresses horizontal text as it approaches cylinder silhouettes, potentially distorting OCR and measurement.
- **Decision:** 
  1. Leverage the **Mathematical Cylinder Generator Vertical Height Invariance Proof**:
     $$\begin{aligned}
     \text{Curvature Parameterization: } & \mathbf{P}(\phi, y) = (R\cos\phi, y, R\sin\phi) \\
     \text{Horizontal Projection: } & w_{\text{proj}} \approx R\Delta\phi\cos\phi \quad (\text{Foreshortened by }\cos\phi) \\
     \text{Vertical Projection: } & y_{\text{proj}} = y_{\text{actual}} \quad (\text{ZERO foreshortening along vertical generator line!})
     \end{aligned}$$
     Because statutory font height under Rule 9 is measured strictly along the **vertical axis** (numeral capital height / ascender-descender), curvature along the horizontal cylinder radius introduces zero vertical distortion!
  2. Restrict automated cylinder evaluation in MVP to the central $60^\circ$ angular field ($\cos\phi \ge 0.866$).
  3. Flag severe multi-curved packaging (spherical jars, tapered conical necks) as "Requires Flat Label Crop / Manual Officer Inspection".
- **Consequences:**
  - *Pros:* Provides an unassailable mathematical defense in technical jury Q&A; avoids complex 3D mesh reconstruction that would fail on an 8–9 day timeline.
  - *Cons:* Horizontal text near outer borders requires rotating the bottle to center the declaration.

---

### ADR-005: LLM Role Boundary — Constrained Normalization vs. Legal Decision
- **Status:** APPROVED / MANDATED
- **Context:** OCR text outputs are frequently noisy, fragmented, or present in varied semantic orderings (e.g., "Mktg by:", "Manufactured and Packed at:").
- **Decision:** Utilize an LLM (Gemini 1.5 Flash / local quantized SLM) **strictly as an Entity Normalizer & Key-Value Structuring Parser**, constrained by a strict Pydantic JSON schema.
- **Input to LLM:** Raw OCR text bounding boxes and extracted text lines.
- **Output of LLM:** Structured JSON object matching `CanonicalPackagingDeclarationSchema` (MRP, Net Quantity, Mfg Date, Units, Address).
- **Prohibited LLM Prompts:** Never ask the LLM: *"Did this brand commit an infraction?"* or *"What penalty should be imposed?"*
- **Offline Fallback:** If offline or API unavailable, a deterministic regex-based rule parser parses standard patterns.

---

### ADR-006: Local Edge vs. Cloud Backend & 100% Offline Hackathon Resilience
- **Status:** APPROVED / MANDATED
- **Context:** Hackathon demonstration venues suffer notoriously from network congestion, captive portal dropouts, and cellular dead zones. A cloud-dependent prototype creates existential demonstration failure risk.
- **Decision:** The primary runtime architecture must be **100% Localhost / Offline Capable**.
  - Backend: Python FastAPI running locally on the demonstrator's laptop (localhost:8000).
  - OCR: Local ONNX runtime loading quantized PaddleOCR weights from local disk cache.
  - Rule Engine: Local Python modules.
  - Storage: Local SQLite database for inspection records and audit logs.
  - Frontend: Responsive web application (Vite/React or PWA) served locally over localhost / local Wi-Fi hotspot.
- **Cloud Extension (Optional Secondary Mode):** A cloud deployment on Vercel/Render will exist for judges to test on their own phones, but the live stage demonstration must run 100% offline.

---

### ADR-007: Evidentiary Integrity, Chain of Custody & Tamper Evidence
- **Status:** APPROVED / MANDATED
- **Context:** Under Section 65B of the Indian Evidence Act / Section 63 of Bharatiya Sakshya Adhiniyam, 2023, electronic records submitted in regulatory proceedings require proof of authenticity, integrity, and origin.
- **Decision:** Generate a **Cryptographically Sealed Inspection Report (Form A PDF)** embedding:
  1. Raw uncompressed capture image hash (SHA-256).
  2. Bounding box overlay and calibrated crop image hash (SHA-256).
  3. System metadata (UTC ISO-8601 timestamp, GPS coordinates, device identifier, model version hash, rule-engine commit SHA).
  4. Composite inspection certificate checksum signing the entire record.
- **Explicit Rejection of Blockchain:** Reject blockchain smart contracts or distributed ledger technology. Blockchain is unnecessary buzzword bloat for an 8–9 day build, adds zero legal admissibility in Indian district courts (which accept SHA-256 digital certificate under Section 65B/63), and wastes precious engineering bandwidth.

---

### ADR-008: Interoperability with Government Infrastructure (eMaap Adapter)
- **Status:** APPROVED / MANDATED
- **Context:** The Ministry of Consumer Affairs operates **eMaap** (National Legal Metrology Portal). A common jury objection is: *"Why build a new app instead of using eMaap?"*
- **Decision:** Design MetroLens AI as a **Perception & Field Audit Microservice for eMaap**.
  - Expose standard REST API webhook endpoints: `POST /api/v1/emaap/sync-inspection`.
  - Provide a dedicated UI mock tab: "eMaap Inspector Sync Portal", demonstrating seamless bidirectional synchronization of inspection cases, Improvement Notices, and compounding records into the national eMaap database.
