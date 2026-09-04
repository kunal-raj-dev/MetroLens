# User Personas Specification

## Purpose
Profiles the core operational personas interacting with Nirikshak, detailing their responsibilities, pain points, statutory workflows, and technical constraints.

## Scope
Informs UI/UX design, access controls, reporting structures, and error messaging.

## Authoritative Inputs
- Field inspection workflows governed by the Legal Metrology Act, 2009.

## Assumptions
- Primary users are government enforcement officers, supervisors, and administrative personnel.

## Open Questions
- State-level training protocols and specialized device deployment policies [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/03_PRODUCT_REQUIREMENTS/USER_JOURNEYS.md`
- `docs/09_SECURITY_PRIVACY/RBAC.md`

## Verification Requirements
- UI flows must be validated against the technical capability and operational constraints of each persona.

---

## 1. Primary Persona: Field Inspector of Legal Metrology
- **Name:** Inspector Rajesh Sharma (Field Enforcement Officer)
- **Environment:** Busy retail supermarkets, wholesale mandis, remote godowns, often with low cellular connectivity and fluorescent lighting.
- **Responsibilities:**
  - Conducting physical retail market surveillance.
  - Examining packaged commodities on retail shelves.
  - Verifying mandatory statutory declarations and net quantity markings.
  - Generating inspection memos and seizing non-compliant packaging samples.
- **Key Pain Points:**
  - Manually reading tiny 1 mm fonts on hundreds of diverse packages causes visual fatigue.
  - Calculating PDP areas on non-rectangular or curved bottles manually is slow and prone to mathematical error.
  - Defending borderline measurement notices against corporate legal pushback.
- **System Need:** Fast, guided multi-panel camera capture, automated blur rejection, objective physical font measurement with clear visual overlays, and offline dossier generation.

## 2. Secondary Persona: Senior Metrology Officer / Controller
- **Name:** Smt. Ananya Sen (Deputy Controller / Adjudicating Officer)
- **Environment:** Directorate / Regional Office workstation.
- **Responsibilities:**
  - Reviewing inspection reports submitted by field officers.
  - Deciding compounding applications or sanctioning formal court prosecutions.
  - Auditing inspection consistency across districts.
- **Key Pain Points:**
  - Dealing with poorly documented seizure memos and blurry cellphone photos that fail judicial scrutiny.
  - Inconsistent rule interpretation among junior field inspectors.
- **System Need:** Cryptographically verifiable inspection dossiers with high-resolution crops, exact statutory citations, and auditable operator logs.

## 3. Tertiary Persona: Systems Administrator & Standards Custodian
- **Name:** Vikram Mehta (Technical & Regulatory Admin)
- **Responsibilities:** Managing model deployment, enrolling field officers, and updating the machine-readable rule catalog when new Gazette amendments are notified.
- **System Need:** Strict rule validation tooling, immutable audit logs, and automated schema checks.
