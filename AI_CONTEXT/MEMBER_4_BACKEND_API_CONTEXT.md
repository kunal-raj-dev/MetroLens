# AI AGENT CONTEXT: MEMBER 4 — BACKEND API GATEWAY, UPLOAD SECURITY & EVIDENTIARY REPORTING
**Project:** MetroLens AI (SIH26034)  
**Lead:** Member 4 — Backend API Gateway, Web Upload Security & Evidentiary Reporting Lead  
**Primary Applications & Packages:** `apps/api/`, `packages/reporting/`  
**Secondary Role:** Pipeline Integration & System Orchestration  
**Document Classification:** AI Agent Context & Knowledge System  
**Last Updated:** 2026-09-05T15:58:00+05:30  

---

## 1. Executive Mission & Identity
Member 4 is personally responsible for delivering an unshakeable, high-performance, and secure FastAPI application gateway and a court-admissible evidentiary reporting infrastructure.
The gateway acts as the central conductor for MetroLens AI, orchestrating the synchronous inspection pipeline (`POST /api/v1/inspect`) within an end-to-end latency budget of $< 2.5\text{s}$ on standard CPU hardware.

### Non-Negotiable Architectural Invariants:
1. **Multi-Layered Ingestion Security (ADR-013):**
   - Strict payload size cap: Reject uploads $> 15.0\text{MB}$ with `HTTP 413 Payload Too Large` (`IMAGE_TOO_LARGE`).
   - In-memory magic byte inspection: Verify the leading 16 bytes for valid JPEG (`\xFF\xD8\xFF`), PNG (`\x89PNG\r\n\x1a\n`), or WebP (`RIFF...WEBP`) signatures; reject disguised or polyglot files with `HTTP 415 Unsupported Media Type` (`UNSUPPORTED_MEDIA_TYPE`).
   - Decompression bomb guard: Enforce Pillow `Image.MAX_IMAGE_PIXELS = 64_000_000` (~64 Megapixels); reject oversized pixel expansions with `HTTP 422 Unprocessable Entity` (`DECOMPRESSION_BOMB_DETECTED`).
   - Dimension boundaries: Minimum resolution $800 \times 600$ pixels; auto-downsample excessively large images ($> 3000\text{px}$) to conserve CPU OCR cycles.
   - Privacy sanitization: Strip all EXIF metadata (GPS, camera serial, author information) from uploaded images.
2. **Ephemeral Storage Lifecycle (ADR-014):**
   - In-memory processing via `io.BytesIO` whenever possible.
   - Spooling to isolated temporary directory (`/tmp/metrolens_uploads/<uuid>/`) only when native disk access is required.
   - Automated 60-minute Time-to-Live (TTL) purge daemon and server startup sweep. Zero permanent database retention of merchant photos.
3. **Synchronous Sub-2.5s Execution (ADR-012):**
   - Synchronous HTTP request/response model (`POST /api/v1/inspect`) completing within $< 2.5\text{s}$ end-to-end latency budget:
     $$\text{Security (<50ms)} \longrightarrow \text{Quality/Calib (<300ms)} \longrightarrow \text{OCR (<800ms)} \longrightarrow \text{Rules (<20ms)} \longrightarrow \text{JSON (<50ms)}$$
4. **Court-Admissible Tamper-Evident Reporting (ADR-007, ADR-010):**
   - Generate official "MetroLens AI — Image-Based Compliance Assessment Report" PDF using ReportLab in $< 500\text{ms}$.
   - Embed cryptographic SHA-256 hash of raw input image and visual crops.
   - Embed Section 36(1) Jan Vishwas Act 2026 statutory Improvement Notice (15-day cure window, zero criminal terminology).
   - Embed standardized disclaimer: *"Automated image-based assessment. Final legal determination remains with the authorized officer."*
5. **eMaap National Portal Mock Integration (ADR-008):**
   - Provide `POST /api/v1/emaap/mock-sync` simulating national legal metrology portal synchronization with HMAC verification and reference tracking.

