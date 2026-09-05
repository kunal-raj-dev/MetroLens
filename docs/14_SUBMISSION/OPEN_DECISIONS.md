# Open Architecture & Engineering Decisions

## Purpose
Tracks unresolved architectural questions, open engineering trade-offs, and pending empirical decisions prior to full-scale code implementation.

## Scope
Universal across optics, backend, UI, and database subsystems.

---

## Open Decisions Registry

### Decision DEC-01: Optical Text Recognition Engine Selection
- **Status:** OPEN / PENDING BENCHMARK
- **Context:** Deciding between PaddleOCR, Tesseract, and Surya OCR for the primary local CPU inference pipeline.
- **Trade-off:** PaddleOCR provides superior Devanagari character accuracy but requires larger binary footprint; Tesseract is lightweight but prone to character misclassifications on stylized packaging fonts.
- **Resolution Path:** Execute benchmark protocol PROTO-OCR-001 on `data/benchmark/` to make an empirically grounded decision.

---

### Decision DEC-02: Preferred Physical Reference Marker Format
- **Status:** OPEN / PENDING USABILITY TRIAL
- **Context:** Deciding between a high-contrast circular sticker ($D = 25.0\text{ mm}$) and a standardized departmental plastic inspection card ($85.6 \times 54.0\text{ mm}$, ID-1 format).
- **Trade-off:** Circular sticker is cheap and can be placed on curved surfaces; ID-1 card provides larger surface area for 4-point homography estimation on flat cartons.
- **Resolution Path:** Field trial testing usability and detection stability across 50 retail packages.

---

### Decision DEC-03: On-Device Database Engine for Mobile Field Unit
- **Status:** OPEN / ACCEPTED IN PRINCIPLE
- **Context:** SQLite (with SQLCipher encryption) vs. Embedded PostgreSQL for local offline storage.
- **Current Direction:** SQLite for mobile client; PostgreSQL for departmental central server.
