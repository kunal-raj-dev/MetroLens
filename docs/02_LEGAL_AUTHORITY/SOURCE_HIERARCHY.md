# Legal Source Hierarchy & Precedence Rules

## Purpose
Establishes the strict hierarchy of authority used to resolve ambiguities, evaluate legal claims, and govern the ingestion of regulatory rules.

## Scope
Universal across all legal, vision, and rule-engineering modules.

## Authoritative Inputs
- Indian Jurisprudence on Delegated Legislation and Statutory Interpretation.

## Assumptions
- Subordinate legislation (Rules) cannot override primary enactments (Acts). In case of conflict, Level 1 primary acts and official gazettes strictly govern.

## Open Questions
- Interplay between Legal Metrology (Packaged Commodities) Rules and Food Safety and Standards (Packaging and Labelling) Regulations [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `regulations/source_registry.yaml`

## Verification Requirements
- No rule or threshold may be derived from Level 4 or Level 5 sources.

---

## The 5-Level Source Hierarchy

```
┌────────────────────────────────────────────────────────┐
│ LEVEL 1: PRIMARY GOVERNMENT AUTHORITY                  │
│ • The Gazette of India                                 │
│ • The Legal Metrology Act, 2009 (India Code)           │
│ • Official LMPC Rules & Gazette Amendments             │
│ • Department of Consumer Affairs (DoCA) Notifications  │
│ • Official SIH Problem Statement Documents             │
└───────────────────────────┬────────────────────────────┘
                            │ Outranks
                            ▼
┌────────────────────────────────────────────────────────┐
│ LEVEL 2: OFFICIAL SUPPORTING MATERIAL                  │
│ • Official DoCA FAQs and Advisory Circulars            │
│ • Official Implementation Guidelines                   │
│ • Bureau of Indian Standards (BIS) Referenced Codes    │
│ • Official Government Datasets (data.gov.in)           │
└───────────────────────────┬────────────────────────────┘
                            │ Outranks
                            ▼
┌────────────────────────────────────────────────────────┐
│ LEVEL 3: PEER-REVIEWED TECHNICAL / STANDARDS           │
│ • Peer-reviewed academic vision & metrology papers     │
│ • OIML International Recommendations (e.g. OIML R 87)  │
│ • ISO/IEC Standards (e.g. ISO/IEC 17025)               │
│ • Official open-source library documentation           │
└───────────────────────────┬────────────────────────────┘
                            │ Outranks
                            ▼
┌────────────────────────────────────────────────────────┐
│ LEVEL 4: REPUTABLE SECONDARY SOURCES                   │
│ • Authoritative legal commentaries on Metrology law    │
│ • Recognized industry association compliance manuals   │
└───────────────────────────┬────────────────────────────┘
                            │ Outranks
                            ▼
┌────────────────────────────────────────────────────────┐
│ LEVEL 5: DISCOVERY ONLY (NEVER LEGAL AUTHORITY)        │
│ • Blogs, news articles, web forums, Reddit             │
│ • AI-generated summaries, search snippets              │
│ *LEVEL 5 IS STRICTLY RESTRICTED TO HYPOTHESIS FORMATION│
│ CAN NEVER ESTABLISH A LEGAL FACT OR THRESHOLD*         │
└────────────────────────────────────────────────────────┘
```

### Precedence Conflict Rules:
1. Level 1 completely outranks Levels 2 through 5.
2. If two Level 1 documents appear to conflict (e.g., an earlier rule vs. a later amendment), the subsequent amendment governs from its explicit commencement date.
3. If no commencement date is specified, or language is ambiguous, the system records a `CONFLICT` record and sets rule status to `BLOCKED`. Never resolve statutory conflict by statistical AI guessing.
