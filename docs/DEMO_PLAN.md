# MetroLens AI™ / Nirikshak AI — Master Live Demonstration & Failover Runbook
**SIH 2026 Problem Statement 26034**
**Automated Legal Metrology Compliance Verification System for Packaged Commodities**
**Role:** Member 6 — Product Integration, Quality Assurance, Benchmark Verification & Release Governance
**Release Gate Version:** `v1.0.0-rc1` (SIH 2026 Prototype Freeze)
**Authoritative SHA:** `a06872f`

---

## 1. Demo Objective

Demonstrate to the SIH 2026 Grand Jury a robust, 100% offline-capable, court-admissible Legal Metrology automated inspection workstation that:
1. Audits retail packaging images in under **2.5 seconds** completely on CPU.
2. Performs scene text detection and multilingual recognition (English + Devanagari Hindi) using **local ONNX models**.
3. Reconciles observations against statutory requirements of the **Legal Metrology (Packaged Commodities) Rules, 2011**:
   - **Rule 6(1)**: Mandatory declarations (MRP, Net Quantity, Date, Address, Consumer Care).
   - **Rule 6(11)**: Unit Sale Price (USP) arithmetic validation.
   - **Rule 7 Table-I/II**: Minimum numeral font height versus Principal Display Panel area.
   - **Rule 26 / Rule 3**: Statutory volume/weight exemptions.
   - **Jan Vishwas Act, 2026**: Section 36(1) substituted civil penalty structure and Improvement Notice generation (15-day demonstration default).
4. Provides an **evidence-first, anti-hallucination interactive canvas** allowing inspectors to audit OCR bounding polygons and manual caliper overrides.
5. Generates a **tamper-evident, court-admissible PDF dossier** with cryptographic SHA-256 hashes.

---

## 2. Hardware Setup

- **Demonstration Host Laptop:** Standard x86_64 or ARM64 workstation (Windows 11 / macOS / Ubuntu Linux).
- **CPU:** 4+ cores, AVX2 support (tested on 16 vCPUs).
- **RAM:** Minimum 8 GB (16 GB recommended; pipeline RSS memory peak: ~254 MB).
- **Physical Props for In-Person Evaluation:**
  1. Authentic **RBI ₹10 Bi-Metallic Coin** (nominal 27.00 mm outer diameter) as primary optical fiducial anchor.
  2. Standard **ISO/IEC 7810 ID-1 Card** (85.60 mm × 53.98 mm) as secondary rectangular anchor.
  3. Pre-packaged retail FMCG test samples (e.g., biscuits, chocolate pouches, confectionery).
  4. Digital vernier caliper (0.01 mm resolution) for physical demonstration of manual reference checking.

---

## 3. Software Startup (Localhost Runbook)

### Step 1: Clone and Set Python Environment
```bash
cd MetroLens
# Activate virtual environment
source .venv/bin/activate  # Or on Windows: .venv\Scripts\Activate.ps1
```

### Step 2: Launch Backend API Gateway
```bash
# Terminal 1: Launch FastAPI Conductor
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```
*Health verification:* Open `http://127.0.0.1:8000/health` in browser -> should return `{"status": "healthy"}`.

### Step 3: Launch Next.js Web Frontend
```bash
# Terminal 2: Launch Next.js Production Server
cd apps/web
npm run build
npm start
```
*UI verification:* Open `http://localhost:3000` in browser.

---

## 4. Exact Live Demonstration Sequence

| Step | Action | UI Component | Statutory Meaning / Expected Output | Time Budget |
|:---:|---|---|---|:---:|
| **1** | Open workstation at `http://localhost:3000` | Header & Status Bar | System shows `"CONNECTED"` to localhost FastAPI node. Telemetry reads local host. | 5 s |
| **2** | Upload package photo with ₹10 coin | `ImageUploadZone.tsx` | Drag-and-drop or file selector. Magic-byte sniffing confirms genuine image. | 3 s |
| **3** | Inspection Conductor executes | Loading Spinner | 7-stage pipeline completes on local CPU in **< 150 ms**. | < 2.5 s |
| **4** | Review Overall Verdict | `StatusIndicator.tsx` | 5-State statutory badge: `COMPLIANT`, `POTENTIAL_NON_COMPLIANCE`, or `MANUAL_REVIEW_REQUIRED`. | 10 s |
| **5** | Inspect Mandatory Declarations | `DeclarationTable.tsx` | Rule 6 items populated with verbatim OCR tokens, SI units, and USP arithmetic match. | 20 s |
| **6** | Audit Spatial Evidence Canvas | `EvidenceCanvas.tsx` | Clockwise 4-point quadrilateral polygons highlighted over raw text lines. Pan & zoom. | 25 s |
| **7** | Demonstrate Rule 7 Font Metrology | PDP & Font Tile | If calibrated, displays physical font height in mm ($h_{px} \times S_{mm/px}$) vs Table-I/II threshold. | 20 s |
| **8** | Generate Court-Admissible Dossier | Button `"Generate PDF Report"` | Downloads signed PDF dossier within 30 ms containing ELA crops, Merkle hash, and draft S.36(1) notice. | 10 s |

