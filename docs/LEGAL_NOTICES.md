# Legal Notices and Disclaimers

## Purpose
This document establishes the formal legal standing, statutory boundaries, and operational disclaimers governing the Nirikshak software system, its generated artifacts, and its interaction with Indian legal frameworks.

## Scope
Applies to all deployments, demonstrations, inspection reports, evidence dossiers, and technical outputs of the Nirikshak project (SIH 2026 — PS 26034).

## Authoritative Inputs
1. Constitution of India — Seventh Schedule (Union & Concurrent Lists regarding Weights and Measures).
2. The Legal Metrology Act, 2009 (Act No. 1 of 2010).
3. The Legal Metrology (Packaged Commodities) Rules, 2011 (G.S.R. 202(E) dated 7th March 2011) as amended.
4. Bharatiya Sakshya Adhiniyam, 2023 (provisions governing electronic records and admissibility).

## Assumptions
- The software is operated by an authorized enforcement officer or authorized trainee under supervision.
- Hardware devices (cameras, mobile phones, workstations) comply with minimum capture specifications.

## Open Questions
- Specific State Government adaptations and State Legal Metrology Enforcement Rules variations [TBD — PRIMARY SOURCE REQUIRED].
- Standard operating procedures for electronic seizure memo generation under specific State Directorate guidelines [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- Verification scripts (`scripts/verification/verify_legal_sources.py`).
- Regulatory artifact repository (`regulations/`).

## Verification Requirements
- All statutory disclaimers must be prominently included in all generated PDF and JSON inspection reports.
- Disclaimers must explicitly state that AI inference does not substitute statutory adjudication.

---

## Statutory Disclaimers

### 1. Decision Support, Not Statutory Adjudication
Nirikshak is an automated engineering decision-support tool. It is designed to assist an authorized Inspector of Legal Metrology in examining packaged commodities by detecting text, calculating calibrated physical dimensions, identifying mandatory declarations, and highlighting potential non-conformities against machine-readable rules.

**The system does NOT:**
- Adjudicate legal guilt or innocence.
- Issue compounding notices or initiate criminal prosecutions autonomously.
- Override the statutory discretion or independent judgment of an authorized officer.

### 2. Legal Evidentiary Status
The system generates technical inspection dossiers, perceptual and cryptographic hashes (SHA-256), and chain-of-custody metadata. **Whether such material possesses legal evidentiary status in any court of law or judicial forum is outside the system's determination and must be decided solely by the competent judicial or quasi-judicial authority under applicable procedural law (including the Bharatiya Sakshya Adhiniyam, 2023 / Indian Evidence Act principles).**

### 3. Government Ownership & Instrument Truth
References to the Department of Consumer Affairs (DoCA), Ministry of Consumer Affairs, Food & Public Distribution, Government of India, and official Acts, Rules, and Gazettes are made for statutory compliance and regulatory traceability purposes. Nirikshak makes no claim of sovereign authority; the official Gazette of India and authoritative notifications published by the Central Government remain the sole and exclusive primary authorities.
