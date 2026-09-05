# INDIVIDUAL WORK PLAN: MEMBER 4
# Backend API Gateway, Upload Security & PDF Reporting Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Packages:** `apps/api/`, `packages/reporting/` | **Secondary Role:** System Integration & Orchestration

---

## 1. Member Role
**Member 4 — Backend API Gateway, Web Upload Security & Evidentiary Reporting Lead**

---

## 2. Mission
Deliver a rock-solid, high-performance FastAPI application gateway and a court-admissible evidentiary reporting infrastructure. Member 4 is personally responsible for orchestrating the synchronous inspection pipeline (`POST /api/v1/inspect`) within an end-to-end latency budget of $< 2.5\text{s}$, enforcing multi-layered upload defense-in-depth (magic-byte validation, 64MP decompression bomb caps, EXIF sanitization), managing the ephemeral storage lifecycle (in-memory processing with 60-minute TTL spooling), compiling tamper-evident PDF assessment reports embedding cryptographic SHA-256 digests and Section 36(1) Improvement Notices in $< 500\text{ms}$, and providing a mock eMaap REST synchronization adapter.

---

## 3. Ownership

### Primary Ownership:
- `apps/api/main.py`: FastAPI application entrypoint, CORS configuration, and lifespan management.
- `apps/api/routes/inspect.py`: Main `POST /api/v1/inspect` synchronous orchestration endpoint.
- `apps/api/routes/report.py`: `POST /api/v1/report/pdf` report generation and download endpoint.
- `apps/api/routes/emaap.py`: `POST /api/v1/emaap/mock-sync` National Portal mock adapter.
- `apps/api/middleware/security.py`: Ingestion security gate (magic-byte checks, Pillow decompression bomb defense, EXIF stripping).
- `apps/api/services/spool_service.py`: Ephemeral buffer and temporary spool directory manager with automated 60-minute TTL cleanup.
- `packages/reporting/pdf_compiler.py`: ReportLab PDF assessment report compiler with SHA-256 seal.
- `tests/integration/test_api_integration.py`: Complete API integration test suite.

### Secondary Support:
- Support **Member 5 (Frontend Lead)** by hosting the local API server and troubleshooting CORS / multipart upload payloads.
- Support **Member 6 (DevOps Lead)** with environment variables and health check probes for containerization.

---

## 4. Concrete Responsibilities
1. Scaffold and implement the FastAPI application gateway conforming 100% to `docs/API_CONTRACT.md`.
2. Implement layered upload security middleware (ADR-013):
   - Check file payload size; reject requests $> 15.0\text{MB}$ with `HTTP 413 Payload Too Large`.
   - Inspect leading 16 magic bytes in memory; verify valid JPEG (`\xFF\xD8\xFF`), PNG (`\x89PNG`), or WebP (`RIFF...WEBP`) signatures; reject disguised extensions with `HTTP 415 Unsupported Media Type`.
   - Protect against decompression bombs: enforce `PIL.Image.MAX_IMAGE_PIXELS = 64_000_000` (64 Megapixels); reject excessive dimensions with `HTTP 422 Unprocessable Entity`.
   - Strip all GPS, device serial, and author EXIF metadata to protect user privacy.
3. Manage ephemeral storage lifecycle (ADR-014):
   - Stream incoming bytes into memory (`io.BytesIO`); spool to `/tmp/metrolens_uploads/<uuid>/` strictly when native OpenCV/PDF generation requires disk files.
   - Enforce 60-minute Time-to-Live (TTL) auto-purge daemon for spooled artifacts.
4. Orchestrate the synchronous pipeline sequence:
   $$\text{Ingestion Security} \longrightarrow \text{Quality Filter (M2)} \longrightarrow \text{Metric Calibration (M2)} \longrightarrow \text{PaddleOCR (M1)} \longrightarrow \text{Normalizer (M3)} \longrightarrow \text{Rule Engine (M3)}$$
   Guarantee that total execution completes within $< 2.5\text{ seconds}$ on standard CPU hardware.
