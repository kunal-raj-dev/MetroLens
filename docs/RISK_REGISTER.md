# RISK REGISTER & 48-HOUR KILL-SWITCH PROTOCOL (V0.3)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Document Status:** Proactive Risk Mitigation & Kill-Switch Governance | **Version:** 0.2 (Post-Audit Edition)  
**Date:** 4 September 2026 | **Governing Principle:** Identify Every Point of Failure Early. Maintain Hard Go/No-Go Decision Gates.

---

## 1. Master Comprehensive Risk Register

| Risk ID | Risk Description | Category | Severity (1–5) | Probability (1–5) | Score (1–25) | Early Warning Trigger | Prevention & Mitigation Strategy | Fallback & Pivot Mechanism | Owner | Deadline |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **R-01** | **Venue Network Failure:** Demonstration venue Wi-Fi crashes, cellular is dead, or captive portal blocks outbound requests. | Operational | 5 | 4 | **20** | Network timeout errors; API calls hang $>2.0\text{s}$. | Mandate 100% offline localhost architecture (`127.0.0.1:8000`); cache all ONNX models locally. | Layer 1: Execute entire demo with Wi-Fi toggled OFF in OS. | Member 1 & M4 | Day 1 (T+24h) |
| **R-02** | **Metric Calibration Failure:** Coin contour detection or ellipse fit fails to achieve $<0.20\text{mm}$ measurement accuracy on tilted surfaces. | Computer Vision | 5 | 3 | **15** | Ellipse eccentricity $>0.60$ ($>35^\circ$ tilt); scale error exceeds $8\%$ on test grid. | Day 1 Calibration Spike; implement ISO card ($85.60 \times 53.98\text{mm}$) rectangular corner homography. | Layer 3: UI Manual Reference Scale Override (click 2 points) or constrain demo to flat boxes with viewfinder guide. | Member 2 | Day 2 (T+48h Kill Switch) |
| **R-03** | **Dual-Project Engineering Overload:** 6-member team developing two SIH projects simultaneously falls behind schedule on core pipeline. | Scope & Schedule | 5 | 3 | **15** | Tasks slip $>12\text{ hours}$ behind Day 2 milestones; team fatigued. | Ruthlessly excise Low Value / High Time features (e-commerce scraper, live eMaap, custom ML); enforce 24h spike. | Trigger 48-hour kill-switch: reduce MetroLens scope or pivot full team to secondary problem statement. | Member 3 & M6 | Day 2 (T+48h) |
| **R-04** | **Specular Glare on Glossy Wrappers:** Metallic pouches reflect overhead lighting, washing out mandatory text fields. | Optical | 4 | 3 | **12** | Viewfinder HSV saturation analysis detects $>5\%$ saturated pixels in text ROI. | Real-time HSV glare pre-check in viewfinder; alert user: "Specular glare detected — tilt phone 10°". | Adaptive CLAHE contrast enhancement + dynamic binarization. | Member 1 | Day 3 (T+60h) |
| **R-05** | **Outdated Legal Claims Challenged:** Jury challenges obsolete Section 36 penalty claims or asks about Image-Based Compliance Assessment Report. | Legal & Domain | 5 | 2 | **10** | Presenter mentions "automatic fines" or "Image-Based Compliance Assessment Report". | Fully align documents and report templates with Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice mechanism; remove Image-Based Compliance Assessment Report. | Presenter correctly cites Section 36(1) Improvement Notice and Section 15 supporting screening. | Member 6 | Day 1 (T+16h) |
| **R-06** | **Cylindrical Packaging Curvature:** Curvature on bottles and cans distorts character geometry and font height calculations. | Geometry | 4 | 2 | **8** | Horizontal bounding boxes compressed near container edges. | Apply right-cylinder generator height invariance principle: measure font height strictly along vertical axis within central $40^\circ$. | Flag tapered bottles or conical jars as `MANUAL_REVIEW_REQUIRED — Non-Planar Curvature`. | Member 2 | Day 4 (T+60h) |
| **R-07** | **Dot-Matrix Mfg Date OCR Failure:** Faded inkjet dot-matrix printing on package crimps is unreadable by OCR. | OCR | 3 | 3 | **9** | Extracted canonical schema missing manufacturing date token. | Apply morphological dilation filter to bridge dot gaps prior to text line recognition. | Mark Rule 6(1)(d) as `MANUAL_REVIEW_REQUIRED — Low Confidence / Faded Inkjet`. | Member 1 | Day 3 (T+60h) |
| **R-08** | **AI Hallucination in Legal Verdicts:** Junior team member tries to use LLM to decide whether a package is legal. | AI Governance | 5 | 1 | **5** | Code commit contains LLM prompt asking "Is this package compliant?". | Architectural invariant: Compliance decisions evaluated strictly by deterministic Python state machine. Zero LLM in legal path. | Automated git pre-commit lint check rejecting prompt-based legal evaluators. | Member 3 | Continuous |
| **R-09** | **Physical Dataset Collection Bottleneck:** Inability to source and micro-measure 100 physical packages within 36 hours. | Data & Ops | 4 | 2 | **8** | Less than 20 packages measured by end of Day 2. | Phase dataset: Phase 1 (20 smoke packages), Phase 2 (35–40 benchmark packages); use 1200 DPI flatbed optical scan. | Focus on 35 high-priority SKUs; do not compromise coding time for dataset volume. | Member 5 | Day 2 (T+36h) |
| **R-10** | **Misleading Evidence / Admissibility Claims:** Jury questions claims that SHA-256 makes reports "supporting inspection evidence". | Legal & Evidence| 4 | 2 | **8** | Presenter claims "supporting inspection evidence under Section 65B by fiat". | Train presenter on legal distinction: hash provides tamper-evidence and integrity; Section 63 BSA certificate requires authorized officer. | Presenter answers: "Software provides supporting tamper-evident proof to assist officer's statutory action." | Member 6 | Day 8 Jury Drill |
| **R-11** | **Camera Hardware Failure at Demo:** USB webcam snaps, phone battery dies, or browser camera permission blocked. | Hardware | 4 | 2 | **8** | Video stream freezes or throws `NotAllowedError`. | Layer 2 Failover: UI includes a persistent "Load Live Sample" dropdown with 10 pristine pre-captured benchmark images. | Click sample image $\rightarrow$ feeds raw pixels directly into local backend pipeline instantly. | Member 4 | Day 7 (T+144h)|
| **R-12** | **Accidental Public Defamation:** Presenting modified branded retail packages as illegal violations in a public hackathon. | Ethics & Legal | 4 | 1 | **4** | Real commercial brand shown with fabricated violation label. | Enforce synthetic defect protocol: all defect cases must use custom printed mock sleeves labeled: "Synthetic Test Specimen". | Immediate disclaimer on screen and in presentation slides. | Member 5 & M6 | Day 3 (T+60h) |
| **R-13** | **Multilingual Packaging (Hindi) Misread:** Bilingual FMCG packaging text unparsed by English-only OCR. | Multilingual | 3 | 2 | **6** | OCR returns garbled text on Devanagari declarations. | Integrate PaddleOCR multilingual weights; implement Hindi keyword dictionary (`अधिकतम खुदरा मूल्य` $\rightarrow$ `mrp`). | Fallback to English declarations (Rule 8 mandates either Hindi or English; interstate goods include English). | Member 1 | Day 5 (T+96h) |
| **R-14** | **Unchecked Rule 26 Miniature Exemption:** System blindly suppresses violations on miniature tobacco or pan masala pouches. | Legal Logic | 4 | 1 | **4** | Sachet of pan masala flagged as "Exempt under Rule 26". | Codify category-aware Rule 26 check: verify commodity is NOT tobacco or pan masala (GSR 881(E)) before exempting. | Unit tests in `test_rule_26.py` specifically testing miniature pan masala non-exemption. | Member 3 | Day 2 (T+36h) |
| **R-15** | **AI-Assisted Code Regression:** Copilot/AI coding introduces subtle concurrency or data race bugs in FastAPI backend. | Code Quality | 3 | 2 | **6** | Intermittent 500 server errors during multi-image testing. | Enforce single-worker synchronous execution per session; run automated pytest regression suite before git commit. | Revert to single-threaded sequential inspection pipeline. | Member 3 | Continuous |

