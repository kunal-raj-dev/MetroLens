# Nirikshak Reporting Package (`nirikshak-reporting`)

## Purpose
Generates official, court-ready Legal Metrology Inspection Dossiers in PDF format (using ReportLab) and standardized JSON audit files. Embeds SHA-256 evidence digests, officer annotations, and statutory citations.

## Owner
Reporting Lead

## Interface Seams
- **Input**: `InspectionResult`, officer signature, issuing authority info.
- **Output**: PDF dossier byte stream and structured JSON summary.
- **Error Codes**: `ERR_REPORT_GENERATION_FAILED`.
