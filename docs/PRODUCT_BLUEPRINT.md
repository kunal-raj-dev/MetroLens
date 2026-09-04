# MASTER PRODUCT BLUEPRINT & TECHNICAL SPECIFICATION (V0.3)
# MetroLens AI™ — Automated Legal Metrology Inspection & Compliance System
### Sponsoring Ministry: Ministry of Consumer Affairs, Food & Public Distribution | Problem Statement: SIH26034
**Evaluation Framework:** InnoHack 3.0 / Smart India Hackathon 2026 (100 Marks Total)  
**Document Status:** Authoritative Single Source of Truth (Post-Audit Edition v0.3) | **Date:** 4 September 2026

---

## 1. Executive Summary

**MetroLens AI™** is an edge-native, perspective-corrected mobile computer vision and regulatory audit system designed for District Legal Metrology Officers (LMOs) and packaging compliance auditors. It transforms a tedious, manual 20-minute ruler-and-magnifier inspection into a **sub-2.5-second, mathematically verified, tamper-evident regulatory compliance audit**.

By combining a **universally available optical metric anchor** (a standard 10-Rupee coin or ISO card) with **planar metric scale calibration**, MetroLens AI solves the fundamental monocular scale ambiguity of smartphone cameras. It directly evaluates statutory numeral heights (Rule 7 Table-I/II) against calibrated Principal Display Panel (PDP) areas, audits Unit Sale Price (USP) arithmetic against Net Quantity and MRP under Rule 6(11) in standardized denominations, extracts mandatory packaging declarations across English and Hindi using local scene text OCR, and verifies compliance through a **100% deterministic statutory state machine**.

The system operates **entirely offline** on local edge hardware without external cloud dependency, generates a cryptographically sealed (SHA-256) **Image-Based Compliance Assessment Report** under Section 15 of the Legal Metrology Act, 2009 (incorporating the **Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice framework** under Section 36(1)), and provides an **eMaap-Inspired Mock REST Adapter Interface** ready for national portal integration.

---

## 2. Problem Statement & Operational Realities

### Official Problem Statement (SIH26034)
> *"Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels."*

### Field Operational Reality Today (The Enforcement Deficit)
In India, pre-packaged commodities represent over ₹12 Lakh Crore ($150 Billion) in annual retail trade across millions of Kirana stores, supermarkets, and quick-commerce dark stores. Enforcement is entrusted to approximately **2,500 District Legal Metrology Officers (LMOs)** across 780+ districts:
1. **Manual Vernier & Ruler Auditing:** An inspecting officer must physically hold a plastic ruler or micrometer against microscopic print on flexible pouches or curved containers—a slow, contentious, and visually fatiguing procedure.
2. **Inspection Coverage $<0.01\%$:** Due to extreme human resource constraints, over 99.99% of retail packages are never inspected unless a formal consumer grievance is escalated.
3. **Shrinkflation & Deceptive USP:** Brands frequently downsize net contents (e.g. from 100g to 82g) while retaining identical packaging footprints and prices. While Rule 6(11) mandates Unit Sale Price (e.g. "₹0.61 per g"), brands often omit USP or print it in microscopic 0.5mm fonts hidden within bottom gussets.
4. **Decriminalization & Administrative Burden:** The **Jan Vishwas (Amendment of Provisions) Act, 2026** decriminalized first-time labeling infractions, requiring officers to issue formal **Improvement Notices** with rigorous prima facie evidence before any repeated-offence penalty can be adjudicated.

---

