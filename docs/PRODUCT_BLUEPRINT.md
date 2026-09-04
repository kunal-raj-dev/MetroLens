# MASTER PRODUCT BLUEPRINT & TECHNICAL SPECIFICATION
# MetroLens AI™ — Automated Legal Metrology Inspection & Compliance System
### Sponsoring Ministry: Ministry of Consumer Affairs, Food & Public Distribution | Problem Statement: SIH26034
**Evaluation Framework:** InnoHack 3.0 / Smart India Hackathon 2026 (100 Marks) | **Document Status:** Authoritative Single Source of Truth

---

## 1. Executive Summary

**MetroLens AI™** is an edge-native, perspective-corrected mobile computer vision and regulatory audit system designed for District Legal Metrology Officers (LMOs) and packaging compliance auditors. It transforms a tedious, manual 20-minute ruler-and-magnifier inspection into a **sub-2-second, mathematically verified, tamper-evident regulatory audit**.

By combining a **universally available optical metric anchor** (a standard 10-Rupee coin or ISO card) with **planar homography rectification**, MetroLens AI solves the fundamental monocular scale ambiguity of smartphone cameras. It directly measures statutory numeral heights (Rule 9 Table 1) with sub-0.12mm precision, audits Unit Sale Price (USP) arithmetic against Net Quantity and MRP under Rule 6(11), extracts mandatory declarations across English and Hindi using localized scene text OCR, and verifies compliance through a **100% deterministic statutory state machine**. 

The system operates **entirely offline** without cloud dependency, produces a cryptographically sealed (SHA-256) Form A Inspection Assessment Report under Section 15 of the Legal Metrology Act, 2009 (incorporating the Jan Vishwas Act, 2023 Improvement Notice framework), and provides seamless REST webhook interoperability for the national **eMaap** portal.

---

## 2. Problem Statement & Baseline Realities

### Official Problem Statement (SIH26034)
> *"Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels."*

### Current Operational Workflow Today (The Human Bottleneck)
In India, packaged commodities represent over ₹12 Lakh Crore ($150 Billion) in annual retail trade across millions of Kirana stores and modern supermarkets. Enforcement is entrusted to approximately **2,500 District Legal Metrology Officers (LMOs)** across 780+ districts:
1. **Manual Vernier / Plastic Ruler Auditing:** An officer must physically hold a plastic ruler or micrometer against microscopic print on flexible pouches or curved bottles—a slow, highly contentious, and visually fatiguing procedure.
2. **Inspection Coverage $<0.01\%$:** Due to extreme human resource deficits, over 99.99% of retail packages are never inspected unless a formal consumer grievance is escalated.
3. **Shrinkflation & Deceptive USP:** Brands frequently downsize net weight (e.g., from 100g to 82g) while retaining identical packaging footprints and MRP. While Rule 6(11) mandates Unit Sale Price (e.g., "₹0.61 per g"), brands often omit USP or print it in microscopic 0.5mm fonts hidden within bottom gusset folds.
4. **E-Commerce Wild West:** Online platforms frequently display front-of-pack marketing glamour shots that omit mandatory statutory declarations (country of origin, packer address, manufacturing dates), violating Rule 6(10).

---

## 3. Project Audit: Current State vs. Target State vs. The Gap

### Current State (Repository Baseline)
- **Framework / Runtime:** Python 3.12 / Node.js installed in environment; no application framework scaffolded.
- **Frontend / Backend / Database:** Zero application code, zero active components, zero database migrations.
- **Documentation & Research:** Comprehensive strategic research dossier (91KB, 1,021 lines), InnoHack evaluation rubrics, problem rankings, and official SIH catalogues.
- **Existing Technical Assets:** Homography optical proofs, cylinder generator invariance equations, Rule 9 Table 1 area-proportional matrices, and Gazette citations documented.
- **Technical Debt:** Zero code debt; previous preliminary research contained outdated Section 36 penalty assumptions (corrected via Jan Vishwas Act 2023 audit).

### Target State (The 8–9 Day Working Prototype)
- **Runtime & Deployment:** 100% offline-capable local execution on demonstrator laptop/phone via FastAPI backend and local Vite/React PWA frontend.
- **AI/CV Pipeline:** Local ONNX quantized PaddleOCR v4 mobile engine ($<800\text{ms}$ CPU inference), OpenCV planar homography coin calibration ($<60\text{ms}$), and vertical cylinder generator invariance evaluator.
- **Statutory Engine:** Deterministic, unit-tested Python state machine evaluating Rules 6(1)(a)–(h), 6(10), 6(11), 7, 8, 9 Table 1, and 26.
- **Output & Evidence:** Three-tier result badge (`VERIFIED_COMPLIANT`, `POTENTIAL_NON_COMPLIANCE`, `NEEDS_MANUAL_REVIEW`), side-by-side rectified crop evidence viewer, and downloadable Form A PDF report embedding SHA-256 hashes, GPS coordinates, and ISO-8601 timestamps.
- **Integrations:** National eMaap REST API mock synchronization endpoint and Brand Pre-Flight Artwork Mode.