---

## 2. Interface Seams & Monorepo Contracts

### 2.1 Upstream from Member 1 (OCR Perception Engine):
- Package: `packages/ocr/` (`nirikshak_ocr`)
- Outputs: List of `OCRToken` / `OCRObservation` instances:
```python
class OCRToken(BaseModel):
    token_id: str
    text: str
    confidence: float
    bbox: List[float]  # [xmin, ymin, xmax, ymax]
    polygon: Optional[List[List[float]]]
    char_height_px: Optional[float]
```

### 2.2 Upstream from Member 2 (CV / Metric Calibration):
- Packages: `packages/vision/`, `packages/calibration/` (`nirikshak_vision`, `nirikshak_calibration`)
- Pre-flight Quality: Blur detection (Laplacian variance), Glare mask percentage.
- Metric Scale: `MetricScaleResult`:
```python
class MetricScaleResult(BaseModel):
    is_calibrated: bool
    scale_factor_mm_per_px: Optional[float]
    pdp_area_sqcm: Optional[float]
    anchor_type_detected: Optional[str]  # 'coin_10rs', 'iso_card', 'none'
    tilt_angle_deg: Optional[float]
    is_cylindrical: bool
```

### 2.3 Upstream from Member 3 (Legal Rules & Compliance Engine):
- Package: `packages/rules-engine/` (`nirikshak_rules_engine`)
- Modules Utilized:
  - `TokenNormalizer`: Parses raw `OCRToken` list into `CanonicalDeclaration`.
  - `StatutoryRuleEngine`: Evaluates `CanonicalDeclaration` and `MetricScaleResult` across Rules 3, 6, 7, 11, 26, GSR 881(E).
  - `ImprovementNoticeBuilder`: Generates Section 36(1) Jan Vishwas Improvement Notice payload and text.
  - `FOPNLValidator`: Evaluates FSSAI nutritional display standards.
  - `PenaltyCalculator`: Evaluates repeat offender multi-year compounding ladders under Section 36(1) and Section 48/48A.
- Output: `ComplianceEvaluationResult`.

### 2.4 Downstream to Member 5 (React Web Frontend):
- Protocol: HTTP/REST (OpenAPI 3.1)
- Endpoints:
  - `POST /api/v1/inspect`: Multipart upload $\rightarrow$ JSON inspection dossier matching `docs/API_CONTRACT.md`.
  - `GET /api/v1/health`: Readiness probe with system memory, CPU, and rules engine version.
  - `POST /api/v1/report/pdf`: PDF binary download with `Content-Disposition: attachment`.
  - `POST /api/v1/emaap/mock-sync`: e-Governance sync mock webhook.

### 2.5 Downstream to Member 6 (DevOps & Deployment):
- Process: Uvicorn ASGI server running on `http://127.0.0.1:8000`.
- Health Probes: `GET /api/v1/health` for Kubernetes / Docker container liveness.

---

## 3. Package Architecture & Layout

```
apps/api/
├── main.py                          # FastAPI app entrypoint, CORS, lifespan management, routes
├── pyproject.toml                   # API package configuration & dependencies
├── errors.py                        # Canonical error taxonomy & exception handlers
├── schemas.py                       # Pydantic v2 schemas conforming to docs/API_CONTRACT.md
├── middleware/
│   ├── __init__.py
│   ├── security.py                  # Ingestion security gate (magic bytes, bomb caps, EXIF sanitization)
│   ├── headers.py                   # Production security headers (CSP, HSTS, X-Frame-Options)
│   └── rate_limit.py                # In-memory leaky bucket IP rate limiter (10 req/min)
├── routes/
│   ├── __init__.py
│   ├── inspect.py                   # POST /api/v1/inspect primary orchestration endpoint
│   ├── report.py                    # POST /api/v1/report/pdf report generation & download
│   ├── emaap.py                     # POST /api/v1/emaap/mock-sync eMaap portal mock webhook
│   └── health.py                    # GET /api/v1/health readiness and system metrics
└── services/
    ├── __init__.py
    ├── spool_service.py             # Ephemeral buffer & temporary directory manager (60-min TTL)
    └── pipeline_orchestrator.py     # Central conductor coordinating M1, M2, M3 modules

packages/reporting/
├── pyproject.toml                   # Reporting package configuration
└── src/nirikshak_reporting/
    ├── __init__.py                  # Exports DossierGenerator, PDFReportCompiler
    └── pdf_compiler.py              # ReportLab tamper-evident assessment report compiler
```

