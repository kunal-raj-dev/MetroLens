# Project Charter — Nirikshak (निरीक्षक)

## Purpose
The purpose of Project Nirikshak is to engineer a dependable, transparent, and auditable computer-vision and rule-evaluation system to assist authorized Legal Metrology enforcement officers in verifying packaged commodity compliance under Indian statutory law.

## Scope
The project encompasses guided multi-panel image capture, automated image quality gating, optical character recognition (OCR), physical reference calibration, principal display panel (PDP) segmentation, deterministic rule verification, cryptographic chain-of-custody logging, and formal inspection dossier generation.

## Authoritative Inputs
1. Smart India Hackathon (SIH) 2026 — Problem Statement 26034.
2. The Legal Metrology Act, 2009 (Act No. 1 of 2010).
3. The Legal Metrology (Packaged Commodities) Rules, 2011 (G.S.R. 202(E)) as amended.
4. Official directives, implementation guidelines, and FAQs published by the Department of Consumer Affairs (DoCA).

## Assumptions
- The system will be utilized as an operational aid by trained inspection personnel rather than an autonomous prosecutorial bot.
- Mobile and desktop hardware will have access to standard high-resolution camera sensors ($\ge 12\text{ MP}$) and sufficient local compute for offline execution.
- Physical reference objects (e.g. standard calibration card or coin) will be introduced in calibration-critical captures.

## Open Questions
- Specific provincial amendments or State Legal Metrology Enforcement Rules adaptations across Indian states [TBD — PRIMARY SOURCE REQUIRED].
- Official API endpoint specifications for the National Consumer Helpline or Departmental Portal integration [TBD — PRIMARY SOURCE REQUIRED; NO FAKE APIS].

## Dependencies
- Canonical source registry (`regulations/source_registry.yaml`).
- Machine-readable rule catalog (`rules/schema/`).
- Automated verification test suite (`scripts/verification/`).

## Verification Requirements
- The project charter must be approved by the core engineering and legal engineering leads.
- All functional capabilities derived from this charter must trace directly to requirements in `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`.

---

## Strategic Objectives & Success Metrics

1. **Zero Hallucination Compliance:**
   Zero fabricated legal citations, section numbers, or automated prosecutorial verdicts. Ambiguous or borderline findings must strictly route to human officer `REVIEW`.

2. **Empirical Measurement Validity:**
   No pixel-based dimension claims without optical reference calibration. Verification must prove font height accuracy within bounded uncertainty ($\le \pm 0.2\text{ mm}$ on calibrated targets).

3. **Multi-Panel Evidence Provenance:**
   Every finding is linked to an immutable cryptographic evidence graph (raw capture $\rightarrow$ ROI crop $\rightarrow$ OCR tokens $\rightarrow$ calibrated measurement $\rightarrow$ applicable rule $\rightarrow$ officer sign-off).

4. **Offline Operational Autonomy:**
   Core inspection, OCR, and deterministic rule evaluation execute completely offline on field laptops or mobile workstations without internet connectivity.
