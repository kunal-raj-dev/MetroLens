# SYSTEM ARCHITECTURE SPECIFICATION — ARCHITECTURE BASELINE V1.0
# MetroLens AI™ — Web Application Architecture & Processing Pipeline
### Document Status: Authoritative System Architecture Reference | Target Platform: Online Web Application
**Authoritative Standards:** RFC 2119 | **Runtime Environment:** Python 3.14+ (FastAPI) | Node.js v25+ (React/Vite)

> **IMPLEMENTATION STATUS — READ FIRST**
> This document is a **specification for a system that is not yet implemented** (repository status: `PRE_IMPLEMENTATION`, per `docs/14_SUBMISSION/` claims governance and `data/manifests/manifest.yaml`).
> Every quantitative value in this document is classified as one of: **DESIGN DECISION** (an accepted engineering constraint), **MVP TARGET** (intended, not yet measured), or **INITIAL HEURISTIC** (starting threshold pending calibration — see `research/research_gaps/RESEARCH_GAPS_REGISTER.md`, GAP-VISION-02).
> No end-to-end latency, accuracy, or throughput figure has been measured yet: `benchmarks/results/` is empty and `apps/`, `packages/` contain scaffolding only. The canonical metrics classification table lives in `docs/ARCHITECTURE_BASELINE_V1_0_REVIEW_REPORT.md`.

---

## 1. Executive Architectural Summary

MetroLens AI is specified as a **containerized web application** backed by a REST API and a **modular inspection pipeline**.

The system replaces the superseded edge-native, local-only concept with an **online web-first platform**. Users interact with MetroLens AI via any standard modern desktop or mobile browser. Packaging images are transmitted over secure HTTP, validated against strict binary standards, and evaluated across a 6-stage processing engine that is designed to execute entirely on server CPU without calling external cloud AI APIs.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  CORE ARCHITECTURE PRINCIPLES                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. No External Cloud AI APIs: All OCR and computer-vision neural networks   │
│    are specified to execute on server CPU using quantized ONNX runtimes.    │
│    Generative LLMs are excluded from statutory adjudication, eliminating    │
│    a class of generative-model hallucination risks in the rule-decision     │
│    layer. (OCR/CV themselves remain probabilistic perception components.)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Clean Boundary Separation: Clear modular layers between Web Transport,   │
│    Image Perception, Mathematical Calibration, Legal State Machine, and     │
│    Evidentiary Packaging. Statutory logic is NEVER mixed into HTTP routes.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Ephemeral Ingestion: Uploads are validated via magic-bytes, processed    │
│    in isolated temporary storage, and purged post-inspection (lifecycle in  │
│    §4). No untrusted image is retained beyond the documented TTL.           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Synchronous Sub-2.5s Budget: The pipeline is DESIGNED to complete within │
│    an MVP TARGET of < 2.5 s end-to-end on the defined demo hardware.        │
│    This is a target, not a measured result; see ADR-012.                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. High-Level Web System Architecture

