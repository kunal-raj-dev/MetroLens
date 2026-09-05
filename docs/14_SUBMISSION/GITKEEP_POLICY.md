# NIRIKSHAK — REPOSITORY GITKEEP & SCAFFOLD GOVERNANCE POLICY

**Policy Standard:** Anti-Hallucination & Artifact Integrity Directive  
**Effective Date:** 2026-09-04  
**Audit Standard:** Strict Separation of Intent from Physical Existence (Truth > Appearance)  
**Authority:** Principal Software Architect, Security Engineer, QA Lead

---

## 1. Core Foundational Principle

```
================================================================================
                         TRUTH > APPEARANCE
================================================================================
```

The objective of repository governance in Project Nirikshak is **NOT** to create the visual illusion of a finished, production-deployed system.  
The objective is to ensure that **every claim made in documentation, manifests, and commit logs accurately reflects physical disk reality**.

---

## 2. Definitive Semantic Meaning of Repository Artifacts

### 2.1 What a `.gitkeep` Means
A `.gitkeep` file has exactly one legitimate meaning:
> *"This directory is intentionally reserved in Git to establish a modular architectural boundary for artifacts that will be generated, acquired, or authored in a later project stage."*

### 2.2 What a `.gitkeep` NEVER Means
Under the Nirikshak Governance Policy, a `.gitkeep` file:
- **NEVER** means that an artifact exists.
- **NEVER** means that code is implemented.
- **NEVER** means that a dataset has been collected.
- **NEVER** means that a model has been trained.
- **NEVER** means that an experiment has been run.
- **NEVER** means that a benchmark has been completed.

---

## 3. Strict Non-Negotiable Invariants

| Domain | Prohibited Invariant (Violation) | Mandatory Governance Rule |
| :--- | :--- | :--- |
| **Datasets (`data/`)** | A manifest or README claiming a dataset exists when the directory contains only `.gitkeep`. | The manifest must explicitly label the dataset `status: PLANNED`, `artifact_status: NOT_GENERATED` or `DECLARED_BUT_MISSING`. |
| **Benchmarks (`benchmarks/`)** | Claiming a benchmark has been completed or citing accuracy metrics when `benchmarks/results/` contains only `.gitkeep`. | Metrics must be labeled `TARGET — NOT VALIDATED; Status: TBD — MEASURE` and benchmarks designated `BENCHMARK_NOT_RUN`. |
| **Experiments (`experiments/`)** | Describing an optical or ML trial as "validated" when `experiments/runs/` contains only `.gitkeep`. | The experiment must be classified as `SPECIFIED_ONLY` or `READY_TO_RUN`, never `RESULT_VERIFIED`. |
| **Applications (`apps/`, `packages/`)** | Calling a service or package "implemented", "functional", or "production-ready" when only `.gitkeep` exists. | The component must be explicitly classified as `SCAFFOLD_ONLY` or `SPECIFIED_PRE_IMPLEMENTATION`. |
| **Legal Sources (`regulations/`, `rules/`)** | Promoting a rule to `rules/current/` or claiming a statute is verified when primary Gazette PDFs are absent. | The rule must remain in `rules/proposed/` with `executable: false` and `verification_status: PRIMARY_SOURCE_REQUIRED`. |
| **Infrastructure (`infra/`)** | Describing Docker or orchestration templates as "deployed production infrastructure" when applications are scaffolds. | The infrastructure must be designated `DEVELOPMENT SCAFFOLD (PRE-IMPLEMENTATION)`. |

---

## 4. The Three Semantic Domains

In any review, pitch, or documentation audit, the system strictly separates three distinct domains:

1. **A Documentation Statement Means:**  
   *"This is our intended architecture, functional requirement, or mathematical algorithm."*  
   $ightarrow$ It **NEVER** means: *"This has been empirically proven on physical hardware."*

2. **A Manifest Entry Means:**  
   *"This dataset or regulatory source is cataloged and its schema is defined."*  
   $ightarrow$ It **NEVER** means: *"The physical dataset or primary PDF already exists on disk."*

3. **Physical Artifacts & Reproducible Tests Mean:**  
   *"This code compiles, this automated test passes, and this SHA-256 hash matches the file on disk."*  
   $ightarrow$ **This, and only this, constitutes verified truth.**

---

## 5. Permissible vs. Prohibited Use of `.gitkeep`

### Permissible Use (Encouraged):
- Holding directories for external weights intentionally excluded from Git due to file size (`models/weights/.gitkeep`).
- Holding directories for physical primary source PDFs to be retrieved by legal counsel (`regulations/sources/.gitkeep`).
- Reserving modular package directories during pre-implementation architecture design (`packages/vision/.gitkeep`).

### Prohibited Use (Strictly Barred):
- Inserting `.gitkeep` into a directory and claiming the dataset is collected.
- Creating empty files named `result.json` or `output.txt` to trick CI scripts into reporting successful runs.
- Failing to document missing physical artifacts in audit registers.

---

**Policy Approval:**  
*Principal Software Architect & Lead Auditor, Project Nirikshak*  
*SIH 2026 — PS 26034*