---

## 4. Standardized Error Contract & Taxonomy

All error responses strictly adhere to the uniform JSON error envelope defined in `docs/API_CONTRACT.md` Section 4:
```json
{
  "error": {
    "code": "IMAGE_TOO_LARGE",
    "message": "The uploaded packaging image exceeds the 15.0 MB file size limit.",
    "details": {
      "file_size_bytes": 18450120,
      "max_allowed_bytes": 15728640
    },
    "remediation": "Please resize or compress your image and try again.",
    "timestamp": "2026-09-05T01:15:31.005Z"
  }
}
```

| HTTP Status | Error Code (`code`) | Trigger Condition | Recommended User Remediation |
| :--- | :--- | :--- | :--- |
| `400` | `INVALID_IMAGE_PAYLOAD` | Missing file stream or corrupted multipart form data. | Select a valid image file. |
| `413` | `IMAGE_TOO_LARGE` | Upload exceeds 15.0 MB size limit. | Compress or downsample image under 15MB. |
| `415` | `UNSUPPORTED_MEDIA_TYPE` | Magic bytes do not match JPEG, PNG, or WebP. | Upload a genuine JPEG, PNG, or WebP photo. |
| `422` | `DECOMPRESSION_BOMB_DETECTED` | Image exceeds 64 Megapixels (`MAX_IMAGE_PIXELS`). | Upload a standard camera resolution image. |
| `422` | `IMAGE_CORRUPTED` | PIL or OpenCV decoder fails to parse raster pixels. | Re-take photograph or export from graphics tool. |
| `422` | `IMAGE_RESOLUTION_TOO_LOW` | Image resolution is below $800 \times 600$ pixels. | Capture at higher resolution to allow text reading. |
| `429` | `RATE_LIMIT_EXCEEDED` | Client IP exceeded 10 inspection requests per minute. | Please wait 60 seconds before submitting again. |
| `500` | `PIPELINE_EXECUTION_ERROR` | Internal Python runtime exception during processing. | Contact technical team with inspection ID. |
| `504` | `PROCESSING_TIMEOUT` | CPU inference exceeded 5.0-second watchdog limit. | Upload a sharper, single-panel crop. |

---

## 5. Scope Boundaries ("Not My Job")
- **Not Member 4:** Training OCR models, tuning PaddleOCR weights, or adjusting det/rec thresholds (Member 1).
- **Not Member 4:** Implementing contour detection, ellipse fitting, or homography unwarping (Member 2).
- **Not Member 4:** Writing statutory rules, USP math formulas, or legal regex extractors (Member 3).
- **Not Member 4:** Building React frontend components, canvas viewports, or Tailwind styles (Member 5).
- **Not Member 4:** Procuring physical benchmark packaging or measuring ground-truth fonts (Member 6).

---

## 6. Execution Tracking & Chunk History

### Chunk 1: Upload Security Middleware & Ingestion Gate (VERIFIED)
- **Modules Created:**
  - `apps/api/errors.py`: Canonical error taxonomy (HTTP 400, 413, 415, 422, 429, 500, 504) and custom FastAPI exception handlers.
  - `apps/api/middleware/security.py`: 7-stage security validation (magic bytes, streaming SOF/IHDR headers, 64MP pre-decode bomb firewall, EXIF/GPS stripping, minimum resolution bounds).
  - `apps/api/middleware/headers.py`: Production security headers (CSP, HSTS, X-Content-Type-Options, X-Frame-Options).
  - `apps/api/middleware/__init__.py`: Unified middleware package exports.