```text
                                  METROLENS AI WEB TOPOLOGY

       CLIENT TIER (Web Browser)
       ┌────────────────────────────────────────────────────────────────────────┐
       │ Responsive React + Vite Web Application (apps/web)                     │
       │ • Modern Upload Dropzone (Drag & Drop, File Picker, Mobile Camera)     │
       │ • Client-Side Format & Size Validation (< 15MB, JPEG/PNG/WebP)         │
       │ • Interactive 5-State Compliance Cards & Side-by-Side Crop Viewer      │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │ HTTPS / REST (multipart/form-data)
                                           ▼
       API TRANSPORT TIER (FastAPI Gateway)
       ┌────────────────────────────────────────────────────────────────────────┐
       │ FastAPI Application Gateway (apps/api - Port 8000)                     │
       │ • Reverse Proxy / TLS Termination (Nginx / Cloudflare)                 │
       │ • CORS Policy, Rate Limiting (IP Leaky Bucket), Payload Caps (15MB)    │
       │ • Request ID & Telemetry Injector                                      │
       │ • Endpoints: POST /api/v1/inspect, GET /api/v1/health, POST /pdf      │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │ Internal Orchestration
                                           ▼
       PROCESSING PIPELINE TIER (Pure Python Modular Core)
       ┌────────────────────────────────────────────────────────────────────────┐
       │ Stage 1: Ingestion & Security Gate (magic bytes, decompression bomb)  │
       │ Stage 2: Optical Metric Calibration (OpenCV coin/card scale S mm/px)   │
       │ Stage 3: Multilingual Scene Text OCR (PaddleOCR v4 Mobile ONNX int8)  │
       │ Stage 4: Canonical Entity Normalizer (Regex token parser + Pydantic)   │
       │ Stage 5: Deterministic Statutory Rule Engine (Rules 6, 6(11), 7, 26)  │
       │ Stage 6: Evidentiary Dossier Builder (SHA-256 seal & PDF compiler)     │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
                                           ▼
       PERSISTENCE & EXPORT TIER
       ┌────────────────────────────────────────────────────────────────────────┐
       │ • Ephemeral Buffer Store (/tmp/metrolens_uploads/<uuid>/, 60-min TTL) │
       │ • Tamper-Evident SHA-256 Compliance Dossier (JSON Response)            │
       │ • Downloadable Official Assessment Report (PDF with Sec 36(1) notice) │
       │ • Mock eMaap Sync Adapter (NIC e-Governance interoperability)          │
       └────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Synchronous vs. Asynchronous Processing Architecture

A pivotal architectural decision for the Web MVP is whether image inspection should be executed **synchronously** (request holds connection until result returns) or **asynchronously** (upload returns a job ID; client polls or listens to WebSockets).

### Architectural Evaluation Matrix

All latency figures below are **estimates and targets, not measurements** — no benchmark has been executed yet (`benchmarks/results/` empty).

| Criterion | Synchronous Pipeline (`POST /inspect` $\rightarrow$ Result) | Asynchronous Pipeline (Job Queue + Polling/WebSocket) |
| :--- | :--- | :--- |
| **End-to-End Latency** | **Target < 2.5 s** (single request-response round trip). | Higher: queue polling delay + handshakes. |
| **Infrastructure Overhead** | **Minimal.** Single FastAPI process + Uvicorn workers. | **High.** Requires Redis broker, Celery/ARQ workers, and state DB. |
| **Operational Complexity** | **Low.** Zero distributed race conditions or zombie tasks. | **High.** Task retry policies, dead-letter queues, WebSocket reconnects. |
| **Hackathon & Demo Risk**| **Low.** No container failure between broker and workers. | **Moderate to High.** Redis container crash kills demonstration. |
| **Scalability Under Concurrency** | Bounded by worker pool (expected adequate for demo/single-team load; TBD by measurement). | Scales to hundreds of concurrent jobs across worker nodes. |

### The Authoritative MVP Decision: Synchronous First (ADR-012)
- **Decision:** The MetroLens AI MVP adopts a **Synchronous Execution Model**.
- **Rationale (honest form):** No pipeline measurement exists yet. Synchronous processing is justified by **workload and simplicity, not by achieved latency**: the expected MVP workload is a single-user or small-audience demo with one image per request; the internal processing *budget* is < 2.5 s; standard HTTP client timeouts (typically 30–60 s) comfortably accommodate a response in that budget even with margin. Adding Celery, Redis, and WebSocket state machines before a single vertical slice exists would add failure surface without user benefit.
- **Measurement condition:** The first end-to-end benchmark of Vertical Slice 0 (see `docs/IMPLEMENTATION_PLAN.md`) must record actual stage timings. If the measured p95 exceeds the budget, the pipeline must be optimized or the target revised before any move to async.
- **When synchronous becomes inadequate** (triggers to revisit, NOT to build now):
  - multi-image inspection sessions (front/back/sides aggregation);
  - sustained concurrency beyond a small demo audience;
  - measured processing consistently exceeding several seconds;
  - larger models or batch catalog scanning;
  - long-running report generation.
- **Evolution path:** The canonical data contract (`CanonicalInspectionContract`) is decoupled from the transport layer. A background queue (`FastAPI.BackgroundTasks`, later Celery/ARQ + Redis if justified) can wrap the same handler without changing the frontend response schema. **No queue infrastructure is to be built during the MVP.**

---

## 4. Web Image Ingestion & Upload Architecture

Image upload is the primary user interaction in the web application. Untrusted file uploads from public clients represent a critical security and reliability surface.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       WEB IMAGE INGESTION PIPELINE                          │
└─────────────────────────────────────────────────────────────────────────────┘
  1. File Received via HTTP POST (multipart/form-data)
         │
         ▼
  2. Request Size Validation (Reject payloads > 15.0 MB with HTTP 413)
         │
         ▼
  3. Header & Magic-Byte Inspection (Inspect first 16 bytes in memory)
         │  ├── JPEG:  FF D8 FF
         │  ├── PNG:   89 50 4E 47 0D 0A 1A 0A
         │  └── WebP:  52 49 46 46 (RIFF) ... 57 45 42 50 (WEBP)
         │  └── ELSE:  Raise HTTP 415 (UNSUPPORTED_MEDIA_TYPE)
         ▼
  4. Decompression Bomb Protection (Pillow MAX_IMAGE_PIXELS = 64,000,000)
         │  └── If pixel count > 64MP: Raise HTTP 422 (IMAGE_TOO_LARGE)
         ▼
  5. Dimension Check & Optical Pre-Check
         │  ├── Minimum: 800 x 600 pixels (Reject unreadable low-res)
         │  └── Downsample: If max dimension > 3000px, resize to 2560px for CPU OCR
         ▼
  6. EXIF & Metadata Sanitization
         │  └── Strip GPS, camera serial, author metadata (Privacy protection)
         ▼
  7. Cryptographic Identity Assignment
            ├── Assign UUID4: inspection_id = "INSP-20260905-XXXX"
            ├── Compute raw payload SHA-256 checksum
            └── Yield sanitized in-memory PIL / NumPy image array to pipeline
```

