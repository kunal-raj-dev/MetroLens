# Contributing to Nirikshak

Thank you for contributing to **Nirikshak**, an automated Legal Metrology inspection assistance system engineered for high trust, statutory adherence, and zero hallucination.

## Non-Negotiable Anti-Hallucination & Governance Rules

All contributors must strictly observe the following core project policies:

1. **Never Invent Legal Rules:** No rule numbers, sub-rules, penalty clauses, exemptions, amendment dates, or official interpretations may be committed without an authenticated primary source record.
2. **Authority Hierarchy Compliance:**
   - **Level 1 (Primary Government):** The Gazette of India, Department of Consumer Affairs (DoCA), India Code.
   - **Level 2 (Official Supporting):** Official DoCA FAQs, implementation guidelines, standards.
   - **Level 3 (Technical):** Peer-reviewed papers, official library docs, ISO standards.
   - **Level 4 (Secondary):** Reputable legal texts, industry manuals.
   - **Level 5 (Discovery Only):** Blogs, forums, search snippets, AI summaries. *Level 5 can never establish legal authority or rule content.*
3. **Tripartite Directory Integrity:**
   - Put official gazettes and primary PDF/texts in `regulations/`.
   - Put machine-readable rule definitions in `rules/` (must link back to `regulations/source_registry.yaml` via exact `source_location`).
   - Put explanatory or governance documentation in `docs/`.
   - Never conflate research or web scraping (`research/`) with official legal authority (`regulations/`).
4. **Mandatory 11-State Evidence Taxonomy:**
   Every legal rule, claim, and observation must use one of:
   `VERIFIED_PRIMARY`, `VERIFIED_SECONDARY`, `PARTIALLY_VERIFIED`, `CONFLICTING`, `UNVERIFIED`, `PRIMARY_SOURCE_REQUIRED`, `EXPERIMENT_REQUIRED`, `HUMAN_REVIEW_REQUIRED`, `SUPERSEDED`, `NOT_APPLICABLE`, `REJECTED`.
5. **No Synthetic or Fabricated Benchmarks:**
   Never commit made-up accuracy numbers or benchmark metrics. Use `TBD — MEASURE` until empirical results are generated under `benchmarks/results/` and logged in `experiments/`.

---

## Development Workflow

1. **Branching:** Create feature branches (`feat/`, `fix/`, `docs/`, `rules/`).
2. **Pre-Commit Checks:** Run automated verification scripts prior to committing:
   ```bash
   python scripts/verification/verify_legal_sources.py
   python scripts/verification/verify_rule_registry.py
   python scripts/verification/verify_claims.py
   python scripts/verification/verify_dataset_manifest.py
   ```
3. **Pull Requests:** Ensure your PR links to a documented task or problem statement requirement in `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`. Any new claim must be logged in `docs/17_CLAIMS/CLAIMS_REGISTER.md`.
