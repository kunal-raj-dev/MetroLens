# Privacy Policy & PII Protection (DPDP Act Compliance)

## Purpose
Specifies data minimization, consumer care PII redaction, officer privacy safeguards, and compliance with the Digital Personal Data Protection (DPDP) Act, 2023.

## Scope
Governs all inspection records, packaging photographs, and exported market surveillance datasets.

## Authoritative Inputs
- Digital Personal Data Protection (DPDP) Act, 2023 (Republic of India).

## Assumptions
- Mandatory declarations on commercial retail packaging (e.g. manufacturer corporate address, toll-free number) are public statutory disclosures. However, personal mobile numbers or private emails mistakenly printed must be safeguarded.

## Open Questions
- Departmental guidelines regarding inspector name and badge number masking on publicly released market surveillance audits [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/extraction/`
- `packages/reporting/`

## Verification Requirements
- Automated tests must verify that personal contact information is masked in anonymized surveillance exports.

---

## Privacy Engineering Safeguards

1. **Consumer Care Details Sanitization:**
   - When generating research or public surveillance summaries, phone numbers matching personal mobile prefixes ($+91\text{-}[6\text{-}9]\dots$) are masked: `+91-XXXXX-XXXXX`.
   - General corporate toll-free numbers ($1800\text{-}\dots$) and official departmental helplines remain unmasked for regulatory auditability.

2. **Facial & Background Redaction:**
   - The guided capture interface focuses strictly on the package surface.
   - If an incidental bystander face or retail store employee is detected in the image periphery, the bounding region is automatically blurred prior to long-term archiving.

3. **Officer Identity Protection:**
   - In field exports distributed to external parties, internal officer IDs are replaced with pseudonymous cryptographic tokens unless explicitly required for legal seizure memos.
