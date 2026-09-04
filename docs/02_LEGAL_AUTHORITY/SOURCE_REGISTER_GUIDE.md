# Guide to the Legal Source Registry

## Purpose
Explains the structure, schema, lifecycle, and operational protocols governing the canonical legal source registry located at `regulations/source_registry.yaml`.

## Scope
Covers all regulatory source artifacts ingested into Nirikshak.

## Authoritative Inputs
- `regulations/source_registry.yaml`
- `scripts/verification/verify_legal_sources.py`

## Assumptions
- Every legal document referenced by the system must be physically archived in `regulations/` and tracked in `source_registry.yaml`.

## Open Questions
- Department of Consumer Affairs archival portal link persistence and digital signature verification of Gazette PDFs [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `regulations/source_registry.yaml`

## Verification Requirements
- All records must validate against `scripts/verification/verify_legal_sources.py`.

---

## Canonical Registry Location
The **single source of truth** for regulatory source records is:
```
regulations/source_registry.yaml
```

Do NOT create duplicate registry files in `docs/`. This guide explains the metadata standards and ingestion workflows.

---

## Mandatory Metadata Fields for Every Source Record

```yaml
source_id: "IN-LMPC-2011-GSR202E"       # Unique immutable ID
title: "The Legal Metrology..."         # Official statutory title
authority:
  organisation: "DoCA"                  # Publishing body
  ministry: "Ministry of Consumer..."   # Central ministry
  jurisdiction: "Republic of India"     # Statutory jurisdiction
source_type: "primary_government"       # Level in source hierarchy
instrument_status: "IN_FORCE"           # IN_FORCE | PROPOSED | DRAFT | SUPERSEDED
official_url: "https://..."             # Official government URL
publication_date: "YYYY-MM-DD"          # Date gazetted/published
commencement_date: "YYYY-MM-DD"         # Date rule entered into legal force
retrieved_at: "YYYY-MM-DD"              # Ingestion date
sha256: "..."                           # SHA-256 hash of PDF on disk (or PRIMARY_SOURCE_REQUIRED)
local_artifact_path: "regulations/..."  # Path to local artifact
verification_status: "VERIFIED_PRIMARY" # Status in taxonomy
verified_by: "NAME_OR_ROLE"             # Legal engineer who authenticated
verified_at: "YYYY-MM-DD"               # Verification date
notes: "..."                            # Scope and statutory context
```

### Ingestion Workflow
1. Download official Gazette PDF directly from `egazette.gov.in` or `consumeraffairs.nic.in` into `regulations/sources/`.
2. Compute cryptographic SHA-256 checksum: `sha256sum path/to/document.pdf`.
3. Create entry in `regulations/source_registry.yaml`.
4. Run `python scripts/verification/verify_legal_sources.py` to ensure schema conformance and hash integrity.
5. Only upon successful verification may machine-readable rules citing this `source_id` be authored in `rules/proposed/` or promoted to `rules/verified/`.

---

## Crucial Regulatory Precedents & Corrigenda Protocol

- **Table-I Corrigendum (`G.S.R. 1373(E)`):** When ingesting substituted rules, engineers must search for official Corrigenda. In the 2017 amendments, `G.S.R. 629(E)` contained a clerical error in Table-I Column (3), which was corrected by `G.S.R. 1373(E)` from 1.5 mm to 2.0 mm. Unverified secondary portals frequently reproduce the uncorrected 1.5 mm figure.
- **Jan Vishwas Act 2023 (`Act No. 18 of 2023`):** Section 36(1) amendments introduce an *Improvement Notice* mechanism for first-time procedural non-compliances, transitioning enforcement from automatic criminal prosecution to corrective compliance.
- **Research Dossiers:** Detailed legal provenance records are cross-cataloged in `research/official_sources/PACK_B_LEGAL_FRAMEWORK.md` and `research/official_sources/PACK_C_MEASUREMENT_STANDARDS.md`.