## 3. Product Scope & Requirements Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ A. OFFICIAL STATUTORY REQUIREMENTS (Strict Problem Statement Baseline)      │
│ • Image ingestion of packaged commodities, labels, and product images.      │
│ • Optical Character Recognition (OCR) of statutory packaging declarations.   │
│ • Rule-based evaluation against Legal Metrology (PC) Rules, 2011.            │
│ • Flagging omissions, non-compliances, and deceptive declarations.          │
│ • Summarized compliance reporting for regulatory enforcement authorities.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ B. ENGINEERING INTERPRETATIONS (Mandated by Physical & Optical Realities)   │
│ • Physical scale recovery via coplanar metric reference (10-Rupee coin/card)│
│ • Constrained near-normal capture (<10° tilt) & planar scale calibration.    │
│ • Deterministic mathematical verification of Unit Sale Price (USP) division.│
│ • Area calculation of Principal Display Panel (PDP) to index Rule 7 Table-I/II.│
│ • 5-State classification model to prevent regulatory merchant harassment.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ C. HACKATHON VALUE DIFFERENTIATORS (Scoring Rubric Optimizers)              │
│ • 100% offline standalone edge execution on localhost.                      │
│ • Cryptographic SHA-256 evidence package with side-by-side rectified crops.  │
│ • Statutory alignment with Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice process. │
│ • eMaap Mock REST Adapter demonstrating enterprise government readiness.    │
│ • Brand Pre-Flight Artwork Mode (DPI-to-mm verification for packaging PDFs).│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Goals & Non-Goals

### Measurable Engineering Goals
1. **Accurate Perception:** Extract statutory packaging declarations with Character Error Rate $<6.0\%$ on local CPU.
2. **Calibrated Physical Measurement:** Measure printed numeral heights with target Mean Absolute Error (MAE) $<0.15\text{mm}$ against 1200 DPI optical scan ground truth.
3. **100% Deterministic Rule Evaluation:** Evaluate legal rules using isolated Python state machines—**zero LLM hallucination in compliance decisions**.
4. **Sub-2.5-Second Latency:** Complete the scan-to-report pipeline in $<2.5\text{ seconds}$ on standard consumer quad-core laptop CPUs.
5. **100% Offline Capability:** Execute the entire live stage demonstration with Wi-Fi and Cellular toggled off.
6. **Legally Grounded Evidentiary Output:** Generate a tamper-evident Compliance Assessment Report embedding SHA-256 hashes and Section 36(1) Improvement Notice recommendations.

### Explicit Non-Goals (What We Will NOT Do)
1. **Physical Weight Verification:** Monocular cameras **cannot weigh objects**. Physical weight verification is governed by Rule 24 and requires a certified physical weighing scale.
2. **Chemical Purity / Nutritional Testing:** Chemical contents and adulteration are governed by FSSAI lab testing, not Legal Metrology visual checks.
3. **Physical Factory Reality Checks:** The system checks the syntactic completeness of the manufacturer address and PIN code; it cannot physically verify whether a factory exists without field officer visits.
4. **Issuing Unilateral Legal Fines:** The software acts as an **assistive screening tool under Section 15**. It does not act as an Adjudicating Officer or automatically impose fines.
5. **Headless E-Commerce Scraping in MVP:** Scraping Amazon/Blinkit listings in real-time introduces bot-detection failures and is deferred to post-hackathon.
6. **Blockchain / Smart Contracts:** Blockchain adds zero legal admissibility in Indian district courts and represents buzzword distraction.

---

## 5. Definitive Feature Prioritization (MVP Scope)

