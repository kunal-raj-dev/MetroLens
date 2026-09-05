# Master Document Index — Project Nirikshak

This master index provides links to all engineering specifications, legal governance frameworks, architectural designs, and verification matrices across the Nirikshak repository.

---

## 1. Repository Root & Core Governance
- [README.md](..\..\README.md) — System overview, repository architecture, and setup instructions.
- [LICENSE](..\..\LICENSE) — Apache License 2.0.
- [CONTRIBUTING.md](..\..\CONTRIBUTING.md) — Contribution guidelines and anti-hallucination policies.
- [SECURITY.md](..\..\SECURITY.md) — Security policy, vulnerability disclosure, and cryptographic principles.
- [LEGAL_NOTICES.md](..\LEGAL_NOTICES.md) — Statutory disclaimers and legal limitations.
- [THIRD_PARTY_LICENSES.md](..\THIRD_PARTY_LICENSES.md) — Open source dependency license inventory.
- [DATA_LICENSES.md](..\DATA_LICENSES.md) — Dataset licenses and image provenance rules.

---

## 2. Project Charter & Scope (`docs/00_PROJECT_CHARTER/`)
- [PROJECT_CHARTER.md](..\00_PROJECT_CHARTER\PROJECT_CHARTER.md) — Project charter and strategic objectives.
- [SCOPE.md](..\00_PROJECT_CHARTER\SCOPE.md) — Full technical and operational scope.
- [MVP_SCOPE.md](..\00_PROJECT_CHARTER\MVP_SCOPE.md) — Scoped deliverables for hackathon demonstration.
- [NON_GOALS.md](..\00_PROJECT_CHARTER\NON_GOALS.md) — Explicit non-goals and out-of-scope declarations.
- [ASSUMPTIONS.md](..\00_PROJECT_CHARTER\ASSUMPTIONS.md) — Operational and technical assumptions.
- [GLOSSARY.md](..\00_PROJECT_CHARTER\GLOSSARY.md) — Statutory and engineering terminology glossary.

---

## 3. Problem Statement & Traceability (`docs/01_PROBLEM_STATEMENT/`)
- [SOURCE_RECORD.md](..\01_PROBLEM_STATEMENT\OFFICIAL_PS\SOURCE_RECORD.md) — Source record for Problem Statement 26034.
- [problem_statement_transcript.md](..\01_PROBLEM_STATEMENT\OFFICIAL_PS\problem_statement_transcript.md) — Verbatim problem statement text.
- [PS_REQUIREMENTS_MATRIX.md](..\01_PROBLEM_STATEMENT\PS_REQUIREMENTS_MATRIX.md) — Master PS requirements mapping and lifecycle stages.
- [REQUIREMENT_TRACEABILITY.md](..\01_PROBLEM_STATEMENT\REQUIREMENT_TRACEABILITY.md) — End-to-end statutory traceability matrix.

---

## 4. Legal Authority & Source Governance (`docs/02_LEGAL_AUTHORITY/`)
- [README.md](..\02_LEGAL_AUTHORITY\README.md) — Legal authority overview.
- [SOURCE_HIERARCHY.md](..\02_LEGAL_AUTHORITY\SOURCE_HIERARCHY.md) — 5-level legal source hierarchy.
- [SOURCE_REGISTER_GUIDE.md](..\02_LEGAL_AUTHORITY\SOURCE_REGISTER_GUIDE.md) — Guide to canonical source registry (`regulations/source_registry.yaml`).
- [LEGAL_CHANGELOG.md](..\02_LEGAL_AUTHORITY\LEGAL_CHANGELOG.md) — Chronological amendment history.
- [rule_catalog.yaml](..\02_LEGAL_AUTHORITY\VERIFIED_RULE_CATALOG\rule_catalog.yaml) — Verified rule catalog reference.
- [applicability_matrix.yaml](..\02_LEGAL_AUTHORITY\VERIFIED_RULE_CATALOG\applicability_matrix.yaml) — Statutory applicability matrix.
- [exemption_catalog.yaml](..\02_LEGAL_AUTHORITY\VERIFIED_RULE_CATALOG\exemption_catalog.yaml) — Statutory exemption catalog.
- [measurement_requirements.yaml](..\02_LEGAL_AUTHORITY\VERIFIED_RULE_CATALOG\measurement_requirements.yaml) — Physical measurement formulas.
- [effective_dates.yaml](..\02_LEGAL_AUTHORITY\VERIFIED_RULE_CATALOG\effective_dates.yaml) — Regulatory epochs timeline.
- [CHANGE_IMPACT_MATRIX.md](..\02_LEGAL_AUTHORITY\2026_AMENDMENTS\CHANGE_IMPACT_MATRIX.md) — 2026 amendments impact analysis.

