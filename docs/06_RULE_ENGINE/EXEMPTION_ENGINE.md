# Statutory Exemption Engine Specification

## Purpose
Defines the programmatic evaluators that verify claims of statutory exemptions under Rule 3 and Rule 26 of the LMPC Rules 2011.

## Scope
Prevents spurious violation notices from being issued against legally exempt packaging configurations.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 3 and Rule 26).
- `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/exemption_catalog.yaml`.

## Assumptions
- Exemption claims require explicit corroborating photographic evidence (e.g. proof of net weight $\le 10\text{ g}$ or presence of institutional markings).

## Open Questions
- Departmental interpretations on combination packs where one item is exempt and another non-exempt [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/rules-engine/`

## Verification Requirements
- Test cases in `tests/rules/test_exemptions.py` must verify all statutory exemption paths.

---

## Exemption Verification Evaluators

1. **Small Quantity Exemption Evaluator:**
   - Input: Detected Net Quantity ($Q$) and Commodity Category.
   - Evaluator: If $Q \le 10\text{ g}$ or $Q \le 10\text{ ml}$ AND category $\notin \{\text{"tobacco"}, \text{"pan\_masala"}\}$, return `EXEMPT`.

2. **Bulk Agricultural & Industrial Exemption Evaluator:**
   - Input: Detected Net Quantity ($Q$) and Commodity Category.
   - Evaluator: If $Q > 25\text{ kg}$ or $Q > 25\text{ L}$ AND category $\notin \{\text{"cement"}, \text{"fertilizer"}\}$, return `EXEMPT`.

3. **Institutional Consumer Exemption Evaluator:**
   - Input: Text tokens across all panels.
   - Evaluator: If tokens match phrase `"FOR INSTITUTIONAL CONSUMER USE ONLY"` or `"NOT FOR RETAIL SALE"`, mark MRP rule as `NOT_APPLICABLE` and log notice for officer review.
