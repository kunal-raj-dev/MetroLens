# MetroLens AI™ — Automated Legal Metrology Inspection & Compliance System
### Sponsoring Ministry: Ministry of Consumer Affairs, Food & Public Distribution | Problem Statement: SIH26034
**Evaluation Framework:** InnoHack 3.0 / Smart India Hackathon 2026 | **Document Status:** Authoritative Repository Overview  
**Environment:** Python 3.14+ | Node.js v25+ | Git 2.52+ | **Architecture:** Online Web Application MVP (FastAPI + React) with Deterministic Core

---

<p align="center">
  <img src="docs/GLOBAL_TEAM_WORKFLOW.svg" alt="MetroLens AI Global Team Development Workflow" width="100%" style="max-width: 1050px; height: auto; display: block; margin: 0 auto;" />
</p>

---

## 📌 Executive Summary

**MetroLens AI™** is an online web application and automated regulatory audit platform designed for District Legal Metrology Officers (LMOs), retail packaging compliance managers, brand quality assurance teams, and e-commerce catalog auditors. It transforms a tedious, manual 20-minute ruler-and-magnifier inspection into a **sub-2.5-second, mathematically verified, tamper-evident regulatory compliance audit**.

The primary product experience is centered on an intuitive web interaction paradigm:
$$\text{UPLOAD IMAGE(S)} \longrightarrow \text{VALIDATE} \longrightarrow \text{PROCESS} \longrightarrow \text{ANALYZE} \longrightarrow \text{VERIFY} \longrightarrow \text{EXPLAIN RESULT}$$

By combining an accessible **browser-based image upload dropzone** with **planar metric scale calibration** (recovering millimeters-per-pixel via a 10-Rupee coin or ISO card anchor), MetroLens AI solves the fundamental monocular scale ambiguity of smartphone photos. It directly audits statutory numeral heights (Rule 7 Table-I/II) against calibrated Principal Display Panel (PDP) areas, verifies Unit Sale Price (USP) arithmetic against Net Quantity and MRP under Rule 6(11) in standardized denominations, extracts mandatory packaging declarations across English and Hindi using server-side quantized scene text OCR, and verifies compliance through a **100% deterministic statutory state machine**.

The system operates as a **first-class online web application** backed by containerized FastAPI endpoints, executes all neural inference on CPU with zero paid cloud AI API dependencies, generates a cryptographically sealed (SHA-256) **Image-Based Compliance Assessment Report PDF** under Section 15 of the Legal Metrology Act, 2009 (incorporating the **Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice framework** under Section 36(1)), and provides an **eMaap-Inspired Mock REST Adapter Interface** ready for national portal integration.

---

## 🚀 Authoritative Project Documentation Suite

The repository is governed by authoritative specifications and architecture contracts:

| Core Specification | Document Scope | Description |
| :--- | :--- | :--- |
| [`docs/PRODUCT_BLUEPRINT.md`](docs/PRODUCT_BLUEPRINT.md) | **Product Master Specification** | Authoritative Blueprint v1.0 defining product vision, user journey, single/multi-image architecture, 5-state framework, and success metrics. |
| [`docs/METROSETU_PROJECT_DETAILS.md`](docs/METROSETU_PROJECT_DETAILS.md) | **Platform Master Guide** | Comprehensive end-to-end guide: statutory context, 5-step user journey, real-world defect scenarios, 5-layer failovers, and competition demonstration script. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | **System Architecture & Security** | Comprehensive web system architecture, synchronous vs. async analysis, upload pipeline, and threat model. |
| [`docs/TEAM_RESPONSIBILITIES.md`](docs/TEAM_RESPONSIBILITIES.md) | **Team RACI & Workstreams** | Authoritative 6-member (M1–M6) ownership matrix, "Not My Job" boundaries, workstream dependency graph, and handoffs. |
| [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md) | **REST API & Schemas** | Frozen OpenAPI 3.1 contract: `POST /api/v1/inspect`, error taxonomies, and Pydantic canonical schemas. |
| [`docs/TESTING_STRATEGY.md`](docs/TESTING_STRATEGY.md) | **Quality Assurance & Verification** | Multi-tiered testing pyramid, automated test nodes (T01–T06), upload fuzzing, and anti-hallucination verification gates. |
| [`GLOBAL_TEAM_WORKFLOW.md`](GLOBAL_TEAM_WORKFLOW.md) | **Governance & Workflow** | Comprehensive 36-section team development guide: Optimized GitHub Flow, Conventional Commits, DoR/DoD gates. |
| [`MVP_UNIFIED_WORKFLOW_GRAPH.md`](MVP_UNIFIED_WORKFLOW_GRAPH.md) | **Pipeline Node Architecture** | Master 16-node unified MVP workflow graph, data contracts, failure fallback policies, and mock fixtures. |
| [`docs/TECHNICAL_DECISIONS.md`](docs/TECHNICAL_DECISIONS.md) | **Architecture Decision Records** | ADR-001 through ADR-014 recording trade-offs in OCR, calibration, web delivery, security, and retention. |
| [`docs/DEFINITION_OF_READY.md`](docs/DEFINITION_OF_READY.md) | **Governance & DoR Gate** | Authoritative 10-point Definition of Ready specification with real-world subsystem examples. |
| [`METROLENS_LEGAL_SOURCE_PACK/`](METROLENS_LEGAL_SOURCE_PACK/) | **Official Legal Source Archive** | Stage 1 verified archive of authentic Ministry of Consumer Affairs gazettes, Acts (2009, 2023, 2026), and LMPC Rules. |

---

## 🏛️ The Four Architectural Pillars

MetroLens AI enforces strict boundaries between probabilistic AI extraction, exact mathematical calibration, deterministic legal logic, and authorized officer discretion:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AI PERCEIVES (Probabilistic Optical Extraction)                          │
│ • Quantized PaddleOCR v4 Mobile (DBNet++, SVTR) running on server CPU.      │
│ • Extracts raw character strings and bounding boxes across English & Hindi.  │
│ • Strict Boundary: AI NEVER decides whether a package violates the law.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MATH VALIDATES (Empirical Geometric & Metric Calibration)                │
│ • Planar scale recovery via 10-Rupee coin anchor (27.0mm diameter).         │
│ • IEEE 754 floating-point arithmetic for Unit Sale Price (USP) division.    │
│ • Strict Boundary: Zero heuristic rounding; strict standard denominations.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. RULES DECIDE (100% Deterministic Statutory Engine)                       │
│ • Isolated Python state machine (Rules 6, 7 Table-I/II, 8, 26).             │
│ • Codifies Gazette clauses, area brackets, and statutory exemptions.        │
│ • Strict Boundary: 100% deterministic, audit-traceable, version-stamped.    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HUMANS GOVERN (Regulatory Discretion & Enforcement)                      │
│ • 5-State compliance classification and interactive web evidence viewer.    │
│ • Inspecting officer reviews visual crops and issues statutory notices.     │
│ • Strict Boundary: System acts as assistive screening under Section 15.    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚦 Five-State Regulatory Compliance Framework

To eliminate false-positive harassment of honest merchants, MetroLens AI categorizes every inspection into one of five rigorous regulatory states:

| Status Badge | Regulatory Classification | Action Required |
| :---: | :--- | :--- |
| 🟢 **Green** | `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` | All mandatory declarations present, font heights conform to Rule 7 tables, USP matches net quantity. Pass. |
| 🔴 **Red** | `POTENTIAL_NON_COMPLIANCE` | Mandatory field omitted, severe font deficit ($> 0.10\text{mm}$), USP arithmetic discrepancy ($> 1\%$), or non-standard units. Recommend Section 36(1) Improvement Notice. |
| 🟡 **Amber** | `MANUAL_REVIEW_REQUIRED` | Borderline font height (within $0.10\text{mm}$ benefit-of-doubt buffer), OCR confidence $60\text{--}80\%$, or non-planar curvature. Inspector 1-tap verification. |
| 🔵 **Blue** | `STATUTORY_EXEMPTION_APPLIED` | Package Net Qty $\le 10\text{g}$ / $\le 10\text{ml}$ (non-tobacco) or wholesale packaging $> 25\text{kg}$ under Rule 26. Violations suppressed. |
| ⚪ **Gray** | `NOT_IMAGE_VERIFIABLE` | Physical net content weight verification under Rule 24 or chemical purity (FSSAI). Flags for physical certified scale check. |