---

## 5. Five-Layer Demo Failover Architecture

Under live hackathon conditions (flaky Wi-Fi, projector disconnects, unexpected edge-case images), the presenter must seamlessly transition through the 5 failover layers:

```
[LAYER 1: Primary Live Inspection (Localhost, Network-Disabled)]
   │ (If camera image has severe blur/glare or missing anchor)
   ▼
[LAYER 2: Preloaded Synthetic Regression Specimens (SYNTH-01 to SYNTH-08)]
   │ (If judge wants to evaluate uncalibrated packaging without anchor)
   ▼
[LAYER 3: Interactive 2-Point Manual Caliper Fallback]
   │ (If local backend server is stopped/crashed)
   ▼
[LAYER 4: Canned Static Workstation Mode (Mock Adapter)]
   │ (If laptop hardware/projector completely fails)
   ▼
[LAYER 5: Pre-Recorded 4K Backup Demonstration Video & Dossier]
```

### Layer 1: Live Localhost System (Offline Rehearsed)
- Primary demo mode.
- System operates completely with OS Wi-Fi and Ethernet adapters **DISCONNECTED**.
- All ONNX models execute from `models/weights/ocr/`.

### Layer 2: Preloaded Sample Package Fixtures
- Accessible via the horizontal carousel in `SamplePackageSelector.tsx`.
- **8 Curated Specimens:**
  - `SYNTH-01`: Standard English FMCG (Compliant baseline).
  - `SYNTH-02`: Pure Devanagari Hindi Atta Bag (Multilingual script demonstration).
  - `SYNTH-03`: Bilingual English + Hindi Snack Carton.
  - `SYNTH-04`: Shrinkflation Micro-Font Deficit (Rule 7 non-compliance flag).
  - `SYNTH-05`: Personal Care Liquid Volume (ml / USP ₹/ml).
  - `SYNTH-06`: Prohibited Units Deficit ("Gms" non-metric flag).
  - `SYNTH-07`: Blank Frame (Quality gate optical defocus rejection).
  - `SYNTH-08`: Low-Contrast Foil (Adverse lighting / suspect review flag).
- **Honesty Invariant:** Displays prominent badge: `"SYNTHETIC DEMO FIXTURE — NOT REAL RETAIL PACKAGING"`.

### Layer 3: Manual Two-Point Caliper Fallback
- If an inspecting officer captures packaging without a ₹10 coin anchor:
  1. Calibration badge displays amber: `"UNCALIBRATED"`.
  2. Click `"Activate Caliper"` in `EvidenceCanvas.tsx`.
  3. Click Point A (e.g., package left border) and Point B (package right border).
  4. Input known package dimension (e.g., `120.0 mm`).
  5. System computes scale $S = \frac{\Delta_{mm}}{\sqrt{\Delta x^2 + \Delta y^2}}$ and sets provenance to `MANUAL_CALIPER`.
  6. Numeral font heights immediately update to calibrated mm!
- **Validation Guardrails:** Rejects $\le 0\text{ mm}$, rejects identical points (< 2 px), rejects out-of-bounds coordinates.

### Layer 4: Static Canned Dashboard (Mock Adapter)
- If the Python API process is completely terminated:
  1. Toggle `"Mock Server Mode"` switch in the workstation header.
  2. Frontend routes requests through `MockInspectionAdapter.ts`.
  3. Instantly renders realistic statutory declarations and evidence crops in-browser without any network communication.
  4. Banner clearly indicates: `"STANDALONE MOCK MODE"`.

### Layer 5: Pre-Recorded Video & Offline PDF Dossier
- Video stored locally on desktop: `assets/demo_recording_4k.mp4`.
- Pre-compiled inspection dossiers stored in `assets/dossiers/`.

---

## 6. Offline Verification Instructions (Proof of Disconnection)

To prove to the jury that the system is 100% offline:
1. Open Windows Network Settings (or run `ipconfig /all`).
2. Turn **Airplane Mode ON** (disable all Wi-Fi and cellular connections).
3. Disconnect any physical Ethernet cables.
4. Ping external IP:
   ```bash
   ping 8.8.8.8
   # Expected output: Destination host unreachable / General failure
   ```
5. In the browser, perform a full packaging inspection and download PDF dossier.
6. The inspection will complete in < 200 ms, demonstrating that **zero cloud APIs, zero remote CDNs, and zero telemetry** are utilized.

---

## 7. Jury Claim Governance (Evidence Table)

