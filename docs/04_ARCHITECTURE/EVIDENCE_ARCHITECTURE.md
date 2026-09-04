# Evidence Architecture & Cryptographic Provenance

## Purpose
Specifies the cryptographic structures, hashing pipelines, and directed acyclic graph (DAG) modeling the chain of custody for all inspection artifacts.

## Scope
Governs raw image storage, bounding box crops, feature extractions, rule evaluations, and audit logs.

## Authoritative Inputs
- Bharatiya Sakshya Adhiniyam, 2023 (Principles governing admissibility of electronic records).
- ISO/IEC 27037 (Guidelines for identification, collection, acquisition, and preservation of digital evidence).

## Assumptions
- Evidence integrity is guaranteed via cryptographic hashes (SHA-256) computed at ingestion before any image resizing or manipulation.

## Open Questions
- Departmental public key infrastructure (PKI) for officer digital signatures on exported PDF dossiers [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/evidence/`
- `packages/reporting/`

## Verification Requirements
- Verification script `scripts/verification/verify_report_provenance.py` must validate sample inspection dossiers.

---

## The Evidence Graph (DAG) Structure

Every inspection produces a directed evidence graph:

```
[Raw Photo I_0: SHA-256 = a8b4...] ───────────────┐
                                                  ▼
[Crop Polygon: BBox(x1, y1, x2, y2)] ───► [Calibrated Measurement]
                                                  │
                                                  ▼
[OCR Token: "Net Wt: 500g", Conf: 0.96] ──► [Normalized Field]
                                                  │
                                                  ▼
[Active Rule Snapshot: LMPC-R7-TABLE1] ──► [Rule Decision: PASS]
                                                  │
                                                  ▼
[Officer Review: Signature & Timestamp] ──► [Audit Log Block: H_prev + H_curr]
                                                  │
                                                  ▼
                                     [Immutable Inspection Dossier PDF]
```

### Stored Provenance Attributes:
1. `raw_image_sha256`: Cryptographic digest of untouched input image.
2. `crop_coordinates`: Normalized coordinates $[x_{\min}, y_{\min}, x_{\max}, y_{\max}]$.
3. `perceptual_hash`: pHash to detect identical packaging across inspections.
4. `calibration_scale_factor`: $\text{mm/pixel}$ and detected target ID.
5. `model_version`: Exact commit hash and weight checksum of OCR/vision models.
6. `ruleset_epoch`: ID of regulatory epoch applied.
7. `operator_id`: Badge number or identifier of the inspecting officer.
8. `timestamp_utc`: ISO 8601 UTC timestamp.
