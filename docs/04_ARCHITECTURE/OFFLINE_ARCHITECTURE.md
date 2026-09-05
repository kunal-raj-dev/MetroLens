# Offline Edge Architecture & Synchronization

## Purpose
Specifies the offline execution capability, local caching, embedded inference runtimes, and eventual consistency synchronization for field inspections.

## Scope
Covers standalone field laptops, mobile devices, and disconnected environments (e.g. basement godowns, rural wholesale markets).

## Authoritative Inputs
- Field operational constraints of enforcement officers under Legal Metrology Act, 2009.

## Assumptions
- An inspecting officer must be able to perform the complete inspection workflow (capture, quality gate, calibration, OCR, rule evaluation, PDF report generation) without an active internet connection.

## Open Questions
- Departmental protocol for conflict resolution if two officers inspect identical batch numbers offline [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `apps/web/`
- `apps/api/`
- `packages/`

## Verification Requirements
- Verification test `tests/e2e/test_offline.py` must execute full inspection with network interfaces disabled.

---

## Offline-First Operational Topology

```
┌────────────────────────────────────────────────────────┐
│ STANDALONE FIELD WORKSTATION / MOBILE DEVICE           │
│                                                        │
│  [Local UI (Browser/App)]                              │
│             │                                          │
│             ▼                                          │
│  [Local FastAPI Server (localhost:8000)]               │
│             │                                          │
│             ▼                                          │
│  [Embedded OCR & Vision Engine (ONNX / CPU)]           │
│             │                                          │
│             ▼                                          │
│  [Deterministic Rule Engine (Local rules/ snapshot)]   │
│             │                                          │
│             ▼                                          │
│  [Local Encrypted SQLite DB & PDF Dossier Generator]   │
└───────────────────────────┬────────────────────────────┘
                            │ When Online
                            ▼ (Opportunistic Sync)
┌────────────────────────────────────────────────────────┐
│ CENTRAL DEPARTMENTAL SERVER (Post-Inspection Sync)     │
│  • Bulk Dossier Ingestion                              │
│  • Central Market Surveillance Aggregation             │
│  • Cryptographic Hash Integrity Verification           │
└────────────────────────────────────────────────────────┘
```

### Local Resilience Guarantees
1. **Zero External API Calls:** No external cloud OCR APIs (e.g. Google Cloud Vision or AWS Rekognition) are required during inspection.
2. **Local Cryptographic Ledger:** Inspection records are hashed and signed locally; tampering with the local database is detected on sync.
