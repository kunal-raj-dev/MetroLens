# RESEARCH EVIDENCE PACK D — PRIOR ART & EXISTING SYSTEMS REGISTER

**Research Scope:** Commercial, Industrial, and Academic Systems in Packaging Compliance, OCR, and Legal Metrology  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Objective Evidence-Based Framing (Mandatory Rule: *"Not identified in reviewed sources"*)  
**Pack Status:** 🔴 CRITICAL (Verified Secondary & Public Industry Records)

---

## 1. Executive Summary & Differentiation Analysis

This audit catalogs 10 distinct systems across government portals, packaging pre-print proofreading tools, industrial conveyor-belt machine vision platforms, and regulatory compliance consulting tools.

### Key Differentiation Finding:
> *In the reviewed systems cataloged below, we did not identify solutions combining physical scale calibration (planar homography for consumer cameras), 3D multi-panel packaging correlation, non-retroactive multi-epoch statutory rule versioning for Indian Legal Metrology, and Section 63 BSA 2023 tamper-evident cryptographic provenance graphs in a single offline-capable mobile inspection platform.*

---

## 2. Comprehensive Prior Art System Records

### 2.1 System 1: eMaap (National Legal Metrology Portal)
- **Name:** eMaap Portal
- **Company / Organization:** Department of Consumer Affairs, Ministry of Consumer Affairs, Food & Public Distribution, Government of India
- **URL:** `https://emaap.gov.in/`
- **Product / Version:** Production Web Portal (v2.x)
- **Input:** Web form text entries, scanned PDF registration documents, fee payments.
- **Capabilities:** Online registration of packaged commodities under Rule 27, importer certificates, model approval tracking, license renewals, digital records of enforcement compounding.
- **Limitations:** Portal for bureaucratic licensing and statutory registrations; **does not perform automated optical scanning, image analysis, font measurement, or label OCR of physical packaging**.
- **Physical Measurement:** No.
- **Multi-Panel Correlation:** No.
- **Regulatory Versioning:** Administrative workflow only; no automated temporal rule engine.
- **Offline Capable:** No (Web portal requiring continuous broadband connection).
- **Evidence Provenance:** Centralized database audit logs.
- **Human Review:** Yes (Government officers review applications).
- **Source Date:** 2024–2026.

---

### 2.2 System 2: Artwork Flow
- **Name:** Artwork Flow
- **Company / Organization:** Bizongo (India / USA)
- **URL:** `https://www.artworkflow.com/`
- **Product / Version:** Cloud SaaS Platform
- **Input:** Digital vector packaging artwork files (Adobe Illustrator `.ai`, `.pdf`).
- **Capabilities:** Digital pre-print proofreading, vector text extraction, font size validation, color separation checks, regulatory checklist workflows for FMCG brands.
- **Limitations:** Designed exclusively for **digital artwork prior to printing**; cannot process photographed physical packaging with lens distortions, perspective skew, folds, or glare in field retail environments.
- **Physical Measurement:** Analyzes digital vector points (`pt`), not physical millimeter scale from camera lenses.
- **Multi-Panel Correlation:** Flat 2D artboard review only.
- **Regulatory Versioning:** Configurable checklists; no automated statutory epoch resolution.
- **Offline Capable:** No (Cloud SaaS).
- **Evidence Provenance:** SaaS activity log.
- **Human Review:** Yes (Brand packaging teams).
- **Source Date:** 2024.

---

### 2.3 System 3: GlobalVision
- **Name:** GlobalVision Quality Inspection Platform
- **Company / Organization:** GlobalVision Inc. (Canada)
- **URL:** `https://www.globalvision.co/`
- **Product / Version:** Desktop & Web Proofreading Suite
- **Input:** High-resolution digital artwork files and calibrated flatbed scanner images.
- **Capabilities:** Pixel-by-pixel text, graphic, barcode, and Braille inspection; compares printed samples against approved digital master proofs.
- **Limitations:** Requires **flatbed document scanners or high-end industrial camera stands**; requires an "approved master proof" to compare against; cannot evaluate uncurated field packages against open-ended statutory law without a master file.
- **Physical Measurement:** Scanner DPI-based measurement.
- **Multi-Panel Correlation:** Limited to stitched flat scans.
- **Regulatory Versioning:** Not identified in reviewed sources.
- **Offline Capable:** Desktop installation available.
- **Evidence Provenance:** PDF audit trail for FDA 21 CFR Part 11.
- **Human Review:** Yes (Operator review).
- **Source Date:** 2023–2024.

---

