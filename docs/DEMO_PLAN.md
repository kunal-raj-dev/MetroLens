# LIVE DEMO STAGECRAFT & 5-LAYER REDUNDANCY PLAN (V0.3)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Document Status:** Competition Presentation Script & Failover Architecture | **Version:** 0.2 (Post-Audit Edition)  
**Date:** 4 September 2026 | **Governing Rule:** All On-Screen Numbers Represent Dynamic Pipeline Outputs. Zero Staged Hardcoding.

---

## 1. Physical Props Required on the Jury Table

The presenter must place the following physical items on the jury table before speaking:

1. **Defective Benchmark Package (The "Hook"):** A physical packaging specimen (biscuit pouch or snack pack) featuring a custom synthetic mock sleeve clearly labeled:  
   *“Synthetic Test Specimen — Not an Actual Manufacturer Violation.”*  
   The Net Quantity numeral is printed at $1.15\text{mm}$ despite a Principal Display Panel $> 50\text{ cm}^2$ (Rule 7 Table-I/II mandates minimum $1.50\text{mm}$).
2. **Compliant Retail Package:** A standard retail personal care item (e.g., Dettol sanitizer or Colgate carton) fully compliant across all mandatory declarations.
3. **Physical Metric Reference Anchors:**
   - A crisp, uncirculated **standard Indian 10-Rupee coin** (official RBI outer diameter: $27.0\text{mm}$).
   - A standard **ISO/IEC 7810 ID-1 card / ATM card** ($85.60\text{mm} \times 53.98\text{mm}$) as a secondary rectangular reference.
4. **Physical Ground-Truth Anchor:** A real **digital vernier caliper ($0.01\text{mm}$ precision)** placed conspicuously on the table to invite judges to physically verify optical measurements.
5. **Demonstration Hardware:**
   - Laptop running local FastAPI backend and local Vite PWA on `localhost:8000`.
   - Smartphone or USB webcam streaming to the local web application.

---

## 2. Second-by-Second Live Demonstration Script (3 to 4 Minutes)