---

## 2. The 48-Hour Kill-Switch Protocol (Mandatory Decision Gate)

To prevent the team from falling into a catastrophic sunk-cost trap, the team enforces a **binding Go / No-Go review at T+48 Hours**:

```
                             THE 48-HOUR GATES
┌─────────────────────────────────────────────────────────────────────────────┐
│ GATE A: Statutory Rule Engine Unit Tests (Member 3)                         │
│ • Threshold: 100% passing tests across 25 synthetic statutory test cases    │
│   (including Rule 6(11) USP denominations and Rule 26 pan masala checks).   │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE B: Local Scene OCR Inference (Member 1)                                │
│ • Threshold: PaddleOCR ONNX CPU latency < 1,200ms and Character Error Rate  │
│   < 8% across 15 physical test packages on host laptop without GPU.         │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE C: Optical Metric Scale Calibration (Member 2)                         │
│ • Threshold: Recovered scale error < 5% (MAE < 0.15mm) on planar packages   │
│   under < 15° tilt against millimeter calibration grid.                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE D: Assessment Report Compilation (Member 6)                            │
│ • Threshold: Renders complete Assessment Report PDF with SHA-256 hash in    │
│   < 500ms without layout clipping.                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE E: Localhost End-to-End Execution (Member 4 & M3)                      │
│ • Threshold: Camera capture to dashboard verdict executes in < 3.0 seconds  │
│   on 127.0.0.1 with network interface disabled.                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Kill-Switch Action Outcomes:
1. **FULL GO (Green Light):** All 5 Gates PASS. Full speed ahead with UI polish, Phase 2 benchmark, and presentation rehearsals.
2. **CONDITIONAL GO (Amber Light):** Gate C (Metric Calibration) shows $5\text{–}8\%$ error. Action: Restrict automated font measurement to flat cartons with viewfinder plane guide; add UI manual scale override.
3. **KILL SWITCH / PIVOT (Red Light):** Gate B (OCR) or Gate C (Calibration) catastrophically fails. **Action: Unconditionally pivot full six-member team to the secondary problem statement (SIH26073: Weather Station Anomaly Detection)** at Hour 48, retaining 7 full days to build a winning time-series data prototype.