### Temporary Storage & Ephemeral Retention Policy (ADR-014)
- **Memory-First Processing:** Small to medium images ($< 8\text{MB}$) are processed directly in RAM (`io.BytesIO`) without touching the physical server disk.
- **Ephemeral Disk Spooling:** When temporary files are required for native OpenCV/PDF generation, they are spooled into `/tmp/metrolens_uploads/<inspection_id>/` with restricted POSIX permissions (`0700`).
- **Full Retention Lifecycle (normative):**
  1. *Upload begins:* the request body is streamed (never buffered whole) under the 15 MB cap; bytes land in memory or the spool directory only.
  2. *Buffering:* nothing is written outside `/tmp/metrolens_uploads/<uuid>/`; client filenames are discarded (server-generated UUID names only).
  3. *Processing:* the pipeline reads from the buffer; EXIF is stripped before any model sees the image.
  4. *Post-response cleanup:* image buffers are freed immediately after the HTTP response is serialized; the spool directory for the inspection is deleted (success path).
  5. *PDF generation:* if the user requests a report, it is compiled from the still-cached artifacts (or the request fails with a clear expiry error if the TTL window has passed); the PDF is itself subject to the same TTL.
  6. *Retention period:* artifacts (crops, PDFs) survive at most **60 minutes** (TTL) strictly to support report download.
  7. *Cleanup mechanism & failure handling:* a TTL purger sweeps the spool root; a startup sweep clears orphans from crashed runs. Cleanup failure must raise an operational alert — silent retention is a defect.
  8. *Persistence:* **no permanent database storage of uploaded images** in the MVP. (The `docker-compose.yml` Postgres service in the current repository scaffold predates this policy and must be reconciled/removed by M6 before deployment — tracked in the Baseline v1.0 report risk register.)
- **Logs vs. image content:** application logs record identifiers, stage names, timings, counts, and error categories only. Raw image bytes, base64 crops, and OCR-extracted personal fields (phone numbers, emails, names) MUST NOT be written to logs. Images cannot be reconstructed from logs.

**Privacy statement (defensible form):** Ephemeral retention reduces long-term image-storage exposure and aligns with data-minimization principles. It does not by itself constitute "zero privacy liability" or "full DPDP compliance"; a formal privacy review against the DPDP Act, 2023 remains an open item (see Baseline v1.0 report, TBD register).

---

## 5. Online Access & Exposure Model (ADR-015)

**Decision — who can use the MetroLens MVP:**

| Option | MVP Posture |
| :--- | :--- |
| A. Anonymous public users | **Selected for MVP (demo posture)** |
| B. Authenticated users | Rejected for MVP (see below) — Future |
| C. Restricted institutional users | Future |
| D. Internal/private deployment | Fallback posture for demo reliability |
| E. Demo-only public deployment | **Selected for MVP** |

