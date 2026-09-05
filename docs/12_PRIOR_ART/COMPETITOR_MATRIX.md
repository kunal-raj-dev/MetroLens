# Competitive Comparison Matrix

## Purpose
Establishes a rigorous, multidimensional technical comparison between Nirikshak and alternative solutions across academic, commercial, and governmental domains.

## Scope
Compares capabilities across physical calibration, multi-panel reasoning, regulatory versioning, offline operation, and evidence integrity.

## Authoritative Inputs
- Technical documentation of commercial and open-source tools.
- `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md`.

## Assumptions
- Evaluations are based on publicly documented capabilities of compared systems.

## Dependencies
- `docs/12_PRIOR_ART/DIFFERENTIATION.md`

## Verification Requirements
- Matrix must not make unsupported negative claims about commercial products.

---

## Evidence-Based Framing Notice
> [!NOTE]
> In the reviewed commercial and academic systems catalogued in `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md`, we did not identify solutions combining physical scale calibration, multi-panel 3D packaging correlation, and multi-epoch statutory versioning for Indian Legal Metrology. The matrix below reflects capabilities observed in publicly documented literature and testing.

---

---

## Technical Comparison Matrix (Reviewed Prior Art vs. Nirikshak Architecture)

> [!NOTE]
> **Implementation Status Notice:** All Nirikshak capabilities listed in the matrix represent architectural design specifications (`DESIGNED / NOT YET IMPLEMENTED`). Production runtime code and empirical benchmarks are pending Stage 2.

| Architectural Capability | Generic Mobile OCR Tools | Pre-Print Artwork QA Systems | Consumer Grievance Portals | Nirikshak Architecture (Design Target) |
| :--- | :--- | :--- | :--- | :--- |
| **Input Modality** | 2D Camera Snapshot | Digital Vector PDF Artwork | Manual Text Entry Form | Guided Multi-Panel Physical Photos (`DESIGNED / NOT YET IMPLEMENTED`) |
| **Physical Scale Calibration** | NOT VERIFIED in reviewed literature | Native vector point (`pt`) dimensions | NOT VERIFIED in reviewed literature | Planar Reference Fiducial ($\text{mm/px}$) (`DESIGNED / NOT YET IMPLEMENTED`) |
| **PDP Area Segmentation** | NOT VERIFIED in reviewed literature | NOT VERIFIED in reviewed literature | NOT VERIFIED in reviewed literature | Algorithmic Rule 7 geometry (`DESIGNED / NOT YET IMPLEMENTED`) |
| **Rule Engine Model** | NOT VERIFIED in reviewed literature | Static brand guidelines | NOT VERIFIED in reviewed literature | Deterministic Statutory Engine (`DESIGNED / NOT YET IMPLEMENTED`) |
| **Regulatory Time-Machine** | NOT VERIFIED in reviewed literature | NOT VERIFIED in reviewed literature | NOT VERIFIED in reviewed literature | Multi-Epoch Snapshot Manager (`DESIGNED / NOT YET IMPLEMENTED`) |
| **Cross-Panel Contradiction** | Single-view only | Single artwork file | Manual officer review | Multi-Panel DAG Correlation (`DESIGNED / NOT YET IMPLEMENTED`) |
| **Offline Edge Execution** | Cloud API observed in public docs | Workstation client observed | Web portal architecture | Designed for local CPU execution — implementation/benchmark pending |
| **Cryptographic Provenance** | Plain export | Proprietary application log | Central database audit log | SHA-256 DAG & Signed Dossier (`DESIGNED / NOT YET IMPLEMENTED`) |

*Note: "NOT VERIFIED in reviewed literature" denotes that an equivalent capability was not documented in the reviewed technical specifications of compared systems. It does NOT assert that a competitor categorically lacks capability beyond the scope of reviewed materials.*

---

## Competitor Claim Evidence Audit

Every comparative assertion regarding prior-art tools is audited against documented technical sources:

| COMPETITOR | CAPABILITY | CLAIM | SOURCE | SOURCE_DATE | EVIDENCE_TYPE | CONFIDENCE |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **Google Lens** | Offline Execution | Cloud connection typically utilized for visual search & multimodal query resolution | Google Support & Cloud Vision API Documentation | 2024 | Official Product Documentation | HIGH |
| **Google Lens** | Metrological Calibration | Physical millimeter font height measurement not supported; outputs bounding box pixel coordinates | Google Vision API Reference (`BoundingPoly`) | 2024 | Technical API Specification | HIGH |
| **GlobalVision** | Input Modality | Ingests digital vector artwork (PDF, AI) and high-resolution flatbed scanner files | GlobalVision System Requirements Specification | 2023 | Vendor Technical Spec | HIGH |
| **GlobalVision** | Environment | Deployed as desktop client workstation software for pre-press quality control | GlobalVision Deployment Architecture Manual | 2023 | Vendor Architecture Guide | HIGH |
| **Artwork Flow** | Packaging Stage | Targets pre-print packaging design approval workflows before plate printing | Bizongo Artwork Flow Product Whitepaper | 2024 | Commercial Product Collateral | HIGH |
| **Artwork Flow** | Scale Metric | Measures digital typography in points/DPI; no physical lens homography calibration | Artwork Flow Technical Feature Overview | 2024 | Technical Feature Guide | HIGH |
| **eMaap** | OCR / CV Automation | Operates as an administrative registration web portal; automated CV label parsing is NOT VERIFIED | Department of Consumer Affairs (`emaap.gov.in`) | 2024 | Official Government Portal | HIGH |
| **e-Daakhil** | Automated Legal Metrology | Consumer grievance filing portal; automated computer-vision label measurement is NOT VERIFIED | National Consumer Dispute Redressal Commission (`edaakhil.nic.in`)| 2024 | Official Government Portal | HIGH |
| **Cognex In-Sight** | Form Factor | Industrial factory-floor machine vision cameras requiring fixed mounting & illumination | Cognex In-Sight 2800 / 3800 Datasheets | 2023 | Industrial Hardware Datasheet | HIGH |
| **Keyence CV-X** | Form Factor | High-speed conveyor inspection controller; not designed as field officer mobile app | Keyence CV-X Series User Manual | 2023 | Industrial Hardware Manual | HIGH |