---

## 5. Product Requirements (`docs/03_PRODUCT_REQUIREMENTS/`)
- [USER_PERSONAS.md](..\03_PRODUCT_REQUIREMENTS\USER_PERSONAS.md) — Inspector, supervisor, and admin personas.
- [USER_JOURNEYS.md](..\03_PRODUCT_REQUIREMENTS\USER_JOURNEYS.md) — Inspection operational workflows.
- [FUNCTIONAL_REQUIREMENTS.md](..\03_PRODUCT_REQUIREMENTS\FUNCTIONAL_REQUIREMENTS.md) — Functional specifications (FR-01 to FR-07).
- [NON_FUNCTIONAL_REQUIREMENTS.md](..\03_PRODUCT_REQUIREMENTS\NON_FUNCTIONAL_REQUIREMENTS.md) — Non-functional specifications (NFR-01 to NFR-05).
- [ACCEPTANCE_CRITERIA.md](..\03_PRODUCT_REQUIREMENTS\ACCEPTANCE_CRITERIA.md) — Gherkin acceptance test scenarios.
- [ERROR_STATE_REQUIREMENTS.md](..\03_PRODUCT_REQUIREMENTS\ERROR_STATE_REQUIREMENTS.md) — Error routing and failure behaviors.

---

## 6. System Architecture (`docs/04_ARCHITECTURE/`)
- [SYSTEM_ARCHITECTURE.md](..\04_ARCHITECTURE\SYSTEM_ARCHITECTURE.md) — System architecture and mermaid diagrams.
- [ARCHITECTURE_DECISIONS.md](..\04_ARCHITECTURE\ARCHITECTURE_DECISIONS.md) — Architecture decisions overview.
- [DATA_FLOW.md](..\04_ARCHITECTURE\DATA_FLOW.md) — Ingestion to dossier data pipeline.
- [AI_PIPELINE.md](..\04_ARCHITECTURE\AI_PIPELINE.md) — AI vision observation pipeline.
- [RULE_ENGINE.md](..\04_ARCHITECTURE\RULE_ENGINE.md) — Deterministic rule engine architecture.
- [EVIDENCE_ARCHITECTURE.md](..\04_ARCHITECTURE\EVIDENCE_ARCHITECTURE.md) — Cryptographic provenance DAG.
- [SECURITY_ARCHITECTURE.md](..\04_ARCHITECTURE\SECURITY_ARCHITECTURE.md) — Security and encryption architecture.
- [OFFLINE_ARCHITECTURE.md](..\04_ARCHITECTURE\OFFLINE_ARCHITECTURE.md) — Offline edge execution model.

---