### The Delta (The Execution Gap)
1. Ingestion & OpenCV Homography Calibration Engine.
2. Local PaddleOCR ONNX Runtime & Text Cropper.
3. Canonical Entity Normalizer (Regex + Constrained SLM).
4. Deterministic Python Statutory Compliance State Machine.
5. Form A PDF Generator with SHA-256 Tamper-Evidence.
6. Responsive Viewfinder PWA with Coin Alignment Guides.
7. Physical 100-Product Benchmark Dataset with Digital Caliper Ground Truth.

---

## 4. Scope Separation: Requirements Classification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ A. OFFICIAL STATUTORY REQUIREMENTS (Strict Problem Statement Baseline)      │
│ • Image ingestion of packaged commodities, labels, and product images.      │
│ • Optical Character Recognition (OCR) of statutory packaging declarations.   │
│ • Rule-based evaluation against Legal Metrology (PC) Rules, 2011.            │
│ • Flagging omissions, non-compliances, and deceptive declarations.          │
│ • Summarized compliance reporting for regulatory enforcement authorities.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ B. ENGINEERING INTERPRETATIONS (Mandated by Technical Feasibility)          │
│ • Physical scale recovery via coplanar metric reference (10-Rupee coin).    │
│ • Perspective rectification via Planar Homography matrix inversion (H^-1).  │
│ • Deterministic mathematical verification of Unit Sale Price (USP) division.│
│ • Area calculation of Principal Display Panel (PDP) to index Rule 9 Table 1.│
│ • Three-tier classification to prevent false regulatory harassment.         │
├─────────────────────────────────────────────────────────────────────────────┤
│ C. OPTIONAL COMPETITIVE EXTENSIONS (High-Scoring Differentiators)            │
│ • Brand Pre-Flight Artwork Mode for pre-printing packaging compliance.      │
│ • E-Commerce listing URL scraper (Playwright) evaluating Rule 6(10)/(10A).   │
│ • REST API adapter for national eMaap portal synchronization.               │
│ • Cryptographic SHA-256 evidentiary chain of custody (Sec 65B Evidence Act).│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Goals & Non-Goals

### Project Goals
1. **Accurate Perception:** Extract statutory packaging declarations with $<4.0\%$ Character Error Rate on local CPU.
2. **Calibrated Physical Measurement:** Measure printed numeral heights with Mean Absolute Error (MAE) $<0.12\text{mm}$ using an Indian 10-Rupee coin anchor.
3. **100% Deterministic Compliance:** Evaluate rules using hardcoded Python state machines—**zero LLM hallucination in legal decisions**.
4. **Sub-2-Second Latency:** Complete full scan-to-verdict pipeline in $<2.0\text{ seconds}$ on standard consumer hardware.
5. **100% Offline Capability:** Execute the entire live demonstration with Wi-Fi and Cellular toggled off.
6. **Defensible Evidentiary Output:** Generate a tamper-evident Form A inspection report adhering to the Jan Vishwas Act 2023 Improvement Notice framework.

### Explicit Non-Goals (What We Will NOT Do)
1. **Physical Weight Verification:** The system will **never** claim to verify whether an unopened pack contains 100g or 80g of physical powder. Monocular cameras cannot weigh items; physical weight requires a physical scale under Rule 24.
2. **Chemical / Ingredient Purity Testing:** Chemical content truth is governed by FSSAI lab testing, not Legal Metrology visual checks.
3. **Physical Factory Verification:** The system verifies the presence and PIN code format of the manufacturer address; it does not physically verify whether a factory building exists.
4. **Issuing Unilateral Legal Penalties:** The software does not act as a judicial magistrate or automatically fine businesses. It provides an evidentiary compliance audit to assist officers.
5. **Complex User Management / Blockchain:** No OAuth2 social logins, payment gateways, or distributed ledger bloat.

---

## 6. Target User Personas & MVP Focus

### Persona 1: Legal Metrology Officer (Primary MVP User)
- **Profile:** Field inspector conducting market surveillance across retail stores, wholesale mandis, and e-commerce dark stores.
- **Pain Points:** Carrying plastic rulers; spending 20 minutes measuring tiny fonts; arguing with shopkeepers; manual paperwork.
- **Needs:** Rapid scanning ($<2\text{s}$); clear red/green violation cards; verifiable font measurements in millimeters; instant PDF inspection reports citing exact Gazette clauses.

### Persona 2: Supervising Controller / Ministry Official (Secondary User)
- **Profile:** State Controller or Ministry Director overseeing statewide compliance trends.
- **Needs:** Audit logs, standardized Form A records, eMaap synchronization, and aggregate market violation analytics.

### Persona 3: FMCG Packaging Designer / Brand Compliance Manager (Secondary User)
- **Profile:** Pre-press packaging manager at an FMCG company reviewing artwork before mass printing.
- **Needs:** Uploading digital artwork (PDF) to verify 100% Legal Metrology compliance prior to committing multi-crore cylinder printing runs.

---

## 7. Product Scope: V0 vs. V1 vs. V2

