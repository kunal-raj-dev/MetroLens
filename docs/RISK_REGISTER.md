# RISK REGISTER & 48-HOUR KILL-SWITCH PROTOCOL
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)

This document details the proactive risk management strategy, comprehensive failure mode mitigations, and the mandatory 48-hour kill switch protocol for MetroLens AI during InnoHack 3.0 / SIH 2026.

---

## 1. Comprehensive Project Risk Register

| Risk ID | Risk Description | Category | Sev (1-5) | Prob (1-5) | Score | Early Warning Indicator | Prevention & Mitigation Strategy | Real-Time Fallback Mechanism |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| **R-01** | Specular glare on glossy/metallized snack wrappers blinds OCR text | Optical | 4 | 4 | **16** | OCR confidence drops below 60% on foil wrappers; whiteout pixels in ROI. | Implement real-time HSV saturation analysis in viewfinder; alert user: "Glare detected — tilt phone 10°". | Adaptive CLAHE local contrast enhancement + dynamic thresholding. |
| **R-02** | Font measurement error exceeds statutory tolerance ($\pm 0.15\text{mm}$) due to angle | Computer Vision | 5 | 3 | **15** | Ellipse fit on reference coin shows eccentricity $>0.60$ (severe tilt $>35^\circ$). | Use Planar Homography matrix ($H^{-1}$) to orthorectify packaging surface; enforce sub-pixel contour refinement. | Flag package as "Borderline Measurement — Requires Physical Caliper Verification". |
| **R-03** | Faded dot-matrix inkjet printing of manufacturing dates cannot be read | OCR | 3 | 4 | **12** | Missing date token in canonical JSON schema; fragmented word boxes. | Apply morphological dilation kernel to bridge dot-matrix gaps prior to OCR text line recognition. | Mark Rule 6(1)(d) as "Illegible / Faded Print — Manual Inspection Required". |
| **R-04** | Outdated legal penalties or obsolete Section 36 citations challenged by jury | Legal / Domain | 5 | 2 | **10** | Team mentions "automatic ₹25,000 fine" during presentation. | Integrate Jan Vishwas Act, 2023 amendments: first offence results in an **Improvement Notice**, not automated penalty. | Ensure generated Form A report specifically quotes Section 36(1) Improvement Notice wording. |
| **R-05** | Curvature of bottles and cans distorts font measurements | Geometry | 4 | 3 | **12** | Horizontal bounding boxes appear compressed on container edges. | Apply cylinder generator vertical invariance principle: measure font height strictly along vertical axis. | Restrict automated measurement to central $60^\circ$ generator strip; prompt manual review for tapered shoulders. |
| **R-06** | Venue Wi-Fi fails or cellular latency spikes during live jury demonstration | Operational | 5 | 4 | **20** | Live API calls hang $>3$ seconds; network timeout errors. | Architecture Mandate: Entire system runs 100% on localhost laptop via ONNX runtime and local SQLite. | Zero internet dependency: run demo completely with airplane mode enabled. |
| **R-07** | Shop price sticker placed over original manufacturer MRP | Retail Reality | 3 | 3 | **9** | Conflicting price numerals detected; rectangular white patch over text. | Anomaly detection for overlapping rectangular labels; flag as specific offence under Section 36(2) (MRP tampering). | Highlight sticker bounding box on inspection report as "Suspected MRP Over-stickering". |
| **R-08** | OCR hallucinates or misidentifies Net Quantity SI units (e.g., reads 'g' as 'q') | OCR | 4 | 2 | **8** | Net quantity parser returns null or unapproved unit string. | Constrain OCR recognition dictionary on quantity crops to statutory units (`g`, `kg`, `ml`, `l`, `m`, `N`). | Fuzzy string matching with Levenshtein distance $\le 1$ against approved SI dictionary. |
| **R-09** | Team spends too much time on unnecessary cloud microservices / blockchain | Scope Creep | 4 | 3 | **12** | Backend engineer builds complex user auth and distributed queues on Day 3. | Strict scope discipline: Do NOT build blockchain, OAuth, or distributed queues. Focus 100% on core vision + rules. | Technical Lead cuts secondary features immediately if core calibration slips behind Day 2. |
| **R-10** | Digital vernier caliper ground truth data collection is delayed | Data | 4 | 2 | **8** | Less than 30 packages measured by end of Day 2. | Dedicate Team Member 5 exclusively to physical package acquisition and caliper measurement in first 36 hours. | Utilize curated subset of 50 packages for initial calibration; expand to 100 on Day 6. |
| **R-11** | Camera hardware fails or phone battery dies right before jury arrives | Hardware | 4 | 2 | **8** | Camera feed freezes; disconnected USB debugging. | Maintain a pre-captured 10-product high-resolution image suite directly accessible via dropdown in the web UI. | "Load Live Sample" button instantly feeds pristine pre-captured imagery to local backend. |
| **R-12** | Judge asks: "Why didn't you just use Gemini / GPT-4V for the whole app?" | Jury Q&A | 4 | 3 | **12** | Judge looks skeptical during architecture slide. | Prepare immediate live rebuttal: demonstrate that LLMs hallucinate legal rules and cannot measure font mm height. | Show side-by-side slide of LLM arithmetic failure vs. deterministic mathematical USP validator. |
| **R-13** | Packaging uses regional language (Devanagari / Tamil) not parsed by English OCR | Multilingual | 3 | 3 | **9** | Extracted text returns garbled non-ASCII characters. | Use PaddleOCR multilingual models supporting Devanagari script; map Hindi phrases to canonical keys. | Fallback to English declarations (Rule 8 mandates either Hindi or English). |
| **R-14** | Package is exempt under Rule 26 ($\le 10\text{g}$) but system flags violation | Legal Logic | 4 | 2 | **8** | False positive violation notice generated on miniature sachet. | Codify Rule 26 exemption switch: If parsed net quantity $\le 10\text{g}$ or $\le 10\text{ml}$, suppress declaration violations. | System outputs: "Verified Compliant — Exempt Commodity under Rule 26". |
| **R-15** | AI-generated code introduces subtle concurrency or data race bugs in backend | Code Quality | 3 | 3 | **9** | Intermittent 500 Internal Server Errors during batch processing. | Enforce strict synchronous processing per inspection session; run automated unit test suite before git commit. | Revert to single-threaded sequential execution pipeline. |