## 7. AI & Computer Vision (`docs/05_AI_VISION/`)
- [OCR_STRATEGY.md](..\05_AI_VISION\OCR_STRATEGY.md) — Multilingual OCR strategy.
- [TEXT_DETECTION.md](..\05_AI_VISION\TEXT_DETECTION.md) — Bounding box localization algorithms.
- [CURVED_SURFACE_PROCESSING.md](..\05_AI_VISION\CURVED_SURFACE_PROCESSING.md) — Cylinder dewarping.
- [IMAGE_QUALITY_GATE.md](..\05_AI_VISION\IMAGE_QUALITY_GATE.md) — Blur and glare detection gates.
- [FIELD_EXTRACTION.md](..\05_AI_VISION\FIELD_EXTRACTION.md) — Mandatory field parsing rules.
- [PDP_DETECTION.md](..\05_AI_VISION\PDP_DETECTION.md) — Principal Display Panel segmentation.
- [FONT_MEASUREMENT.md](..\05_AI_VISION\FONT_MEASUREMENT.md) — Millimetre font height measurement.
- [CALIBRATION.md](..\05_AI_VISION\CALIBRATION.md) — Reference target optical calibration.
- [MODEL_EVALUATION.md](..\05_AI_VISION\MODEL_EVALUATION.md) — Model evaluation benchmark metrics.

---

## 8. Rule Engine & Statutory Logic (`docs/06_RULE_ENGINE/`)
- [RULE_ENGINE_SPEC.md](..\06_RULE_ENGINE\RULE_ENGINE_SPEC.md) — Rule evaluation engine specification.
- [APPLICABILITY_ENGINE.md](..\06_RULE_ENGINE\APPLICABILITY_ENGINE.md) — Statutory applicability decision trees.
- [EXEMPTION_ENGINE.md](..\06_RULE_ENGINE\EXEMPTION_ENGINE.md) — Statutory exemptions evaluators.
- [VERSIONING.md](..\06_RULE_ENGINE\VERSIONING.md) — Regulatory time-machine versioning.
- [CONFLICT_RESOLUTION.md](..\06_RULE_ENGINE\CONFLICT_RESOLUTION.md) — Cross-panel contradiction detection.
- [RULE_TEST_STRATEGY.md](..\06_RULE_ENGINE\RULE_TEST_STRATEGY.md) — 4-vector test strategy for rules.

---

## 9. Data Strategy & Provenance (`docs/07_DATA/`)
- [DATA_STRATEGY.md](..\07_DATA\DATA_STRATEGY.md) — Dataset governance and stratification.
- [DATA_SOURCES.md](..\07_DATA\DATA_SOURCES.md) — Acquisition source registry.
- [DATA_LICENSES.md](..\07_DATA\DATA_LICENSES.md) — Dataset licensing permissions.
- [DATA_DICTIONARY.md](..\07_DATA\DATA_DICTIONARY.md) — Schema definitions and units.
- [ANNOTATION_GUIDE.md](..\07_DATA\ANNOTATION_GUIDE.md) — Annotation protocol and caliper ground truth.
- [DATASET_CARD.md](..\07_DATA\DATASET_CARD.md) — Datasheet for packaging benchmark datasets.
- [BENCHMARK_PROTOCOL.md](..\07_DATA\BENCHMARK_PROTOCOL.md) — Master benchmark evaluation protocols.

---

## 10. Evidence & Chain of Custody (`docs/08_EVIDENCE/`)
- [EVIDENCE_MODEL.md](..\08_EVIDENCE\EVIDENCE_MODEL.md) — Evidence entity-relationship model.
- [CHAIN_OF_CUSTODY.md](..\08_EVIDENCE\CHAIN_OF_CUSTODY.md) — Digital chain of custody procedures.
- [HASHING.md](..\08_EVIDENCE\HASHING.md) — SHA-256 and pHash standards.
- [AUDIT_LOG.md](..\08_EVIDENCE\AUDIT_LOG.md) — Append-only audit log schema.
- [REPORT_SPEC.md](..\08_EVIDENCE\REPORT_SPEC.md) — PDF inspection dossier specification.
- [EVIDENCE_LIMITATIONS.md](..\08_EVIDENCE\EVIDENCE_LIMITATIONS.md) — Evidentiary disclaimers and court standing.

---