```
                              PRODUCT SCOPE PHASING
┌─────────────────────────────────────────────────────────────────────────────┐
│ V0: 24-Hour Proof of Concept                                                │
│ • Local Python script reading packaging image + 10-Rupee coin.              │
│ • Basic OpenCV contour detection computing scale factor.                    │
│ • PaddleOCR extracting MRP and Net Quantity text.                           │
│ • Deterministic USP arithmetic division test script.                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ V1: 8–9 Day InnoHack MVP (OUR TARGET BUILD)                                 │
│ • Responsive PWA Viewfinder with real-time coin alignment guides.           │
│ • Planar Homography Rectification eliminating perspective tilt up to 35°.   │
│ • Local quantized PaddleOCR v4 ONNX running on CPU (<800ms).                │
│ • Complete 8-Module Statutory Rule Engine (Rules 6, 7, 8, 9, 11, 26).       │
│ • Side-by-side evidence viewer with calibrated font stroke measurements.    │
│ • Cryptographically signed (SHA-256) Form A PDF Inspection Report.          │
│ • Brand Pre-Flight Artwork Mode + eMaap REST API mock sync.                 │
│ • 100-Product Physical Benchmark Dataset with Caliper Ground Truth.         │
├─────────────────────────────────────────────────────────────────────────────┤
│ V2: National Production Vision (Post-Hackathon)                             │
│ • Distributed microservice mesh deployed on NIC MeghRaj Government Cloud.   │
│ • Automated headless crawling of 500,000 daily listings on Amazon/Blinkit.  │
│ • Real-time API integration with GSTN / MCA21 for instant factory lookup.   │
│ • Native Android APK with camera laser-assisted auto-focus hooks.          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Feature Categorization: MUST / SHOULD / NICE / DO NOT BUILD

### MUST HAVE (Non-Negotiable Core for Day 4)
- Planar homography metric scale calibration via standard 10-Rupee coin.
- Local multilingual OCR (English + Devanagari) extracting MRP, Net Qty, Dates, Contact, Address.
- Deterministic Rule Engine codifying Rules 6(1)(a)–(h), Rule 6(11) USP math, Rule 8 clear space, Rule 9 Table 1, and Rule 26 exemptions.
- Three-tier result classification (`VERIFIED_COMPLIANT`, `POTENTIAL_NON_COMPLIANCE`, `NEEDS_MANUAL_REVIEW`).
- Downloadable Form A PDF inspection report embedding SHA-256 image hashes and GPS metadata.
- 100% offline standalone execution capability.

### SHOULD HAVE (Target for Day 6–7)
- Viewfinder real-time coin contour visualizer and HSV glare pre-check warning.
- Cylinder generator vertical font height invariance module.
- Brand Pre-Flight Artwork Mode (DPI-to-mm verification on digital PDFs).
- E-commerce listing URL scraper (Playwright) evaluating Rule 6(10) declarations.
- eMaap REST API webhook synchronization mock.

### NICE TO HAVE (Day 8 Buffer Only)
- Oblique LED torch assist guidance for transparent / embossed PET bottles.
- Multi-panel inspection mode (aggregating front PDP and back declaration panel).

### DO NOT BUILD (Strategic Distractions That Lose Hackathons)
- **NO Blockchain / Smart Contracts:** Adds zero legal validity in Indian courts; pure buzzword distraction.
- **NO Complex User Authentication:** No OAuth2, Firebase Auth, or JWT user management.
- **NO Custom Neural Network Training from Scratch:** Training custom OCR or detector models in 8 days is suicide. Use pretrained PaddleOCR and YOLOv8-Nano.
- **NO End-to-End LLM Legal Deciders:** Zero LLM calls in the compliance path.
- **NO Native Mobile App Store Packaging:** A responsive PWA is faster to build, test, and demonstrate.

---

## 9. Comprehensive System Architecture

```
                                SYSTEM ARCHITECTURE
                                
  [ Physical Package + 10-Rupee Coin ]       [ Digital Packaging Artwork (PDF) ]
                 │                                           │
                 ▼                                           ▼
      ┌──────────────────────┐                   ┌───────────────────────┐
      │ Mobile PWA Camera    │                   │ Brand Pre-Flight Mode │
      │ Viewfinder (WebRTC)  │                   │ (DPI to mm Converter) │
      └──────────┬───────────┘                   └───────────┬───────────┘
                 │                                           │
                 ▼                                           ▼
      ┌──────────────────────────────────────────────────────────┐
      │ Quality Gate: HSV Glare Pre-Check & Laplacian Blur Filter │
      └──────────────────────────┬───────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌──────────────────────┐       ┌───────────────────────┐
      │ Package & PDP Outer  │       │ Metric Scale Anchor   │
      │ Bounding Box Detector│       │ (OpenCV Coin Contour) │
      │ (YOLOv8-Nano)        │       │ (27.0mm Scale Factor) │
      └──────────┬───────────┘       └───────────┬───────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
      ┌──────────────────────────────────────────────────────────┐
      │ Planar Homography Rectification Engine (OpenCV H^-1)     │
      │ -> Produces Orthorectified Metric Image (Constant mm/px) │
      └──────────────────────────┬───────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌──────────────────────┐       ┌───────────────────────┐
      │ Local Scene OCR      │       │ Physical Measurement  │
      │ (PaddleOCR v4 ONNX)  │       │ (Stroke x-height mm)  │
      └──────────┬───────────┘       └───────────┬───────────┘
                 │ Text Blocks + BBoxes          │ Calibrated Dimensions
                 └───────────────┬───────────────┘
                                 │
                                 ▼
      ┌──────────────────────────────────────────────────────────┐
      │ Canonical Entity Normalizer (Regex + Pydantic Schema)    │
      └──────────────────────────┬───────────────────────────────┘
                                 │ Canonical JSON Entity
                                 ▼
      ┌──────────────────────────────────────────────────────────┐
      │ Deterministic Statutory Compliance Rule Engine (Python)  │
      │ • Rule 6(1)(a-h) Mandatory Declaration Verifier          │
      │ • Rule 6(11) Unit Sale Price Deterministic Math Auditor   │
      │ • Rule 7 & Rule 9 Table 1 PDP Area & Font Height Matrix  │
      │ • Rule 26 Miniature Package Statutory Exemption Switch   │
      └──────────────────────────┬───────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌──────────────────────┐       ┌───────────────────────┐
      │ Three-Tier Result    │       │ Cryptographically     │
      │ Dashboard + Evidence │       │ Signed Form A PDF     │
      │ Side-by-Side Crop    │       │ Notice (SHA-256 Hash) │
      └──────────────────────┘       └───────────┬───────────┘
                                                 │
                                                 ▼
                                     ┌───────────────────────┐
                                     │ National eMaap REST   │
                                     │ Webhook Sync Adapter  │
                                     └───────────────────────┘
