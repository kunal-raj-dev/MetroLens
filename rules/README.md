# Machine-Readable Rules Engine Directory

This directory contains declarative, machine-readable representations of verified Legal Metrology (Packaged Commodities) rules.

## Strict Lifecycle & Segregation Policy

Rules transition through a formal multi-stage directory lifecycle:

```
rules/
├── schema/       # JSON Schemas governing rule structures
├── proposed/     # Candidate or drafted rule definitions (Awaiting primary source verification)
├── verified/     # Verified against authoritative primary source, awaiting commencement date
├── current/      # Active rules IN FORCE with verified commencement dates
├── historical/   # Historical rules active in prior regulatory windows (for retrospective audits)
├── superseded/   # Deprecated or replaced rule versions
├── tests/        # Pytest test suites testing rule evaluators against test vectors
└── fixtures/     # Test fixture packages with synthetic or validated ground truth
```

### Inviolable Rule:
`rules/current/` **MUST contain ONLY rules whose `instrument_status == "IN_FORCE"` and whose `verification_status == "VERIFIED_PRIMARY"` from a verified primary source document.**
No placeholders, no draft amendments, and no unverified interpretations are permitted in `rules/current/`.
Any rule whose primary text is pending verification must reside in `rules/proposed/` with status `PRIMARY_SOURCE_REQUIRED`.