---

## 👥 Six-Member Engineering Ownership Matrix

Aligned with [`docs/TEAM_RESPONSIBILITIES.md`](docs/TEAM_RESPONSIBILITIES.md):

| Member | Primary Role | Secondary Support | Core Subsystem Ownership |
| :---: | :--- | :--- | :--- |
| **M1** | **AI & OCR Perception Lead** | Backend API Support | PaddleOCR ONNX int8 runtime, CPU thread optimization, Devanagari translation mapping, text box cropping. |
| **M2** | **Calibration & Geometry Lead** | Physical Data Collection | Optical metric scale recovery ($S = 27.0\text{mm} / d_{\text{major}}$), coin contour detection, vertical cylinder generator invariance. |
| **M3** | **Backend & Rule Engine Lead** | Architecture Governance | FastAPI server, Pydantic canonical schemas, deterministic Legal Metrology state machine (Rules 6, 7, 8, 26), USP math auditor. |
| **M4** | **Frontend & Web UX Lead** | Demo Stagecraft Support | Responsive Vite/React web application, image upload dropzone, 5-state compliance badges, side-by-side evidence viewer. |
| **M5** | **Data & Benchmark Lead** | Calibration Support | Physical packaging collection (35+ SKUs), 1200 DPI flatbed ground-truth optical scanning, automated CER/WER evaluation. |
| **M6** | **Product, DevOps & Security Lead** | QA & Compliance Audit | Repository governance, GitHub CI/CD workflows, upload security hardening, cryptographic SHA-256 PDF report generator, eMaap mock sync. |

---

## 🛠️ Repository Architecture & Directory Structure

```text
MetroLens/
├── GLOBAL_TEAM_WORKFLOW.md                 # Authoritative 36-Section Team Development Workflow
├── MVP_UNIFIED_WORKFLOW_GRAPH.md           # Master 16-Node Workflow Graph & JSON Contracts
├── README.md                               # Project Overview, Setup & Deliverables
├── ALL-IN-ONE context/                     # Unified Master Documentation Dossier (228KB)
│   └── METROLENS_AI_ALL_IN_ONE_DOCS.md
├── docs/                                   # Architecture, Legal & Planning Suite (v0.3)
│   ├── GLOBAL_TEAM_WORKFLOW.svg            # Vector Visual Architecture Diagram
│   ├── PRODUCT_BLUEPRINT.md                # Master Product Blueprint & Technical Specs
│   ├── LEGAL_RULE_MATRIX.md                # Statutory Rules & 2026 Legal Foundation
│   ├── TECHNICAL_DECISIONS.md              # Architecture Decision Records (ADRs)
│   ├── IMPLEMENTATION_PLAN.md              # 8–9 Day Roadmap & Member Allocation
│   ├── DATA_AND_BENCHMARK_PLAN.md          # 35-SKU Ground-Truth Benchmark Protocol
│   ├── DEMO_PLAN.md                        # Live Pitch Script & 5-Layer Failover
│   ├── RISK_REGISTER.md                    # 15 Risks & 48-Hour Kill Switch Protocol
│   └── JURY_QA.md                          # 32 Adversarial Questions & Defenses
├── METROLENS_LEGAL_SOURCE_PACK/            # Stage 1 Official Legal Source Archive
│   ├── 00_SOURCE_INDEX/                    # Registries, Timelines & Checksum Manifest
│   ├── 01_PRIMARY_ACTS/                    # Legal Metrology Act 2009 & Jan Vishwas Acts
│   ├── 02_CURRENT_CONSOLIDATED_RULES/      # Consolidated LMPC Rules 2011
│   ├── 03_PACKAGED_COMMODITIES_AMENDMENTS/ # Official Gazette Amendments (2011–2026)
│   ├── 04_OFFICIAL_NOTIFICATIONS/          # Commencement & Enforcement Notifications
│   ├── 05_OFFICIAL_FAQ_GUIDANCE/           # Official FAQs & GST Price Revision Orders
│   ├── 06_OFFICIAL_ENFORCEMENT_INSPECTION/ # SOPs & Landmark Supreme Court Judgments
│   └── 07_E_MAAP/                          # NIC eMaap System Design & Workflows
└── tools/                                  # Automation & Validation Tooling
    └── legal_sources/
        └── collect_official_legal_sources.py
```