```

### Architectural Layer Breakdown:

| Layer | Responsibility | Input | Output | Technology / Algorithm | Fallback Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Ingestion & Quality** | Camera stream capture, glare detection, blur assessment | Camera frames | Validated RGB frame | OpenCV HSV saturation check ($V>250$), Laplacian variance | Viewfinder warning: "Tilt camera to avoid glare" |
| **2. Metric Calibration** | Scale factor recovery & tilt elimination | RGB frame | Scale factor $S$ (mm/px) + Homography $H$ | OpenCV `findContours`, ellipse fit, `findHomography` | Manual reference override (click 2 points) |
| **3. Detection & Rectification** | Packaging boundary segmentation & projective unwarping | Frame + $H$ | Orthorectified metric image | YOLOv8-Nano + OpenCV `warpPerspective` | Full image bounding box preset |
| **4. Scene Text OCR** | Multilingual text detection & recognition | Rectified image | Text lines, bboxes, confidence | PaddleOCR v4 Mobile (ONNX int8) | Local Tesseract 5 hot-swap |
| **5. Entity Normalizer** | Map raw text strings to legal schema | OCR text lines | `CanonicalPackagingDeclaration` | Regex normalizers + Pydantic | Constrained Gemini 1.5 Flash parser |
| **6. Geometric Measurement** | Measure numeral capital height in mm | Binary text crop | Font height $h$ (mm) | Morphological stroke-width contour analysis | Bounding box height $\times S$ |
| **7. Statutory Rule Engine** | Deterministic legal & arithmetic evaluation | Canonical JSON + mm | Violation list, compliance status | Python Statutory State Machine | Safe failure: "Needs Manual Officer Review" |
| **8. Evidence & Reporting** | Cryptographic sealing & PDF generation | Violations + metadata | Form A PDF + SHA-256 | ReportLab / Weasyprint + Python `hashlib` | JSON export in UI |

---

## 10. AI vs. Deterministic Architecture: The Four Pillars

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AI PERCEIVES (Probabilistic Domain)                                      │
│ • Technology: PaddleOCR v4 (DBNet++ text detection, SVTR text recognition). │
│ • Role: Converts messy raw packaging pixels into character strings.         │
│ • Boundary: AI never decides if the extracted text is legal.                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MATH VALIDATES (Empirical Domain)                                        │
│ • Technology: OpenCV Planar Homography Matrix ($H^{-1}$) & Float Division.  │
│ • Role: Recovers physical millimeters; calculates $\text{MRP}/\text{Qty}$.  │
│ • Boundary: Zero heuristic rounding; strict IEEE 754 precision ($\pm 1\%$). │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. RULES DECIDE (Deterministic Statutory Domain)                            │
│ • Technology: Versioned Python State Machine (`modules/rules/`).            │
│ • Role: Codifies Gazette clauses, Table 1 thresholds, and exemptions.       │
│ • Boundary: 100% deterministic, audit-traceable, and versioned.             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HUMANS HANDLE UNCERTAINTY (Regulatory Governance)                        │
│ • Technology: Three-tier compliance classification & Manual Review UI.     │
│ • Role: Inspecting officer reviews borderline cases ($1.40\text{–}1.50$mm). │
│ • Boundary: System assists officers; human officer signs the legal notice.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Physical Measurement Pipeline & Optical Proofs

### The Monocular Scale Proof
A camera projects real-world metric dimensions $X$ at distance $Z$ onto sensor pixels $u$ via:
$$u = f \cdot \frac{X}{Z}$$
Without a known scale reference or physical depth $Z$, absolute metric measurement is impossible.

### The Standard Indian Currency Anchor
An Indian 10-Rupee coin is officially minted by the Reserve Bank of India with an outer diameter strictly equal to **$27.0\text{mm}$** ($\pm 0.05\text{mm}$ minting tolerance).
1. The pipeline identifies the coin contour in the image plane using `cv2.findContours` and fits an ellipse parameterized by major axis $d_{\text{major}}$ and minor axis $d_{\text{minor}}$ in pixels.
2. It computes the metric scale factor $S$:
   $$S = \frac{27.0\text{ mm}}{d_{\text{major}}} \quad (\text{mm/pixel})$$
3. Because perspective inclination angle $\theta$ compresses dimensions along the tilt axis by $\cos\theta = \frac{d_{\text{minor}}}{d_{\text{major}}}$, the homography matrix $H$ rotates the plane back to normal incidence ($\theta = 0^\circ$), yielding an orthorectified image where $1\text{ pixel} \equiv S\text{ millimeters}$ uniformly in all directions.

### The Cylinder Vertical Generator Invariance Proof
A cylindrical container (can, bottle) has 3D coordinates $\mathbf{P}(\phi, y) = (R\cos\phi, y, R\sin\phi)$.
- Along the circumferential axis ($X$), surface distance $R\Delta\phi$ projects to image width $w_{\text{proj}} \approx R\Delta\phi\cos\phi$ (heavily compressed near the edges).
- Along the vertical generator line ($Y$), the generator line is parallel to the cylinder axis:
  $$y_{\text{proj}} = y_{\text{actual}}$$
- **Statutory Impact:** Rule 9 font height is strictly measured along the **vertical axis** (numeral capital height / ascender-descender height). Therefore, cylindrical curvature introduces **ZERO vertical foreshortening**. Text stroke heights measured along the vertical generator line require zero cylindrical unwarping!

---

## 12. Statutory Compliance Rule Engine Specification

### Data Model (`CanonicalPackagingDeclaration`)
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class UnitType(str, Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    METER = "m"
    NUMBER = "N"
    PIECE = "piece"

class CanonicalDeclaration(BaseModel):
    mrp: Optional[float] = Field(None, description="Maximum retail price in INR")
    tax_qualifier_present: bool = Field(False, description="Presence of 'inclusive of all taxes'")
    net_quantity: Optional[float] = Field(None, description="Numerical net quantity")
    net_quantity_unit: Optional[UnitType] = Field(None, description="SI unit symbol")
    declared_usp: Optional[float] = Field(None, description="Declared Unit Sale Price in INR")
    declared_usp_unit: Optional[str] = Field(None, description="Unit string (e.g. per g, per ml)")
    mfg_month: Optional[int] = Field(None, description="1-12")
    mfg_year: Optional[int] = Field(None, description="Four digit year")
    manufacturer_name: Optional[str] = None
    manufacturer_pincode: Optional[str] = None
    consumer_care_phone: Optional[str] = None
    consumer_care_email: Optional[str] = None
    country_of_origin: Optional[str] = None
    pdp_area_sqcm: Optional[float] = Field(None, description="Measured PDP area in cm^2")
    measured_font_height_mm: Optional[float] = Field(None, description="Measured numeral height in mm")
    is_medical_device: bool = False
    is_electronic_product: bool = False
    qr_code_present: bool = False
```

