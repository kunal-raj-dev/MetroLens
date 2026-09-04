# ARCHITECTURAL REVIEW & TOPOLOGY UPGRADE (V0.3)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Review Date:** 4 September 2026 | **Reviewer:** Principal System Architect  
**Core Assessment:** Formal transition from over-extended V0.1 architecture to resilient, experiment-backed, edge-native V0.3 architecture.

---

## 1. Architectural Evolution: V0.1 vs. V0.3

```
================================================================================
                           ARCHITECTURE V0.1 (PREVIOUS)
================================================================================
  [Physical Package]                [E-Commerce Listing URL] (Amazon/Blinkit)
           |                                      |
           v                                      v
  [Camera Viewfinder]                [Playwright Headless Web Scraper]
           |                                      |
           v                                      v
  [OpenCV Coin Ellipse] ------> [8-DOF Planar Homography Warper] (UNVERIFIED)
           |                                      |
           v                                      v
  [PaddleOCR Local ONNX] ----> [Constrained Gemini 1.5 Flash Cloud LLM]
           |                                      |
           v                                      v
  [Python Rule Functions] ---> [Automated Section 36 Penalty / Fine Issuer]
           |                                      |
           v                                      v
  [Image-Based Compliance Assessment Report PDF] -------> [Live National eMaap Webhook Sync] (UNVERIFIED API)

================================================================================
                          ARCHITECTURE V0.3 (CORRECTED)
================================================================================
  [Physical Package + Metric Anchor] --> [Quality Guard: Glare & Blur Filter]
                                                       |
                                                       v
                                         [Primary: Planar Metric Calibration]
                                         [Secondary: Right Cylinder Strip]
                                         [Fallback: Manual Reference Scale]
                                                       |
                                                       v
                                         [Local Multilingual OCR (ONNX int8)]
                                                       |
                                                       v
                                         [Canonical Entity Normalizer]
                                         (Deterministic Regex + Pydantic)
                                         (Cloud LLM: OPTIONAL Enrichment Only)
                                                       |
                                                       v
                                  [Versioned Statutory Rule Engine (Python)]
                                  - Rule 6 Declarations (a-h)
                                  - Rule 6(11) Denominated USP Auditor
                                  - Rule 7 Tables I and II Area & Font Matrix
                                  - Rule 26 Commodity-Aware Exemption Switch
                                                       |
                                 +---------------------+---------------------+
                                 v                                           v
                    [5-State Inspector UI]                   [Assessment Report Generator]
                    - Side-by-Side Visual Crops              - Cryptographic SHA-256 Hashes
                    - Metric Measurement Deficits            - Statutory Improvement Notice
                    - 1-Tap Manual Review Toggle             - eMaap-Compatible JSON Export
```

---

## 2. Deep-Dive: What Was Wrong in V0.1 and Why

### Defect 1: Unverified Planar Homography & Scale Recovery
- **What Was Wrong:** V0.1 asserted that fitting an ellipse to an Indian 10-Rupee coin contour uniquely resolves an 8-DOF planar homography matrix (H) to unwarp perspective tilt up to 35° with sub-0.12mm accuracy.
- **Why It Is Problematic:** Mathematically, a circle projected under perspective forms an ellipse whose major and minor axes provide metric scale along the major axis and tilt inclination angle cos(theta) = b/a. However, it leaves the azimuthal orientation around the surface normal ambiguous without coplanar corner correspondences (such as package boundaries or rectangular markers). Treating this as a settled, production-ready algorithm before running an empirical spike risked catastrophic pipeline failure on Day 3.
- **V0.3 Correction:** Replaced the unverified assumption with a formal **Day 1 Calibration Feasibility Spike**. The pipeline decouples scale estimation (S = diameter / d_major) for near-normal captures from full homography, introduces standard rectangular ID card fallback (85.60 x 53.98mm providing 4 true corners), and enforces viewfinder plane-alignment guides.

### Defect 2: Statutory Misnomer & Illegal Enforcement Logic
- **What Was Wrong:** V0.1 generated a document titled "Image-Based Compliance Assessment Report", cited Section 36 penalties up to ₹25,000, and framed the output as an automated fine.
- **Why It Is Problematic:** Under the Legal Metrology (Packaged Commodities) Rules, 2011, "Image-Based Compliance Assessment Report" is an application for manufacturer registration under Rule 27; it has nothing to do with inspection reports. Furthermore, under the **Jan Vishwas (Amendment of Provisions) Act, 2026**, Section 36(1) labeling violations have been decriminalized: the first offence mandates an **Improvement Notice** giving the brand time to rectify, with zero initial fine. Adjudication of repeated offences is restricted to statutory Adjudicating Officers under Section 48A.
- **V0.3 Correction:** Completely removed "Image-Based Compliance Assessment Report". The output is renamed **"MetroLens AI — Image-Based Compliance Assessment Report"**. The system acts strictly as an **assistive evidentiary screening tool under Section 15**, generating supporting evidence and recommending an Improvement Notice under Section 36(1).

