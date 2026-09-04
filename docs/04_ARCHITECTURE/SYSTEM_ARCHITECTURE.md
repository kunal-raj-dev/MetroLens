# Nirikshak System Architecture Specification

## Purpose
Documents the high-level architecture, module decomposition, inter-process communication, and technology stack of Nirikshak.

## Scope
Encompasses the client presentation tier, API gateway, inspection pipeline, rule engine, data persistence, and offline edge capabilities.

## Authoritative Inputs
- SIH 2026 Problem Statement 26034.
- Lean Hackathon Architecture Mandate: Avoid microservice overengineering.

## Assumptions
- The system operates as a unified modular monolith / 3-tier architecture capable of running locally on an inspector's workstation or portable device.

## Open Questions
- Target embedded runtime for ultra-low-power field hardware [TBD — MEASURE].

## Dependencies
- `apps/`
- `packages/`
- `infra/`

## Verification Requirements
- End-to-end integration tests must confirm communication between UI, API, pipeline, and storage.

---

## 1. High-Level Architectural Diagram

```mermaid
graph TD
    subgraph Client Tier ["Client / Field Device (Web/Mobile UI)"]
        UI["Guided Capture UI & Inspection Dashboard (apps/web)"]
        CamPreview["Real-Time Camera Preview & Quality Feedback"]
        ReviewScreen["Interactive Bounding Box & Dossier Review"]
    end

    subgraph API Tier ["Core Service API (apps/api)"]
        Gateway["FastAPI Gateway (REST / JSON)"]
        AuthRBAC["RBAC & Session Manager"]
        IngestionCtrl["Ingestion & Hashing Controller"]
    end

    subgraph Inspection Pipeline ["Inspection Engine (packages/)"]
        QGate["Image Quality Gate (Laplacian Blur & Specular Glare)"]
        Calib["Optical Scale Calibration (mm/pixel)"]
        PDPSeg["PDP Boundary Segmentation & Area Calculation"]
        OCR["Multilingual OCR & Text Localization"]
        Extract["Mandatory Declaration Categorization"]
        RuleEng["Deterministic Rule Engine (Historical Snapshots)"]
    end

    subgraph Persistence Tier ["Local / Remote Storage"]
        DB[(PostgreSQL / SQLite Database)]
        DocStore[(Local File System / Object Storage)]
        AuditLog[(Cryptographic Append-Only Audit Log)]
    end

    UI -->|Image Frames & Meta| Gateway
    Gateway --> IngestionCtrl
    IngestionCtrl -->|Compute SHA-256| QGate
    QGate -->|Clean Frames| Calib
    Calib --> PDPSeg
    PDPSeg --> OCR
    OCR --> Extract
    Extract --> RuleEng
    RuleEng -->|Verdict: PASS / FAIL / REVIEW| ReviewScreen
    ReviewScreen -->|Officer Sign-Off| AuditLog
    AuditLog --> DB
    IngestionCtrl --> DocStore
```

---

## 2. Core Architectural Principles

1. **AI as Observation, Determinism for Law:**
   Computer vision models locate text and segment polygons. They do NOT evaluate legality. All legal decisions are computed by purely deterministic rule evaluators matching statutory thresholds.

2. **Zero Architecture Cosplay (Lean & Robust):**
   Rather than spinning up 14 distributed microservices, message queues, and Kubernetes pods, Nirikshak uses a battle-tested modular structure:
   - Client Web UI (`apps/web`)
   - High-throughput asynchronous API (`apps/api`)
   - Pure Python / C++ optimized packages (`packages/*`)
   - Embedded SQLite / PostgreSQL storage (`infra/db`)

3. **Regulatory Snapshot Versioning:**
   The rule engine loads historical rule schemas matching the package's declared manufacturing date.

4. **Offline-First Resilience:**
   The entire stack can execute self-contained on a field laptop without active external internet access.
