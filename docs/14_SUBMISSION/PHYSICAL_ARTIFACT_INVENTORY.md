# NIRIKSHAK — PHYSICAL ARTIFACT INVENTORY

**Audit Standard:** Forensic Verification of Physical Disk Reality (Truth > Appearance)  
**Audit Execution Date:** 2026-09-04  
**Total Tracked Files:** 243  
**Total Tracked Directories:** 150  

---

## 1. Executive Summary

This document records the physical reality of every single file and directory in the `sih26034-nirikshak` repository. No file is assumed to exist; every entry is physically probed on the local filesystem.

### Physical Composition Summary

- **Total Files on Disk:** 243
- **Total Directories:** 150
- **Total `.gitkeep` Scaffolds:** 71
- **Active Functional Files (Code/Docs/Config):** 172
- **Empty Directories (0 files, 0 subdirs):** 26

---

## 2. Comprehensive File Inventory

| File Path | Size (Bytes) | Category | Expected Purpose | Actual State on Disk |
| :--- | :---: | :--- | :--- | :--- |
| `.env.example` | 1,348 | `SYSTEM_METADATA` | Project configuration or metadata | Active configuration file |
| `.gitignore` | 825 | `SYSTEM_METADATA` | Project configuration or metadata | Active configuration file |
| `CONTRIBUTING.md` | 2,706 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `LICENSE` | 10,169 | `SYSTEM_METADATA` | Project configuration or metadata | Active configuration file |
| `Makefile` | 1,546 | `SYSTEM_METADATA` | Project configuration or metadata | Active configuration file |
| `README.md` | 8,320 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `SECURITY.md` | 2,172 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `apps/api/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `apps/web/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `apps/worker/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `assets/demo/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `assets/diagrams/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `assets/presentation/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `assets/sample_packages/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `assets/screenshots/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `benchmarks/datasets/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `benchmarks/protocols/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `benchmarks/reports/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `benchmarks/results/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `benchmarks/runs/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `data/annotations/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `data/benchmark/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `data/manifests/manifest.yaml` | 2,006 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `data/processed/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `data/raw/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `data/synthetic/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `docker-compose.yml` | 1,623 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/00_PROJECT_CHARTER/ASSUMPTIONS.md` | 3,021 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/00_PROJECT_CHARTER/GLOSSARY.md` | 3,245 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/00_PROJECT_CHARTER/MVP_SCOPE.md` | 2,400 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/00_PROJECT_CHARTER/NON_GOALS.md` | 2,352 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/00_PROJECT_CHARTER/PROJECT_CHARTER.md` | 3,188 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/00_PROJECT_CHARTER/SCOPE.md` | 2,635 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/01_PROBLEM_STATEMENT/OFFICIAL_PS/SOURCE_RECORD.md` | 932 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/01_PROBLEM_STATEMENT/OFFICIAL_PS/problem_statement_transcript.md` | 2,080 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md` | 2,946 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/01_PROBLEM_STATEMENT/REQUIREMENT_TRACEABILITY.md` | 2,998 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/CHANGE_IMPACT_MATRIX.md` | 1,946 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/LEGAL_CHANGELOG.md` | 2,654 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/README.md` | 2,174 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/SOURCE_HIERARCHY.md` | 4,979 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/SOURCE_REGISTER_GUIDE.md` | 3,806 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/applicability_matrix.yaml` | 1,194 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/effective_dates.yaml` | 1,083 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/exemption_catalog.yaml` | 1,217 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/measurement_requirements.yaml` | 1,383 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG/rule_catalog.yaml` | 2,270 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `docs/03_PRODUCT_REQUIREMENTS/ACCEPTANCE_CRITERIA.md` | 2,600 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/03_PRODUCT_REQUIREMENTS/ERROR_STATE_REQUIREMENTS.md` | 2,624 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/03_PRODUCT_REQUIREMENTS/FUNCTIONAL_REQUIREMENTS.md` | 3,886 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/03_PRODUCT_REQUIREMENTS/NON_FUNCTIONAL_REQUIREMENTS.md` | 2,688 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/03_PRODUCT_REQUIREMENTS/USER_JOURNEYS.md` | 2,095 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/03_PRODUCT_REQUIREMENTS/USER_PERSONAS.md` | 3,075 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/AI_PIPELINE.md` | 2,798 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/ARCHITECTURE_DECISIONS.md` | 1,929 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/DATA_FLOW.md` | 2,220 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/EVIDENCE_ARCHITECTURE.md` | 2,720 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/OFFLINE_ARCHITECTURE.md` | 3,417 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/RULE_ENGINE.md` | 3,806 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/SECURITY_ARCHITECTURE.md` | 1,981 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/04_ARCHITECTURE/SYSTEM_ARCHITECTURE.md` | 3,475 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/CALIBRATION.md` | 2,871 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/CURVED_SURFACE_PROCESSING.md` | 2,003 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/FIELD_EXTRACTION.md` | 4,116 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/FONT_MEASUREMENT.md` | 4,878 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/IMAGE_QUALITY_GATE.md` | 2,388 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/MODEL_EVALUATION.md` | 1,996 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/OCR_STRATEGY.md` | 2,217 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/PDP_DETECTION.md` | 2,974 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/05_AI_VISION/TEXT_DETECTION.md` | 1,399 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/APPLICABILITY_ENGINE.md` | 2,436 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/CONFLICT_RESOLUTION.md` | 2,645 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/EXEMPTION_ENGINE.md` | 1,794 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/RULE_ENGINE_SPEC.md` | 2,108 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/RULE_TEST_STRATEGY.md` | 1,926 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/06_RULE_ENGINE/VERSIONING.md` | 2,445 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/ANNOTATION_GUIDE.md` | 1,834 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/BENCHMARK_PROTOCOL.md` | 2,657 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/DATASET_CARD.md` | 1,822 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/DATA_DICTIONARY.md` | 1,892 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/DATA_LICENSES.md` | 1,286 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/DATA_SOURCES.md` | 1,576 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/07_DATA/DATA_STRATEGY.md` | 2,011 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/AUDIT_LOG.md` | 1,652 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/CHAIN_OF_CUSTODY.md` | 1,957 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/EVIDENCE_LIMITATIONS.md` | 2,538 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/EVIDENCE_MODEL.md` | 3,213 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/HASHING.md` | 1,691 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/08_EVIDENCE/REPORT_SPEC.md` | 3,633 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/09_SECURITY_PRIVACY/DATA_RETENTION.md` | 1,521 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/09_SECURITY_PRIVACY/PRIVACY.md` | 1,980 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/09_SECURITY_PRIVACY/RBAC.md` | 1,946 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/09_SECURITY_PRIVACY/SECURITY_TESTING.md` | 1,568 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/09_SECURITY_PRIVACY/THREAT_MODEL.md` | 2,347 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/ADVERSARIAL_TESTS.md` | 2,134 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/FAILURE_MODES.md` | 1,676 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/PERFORMANCE_TESTS.md` | 1,494 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/REGRESSION_TESTS.md` | 1,334 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/TEST_MATRIX.md` | 1,906 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/10_TESTING/TEST_STRATEGY.md` | 2,044 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/CRITERION_EVIDENCE_MATRIX.md` | 5,715 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/DEMO_SCRIPT.md` | 3,149 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/FEASIBILITY_CASE.md` | 1,544 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/INNOVATION_CASE.md` | 2,023 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/JUDGING_CRITERIA.md` | 2,269 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/PRESENTATION_CASE.md` | 2,399 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/PROBLEM_SOLVING_CASE.md` | 2,230 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/PROTOTYPE_CASE.md` | 1,727 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/Q_AND_A.md` | 4,927 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/SCALABILITY_CASE.md` | 1,652 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/11_JUDGING/UX_CASE.md` | 1,877 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/COMPETITOR_MATRIX.md` | 2,605 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/DIFFERENTIATION.md` | 3,354 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/GOVERNMENT_SYSTEMS/README.md` | 781 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/PAPERS/README.md` | 614 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md` | 3,023 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/12_PRIOR_ART/PRODUCTS/README.md` | 603 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/13_BUILD_PLAN/DEFINITION_OF_DONE.md` | 2,221 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/13_BUILD_PLAN/MILESTONES.md` | 3,588 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/13_BUILD_PLAN/ROADMAP.md` | 3,841 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/13_BUILD_PLAN/TASK_BREAKDOWN.md` | 2,837 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/13_BUILD_PLAN/TEAM_OWNERSHIP.md` | 1,675 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/AUDIT_SUMMARY.md` | 8,780 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/CLAIM_VERIFICATION.md` | 1,881 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/DATA_API_AUDIT.md` | 8,129 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/DEMO_RUNBOOK.md` | 1,351 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/DEPENDENCY_AUDIT.md` | 7,543 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/DOCUMENT_INDEX.md` | 15,391 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_ARCHITECTURE.md` | 1,480 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_FEATURES.md` | 4,934 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_GOVERNANCE_AUDIT.md` | 13,968 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_REPOSITORY_AUDIT.md` | 14,354 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_REPOSITORY_INVENTORY.md` | 26,804 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/FINAL_REPOSITORY_STATUS.md` | 5,496 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/IMPLEMENTATION_CLAIM_AUDIT.md` | 12,316 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/IMPLEMENTATION_READINESS.md` | 4,209 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/LEGAL_VERIFICATION_BACKLOG.md` | 1,595 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/OPEN_DECISIONS.md` | 1,753 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/PRIMARY_SOURCE_VERIFICATION_STATUS.md` | 6,977 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/REPOSITORY_AUDIT.md` | 10,915 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/RESEARCH_GAPS.md` | 4,626 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/SIH_CLAIM_VERIFICATION.md` | 2,554 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/SOURCE_GAPS.md` | 5,242 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/SUBMISSION_CHECKLIST.md` | 1,905 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/14_SUBMISSION/TEST_COVERAGE_AUDIT.md` | 7,360 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/15_DECISIONS/ADR_TEMPLATE.md` | 1,264 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/15_DECISIONS/README.md` | 908 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/AI_LIMITATIONS.md` | 939 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/DATA_LIMITATIONS.md` | 825 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/DEPLOYMENT_LIMITATIONS.md` | 767 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/KNOWN_FAILURES.md` | 1,527 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/LEGAL_LIMITATIONS.md` | 960 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/16_LIMITATIONS/MEASUREMENT_LIMITATIONS.md` | 2,048 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/17_CLAIMS/CLAIMS_REGISTER.md` | 3,162 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/17_CLAIMS/CLAIM_EVIDENCE_MATRIX.md` | 1,317 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/17_CLAIMS/COMPETITIVE_CLAIMS.md` | 2,024 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/17_CLAIMS/LEGAL_CLAIMS.md` | 1,356 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/17_CLAIMS/PERFORMANCE_CLAIMS.md` | 1,968 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/DATA_LICENSES.md` | 3,663 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/LEGAL_NOTICES.md` | 3,354 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `docs/THIRD_PARTY_LICENSES.md` | 3,139 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `experiments/calibration/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/dewarping/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/end_to_end/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/extraction/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/font_measurement/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/ocr/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/pdp_detection/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `experiments/rules/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `infra/db/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `infra/deployment/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `infra/docker/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `infra/docker/Dockerfile.api` | 672 | `CONTAINER_SPEC` | Container build definition | Development container scaffold |
| `infra/docker/Dockerfile.web` | 348 | `CONTAINER_SPEC` | Container build definition | Development container scaffold |
| `infra/monitoring/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `infra/storage/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `models/cards/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `models/configs/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `models/registry/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `models/weights/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/calibration/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/evidence/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/extraction/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/measurement/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/ocr/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/reporting/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/rules-engine/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/shared/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `packages/vision/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/amendments/packaged_commodities/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/applicability/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/current/legal_metrology_act_2009/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/current/packaged_commodities_rules/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/exemptions/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/historical/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/interpretations/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/proposed/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `regulations/source_registry.yaml` | 4,978 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `regulations/superseded/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `requirements.txt` | 751 | `SYSTEM_METADATA` | Project configuration or metadata | Active configuration file |
| `research/README.md` | 1,532 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/academic_papers/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/competitors/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/datasets/PACK_E_DATASETS.md` | 9,150 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/hackathon_winners/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/models/PACK_F_AI_STACK.md` | 6,872 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/official_sources/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/official_sources/PACK_A_OFFICIAL_PS.md` | 4,917 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/official_sources/PACK_B_LEGAL_FRAMEWORK.md` | 11,698 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/official_sources/PACK_C_MEASUREMENT_STANDARDS.md` | 8,344 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/prior_art/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/prior_art/PACK_D_PRIOR_ART.md` | 13,365 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/research_gaps/RESEARCH_GAPS_REGISTER.md` | 4,632 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/research_notes/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/secondary_sources/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `research/secondary_sources/SECONDARY_ANALYSIS.md` | 4,212 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `research/sih/PACK_G_SIH_FRAMEWORK.md` | 5,958 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `rules/README.md` | 1,426 | `DOCUMENTATION` | Engineering or submission documentation | Active Markdown specification |
| `rules/proposed/rule_06_mandatory_declarations_candidate.yaml` | 2,527 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `rules/proposed/rule_07_table1_font_height_candidate.yaml` | 2,242 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `rules/proposed/template_declarations_rule.yaml` | 1,544 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `rules/proposed/template_numeral_height_rule.yaml` | 1,264 | `CONFIG_SCHEMA` | Configuration or data manifest | Active YAML specification/config |
| `rules/schema/applicability.schema.json` | 1,188 | `JSON_SCHEMA` | Machine-readable schema specification | Active JSON schema definition |
| `rules/schema/evidence.schema.json` | 1,739 | `JSON_SCHEMA` | Machine-readable schema specification | Active JSON schema definition |
| `rules/schema/rule.schema.json` | 1,944 | `JSON_SCHEMA` | Machine-readable schema specification | Active JSON schema definition |
| `scripts/benchmark/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `scripts/dataset/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `scripts/legal/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `scripts/reports/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `scripts/verification/verify_claims.py` | 3,997 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `scripts/verification/verify_dataset_manifest.py` | 3,010 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `scripts/verification/verify_legal_sources.py` | 4,984 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `scripts/verification/verify_report_provenance.py` | 2,316 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `scripts/verification/verify_repository_integrity.py` | 5,461 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `scripts/verification/verify_rule_registry.py` | 4,716 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `tests/e2e/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/fixtures/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/integration/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/rules/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/security/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/unit/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |
| `tests/unit/test_verification_pipeline.py` | 1,468 | `PYTHON_CODE` | Executable script or unit test | Active Python source code |
| `tests/vision/.gitkeep` | 0 | `SCAFFOLD` | Preserve intentional empty directory structure | Gitkeep placeholder file |

---

## 3. Directory Emptiness & Purpose Audit

| Directory Path | Subdirectories | Files | Emptiness Status | Documented Expected Purpose | Actual Reality on Disk |
| :--- | :---: | :---: | :--- | :--- | :--- |
| `.` | 15 | 9 | `ACTIVE_CONTENT` | Repository functional module | Contains 9 active file(s) |
| `apps` | 3 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `apps/api` | 0 | 1 | `GITKEEP_ONLY` | Application service source code (FastAPI, React web, task worker) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `apps/web` | 0 | 1 | `GITKEEP_ONLY` | Application service source code (FastAPI, React web, task worker) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `apps/worker` | 0 | 1 | `GITKEEP_ONLY` | Application service source code (FastAPI, React web, task worker) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `assets` | 5 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `assets/demo` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `assets/diagrams` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `assets/presentation` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `assets/sample_packages` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `assets/screenshots` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `benchmarks` | 5 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `benchmarks/datasets` | 0 | 1 | `GITKEEP_ONLY` | Standardized dataset benchmarks and quantitative performance logs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `benchmarks/protocols` | 0 | 1 | `GITKEEP_ONLY` | Standardized dataset benchmarks and quantitative performance logs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `benchmarks/reports` | 0 | 1 | `GITKEEP_ONLY` | Standardized dataset benchmarks and quantitative performance logs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `benchmarks/results` | 0 | 1 | `GITKEEP_ONLY` | Standardized dataset benchmarks and quantitative performance logs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `benchmarks/runs` | 0 | 1 | `GITKEEP_ONLY` | Standardized dataset benchmarks and quantitative performance logs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `data` | 6 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `data/annotations` | 0 | 1 | `GITKEEP_ONLY` | Physical retail packaging images, annotations, and synthetic labels | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `data/benchmark` | 0 | 1 | `GITKEEP_ONLY` | Physical retail packaging images, annotations, and synthetic labels | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `data/manifests` | 0 | 1 | `ACTIVE_CONTENT` | Physical retail packaging images, annotations, and synthetic labels | Contains 1 active file(s) |
| `data/processed` | 0 | 1 | `GITKEEP_ONLY` | Physical retail packaging images, annotations, and synthetic labels | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `data/raw` | 0 | 1 | `GITKEEP_ONLY` | Physical retail packaging images, annotations, and synthetic labels | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `data/synthetic` | 0 | 1 | `GITKEEP_ONLY` | Physical retail packaging images, annotations, and synthetic labels | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `docs` | 18 | 3 | `ACTIVE_CONTENT` | Repository functional module | Contains 3 active file(s) |
| `docs/00_PROJECT_CHARTER` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/01_PROBLEM_STATEMENT` | 1 | 2 | `ACTIVE_CONTENT` | Repository functional module | Contains 2 active file(s) |
| `docs/01_PROBLEM_STATEMENT/OFFICIAL_PS` | 0 | 2 | `ACTIVE_CONTENT` | Repository functional module | Contains 2 active file(s) |
| `docs/02_LEGAL_AUTHORITY` | 5 | 4 | `ACTIVE_CONTENT` | Repository functional module | Contains 4 active file(s) |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS` | 3 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_128_E` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_312_E` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/2026_AMENDMENTS/GSR_418_E` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/ACT` | 2 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `docs/02_LEGAL_AUTHORITY/ACT/amendments` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/ACT/legal_metrology_act_2009` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES` | 3 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/FAQs` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/implementation_guidelines` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/GUIDELINES/official_advisories` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES` | 3 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS` | 9 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2012` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2013` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2014` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2015` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2016` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2017` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2022` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2023` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/AMENDMENTS/2026` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/BASE_2011` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/PACKAGED_COMMODITIES_RULES/CONSOLIDATED` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for authenticated Gazette of India primary source PDFs | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/02_LEGAL_AUTHORITY/VERIFIED_RULE_CATALOG` | 0 | 5 | `ACTIVE_CONTENT` | Repository functional module | Contains 5 active file(s) |
| `docs/03_PRODUCT_REQUIREMENTS` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/04_ARCHITECTURE` | 1 | 8 | `ACTIVE_CONTENT` | Repository functional module | Contains 8 active file(s) |
| `docs/04_ARCHITECTURE/diagrams` | 0 | 0 | `COMPLETELY_EMPTY` | Repository functional module | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `docs/05_AI_VISION` | 0 | 9 | `ACTIVE_CONTENT` | Repository functional module | Contains 9 active file(s) |
| `docs/06_RULE_ENGINE` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/07_DATA` | 0 | 7 | `ACTIVE_CONTENT` | Repository functional module | Contains 7 active file(s) |
| `docs/08_EVIDENCE` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/09_SECURITY_PRIVACY` | 0 | 5 | `ACTIVE_CONTENT` | Repository functional module | Contains 5 active file(s) |
| `docs/10_TESTING` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/11_JUDGING` | 0 | 11 | `ACTIVE_CONTENT` | Repository functional module | Contains 11 active file(s) |
| `docs/12_PRIOR_ART` | 3 | 3 | `ACTIVE_CONTENT` | Repository functional module | Contains 3 active file(s) |
| `docs/12_PRIOR_ART/GOVERNMENT_SYSTEMS` | 0 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `docs/12_PRIOR_ART/PAPERS` | 0 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `docs/12_PRIOR_ART/PRODUCTS` | 0 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `docs/13_BUILD_PLAN` | 0 | 5 | `ACTIVE_CONTENT` | Repository functional module | Contains 5 active file(s) |
| `docs/14_SUBMISSION` | 0 | 23 | `ACTIVE_CONTENT` | Repository functional module | Contains 23 active file(s) |
| `docs/15_DECISIONS` | 0 | 2 | `ACTIVE_CONTENT` | Repository functional module | Contains 2 active file(s) |
| `docs/16_LIMITATIONS` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `docs/17_CLAIMS` | 0 | 5 | `ACTIVE_CONTENT` | Repository functional module | Contains 5 active file(s) |
| `experiments` | 8 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `experiments/calibration` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/dewarping` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/end_to_end` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/extraction` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/font_measurement` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/ocr` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/pdp_detection` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `experiments/rules` | 0 | 1 | `GITKEEP_ONLY` | Physical camera calibration, OCR, and dewarping trial scripts | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `infra` | 5 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `infra/db` | 0 | 1 | `GITKEEP_ONLY` | Docker, database, and infrastructure deployment templates | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `infra/deployment` | 0 | 1 | `GITKEEP_ONLY` | Docker, database, and infrastructure deployment templates | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `infra/docker` | 0 | 3 | `MIXED` | Docker, database, and infrastructure deployment templates | Contains 3 file(s) including `.gitkeep` |
| `infra/monitoring` | 0 | 1 | `GITKEEP_ONLY` | Docker, database, and infrastructure deployment templates | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `infra/storage` | 0 | 1 | `GITKEEP_ONLY` | Docker, database, and infrastructure deployment templates | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `models` | 4 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `models/cards` | 0 | 1 | `GITKEEP_ONLY` | Model configuration cards, ONNX weights, and execution configs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `models/configs` | 0 | 1 | `GITKEEP_ONLY` | Model configuration cards, ONNX weights, and execution configs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `models/registry` | 0 | 1 | `GITKEEP_ONLY` | Model configuration cards, ONNX weights, and execution configs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `models/weights` | 0 | 1 | `GITKEEP_ONLY` | Model configuration cards, ONNX weights, and execution configs | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages` | 9 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `packages/calibration` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/evidence` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/extraction` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/measurement` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/ocr` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/reporting` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/rules-engine` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/shared` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `packages/vision` | 0 | 1 | `GITKEEP_ONLY` | Modular Python package code (vision, rule engine, reporting) | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations` | 8 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `regulations/amendments` | 1 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `regulations/amendments/packaged_commodities` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/applicability` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/current` | 2 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `regulations/current/legal_metrology_act_2009` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/current/packaged_commodities_rules` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/exemptions` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/historical` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/interpretations` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/proposed` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `regulations/superseded` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `research` | 11 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `research/academic_papers` | 0 | 1 | `GITKEEP_ONLY` | Primary and secondary evidence dossiers and research gaps | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `research/competitors` | 0 | 1 | `GITKEEP_ONLY` | Primary and secondary evidence dossiers and research gaps | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `research/datasets` | 0 | 1 | `ACTIVE_CONTENT` | Primary and secondary evidence dossiers and research gaps | Contains 1 active file(s) |
| `research/hackathon_winners` | 0 | 1 | `GITKEEP_ONLY` | Primary and secondary evidence dossiers and research gaps | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `research/models` | 0 | 1 | `ACTIVE_CONTENT` | Primary and secondary evidence dossiers and research gaps | Contains 1 active file(s) |
| `research/official_sources` | 0 | 4 | `MIXED` | Primary and secondary evidence dossiers and research gaps | Contains 4 file(s) including `.gitkeep` |
| `research/prior_art` | 0 | 2 | `MIXED` | Primary and secondary evidence dossiers and research gaps | Contains 2 file(s) including `.gitkeep` |
| `research/research_gaps` | 0 | 1 | `ACTIVE_CONTENT` | Primary and secondary evidence dossiers and research gaps | Contains 1 active file(s) |
| `research/research_notes` | 0 | 1 | `GITKEEP_ONLY` | Primary and secondary evidence dossiers and research gaps | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `research/secondary_sources` | 0 | 2 | `MIXED` | Primary and secondary evidence dossiers and research gaps | Contains 2 file(s) including `.gitkeep` |
| `research/sih` | 0 | 1 | `ACTIVE_CONTENT` | Primary and secondary evidence dossiers and research gaps | Contains 1 active file(s) |
| `rules` | 8 | 1 | `ACTIVE_CONTENT` | Repository functional module | Contains 1 active file(s) |
| `rules/current` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `rules/fixtures` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `rules/historical` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `rules/proposed` | 0 | 4 | `ACTIVE_CONTENT` | Repository functional module | Contains 4 active file(s) |
| `rules/schema` | 0 | 3 | `ACTIVE_CONTENT` | Repository functional module | Contains 3 active file(s) |
| `rules/superseded` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `rules/tests` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `rules/verified` | 0 | 0 | `COMPLETELY_EMPTY` | Reserved for verified rule promotion lifecycle stages | 0 files, 0 subdirectories (Preserved for Level 1 primary assets) |
| `scripts` | 5 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `scripts/benchmark` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `scripts/dataset` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `scripts/legal` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `scripts/reports` | 0 | 1 | `GITKEEP_ONLY` | Repository functional module | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `scripts/verification` | 0 | 6 | `ACTIVE_CONTENT` | Repository functional module | Contains 6 active file(s) |
| `tests` | 7 | 0 | `MIXED` | Repository functional module | Contains 0 file(s) including `.gitkeep` |
| `tests/e2e` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `tests/fixtures` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `tests/integration` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `tests/rules` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `tests/security` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |
| `tests/unit` | 0 | 2 | `MIXED` | Automated unit, integration, and compliance test suites | Contains 2 file(s) including `.gitkeep` |
| `tests/vision` | 0 | 1 | `GITKEEP_ONLY` | Automated unit, integration, and compliance test suites | Contains only `.gitkeep` (Pre-implementation scaffold) |

