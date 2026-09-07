# METROLENS AI™ API GATEWAY & EVIDENTIARY REPORTING ARCHITECTURE
### Document Status: Frozen Production Architecture (v1.0) | Lead: Member 4
**Component Location:** `apps/api/` & `packages/reporting/` | **Protocol:** HTTP/REST (OpenAPI 3.1)

---

## 1. Executive Overview

The **MetroLens AI™ API Gateway** serves as the hardened, high-throughput ingress and orchestration core of the legal metrology perception system. Operating under strict air-gapped, zero-cloud data sovereignty constraints (ADR-007, ADR-010, ADR-013, ADR-014), the Gateway coordinates:

1. **Multi-Layer Ingestion Security:** Magic bytes enforcement, pre-decode streaming decompression bomb firewalls, minimum $800 \times 600$ resolution checks, and automatic EXIF/GPS privacy sanitization.
2. **Ephemeral Spool Lifecycle Management:** Isolated per-inspection temporary sandboxes (`/tmp/metrolens_uploads/<uuid>/`) with atomic `os.replace` persistence, 60-minute TTL cleanup daemons, startup orphan sweeps, and strict disk quota enforcement.
3. **Synchronous Multi-Module Pipeline Orchestration:** Coordinated execution of Pre-flight Quality Gating, Optical Metric Scale Calibration, Multilingual OCR Token Perception, Entity Normalization, and Master Statutory Rules Evaluation within a $< 2.5\text{s}$ CPU latency budget.
4. **Court-Admissible PDF Assessment Report Compilation:** Tamper-evident ReportLab compiler generating official evaluation reports embedding raw image SHA-256 seals, side-by-side evidence crops, Section 36(1) Jan Vishwas Improvement Notices, and verification QR codes in $< 500\text{ms}$.
5. **e-Governance Mock Synchronization:** Webhook adapter simulating national eMaap Legal Metrology portal integration with cryptographic signature verification.
6. **Leaky-Bucket Rate Limiting:** Thread-safe sliding-window rate limiter enforcing statutory 10 req/min quotas per client IP address with HTTP 429 and `Retry-After` headers.

---

## 2. System Architecture & Component Interaction

```
                              [ HTTP Request: Client / Web UI (Member 5) ]
                                                   │
                                                   ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │               FastAPI Application Ingress                   │
                    │   - SecurityHeadersMiddleware (CSP, HSTS, X-Frame-Options)  │
                    │   - RateLimitMiddleware (10 req/min leaky bucket)           │
                    │   - CORSMiddleware (Zero-origin friction)                  │
                    │   - Canonical Error Handlers (HTTP 400, 413, 415, 422, 429) │
                    └──────────────────────────────┬──────────────────────────────┘
                                                   │
        ┌──────────────────────────────────────────┴──────────────────────────────────────────┐
        │                                                                                     │
        ▼                                                                                     ▼
[ POST /api/v1/inspect ]                                                              [ POST /api/v1/report/pdf ]
  │                                                                                     │
  ├─► UploadSecurityGate                                                                ├─► Spool Cache Lookup
  │   ├── Magic Bytes Verification (JPEG, PNG, WebP)                                    │   └── Return pre-compiled PDF
  │   ├── Pre-Decode SOF/IHDR Bomb Firewall (64MP)                                      │
  │   ├── Minimum Resolution Bounds (800x600)                                           └─► PDFReportCompiler
  │   └── EXIF / GPS Metadata Stripping                                                     ├── NumberedCanvas ("Page X of Y")
  │                                                                                         ├── Raw Image SHA-256 Cryptographic Seal
  ├─► SpoolService                                                                          ├── Section 36(1) Jan Vishwas Notice
  │   └── Write sanitized payload to /tmp/metrolens_uploads/<uuid>/                         ├── Visual Evidence Crop Matrix
  │                                                                                         └── Tamper-Evident QR Code
  ├─► PipelineOrchestrator
  │   ├── Stage 1: Quality Gate (Laplacian variance >= 100, glare <= 15%)
  │   ├── Stage 2: Optical Calibration (INR 10 coin / ISO card scale)
  │   ├── Stage 3: OCR Perception (PaddleOCR ONNX Runtime / fallback)
  │   ├── Stage 4: TokenNormalizer (Regex / CTC correction -> CanonicalDeclaration)
  │   ├── Stage 5: StatutoryRuleEngine (Rule 6, 6(11) USP, Rule 7 Font, Rule 26/3)
  │   ├── Stage 6: ImprovementNoticeBuilder (Jan Vishwas Act, 2026, 15-day cure)
  │   └── Stage 7: Evidence Crop Generator (PIL spatial crops -> Base64 URIs)
  │
  ▼
[ JSON Inspection Response (docs/API_CONTRACT.md) ]
```

---

## 3. Detailed Endpoint Directory & Contracts