- **Verification Suite:**
  - `tests/integration/test_security_middleware.py`: 15 passed in 0.60s.
  - Verified: authentic JPEG/PNG/WebP, polyglot rejections, 15MB file cap, 64MP bomb defense, EXIF GPS sanitization, security headers, canonical error JSON envelopes.

### Chunk 2: Ephemeral Spooling Service & Session Lifecycle Management (VERIFIED)
- **Modules Created:**
  - `apps/api/services/spool_service.py`: Thread-safe `SpoolService`, `SpoolSession`, atomic writes with `os.replace`, 60-min TTL background daemon, startup sweep, quota enforcement.
  - `apps/api/services/__init__.py`: Unified services package exports.
- **Verification Suite:**
  - `tests/unit/test_spool_service.py`: 9 unit tests passed in 6.9s.
  - Verified: directory isolation (`/tmp/metrolens_uploads/<uuid>/`), atomic persistence for raw/sanitized/crops/PDF, 60-min TTL expiration, startup sweep, explicit purge, quota prunes, background cleaner daemon lifecycle.

### Chunk 3: ReportLab Evidentiary PDF Assessment Report Compiler (VERIFIED)
- **Modules Created:**
  - `packages/reporting/src/nirikshak_reporting/pdf_compiler.py`: Court-admissible ReportLab PDF assessment compiler with `NumberedCanvas` (two-pass "Page X of Y", security running headers and footers, micro-print borders), SHA-256 raw image cryptographic seal, Section 36(1) Jan Vishwas Improvement Notice box (15-day cure window), visual forensic evidence crops, embedded tamper-evident verification QR code, uncompressed stream (`pageCompression=0`), `< 500ms` generation speed.
  - `packages/reporting/src/nirikshak_reporting/__init__.py`: Package exports and backward-compatible `DossierGenerator`.
  - `packages/reporting/pdf_compiler.py`: Top-level re-export shim.
- **Verification Suite:**
  - `tests/integration/test_pdf_generation.py`: 6 tests passed in 0.53s.
  - Verified: binary structure (`%PDF-` to `%%EOF`), sub-500ms execution latency, SHA-256 seal presence, Section 36(1) notice rendering, currency symbol sanitization (`₹` to `Rs.`), and legacy `DossierGenerator` integration.

### Chunk 4: Pipeline Orchestrator & Synchronous Inspection Endpoint (VERIFIED)
- **Modules Created:**
  - `apps/api/schemas.py`: Authoritative API v1.0 contracts (`InspectionResponse`, `ImageMetadata`, `CalibrationInfo`, `DeclarationsInfo`, `RuleEvaluationsGroup`, `ImprovementNoticeInfo`, `EvidenceCrop`, `TelemetryInfo`, `HealthResponse`, `ReportPdfRequest`, `EMaapSyncRequest`, `EMaapSyncResponse`).
  - `apps/api/services/pipeline_orchestrator.py`: Central conductor orchestrating Ingestion Security $\rightarrow$ Ephemeral Spooling $\rightarrow$ Quality Gate Pre-flight $\rightarrow$ Optical Metric Scale Calibration $\rightarrow$ Multilingual OCR (with offline fallback) $\rightarrow$ Token Normalization $\rightarrow$ Master Statutory Rules Evaluation $\rightarrow$ Jan Vishwas Improvement Notice $\rightarrow$ Visual Evidence Crops Packaging.
  - `apps/api/routes/inspect.py`: `POST /api/v1/inspect` multipart upload endpoint.
  - `apps/api/main.py`: Updated with router integration, lifespan startup sweep and cleaner daemon management, security headers, and error handlers.
