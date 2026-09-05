# Prior Art Register & Literature Review

## Purpose
Catalogues existing academic papers, commercial systems, open-source repositories, and government tools relevant to packaging inspection and optical metrology.

## Scope
Covers pre-print packaging QA tools, mobile OCR scanners, government e-governance systems, and scene text detection benchmarks.

## Authoritative Inputs
- Academic literature (IEEE, ACM, Springer, arXiv).
- Commercial packaging compliance software documentation.
- Government Legal Metrology portals.

## Assumptions
- Never claim "no existing solution exists" without rigorous literature analysis. Differentiation must focus on the unique architectural combination of optical metrology, regulatory time-machine, and cryptographic provenance.

## Open Questions
- Specific technical capabilities of state-level Legal Metrology e-Parapadhati / e-Map systems [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/12_PRIOR_ART/COMPETITOR_MATRIX.md`
- `docs/12_PRIOR_ART/DIFFERENTIATION.md`

## Verification Requirements
- Prior-art claims must cite verified public sources or patent/paper publications.

---

## Prior Art Categories

1. **Academic Computer Vision & Scene Text Literature:**
   - Liao et al., "Real-time Scene Text Detection with Differentiable Binarization" (DBNet, AAAI 2020).
   - Du et al., "SVTR: Scene Text Recognition with a Single Visual Model" (IJCAI 2022).
   - Bounded limitation: Focuses on word transcription in natural scenes; zero capability for physical scale calibration in millimetres or legal rule reasoning.

2. **Commercial Packaging Pre-Print QA Software:**
   - Esko Global Vision / Artwork Inspection Systems, Global Vision Digital Inspection Suite.
   - Bounded limitation: Operates on native vector PDF files during pre-press printing; cannot evaluate physical distorted packaging on retail shelves via smartphone camera.

3. **Generic Mobile Document & OCR Scanners:**
   - Google Lens, Microsoft Lens, Adobe Scan.
   - Bounded limitation: Dimensionless 2D text extraction; lacks Legal Metrology knowledge, PDP area segmentation, multi-panel correlation, and regulatory snapshots.

4. **Government Portals & Legal Metrology Systems:**
   - eMaap (National Legal Metrology Portal, `emaap.gov.in`), National Consumer Helpline, e-Daakhil.
   - Bounded limitation: Administrative fee payment, Rule 27 registrations, and complaint portals; zero automated computer vision, optical measurement, or AI label inspection assistance.

5. **Industrial Machine Vision & Sensor Systems:**
   - Cognex In-Sight, Keyence CV-X/XG-X, Omron Microscan.
   - Bounded limitation: Heavy factory-floor capital equipment requiring fixed strobe lighting and conveyor geometry; not deployable as mobile edge inspection software for field officers in retail stores.

6. **Comprehensive Systems Catalog:**
   - Detailed 10-system evaluation records and comparative matrices are documented in [`research/prior_art/PACK_D_PRIOR_ART.md`](../../research/prior_art/PACK_D_PRIOR_ART.md).

