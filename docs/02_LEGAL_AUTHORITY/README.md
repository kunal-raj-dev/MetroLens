# Legal Authority & Governance Documentation

## Purpose
Establishes the governance structure, legal source hierarchy, verification methodologies, and provenance tracking for all regulatory instruments governing packaged commodities inspection.

## Scope
Defines how primary legal instruments published by the Government of India are ingested, authenticated, tracked, and translated into verified engineering specifications.

## Authoritative Inputs
- The Gazette of India.
- Department of Consumer Affairs (DoCA) official portal.
- India Code (Legislative Department, Ministry of Law and Justice).

## Assumptions
- Legal authority resides strictly in the sovereign instruments published by the Central/State Governments. The software repository and its catalogs are representations, not authorities.

## Open Questions
- Departmental notifications issued under emergency powers or temporary exemptions (e.g. transitional labeling relaxations) [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `regulations/source_registry.yaml`
- `scripts/verification/verify_legal_sources.py`

## Verification Requirements
- Every legal statement in documentation must cite a source registered in `regulations/source_registry.yaml`.

---

## Architecture of Authority

```
[Level 1: Sovereign Primary Source (Gazette / Act / Official Rule)]
                               │
                               ▼
   [regulations/ : Authoritative Artifacts & Source Registry]
                               │
                               ▼
     [docs/02_LEGAL_AUTHORITY/ : Human Governance & Changelog]
                               │
                               ▼
       [rules/ : Machine-Readable Declarative Rules]
```

### Tripartite Directory Rule:
1. `regulations/`: Contains the actual primary source PDFs, verified text transcriptions, and the canonical `source_registry.yaml`.
2. `rules/`: Contains the executable, machine-readable JSON/YAML definitions used by the deterministic rule engine. Every rule points back to `regulations/`.
3. `docs/02_LEGAL_AUTHORITY/`: Contains human explanations, legal changelog, authority hierarchy, and statutory impact matrices.