- **Verification Suite:**
  - `tests/integration/test_inspect_endpoint.py`: 10 passed in 1.35s.
  - Verified: compliant FMCG roundtrip, non-compliant packaging with Section 36(1) notice, bilingual Hindi attributions, non-standard units, uncalibrated mode, client tracing UUID header, and security rejections (HTTP 400, 413, 415, 422).

### Chunk 5: Mock eMaap REST Adapter & PDF Export Route (VERIFIED)
- **Modules Created:**
  - `apps/api/routes/report.py`: `POST /api/v1/report/pdf` streaming PDF assessment report with attachment header and spool caching.
  - `apps/api/routes/emaap.py`: `POST /api/v1/emaap/mock-sync` simulating national eMaap legal metrology webhook synchronization and tamper verification.
  - `apps/api/routes/health.py`: `GET /api/v1/health` comprehensive readiness and health probe with system telemetry and rules engine metadata.
  - `apps/api/routes/__init__.py`: Router bundle export.
- **Verification Suite:**
  - `tests/integration/test_emaap_report.py`: 6 passed in 0.90s.
  - Verified: PDF stream validity, sub-500ms compilation latency, ephemeral spool caching, eMaap registry reference code assignments, tamper detection on non-hex SHA-256 hashes, and live CPU/memory telemetry.

### Chunk 6: Leaky-Bucket Rate Limiter & Security Hardening (VERIFIED)
- **Modules Created:**
  - `apps/api/middleware/rate_limit.py`: In-memory thread-safe sliding-window rate limiter enforcing 10 requests per minute with automatic stale bucket sweeps, proxy forward header resolution, and HTTP 429 `RATE_LIMIT_EXCEEDED` with `Retry-After` header.
  - `apps/api/middleware/__init__.py`: Exporting `RateLimitMiddleware`, `InMemoryRateLimiter`, and `rate_limiter`.
  - `apps/api/main.py`: Active production middleware integration.
- **Verification Suite:**
  - `tests/integration/test_rate_limit.py`: 5 passed in 0.55s.
  - Verified: sliding-window burst limits, multi-IP quota isolation, stale bucket eviction, 429 error envelope with Retry-After header, and route exemptions (/health, /docs).

### Chunk 7: Comprehensive Integration, Fuzzing & Latency Benchmarks (VERIFIED)
- **Modules Created:**
  - `tests/integration/test_api_integration.py`: End-to-end 100-request stability stress test, adversarial input fuzzing (polyglot files, truncated streams, giant headers, SQL/Unicode injection filenames), cold-start lifespan warm-up verification. 8 tests passing in 5.85s.
  - `benchmarks/api_latency_benchmark.py`: Latency breakdown benchmark script auditing $< 2.5\text{s}$ CPU pipeline budget and $< 500\text{ms}$ PDF compilation.
  - `benchmarks/results/latency_benchmark_report.json`: Persisted benchmark metric telemetry.
- **Benchmark Results:**
  - Pipeline Latency: Mean 72.82ms, P50 72.74ms, P95 76.75ms, P99 77.91ms (Budget $< 2500\text{ms}$).
  - PDF Compilation: Mean 20.22ms, P50 19.38ms, P95 24.05ms, P99 28.82ms (Budget $< 500\text{ms}$).

### Chunk 8: Final Code Freeze, Documentation & Monorepo Handoff (VERIFIED)
- **Modules Created:**
  - `apps/api/main.py`: Fully assembled FastAPI application with lifecycle daemon management, CORS, CSP/HSTS headers, sliding-window rate limiter, and all route blueprints.
  - `docs/04_ARCHITECTURE/API_GATEWAY.md`: Comprehensive architectural documentation covering data flows, security firewalls, ephemeral lifecycle, and API contracts.
- **Verification Suite Status:** 180 passed / 180 total tests (100% green).