- **MVP decision:** the MVP ships as an **anonymous, demo-oriented public deployment**: anyone with the URL may submit images for inspection. This maximizes jury/self-serve evaluation and removes authentication from the critical path.
- **Authentication:** NOT built in the MVP (explicitly a DO-NOT-BUILD item). Post-MVP authentication model is **TBD**; when introduced it must not retroactively change the API contract's core inspection schema.
- **Authorization:** none in MVP; all callers have identical capability. Officer-vs-public distinctions are out of scope.
- **Anonymous API access:** allowed, with the controls below; the API must assume every caller is untrusted.
- **Rate limiting (design decision):** per-IP leaky bucket, **10 inspection requests/minute** (canonical value; tunable), returning `429 RATE_LIMIT_EXCEEDED`.
- **Abuse prevention & quotas:** 15 MB payload cap, 64 MP decode cap, 5.0 s per-request processing watchdog, concurrent-request cap per IP (TBD value, set at deployment).
- **CORS / origin restrictions:** in demo deployments the API allows only the configured frontend origin; wildcard `*` origins are prohibited in any deployed environment.
- **Auditability:** request ID + inspection ID + timestamps + failure category are logged for every request (no image content — see §4). Anonymous access means user-level audit trails are not available in the MVP; this is an accepted limitation, documented for judges.
- **Brute-force surface:** none (no credentials exist in the MVP); re-evaluated when authentication is added.

---

## 6. End-to-End Processing Pipeline Contract

The processing pipeline guarantees the strict separation of concerns mandated by the Four Pillars. Module paths use the repository's canonical package layout (`apps/`, `packages/`):

```text
RAW IMAGE BYTES
      │
      ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: INGESTION & QUALITY GATE (M2 / M6)                            │
│ • Module: packages/vision/quality.py                                   │
│ • Tests: Laplacian variance for blur; HSV V/S channels for glare.      │
│ • Exit criteria: Rejects unusable frames early (target < 50ms).        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Validated Frame
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: METRIC SCALE CALIBRATION (M2)                                 │
│ • Modules: packages/calibration/anchor_detector.py & homography.py     │
│ • Algorithm: ₹10 coin ellipse fitting (27.0mm) or ISO card homography. │
│ • Output: Scale Factor S (mm/pixel) + Unwarped orthorectified image.   │
│ • Fallback: If coin absent, set S = null; flag font as NOT_VERIFIABLE. │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ S (mm/px) + Rectified Image
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: MULTILINGUAL SCENE TEXT OCR (M1)                              │
│ • Module: packages/ocr/engine.py                                       │
│ • Engine: PaddleOCR v4 Mobile ONNX int8 (DBNet++ text det, SVTR rec).  │
│ • Output: List of { text: str, bbox: [x,y,w,h], confidence: float }.   │
│ • Sub-task: Calibrated numeral stroke measurement (h_mm = h_px * S).   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Raw Text Tokens + Measured Heights
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: CANONICAL ENTITY NORMALIZER (M3)                              │
│ • Module: packages/rules-engine/normalizer.py                          │
│ • Algorithm: Deterministic regex token extractors & unit normalizers.  │
│ • Output: CanonicalDeclaration (Pydantic schema).                      │
│ • Strictly parses MRP, Net Quantity, Mfg Date, Address, USP.           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ CanonicalDeclaration JSON
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 5: STATUTORY RULE ENGINE (M3) — deterministic by scope           │
│ • Module: packages/rules-engine/rule_engine.py                         │
│ • Rule 26: Statutory Exemption Switch (Net Qty <= 10g/ml, > 25kg).     │
│ • Rule 6(1)(a)-(h): Mandatory 8-declaration completeness verifier.     │
│ • Rule 6(11): Unit Sale Price arithmetic auditor (Expected = MRP / Qty)│
│ • Rule 7 Table-I/II: Area-to-font height matrix conformance checker.   │
│ • Output: 5-State Adjudication Verdict + draft Improvement Notice data.│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ ComplianceEvaluationResult
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 6: EVIDENTIARY DOSSIER & REPORT BUILDER (M6)                     │
│ • Module: packages/reporting/pdf_generator.py                          │
│ • Computes SHA-256 digests over raw capture, crops, and audit JSON.    │
│ • Generates draft Compliance Assessment Report PDF for human review.   │
│ • Prepares optional payload for eMaap mock sync adapter.               │
└────────────────────────────────────────────────────────────────────────┘
```

