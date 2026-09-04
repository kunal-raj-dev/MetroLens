# Security Policy

## Reporting a Vulnerability

The Nirikshak development team treats system integrity, chain of custody, and cryptographic auditability with highest priority.

If you discover a potential vulnerability, please do NOT open a public GitHub issue.

- Contact: `SECURITY_CONTACT_REQUIRED` (Project security lead designated upon deployment)
- Protocol: Submit vulnerability details privately with reproducible steps.
- Response Commitment: Acknowledgement and triage will be performed during standard engineering review cycles. (Production SLA: `SECURITY_SLA_PENDING_DEPLOYMENT`).

---

## Security Architecture Principles

Nirikshak implements defense-in-depth principles across all inspection pipelines:

1. **Cryptographic Immutability:**
   - Raw package captures are hashed (SHA-256) at the point of ingestion before any pre-processing, cropping, or optical analysis.
   - Audit logs follow append-only semantics to prevent evidence tampering.

2. **File Upload & Image Security:**
   - Strict MIME type verification (magic bytes inspection for JPEG, PNG, TIFF).
   - EXIF/metadata sanitization to eliminate location leakage unless authorized officer location tagging is activated.
   - Decompression bomb mitigation (strict pixel dimension limits: maximum 40 megapixels per image, memory allocation caps).

3. **Role-Based Access Control (RBAC):**
   - Three distinct operational roles:
     - `INSPECTOR`: Guided capture, evidence review, draft report submission.
     - `SENIOR_OFFICER` / `SUPERVISOR`: Report adjudication, formal issuance, appeal handling.
     - `SYSTEM_ADMIN`: Node configuration, model version deployment, regulatory catalog updates.
   - Least privilege enforced at both API routing and database row levels.

4. **Secrets & Credentials Management:**
   - No hardcoded API keys, JWT signing secrets, or database credentials.
   - All runtime configurations loaded via environment variables conforming to `.env.example`.

5. **Offline & Edge Security:**
   - On-device local inspection caches use AES-GCM encryption at rest.
   - Synchronizations with central repository require mutual TLS (mTLS) or authenticated signed payloads.
