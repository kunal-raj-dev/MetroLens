# Mandatory Field Extraction & Normalization

## Purpose
Specifies the rule-assisted parsing algorithms, regular expression grammars, and named-entity normalization rules used to map raw OCR tokens into structured statutory fields under Rule 6(1).

## Scope
Covers the 7 mandatory declaration categories mandated on pre-packaged commodities.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 6).

## Assumptions
- Declarations may appear anywhere on the package (or specifically on the Principal Display Panel depending on the specific field).

## Open Questions
- Standardizing extraction of varied multi-entity manufacturing agreements (e.g. "Manufactured by X for Y, marketed by Z") [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/extraction/`
- `rules/schema/evidence.schema.json`

## Verification Requirements
- Field extraction precision and recall must be benchmarked on `benchmarks/datasets/`.

---

## The 7 Mandatory Declaration Grammars

```
┌────────────────────────────────────────────────────────┐
│ MANDATORY STATUTORY FIELD                              │
├───────────────────────────┬────────────────────────────┤
│ 1. Manufacturer / Packer  │ Regex keywords: Mfd by,    │
│    / Importer Details     │ Pkd by, Manufactured by,   │
│                           │ Imported by, Regd Office.  │
├───────────────────────────┼────────────────────────────┤
│ 2. Country of Origin      │ Regex: Country of Origin:, │
│                           │ Made in India / [Country]. │
├───────────────────────────┼────────────────────────────┤
│ 3. Common / Generic Name  │ Commodity title token near │
│                           │ brand name or description. │
├───────────────────────────┼────────────────────────────┤
│ 4. Net Quantity           │ Regex: Net (Qty|Weight|Vol)│
│                           │ (\d+(\.\d+)?)\s*(g|kg|ml|l)│
├───────────────────────────┼────────────────────────────┤
│ 5. Date of Manufacture /  │ Regex: (Mfg|Pkd|Import):   │
│    Packing / Import       │ (MM/YYYY|MM/YY|DD/MM/YYYY) │
├───────────────────────────┼────────────────────────────┤
│ 6. Maximum Retail Price   │ Regex: MRP\s*(Rs\.?|INR|₹) │
│    & Unit Sale Price      │ (\d+(\.\d+)?)\s*incl taxes │
├───────────────────────────┼────────────────────────────┤
│ 7. Consumer Care Details  │ Regex: Consumer Care, Toll │
│                           │ Free, Email, Phone, Address│
└───────────────────────────┴────────────────────────────┘
```

### Normalization Logic:
1. **Net Quantity Normalization:** Convert all units to standard SI metric base (e.g., $500\text{ gm} \rightarrow 500\text{ g}$, $1.5\text{ Litres} \rightarrow 1500\text{ ml}$).
2. **MRP Normalization:** Verify explicit presence of *"inclusive of all taxes"*. If missing, flag statutory defect under Rule 6(1)(e).
3. **Date Normalization:** Convert ambiguous date expressions into standardized ISO YYYY-MM format to establish the applicable regulatory snapshot epoch.
