# Evidence Limitations & Evidentiary Disclaimer

## Purpose
Establishes clear statutory and engineering limitations concerning the evidentiary standing of automatically generated inspection artifacts.

## Scope
Applies to all generated JSON inspection records, PDF dossiers, cryptographic hashes, and visual bounding box overlays.

## Authoritative Inputs
- Section 63 (Admissibility of electronic records) of the Bharatiya Sakshya Adhiniyam, 2023.
- Legal Metrology Act, 2009 statutory officer authority boundaries.

## Assumptions
- Technical software outputs require formal verification and endorsement by authorized enforcement personnel before introduction into any legal proceeding.

## Open Questions
- Specific state procedural rules regarding submission of digital photographs in summary compounding trials [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/LEGAL_NOTICES.md`
- `packages/reporting/`

## Verification Requirements
- This disclaimer must be incorporated into every exported inspection dossier.

---

## Controlled Evidentiary Standing Statement

> **Statutory Notice on Evidentiary Status:**  
> **The system produces inspection-assistance evidence and provenance records. Whether such material has legal evidentiary status is outside the system's determination and must be decided by the competent authority under applicable law and procedure.**

### Specific Engineering & Evidentiary Limitations

1. **Non-Substitution of Statutory Authority:**
   Nirikshak does not possess statutory authority under the Legal Metrology Act, 2009. The system acts as an observational and computational aid to the authorized Inspector of Legal Metrology. Any enforcement notice, seizure memo, compounding notice, or prosecution remains the exclusive statutory responsibility of the authorized officer.

2. **Optical Measurement Limits:**
   All physical measurements (font height, character width, PDP area) represent optical approximations subject to physical camera calibration and perspective homography. Where confidence bounds overlap with statutory thresholds, the system deliberately refuses to issue a binary determination and flags `REVIEW`.

3. **Admissibility of Electronic Records:**
   Cryptographic hashing (SHA-256) and append-only audit logging provide tamper-detection mechanisms. However, the legal admissibility of electronic records in judicial proceedings is governed by the Bharatiya Sakshya Adhiniyam, 2023 (and applicable procedural codes), requiring formal officer certificate of authenticity.

4. **Cryptographic Property vs. Legal Consequence Distinction:**
   - **Cryptographic Property:** `HASH VERIFIED` (Technical verification that raw image and metadata bitstreams match cryptographic digests without bit-level alteration).
   - **Legal Consequence:** `NOT DETERMINED BY NIRIKSHAK` (Evidentiary admissibility, legal authenticity, statutory sufficiency, and procedural compliance are matters of sovereign law determined solely by authorized officers and judicial forums under Section 63 BSA 2023).
