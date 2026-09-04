# LIVE DEMO STAGECRAFT & 5-LAYER REDUNDANCY PLAN
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)

This document specifies the second-by-second live stage demonstration script, physical prop requirements, and the 5-layer failover redundancy architecture for InnoHack 3.0 / SIH 2026.

---

## 1. Physical Props Required on the Jury Table

The demonstrator must carry and place the following physical items on the table before the presentation begins:

1. **Defective Test Package (The "Hook"):** A real retail biscuit pouch or snack pack where Net Quantity font is printed at $1.15\text{mm}$ despite a Principal Display Panel $> 50\text{ cm}^2$ (Rule 9 Table 1 mandates minimum $1.50\text{mm}$).
2. **Compliant Standard Package:** A standard retail personal care item (e.g., Dettol hand sanitizer or Colgate toothpaste carton) that is 100% compliant across all declarations.
3. **Physical Metric Reference:** A crisp, uncirculated **standard Indian 10-Rupee coin** (official RBI diameter: strictly $27.0\text{mm}$).
4. **Physical Verification Anchor:** A real **digital vernier caliper (0.01mm resolution)** sitting conspicuously on the table to invite judges to physically verify our optical measurements.
5. **Demonstration Hardware:**
   - Primary: Smartphone or USB webcam connected to demonstrator's laptop.
   - Secondary: Laptop running local FastAPI + Vite frontend on `localhost`.

---

## 2. Minute-by-Minute Live Demo Script (3 to 4 Minutes)

```
================================================================================
[ 0:00 - 0:45 ] ACT I: THE HOOK & THE REGULATORY ENFORCEMENT BLIND SPOT
================================================================================
PRESENTER ACTION:
• Slams the physical biscuit packet onto the jury table directly in front of the lead judge.
• Holds up the digital vernier caliper.

SPOKEN SCRIPT:
"Judges, this packet was purchased yesterday from a retail market. It is being sold 
to millions of consumers right now. 
Can anyone on this panel tell me if the Net Quantity declaration complies with Indian law?

No human eye can tell whether that printed '50g' numeral is 1.2 millimeters or the 
statutory 1.5 millimeters. 
Right now, 2,500 District Legal Metrology Officers across India are expected to audit 
millions of packages by manually squinting with handheld plastic rulers. 
Because manual inspection takes 20 minutes per item, less than 0.01% of retail goods are 
ever checked. Brands hide shrinkflation and print microscopic declarations with total impunity.

We built MetroLens AI to convert that 20-minute manual argument into a 2-second 
indisputable mathematical audit."

================================================================================
[ 0:45 - 1:30 ] ACT II: THE 2-SECOND OPTICAL AUDIT (THE AHA! MOMENT)
================================================================================
PRESENTER ACTION:
• Places the standard 10-Rupee coin flat on the table next to the biscuit packet.
• Points the camera at the packet and coin.
• Taps "Scan Package".

SCREEN DISPLAY:
• Live viewfinder draws a cyan contour around the coin: "Reference Coin Detected: 27.0mm Scale Anchor Active."
• Viewfinder detects package boundary: "Principal Display Panel Area: 72.4 cm²."
• Latency timer stops at: "Processing Complete: 1.68 seconds."

SPOKEN SCRIPT:
"Watch what just happened. We didn't use a proprietary laser scanner. We dropped an 
ordinary 10-Rupee coin—an item sitting in every citizen's pocket with an official 
RBI minting diameter of 27.0 millimeters. 
Our vision engine detected the coin contour, computed the planar homography matrix, 
and rectified perspective tilt into an orthorectified metric plane."

================================================================================
[ 1:30 - 2:30 ] ACT III: THE SCIENTIFIC EXPLAINABILITY & STATUTORY VIOLATION
================================================================================
PRESENTER ACTION:
• Clicks on the "Extracted Declarations" card on the laptop screen.

SCREEN DISPLAY:
• Left: High-resolution rectified image crop of the net quantity numeral.
• Middle: Detected bounding box with vertical stroke analysis showing:
  - PDP Area: 72.4 cm²
  - Applicable Statute: Rule 9 Table 1, Row 2 (50 to 100 cm²)
  - Mandatory Minimum Height: 1.50 mm
  - Measured Font Height: 1.14 mm ± 0.08 mm
  - DEFICIT: -0.36 mm (AMBER/RED STATUTORY VIOLATION)
• Bottom: Unit Sale Price verification:
  - Extracted Net Qty: 50g | Extracted MRP: ₹20.00
  - Expected USP under Rule 6(11): ₹0.40 / g
  - Declared USP on pack: NONE DETECTED (RED STATUTORY VIOLATION)

SPOKEN SCRIPT:
"Notice the scientific explainability. We do not show an opaque AI score. 
The system identifies that the package surface area is 72.4 square centimeters. 
Under Rule 9 Table 1 of the Legal Metrology Rules, an area between 50 and 100 cm² 
legally mandates a minimum numeral height of 1.50 millimeters. 
Our metric homography pipeline measured this numeral at 1.14 millimeters—a deficit of 
0.36 millimeters! 
Furthermore, under the 2021 amendments enforced in October 2022, pre-packaged goods 
must declare Unit Sale Price. This package omitted it entirely."

================================================================================
[ 2:30 - 3:15 ] ACT IV: THE EVIDENTIARY INSPECTION NOTICE (THE HAMMER)
================================================================================
PRESENTER ACTION:
• Taps "Generate Legal Notice".
• A formal PDF document renders instantly on screen and downloads.

SCREEN DISPLAY:
• Title: "FORM A — STATUTORY COMPLIANCE ASSESSMENT REPORT"
• High-res image crop with bounding box coordinates.
• Exact gazetted legal citations: Rule 6(11) and Rule 9 Table 1.
• Recommended Regulatory Action: "Issue Improvement Notice under Section 36(1) 
  (as amended by Jan Vishwas Act, 2023)".
• Audit Chain of Custody:
  - SHA-256 Image Checksum: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b...`
  - GPS Coordinates: 28.6139° N, 77.2090° E (New Delhi)
  - UTC Timestamp: 2026-09-04T10:14:22Z
  - Model Version: PaddleOCR-v4-ONNX-quant

