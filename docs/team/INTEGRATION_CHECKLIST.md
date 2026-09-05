# CROSS-WORKSTREAM INTEGRATION CHECKLIST
# MetroLens AI™ (SIH26034)
### Evaluation: Smart India Hackathon 2026 | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Operational Cross-Workstream Handshake Specification | **Version:** 1.0.0

---

## 1. Primary Cross-Workstream Handoffs

```
   ┌─────────────────────────────────────────────────────────────┐
   │                    INTEGRATION TOPOLOGY                     │
   └─────────────────────────────────────────────────────────────┘
      M2 (Vision / Scale) ───► M1 (OCR Engine)
               │                      │
               ▼                      ▼
      M2 (Metric Dimensions)  M1 (OCR Tokens)
               │                      │
               └──────────┬───────────┘
                          ▼
               M3 (Canonical Normalizer & Rules)
                          │
                          ▼
               M4 (FastAPI Gateway & PDF Dossier)
                          │
               ┌──────────┴──────────┐
               ▼                     ▼
        M5 (React Web UI)     M6 (Docker / Benchmark)
```

---

## 2. Handoff Matrix & Protocol Checklists

### HANDOFF 1: Member 2 (CV/Calib) ──► Member 1 (OCR)
- **Artifact:** Orthorectified, perspective-corrected packaging crop (`numpy.ndarray`).
- **Interface:** In-memory array or temporary file path.
- **Contract Schema:**
  ```python
  rectified_crop: np.ndarray  # Dimensions: H x W x 3 (BGR uint8)
  scale_factor_s: float       # mm / pixel
  is_calibrated: bool         # True if ₹10 coin or ISO card detected
  ```
- **Environment Requirements:** OpenCV 4.x (`opencv-python-headless`).
- **Test Evidence:** `pytest tests/unit/test_calibration.py` passes with scale error $< 5.0\%$.
- **Known Limitations:** If surface tilt $> 15^\circ$, unwarping may have edge shearing; fallback to unrectified crop.
- **Rollback / Fallback:** Pass raw image array directly to Member 1; set `is_calibrated = False`.

---

### HANDOFF 2: Member 1 (OCR) ──► Member 3 (Rule Engine)
- **Artifact:** Standardized list of extracted character tokens with coordinates and confidences.
- **Interface:** Python object list or JSON stream.
- **Contract Schema (`OCRToken`):**
  ```python
  class OCRToken(BaseModel):
      token_id: str              # Unique token identifier (e.g. 'tok_001')
      text: str                  # Transcribed character sequence
      confidence: float          # 0.0 to 1.0 (CTC / decoder confidence)
      polygon: List[List[float]] # Clockwise 4-point quad [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] in original image pixels
      bbox: List[float]          # Derived axis-aligned bbox: [xmin, ymin, xmax, ymax]
      script: ScriptType         # 'latin' | 'devanagari' | 'unknown'
      line_id: int               # Reading order line index
      raw_pixel_height: Optional[float] = None  # Raw pixel geometry only; NOT legal font height (owned by Member 2)
      model_name: str = ""
  ```
- **Environment Requirements:** ONNX Runtime (`onnxruntime`), PaddleOCR quantized weights.
- **Test Evidence:** `pytest tests/unit/test_ocr_engine.py` passes; Character Error Rate $< 6.0\%$.
- **Known Limitations:** Dot-matrix dates and curved text near can rims have degraded confidence ($< 0.60$).
- **Rollback / Fallback:** Member 3 tests against `tests/fixtures/mock_ocr_tokens.json`.

---

### HANDOFF 3: Member 2 (Calibration) ──► Member 3 (Rule Engine)
- **Artifact:** Metric dimensions and measured numeral stroke heights in millimeters.
- **Interface:** Python object matching `MetricScaleResult`.
- **Contract Schema (`MetricScaleResult`):**
  ```python
  class MetricScaleResult(BaseModel):
      is_calibrated: bool
      scale_factor_mm_per_px: Optional[float]
      pdp_area_sqcm: Optional[float]
      anchor_type_detected: Optional[str]  # 'coin_10rs' | 'iso_card' | 'none'
      tilt_angle_deg: Optional[float]
      is_cylindrical: bool
  ```