```
================================================================================
                          DEFINITIVE FEATURE PRIORITY
================================================================================
  [ MUST HAVE ] (Core 8–9 Day MVP Spine — Non-Negotiable)
  • Mobile web viewfinder with real-time HSV glare pre-check & blur filter
  • Planar metric scale recovery using 10-Rupee coin / ISO card
  • Local multilingual OCR (PaddleOCR v4 ONNX int8) on CPU
  • Canonical entity normalizer (regex + Pydantic schema)
  • Deterministic Rule Engine (Rules 6(1)(a)-(h), 6(11) USP, 7, 8, 26)
  • 5-State compliance classification & side-by-side evidence crop viewer
  • Cryptographic Image-Based Compliance Assessment Report PDF (SHA-256)
  • 100% offline localhost execution architecture

  [ SHOULD HAVE ] (Target for Day 5–6)
  • Right-cylinder central generator vertical font height invariance module
  • eMaap Mock REST Webhook Adapter (`POST /api/v1/emaap/mock-sync`)
  • Inspector 1-tap manual review toggle & confirmation UI
  • UI manual reference scale override mode (click 2 points)

  [ NICE TO HAVE ] (Day 7 Buffer Only)
  • Brand Pre-Flight Artwork Mode (DPI-to-mm verification on PDF artwork)
  • Multi-panel inspection aggregation (front PDP + back panel stitching)

  [ DO NOT BUILD ] (Excised Strategic Distractions)
  • NO Playwright e-commerce marketplace scraping (deferred to post-hackathon)
  • NO live unverified eMaap production integration (mock adapter only)
  • NO custom neural network training from scratch (use pretrained ONNX)
  • NO blockchain or distributed ledger technology
  • NO complex OAuth2 / JWT authentication bloat
  • NO native Android APK packaging (responsive PWA is faster and portable)
================================================================================
```

---

## 6. Comprehensive System Architecture (V0.3)

```
                                SYSTEM ARCHITECTURE
                                
  [ Physical Package + Metric Anchor ]       [ Digital Packaging Artwork (PDF) ]
                 │                                           │
                 ▼                                           ▼
       ┌──────────────────────┐                   ┌───────────────────────┐
       │ Mobile Web Camera    │                   │ Brand Pre-Flight Mode │
       │ Viewfinder (WebRTC)  │                   │ (DPI to mm Converter) │
       └──────────┬───────────┘                   └───────────┬───────────┘
                  │                                           │
                  ▼                                           ▼
       ┌──────────────────────────────────────────────────────────┐
       │ Quality Gate: HSV Glare Pre-Check & Laplacian Blur Filter │
       └──────────────────────────┬───────────────────────────────┘
                                  │ Validated Frame
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       ┌──────────────────────┐       ┌───────────────────────┐
       │ Package & PDP Outer  │       │ Metric Scale Anchor   │
       │ Bounding Box Detector│       │ (27.0mm Coin Contour  │
       │ (Contour / Bounding) │       │  or ISO Card Corners) │
       └──────────┬───────────┘       └───────────┬───────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
       ┌──────────────────────────────────────────────────────────┐
       │ Metric Scale & Planar Rectification Engine               │
       │ -> Recovers Millimeters per Pixel Scale Factor (S)       │
       │ -> Secondary: Right Cylinder Generator Strip Projection  │
       └──────────────────────────┬───────────────────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       ┌──────────────────────┐       ┌───────────────────────┐
       │ Local Scene Text OCR │       │ Calibrated Stroke     │
       │ (PaddleOCR v4 ONNX)  │       │ Measurement Engine    │
       │ (English + Hindi)    │       │ (Numeral Height mm)   │
       └──────────┬───────────┘       └───────────┬───────────┘
                  │ Text Lines + BBoxes           │ Measured Dimensions
                  └───────────────┬───────────────┘
                                  │
                                  ▼
       ┌──────────────────────────────────────────────────────────┐
       │ Canonical Entity Normalizer (Regex + Pydantic Schema)    │
       │ (Cloud LLM: OPTIONAL Secondary Cloud Enrichment Only)    │
       └──────────────────────────┬───────────────────────────────┘
                                  │ Canonical JSON Entity
                                  ▼
       ┌──────────────────────────────────────────────────────────┐
       │ Deterministic Statutory Compliance Rule Engine (Python)  │
       │ • Rule 6(1)(a-h) Mandatory Declaration Verifier          │
       │ • Rule 6(11) Unit Sale Price Deterministic Math Auditor  │
       │ • Rule 7 & Rule 7 Table-I/II Area-to-Font Height Matrix     │
       │ • Rule 26 Category-Aware Statutory Exemption Switch      │
       └──────────────────────────┬───────────────────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       ┌──────────────────────┐       ┌───────────────────────┐
       │ 5-State Compliance   │       │ Cryptographically     │
       │ Inspector Dashboard  │       │ Sealed Assessment     │
       │ & Evidence Viewer    │       │ Report PDF (SHA-256)  │
       └──────────────────────┘       └───────────┬───────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │ eMaap Mock REST       │
                                      │ Webhook Sync Adapter  │
                                      └───────────────────────┘
```

