# Nirikshak Evidence Package (`nirikshak-evidence`)

## Purpose
Generates immutable, cryptographically verifiable Evidence DAG nodes conforming to `rules/schema/evidence.schema.json`. Links raw image SHA-256 digests to normalized spatial crops, OCR observations, and physical calibration measurements.

## Owner
Systems & Security Lead

## Interface Seams
- **Input**: Raw image bytes / SHA-256, bounding boxes, observations, measurements.
- **Output**: `List[EvidenceItem]`.
- **Error Codes**: `ERR_EVIDENCE_HASH_MISMATCH`.