| Subject | Jury Claim | Empirical Evidence | Release Status | Mandatory Safe Wording |
|---|---|---|:---:|---|
| **OCR Perception** | "Extracts text from packaging" | 33 unit tests, 8 synthetic fixtures, PaddleOCR ONNX models on disk | **VERIFIED** | *"Performs automated scene text detection and bilingual Latin/Devanagari recognition."* |
| **Multilingual** | "Supports Hindi declarations" | Devanagari SVTR model with 167-char dictionary (`rec_hi/rec.onnx`), `SYNTH-02` test | **VERIFIED** | *"Recognizes Devanagari Hindi statutory declarations alongside Latin script."* |
| **Optical Calibration** | "Estimates physical dimensions" | 53 calibration tests, ellipse fitting for ₹10 coin, ID-1 homography | **CONDITIONALLY VERIFIED** | *"Estimates physical dimensions in millimeters only when a verified fiducial anchor is detected or manual caliper is provided."* |
| **Physical Scale Zero-Fabrication**| "Never invents scale" | Zero-scale tests (`test_calculate_font_height_uncalibrated`), scale returns `None` without anchor | **VERIFIED** | *"When uncalibrated, physical scale is null and statutory font conclusions are withheld."* |
| **Jan Vishwas Adherence** | "Enforces 2026 legal rules" | 122 rules engine tests, `penalties.py`, `notice_builder.py` | **VERIFIED** | *"Generates Section 36(1) Improvement Notices under the Jan Vishwas Act 2026 with a configurable 15-day demonstration default."* |
| **Physical Font MAE < 0.15 mm** | "Accurate to 0.12 mm" | 35 retail SKUs not yet on disk | **BENCHMARK_BLOCKED** | *"Physical metrological benchmark is gated awaiting field collection with calibrated vernier calipers."* |
| **System Latency** | "Operates in real-time" | 20 iterations measured in `api_latency_benchmark.py`: mean 72.82 ms | **VERIFIED** | *"End-to-end CPU inference pipeline completes in under 150 ms (budget: 2500 ms)."* |
| **Production Certification**| "Production-ready system" | Hackathon prototype environment | **UNSUPPORTED** | *"SIH 2026 controlled demonstration prototype; not certified for legal enforcement without physical benchmark sign-off."* |

---

## 8. Claims We CAN Make vs Claims We MUST NOT Make

### What We CAN Say:
- "The system is 100% offline and requires zero internet connectivity."
- "The system replaces legacy criminal threats with civil Improvement Notices per the Jan Vishwas Act, 2026."
- "The system guarantees zero scale fabrication: if an anchor is not detected, scale is null."
- "The system audits mandatory declarations under Rule 6, 6(11) USP arithmetic, and Rule 26 statutory exemptions."
- "The system provides an evidence canvas with quadrilateral polygon overlays and a 2-point manual caliper fallback."
- "The system passes 832 backend tests, 307 frontend tests, and 3 Playwright browser E2E workflows."

### What We MUST NOT Say:
- **DO NOT SAY:** "This system is production-ready or certified by the Department of Consumer Affairs."
- **DO NOT SAY:** "Our font height measurement achieves 0.12 mm MAE across retail products" (mark as *BENCHMARK_BLOCKED* until physical SKUs are collected).
- **DO NOT SAY:** "The system has 100% accuracy and zero false positives."
- **DO NOT SAY:** "The 15-day cure period is a rigid statutory mandate in Section 36(1)" (clarify it is a *reasonable cure period* with a 15-day system demonstration default).
- **DO NOT SAY:** "A smartphone camera alone can legally certify packaging dimensions without calibration."

---

## 9. Judge Q&A Defense Strategy

### Question 1: *"How do you measure font height in millimeters from a 2D camera photograph?"*
> **Officer Answer:**
> "A 2D photograph alone has no intrinsic physical scale. MetroLens enforces a **Zero Scale Fabrication Guarantee**. Physical millimeters are calculated strictly when an optical fiducial standard (such as an RBI ₹10 coin with a known 27.00 mm diameter or an ID-1 card) is detected in the image plane, rectified via algebraic ellipse fitting or planar homography. If no anchor is present, the system preserves scale as `null` and withholds automatic font conclusions, prompting the officer to either use the built-in 2-point manual caliper tool or take a calibrated photo."

### Question 2: *"What statutory amendments have you incorporated from the Jan Vishwas Act, 2026?"*
> **Officer Answer:**
> "Under the Jan Vishwas (Amendment of Provisions) Act, 2026, Section 36(1) of the Legal Metrology Act was decriminalized. The first offence mandates the issuance of an **Improvement Notice** granting a reasonable cure period without monetary penalty. MetroLens configures a 15-day demonstration default for this notice. Second offences incur civil adjudication penalties up to ₹5,00,000, and third offences up to ₹50,00,000. All legacy ₹25k/₹50k fine tables have been completely removed from our statutory engine."

### Question 3: *"Have you benchmarked this on real retail packages?"*
> **Officer Answer:**
> "We practice strict anti-hallucination governance. While our OCR and rules engines are verified against synthetic FMCG test specimens and our pipeline latency is verified at 72 ms on CPU, our **Physical Metrology Benchmark is formally declared BENCHMARK_BLOCKED**. We have 1 authentic Cadbury specimen on disk, but until dual-rater vernier caliper measurements and 1200 DPI comparator scans for 35 distinct retail SKUs are acquired, we do not claim empirical physical font MAE."