### Rule Execution Flow:
1. **Rule 26 Check:** If `net_quantity` $\le 10\text{g}$ or $\le 10\text{ml}$ (non-tobacco), flag as `EXEMPT_RULE_26`, approve, and exit.
2. **Rule 6(1)(e) MRP Check:** Verify `mrp > 0` and `tax_qualifier_present == True`.
3. **Rule 6(1)(c) Net Qty Check:** Verify `net_quantity_unit` in approved SI units; flag non-standard notations (`Gms`, `ML`).
4. **Rule 6(11) USP Arithmetic Audit:**
   - If `net_quantity` $> 1\text{ unit/kg/L}$: calculate $\text{Expected USP} = \frac{\text{mrp}}{\text{net\_quantity}}$.
   - Verify $|\text{declared\_usp} - \text{Expected USP}| / \text{Expected USP} \le 0.01$.
5. **Rule 7 & 9 Table 1 Font Height Check:**
   - Lookup statutory minimum font height $h_{\text{min}}$ from Table 1 using `pdp_area_sqcm`.
   - If `measured_font_height_mm` $< (h_{\text{min}} - 0.10\text{mm})$: Flag **DEFICIT VIOLATION**.
   - If $(h_{\text{min}} - 0.10) \le \text{measured} < h_{\text{min}}$: Flag **NEEDS_MANUAL_REVIEW**.