## 11. Security & Privacy (`docs/09_SECURITY_PRIVACY/`)
- [THREAT_MODEL.md](..\09_SECURITY_PRIVACY\THREAT_MODEL.md) — STRIDE threat model.
- [RBAC.md](..\09_SECURITY_PRIVACY\RBAC.md) — Role-based access control specifications.
- [PRIVACY.md](..\09_SECURITY_PRIVACY\PRIVACY.md) — DPDP Act compliance and PII redaction.
- [DATA_RETENTION.md](..\09_SECURITY_PRIVACY\DATA_RETENTION.md) — Data lifecycle and disposal policy.
- [SECURITY_TESTING.md](..\09_SECURITY_PRIVACY\SECURITY_TESTING.md) — Security testing and vulnerability assessments.

---

## 12. Quality Assurance & Testing (`docs/10_TESTING/`)
- [TEST_STRATEGY.md](..\10_TESTING\TEST_STRATEGY.md) — Testing strategy and pyramid.
- [TEST_MATRIX.md](..\10_TESTING\TEST_MATRIX.md) — Test matrix cross-reference.
- [ADVERSARIAL_TESTS.md](..\10_TESTING\ADVERSARIAL_TESTS.md) — Adversarial test scenarios.
- [REGRESSION_TESTS.md](..\10_TESTING\REGRESSION_TESTS.md) — Continuous regression suite.
- [PERFORMANCE_TESTS.md](..\10_TESTING\PERFORMANCE_TESTS.md) — Load and latency benchmarks.
- [FAILURE_MODES.md](..\10_TESTING\FAILURE_MODES.md) — FMEA failure mode analysis.

---

## 13. Hackathon Judging Strategy (`docs/11_JUDGING/`)
- [JUDGING_CRITERIA.md](..\11_JUDGING\JUDGING_CRITERIA.md) — Analyst framework for judging criteria.
- [CRITERION_EVIDENCE_MATRIX.md](..\11_JUDGING\CRITERION_EVIDENCE_MATRIX.md) — Executable feature defense matrix.
- [INNOVATION_CASE.md](..\11_JUDGING\INNOVATION_CASE.md) — The 4 pillars of innovation.
- [FEASIBILITY_CASE.md](..\11_JUDGING\FEASIBILITY_CASE.md) — Technical feasibility case.
- [PROBLEM_SOLVING_CASE.md](..\11_JUDGING\PROBLEM_SOLVING_CASE.md) — Problem solving and inspector alignment case.
- [PROTOTYPE_CASE.md](..\11_JUDGING\PROTOTYPE_CASE.md) — Working prototype case.
- [SCALABILITY_CASE.md](..\11_JUDGING\SCALABILITY_CASE.md) — National scalability impact.
- [UX_CASE.md](..\11_JUDGING\UX_CASE.md) — Field ergonomics and UX case.
- [PRESENTATION_CASE.md](..\11_JUDGING\PRESENTATION_CASE.md) — 5-minute timed evaluation pitch.
- [Q_AND_A.md](..\11_JUDGING\Q_AND_A.md) — 10 tough judge questions and defenses.
- [DEMO_SCRIPT.md](..\11_JUDGING\DEMO_SCRIPT.md) — Live demonstration runbook.

---

## 14. Prior Art & Differentiation (`docs/12_PRIOR_ART/`)
- [PRIOR_ART_REGISTER.md](..\12_PRIOR_ART\PRIOR_ART_REGISTER.md) — Literature review and prior art.
- [COMPETITOR_MATRIX.md](..\12_PRIOR_ART\COMPETITOR_MATRIX.md) — Commercial and academic comparison.
- [DIFFERENTIATION.md](..\12_PRIOR_ART\DIFFERENTIATION.md) — The 7-part defensible differentiation formula.

---

