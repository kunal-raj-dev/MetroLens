# Final Architecture Synthesis

## Purpose
Synthesizes the finalized, frozen system architecture for Nirikshak for evaluation panels and technical reviewers.

## Architecture Highlights
1. **Tier 1 (Presentation):** React/Next.js guided capture interface with real-time on-screen quality gate overlays and touch-friendly inspection review screens (`apps/web/`).
2. **Tier 2 (Gateway & API):** FastAPI backend with JWT-based RBAC, SHA-256 stream hashing, and request controllers (`apps/api/`).
3. **Tier 3 (Pipeline Packages):** Decoupled, modular Python packages:
   - `packages/vision/`: Image quality gate (Laplacian variance blur, specular glare), PDP segmentation, and contour analysis.
   - `packages/calibration/`: Planar fiducial target detection and $\text{mm/px}$ scale estimation.
   - `packages/ocr/`: Multilingual OCR engine with Latin and Devanagari character recognition.
   - `packages/extraction/`: Rule 6(1) mandatory declaration entity parser and metric normalizer.
   - `packages/measurement/`: Millimetre font height and area calculator with bounded uncertainty.
   - `packages/rules-engine/`: Deterministic 4-state rule evaluator with regulatory time-machine snapshot loading.
   - `packages/evidence/`: Directed Acyclic Graph (DAG) provenance builder and append-only audit logger.
   - `packages/reporting/`: Cryptographic PDF inspection dossier generator.
4. **Tier 4 (Persistence):** Local SQLite / PostgreSQL storage with cryptographic checksum chaining.