### Defect 3: Scope Creep (Headless E-Commerce Scraping & Live eMaap Sync)
- **What Was Wrong:** V0.1 scheduled building a Playwright headless browser scraper for Amazon/Blinkit listings and a live webhook integration with the National eMaap portal.
- **Why It Is Problematic:** Team of 6 students is building two projects in parallel over 8–9 days. E-commerce scraping against modern anti-bot systems (Cloudflare, CAPTCHAs, dynamic React DOMs) is notoriously flaky and adds massive debugging overhead with zero core scoring benefit under SIH26034. Furthermore, eMaap does not publish an open third-party developer API.
- **V0.3 Correction:** **Excised E-Commerce Scraper from MVP entirely** (deferred to post-hackathon). Refactored eMaap integration to an **"eMaap-Inspired Architecture / Mock REST Adapter"** with standardized JSON export, saving over 16 engineering hours.

### Defect 4: Cloud LLM in the Critical Compliance Decision Path
- **What Was Wrong:** V0.1 suggested using Gemini 1.5 Flash to parse entities and assist with compliance evaluation.
- **Why It Is Problematic:** Any live internet dependency during a hackathon demonstration creates existential failure risk when venue Wi-Fi drops. Furthermore, LLMs hallucinate statutory clauses and fail on decimal arithmetic required for Unit Sale Price (USP).
- **V0.3 Correction:** **100% Offline Localhost Execution.** Quantized PaddleOCR v4 ONNX running on CPU handles text extraction. Entity normalization is performed by deterministic regex pipelines. The statutory compliance engine is high-confidence deterministic Python. Gemini is restricted to an optional, secondary cloud enrichment demo.

### Defect 5: Binary Pass/Fail Status Model
- **What Was Wrong:** V0.1 used a binary red/green verdict model (VERIFIED_COMPLIANT vs NON_COMPLIANT).
- **Why It Is Problematic:** In field regulatory enforcement, low-contrast packaging, borderline font heights (1.45mm vs 1.50mm), or faded dot-matrix inkjet dates cannot be definitively classified as illegal without risking regulatory harassment.
- **V0.3 Correction:** Implemented a **5-State Compliance Model**:
  1. `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` (Green)
  2. `POTENTIAL_NON_COMPLIANCE` (Red)
  3. `MANUAL_REVIEW_REQUIRED` (Amber)
  4. `STATUTORY_EXEMPTION_APPLIED` (Blue - Rule 26)
  5. `NOT_IMAGE_VERIFIABLE` (Gray - requires physical weighing scale or chemical lab).

---

## 3. Corrected Component Architecture (V0.3 Specifications)

| Subsystem | Module Name | Implementation Technology | Primary Responsibility | Error Handling & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion Guard** | `modules/cv/glare_precheck.py` | OpenCV (HSV space V>250, Laplacian variance) | Evaluates frame quality; checks for specular whiteout glare and defocus blur. | Viewfinder alert: "Specular glare detected — tilt package 10°". |
| **Metric Scale Anchor** | `modules/cv/scale_calibration.py` | OpenCV `findContours`, ellipse fit, minimum area bounding box | Recovers pixel-to-mm scale factor S from 27.0mm 10-Rupee coin or ISO card. | UI Manual Scale Override (tap 2 reference points or enter box height). |
| **Geometry Engine** | `modules/cv/cylinder_invariance.py` | OpenCV coordinate projection | Evaluates font heights along vertical generator line on verified right circular cylinders. | Non-cylindrical or tapered surfaces routed to `MANUAL_REVIEW_REQUIRED`. |
| **Scene Text OCR** | `modules/ocr/paddle_onnx_engine.py` | PaddleOCR v4 Mobile (ONNX int8 quantized) | Local multilingual text detection (DBNet++) and recognition (SVTR) on CPU. | Local Tesseract 5 hot-swap fallback if ONNX initialization fails. |
| **Entity Normalizer** | `modules/normalizer/entity_parser.py` | Python Regex + Pydantic Schema | Maps raw OCR bounding boxes into canonical packaging fields (`CanonicalDeclaration`). | Low-confidence fields marked `None`; flagged for manual confirmation. |
| **Statutory Rule Engine**| `modules/rules/rule_engine.py` | Versioned Python State Machine | Deterministic evaluation of Rules 6(1)(a)-(h), 6(11) USP, 7 Tables I and II, 8, and 26. | Graceful fallback: borderline values routed to `MANUAL_REVIEW_REQUIRED`. |
| **Evidence & Reporting**| `modules/reporting/report_generator.py` | ReportLab / WeasyPrint + `hashlib` | Renders tamper-evident Assessment Report PDF embedding SHA-256 hashes and evidence crops. | In-app visual JSON report viewer if PDF compilation fails. |
| **eMaap Adapter** | `modules/integration/emaap_mock_adapter.py` | FastAPI REST Endpoint | Simulates national eMaap portal synchronization using standardized schema. | Local offline queue if network interface is disabled. |

---

## 4. Architectural Invariant Rules (Non-Negotiable)
1. **Rule of Determinism:** Zero neural network or LLM probabilistic outputs in the legal compliance verdict path. AI extracts; mathematics validates; deterministic rules decide.
2. **Rule of Offline Resilience:** The core demonstration pipeline MUST execute end-to-end on `localhost:8000` with zero outbound internet requests.
3. **Rule of Assistive Governance:** The system NEVER pretends to issue fines or judicial orders. It generates supporting compliance assessments to assist authorized officers.
