# MetroLens AI™ — Automated Legal Metrology Inspection & Compliance System
### Sponsoring Ministry: Ministry of Consumer Affairs, Food & Public Distribution | Problem Statement: SIH26034
**Evaluation Framework:** InnoHack 3.0 / Smart India Hackathon 2026 | **Document Status:** Authoritative Repository Overview  
**Local Environment:** Python 3.14+ | Node.js v25+ | Git 2.52+ | **Architecture:** 100% Offline Edge-Native

---

<p align="center">
  <img src="docs/GLOBAL_TEAM_WORKFLOW.svg" alt="MetroLens AI Global Team Development Workflow" width="100%" style="max-width: 1050px; height: auto; display: block; margin: 0 auto;" />
</p>

---

## 📌 Executive Summary

**MetroLens AI™** is an edge-native, perspective-corrected mobile computer vision and regulatory audit system designed for District Legal Metrology Officers (LMOs) and packaging compliance auditors. It transforms a tedious, manual 20-minute ruler-and-magnifier inspection into a **sub-2.5-second, mathematically verified, tamper-evident regulatory compliance audit**.

By combining a **universally available optical metric anchor** (a standard 10-Rupee coin or ISO card) with **planar metric scale calibration**, MetroLens AI solves the fundamental monocular scale ambiguity of smartphone cameras. It directly evaluates statutory numeral heights (Rule 7 Table-I/II) against calibrated Principal Display Panel (PDP) areas, audits Unit Sale Price (USP) arithmetic against Net Quantity and MRP under Rule 6(11) in standardized denominations, extracts mandatory packaging declarations across English and Hindi using local scene text OCR, and verifies compliance through a **100% deterministic statutory state machine**.

The system operates **entirely offline** on local edge hardware without external cloud dependency, generates a cryptographically sealed (SHA-256) **Image-Based Compliance Assessment Report** under Section 15 of the Legal Metrology Act, 2009 (incorporating the **Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice framework** under Section 36(1)), and provides an **eMaap-Inspired Mock REST Adapter Interface** ready for national portal integration.

---

## 🚀 Newly Committed Core Files & Deliverables

The latest repository commits deliver the authoritative engineering workflow, architecture visuals, authentic legal source archives, and automation tooling:

| Core Deliverable / File | Type / Scope | Description |
| :--- | :--- | :--- |
| [`GLOBAL_TEAM_WORKFLOW.md`](GLOBAL_TEAM_WORKFLOW.md) | **Governance & Workflow** | Comprehensive 36-section team development guide adhering to RFC 2119 standards. Covers Optimized GitHub Flow, Conventional Commits, DoR/DoD, testing matrix, code review protocols, and beginner troubleshooting. |
| [`docs/DEFINITION_OF_READY.md`](docs/DEFINITION_OF_READY.md) | **Governance & DoR Gate** | Authoritative 10-point Definition of Ready specification with real-world subsystem examples, state lifecycle transitions, and beginner quick-start checklist. |
| [`docs/GLOBAL_TEAM_WORKFLOW.svg`](docs/GLOBAL_TEAM_WORKFLOW.svg) | **Visual Architecture** | High-resolution vector flowchart illustrating all 5 lifecycle phases (Task DoR $\rightarrow$ Branch Isolation $\rightarrow$ Commits & Sync $\rightarrow$ PR & CI $\rightarrow$ Squash Merge), linear trunk architecture, and golden rules. |
| [`METROLENS_LEGAL_SOURCE_PACK/`](METROLENS_LEGAL_SOURCE_PACK/) | **Official Legal Pack** | Stage 1 verified archive of authentic Ministry of Consumer Affairs (DoCA) gazettes, Primary Acts (2009, Jan Vishwas 2023 & 2026), LMPC Amendments (2011–2026), GST Advisories, Enforcement SOPs, and Judicial Precedents. |
| [`METROLENS_LEGAL_SOURCE_PACK/00_SOURCE_INDEX/CHECKSUM_MANIFEST.csv`](METROLENS_LEGAL_SOURCE_PACK/00_SOURCE_INDEX/CHECKSUM_MANIFEST.csv) | **Cryptographic Manifest** | SHA-256 integrity checksums and metadata catalog for all official legal PDFs. |
| [`ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`](ALL-IN-ONE%20context/METROLENS_AI_ALL_IN_ONE_DOCS.md) | **Master Context** | Single unified 228KB engineering dossier consolidating all research, statutory rules, technical specs, and hackathon strategies. |
| [`tools/legal_sources/collect_official_legal_sources.py`](tools/legal_sources/collect_official_legal_sources.py) | **Operational Tooling** | Automated, reproducible Python pipeline script for scraping, validating, checksumming, and cataloging official legal gazette publications. |
| [`MVP_UNIFIED_WORKFLOW_GRAPH.md`](MVP_UNIFIED_WORKFLOW_GRAPH.md) | **Technical Architecture** | Master 16-node unified MVP workflow graph, data contracts, failure fallback policies, and M1–M6 team ownership matrix. |
| [`docs/PRODUCT_BLUEPRINT.md`](docs/PRODUCT_BLUEPRINT.md) | **Technical Specification** | Master Product Blueprint v0.3 establishing the system architecture, mathematical proofs, optical formulas, and acceptance criteria. |
| [`docs/LEGAL_RULE_MATRIX.md`](docs/LEGAL_RULE_MATRIX.md) | **Statutory Rule Matrix** | Formal codification of Legal Metrology (Packaged Commodities) Rules, 2011 and 2026 statutory amendments. |
| [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) | **Execution Roadmap** | 8–9 day execution plan with the 6-member cross-functional allocation matrix and 24-hour validation spikes. |

---

## 🏛️ The Four Architectural Pillars

MetroLens AI enforces strict boundaries between probabilistic AI extraction, exact mathematical calibration, deterministic legal logic, and authorized officer discretion:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AI PERCEIVES (Probabilistic Optical Extraction)                          │
│ • Quantized PaddleOCR v4 Mobile (DBNet++, SVTR) running on local CPU.       │
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
│ • 5-State compliance classification and 1-tap inspector confirmation UI.    │
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

Aligned with the dual-project hackathon allocation defined in [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md):

| Member | Primary Role | Secondary Support | Core Subsystem Ownership |
| :---: | :--- | :--- | :--- |
| **M1** | **AI & OCR Lead** | Backend API Support | PaddleOCR ONNX int8 runtime, CPU thread optimization, Devanagari translation mapping, text box cropping. |
| **M2** | **Calibration & Geometry Lead** | Physical Data Collection | Optical metric scale recovery ($S = 27.0\text{mm} / d_{\text{major}}$), coin contour detection, vertical cylinder generator invariance. |
| **M3** | **Backend & Rule Engine Lead** | Architecture Governance | FastAPI server, Pydantic canonical schemas, deterministic Legal Metrology state machine (Rules 6, 7, 8, 26), USP math auditor. |
| **M4** | **Frontend & UX Lead** | Demo Stagecraft Support | Responsive Vite/React PWA, camera WebRTC viewfinder, 5-state compliance badges, side-by-side evidence viewer. |
| **M5** | **Data & Benchmark Lead** | Calibration Support | Physical packaging collection (35+ SKUs), 1200 DPI flatbed ground-truth optical scanning, automated CER/WER evaluation. |
| **M6** | **Product, DevOps & Presentation Lead** | QA & Compliance Audit | Repository governance, GitHub CI/CD workflows, cryptographic SHA-256 PDF report generator, eMaap mock sync adapter. |

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
pytest backend/tests/

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
*For questions or technical contributions, refer to [`GLOBAL_TEAM_WORKFLOW.md`](GLOBAL_TEAM_WORKFLOW.md) or open an issue on the repository.*
