# ADR-004: Cryptographic Directed Acyclic Graph (DAG) Evidence Chain of Custody

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Systems & Security Lead, Legal Engineering Lead

---

## Context & Problem Statement
When an inspection report alleges a violation of the Legal Metrology Act (such as undersized font height or missing country of origin), the evidence must be admissible and legally defensible. A standard relational database table row or flat JSON report can be modified after the fact, creating evidentiary vulnerability in court proceedings.

We must decide how evidence items, optical crops, intermediate measurements, and rule decisions are structured and validated for immutability.

---

## Decision Drivers
- **Legal Admissibility**: Conformance to electronic record evidence standards under Section 65B of the Indian Evidence Act, 1872 / Bharatiya Sakshya Adhiniyam, 2023.
- **Tamper Evidence**: Any alteration to raw image pixels, cropped bounding boxes, or evaluated values must break the cryptographic hash chain.
- **Traceability**: Ability to trace from a final violation notice directly back to the exact source pixel polygon.

---

## Considered Options
1. **Option 1: Cryptographic Directed Acyclic Graph (DAG) Evidence Nodes** (Chosen)
   - Every raw frame is hashed (SHA-256). Every derivative observation, bounding box, crop, and rule evaluation contains cryptographic hashes referencing its parent node.
2. **Option 2: Flat Relational Database Rows**
   - Storing OCR results and violations as flat database records with auto-increment IDs.
3. **Option 3: External Blockchain Ledger**
   - Writing evidence hashes to a public or permissioned blockchain network.

---

## Decision Outcome
**Chosen Option:** Option 1: Cryptographic Directed Acyclic Graph (DAG) Evidence Nodes.
Evidence items are modeled according to `rules/schema/evidence.schema.json`, linking raw image SHA-256 hashes, normalized coordinates, observed values, and calibration metrics into an immutable directed acyclic graph.

### Positive Consequences
- Guarantees forensic integrity and verifiable chain-of-custody.
- Enables cryptographic verification of generated PDF inspection dossiers.
- Self-contained and operable offline without external blockchain transaction fees or connectivity requirements.

### Negative Consequences / Trade-offs
- Requires generating and storing SHA-256 checksums and parent-child linkage references at every pipeline stage.

---

## References & Statutory Linkages
- Indian Evidence Act Section 65B / Bharatiya Sakshya Adhiniyam, 2023.
- `rules/schema/evidence.schema.json`.