6. **Rule 6(1)(g) Consumer Care Check:** Verify presence of valid telephone regex and RFC 5322 email regex.

---

## 13. Three-Tier Compliance Result Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. VERIFIED COMPLIANT (Green)                                               │
│ • All mandatory declarations present and syntactically valid.               │
│ • Measured font heights meet or exceed Rule 9 Table 1 minimums.             │
│ • Declared USP matches calculated MRP / Net Quantity within 1% tolerance.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. POTENTIAL NON-COMPLIANCE (Red)                                           │
│ • Omission of mandatory declaration (missing USP, MRP, or contact details). │
│ • Severe font size deficit (measured height < statutory minimum - 0.10mm).  │
│ • Arithmetic USP discrepancy (> 1% rounding error).                         │
│ • Prohibited non-metric units ("Gms", "Kgs").                               │
│ • Recommended Action: Issue Improvement Notice under Section 36(1).         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. NEEDS MANUAL REVIEW (Amber)                                              │
│ • OCR confidence on critical field falls between 60% and 80%.               │
│ • Measured font height is borderline (within 0.10mm tolerance buffer).      │
│ • Address present but PIN code format ambiguous.                            │
│ • Action: Inspector visual crop verification via 1-tap confirmation UI.    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 14. Evidence Model & Tamper-Evident Reporting

Under Section 65B of the Indian Evidence Act / Section 63 of Bharatiya Sakshya Adhiniyam, 2023, electronic evidence requires verifiable integrity:

```json
{
  "inspection_id": "INSP-2026-DEL-04921",
  "utc_timestamp": "2026-09-04T10:14:22.841Z",
  "device_telemetry": {
    "gps_latitude": 28.6139,
    "gps_longitude": 77.2090,
    "device_fingerprint": "LMO-TAB-DELHI-04"
  },
  "cryptographic_hashes": {
    "raw_image_sha256": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "rectified_crop_sha256": "8a35e612f17094b80e8f39572458f334a1796d11f8e1329c3629393963496924",
    "composite_record_sha256": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
  },
  "pipeline_versions": {
    "ocr_engine": "PaddleOCR-v4-Mobile-ONNX-int8",
    "rule_engine_version": "2026.09-JanVishwas-rev3"
  }
}
```

The generated **Form A Inspection Assessment Report** is rendered as a clean, multi-page PDF embedding:
1. Sponsoring Ministry Banner (Ministry of Consumer Affairs, Food & Public Distribution).
2. Inspection Metadata (Officer ID, GPS, Timestamp, Store Location).
3. Side-by-Side Visual Evidence Crop (Raw image, rectified crop, bounding box overlay).
4. Statutory Violation Table (Applicable Rule, Statutory Mandate, Measured Value, Deficit).
5. Recommended Legal Action (Improvement Notice under Section 36(1) as amended by Jan Vishwas Act 2023).
6. Cryptographic Verification Seal & QR Code linking to local audit hash.

---

## 15. UX / UI Specification: 8-Screen Inspector Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 1: Home / Market Surveillance Portal                                 │
│ • Actions: "Start New Field Inspection", "Brand Pre-Flight Mode", "eMaap"   │
│ • Displays: Quick stats (Inspections today, compliance rate, recent notices)│
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 2: Real-Time Viewfinder & Coin Alignment                             │
│ • Viewfinder: Full-screen camera stream with circular cyan targeting reticle│
│ • Guidance: "Place 10-Rupee Coin next to package panel"                     │
│ • Quality Indicators: Glare alert badge, focus indicator, resolution meter  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 3: Processing & Rectification (Latency Bar)                          │
│ • Animated radar pulse with real-time latency timer (<2.0s countdown)       │
│ • Step Tracker: [Coin Detected] -> [Homography] -> [OCR] -> [Rule Audit]    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 4: Extracted Declarations Card                                       │
│ • Clean key-value grid displaying extracted MRP, Net Qty, Dates, Contact    │
│ • Confidence pill tags: Green (>90%), Amber (70-90%), Red (<70%)            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 5: Statutory Compliance Verdict                                      │
│ • Large status banner: VERIFIED COMPLIANT / POTENTIAL NON-COMPLIANCE        │
│ • Metric card: Measured PDP Area (cm²) vs. Minimum Font Height Required     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 6: Visual Evidence & Font Deficit Viewer                             │
│ • Interactive zoom-in on the exact offending text crop                      │
│ • Calibrated millimeter ruler overlay showing measured height vs statutory  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 7: Officer Review & Confirmation (Human in the Loop)                 │
│ • 1-tap confirmation toggles for ambiguous fields                           │
│ • Officer signature canvas and notes field                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Screen 8: Form A Inspection Report & eMaap Sync                             │
│ • In-app PDF preview with 1-click "Download Legal Notice"                   │
│ • "Sync to National eMaap Database" webhook button with confirmation toast  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Design System Tokens (Professional Government Inspection Aesthetic)
- **Palette:** Deep Navy (`#0F172A`), Slate (`#1E293B`), Government Blue (`#1D4ED8`), Compliant Emerald (`#059669`), Non-Compliant Crimson (`#DC2626`), Review Amber (`#D97706`).
- **Typography:** Inter / Outfit (Clean, legible, modern geometric sans-serif).
- **Styling:** Glassmorphism accents, crisp hairline borders (`1px solid rgba(255,255,255,0.1)`), high-contrast accessibility (WCAG AAA compliant).

