# AI CONTEXT: MEMBER 5 — PROJECT CONTEXT & DESIGN SPECIFICATION
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Last Updated:** 2026-09-05T18:25:00+05:30  
**Phase:** Chunk M5-5 (Complete)

---

## 1. Product Identity & Purpose
MetroLens AI is a sovereign **Officer Inspection Workstation & Evidence Analysis System** built for District Legal Metrology Officers (LMOs), state enforcement directorates, and hackathon judging juries. It transforms manual, error-prone ruler-and-magnifier compliance checks under the *Legal Metrology (Packaged Commodities) Rules, 2011* into a mathematically verified, auditable, sub-2.5-second automated verification workflow.

---

## 2. Visual Language & Sovereign Design Tokens
- **Design Philosophy**: Mastercard-inspired high-trust magazine feel, clean tactile surfaces, authoritative typography, and extreme radii.
- **Canvas Base**: Putty cream `#F3F0EE` (light, high-trust sovereign workstation).
- **Surface Elevation**: `#FFFFFF` cards with 40px stadium radii, subtle `#000000/0.06` borders, and soft diffuse halo shadows.
- **Headline Styling**: Ghost cream-on-cream watermark layer (`METROLENS` in 180px bold sans tracking-tighter) layered behind high-contrast text.
- **Pill Primitives**: 999px fully rounded pill buttons and badges for mode toggles, status indicators, and actions.
- **Signal Accents**: Signal Orange (`#EB5B28` / `#C84617`) for satellite action prompts and focused evidence highlights.

---

## 3. Four Core Statutory Statuses (PCR, 2011)
Every status communicates via **Color + Icon + Text Label + Plain Language Explanation**:
1. **COMPLIANT** (Emerald / Green) — `ShieldCheck` icon: All Rule 6 mandatory declarations detected; measured numeral heights satisfy Rule 7 minimums; Rule 6(11) Unit Sale Price mathematically verified.
2. **NON_COMPLIANT** (Crimson / Red) — `AlertTriangle` icon: Missing mandatory declaration, numeral height below statutory threshold, or Rule 12 prohibited unit ('gms').
3. **SUSPECT_REVIEW** (Amber / Gold) — `HelpCircle` icon: Uncalibrated frame, borderline measurement within uncertainty interval, or degraded/faded thermal stamp.
4. **INCONCLUSIVE** (Slate / Neutral) — `FileQuestion` icon: Quality gate rejected (Laplacian variance $<50.0$, specular glare), or zero readable text detected.

---

## 4. Benchmark Demonstration Catalog (8 Verified Packages)
1. `SYNTH-01-ENG-FMCG`: Standard English Biscuit Pouch (Rule 6 Pass, 5 declarations)
2. `SYNTH-02-HIN-FMCG`: Pure Hindi FMCG Atta Bag (Devanagari script, valid ₹ currency symbol)
3. `SYNTH-03-BIL-FMCG`: Bilingual Snack Carton (English + Hindi bilingual compliance)
4. `SYNTH-04-MICRO-FONT`: Shrinkflation Micro-Font Confectionery Pouch (Rule 7 font height deficit)
5. `SYNTH-05-LIQUID-VOLUME`: Handwash Liquid Volume Bottle (Volume ml metric pass)
6. `SYNTH-06-PROHIBITED-UNITS`: Detergent Pouch (Rule 12 non-standard 'gms' deficit)
7. `SYNTH-07-BLANK-FRAME`: Blank Cardboard Frame (Laplacian quality gate rejection)
8. `SYNTH-08-LOW-CONTRAST-FADED`: Low-Contrast Foil Packaging (Suspect review case)

---

## 5. Sovereign Guardrails & Non-Goals
- **No Client-Side Legal Calculation**: The browser never adjudicates Rule 6/7 legality or calculates font millimeter sizes.
- **No Fake Client PDFs**: Reports must be generated authoritatively by `POST /api/v1/report/pdf`. If offline, report service unavailability is cleanly reported.
- **No Silent Mock Fallback**: Live network errors display actionable alerts; they never secretly pretend to succeed with mock data.
- **No Unsafe State Persistence**: Sessions reset completely via "New Inspection" to prevent cross-inspection evidence contamination.