---

## ⚡ Quick Start for Developers

For complete developer onboarding and daily routines, review [Section 36 of `GLOBAL_TEAM_WORKFLOW.md`](GLOBAL_TEAM_WORKFLOW.md#36-new-teammate-quick-start).

### 1. Clone & Configure
```bash
git clone https://github.com/kunal-raj-dev/MetroLens.git
cd MetroLens

# Configure identity
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. Starting Work on an Assigned Task
```bash
# Always start from fresh, updated main
git checkout main
git fetch origin
git pull --ff-only origin main

# Create your dedicated branch (kebab-case, prefixed)
git checkout -b feat/14-usp-arithmetic-auditor
```

### 3. Local Verification & Commits
```bash
# Run tests locally
python -m pytest tests/

# Commit using Conventional Commits
git add <modified-files>
git commit -m "feat(rules): implement Rule 6(11) USP rounding logic"

# Push branch and open Pull Request
git push -u origin feat/14-usp-arithmetic-auditor
```

---

## ⚖️ Statutory & Legal References
* **Primary Act:** *The Legal Metrology Act, 2009* (Act No. 1 of 2010).
* **Principal Rules:** *Legal Metrology (Packaged Commodities) Rules, 2011* (G.S.R. 202(E)).
* **Decriminalization Mandate:** *Jan Vishwas (Amendment of Provisions) Act, 2023 & 2026* (Decriminalization of Section 36(1) and introduction of statutory Improvement Notices).
* **Evidentiary Standard:** *Bharatiya Sakshya Adhiniyam, 2023* (Section 63) / *Indian Evidence Act, 1872* (Section 65B electronic record integrity).

---

## 🔍 Verification Automation & Integrity Scripts

To ensure consistency and prevent hallucination across the codebase, automated verification scripts are available:
```bash
# Verify all legal source artifacts, checksums, and registry entries
python scripts/verification/verify_legal_sources.py

# Verify machine-readable rules against schema and source provenance
python scripts/verification/verify_rule_registry.py

# Verify claim statuses against empirical benchmark reports
python scripts/verification/verify_claims.py

# Verify dataset manifests and licenses
python scripts/verification/verify_dataset_manifest.py

# Verify end-to-end verification pipeline
python -m pytest tests/unit/test_verification_pipeline.py
```

---

## 📜 Licensing & Legal Disclaimer

- Software code is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE).
- Third-party licenses, data permissions, and legal notices are detailed in:
  - [`docs/LEGAL_NOTICES.md`](docs/LEGAL_NOTICES.md)
  - [`docs/THIRD_PARTY_LICENSES.md`](docs/THIRD_PARTY_LICENSES.md)
  - [`docs/DATA_LICENSES.md`](docs/DATA_LICENSES.md)

> **Official Notice:** MetroLens AI is an engineering decision-support tool. It does not replace the statutory authority of an Inspector of Legal Metrology. Generated reports constitute technical inspection assistance and provenance records; statutory evidentiary determination remains the exclusive prerogative of competent authorities under applicable law and procedure.

---
*For questions or technical contributions, refer to [`GLOBAL_TEAM_WORKFLOW.md`](GLOBAL_TEAM_WORKFLOW.md) or open an issue on the repository.*

