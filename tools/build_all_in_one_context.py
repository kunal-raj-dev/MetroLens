"""
MetroLens AI — All-In-One Master Context Builder
Compiles all canonical product, architecture, team, legal, benchmark, and decision documents
into a single, unified, authoritative context file:
ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md
"""

import os
import sys
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_FILE = os.path.join(ROOT_DIR, "ALL-IN-ONE context", "METROLENS_AI_ALL_IN_ONE_DOCS.md")

def read_file(rel_path: str) -> str:
    full_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(full_path):
        print(f"WARNING: File not found: {rel_path}", file=sys.stderr)
        return f"> [!WARNING]\n> File `{rel_path}` not found during compilation.\n"
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_master_context():
    print(f"Compiling master context from {ROOT_DIR}...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    sections = [
        ("HEADER", None),
        ("SECTION 1: PRODUCT BLUEPRINT, METROSETU PLATFORM DETAILS & PROBLEM STATEMENT", [
            ("docs/METROLENS_PROJECT_DETAILS.md", "MetroLens AI (MetroSetu) — End-to-End Platform Guide & Product Blueprint"),
            ("docs/00_PROJECT_CHARTER/PROJECT_CHARTER.md", "Official Project Charter & Sponsoring Ministry Mandate"),
            ("docs/00_PROJECT_CHARTER/MVP_SCOPE.md", "Web MVP Scope Definition & Boundaries"),
            ("docs/00_PROJECT_CHARTER/GLOSSARY.md", "Legal Metrology & Vision Domain Glossary"),
            ("docs/01_PROBLEM_STATEMENT/OFFICIAL_PS/problem_statement_transcript.md", "SIH26034 Official Problem Statement Transcript"),
            ("docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md", "Official Problem Statement Requirements Traceability Matrix"),
            ("docs/03_PRODUCT_REQUIREMENTS/ACCEPTANCE_CRITERIA.md", "End-to-End System Acceptance Criteria")
        ]),
        ("SECTION 2: WEB SYSTEM ARCHITECTURE, SECURITY & OPENAPI CONTRACT", [
            ("docs/ARCHITECTURE.md", "System Architecture Specification (Baseline V1.0 - Web Application)"),
            ("docs/API_CONTRACT.md", "OpenAPI 3.1 Contract Specification & Data Schemas"),
            ("docs/04_ARCHITECTURE/DATA_FLOW.md", "End-to-End Inspection Pipeline Data Flow"),
            ("docs/04_ARCHITECTURE/SECURITY_ARCHITECTURE.md", "Zero-Trust Security & Evidence Integrity Architecture"),
            ("docs/04_ARCHITECTURE/EVIDENCE_ARCHITECTURE.md", "Tamper-Evident SHA-256 Chain of Custody & PDF Dossier Spec"),
            ("docs/04_ARCHITECTURE/OFFLINE_ARCHITECTURE.md", "Offline Edge Architecture & Synchronization")
        ]),
        ("SECTION 3: 6-MEMBER TEAM EXECUTION ARCHITECTURE & WORK PACKAGES", [
            ("docs/team/PROJECT_EXECUTION_OVERVIEW.md", "Master 6-Member Team Execution Plan & Outcome Work Packages"),
            ("docs/team/MEMBER_1_WORK_PLAN.md", "Member 1 Work Plan: AI, Multilingual OCR & Scene Text Extraction Lead"),
            ("docs/team/MEMBER_2_WORK_PLAN.md", "Member 2 Work Plan: Computer Vision, Metric Calibration & Physical Measurement Lead"),
            ("docs/team/MEMBER_3_WORK_PLAN.md", "Member 3 Work Plan: Legal Metrology Rule Engine & Statutory Logic Lead"),
            ("docs/team/MEMBER_4_WORK_PLAN.md", "Member 4 Work Plan: Backend Architecture, Inspection Pipeline & Evidence Dossier Lead"),
            ("docs/team/MEMBER_5_WORK_PLAN.md", "Member 5 Work Plan: Frontend, Inspector UX & Interactive Visual Verification Canvas Lead"),
            ("docs/team/MEMBER_6_WORK_PLAN.md", "Member 6 Work Plan: Ground Truth Dataset, Benchmark Protocol, DevOps & QA Lead"),
            ("docs/team/MASTER_CHECKLIST.md", "Team Master Deliverables & Gate Checklist"),
            ("docs/team/INTEGRATION_CHECKLIST.md", "Inter-Member Pipeline Integration Contracts & Checklists"),
            ("docs/team/DAILY_STATUS_TEMPLATE.md", "Daily Standup & Checkpoint Reporting Template")
        ]),
        ("SECTION 4: CANONICAL ARCHITECTURAL DECISION RECORDS (ADR-001 TO ADR-017)", [
            ("docs/DECISION_LOG.md", "Foundational Architecture Decisions (ADR-001 to ADR-010)"),
            ("docs/TECHNICAL_DECISIONS.md", "Web MVP Re-Baseline Decisions (ADR-011 to ADR-017)")
        ]),
        ("SECTION 5: CHUNK 1 OCR FEASIBILITY SPIKE & ENGINEERING BASELINE", [
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/01_PLAN/SPIKE_PLAN.md", "Chunk 1: OCR Feasibility Spike Execution Plan"),
            ("AI_CONTEXT/RESEARCH/CHUNK_1_OCR_RESEARCH.md", "Chunk 1: OCR Model Research & Evaluation Criteria"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/06_ANALYSIS/FINAL_SPIKE_REPORT.md", "Chunk 1: OCR Feasibility Spike — Final Engineering Analysis Report"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/05_RESULTS/MODEL_COMPARISON.md", "Empirical OCR Candidate Performance Matrix (CPU Inference)"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/07_DECISION/OCR_MODEL_DECISION.md", "Provisional OCR Model Selection Decision Record"),
            ("AI_CONTEXT/HANDOFFS/CHUNK_1_TO_CHUNK_2.md", "Engineering Handoff Specification: Chunk 1 to Chunk 2"),
            ("AI_CONTEXT/RUN_LOGS/CHUNK_1_RUN_LOG.md", "Chunk 1 Operational Execution Run Log")
        ]),
        ("SECTION 6: CHUNK 2 OCR ENGINE FOUNDATION & DIRECT ONNX RUNTIME SUBSYSTEM", [
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/01_PLAN/CHUNK_2_PLAN.md", "Chunk 2: OCR Engine Foundation Execution Plan"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/07_REVIEW/FINAL_CHUNK_2_REPORT.md", "Chunk 2: OCR Engine Foundation — Final Engineering Review Report"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/02_RESEARCH/RUNTIME_DECISION.md", "Python 3.14 Direct ONNX Runtime Dependency & Compatibility Decision"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/02_RESEARCH/MODEL_CURRENCY_CHECK.md", "PaddleOCR PP-OCRv5 vs PP-OCRv3 CTC Architecture Sanity Check"),
            ("benchmarks/ocr/chunk2/README.md", "Chunk 2 Multi-Thread CPU Benchmark & Memory Stability Trace"),
            ("models/manifest.yaml", "Cryptographic Model Weights Manifest & SHA-256 Checksums"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK2.md", "Inter-Member Handoff: M1 (OCR) to M2 (Calibration & Measurement)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M3_CHUNK2.md", "Inter-Member Handoff: M1 (OCR) to M3 (Rule Engine & Semantics)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M4_CHUNK2.md", "Inter-Member Handoff: M1 (OCR) to M4 (Backend FastAPI Service)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M5_CHUNK2.md", "Inter-Member Handoff: M1 (OCR) to M5 (Frontend Verification Canvas)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M6_CHUNK2.md", "Inter-Member Handoff: M1 (OCR) to M6 (Ground Truth & Benchmark)"),
            ("AI_CONTEXT/HANDOFFS/CHUNK_2_TO_CHUNK_3.md", "Engineering Handoff Specification: Chunk 2 to Chunk 3"),
            ("AI_CONTEXT/RUN_LOGS/CHUNK_2_RUN_LOG.md", "Chunk 2 Operational Execution Run Log")
        ]),
        ("SECTION 7: CHUNK 3 REAL-DATA OCR VALIDATION, DOMAIN PREPROCESSING & ROBUSTNESS", [
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/01_PLAN/CHUNK_3_PLAN.md", "Chunk 3: Real-Data OCR Validation Execution Plan"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_DATA/REAL_DATA_AUDIT.md", "Chunk 3: Real Data Audit & Path B Blocker Declaration"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_DATA/PROVENANCE_SPECIFICATION.md", "Packaging Dataset Metadata & Provenance Specification"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_DATA/SKU_SPLIT_PROTOCOL.md", "SKU-Level Zero-Leakage Partition Protocol"),
            ("data/manifests/real_packaging_manifest.json", "Canonical 35-SKU Real Packaging Dataset Registry Schema (Path B Enforced)"),
            ("data/manifests/ground_truth_benchmark.json", "Standardized Ground Truth Annotation Specification"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_ANALYSIS/FAILURE_TAXONOMY.md", "Standardized Packaging OCR Failure Taxonomy"),
            ("CURRENT_STATE/CHUNK_3_BASELINE.md", "Chunk 3: Starting Environment Baseline Snapshot (B0)"),
            ("CURRENT_STATE/CHUNK_3_CORRECTION_BASELINE.md", "Chunk 3: Correction Baseline & Hardening Snapshot"),
            ("CURRENT_STATE/CHUNK_3_STATUS.md", "Active Development Phase: Chunk 3 Status Summary"),
            ("CURRENT_STATE/CHUNK_3_FINAL_STATUS.md", "Active Development Phase: Chunk 3 Final Verified Status"),
            ("benchmarks/ocr/chunk3/README.md", "Chunk 3 Preprocessing Benchmark Suite & Summary of Results"),
            ("benchmarks/ocr/chunk3/final_results.json", "Chunk 3 Final Benchmark Results Matrix (8 Configs, 72 Passes)"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/07_DECISION/FINAL_CHUNK_3_REPORT.md", "Chunk 3: Real Packaging OCR Validation & Robustness — Final Report"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/07_DECISION/CHUNK_3_CORRECTION_REVIEW.md", "Chunk 3: Engineering Audit & Hardening Review"),
            ("tests/unit/test_ocr_chunk3_hardening.py", "Chunk 3: Phase 32 Hardening Test Specification"),
            ("tests/unit/test_ocr_chunk3_regression.py", "Chunk 3: Geometric Invariance & Determinism Regression Tests"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK3.md", "Inter-Member Handoff: M1 (OCR) to M2 (Calibration & Geometric Guarantees)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M6_CHUNK3.md", "Inter-Member Handoff: M1 (OCR) to M6 (Dataset Delivery & Benchmark Reproduction)"),
            ("AI_CONTEXT/HANDOFFS/CHUNK_3_TO_CHUNK_4.md", "Engineering Handoff Specification: Chunk 3 to Chunk 4"),
            ("AI_CONTEXT/RUN_LOGS/CHUNK_3_RUN_LOG.md", "Chunk 3 Operational Execution Run Log")
        ]),
        ("SECTION 8: CHUNK 4 OCR MONOREPO INTEGRATION, SERVICE ADAPTER & CONTRACT VERIFICATION", [
            ("CURRENT_STATE/CHUNK_4_BASELINE.md", "Chunk 4: Starting Environment Baseline Snapshot"),
            ("CURRENT_STATE/CHUNK_4_STATUS.md", "Chunk 4: Active Phase Verified Status Summary"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/01_PLAN/CHUNK_4_PLAN.md", "Chunk 4: OCR Monorepo Integration Execution Plan"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/02_AUDIT/REPOSITORY_AUDIT.md", "Chunk 4: Monorepo Repository Audit & Boundary Verification"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/03_DESIGN/SERVICE_ADAPTER_SPEC.md", "Chunk 4: OCR Service Adapter Technical Specification"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/04_IMPLEMENTATION/INTEGRATION_RECORD.md", "Chunk 4: Monorepo Packaging & Integration Implementation Record"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/05_TESTS/TEST_MATRIX.md", "Chunk 4: Integration Test Matrix & Verification Suite"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/06_RESULTS/INTEGRATION_RESULTS.md", "Chunk 4: Integration Performance & Contract Verification Results"),
            ("AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/07_REVIEW/FINAL_CHUNK_4_REPORT.md", "Chunk 4: Final Engineering Review Report (24 Sections)"),
            ("benchmarks/ocr/chunk4/README.md", "Chunk 4: Integration Benchmark Suite & Concurrency Guide"),
            ("benchmarks/ocr/chunk4/integration_results.json", "Chunk 4: Machine-Readable Integration Benchmark Artifacts"),
            ("tests/integration/test_ocr_service_integration.py", "Chunk 4: Service Integration Test Suite (16 Comprehensive Tests)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M4_CHUNK4.md", "Inter-Member Handoff: M1 (OCR) to M4 (Backend FastAPI Service)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M5_CHUNK4.md", "Inter-Member Handoff: M1 (OCR) to M5 (Frontend Verification Canvas)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M3_CHUNK4.md", "Inter-Member Handoff: M1 (OCR) to M3 (Rule Engine & Semantics)"),
            ("AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK4.md", "Inter-Member Handoff: M1 (OCR) to M2 (Vision & Optical Measurement)"),
            ("AI_CONTEXT/HANDOFFS/CHUNK_4_TO_CHUNK_5.md", "Engineering Handoff Specification: Chunk 4 to Chunk 5"),
            ("AI_CONTEXT/RUN_LOGS/CHUNK_4_RUN_LOG.md", "Chunk 4 Operational Execution Run Log")
        ]),
        ("SECTION 9: COMPUTER VISION, CALIBRATION & OPTICAL MEASUREMENT SPECIFICATIONS", [
            ("docs/05_AI_VISION/IMAGE_QUALITY_GATE.md", "Optical Image Quality Gate & Pre-Flight Validation Spec"),
            ("docs/05_AI_VISION/CALIBRATION.md", "Physical Scale Calibration & Reference Target Recovery Spec"),
            ("docs/05_AI_VISION/FONT_MEASUREMENT.md", "Rule 7 Font Height Optical Measurement & Table-I Uncertainty Model"),
            ("docs/07_DATA/BENCHMARK_PROTOCOL.md", "35-SKU Ground Truth Dataset & Evaluation Benchmark Protocol")
        ]),
        ("SECTION 10: STATUTORY LEGAL METROLOGY RULE MATRIX & JAN VISHWAS ACT 2026", [
            ("docs/LEGAL_RULE_MATRIX.md", "Legal Metrology (Packaged Commodities) Rules, 2011 — Complete Statutory Matrix"),
            ("docs/LEGAL_CHANGELOG_2025_2026.md", "Legal Changelog & Regulatory Evolution (2011–2026)")
        ]),
        ("SECTION 11: DETERMINISTIC RULE ENGINE SPECIFICATIONS & VERIFICATION STRATEGY", [
            ("docs/06_RULE_ENGINE/RULE_ENGINE_SPEC.md", "Deterministic Statutory Rule Engine & Evaluation Spec"),
            ("docs/06_RULE_ENGINE/EXEMPTION_ENGINE.md", "Statutory Exemption Engine Specification (Rules 3 & 26)"),
            ("docs/06_RULE_ENGINE/RULE_TEST_STRATEGY.md", "Rule Verification Strategy & Test Case Design")
        ]),
        ("SECTION 12: CODEBASE MONOREPO ARCHITECTURE, SNAPSHOTS & PERSISTENT CONTEXT", [
            ("CURRENT_STATE/PROJECT_SNAPSHOT.md", "Active Project Snapshot & Architectural Status"),
            ("CURRENT_STATE/REPOSITORY_SNAPSHOT.md", "Monorepo Directory Layout & Subsystem Mapping"),
            ("CURRENT_STATE/CHUNK_4_STATUS.md", "Active Development Phase: Chunk 4 Final Verified Status"),
            ("CURRENT_STATE/CHUNK_4_BASELINE.md", "Chunk 4 Starting Environment Baseline Snapshot"),
            ("CURRENT_STATE/CHUNK_3_FINAL_STATUS.md", "Active Development Phase: Chunk 3 Final Verified Status"),
            ("CURRENT_STATE/CHUNK_3_STATUS.md", "Active Development Phase: Chunk 3 Status Summary"),
            ("CURRENT_STATE/CHUNK_3_CORRECTION_BASELINE.md", "Chunk 3 Correction Baseline Snapshot"),
            ("CURRENT_STATE/CHUNK_3_BASELINE.md", "Chunk 3 Starting Environment Baseline Snapshot"),
            ("CURRENT_STATE/DEPENDENCY_SNAPSHOT.md", "Direct ONNX Runtime Dependency Freeze Snapshot"),
            ("CURRENT_STATE/ENVIRONMENT_SNAPSHOT.md", "Host Machine Hardware, Runtime & Environment Snapshot"),
            ("CURRENT_STATE/GIT_STATE.md", "Git Working Tree State Snapshot (Zero Commits / Zero Push)"),
            ("AI_CONTEXT/PROJECT_CONTEXT.md", "Persistent AI Context & Operating Directives"),
            ("AI_CONTEXT/INDEX.md", "AI Context Directory Index & Knowledge Base")
        ]),
        ("SECTION 13: JURY DEFENSE, ADVERSARIAL Q&A & SCORING RUBRIC", [
            ("docs/JURY_QA.md", "Jury Defense Playbook — 32 Adversarial Technical & Legal Q&A")
        ]),
        ("SECTION 14: RISK REGISTER, ASSUMPTIONS & TRACEABILITY MATRIX", [
            ("docs/RISK_REGISTER.md", "Technical & Operational Risk Register"),
            ("docs/ASSUMPTION_REGISTER.md", "Scientific & Engineering Assumption Register"),
            ("docs/TRACEABILITY_MATRIX.md", "End-to-End Problem Statement to Evaluation Rubric Traceability Matrix")
        ])
    ]
    
    out = []
    
    # Master Header
    out.append(f"""# METROLENS AI™ (METROSETU) — ALL-IN-ONE MASTER CONTEXT SPECIFICATION
### Automated Legal Metrology Inspection & Compliance Platform (SIH26034)
**Status:** CANONICAL MASTER CONTEXT (V1.6 — CHUNK 4 COMPLETED & VERIFIED: MONOREPO PACKAGED, SERVICE ADAPTER IMPLEMENTED, SHARED CONTRACT VERIFIED, B0 BASELINE CANONICAL DEFAULT, MULTI-THREADED CONCURRENCY VERIFIED, 89 REPOSITORY TESTS PASSING)  
**Compilation Timestamp:** {timestamp}  
**Sponsoring Ministry:** Ministry of Consumer Affairs, Food & Public Distribution (Government of India)  
**Repository Working Tree:** Production Web MVP Monorepo (`packages/`, `apps/`, `infra/`, `tests/`)  
**Active Phase:** Chunk 4 Completed & Verified (Service Adapter Operational, 89 Tests Passing, Path B Gate Active) | Chunk 5 Ready  

**Target Duration:** 8–9 Day Sprint | **Team Composition:** 6 Engineers (Decoupled Parallel Execution)

---

## CANONICAL NOTICE
This master document consolidates all authoritative engineering specifications, product blueprints, system architecture, 6-member individual work packages, architectural decisions (ADR-001 through ADR-017), empirical CPU benchmark results, direct ONNX Runtime OCR engine implementations, OCR service adapter specifications, computer vision & calibration specifications, statutory legal rule matrices, and jury defense playbooks for the **MetroLens AI™ (MetroSetu)** project.

It serves as the definitive, zero-ambiguity single source of truth for all human developers, AI agents, and project evaluators.

---

## MASTER TABLE OF CONTENTS
1. [SECTION 1: Product Blueprint, MetroSetu Platform Details & Problem Statement](#section-1-product-blueprint-metrosetu-platform-details--problem-statement)
2. [SECTION 2: Web System Architecture, Security & OpenAPI Contract](#section-2-web-system-architecture-security--openapi-contract)
3. [SECTION 3: 6-Member Team Execution Architecture & Work Packages](#section-3-6-member-team-execution-architecture--work-packages)
4. [SECTION 4: Canonical Architectural Decision Records (ADR-001 to ADR-017)](#section-4-canonical-architectural-decision-records-adr-001-to-adr-017)
5. [SECTION 5: Chunk 1 OCR Feasibility Spike & Engineering Baseline](#section-5-chunk-1-ocr-feasibility-spike--engineering-baseline)
6. [SECTION 6: Chunk 2 OCR Engine Foundation & Direct ONNX Runtime Subsystem](#section-6-chunk-2-ocr-engine-foundation--direct-onnx-runtime-subsystem)
7. [SECTION 7: Chunk 3 Real-Data OCR Validation, Domain Preprocessing & Robustness](#section-7-chunk-3-real-data-ocr-validation-domain-preprocessing--robustness)
8. [SECTION 8: Chunk 4 OCR Monorepo Integration, Service Adapter & Contract Verification](#section-8-chunk-4-ocr-monorepo-integration-service-adapter--contract-verification)
9. [SECTION 9: Computer Vision, Calibration & Optical Measurement Specifications](#section-9-computer-vision-calibration--optical-measurement-specifications)
10. [SECTION 10: Statutory Legal Metrology Rule Matrix & Jan Vishwas Act 2026](#section-10-statutory-legal-metrology-rule-matrix--jan-vishwas-act-2026)
11. [SECTION 11: Deterministic Rule Engine Specifications & Verification Strategy](#section-11-deterministic-rule-engine-specifications--verification-strategy)
12. [SECTION 12: Codebase Monorepo Architecture, Snapshots & Persistent Context](#section-12-codebase-monorepo-architecture-snapshots--persistent-context)
13. [SECTION 13: Jury Defense, Adversarial Q&A & Scoring Rubric](#section-13-jury-defense-adversarial-qa--scoring-rubric)
14. [SECTION 14: Risk Register, Assumptions & Traceability Matrix](#section-14-risk-register-assumptions--traceability-matrix)

---
""")

    for sec_title, file_list in sections:
        if not file_list:
            continue
        
        anchor = sec_title.lower().replace(" ", "-").replace(":", "").replace("(", "").replace(")", "").replace("&", "")
        out.append(f"\n\n# {sec_title}\n")
        out.append(f"**Section Anchor:** `{anchor}`\n\n---\n")
        
        for rel_path, doc_title in file_list:
            content = read_file(rel_path)
            out.append(f"\n\n# --- SOURCE: {rel_path} ({doc_title}) ---\n\n")
            out.append(content)
            out.append("\n\n---\n")
            print(f"  [+] Ingested: {rel_path} ({len(content):,} chars)")
            
    master_content = "\n".join(out)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(master_content)
        
    print(f"\nSuccessfully written master context to: {OUTPUT_FILE}")
    print(f"Total Size: {len(master_content):,} characters | {len(master_content.splitlines()):,} lines.")

if __name__ == "__main__":
    build_master_context()
