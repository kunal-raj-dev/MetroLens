# Security Architecture Specification

## Purpose
Defines the threat model, authentication mechanisms, authorization boundaries, cryptographic safeguards, and data protection policies for Nirikshak.

## Scope
Covers mobile clients, web portals, APIs, inference workers, databases, and evidentiary storage.

## Authoritative Inputs
- OWASP Top 10 API Security Risks.
- Digital Personal Data Protection (DPDP) Act, 2023.

## Assumptions
- Systems operate across untrusted local wireless networks and field devices requiring local encryption.

## Open Questions
- Departmental VPN and token-based hardware security key standards [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/09_SECURITY_PRIVACY/THREAT_MODEL.md`
- `docs/09_SECURITY_PRIVACY/RBAC.md`

## Verification Requirements
- All API endpoints must enforce RBAC and pass automated vulnerability scans.

---

## Defense-in-Depth Layers

1. **Authentication & Session Management:**
   - Stateless JWT tokens signed with HMAC-SHA256 or asymmetric Ed25519 keys.
   - Configurable session timeout (default: 8 hours for continuous shift duty).

2. **Authorization (RBAC):**
   - Three discrete permission tiers: `INSPECTOR`, `SUPERVISOR`, and `SYSTEM_ADMIN`.
   - Resource-level authorization: Inspectors cannot alter finalized supervisory decisions.

3. **Input Validation & Decompression Bomb Defense:**
   - Strict image dimension caps: maximum $8192 \times 8192$ pixels ($\le 67\text{ MP}$).
   - Image stream magic bytes verification (reject disguised payloads).
   - Memory allocation quotas per inference worker.

4. **Cryptographic Protection at Rest & Transit:**
   - Transport: TLS 1.3 mandatory for all network communications.
   - Storage: AES-256-GCM encryption for local SQLite inspection caches on mobile/edge devices.

5. **Privacy & Consumer Care Masking:**
   - Automated redaction of personal phone numbers and private email addresses when exporting public surveillance datasets (DPDP Act compliance).
