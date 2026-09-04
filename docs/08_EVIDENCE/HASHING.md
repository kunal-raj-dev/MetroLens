# Cryptographic Hashing & Perceptual Hashing Standards

## Purpose
Specifies the exact cryptographic algorithms, block sizes, perceptual hashing methods, and verification routines utilized across Nirikshak.

## Scope
Applies to image files, rule catalogs, machine-readable rule definitions, and audit blocks.

## Authoritative Inputs
- FIPS PUB 180-4 (Secure Hash Standard - SHA-256).

## Assumptions
- SHA-256 provides collision resistance sufficient for legal and evidentiary integrity.

## Open Questions
- None.

## Dependencies
- Standard Python `hashlib` and OpenCV perceptual hashing modules.

## Verification Requirements
- All hashing implementations must pass standard NIST test vectors.

---

## 1. Cryptographic Hashing (SHA-256)

Used for absolute, bit-level integrity verification:
- **Block Size:** 64 KB streaming buffer during file reads.
- **Representation:** 64-character lowercase hexadecimal string.
- **Application:**
  - Raw camera frames.
  - Exported PDF dossiers.
  - Source legal documents in `regulations/`.

```python
import hashlib

def compute_sha256(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()
```

---

## 2. Perceptual Hashing (pHash)

Used to detect duplicate or near-identical packaging across inspections (even under minor lighting or compression variations):
- **Algorithm:** Discrete Cosine Transform (DCT) based perceptual hash.
- **Hash Length:** 64-bit integer / 16-character hex.
- **Hamming Distance Threshold:** Packages with Hamming distance $d_H \le 4$ are flagged as identical trade dress SKUs.