### 2.4 System 4: Cognex In-Sight Vision Systems
- **Name:** In-Sight Explorer / In-Sight 2800 / 3800
- **Company / Organization:** Cognex Corporation (USA)
- **URL:** `https://www.cognex.com/`
- **Product / Version:** In-Sight Software v6.x / Edge Learning OCR
- **Input:** High-speed industrial camera video streams on factory conveyor lines.
- **Capabilities:** High-speed optical character recognition (OCR), 1D/2D barcode grading, date/lot code presence check, packaging seal inspection at $> 500$ parts per minute.
- **Limitations:** Designed for fixed factory automation with **controlled strobe lighting and fixed camera geometry**; does not support dynamic smartphone captures, Indian Legal Metrology Table-I font height validation, or non-retroactive statutory rule evaluation.
- **Physical Measurement:** Calibrated fixed-focal length camera grid calibration.
- **Multi-Panel Correlation:** Requires multiple physical cameras positioned around conveyor.
- **Regulatory Versioning:** Not identified in reviewed sources.
- **Offline Capable:** Yes (On-premise edge vision smart cameras).
- **Evidence Provenance:** Industrial PLC logs.
- **Human Review:** Exception reject bin only.
- **Source Date:** 2023–2024.

---

### 2.5 System 5: Keyence CV-X / XG-X Series
- **Name:** CV-X / XG-X Series Vision Systems
- **Company / Organization:** Keyence Corporation (Japan)
- **URL:** `https://www.keyence.com/`
- **Product / Version:** Vision Controller Firmware & Terminal
- **Input:** Multi-camera industrial CMOS image sensors.
- **Capabilities:** Industrial dimension measurement, edge detection, OCR, color verification, surface flaw detection.
- **Limitations:** Heavy capital expenditure hardware; intended for manufacturing plant QA lines; cannot be carried by a Legal Metrology officer into a retail grocery store or rural warehouse.
- **Physical Measurement:** Factory telecentric lens calibration down to micrometers.
- **Multi-Panel Correlation:** Multi-camera hardware synchronization.
- **Regulatory Versioning:** Not identified in reviewed sources.
- **Offline Capable:** Yes (Closed embedded controller).
- **Evidence Provenance:** Proprietary log export.
- **Human Review:** Hardware operator interface.
- **Source Date:** 2023–2024.

---

### 2.6 System 6: EyeC Proofiler
- **Name:** EyeC Proofiler Graphic & Print
- **Company / Organization:** EyeC GmbH (Germany)
- **URL:** `https://www.eyec-inspection.com/`
- **Product / Version:** Proofiler Software v4.x
- **Input:** High-resolution optical scanner and camera captures.
- **Capabilities:** Print quality verification for pharmaceutical and folding carton packaging; 100% inspection of print defects, missing text, color variance.
- **Limitations:** Pharmaceutical print verification focus; relies on master file comparison; no Legal Metrology Act rule engine.
- **Physical Measurement:** Scanner DPI calibration.
- **Multi-Panel Correlation:** Flat sheet scans.
- **Regulatory Versioning:** Not identified in reviewed sources.
- **Offline Capable:** Yes.
- **Evidence Provenance:** Audit trail compliant with pharmaceutical regulations.
- **Human Review:** Yes.
- **Source Date:** 2023.

---

### 2.7 System 7: OpenFoodFacts
- **Name:** OpenFoodFacts Scanner & Database
- **Company / Organization:** Open Food Facts Non-Profit (France / Global)
- **URL:** `https://world.openfoodfacts.org/`
- **Product / Version:** Mobile App & Open Web API
- **Input:** Smartphone photo of barcode and ingredients label.
- **Capabilities:** Barcode lookup, ingredient list extraction, Nutri-Score calculation, crowdsourced public product database.
- **Limitations:** Focuses on **nutritional consumer awareness**, not statutory compliance; does not measure font heights, verify MRP / USP mathematical ratios, or generate evidentiary dossiers for enforcement.
- **Physical Measurement:** No.
- **Multi-Panel Correlation:** Photos stored as unordered gallery.
- **Regulatory Versioning:** No.
- **Offline Capable:** Limited (Requires API for database lookup).
- **Evidence Provenance:** Open crowdsourced history (no cryptographic chain).
- **Human Review:** Crowdsourced community edits.
- **Source Date:** 2024.

---