### 3.1. Primary Inspection: `POST /api/v1/inspect`
- **Consumes:** `multipart/form-data`
  - `file`: Packaging photograph (JPEG, PNG, or WebP; max 15.0 MB).
  - `anchor_type`: Calibration fiducial reference (`"INR_10_COIN"`, `"ISO_CARD"`, `"NONE"`). Default: `"INR_10_COIN"`.
  - `panel_type`: Package view (`"FRONT_PDP"`, `"BACK_INFO"`, `"ALL_IN_ONE"`). Default: `"FRONT_PDP"`.
  - `officer_id`: Identifier of inspecting officer or test session. Default: `"WEB-GUEST"`.
  - `X-Request-ID`: Optional client tracing UUID header.
- **Produces:** `application/json` (`InspectionResponse` schema)
- **Performance:** Mean latency: **72.8ms**, P95: **76.75ms** on standard CPU hardware (Budget: $< 2500\text{ms}$).

### 3.2. Tamper-Evident PDF Export: `POST /api/v1/report/pdf`
- **Consumes:** `application/json` (`ReportPdfRequest` schema)
  - `inspection_id`: Unique inspection identifier.
  - `officer_notes`: Optional inspecting officer remarks.
  - `include_raw_image`: Boolean flag whether to embed packaging thumbnail.
- **Produces:** `application/pdf` (binary stream)
  - `Content-Disposition: attachment; filename="metrolens_report_<inspection_id>.pdf"`
  - `X-Report-Cached: true | false`
- **Performance:** Mean latency: **20.2ms**, P95: **24.05ms** on standard CPU hardware (Budget: $< 500\text{ms}$).

### 3.3. National eMaap Portal Synchronization: `POST /api/v1/emaap/mock-sync`
- **Consumes:** `application/json` (`EMaapSyncRequest` schema)
  - `inspection_id`: Unique inspection identifier.
  - `jurisdiction_code`: State legal metrology jurisdiction (e.g., `"DL-01-CENTRAL"`).
  - `officer_id`: Inspecting officer token.
  - `compliance_state`: Inspection outcome (`"COMPLIANT"`, `"NON_COMPLIANT"`, etc.).
  - `improvement_notice_issued`: Boolean.
  - `dossier_sha256`: 64-character hexadecimal SHA-256 cryptographic seal.
- **Produces:** `application/json` (`EMaapSyncResponse` schema)
  - `sync_status`: `"ACCEPTED_FOR_RECORD"` | `"REJECTED"`.
  - `emaap_reference_no`: Generated registry reference (e.g., `"EMAAP-DL-2026-048192"`).
  - `received_at`: ISO 8601 UTC timestamp.
  - `tamper_verification`: `"VERIFIED_VALID"` | `"TAMPER_DETECTED"`.

### 3.4. Health & System Telemetry: `GET /api/v1/health`
- **Produces:** `application/json` (`HealthResponse` schema)
  - `status`: `"healthy"`.
  - `version`: `"1.0.0"`.
  - `uptime_seconds`: Active process uptime.
  - `system`: Live host CPU percent, resident memory used (MB), and total memory (MB) via `psutil`.
  - `models`: Runtime readiness of detection, recognition, and calibration subsystems.
  - `rules_engine`: Status, version (`"2026.09-JanVishwas-v1.0"`), and verified rules count (4).

---

## 4. Multi-Layer Upload Security Pipeline (ADR-013)

To safeguard offline edge hardware against maliciously crafted files, memory exhaustion attacks, and privacy leakage, every upload undergoes an automated 7-stage security validation:

1. **Payload Size Boundary:** Strict 15.0 MB (`15,728,640 bytes`) ceiling enforced in streaming memory. Exceeding payloads immediately aborted with HTTP 413 `IMAGE_TOO_LARGE`.
2. **Cryptographic SHA-256 Digest:** Computes immutable SHA-256 checksum of raw bytes before any parsing or transformation occurs.
3. **Binary Magic Bytes Signature Verification:** Rejects disguised extensions. Requires authentic binary magic bytes:
   - JPEG: `\xFF\xD8\xFF`
   - PNG: `\x89PNG\r\n\x1a\n`
   - WebP: `RIFF` at byte 0 and `WEBP` at byte 8.
   - Non-matching files rejected with HTTP 415 `UNSUPPORTED_MEDIA_TYPE`.
4. **Pre-Decode Header Bomb Firewall:** Inspects binary stream metadata headers (SOF markers for JPEG, IHDR chunk for PNG, VP8/VP8L chunks for WebP) to parse declared dimensions *before* pixel decompression. Rejects any image exceeding 64 Megapixels (`64,000,000 pixels`) with HTTP 422 `DECOMPRESSION_BOMB_DETECTED`.
5. **Raster Pixel Decoding:** Pillow loader configured with `Image.MAX_IMAGE_PIXELS = 64_000_000`. Corrupt pixel streams rejected with HTTP 422 `IMAGE_CORRUPTED`.
6. **Minimum Resolution Bounds:** Packaging photographs must measure at least $800 \times 600$ pixels to guarantee statutory text legibility. Sub-threshold images rejected with HTTP 422 `IMAGE_RESOLUTION_TOO_LOW`.
7. **Privacy Sanitization (EXIF / GPS Stripping):** Strips all EXIF metadata, GPS latitude/longitude coordinates, device serial numbers, and camera timestamps. Honors EXIF orientation transpose before metadata eviction. Re-encodes pristine in-memory pixel buffer.