SPOKEN SCRIPT:
"Under the Jan Vishwas Act of 2023, the law decriminalized first-time labeling infractions, 
mandating an Improvement Notice giving the manufacturer an opportunity to rectify. 
Our system generates a tamper-evident Form A report compliant with Section 65B of the 
Indian Evidence Act and Section 63 of Bharatiya Sakshya Adhiniyam, 2023. 
The uncompressed crop, the caliper trace, GPS coordinates, and a cryptographic SHA-256 
hash are permanently sealed. An inspecting officer can sign and issue this in 10 seconds."

================================================================================
[ 3:15 - 3:45 ] ACT V: PROVING ZERO FALSE-POSITIVE BIAS & CLOSING
================================================================================
PRESENTER ACTION:
• Quickly swaps the biscuit pack with the compliant hand sanitizer bottle.
• Snaps the sanitizer with the 10-Rupee coin.

SCREEN DISPLAY:
• Green status banner: "VERIFIED COMPLIANT (8/8 Statutory Declarations Satisfied)."
• Font height measured: 2.62 mm (Mandatory: 2.50 mm -> PASS).
• USP verified: ₹0.50/ml matches calculated MRP/Volume (PASS).

SPOKEN SCRIPT:
"And to prove our system does not simply flag everything, here is a fully compliant 
sanitizer bottle. All 8 statutory declarations are verified green, and the USP arithmetic 
matches perfectly. 
We have converted manual guesswork into rapid mathematical enforcement. 
We protect Indian consumers from shrinkflation and give the Ministry of Consumer Affairs 
an unshakeable enforcement tool. 
Thank you, and we invite you to verify our measurements using this caliper."
```

---

## 3. Five-Layer Redundancy Failover Architecture

Hackathons are unpredictable environments where Wi-Fi crashes, lighting varies, and hardware glitches occur. MetroLens AI implements an automatic **5-layer failover defense**:

```
                              5-LAYER FAILOVER
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: 100% Offline Localhost Execution                                   │
│ • Failure Guard: Venue Wi-Fi dies or captive portal disconnects.            │
│ • Mitigation: Frontend and Backend run entirely on localhost (127.0.0.1).   │
│ • Zero outbound HTTP requests required for inference.                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: Pre-Captured High-Resolution Sample Suite                          │
│ • Failure Guard: Camera feed glitches, USB cable snaps, or severe glare.    │
│ • Mitigation: UI features a persistent "Load Sample Package" dropdown with  │
│   10 pre-captured benchmark images (5 compliant, 5 non-compliant).          │
│ • Tapping a sample immediately feeds raw pristine pixels into local backend.│
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: Manual Reference Scale Override Mode                               │
│ • Failure Guard: Coin contour detector fails due to dark wooden table.      │
│ • Mitigation: Inspector taps "Manual Scale Override" -> clicks two opposite │
│   edges of the coin or an ATM card -> system locks the pixel distance.      │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: Static Bundled Inspection Dashboard (Canned JSON Mode)             │
│ • Failure Guard: Python FastAPI backend crashes or port is blocked.         │
│ • Mitigation: Pure static HTML/JS dashboard pre-loaded with cached JSON     │
│   audit records renders full UI and inspection report in standalone browser.│
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: 4K Uncut Video Walkthrough (The Ultimate Insurance)                │
│ • Failure Guard: Total laptop operating system crash or hardware failure.   │
│ • Mitigation: Pre-recorded 4K uncut continuous demonstration video stored   │
│   locally on demonstrator's smartphone and a USB thumb drive.               │
└─────────────────────────────────────────────────────────────────────────────┘
```