---

## 16. Traceability Matrix: From Official PS to Judging Marks

| Official PS Requirement | Product Feature | Technical Implementation | Unit / Benchmark Test | Live Demo Moment | InnoHack Scoring Criterion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **"Scanning products, images and labels"** | Mobile Viewfinder + Glare Guard | WebRTC camera stream + OpenCV HSV glare check | `test_glare_precheck.py` | Dropping 10-Rupee coin and snapping packet | **UX (10/10) & Feasibility (20/20)** |
| **"Extract statutory declarations"** | Multilingual Scene Text OCR | Local PaddleOCR v4 ONNX (English + Devanagari) | `test_ocr_accuracy.py` (CER $<4\%$) | Instant bounding box render in $<2\text{s}$ | **Technical Feasibility (20/20)** |
| **"Check font size compliance"** | Metric Homography Font Engine | $27.0\text{mm}$ coin contour anchor + Planar Homography ($H^{-1}$) | `test_homography_mae.py` (MAE $<0.12\text{mm}$) | Screen showing $1.14\text{mm}$ vs $1.50\text{mm}$ deficit | **Innovation & Creativity (20/20)** |
| **"Check mandatory rules (USP/MRP)"** | Deterministic Statutory State Machine | Python rule classes + IEEE 754 float division | `test_usp_arithmetic.py` ($100\%$ pass) | Flagging omitted USP on biscuit pouch | **Problem Solving (15/15)** |
| **"Curved packaging handling"** | Cylinder Generator Invariance Module | Vertical axis coordinate projection lock | `test_cylinder_invariance.py` | Scanning curved beverage can live | **Innovation (20/20) & Feasibility** |
| **"Summarizing compliance for Ministry"** | Cryptographic Form A PDF Generator | ReportLab generator with SHA-256 image hashes | `test_pdf_hash_integrity.py` | 1-click generation of official notice | **Prototype / Implementation (15/15)** |
| **"Field usability in retail stores"** | 100% Offline Localhost Execution | Local ONNX runtime + SQLite local database | `test_offline_pipeline.py` | Demonstrating with Wi-Fi & Cellular OFF | **Presentation & Q&A (10/10)** |
| **"Integration with Government ERP"** | eMaap REST API Webhook Adapter | FastAPI mock synchronization endpoint | `test_emaap_sync.py` | Showing eMaap sync dashboard update | **Scalability (10/10)** |

---

## 17. Acceptance Criteria & Definition of Done

### Measurable Feature Acceptance Criteria:
1. **Coin Scale Recovery:** Detects standard 10-Rupee coin diameter ($27.0\text{mm}$) with error $<4.0\%$ at perspective angles up to $30^\circ$.
2. **Local OCR Latency & Accuracy:** Extracts MRP and Net Qty tokens in $<1,000\text{ms}$ on quad-core CPU with Character Error Rate $<4.0\%$.
3. **USP Arithmetic Auditor:** Correctly identifies $100\%$ of synthetic mathematical rounding errors exceeding $1\%$.
4. **Font Height Accuracy:** Achieves Mean Absolute Error $<0.12\text{mm}$ against digital vernier caliper ground truth on planar retail cartons.
5. **Form A PDF Generation:** Compiles and renders complete PDF with SHA-256 hash in $<400\text{ms}$.
6. **Rule Engine Coverage:** Passes $100\%$ of test cases across Rules 6(1)(a)–(h), 6(10), 6(11), 7, 8, 9, and 26.

### Project-Wide Definition of Done (DoD):
A feature is considered **DONE** only when:
- Code is implemented and strictly formatted with type annotations.
- Automated unit tests pass locally (`pytest`).
- Verified visually on the mobile PWA interface.
- Evaluated against physical ground truth on the 100-package benchmark.
- Error states and low-confidence fallbacks are verified.
- Documented in the architecture records and works in the 100% offline demonstration environment.

---

## 18. Proposed Repository Architecture