5. Implement `packages/reporting/pdf_compiler.py` using ReportLab:
   - Compile official "Image-Based Compliance Assessment Report".
   - Embed side-by-side visual evidence crops with bounding boxes.
   - Embed cryptographic integrity block: raw image SHA-256 hash, UTC timestamp, GPS coordinates (if provided), and model commit SHA.
   - Embed draft Section 36(1) Improvement Notice citing 15-day cure window.
6. Implement `POST /api/v1/emaap/mock-sync` simulating national registry synchronization.

---

## 5. What Member 4 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Running OCR neural models or writing character tokenizers (owned strictly by Member 1).
- **NOT MY JOB:** Implementing contour detection, ellipse fitting, or homography unwarping (owned strictly by Member 2).
- **NOT MY JOB:** Writing statutory rules, USP math formulas, or legal regex extractors (owned strictly by Member 3).
- **NOT MY JOB:** Building React frontend components, canvas viewports, or Tailwind styles (owned strictly by Member 5).
- **NOT MY JOB:** Procuring physical benchmark packaging or measuring ground-truth fonts (owned strictly by Member 6).

---

## 6. Inputs Received
- **From Member 1 (OCR):** `OCRToken` token lists from `packages/ocr/`.
- **From Member 2 (CV/Calib):** `MetricScaleResult` and pre-flight quality checks from `packages/calibration/` and `packages/vision/`.
- **From Member 3 (Rules):** `ComplianceEvaluationResult` and Section 36(1) notice payloads from `packages/rules-engine/`.
- **Specification:** `docs/API_CONTRACT.md` and `docs/TECHNICAL_DECISIONS.md` (ADR-011 through ADR-014).

---

## 7. Concrete Outputs Delivered
- `apps/api/`: Fully functional, secure FastAPI application gateway.
- `POST /api/v1/inspect`, `POST /api/v1/report/pdf`, `POST /api/v1/emaap/mock-sync`, `GET /api/v1/health`.
- `packages/reporting/pdf_compiler.py`: Tamper-evident PDF generation module.
- Ephemeral spooling service with automatic 60-minute TTL cleanup.
- `tests/integration/test_api_integration.py`: End-to-end integration test suite.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **Pydantic Schemas** | Member 3 | Request and response schema definitions | Day 1, 12:00 PM | Use frozen schemas from `docs/API_CONTRACT.md`. |
| **PaddleOCR Engine** | Member 1 | Text extraction service integration | Day 3, 2:00 PM | Use mock OCR service returning canned tokens from `tests/fixtures/`. |
| **Calibration Module** | Member 2 | Scale recovery and quality filter service | Day 3, 2:00 PM | Use mock calibration service returning $S=0.045\text{mm/px}$. |
| **Rule Engine** | Member 3 | Statutory compliance evaluation service | Day 3, 4:00 PM | Use mock rule engine returning canned 5-State JSON verdict. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: Risk Spike — FastAPI Scaffold & Upload Ingestion Security
- **Goal:** Stand up FastAPI server and prove layered upload security defenses.
- **Tasks:** Initialize `apps/api/`; implement CORS and health check routes; author `middleware/security.py` with magic-byte validator and Pillow decompression bomb defense; test with valid and malicious files.
- **Deliverables:** Working FastAPI gateway rejecting non-image payloads and zip bombs.
- **Expected Time:** 7 hours.
- **Dependencies:** None (self-contained).
- **Checkpoint (Gate 1 - T+24h):** Server boots on `http://127.0.0.1:8000/api/v1/health`; upload security tests pass 100%.
- **Risk:** Magic-byte inspection rejects valid modern WebP images.
- **Fallback:** Allow `RIFF....WEBP` header variations; verify with Python `puremagic`.

