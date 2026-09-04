# ADR-005: Date-of-Manufacture Temporal Regulatory Snapshotting

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Legal Engineering Lead, Rule Engine Lead

---

## Context & Problem Statement
The Legal Metrology (Packaged Commodities) Rules, 2011 have undergone numerous statutory amendments (e.g. 2017 amendments, 2021 amendments, 2022 amendments introducing unit sale price, 2024 revisions). In legal metrology, a pre-packaged commodity is governed by the law in force at the time of its manufacture or packaging, not the date of inspection.

Evaluating a package manufactured in 2019 under the 2022 amendment rules would result in an illegal, invalid prosecution.

We must decide how regulatory rules are resolved and executed against inspected goods.

---

## Decision Drivers
- **Non-Retroactivity of Penal Laws**: Article 20(1) of the Constitution of India forbids retroactive imposition of greater penalties or new offenses.
- **Audit Defensibility**: Clear legal justification showing which specific Gazette notification was active on the date of packaging.

---

## Considered Options
1. **Option 1: Temporal Regulatory Snapshotting by Date of Packaging** (Chosen)
   - Extract the month/year of manufacture or import, resolve the active statutory epoch, and load the specific versioned ruleset active during that epoch.
2. **Option 2: Fixed Current Ruleset**
   - Evaluating all packages against today's rules.
3. **Option 3: Manual Rule Selection by Officer**
   - Requiring the inspecting officer to manually select which rulebook to apply.

---

## Decision Outcome
**Chosen Option:** Option 1: Temporal Regulatory Snapshotting by Date of Packaging.
The rule engine parses the package's declared date of packaging (`mfg_date`), maps it to the corresponding statutory epoch, and executes the specific ruleset version corresponding to that temporal window.

### Positive Consequences
- Prevents unlawful retroactive statutory penalties.
- Accurately inspects warehouse stock, slow-moving retail goods, and historical inventory.

### Negative Consequences / Trade-offs
- Requires maintaining versioned rule directories (`rules/current/`, `rules/historical/`).
- If the packaging date is illegible or missing, the system must trigger a specific violation for missing date rather than applying an assumed ruleset.

---

## References & Statutory Linkages
- Constitution of India, Article 20(1).
- Legal Metrology (Packaged Commodities) Rules, 2011, Rule 6(1)(d).