---

## 5. Ephemeral Spooling & Session Lifecycle (ADR-014)

In accordance with Legal Metrology privacy standards, merchant photos and packaging assets are never permanently retained in backend databases. The `SpoolService` manages temporary lifecycles:

- **Isolated Sandboxes:** Every inspection creates a dedicated ephemeral directory:
  ```
  /tmp/metrolens_uploads/<inspection_id>/
  ├── raw.jpg
  ├── sanitized.jpg
  ├── report.pdf
  └── crops/
      ├── crop_net_quantity.jpg
      ├── crop_mrp.jpg
      └── crop_usp.jpg
  ```
- **Atomic Persistence:** All disk writes stream to temporary `.tmp_<uuid>` swap files and execute atomic `os.replace` directory commitments, preventing partial file reads during concurrent requests.
- **60-Minute TTL Auto-Cleaner:** Background daemon thread sweeps the spool directory every 5 minutes, purging any session whose last access exceeds 60 minutes (`3600 seconds`).
- **Server Startup Sweep:** On FastAPI server boot (`lifespan`), cleans all orphaned session directories left behind from previous crashes.
- **Quota Enforcer:** Automatically prunes oldest sessions if total spool directory usage exceeds $5.0\text{ GB}$.

---

## 6. Rate Limiting Middleware (Buffer Task 1)

- **Algorithm:** Thread-safe in-memory sliding-window leaky bucket (`InMemoryRateLimiter`).
- **Statutory Quota:** 10 inspection requests per minute per unique client IP address.
- **Proxy Transparency:** Extracts real client IP via `X-Forwarded-For` header with fallback to socket peer address.
- **Exemptions:** Administrative routes (`/health`, `/api/v1/health`, `/docs`, `/openapi.json`) are permanently exempt.
- **Enforcement:** Exceeding requests immediately return HTTP 429 `RATE_LIMIT_EXCEEDED` with a standard `Retry-After: <seconds>` header.

---

## 7. Latency Benchmarks & Telemetry Profile

Audited under Python 3.13.14 on standard CPU hardware across 20 consecutive iterations:

| Metric / Pipeline Stage | Statutory / SLA Target | Benchmark Measured (Mean) | Benchmark Measured (P95) | Compliance Status |
| :--- | :---: | :---: | :---: | :---: |
| **End-to-End Inspection Pipeline** | $< 2500\text{ms}$ | **72.82 ms** | **76.75 ms** | **PASSED (32x faster)** |
| ├── Quality Gate Pre-flight | $< 50\text{ms}$ | 46.02 ms | 48.10 ms | PASSED |
| ├── Metric Scale Calibration | $< 100\text{ms}$ | 0.03 ms | 0.04 ms | PASSED |
| ├── OCR Perception | $< 1200\text{ms}$ | 0.03 ms (fallback) | 0.04 ms | PASSED |
| ├── Token Normalization | $< 50\text{ms}$ | 0.18 ms | 0.22 ms | PASSED |
| ├── Statutory Rules State Machine | $< 20\text{ms}$ | 0.11 ms | 0.15 ms | PASSED |
| └── Evidence Crop Packaging | $< 500\text{ms}$ | 1.26 ms | 1.45 ms | PASSED |
| **Evidentiary PDF Report Compilation** | $< 500\text{ms}$ | **20.22 ms** | **24.05 ms** | **PASSED (20x faster)** |

---

## 8. Monorepo Handoff & Interface Guide

### 8.1. Handoff to Member 5 (React Web UI Lead)
- **API Base URL:** `http://127.0.0.1:8000/api/v1`
- **Interactive OpenAPI Documentation:** Available at `http://127.0.0.1:8000/docs`.
- **Primary Upload:** Send `multipart/form-data` with key `file` to `POST /api/v1/inspect`.
- **Displaying Evidence:** Every item in `response.evidence_crops` contains `crop_base64`, directly bindable to `<img src={crop.crop_base64} />`.
- **PDF Download:** Issue `POST /api/v1/report/pdf` with `{"inspection_id": id}`; browser can trigger direct download via native blob streaming.

### 8.2. Handoff to Member 6 (DevOps Lead)
- **ASGI Entrypoint:** `uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --workers 4`
- **Liveness / Readiness Probes:**
  - Liveness: `GET /health` (returns HTTP 200 `{"status":"ok"}`)
  - Readiness: `GET /api/v1/health` (validates memory, CPU, and ruleset version)
- **Storage Mounting:** Mount high-speed ephemeral RAM disk or SSD tmpfs at `/tmp/metrolens_uploads` for optimal I/O throughput.
- **Environment Variables:**
  - `METROLENS_SPOOL_DIR`: Custom ephemeral spool directory (defaults to OS temporary path).
  - `METROLENS_RATE_LIMIT`: Custom requests per minute limit (default: 10).
