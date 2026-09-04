# Team Roles & Ownership Matrix

## Purpose
Establishes discrete engineering roles, code ownership zones, review responsibilities, and presentation tracks for the Nirikshak project team.

## Scope
Universal across development, testing, and live presentation.

## Authoritative Inputs
- Standard software engineering RACI (Responsible, Accountable, Consulted, Informed) model.

## Assumptions
- Every package and documentation directory has a dedicated technical owner.

## Dependencies
- All repository directories.

## Verification Requirements
- PR reviews must be approved by the designated code owner before merge.

---

## Ownership Matrix (RACI)

| Subsystem / Directory | Primary Lead / Owner | Accountable Role | Backup Engineer |
| :--- | :--- | :--- | :--- |
| **`regulations/` & `docs/02_`** | Legal Engineering Lead | Principal Software Architect | QA Lead |
| **`rules/` & `packages/rules-engine/`**| Rule Engine Lead | Principal Software Architect | Legal Engineering Lead |
| **`packages/vision/` & `calibration/`**| Computer Vision Lead | Principal Software Architect | AI/OCR Engineer |
| **`packages/ocr/` & `extraction/`** | AI / OCR Lead | Computer Vision Lead | Backend Engineer |
| **`packages/evidence/` & `reporting/`**| Systems & Security Lead| QA Lead | Backend Engineer |
| **`apps/web/` (Frontend UI)** | Frontend Lead | Full-Stack Engineer | UX Designer |
| **`apps/api/` & `infra/`** | Backend / Infra Lead | Principal Software Architect | Security Lead |
| **`benchmarks/` & `experiments/`** | QA / Metrology Lead | AI / OCR Lead | Computer Vision Lead |
| **Judging Strategy & Demo** | Hackathon Lead | All Team Leads | Presentation Speaker |