---

## 2. The 48-Hour Kill-Switch Protocol

To prevent catastrophic sunk-cost traps (spending 9 days on a project whose core mathematical premise fails), the team will enforce an **unconditional 48-hour Go / No-Go review gate**.

### The 4 Mandatory Validation Gates:

```
                            THE 48-HOUR GATES
┌─────────────────────────────────────────────────────────────────────────────┐
│ GATE 1: Optical Scale Recovery via Metric Homography                        │
│ • Criterion: OpenCV coin contour detection accurately recovers the 27.0mm   │
│   scale factor on a 25° tilted surface with < 5.0% error (MAE < 0.15mm).    │
│ • Validation Test: Measure a physical 1.50mm printed font target.           │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE 2: Local Scene OCR Accuracy on Physical Retail Packages                │
│ • Criterion: PaddleOCR ONNX extracts MRP, Net Qty, and Date tokens with     │
│   > 90% character accuracy across 10 physical test packages on local CPU.   │
│ • Validation Test: Run offline extraction script on local laptop.           │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE 3: Deterministic Compliance Rule Engine Test Suite                     │
│ • Criterion: Python rule engine achieves 100% passing tests across 25       │
│   synthetic statutory test cases (including USP math and Rule 26 exempts).  │
│ • Validation Test: `pytest tests/test_rule_engine.py` passes completely.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ GATE 4: Ground Truth Physical Dataset Assembly                              │
│ • Criterion: At least 50 physical retail packages assembled and measured    │
│   with digital vernier calipers, recorded into JSON schema.                 │
│ • Validation Test: Verify `ground_truth_benchmark.json` schema integrity.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Action Thresholds at T+48 Hours:

1. **GREEN LIGHT (GO) — All 4 Gates Pass:**
   - *Action:* Proceed full speed with mobile UI integration, PDF notice generator, and full 100-package benchmark.
2. **AMBER LIGHT (CONDITIONAL GO) — Gate 1 or Gate 2 marginally below target:**
   - If Gate 1 error is $5\text{–}8\%$: Restrict MVP font height claims to planar cardboard boxes and add manual reference corner confirmation in UI.
   - If Gate 2 OCR is noisy: Add CLAHE contrast preprocessing and restrict MVP to high-contrast retail packaging.
3. **RED LIGHT (KILL SWITCH / PIVOT) — Gate 1 or Gate 3 Catastrophically Fails:**
   - If optical homography cannot reliably resolve font heights within $\pm 0.3\text{mm}$: **Trigger immediate project pivot to the complementary Problem Statement (SIH26073: Weather Station Anomaly Detection)**.
   - *Why this protects the team:* Because SIH26073 uses pure numerical time-series data with zero optical hardware risk, the team can pivot at T+48 hours with 7 full days remaining, guaranteeing a high-scoring final submission rather than presenting a broken computer vision demo.