---

## 7. The Four Pillars: AI vs. Deterministic Boundaries

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AI PERCEIVES (Probabilistic Domain)                                      │
│ • Technology: Quantized PaddleOCR v4 Mobile (DBNet++, SVTR).                │
│ • Role: Converts raw packaging pixels into character strings and bboxes.    │
│ • Boundary: AI never decides whether the extracted text violates the law.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MATH VALIDATES (Empirical Geometric Domain)                              │
│ • Technology: Metric Scale Calibration & IEEE 754 Floating-Point Division.  │
│ • Role: Recovers physical millimeters; calculates Expected USP = MRP / Qty. │
│ • Boundary: Zero heuristic rounding; strict standard denomination rules.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. RULES DECIDE (Deterministic Statutory Domain)                            │
│ • Technology: Versioned Python State Machine (`modules/rules/`).            │
│ • Role: Codifies Gazette clauses, Table 1 area thresholds, and exemptions.  │
│ • Boundary: 100% deterministic, audit-traceable, and version-stamped.       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HUMANS GOVERN (Regulatory Enforcement & Discretion)                      │
│ • Technology: 5-State Result Classification & 1-Tap Manual Review UI.       │
│ • Role: Inspecting officer reviews borderline cases and signs notices.      │
│ • Boundary: System assists officers; human officer issues statutory notice. │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Physical Measurement Pipeline & Optical Principles

### The Monocular Scale Proof
A camera projects real-world metric dimensions $X$ at distance $Z$ onto sensor pixels $u$ via:
$$u = f \cdot \frac{X}{Z}$$
Without a known scale reference or physical depth $Z$, absolute metric measurement from a single image is mathematically impossible.

### Metric Scale Recovery
1. The inspector places a standard Indian 10-Rupee coin (outer diameter: $27.0\text{mm}$) coplanar with the packaging panel.
2. The vision pipeline detects the coin contour using OpenCV edge detection and fits an ellipse parameterized by major axis $d_{\text{major}}$ and minor axis $d_{\text{minor}}$.
3. Under near-normal capture ($\le 10^\circ$ tilt enforced by viewfinder reticle guides), the metric scale factor $S$ is:
   $$S = \frac{27.0\text{ mm}}{d_{\text{major}}} \quad (\text{mm/pixel})$$
4. When perspective tilt is present, 4-corner correspondences (from an ISO card or rectangular carton boundary) compute the planar homography matrix $H$, warping the panel into an orthorectified metric plane where $1\text{ pixel} \equiv S\text{ millimeters}$.

### Right-Cylinder Vertical Generator Invariance
For standard upright cylindrical containers (cans, bottles):
- Curvature along the circumferential horizontal axis foreshortens text by $\cos\phi$.
- Along the vertical generator line parallel to the cylinder axis: $y_{\text{proj}} = y_{\text{actual}}$.
- **Statutory Impact:** Rule 7 font height is strictly measured along the **vertical axis** (numeral capital height / ascender-descender). Therefore, cylindrical curvature introduces zero vertical foreshortening along the generator strip. The system measures font heights strictly within the central $40^\circ$ generator strip ($\cos\phi \ge 0.94$). Tapered, conical, or irregular containers are routed to `MANUAL_REVIEW_REQUIRED`.

---

## 9. Statutory Compliance Rule Engine Specification