- **Environment Requirements:** None (pure data model).
- **Test Evidence:** Scale factor matches RBI coin diameter ($27.0\text{mm}$) within $\pm 5\%$.
- **Known Limitations:** Non-planar bottles flag `is_cylindrical: true` and restrict measurement to central vertical generator.
- **Rollback / Fallback:** If coin is missing, `is_calibrated = False`; Member 3 evaluates text compliance and flags font heights as `NOT_IMAGE_VERIFIABLE`.

---

### HANDOFF 4: Member 3 (Rule Engine) ──► Member 4 (Backend API)
- **Artifact:** Statutory compliance evaluation verdict, parsed entities, and Section 36(1) notice payload.
- **Interface:** Pydantic object serializable to JSON.
- **Contract Schema (`ComplianceEvaluationResult`):**
  ```python
  class ComplianceEvaluationResult(BaseModel):
      inspection_id: str
      timestamp_utc: str
      overall_verdict: str       # 'COMPLIANT' | 'NON_COMPLIANCE' | 'MANUAL_REVIEW' | 'EXEMPTED'
      verdict_badge_color: str   # 'green' | 'red' | 'amber' | 'blue' | 'gray'
      primary_legal_summary: str
      rule_evaluations: List[RuleEvaluationRecord]
      declarations: CanonicalDeclaration
      calibrated_measurements: MetricScaleResult
      evidence_crops: List[EvidenceCropMetadata]
      sha256_hash: str
      pdf_report_url: str
  ```
- **Environment Requirements:** Pydantic v2.
- **Test Evidence:** `pytest tests/rules/` passes all 25 statutory test cases.
- **Known Limitations:** Address physical existence cannot be checked optically; net weight requires physical scale.
- **Rollback / Fallback:** Member 4 mocks endpoint with canned 5-State JSON fixtures.

---

### HANDOFF 5: Member 4 (Backend API) ──► Member 5 (Web UI)
- **Artifact:** REST API endpoints (`POST /api/v1/inspect`, `POST /api/v1/report/pdf`, `GET /health`).
- **Interface:** HTTP/JSON over `http://127.0.0.1:8000`.
- **Contract Schema:** Conforms 100% to OpenAPI 3.1 specification in `docs/API_CONTRACT.md`.
- **Environment Requirements:** FastAPI running on port 8000 with CORS configured for `http://localhost:5173`.
- **Test Evidence:** `pytest tests/integration/test_api_integration.py` passes 100%.
- **Known Limitations:** Ephemeral spool purged after 60 minutes; PDF requests after TTL return 404.
- **Rollback / Fallback:** Member 5 toggles UI into `MOCK_MODE=true` to render canned responses.

---

### HANDOFF 6: Member 4 & M3 ──► Member 6 (Evidentiary PDF & Release)
- **Artifact:** Tamper-evident PDF assessment report compiler and CLI entrypoints.
- **Interface:** `packages/reporting/pdf_compiler.py` and `apps/cli/inspect_cli.py`.
- **Contract Schema:** Generates PDF binary embedding SHA-256 digests and Section 36(1) notices.
- **Environment Requirements:** ReportLab 4.x, DejaVu Sans font assets.
- **Test Evidence:** PDF compiles in $< 500\text{ms}$; opens without corruption in Adobe Acrobat and Chrome.
- **Known Limitations:** PDF compilation requires image crops to be spooled in temporary directory.
- **Rollback / Fallback:** Fall back to static pre-compiled sample PDF reports.

---

## 3. Integration Verification Script

Before any PR is merged into `main`, run the project integration verification script:

```bash
# Verify entire pipeline locally
python -m pytest tests/unit/
python -m pytest tests/rules/
python -m pytest tests/integration/
python scripts/verification/verify_claims.py
python scripts/verification/verify_legal_sources.py
```
