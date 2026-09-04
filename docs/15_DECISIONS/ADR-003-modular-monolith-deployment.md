# ADR-003: Modular Monolith vs. Distributed Microservices Architecture

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Backend / Infra Lead, DevOps Lead

---

## Context & Problem Statement
The inspection pipeline involves multiple stages: image ingestion, blur/glare quality gate, optical calibration, text detection/OCR, field extraction, geometric measurement, rule execution, cryptographic signing, and dossier rendering.

We must decide on the software architecture and deployment topology: a distributed microservices network (e.g. 10+ separate containers communicating via network RPC) versus a modular monolith package architecture with an API service, background worker, and lightweight web client.

---

## Decision Drivers
- **Operational Feasibility**: The system must run reliably on offline edge hardware (laptops, on-premise local inspection servers) and standard developer setups without Kubernetes or network service meshes.
- **Latency & Reliability**: Eliminating inter-service HTTP/gRPC serialization overhead, connection timeouts, and distributed failure states during inspection.
- **Development Velocity**: Team leads need clear package ownership without the friction of deploying 10 different network services locally.

---

## Considered Options
1. **Option 1: Python Modular Monolith with Shared Packages** (Chosen)
   - Clean boundary packages (`packages/*`) with typed interfaces, running within a unified API service and asynchronous task worker.
2. **Option 2: 12-Service Distributed Microservices**
   - Independent microservice per pipeline step (Vision Service, OCR Service, Rule Service, etc.) orchestrated via Kafka/RabbitMQ.
3. **Option 3: Single Unstructured Script / Monolithic App**

---

## Decision Outcome
**Chosen Option:** Option 1: Python Modular Monolith with Shared Packages.
The architecture organizes domain logic into discrete reusable packages (`packages/*`), which are deployed via Docker Compose as an API container, an async task worker, a Next.js web UI, and a PostgreSQL database.

### Positive Consequences
- Zero network hops between pipeline calculation stages within the worker process.
- Can be packaged into a single self-contained offline installer.
- Simplifies local debugging, end-to-end integration testing, and CI execution.

### Negative Consequences / Trade-offs
- Scaling compute-heavy OCR independently requires dedicating worker replica instances.

---

## References & Statutory Linkages
- Lean Architecture Mandate (`docs/04_ARCHITECTURE/`).
- System Architecture Specification (`docs/04_ARCHITECTURE/SYSTEM_ARCHITECTURE.md`).
