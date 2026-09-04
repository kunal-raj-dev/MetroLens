# Threat Model Specification (STRIDE Framework)

## Purpose
Identifies security threats, attack surfaces, malicious manipulation vectors, and defensive countermeasures using the Microsoft STRIDE methodology.

## Scope
Covers mobile capture, image upload endpoints, rule engine execution, database storage, and PDF dossier generation.

## Authoritative Inputs
- OWASP Top 10 API Security Risks.
- NIST SP 800-30 (Risk Assessment Guide).

## Assumptions
- Adversaries may include non-compliant manufacturers attempting to evade penalties, disgruntled retail operators, or external network attackers.

## Open Questions
- Departmental network firewall and whitelisting requirements [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `apps/api/`
- `infra/`

## Verification Requirements
- All high-severity threats identified in the STRIDE matrix must have automated or architectural mitigations.

---

## STRIDE Threat Assessment Matrix

| STRIDE Category | Threat Description | Attack Vector | Severity | Engineering Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **Spoofing** | Adversary attempts to forge officer identity or inspection session. | Stolen JWT or credential replay. | HIGH | Short-lived JWTs (HMAC-SHA256) + device fingerprint binding. |
| **Tampering** | Operator or adversary modifies raw package image or alters rule verdict. | Modifying SQLite database or swapping cached image. | CRITICAL | SHA-256 computed on ingest; hash-chained audit log; append-only triggers. |
| **Repudiation** | Inspecting officer denies having approved or altered a borderline verdict. | Lack of action logging. | MEDIUM | Immutable event block in audit log capturing operator ID and timestamp. |
| **Information Disclosure** | Leakage of proprietary trade dress or consumer grievance phone numbers. | Unauthenticated API endpoint access or data dumps. | MEDIUM | Strict RBAC; automated PII redaction on public export (DPDP Act). |
| **Denial of Service** | System crash via image decompression bomb. | Upload of 500 MB malicious TIFF/PNG. | HIGH | Pre-decoding pixel dimension check ($\le 8192 \times 8192$); memory caps. |
| **Elevation of Privilege** | Standard field inspector attempts to alter statutory rules or thresholds. | Unauthorized PUT to `/api/v1/rules`. | CRITICAL | RBAC gate enforcing `SYSTEM_ADMIN` role for rule mutations. |