### Data Model (`CanonicalDeclaration`)
```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UnitType(str, Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    METER = "m"
    NUMBER = "N"
    PIECE = "piece"

class ComplianceStatus(str, Enum):
    NO_VIOLATION = "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED"
    POTENTIAL_VIOLATION = "POTENTIAL_NON_COMPLIANCE"
    MANUAL_REVIEW = "MANUAL_REVIEW_REQUIRED"
    STATUTORY_EXEMPT = "STATUTORY_EXEMPTION_APPLIED"
    NOT_VERIFIABLE = "NOT_IMAGE_VERIFIABLE"

class CanonicalDeclaration(BaseModel):
    mrp: Optional[float] = Field(None, description="Maximum retail price in INR")
    tax_qualifier_present: bool = Field(False, description="Presence of 'inclusive of all taxes'")
    net_quantity: Optional[float] = Field(None, description="Numerical net quantity")
    net_quantity_unit: Optional[UnitType] = Field(None, description="Standard SI unit symbol")
    declared_usp: Optional[float] = Field(None, description="Declared Unit Sale Price in INR")
    declared_usp_unit: Optional[str] = Field(None, description="Unit denomination (e.g. per g, per kg)")
    mfg_month: Optional[int] = Field(None, ge=1, le=12)
    mfg_year: Optional[int] = Field(None, ge=2020, le=2030)
    manufacturer_name: Optional[str] = None
    manufacturer_pincode: Optional[str] = None
    consumer_care_phone: Optional[str] = None
    consumer_care_email: Optional[str] = None
    country_of_origin: Optional[str] = None
    pdp_area_sqcm: Optional[float] = Field(None, description="Measured PDP area in cm^2")
    measured_font_height_mm: Optional[float] = Field(None, description="Measured numeral height in mm")
    product_category: Optional[str] = Field("General FMCG", description="Commodity taxonomy category")
```

---

## 10. Five-State Compliance Result Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. NO IMAGE-VERIFIABLE VIOLATION DETECTED (Green)                           │
│ • All mandatory declarations present and syntactically valid.               │
│ • Measured font heights meet or exceed Rule 7 Table-I/II minimums.             │
│ • Declared USP matches calculated MRP / Net Quantity in standard units.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. POTENTIAL NON-COMPLIANCE (Red)                                           │
│ • Omission of mandatory declaration (missing USP, MRP, or contact details). │
│ • Severe font deficit (measured height < statutory minimum - 0.10mm).       │
│ • Arithmetic USP discrepancy exceeding 1% statutory rounding margin.        │
│ • Prohibited non-metric units ("Gms", "Kgs", "ML").                         │
│ • Recommended Action: Issue Improvement Notice under Section 36(1).         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. MANUAL REVIEW REQUIRED (Amber)                                           │
│ • OCR confidence on critical field falls between 60% and 80%.               │
│ • Measured font height is borderline (within 0.10mm benefit-of-doubt buffer)│
│ • Address present but PIN code format ambiguous.                            │
│ • Non-planar or tapered container curvature detected.                       │
│ • Action: Inspector visual crop verification via 1-tap confirmation UI.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. STATUTORY EXEMPTION APPLIED (Blue)                                       │
│ • Net quantity <= 10g or <= 10ml on non-tobacco / non-pan masala goods.     │
│ • Wholesale industrial package > 25kg or > 25L.                             │
│ • Action: Suppress false-positive violation notices under Rule 26.          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. NOT IMAGE-VERIFIABLE (Gray)                                              │
│ • Physical net contents weight/volume check under Rule 24.                  │
│ • Chemical/nutritional purity (FSSAI laboratory testing).                  │
│ • Action: Flag for physical check-weighing on certified scale.              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Evidence Model & Tamper-Evident Reporting

Under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 / Section 65B of the Indian Evidence Act, 1872, electronic records require verifiable integrity and provenance:

```json
{
  "inspection_id": "INSP-2026-DEL-04921",
  "utc_timestamp": "2026-09-04T10:14:22.841Z",
  "device_telemetry": {
    "gps_latitude": 28.6139,
    "gps_longitude": 77.2090,
    "device_fingerprint": "LMO-NODE-DELHI-04"
  },
  "cryptographic_integrity": {
    "raw_capture_sha256": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "rectified_crop_sha256": "8a35e612f17094b80e8f39572458f334a1796d11f8e1329c3629393963496924",
    "composite_record_sha256": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
  },
  "pipeline_versions": {
    "ocr_engine": "PaddleOCR-v4-Mobile-ONNX-int8",
    "rule_engine_version": "2026.09-JanVishwas-v0.3"
  }
}
```

The generated **Image-Based Compliance Assessment Report** is rendered as a clean multi-page PDF embedding:
1. Sponsoring Ministry Banner (Ministry of Consumer Affairs, Food & Public Distribution).
2. Inspection Metadata (Inspection ID, UTC Timestamp, Officer ID, GPS Coordinates).
3. Side-by-Side Visual Evidence Crop (Raw capture, rectified crop, bounding box overlay).
4. Statutory Rule Assessment Table (Applicable Rule, Statutory Mandate, Measured Value, Deficit).
5. Recommended Regulatory Action (Improvement Notice under Section 36(1) or Section 15 sample seizure).
6. Cryptographic Integrity Seal & QR Code linking to local audit hash.
7. Statutory Disclaimer: *"Automated image-based assessment. Final legal determination remains with the authorized officer."*

---

## 12. Proposed Repository Structure