### DAY 2: Ephemeral Spool Manager & Headless Vertical Slice 0 Runner
- **Goal:** Build ephemeral file lifecycle manager and assemble headless CLI pipeline.
- **Tasks:** Implement `spool_service.py` (`/tmp/metrolens_uploads/<uuid>/`); write `apps/cli/inspect_cli.py` integrating M1 OCR, M2 Calibration, and M3 Normalizer into Vertical Slice 0; test end-to-end in terminal.
- **Deliverables:** Working Vertical Slice 0 CLI runner executing the full pipeline.
- **Expected Time:** 7 hours.
- **Dependencies:** Prototype modules from M1, M2, M3.
- **Checkpoint (Gate 2 - T+48h):** Vertical Slice 0 executes via CLI in $< 2.5\text{s}$ on a sample packaging photo.
- **Risk:** File permission errors on Windows temporary directory.
- **Fallback:** Use Python `tempfile.TemporaryDirectory` with cross-platform path abstraction (`pathlib.Path`).

### DAY 3: ReportLab PDF Assessment Report Scaffold & Cryptographic Seal
- **Goal:** Scaffold court-admissible PDF generator embedding SHA-256 digests.
- **Tasks:** Set up ReportLab; design PDF layout: header, metadata block, side-by-side evidence crops, legal citations, and Section 36(1) notice draft; compute SHA-256 hashes of input image and crops; render sample PDF in $< 500\text{ms}$.
- **Deliverables:** `packages/reporting/pdf_compiler.py` generating valid PDF.
- **Expected Time:** 6 hours.
- **Dependencies:** Mock compliance JSON from Member 3.
- **Checkpoint (Gate 3 - Day 3):** PDF compiles in $< 500\text{ms}$ with zero layout clipping.
- **Risk:** Missing system fonts cause ReportLab crash on special currency glyphs (`₹`).
- **Fallback:** Bundle open-source DejaVu Sans TTF directly in repository assets (`assets/fonts/`).

### DAY 4: Pipeline Orchestration & Live API Endpoint Integration
- **Goal:** Wire `POST /api/v1/inspect` to live pipeline and connect with Member 5's React UI.
- **Tasks:** Wire `apps/api/routes/inspect.py` to live M1 OCR, M2 Calibration, and M3 Rule Engine; implement comprehensive error taxonomy (HTTP 400, 413, 415, 422, 500); support Member 5 with live frontend integration.
- **Deliverables:** End-to-end operational `POST /api/v1/inspect` endpoint.
- **Expected Time:** 7 hours.
- **Dependencies:** Operational modules from M1, M2, M3, M5.
- **Checkpoint (Gate 4 - Day 4):** React upload dropzone triggers FastAPI, executes pipeline, and receives valid JSON.
- **Risk:** Pipeline latency exceeds $2.5\text{s}$ under full integration.
- **Fallback:** Profile individual stages; optimize image resizing in pre-flight.

### DAY 5: PDF Export Endpoint & Mock eMaap REST Adapter
- **Goal:** Expose PDF download route and eMaap synchronization webhook.
- **Tasks:** Implement `apps/api/routes/report.py` (`POST /api/v1/report/pdf`); stream PDF binary to client; implement `apps/api/routes/emaap.py` (`POST /api/v1/emaap/mock-sync`); simulate national portal sync with status badges.
- **Deliverables:** Working PDF download endpoint and mock eMaap adapter.
- **Expected Time:** 6 hours.
- **Dependencies:** PDF compiler from Day 3.
- **Checkpoint (Gate 5 - Day 5):** Clicking "Download Report" in browser immediately downloads court-admissible PDF.
- **Risk:** PDF generation times out if images are re-processed from scratch.
- **Fallback:** Cache pre-generated crop images in the 60-minute ephemeral spool during inspection.

### DAY 6: End-to-End API Integration & Security Fuzz Testing
- **Goal:** Guarantee API reliability under concurrent calls and adversarial inputs.
- **Tasks:** Write comprehensive pytest suite in `tests/integration/test_api_integration.py`; test corrupted uploads, huge files, missing form fields, rapid consecutive calls; verify ephemeral spool auto-cleanup daemon.
- **Deliverables:** Robust API integration test suite passing 100%.
- **Expected Time:** 6 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 6):** 100 consecutive requests execute with zero server crashes or file leaks.
- **Risk:** Spool directory fills disk with orphaned files on aborted uploads.
- **Fallback:** Add server startup sweep clearing all temporary directories; run TTL cleaner every 10 minutes.