## 15. Build Plan & Engineering Execution (`docs/13_BUILD_PLAN/`)
- [ROADMAP.md](..\13_BUILD_PLAN\ROADMAP.md) — Product roadmap and horizons.
- [TASK_BREAKDOWN.md](..\13_BUILD_PLAN\TASK_BREAKDOWN.md) — Work breakdown structure.
- [TEAM_OWNERSHIP.md](..\13_BUILD_PLAN\TEAM_OWNERSHIP.md) — RACI team ownership matrix.
- [MILESTONES.md](..\13_BUILD_PLAN\MILESTONES.md) — Milestones and critical path.
- [DEFINITION_OF_DONE.md](..\13_BUILD_PLAN\DEFINITION_OF_DONE.md) — 7-point Definition of Done checklist.

---

## 16. Submission Governance & Quality Gates (`docs/14_SUBMISSION/`)
- [FINAL_PHYSICAL_TRUTH_AUDIT.md](FINAL_PHYSICAL_TRUTH_AUDIT.md) — Master physical repository truth audit and absolute final gate report.
- [FINAL_ZERO_RESIDUAL_AUDIT.md](FINAL_ZERO_RESIDUAL_AUDIT.md) — Master zero-residual forensic audit report and acceptance matrix.
- [FINAL_CONSISTENCY_AUDIT.md](FINAL_CONSISTENCY_AUDIT.md) — Master cross-document consistency and truth audit report.
- [CANONICAL_PROJECT_STATUS.md](CANONICAL_PROJECT_STATUS.md) — Single source of truth for canonical state vector and dataset reality.
- [FACT_CONSISTENCY_MATRIX.md](FACT_CONSISTENCY_MATRIX.md) — Master cross-document fact consistency matrix and audit trail.
- [FINAL_ARTIFACT_AUDIT.md](FINAL_ARTIFACT_AUDIT.md) — Definitive forensic artifact, gitkeep, and phantom data audit report.
- [FINAL_TRUTH_CHECK.md](FINAL_TRUTH_CHECK.md) — Direct answers to 14 core forensic truth check questions.
- [ARTIFACT_STATUS_REGISTRY.md](ARTIFACT_STATUS_REGISTRY.md) — Master artifact status registry with physical verification proofs.
- [CLAIM_ARTIFACT_TRACEABILITY.md](CLAIM_ARTIFACT_TRACEABILITY.md) — Substantive claim-to-disk artifact forensic cross-check matrix.
- [DATASET_EXISTENCE_AUDIT.md](DATASET_EXISTENCE_AUDIT.md) — Forensic audit of declared datasets vs physical files on disk.
- [GITKEEP_AUDIT.md](GITKEEP_AUDIT.md) — Comprehensive audit and classification (Classes A–F) of all 71 .gitkeep files.
- [GITKEEP_POLICY.md](GITKEEP_POLICY.md) — Repository policy establishing the semantic meaning and boundaries of .gitkeep.
- [PHYSICAL_ARTIFACT_INVENTORY.md](PHYSICAL_ARTIFACT_INVENTORY.md) — Complete byte-level physical inventory of all files and directories on disk.
- [PRIMARY_SOURCE_VERIFICATION_STATUS.md](PRIMARY_SOURCE_VERIFICATION_STATUS.md) — Primary source verification status and 8-part quality gate report.
- [RESEARCH_GAPS.md](RESEARCH_GAPS.md) — Research gaps and evidence requirements register across Evidence Packs A–G.
- [FINAL_REPOSITORY_AUDIT.md](FINAL_REPOSITORY_AUDIT.md) — Definitive master repository completeness and integrity audit report.
- [FINAL_REPOSITORY_STATUS.md](FINAL_REPOSITORY_STATUS.md) — Standardized final repository status matrix.
- [FINAL_REPOSITORY_INVENTORY.md](FINAL_REPOSITORY_INVENTORY.md) — Comprehensive 146-directory filesystem inventory and lifecycle audit.
- [IMPLEMENTATION_CLAIM_AUDIT.md](IMPLEMENTATION_CLAIM_AUDIT.md) — File-by-file implementation claim audit and lifecycle classification.
- [DATA_API_AUDIT.md](DATA_API_AUDIT.md) — Dataset provenance, portal integration, and privacy compliance audit.
- [DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md) — Third-party library licenses, anti-AGPL policy, and CPU runtime audit.
- [TEST_COVERAGE_AUDIT.md](TEST_COVERAGE_AUDIT.md) — Automated test suite verification and testing pyramid audit.
- [FINAL_GOVERNANCE_AUDIT.md](FINAL_GOVERNANCE_AUDIT.md) — Definitive governance audit and hardening certification report.
- [REPOSITORY_AUDIT.md](REPOSITORY_AUDIT.md) — Comprehensive repository inventory and audit report.
- [AUDIT_SUMMARY.md](AUDIT_SUMMARY.md) — Hardening audit summary and action report.
- [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) — Final submission readiness checklist.
- [FINAL_ARCHITECTURE.md](FINAL_ARCHITECTURE.md) — Architecture synthesis.
- [FINAL_FEATURES.md](FINAL_FEATURES.md) — Final features catalog and disciplined lifecycle status.
- [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) — Final demo staging runbook.
- [CLAIM_VERIFICATION.md](CLAIM_VERIFICATION.md) — Claims verification registry.
- [SIH_CLAIM_VERIFICATION.md](SIH_CLAIM_VERIFICATION.md) — SIH-specific claim audit register.
- [SOURCE_GAPS.md](SOURCE_GAPS.md) — Final quality gate audit and source gaps register.
- [LEGAL_VERIFICATION_BACKLOG.md](LEGAL_VERIFICATION_BACKLOG.md) — Legal source retrieval backlog.
- [OPEN_DECISIONS.md](OPEN_DECISIONS.md) — Open architecture trade-offs.
- [IMPLEMENTATION_READINESS.md](IMPLEMENTATION_READINESS.md) — Readiness assessment scorecard.

