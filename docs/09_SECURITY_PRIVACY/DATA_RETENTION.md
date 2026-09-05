# Data Retention, Archival & Disposal Policy

## Purpose
Establishes storage lifecycle rules, statutory evidence retention periods, cryptographic verification intervals, and secure data wiping procedures.

## Scope
Covers local on-device caches, central database records, and cold archival storage.

## Authoritative Inputs
- Statutory limitation periods under the Legal Metrology Act, 2009.
- General Government of India record retention schedules.

## Assumptions
- Completed enforcement dossiers must be retained for at least the statutory limitation period for compounding or court trials.

## Open Questions
- Departmental data retention mandates across different Indian States [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `infra/storage/`
- `infra/db/`

## Verification Requirements
- Automated purging scripts must delete temporary unsubmitted scratch files older than 48 hours without affecting finalized inspection dossiers.

---

## Retention Schedules

| Data Category | Primary Storage | Retention Window | Action upon Expiry |
| :--- | :--- | :--- | :--- |
| **Temporary Scratch Frames** | Local Device RAM / Temp | 24 Hours | Secure cryptographic wipe |
| **Unsubmitted Draft Inspections**| Local SQLite Cache | 7 Days | Warning prompt, then purge |
| **Finalized Inspection Dossiers**| Encrypted DB & Object Store | 7 Years (Statutory) | Move to cold archival storage |
| **Tamper-Evident Audit Logs** | Immutable Append-Only Log | Indefinite / Permanent | Retain permanently for forensic audit |