```
SIH26034_MetroLens_AI/
├── docs/                                  # Project Documentation Suite (v0.3)
│   ├── PRODUCT_BLUEPRINT.md               # Master Single Source of Truth
│   ├── LEGAL_RULE_MATRIX.md               # Statutory Rules & 2026 Legal Foundation
│   ├── TECHNICAL_DECISIONS.md             # Architecture Decision Records (ADRs)
│   ├── DATA_AND_BENCHMARK_PLAN.md         # Phased Data & Measurement Protocol
│   ├── IMPLEMENTATION_PLAN.md             # 8–9 Day Roadmap & 6-Member Ownership
│   ├── DEMO_PLAN.md                       # Live Pitch Script & 5-Layer Failover
│   ├── RISK_REGISTER.md                   # 15 Risks & 48-Hour Kill Switch
│   ├── JURY_QA.md                         # 32 Adversarial Questions & Defenses
│   ├── AUDIT_V0_2.md                      # Formal Audit Report (Issues 1-34)
│   ├── ASSUMPTION_REGISTER.md             # Living Assumption Tracking
│   ├── OPEN_QUESTIONS.md                  # Prioritized P0/P1/P2 Questions
│   ├── TRACEABILITY_MATRIX.md             # End-to-End Requirements Traceability
│   ├── ARCHITECTURE_REVIEW_V0_2.md        # Architectural Evolution Record
│   └── DECISION_LOG.md                    # ADR Validation Status Log
├── backend/                               # Python FastAPI Backend (100% Localhost)
│   ├── main.py                            # Application Entry Point
│   ├── requirements.txt                   # Dependency Specification
│   ├── modules/
│   │   ├── cv/                            # Computer Vision & Metric Scale
│   │   │   ├── scale_calibration.py       # Coin contour detection & scale factor S
│   │   │   ├── glare_precheck.py          # HSV saturation glare filter
│   │   │   ├── cylinder_invariance.py     # Vertical generator line height logic
│   │   │   └── pdp_detector.py            # Packaging boundary & area estimator
│   │   ├── ocr/                           # Multilingual Scene Text OCR
│   │   │   ├── paddle_onnx_engine.py      # Local quantized ONNX runtime
│   │   │   ├── text_cropper.py            # Bounding box extraction & slicing
│   │   │   └── hindi_mapping.py           # Devanagari phrase mapping
│   │   ├── normalizer/                    # Entity Structuring
│   │   │   ├── entity_parser.py           # Regex key-value extractor
│   │   │   └── schemas.py                 # Pydantic Canonical Schemas
│   │   ├── rules/                         # Deterministic Rule Engine
│   │   │   ├── base_rule.py               # Abstract Rule Interface
│   │   │   ├── rule_6_declarations.py     # Rule 6(1)(a)-(h) mandatory checks
│   │   │   ├── rule_6_11_usp.py           # Unit Sale Price arithmetic auditor
│   │   │   ├── rule_9_font_matrix.py      # Rule 7 Table-I/II area lookup
│   │   │   ├── rule_26_exemptions.py      # Category-aware exemption switch
│   │   │   └── rule_engine.py             # Master Compliance Evaluator
│   │   ├── reporting/                     # Evidence & Assessment Report
│   │   │   ├── report_generator.py        # PDF Assessment Report compiler
│   │   │   └── tamper_evident_hasher.py   # SHA-256 integrity hasher
│   │   └── integration/                   # Government Interoperability
│   │       └── emaap_mock_adapter.py      # eMaap Mock REST sync endpoint
│   └── tests/                             # Automated Test Suite
│       ├── test_rule_engine.py            # 25 synthetic statutory unit tests
│       ├── test_usp_arithmetic.py         # Unit Sale Price math checks
│       ├── test_scale_calibration.py      # Scale recovery accuracy tests
│       └── test_e2e_pipeline.py           # Headless end-to-end integration
├── frontend/                              # Responsive Vite / React PWA
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Viewfinder.tsx             # Camera stream & coin reticle
│   │   │   ├── DeclarationsCard.tsx       # Extracted key-value grid
│   │   │   ├── ComplianceBadge.tsx        # 5-State status badge
│   │   │   ├── EvidenceViewer.tsx         # Side-by-side rectified crops
│   │   │   └── ManualReviewModal.tsx      # 1-Tap officer confirmation
│   │   └── App.tsx                        # Master Layout Shell
└── data/                                  # Benchmark & Ground Truth Storage
    ├── ground_truth_benchmark.json        # 35-SKU Ground Truth Dataset
    └── sample_packages/                   # Layer 2 Demo Fallback Images
```

---

## 13. Acceptance Criteria & Definition of Done

### Feature-Specific Acceptance Criteria:
1. **Metric Scale Recovery:** Recovers standard 10-Rupee coin outer diameter ($27.0\text{mm}$) with scale error $<5.0\%$ at perspective angles up to $15^\circ$.
2. **Local Scene OCR:** Extracts MRP, Net Qty, and Date tokens in $<1,200\text{ms}$ on quad-core CPU with Character Error Rate $<6.0\%$.
3. **USP Arithmetic Auditor:** Detects $100\%$ of synthetic calculation errors exceeding $\pm 1\%$ rounding margin and flags illegal unit denominations.
4. **Font Height Measurement:** Achieves Mean Absolute Error $<0.15\text{mm}$ against 1200 DPI flatbed optical scan ground truth on planar packaging.
5. **Assessment Report Generation:** Renders complete PDF report with SHA-256 hashes and evidence crops in $<500\text{ms}$.
6. **Rule Engine Test Coverage:** Passes $100\%$ of automated unit test cases across Rules 6(1)(a)-(h), 6(11), 7, 8, and 26.

### Project-Wide Definition of Done (DoD):
A feature is marked **DONE** only when:
- Code is implemented with strict Python/TypeScript type annotations.
- Automated unit tests pass locally (`pytest`).
- Verified visually on the responsive mobile web interface.
- Evaluated against physical ground truth on the Phase 2 benchmark set.
- Error states, low-confidence degradation, and fallbacks are verified.
- Operates 100% offline without outbound network calls.