### DAY 7: Performance Profiling, Sub-2.5s Latency Tuning & Hardening
- **Goal:** Guarantee synchronous sub-2.5s execution budget across all benchmark SKUs.
- **Tasks:** Benchmark wall-clock execution breakdown: Ingestion ($<50\text{ms}$) $\rightarrow$ Quality/Calib ($<300\text{ms}$) $\rightarrow$ OCR ($<800\text{ms}$) $\rightarrow$ Rules ($<20\text{ms}$) $\rightarrow$ JSON ($<50\text{ms}$); tune Uvicorn worker threads.
- **Deliverables:** Latency audit report in `benchmarks/results/api_latency.json`.
- **Expected Time:** 5 hours.
- **Dependencies:** Benchmark dataset from Member 6.
- **Checkpoint (Gate 7):** P95 latency $< 2.2\text{ seconds}$ on demonstrator laptop.
- **Risk:** Cold-start latency on first request exceeds $3.5\text{s}$.
- **Fallback:** Implement application lifespan warm-up routine: run dummy $100\times100$ image through OCR on server boot.

### DAY 8: Code Freeze & Operational Runbook Preparation
- **Goal:** Lock all backend code; write deployment and execution runbooks.
- **Tasks:** Freeze `apps/api/` and `packages/reporting/`; verify non-root user execution with Member 6; author API documentation in `docs/04_ARCHITECTURE/`; rehearse live demo failover Layer 1.
- **Deliverables:** Frozen code, passing CI, and deployment runbook.
- **Expected Time:** 4 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Zero open backend PRs; clean boot in $< 5\text{s}$.

### DAY 9: Buffer Day & Live Demonstration Support
- **Goal:** Support live stage demonstration.
- **Tasks:** Monitor local Uvicorn process during presentation; verify network independence (Wi-Fi off); assist with technical architecture Q&A during jury evaluation.
- **Expected Time:** As needed.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | FastAPI & Uvicorn installed | `uvicorn --version` succeeds | Fix virtualenv / dependencies |
| **CP-1** | T+24h | Security middleware operational | Rejects zip bomb; passes clean JPEG | Review Pillow security settings |
| **CP-2** | T+48h | Vertical Slice 0 CLI works | Terminal command outputs valid JSON in $<2.5\text{s}$ | Debug individual pipeline stages |
| **CP-3** | Day 3 | ReportLab PDF layout complete | Renders PDF with SHA-256 hash in $<500\text{ms}$ | Embed DejaVu fallback font |
| **CP-4** | Day 5 | Full Web API integrated | Browser upload triggers API and renders cards | Debug CORS / multipart parser |
| **CP-5** | Day 7 | Latency budget verified | P95 latency $< 2.5\text{s}$ across 35 benchmark runs | Add server lifespan warm-up |
| **CP-6** | Day 8 | Final code freeze | All integration tests green; zero leaked temp files | Revert unverified changes |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **Upload Security** | Rejects non-images (415) and $>15\text{MB}$ payloads (413) | `pytest tests/integration/test_security.py` | Test report showing HTTP 413/415 rejections |
| **Decompression Guard**| Rejects images $>64\text{MP}$ without crashing Uvicorn | `pytest tests/integration/test_security.py` | Test report showing HTTP 422 on bomb image |
| **Inspection Route** | `POST /inspect` returns valid compliance JSON in $<2.5\text{s}$ | `pytest tests/integration/test_api.py` | Latency benchmark log showing P95 $< 2.5\text{s}$ |
| **PDF Report** | `POST /report/pdf` compiles tamper-evident PDF in $<500\text{ms}$| `pytest tests/integration/test_pdf.py` | Generated PDF file validated with `pdfinfo` |
| **Mock eMaap** | `POST /emaap/mock-sync` returns 200 OK with sync ID | `pytest tests/integration/test_emaap.py` | Unit test assertions verifying mock sync payload |