### 2.8 System 8: Omron Microscan (LVS-7510)
- **Name:** LVS-7510 Print Quality Inspection System
- **Company / Organization:** Omron Corporation
- **URL:** `https://www.microscan.com/`
- **Product / Version:** Print Verification Engine
- **Input:** Thermal transfer and ink-jet label printer web stream.
- **Capabilities:** ISO/IEC 15415/15416 barcode grading, OCR/OCV verification, label defect detection directly on label printers.
- **Limitations:** Pre-application label printer accessory; cannot inspect packaged commodities already distributed in the field.
- **Physical Measurement:** Printer head DPI.
- **Multi-Panel Correlation:** Single label strip.
- **Regulatory Versioning:** Not identified in reviewed sources.
- **Offline Capable:** Yes.
- **Evidence Provenance:** Printer batch log.
- **Human Review:** Operator alert on bad print.
- **Source Date:** 2023.

---

### 2.9 System 9: Vincular / Corpbiz Compliance Platforms
- **Name:** Regulatory Advisory & Packaging Services
- **Company / Organization:** Vincular Solutions / Corpbiz Advisors (India)
- **URL:** `https://vincular.in/`, `https://corpbiz.net/`
- **Product / Version:** Professional Consulting Services
- **Input:** Customer artwork PDFs and physical product samples mailed to office.
- **Capabilities:** Manual legal review by human lawyers/consultants; filing applications on eMaap portal; advisory on Table-I font sizes.
- **Limitations:** Manual, human-intensive consulting services with turnaround times of days or weeks; **no automated computer vision inspection software**.
- **Physical Measurement:** Manual measurement by consultants using rulers / calipers.
- **Multi-Panel Correlation:** Manual human inspection.
- **Regulatory Versioning:** Dependent on lawyer knowledge.
- **Offline Capable:** N/A (Consulting firm).
- **Evidence Provenance:** Signed legal opinion letters.
- **Human Review:** 100% human labor.
- **Source Date:** 2024.

---

### 2.10 System 10: Loftware Enterprise Labeling (Smartflow)
- **Name:** Loftware Enterprise Labeling & Packaging Artwork Management
- **Company / Organization:** Loftware Inc. (USA)
- **URL:** `https://www.loftware.com/`
- **Product / Version:** Loftware Spectrum / Cloud
- **Input:** Enterprise ERP product data (SAP, Oracle) and digital label templates.
- **Capabilities:** Automated generation of compliant labels across global enterprise supply chains; role-based template design; integration with GS1 standards.
- **Limitations:** Enterprise label *generation* and printing software for manufacturers; does not inspect physical packages in retail distribution or detect tampering.
- **Physical Measurement:** Vector template layout.
- **Multi-Panel Correlation:** Label template designer.
- **Regulatory Versioning:** Template version control.
- **Offline Capable:** Enterprise on-premise available.
- **Evidence Provenance:** Enterprise database logs.
- **Human Review:** Template designer approval.
- **Source Date:** 2023–2024.

---

## 3. Comparison Matrix

| System Name | Primary Target | Physical Calibrated Measurement? | Multi-Panel 3D Assembly? | Indian Legal Metrology Non-Retroactive Rules? | Offline Smartphone/Laptop? | Section 63 BSA Evidence Graph? | Human-in-the-Loop Review? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **eMaap** | Government Licensing Portal | No | No | No | No | No | Yes |
| **Artwork Flow** | Pre-Print Vector Artwork Proofing | No (Vector `pt`) | No | No | No | No | Yes |
| **GlobalVision** | Pre-Print / Flatbed Scanner QA | Yes (DPI-based) | No | No | Limited | No (FDA focus) | Yes |
| **Cognex In-Sight** | Factory Conveyor High-Speed OCR | Yes (Fixed mount) | Limited (Multi-cam) | No | Yes | No | No |
| **Keyence CV-X** | Industrial Quality Assurance | Yes (Telecentric) | Limited (Multi-cam) | No | Yes | No | No |
| **EyeC Proofiler** | Pharma Print Defect Inspection | Yes (Scanner) | No | No | Yes | No (Pharma) | Yes |
| **OpenFoodFacts** | Crowdsourced Consumer Info | No | No | No | No | No | Yes |
| **Omron LVS-7510** | Label Printer Barcode Grading | Yes (Printhead) | No | No | Yes | No | No |
| **Vincular/Corpbiz**| Legal Consulting Service | Manual (Calipers) | Manual | Yes (Manual lawyer) | No | No | Yes (Manual legal staff) |
| **Loftware** | Enterprise Label Generation | No (Template) | No | No | Limited | No | Yes |
| **Nirikshak (PS 26034)**| **Field Inspection Assistance** | **Yes (Planar Homography)** | **Yes (Pose Correlation)**| **Yes (Statutory Epoch Engine)**| **Yes (Edge CPU)** | **Yes (SHA-256 Merkle DAG)**| **Yes (Mandatory Officer Gate)**|
