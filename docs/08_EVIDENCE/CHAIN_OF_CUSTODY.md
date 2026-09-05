# Digital Chain of Custody Specification

## Purpose
Establishes the procedural and technical safeguards guaranteeing that digital evidence collected during an inspection cannot be altered, substituted, or deleted undetected.

## Scope
Covers device camera capture, temporary cache storage, database persistence, and final dossier export.

## Authoritative Inputs
- Section 63 (Admissibility of electronic records) of the Bharatiya Sakshya Adhiniyam, 2023.
- ISO/IEC 27037 Digital Evidence Handling Guidelines.

## Assumptions
- The chain of custody begins the millisecond an image frame is ingested into application memory.

## Open Questions
- Departmental requirements for hardware-bound cryptoprocessor (TPM / Secure Enclave) key attestation [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/evidence/`

## Verification Requirements
- Simulating byte alteration in a raw image file must immediately break dossier checksum verification.

---

## Chain of Custody Workflow

1. **Ingestion & Initial Hashing:**
   - Raw byte stream read from camera sensor.
   - SHA-256 digest calculated immediately: $H_0 = \text{SHA-256}(B_{\text{raw}})$.
   - Timestamp and GPS coordinates (if enabled) cryptographically bound to $H_0$.

2. **Crop & Derivative Traceability:**
   - When a region of interest (e.g. Net Quantity declaration) is cropped, its relative coordinates $(x_1, y_1, x_2, y_2)$ and derivative hash $H_{\text{crop}}$ are recorded with parent reference $H_0$.

3. **Immutable Audit Ledger:**
   - Each state transition (Capture $\rightarrow$ Process $\rightarrow$ Officer Review $\rightarrow$ Finalize) appends an event block to an append-only log where each block contains the cryptographic hash of the preceding block ($H_{n} = \text{SHA-256}(H_{n-1} + \text{Payload})$).

4. **Officer Attestation:**
   - Final report generation requires inspecting officer PIN or biometric sign-off, recording operator ID and attestation timestamp.