---

## 17. Architecture Decision Records (`docs/15_DECISIONS/`)
- [README.md](..\15_DECISIONS\README.md) — ADR repository guide and decision index.
- [ADR_TEMPLATE.md](..\15_DECISIONS\ADR_TEMPLATE.md) — Standardized ADR template.

---

## 18. Known Limitations & Failure Boundaries (`docs/16_LIMITATIONS/`)
- [LEGAL_LIMITATIONS.md](..\16_LIMITATIONS\LEGAL_LIMITATIONS.md) — Statutory and legal boundaries.
- [AI_LIMITATIONS.md](..\16_LIMITATIONS\AI_LIMITATIONS.md) — Optical and AI observation boundaries.
- [MEASUREMENT_LIMITATIONS.md](..\16_LIMITATIONS\MEASUREMENT_LIMITATIONS.md) — Physical scale and error bounds.
- [DATA_LIMITATIONS.md](..\16_LIMITATIONS\DATA_LIMITATIONS.md) — Dataset coverage constraints.
- [DEPLOYMENT_LIMITATIONS.md](..\16_LIMITATIONS\DEPLOYMENT_LIMITATIONS.md) — Edge hardware limitations.
- [KNOWN_FAILURES.md](..\16_LIMITATIONS\KNOWN_FAILURES.md) — Controlled refusal registry.

---

## 19. Anti-Hallucination Claims Tracking (`docs/17_CLAIMS/`)
- [CLAIMS_REGISTER.md](..\17_CLAIMS\CLAIMS_REGISTER.md) — Master claims register.
- [CLAIM_EVIDENCE_MATRIX.md](..\17_CLAIMS\CLAIM_EVIDENCE_MATRIX.md) — Claim to evidence mapping.
- [PERFORMANCE_CLAIMS.md](..\17_CLAIMS\PERFORMANCE_CLAIMS.md) — Performance claims and placeholders.
- [LEGAL_CLAIMS.md](..\17_CLAIMS\LEGAL_CLAIMS.md) — Authorized legal statements.
- [COMPETITIVE_CLAIMS.md](..\17_CLAIMS\COMPETITIVE_CLAIMS.md) — Competitive claims policy.