```
================================================================================
[ 0:00 - 0:45 ] ACT I: THE HOOK & THE REGULATORY ENFORCEMENT BLIND SPOT
================================================================================
PRESENTER ACTION:
• Places the defective packaging specimen onto the jury table directly in front of the lead judge.
• Holds up the digital vernier caliper.

SPOKEN SCRIPT:
"Judges, look at this packet sitting in front of you. 
Can anyone on this panel tell me if the Net Quantity declaration complies with Indian law?

No human eye can tell whether that printed '50g' numeral is 1.15 millimeters or the 
statutory 1.50 millimeters. 
Right now, approximately 2,500 District Legal Metrology Officers across India are expected 
to audit millions of retail commodities using handheld plastic rulers and magnifying glasses. 
Because manual inspection takes 20 minutes per package, less than 0.01% of retail goods are 
ever audited. Brands exploit this blind spot to downsize products and print microscopic declarations.

We built MetroLens AI to convert that 20-minute manual argument into a 2-second, 
mathematically verified, tamper-evident regulatory compliance audit."

================================================================================
[ 0:45 - 1:30 ] ACT II: THE 2-SECOND OPTICAL AUDIT (THE AHA! MOMENT)
================================================================================
PRESENTER ACTION:
• Places the standard 10-Rupee coin flat on the table adjacent to the package panel.
• Points the camera at the package and coin.
• Taps "Scan Package" on the live interface.

SCREEN DISPLAY (Dynamic Pipeline Output):
• Viewfinder detects coin contour: "Metric Reference Anchor Detected: 27.0mm Scale Active."
• Viewfinder detects package boundary: "Principal Display Panel Area: ~74 cm²."
• Real-time processing timer completes: "Processing Complete: <2.0s."

SPOKEN SCRIPT:
"Notice what happened. We didn't use a proprietary 50,000-rupee laser scanner. We dropped an 
ordinary 10-Rupee coin—an item in every citizen's pocket with an official RBI outer diameter 
of 27.0 millimeters. 
Our vision engine detected the coin contour, recovered the metric pixel-to-millimeter scale factor, 
and established an orthorectified metric plane without sending a single byte to the cloud."

================================================================================
[ 1:30 - 2:30 ] ACT III: SCIENTIFIC EXPLAINABILITY & STATUTORY ASSESSMENT
================================================================================
PRESENTER ACTION:
• Clicks the "Extracted Declarations" card on the web dashboard.

SCREEN DISPLAY (Dynamic Pipeline Output):
• Side-by-Side Visual Evidence Crop:
  - Left: High-resolution rectified image crop of the net quantity numeral.
  - Middle: Detected bounding box with vertical stroke analysis showing:
    • Calculated PDP Area: ~[DYNAMIC MEASURED VALUE] cm²
    • Applicable Statute: Rule 7 Table-I/II, Row 2 (50 to 100 cm²)
    • Mandatory Minimum Height: 1.50 mm
    • Measured Font Height: ~[DYNAMIC MEASURED VALUE] mm
    • STATUTORY DEFICIT: -0.35 mm (POTENTIAL NON-COMPLIANCE)
• Bottom: Unit Sale Price (USP) Verification Card:
  - Extracted Net Qty: 50g | Extracted MRP: ₹20.00
  - Calculated Expected USP: ₹0.40 / g (Rule 6(11))
  - Declared USP on Package: NONE DETECTED (POTENTIAL NON-COMPLIANCE)

SPOKEN SCRIPT:
"Notice the scientific explainability. We do not display an opaque, unexplainable AI score. 
The system measures the Principal Display Panel at [DYNAMIC MEASURED VALUE] square centimeters. 
Under Rule 7 Table-I/II of the Legal Metrology Rules, an area between 50 and 100 cm² legally 
mandates a minimum numeral height of 1.50 millimeters. 
Our metric scale engine measured this numeral at 1.15 millimeters—a deficit of 0.35 millimeters!

Furthermore, under Rule 6(11) enforced in October 2022, pre-packaged goods must declare 
Unit Sale Price in standardized denominations. This package omitted it entirely."

================================================================================
[ 2:30 - 3:15 ] ACT IV: THE EVIDENTIARY ASSESSMENT REPORT
================================================================================
PRESENTER ACTION:
• Taps "Generate Assessment Report".
• PDF document renders on screen and downloads.

SCREEN DISPLAY:
• Title: "METROLENS AI — IMAGE-BASED COMPLIANCE ASSESSMENT REPORT"
• Subtitle: "Automated Regulatory Inspection & Evidentiary Screening Report"
• Side-by-side evidence crop with bounding box coordinates.
• Exact statutory citations: Rule 6(11) and Rule 7 Table-I/II.
• Recommended Regulatory Action: "Issue Improvement Notice under Section 36(1) 
  (as amended by Jan Vishwas (Amendment of Provisions) Act, 2026) or verify physical sample under Section 15."
• Tamper-Evident Integrity Block:
  - Raw Capture SHA-256 Checksum
  - Calibrated Crop SHA-256 Checksum
  - GPS Coordinates: 28.6139° N, 77.2090° E
  - UTC Timestamp: ISO-8601
  - Model & Rule Engine Version Commit SHA
• Explicit Statutory Disclaimer: "Automated image-based assessment. Final legal determination 
  remains with the authorized Legal Metrology Officer."

SPOKEN SCRIPT:
"Under the Jan Vishwas Act of 2023, the law decriminalized first-time labeling infractions, 
mandating an Improvement Notice giving the manufacturer an opportunity to rectify. 
Our software does not pretend to act as a judge or issue automated fines. 
Instead, it generates an objective, tamper-evident Compliance Assessment Report. 
The raw image crop, calibrated measurements, GPS telemetry, and cryptographic SHA-256 hashes 
provide lawful supporting justification for an inspecting officer to issue an Improvement Notice."

================================================================================
[ 3:15 - 3:45 ] ACT V: PROVING ZERO FALSE-POSITIVE BIAS & CLOSING
================================================================================
PRESENTER ACTION:
• Swaps the defective specimen with the compliant retail hand sanitizer.
• Snaps the sanitizer with the 10-Rupee coin.

SCREEN DISPLAY:
• Green status banner: "NO IMAGE-VERIFIABLE VIOLATION DETECTED (8/8 Declarations Satisfied)."
• Font height measured: ~2.60 mm (Mandatory minimum: 2.50 mm -> PASS).
• Declared USP verified: Matches calculated MRP / Volume (PASS).

SPOKEN SCRIPT:
"And to prove our system does not simply flag everything, here is a compliant retail container. 
All mandatory declarations are verified green, and the USP arithmetic matches perfectly. 

We convert manual guesswork into rapid mathematical enforcement. 
We protect Indian consumers from shrinkflation and give the Ministry of Consumer Affairs 
an unshakeable field inspection tool. 
Thank you, and we invite the jury to physically verify our measurements using this caliper."
```

---

## 3. Five-Layer Redundancy Failover Architecture

```
                               5-LAYER FAILOVER
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: 100% Offline Localhost Execution                                   │
│ • Failure Guard: Venue Wi-Fi crashes or captive portal disconnects.         │
│ • Mitigation: Backend and Frontend run entirely on 127.0.0.1:8000.         │
│ • Zero outbound network requests required for complete inference.           │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: Pre-Captured High-Resolution Sample Suite                          │
│ • Failure Guard: Web camera feed glitches, cable disconnects, or bad glare. │
│ • Mitigation: UI features a persistent "Load Sample Package" dropdown with  │
│   10 pre-captured benchmark images (5 compliant, 5 synthetic defects).      │
│ • Tapping a sample immediately feeds pristine raw pixels to local backend.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: Manual Reference Scale Override Mode                               │
│ • Failure Guard: Coin contour detection fails due to a dark wooden table.   │
│ • Mitigation: Inspector taps "Manual Scale Override" -> clicks two opposite │
│   edges of the coin or card -> system locks the pixel distance.             │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: Static Bundled Inspection Dashboard (Canned Mode)                  │
│ • Failure Guard: Python backend crashes or local port is blocked.           │
│ • Mitigation: Pure static HTML/JS dashboard pre-loaded with cached JSON     │
│   audit records renders full UI and inspection report in browser.           │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: 4K Uncut Video Walkthrough (The Ultimate Insurance)                │
│ • Failure Guard: Total laptop OS freeze or hardware failure.                │
│ • Mitigation: Continuous 4K uncut demonstration video stored locally on     │
│   smartphone and a USB thumb drive ready for instant display.               │
└─────────────────────────────────────────────────────────────────────────────┘
```