---

## 12. Testing Responsibility
- **Integration Tests:** `tests/integration/test_api_integration.py` (complete HTTP lifecycle from upload to response).
- **Security Tests:** `tests/integration/test_security_middleware.py` (magic bytes, decompression bombs, EXIF stripping).
- **PDF Verification Tests:** `tests/integration/test_pdf_generation.py` (PDF structure, SHA-256 hash presence, font rendering).
- **Failure Cases:** Uploading corrupted binary bytes, disconnecting client mid-upload, requesting expired PDF after TTL window.

---

## 13. Handoff Protocol & Checklist

### Handoff to Member 5 (Web UI) & Member 6 (DevOps):
1. **Running Service:** FastAPI backend running on `http://127.0.0.1:8000`.
2. **API Specification:** Interactive Swagger UI live at `http://127.0.0.1:8000/docs`.
3. **Usage Documentation:**
   ```bash
   # Start API server locally
   uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. **Test Evidence:** Attached pytest log showing 100% pass on all API integration tests.
5. **Known Limitations:** Ephemeral spooled files purged after 60 minutes; PDF requests after TTL return `HTTP 404 EXPIRED_SESSION`.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** CORS or multipart upload errors blocking frontend $\rightarrow$ Pair with Member 5 immediately.
- **Blocked for 2 hours:** ReportLab crashing on font glyphs or PDF rendering $\rightarrow$ Fall back to pre-built HTML-to-PDF template or standard Helvetica.
- **Blocked for half-day:** Synchronous pipeline latency exceeding $3.5\text{s}$ $\rightarrow$ Escalate to Lead Architect to profile and downsample input resolution.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Pipeline Latency $> 2.5\text{s}$** | Med | High | Benchmark latency log | Downsample images $>2000\text{px}$ during pre-flight | Increase client timeout to 10s |
| **Decompression Bomb Crash** | Low | High | Server OOM crash | Pillow `MAX_IMAGE_PIXELS = 64_000_000` cap | Hard process memory ceiling |
| **ReportLab Font Rendering Crash** | Med | Med | UnicodeEncodeError on `₹` | Bundle DejaVu Sans TTF in repository assets | Render currency as "INR" or "Rs." |
| **Disk Exhaustion from Spool** | Low | High | `/tmp` disk space $>90\%$ | Automated 60-min TTL cleaner + startup sweep | Process in-memory (`io.BytesIO`) |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 4 DAILY STATUS (DATE: ________)
• DONE: [Endpoints created and integration tests passing]
• BLOCKED: [Any gateway or security blockers > 30 mins]
• TESTED: [API latency numbers / security test results]
• NEXT: [Tomorrow's backend milestone]
• RISK: [Any performance or memory concerns]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. Python code is written with complete type annotations in `apps/api/` and `packages/reporting/`.
2. All REST endpoints pass automated integration tests with 100% pass rate.
3. Synchronous pipeline executes in $< 2.5\text{s}$ on demo hardware.
4. Tamper-evident PDF compiles in $< 500\text{ms}$ with valid SHA-256 hash.
5. Handshake is verified with Member 5 (Web UI) and Member 6 (DevOps).

---

## 18. AI Coding Workflow
$$\text{PLAN (Review API Contract)} \longrightarrow \text{PROMPT AI (FastAPI Routes)} \longrightarrow \text{REVIEW (Security \& Error Codes)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Write boilerplate FastAPI route controllers, Pydantic field validators, and ReportLab canvas styling.
- **MEMBER MUST DECIDE:** Security thresholds, TTL lifecycle rules, pipeline execution order, and error status code mappings.

---

## 19. Buffer Work
- **Primary:** FastAPI gateway, security middleware, ephemeral spool manager, PDF generator, mock eMaap.
- **Buffer Task 1:** Implement IP rate limiting using an in-memory leaky bucket algorithm (10 req/min).
- **Buffer Task 2:** Build standalone health dashboard showing CPU usage and warm-start model status.
