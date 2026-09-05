# Problem Solving Case Specification

## Criterion
Problem Solving & Alignment with Statutory Enforcement Reality

## What Judges Need to Believe
1. The team deeply understands the real-world operational challenges of an Inspector of Legal Metrology in India (manual caliper measurements, visual fatigue, confusing packaging shapes, defending seizure memos in compounding trials).
2. The solution directly eliminates enforcement bottlenecks rather than presenting an academic computer vision demo detached from statutory procedure.

## Evidence Required
- Verification against the Legal Metrology Act, 2009 and Packaged Commodities Rules, 2011.
- Clear operational mappings in `docs/03_PRODUCT_REQUIREMENTS/USER_JOURNEYS.md`.

## Nirikshak Feature
1. **Automated PDP Area & Font Height Check:** Replaces manual geometric calculations and magnifying-glass inspection with instant physical measurement in millimetres.
2. **Deterministic Declarations Extraction:** Automatically detects the 7 mandatory declarations under Rule 6(1).
3. **Cryptographic Evidence Dossier:** Generates tamper-evident PDF dossiers that preserve chain-of-custody for compounding hearings.

## Demo Proof
Live inspection of a commercial retail package with simultaneous PDP area calculation ($124\text{ cm}^2$), Net Qty font height evaluation ($2.15\text{ mm}$ vs $2.0\text{ mm}$ statutory limit), and instant PDF report export.

## Benchmark Proof
Time reduction from manual inspection ($\approx 8\text{ to }15\text{ minutes}$) to guided inspection ($\le 30\text{ seconds}$). Empirical baseline: `TBD — MEASURE`.

## Known Weakness
Severely crushed or mutilated packages cannot establish a planar surface and must be routed to manual officer inspection.

## Answer to Likely Judge Challenge
- **Judge Challenge:** *"Why can't an inspector just glance at the package like they do today?"*
- **Answer:** *"Visual examination of 1.0 mm or 1.5 mm text under warehouse fluorescent lights is subjective and causes severe eye fatigue across hundreds of packages. Furthermore, visual estimates fail in compounding hearings when corporate manufacturers challenge the seizure. Nirikshak provides objective, calibrated optical evidence backed by SHA-256 hashes."*
