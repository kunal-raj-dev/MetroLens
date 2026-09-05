# Third-Party Licenses & Software Dependencies

## Purpose
Establishes clear copyright attribution and licensing conformance for all third-party software libraries, pre-trained neural networks, and system tools evaluated or incorporated into the Nirikshak architecture.

## Scope
Covers open-source computer vision libraries, optical character recognition engines, web frameworks, and database drivers utilized across `apps/`, `packages/`, and `infra/`.

## Authoritative Inputs
- Official upstream repository licenses (GitHub / Apache Software Foundation / Linux Foundation).
- Python Package Index (PyPI) and Node Package Manager (NPM) declared package metadata.

## Assumptions
- Only open-source components with non-copyleft or permissively compatible licenses (Apache 2.0, MIT, BSD 2/3-Clause) are integrated into core distribution modules.
- Copyleft-licensed components (e.g. AGPL/GPL) must be strictly isolated behind standardized service boundaries or avoided where licensing contamination is a concern.

## Open Questions
- Final optical character recognition engine selection (PaddleOCR vs. Tesseract vs. Surya) based on empirical benchmark results on Indian packaging [TBD — MEASURE].
- Specific pre-trained model weight licensing terms for commercial or governmental deployment [TBD — VERIFICATION REQUIRED].

## Dependencies
- Package manifests (`apps/*/package.json`, `apps/*/requirements.txt`, `packages/*/pyproject.toml`).

## Verification Requirements
- All third-party packages must be verified via automated license audit scripts during CI.
- No package with ambiguous or missing license declaration may be merged.

---

## Architectural Dependency Registry (Planned & Evaluated)

| Component / Library | Evaluated Role | Upstream License | Commercial / Gov Reuse Permitted? | Attribution / Notice Requirement | License Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | REST API Routing | MIT License | Yes | Retain copyright notice | LICENSE_VERIFIED |
| **Pydantic** | Schema & Rule Validation | MIT License | Yes | Retain copyright notice | LICENSE_VERIFIED |
| **OpenCV (opencv-python)** | Image Preprocessing & Edge Detection | Apache 2.0 | Yes | Retain Apache 2.0 notices | LICENSE_VERIFIED |
| **PaddleOCR** | Multilingual OCR Engine | Apache 2.0 | Yes | Retain Apache 2.0 notices | LICENSE_VERIFIED |
| **Tesseract OCR** | Secondary OCR Engine | Apache 2.0 | Yes | Retain Apache 2.0 notices | LICENSE_VERIFIED |
| **PostgreSQL Driver (asyncpg)** | Database Persistence | Apache 2.0 | Yes | Retain Apache 2.0 notices | LICENSE_VERIFIED |
| **PyYAML / jsonschema** | Rule Catalog & Registry Parsing | MIT / MIT | Yes | Retain copyright notice | LICENSE_VERIFIED |
| **ReportLab / WeasyPrint** | PDF Dossier Generation | BSD / BSD 3-Clause | Yes | Retain copyright notice | LICENSE_VERIFIED |

> [!NOTE]
> Pre-trained weights for computer vision models have distinct licensing terms from the underlying inference code. Every model utilized in `models/` must carry a dedicated `models/cards/<model_name>.md` detailing weight provenance, training dataset rights, and commercial applicability.
