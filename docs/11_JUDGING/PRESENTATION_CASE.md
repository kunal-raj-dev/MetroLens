# 5-Minute Evaluation Pitch & Presentation Strategy

## Purpose
Provides the timed script, slide narrative, rhetorical strategy, and stage presence guidelines for the 5-minute hackathon evaluation round.

## Scope
Universal for the pitching team.

## Authoritative Inputs
- Standard SIH evaluation format: 3 to 5-minute pitch followed by 3-minute Q&A.

## Assumptions
- Strict time enforcement by judges: every second must deliver dense technical and legal proof points.

## Dependencies
- `docs/11_JUDGING/DEMO_SCRIPT.md`

## Verification Requirements
- Team must rehearse and finish within 4 minutes and 30 seconds, leaving 30 seconds buffer.

---

## Timed Pitch Structure (Total: 4 Min 30 Sec)

### Minute 0:00 - 0:45 | The Statutory Challenge & Reality
- *"Every packaged commodity in India is governed by the Legal Metrology Act and the 2011 Rules. Millions of packages are sold daily, yet enforcement officers still examine tiny 1 mm fonts with manual magnifying glasses and calipers. Blurry smartphone photos get thrown out in court. We built Nirikshak: an auditable, offline inspection system that bridges the physical-digital divide."*

### Minute 0:45 - 1:45 | Core Innovations (The 4 Pillars)
- **Point 1:** Physical scale calibration ($\text{mm/px}$) with bounded uncertainty—pixels are not millimetres.
- **Point 2:** The Regulatory Time-Machine—evaluating packages against rules active on their manufacturing date.
- **Point 3:** Separation of Observation from Adjudication—AI never determines legal guilt.
- **Point 4:** Tamper-evident evidence DAG with SHA-256 chain-of-custody.

### Minute 1:45 - 3:30 | Live Interactive Demonstration
- Execute live demo using physical package:
  1. Trigger blur check.
  2. Detect reference calibration card.
  3. Extract Rule 6 declarations.
  4. Measure Net Qty font height in mm vs. Table I.
  5. Toggle manufacturing date to show time-machine snapshot.
  6. Generate signed PDF dossier with cryptographic hash.

### Minute 3:30 - 4:15 | Scalability & Architecture
- Highlight pure local CPU execution, zero external cloud dependencies, offline SQLite storage, and modular YAML rule catalogs.

### Minute 4:15 - 4:30 | The Anti-Hallucination Close
- *"In a high-trust legal system, false certainty is fatal. Nirikshak never guesses, never fabricates rules, and routes uncertainty to human review. Thank you, we welcome your questions."*