```
SIH26034_MetroLens_AI/
├── docs/                                  # Project Documentation Suite
│   ├── PRODUCT_BLUEPRINT.md               # Master Single Source of Truth
│   ├── LEGAL_RULE_MATRIX.md               # Statutory Rules & Jan Vishwas Matrix
│   ├── TECHNICAL_DECISIONS.md             # Architecture Decision Records (ADRs)
│   ├── DATA_AND_BENCHMARK_PLAN.md         # Caliper Protocol & Metrics
│   ├── DEMO_PLAN.md                       # Live Pitch Script & Failover
│   ├── RISK_REGISTER.md                   # 15 Risks & 48-Hour Kill Switch
│   └── JURY_QA.md                         # 32 Adversarial Questions & Defenses
├── backend/                               # Python FastAPI Backend
│   ├── main.py                            # Application Entry Point
│   ├── requirements.txt                   # Dependency Specification
│   ├── modules/
│   │   ├── cv/                            # Computer Vision & Calibration
│   │   │   ├── scale_calibration.py       # Coin contour detection & scale factor
│   │   │   ├── homography_rectifier.py    # Planar homography matrix inversion
│   │   │   ├── glare_precheck.py          # HSV saturation mask detector
│   │   │   ├── cylinder_invariance.py     # Vertical generator height logic
│   │   │   └── pdp_detector.py            # Packaging boundary & area estimator
│   │   ├── ocr/                           # Multilingual Scene Text OCR
│   │   │   ├── paddle_onnx_engine.py      # Local quantized ONNX runtime
│   │   │   ├── text_cropper.py            # Word & line bounding box slicer
│   │   │   └── hindi_normalizer.py        # Devanagari phrase mapping
│   │   ├── normalizer/                    # Entity Structuring
│   │   │   ├── entity_parser.py           # Regex key-value extractor
│   │   │   └── schemas.py                 # Pydantic Canonical Declaration Schemas
│   │   ├── rules/                         # Deterministic Statutory Rule Engine
│   │   │   ├── base_rule.py               # Abstract Rule Interface
│   │   │   ├── rule_6_declarations.py     # Rule 6(1)(a)-(h) mandatory checks
│   │   │   ├── rule_6_11_usp.py           # Unit Sale Price arithmetic auditor
│   │   │   ├── rule_9_font_matrix.py      # Rule 9 Table 1 area-to-font lookup
│   │   │   ├── rule_26_exemptions.py      # Miniature commodity exemption switch
│   │   │   └── rule_engine.py             # Master Compliance Evaluator
│   │   ├── reporting/                     # Evidence & PDF Generator
│   │   │   ├── form_a_generator.py        # Statutory inspection PDF builder
│   │   │   └── hasher.py                  # SHA-256 cryptographic audit sealer
│   │   └── integration/                   # Government & External Adapters
│   │       ├── emaap_adapter.py           # National eMaap REST webhook mock
│   │       └── ecommerce_scraper.py       # Playwright Amazon/Blinkit parser
│   └── tests/                             # Automated Test Suite
│       ├── test_calibration.py            # Homography accuracy tests
│       ├── test_rule_engine.py            # Statutory compliance unit tests
│       └── test_e2e_pipeline.py           # End-to-end integration tests
├── frontend/                              # Responsive Vite + React PWA
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Viewfinder.jsx             # Camera stream with coin reticle
│   │   │   ├── DeclarationGrid.jsx        # Extracted entity key-value cards
│   │   │   ├── ComplianceBadge.jsx        # Three-tier verdict banner
│   │   │   ├── EvidenceViewer.jsx         # Zoom-in rectified crop visualizer
│   │   │   ├── PreFlightPortal.jsx        # Digital artwork PDF upload tab
│   │   │   └── EmaapSyncModal.jsx         # Government sync modal
│   │   ├── styles/
│   │   │   └── tokens.css                 # Government aesthetic CSS variables
│   │   └── App.jsx                        # Master 8-screen state controller
├── data/                                  # Benchmark & Ground Truth
│   ├── ground_truth_benchmark_100.json    # Caliper measurements for 100 SKUs
│   ├── sample_images/                     # Pre-captured sample suite for demo
│   └── gazette_rules/                     # PDF copies of official amendments
└── scripts/                               # Automation & Evaluation Utilities
    ├── run_benchmark.py                   # Computes CER, WER, MAE, F1
    └── package_offline_bundle.py          # Builds standalone USB offline bundle
```

---

## 19. Final Architecture Recommendation & Fallback Strategy

### The Recommended Architecture (Primary Path)
- **Perception:** Localhost FastAPI server running **PaddleOCR v4 ONNX (int8 quantized)** on laptop CPU.
- **Calibration:** Standard **Indian 10-Rupee coin ($27.0\text{mm}$)** with OpenCV Planar Homography ($H^{-1}$).
- **Logic:** **Deterministic Python Statutory State Machine** enforcing Jan Vishwas Act 2023 Improvement Notices.
- **Client:** **Vite + React PWA** running locally and accessed via laptop browser or local Wi-Fi hotspot on smartphone.
- **Evidence:** **ReportLab Form A PDF** with SHA-256 raw image hashes and GPS coordinates.

### The Fallback Architecture (If Primary Fails)
- **If Coin Contour Fails:** Manual 2-Point Reference Mode (Inspector taps 2 corners of an ATM card or coin in UI to lock scale).
- **If ONNX Runtime Fails:** Hot-swap to local **Tesseract 5** OCR engine with CLAHE binarization.
- **If Curved Cylinder Distorts:** Restrict measurement to planar box packaging and use central vertical generator lock for cans.
- **If Backend Server Crashes:** Standalone static HTML/JS dashboard pre-loaded with cached inspection JSON records.
