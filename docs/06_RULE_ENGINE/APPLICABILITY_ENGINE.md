# Applicability Engine Specification

## Purpose
Defines the decision logic used to determine whether a given packaged commodity falls under the jurisdiction of Chapter II (Packages intended for retail sale) or Chapter III (Wholesale packages) of the LMPC Rules 2011.

## Scope
Executes preliminary scoping prior to detailed declaration checking.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Chapter I, Rule 2 and Rule 3).

## Assumptions
- Standard retail packaged commodities sold directly to consumers fall under Chapter II.

## Open Questions
- Categorization of industrial lubricants and institutional chemicals sold through commercial hardware outlets [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `rules/schema/applicability.schema.json`

## Verification Requirements
- All commodity categories must be verified against `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/applicability_matrix.yaml`.

---

## Applicability Decision Tree

```
                     [Packaged Commodity Ingested]
                                   │
                                   ▼
                    [Is Net Quantity ≤ 10g or ≤ 10ml?]
                     (Excluding tobacco / pan masala)
                        ├── YES ──► [Verdict: EXEMPT under Rule 3(a)]
                        └── NO
                                   │
                                   ▼
             [Is it Fast Food packed by hotel/restaurant?]
                        ├── YES ──► [Verdict: EXEMPT under Rule 3(b)]
                        └── NO
                                   │
                                   ▼
           [Is it sold to an Institutional / Industrial Consumer?]
          (With explicit notice 'Not for Retail Sale' marked)
                        ├── YES ──► [Verdict: PARTIALLY EXEMPT from MRP]
                        └── NO
                                   │
                                   ▼
                   [Is Net Quantity > 25kg or > 25L?]
                     (Excluding cement & fertilizer)
                        ├── YES ──► [Verdict: EXEMPT under Rule 3(c)]
                        └── NO
                                   │
                                   ▼
              [STANDARD RETAIL COMMODITY: CHAPTER II MANDATORY]
               Evaluate Rules 6, 7, 8, 9, 10, 11, 18.
```