**Scope of the determinism claim (normative):** Stages 1–3 are perception/measurement components whose outputs may vary with image quality and lighting. The correct system-wide statement is: **given a defined set of normalized observations, the legal rule engine (Stages 4–5) produces deterministic and reproducible outcomes.** Documents must not describe the *entire system* as deterministic, and must not use "zero hallucination risk" as a blanket guarantee — the precise statement is that generative LLMs are excluded from statutory adjudication, eliminating a class of generative-model hallucination risks in the rule-decision layer.

**Where things happen (quick map):** data enters at the upload boundary (trust boundary #1: browser → API); validation occurs at Stages 1–2; legal decisions occur only at Stage 5; uncertainty is surfaced everywhere as explicit states (Amber/Gray), never silently discarded; persistence occurs ONLY in the ephemeral spool (§4); user interaction occurs in the browser before upload and after the response.

---

## 7. Comprehensive Web Security Threat Model

Deploying an image-processing service to the public web introduces distinct attack surfaces. Every mitigation below **reduces** risk; none makes the system "immune". Residual risk is stated explicitly. (These are specified controls — implementation and verification live in `tests/security/`, Tier 3 of the testing strategy.)

| # | Threat | Mitigation (specified control) | Residual Risk |
| :-- | :--- | :--- | :--- |
| 1 | **Decompression / pixel bomb** (small file → huge raster) | Pillow `MAX_IMAGE_PIXELS = 64_000_000` (~64MP); pre-decode header dimension check; reject with HTTP 422 | New decoder-level bypasses in image libraries; keep dependencies patched |
| 2 | **Malformed / truncated images** | Decode wrapped in strict try/except; uniform `IMAGE_CORRUPTED` 422 error; no stack traces to client | Fuzzing may reveal crash paths — Tier 3 fuzz suite required |
| 3 | **Executable polyglot / MIME spoofing** | Magic-byte whitelist (first 16 bytes: JPEG/PNG/WebP); reject with 415; decode strictly in RAM; never execute or shell out on uploads | Exotic polyglots passing magic-byte check but failing decode are rejected downstream; parser bugs remain a dependency risk |
| 4 | **Path traversal** (`../../etc`) | Client filenames discarded entirely; server-generated `uuid4().hex` names only; spool confined to `/tmp/metrolens_uploads/` | Low, if no library reintroduces client-controlled paths (audit at review) |
| 5 | **Denial of service — flood / large uploads** | 15 MB streaming cap (413); per-IP leaky-bucket rate limit 10 req/min (429); per-IP concurrency cap (TBD) | Distributed (multi-IP) floods not mitigated by per-IP limits; acceptable for demo posture, needs WAF/CDN if scaled |
| 6 | **CPU starvation via expensive OCR requests** | 5.0 s per-request processing watchdog (504); request queuing bounded by worker pool | Sustained adversarial load can still degrade service; monitor + alert required |
| 7 | **Excessive storage consumption** | Ephemeral spool only; 60-min TTL purger; startup orphan sweep; no persistent image store | A burst within the TTL window can fill `/tmp`; disk-space alerting required |
| 8 | **EXIF / metadata leakage** | Strip all EXIF (GPS, device, author) before processing; logs never contain image bytes or extracted personal fields | Metadata may transit memory/logs in the window before stripping — strip as the FIRST decode step |
| 9 | **Report / inspection exposure** | Inspection IDs are unguessable UUIDs; no public listing endpoint; reports expire with the TTL; no authentication in MVP (accepted limitation, ADR-015) | Anyone holding an inspection ID within the TTL can fetch its report — accepted for demo; must change before any real deployment |
| 10 | **Log leakage** | Structured logs limited to IDs, stage names, timings, counts, error categories | Misconfigured log shipping could violate this — verify at deployment review |
| 11 | **Secrets exposure** | Secrets via environment variables only; never in code, images, or client bundles; `.env` excluded from VCS | Leaked deployment secrets remain an operational risk; rotation procedure TBD (M6) |
| 12 | **Dependency vulnerabilities** | Pinned dependencies; `requirements.txt` audit at CI; minimal dependency set | Zero-day vulnerabilities in OCR/image libraries remain; patch cadence required |
| 13 | **Injection (SQL/command/XSS via OCR text)** | No SQL in the core path; Pydantic schema validation on all inputs/outputs; HTML entity escaping in UI; safe PDF canvas APIs | OCR text is untrusted input and must be escaped in every render surface (frontend, PDF) — enforced by review checklist |
| 14 | **Brute-force of credentials** | Not applicable in MVP (no authentication exists — ADR-015) | Re-open when authentication is added |

**Language rule for security claims:** documentation and demos must use *mitigates / rejects / reduces exposure / limits / detects* — never *immune / guaranteed / impossible to attack* — unless a control is objectively demonstrated by a passing security test artifact.

---

## 8. Logical Deployment Architecture (Vendor-Neutral)

The MVP is specified as a logical topology; **the cloud provider remains TBD** and must be selected at deployment time based on cost, region, and jury-accessibility. Candidate hosting options below are examples, not commitments.

```text
Browser
  ↓ HTTPS
Frontend Hosting (static SPA build of apps/web)
  ↓ HTTPS (same-origin or CORS-restricted)
Backend API (containerized FastAPI, apps/api)
  ↓ in-process
Processing Runtime (ONNX CPU inference + rule engine)
  ↓
Ephemeral Storage (/tmp/metrolens_uploads/<uuid>/, 60-min TTL)
```

### Deployment Requirements Checklist (normative for M6)
- **Compute:** container with ≥2 vCPU (target demo class: 4-core); scale quantified after Vertical Slice 0 measurement.
- **Memory:** process budget < 500 MB (models + working set); enforce via container memory limit.
- **Model startup:** ONNX weights baked into the image (no runtime downloads); cold-start initialization budget < 2 s (target).
- **Environment variables:** `METROLENS_ENV` (dev/staging/demo), `CORS_ALLOWED_ORIGINS`, `RATE_LIMIT_PER_MINUTE`, `MAX_UPLOAD_MB`, `EMAAP_MOCK_SYNC_ENABLED`; documented in `.env.example` (to be created).
- **Secrets:** none required for the anonymous MVP beyond deployment platform credentials; rotation ownership M6.
- **Health checks:** `GET /api/v1/health` used by the platform for readiness/liveness.
- **Logging & monitoring:** structured request/stage logs (§9); disk, CPU, memory, and error-rate alerting at the platform level.
- **Rollback:** image-tag-based deploys; previous tag restorable within minutes; no data migration concerns (ephemeral storage).
- **Environments:** `development` (local docker-compose), `staging` (pre-demo rehearsal), `demo` (public URL for judges). No production environment exists in the MVP.
- **Known scaffold inconsistency:** the current `docker-compose.yml` (inherited "Nirikshak" scaffold) starts a Postgres service that contradicts ADR-014; M6 must remove or justify it before the first deployment (tracked in the risk register).

To ensure operational visibility and fast troubleshooting without compromising merchant privacy:

- **Correlation Tracking:** Every incoming request receives a unique `X-Request-ID` and `inspection_id` (`INSP-YYYYMMDD-XXXX`), propagated through all logging statements.
- **Stage Execution Timing:** Pipeline logs record execution latency for each stage:
  `[INFO] [INSP-8741] stage=quality_gate duration_ms=22 status=PASS`
  `[INFO] [INSP-8741] stage=metric_calibration duration_ms=84 status=COIN_DETECTED scale=0.125`
  `[INFO] [INSP-8741] stage=paddleocr_cpu duration_ms=640 status=TOKENS_EXTRACTED count=18`
  `[INFO] [INSP-8741] stage=rule_engine duration_ms=4 status=EVALUATED verdict=POTENTIAL_NON_COMPLIANCE`
- **Privacy-Safe Logging:** Log messages record character error counts, field names, and numeric deficits—**NEVER** raw merchant phone numbers, unredacted names, or raw image payloads.
- **Health Check Endpoint (`GET /api/v1/health`):** Reports service status, CPU utilization, system RAM, and ONNX runtime availability.
