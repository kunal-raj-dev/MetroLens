# AI AGENT CONTEXT: MEMBER 3 — LEGAL RULES & COMPLIANCE ENGINE
**Project:** MetroLens AI (SIH26034)  
**Lead:** Member 3 — Legal Rules, Domain Logic & Statutory Compliance Engine Lead  
**Primary Package:** `packages/rules-engine/` (`src/nirikshak_rules_engine/`)  
**Document Classification:** AI Agent Context & Knowledge System  
**Last Updated:** 2026-09-05T14:48:00+05:30  

---

## 1. Executive Mission & Identity
Member 3 is personally responsible for delivering an unshakeable, 100% deterministic, audit-traceable statutory compliance engine for MetroLens AI.
The engine transforms raw OCR tokens and metric dimension measurements into verified statutory compliance determinations under the *Legal Metrology (Packaged Commodities) Rules, 2011* (incorporating the *Jan Vishwas (Amendment of Provisions) Act, 2026*).

### Non-Negotiable Invariants:
1. **Zero Generative Hallucination (ADR-001):** Under no circumstances may compliance verdicts, statutory citations, numeral height comparisons, or penalty calculations be derived from generative LLM calls. All decisions must be 100% deterministic, auditable, and reproducible Python code.
2. **Deterministic Execution Latency:** Complete compliance evaluation across all applicable statutory clauses must execute in $< 20\text{ms}$ on a standard CPU.
3. **5-State Compliance Taxonomy:** Every inspection must be adjudicated into the 5-State taxonomy:
   - `COMPLIANT`: Evidence demonstrates adherence to all verifiable statutory declarations.
   - `NON_COMPLIANT`: Concrete, verified violation of a statutory rule (e.g. missing mandatory field, sub-threshold numeral height, arithmetic mismatch).
   - `DEVIATION_DETECTED`: Non-standard notations or borderline conditions that warrant administrative correction.
   - `UNCERTAIN`: Image quality, uncalibrated scale, optical occlusion, or low OCR confidence prevents definitive automated verification.
   - `EXEMPTED`: Commodity or package qualifies for statutory exemption under Rule 3 or Rule 26.
4. **2026 Decriminalized Enforcement Alignment:** Aligns 100% with the *Jan Vishwas (Amendment of Provisions) Act, 2026* (effective May 1, 2026). Packaging declaration non-compliances under Section 36(1) generate a recommended 15-day **Improvement Notice**. The codebase must strictly contain **ZERO** obsolete criminal penalty or imprisonment language.

---

## 2. Statutory Legal Foundation & Gazette Register

| Statute / Gazette | Subject Matter | Engineering Codification in MetroLens |
| :--- | :--- | :--- |
| **Legal Metrology Act, 2009** (Act 1 of 2010) | Parent statute; Section 15 (inspection power), Section 36 (penalties) | Inspection metadata provenance, Section 36(1) Improvement Notice data structure. |
| **Jan Vishwas Act, 2026** (Act 18 of 2023 / 2026 Amdt) | Decriminalization of Section 36(1); introduces statutory Improvement Notice | Emits 15-day cure notice structure; strictly suppresses criminal/jail terms. |
| **LM(PC) Rules, 2011 — Rule 3** | Scope of application & wholesale exclusions | Excludes wholesale packages ($> 25\text{kg}$ or $> 25\text{L}$), except cement/fertilizers up to 50kg. |
| **LM(PC) Rules, 2011 — Rule 26** | Statutory small-package exemptions | Exempts packages $\le 10\text{g}$ or $\le 10\text{ml}$ from mandatory declarations. |
| **G.S.R. 881(E)** (Dec 2, 2025 / Feb 1, 2026) | Pan Masala & Gutkha packaging amendment | **Carve-out:** Pan masala pouches are **NEVER** exempt under Rule 26 regardless of miniature size ($\le 10\text{g}$). |
| **LM(PC) Rules, 2011 — Rule 6(1)** | Mandatory declarations on retail packages | Codifies the 8 mandatory declarations: (a) Mfr/Packer Name & Address, (aa) Country of Origin, (b) Generic Name, (c) Net Qty, (d) Mfg Date, (e) MRP, (g) Consumer Care. |
| **G.S.R. 226(E) / G.S.R. 779(E) — Rule 6(11)** | Unit Sale Price (USP) mandate | Codifies statutory denominators ($\le 1\text{kg} \rightarrow \text{₹/g}$, $> 1\text{kg} \rightarrow \text{₹/kg}$, etc.), decimal rounding to 2 places, $1.0\%$ comparison buffer. |
| **G.S.R. 629(E) / G.S.R. 1373(E) — Rule 7** | Minimum height of numerals and letters (Tables I & II) | Maps PDP area brackets ($\le 50$, $50\text{--}100$, $100\text{--}500$, $500\text{--}2500$, $> 2500\text{ cm}^2$) to minimum heights with $0.10\text{mm}$ benefit-of-doubt buffer. |

---

## 3. Interface Seams & Data Contracts

### 3.1 Upstream from Member 1 (AI / OCR Engine):
List of extracted `OCRToken` / `OCRObservation` instances:
```python
class OCRToken(BaseModel):
    token_id: int
    text: str
    confidence: float
    bbox: List[int]            # [x, y, width, height]
    char_height_px: float
    polygon: Optional[List[List[int]]] = None
```

### 3.2 Upstream from Member 2 (Computer Vision / Calibration):
Optical metric scale and PDP area computation:
```python
class MetricScaleResult(BaseModel):
    is_calibrated: bool
    scale_factor_mm_per_px: Optional[float]
    pdp_area_sqcm: Optional[float]
    anchor_type_detected: Optional[str]  # 'coin_10rs' | 'iso_card' | 'none'
    tilt_angle_deg: Optional[float]
    is_cylindrical: bool
```

### 3.3 Downstream to Member 4 (FastAPI) & Member 5 (Web UI):
Canonical evaluated compliance result:
```python
class ComplianceEvaluationResult(BaseModel):
    inspection_id: str
    timestamp_utc: str
    overall_verdict: str       # 'COMPLIANT' | 'NON_COMPLIANT' | 'DEVIATION_DETECTED' | 'UNCERTAIN' | 'EXEMPTED'
    verdict_badge_color: str   # 'green' | 'red' | 'amber' | 'blue' | 'gray'
    primary_legal_summary: str
    rule_evaluations: List[RuleEvaluationRecord]
    declarations: CanonicalDeclaration
    calibrated_measurements: MetricScaleResult
    evidence_crops: List[EvidenceCropMetadata]
    improvement_notice: Optional[ImprovementNoticePayload]
    sha256_hash: str
```

---

## 4. Package Architecture (`packages/rules-engine/`)

```
packages/rules-engine/src/nirikshak_rules_engine/
├── __init__.py          # Unified exports (RuleEngine, Normalizer, USPValidator, FontMatrix, FOPNL, Penalties, Schemas)
├── schemas.py           # Canonical Pydantic schemas (frozen contract)
├── normalizer.py        # Deterministic regex entity extractor from noisy OCR tokens
├── rule_engine.py       # Master statutory state machine (Rules 3, 6, 7, 11, 26)
├── usp_validator.py     # IEEE-754 / decimal.Decimal verified USP math auditor
├── font_matrix.py       # Rule 7 Tables I & II PDP bracket matcher with 0.10mm buffer
├── notice_builder.py    # Section 36(1) Jan Vishwas Improvement Notice generator
├── fopnl.py             # FSSAI Front-of-Pack Nutritional Labeling (FOPNL) & Dietary Display checklist
└── penalties.py         # Section 36(1) & 48/48A multi-year penalty compounding & recidivism router
```

---

## 5. Scope Boundaries ("Not My Job")
- **Not Member 3:** Training OCR models, tuning PaddleOCR weights, or adjusting det/rec thresholds (Member 1).
- **Not Member 3:** Perspective transformation, coin ellipse fitting, or homography unwarping (Member 2).
- **Not Member 3:** FastAPI routes, HTTP uploads, or multipart parsing (Member 4).
- **Not Member 3:** React components, Tailwind styling, or canvas overlays (Member 5).
- **Not Member 3:** Docker orchestration, Nginx reverse proxy, or CI runner setup (Member 6).

---

## 6. Execution Tracking & Chunk History

### Chunk 1: Canonical Pydantic Schemas & Contract Freezing (VERIFIED)
- `packages/rules-engine/src/nirikshak_rules_engine/schemas.py` created and frozen.
- Pydantic v2 models: `ComplianceState`, `VerdictBadgeColor`, `UnitType`, `ScriptType`, `OCRToken`, `MetricScaleResult`, `CanonicalDeclaration`, `RuleEvaluationRecord`, `EvidenceCropMetadata`, `ImprovementNoticePayload`, `ComplianceEvaluationResult`.
- Verification: 8 tests passing in `tests/rules/test_schemas.py` in 0.21s.
- Conformance verified against `docs/API_CONTRACT.md` and `docs/team/INTEGRATION_CHECKLIST.md`.

### Chunk 2: Synthetic Token Fixtures & Deterministic Normalizer (VERIFIED)
- **Fixtures:** `tests/fixtures/mock_ocr_tokens.json` containing 12 comprehensive packaging scenarios.
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/normalizer.py`.
- **Parsing Rules:**
  - **MRP:** Match currency symbols (`₹`, `Rs.`, `Rs`, `INR`), decimal amounts, and mandatory tax qualifiers (`inclusive of all taxes`, `सभी कर सहित`).
  - **Net Quantity:** Match magnitudes and standard SI units (`g`, `kg`, `ml`, `l`, `m`, `cm`, `piece`, `N`), flagging non-standard notations (`Gms`, `Kgs`, `ML`).
  - **Dates:** Extract month and year (`MM/YY`, `MM/YYYY`, `Best Before`, `पैकिंग तिथि`).
  - **Consumer Care:** Extract 1800 toll-free phone and email addresses.
  - **Country of Origin:** Identify origin statements under Rule 6(1)(aa).
  - **CTC Confusion Repair:** Repair OCR character confusions (`O` $\rightarrow$ `0`, `l` $\rightarrow$ `1`).
- **Verification:** 11 tests passing in `tests/rules/test_normalizer.py` in 0.19s ($< 0.1\text{ms}$ average latency).

### Chunk 3: Rule 6 Mandatory Completeness, Rule 3 Scope & Rule 26 Exemption State Machine (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/rule_engine.py`.
- **Statutory Evaluation:**
  - **Rule 3 Wholesale Exclusions:** Packages $> 25\text{kg}$ or $> 25\text{L}$ are excluded from retail mandatory declarations (except cement/fertilizer up to 50kg).
  - **Rule 26(a) Small Pack Exemptions:** Packages $\le 10\text{g}$ or $\le 10\text{ml}$ are exempt from general declarations.
  - **G.S.R. 881(E) Pan Masala & Tobacco Override:** Sachet sizes ($\le 10\text{g}$) for pan masala and tobacco are strictly **NON-EXEMPT** under G.S.R. 881(E) and must bear all declarations.
  - **Rule 6(1)(a)-(h) Mandatory Completeness:** Evaluates 8 declarations with authentic Gazette citations:
    - 6(1)(a): Manufacturer/Packer Name and Address
    - 6(1)(aa): Country of Origin (G.S.R. 629(E))
    - 6(1)(b): Generic or Common Commodity Name
    - 6(1)(c): Net Quantity in standard SI units (Rule 13)
    - 6(1)(d): Month and Year of Manufacture / Packing
    - 6(1)(e): Maximum Retail Price (MRP) inclusive of all taxes
    - 6(1)(g): Consumer Care phone & email grievance contacts
- **Tests:** `tests/rules/test_rule_6.py` (7 tests) and `tests/rules/test_rule_26_exemptions.py` (5 tests) passing 100%.

### Chunk 4: Rule 6(11) Unit Sale Price (USP) Arithmetic Auditor (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/usp_validator.py`.
- **Statutory Authority:** Rule 6(11) inserted by G.S.R. 779(E) and amended by G.S.R. 226(E) (effective 01.10.2022).
- **Statutory Denominators:**
  - Weight: $< 1\text{kg} \rightarrow \text{₹/g}$; $\ge 1\text{kg} \rightarrow \text{₹/kg}$.
  - Volume: $< 1\text{L} \rightarrow \text{₹/ml}$; $\ge 1\text{L} \rightarrow \text{₹/L}$.
  - Length: $< 1\text{m} \rightarrow \text{₹/cm}$; $\ge 1\text{m} \rightarrow \text{₹/m}$.
  - Area: $< 1\text{ m}^2 \rightarrow \text{₹/sq cm}$; $\ge 1\text{ m}^2 \rightarrow \text{₹/sq m}$.
  - Count: Any number $\rightarrow$ per piece / per number / per unit.
  - *Prohibited*: "per 100g" / "per 100ml" is obsolete and non-compliant.
- **Statutory Provisos / Exemptions:**
  - Proviso (a): Net quantity $< 10\text{g}$ or $< 10\text{ml}$ exempt from USP declaration.
  - Proviso (b): Wholesale packages exempt from USP declaration.
  - Proviso (c): Packages where MRP equals Unit Sale Price (e.g. exactly 1kg, 1L, or 1 piece).
- **Arithmetic Precision & Rounding:**
  - High-precision `decimal.Decimal` division.
  - Statutory rounding: `ROUND_HALF_UP` to 2 decimal places.
  - Engineering comparison tolerance buffer: $1.0\%$ relative tolerance OR absolute difference $\le 0.02$.
- **Verification Suite:** `tests/rules/test_rule_6_11.py` (15 tests) and `tests/rules/test_usp_arithmetic.py` (11 tests) passing 100%.

### Chunk 5: Rule 7 Tables I & II Font Height Matrix & 5-State Classifier (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/font_matrix.py`.
- **Statutory Authority:** Rule 7 of LM(PC) Rules, 2011, Table-I (General) and Table-II (Food Products), amended by G.S.R. 629(E) and G.S.R. 1373(E).
- **Statutory PDP Area Brackets & Minimum Numeral Heights:**
  - $A \le 50\text{ cm}^2$: Normal $\ge 1.0\text{mm}$, Blown/Formed $\ge 1.5\text{mm}$ (Table I: $1.0\text{mm}$, Table II: $1.0\text{mm}$).
  - $50 < A \le 100\text{ cm}^2$: Normal $\ge 1.5\text{mm}$, Blown/Formed $\ge 3.0\text{mm}$.
  - $100 < A \le 500\text{ cm}^2$: Normal $\ge 2.5\text{mm}$, Blown/Formed $\ge 4.0\text{mm}$ (Table I: $2.0\text{mm}$, Table II: $2.5\text{mm}$).
  - $500 < A \le 2500\text{ cm}^2$: Normal $\ge 4.0\text{mm}$, Blown/Formed $\ge 6.0\text{mm}$.
  - $A > 2500\text{ cm}^2$: Normal $\ge 6.0\text{mm}$, Blown/Formed $\ge 6.0\text{mm}$.
- **Benefit-of-Doubt Tolerance Buffer:**
  - Statutory compliance check must apply a $0.10\text{mm}$ buffer in favor of the manufacturer before asserting non-compliance ($h_{\text{eff}} = h_{\text{meas}} + 0.10\text{mm}$).
- **5-State Compliance Taxonomy:**
  - Classifies composite evaluation into `COMPLIANT`, `NON_COMPLIANT`, `DEVIATION_DETECTED`, `UNCERTAIN`, `EXEMPTED`.
- **Verification Suite:** `tests/rules/test_rule_7.py` (15 tests passed in 0.27s).

### Chunk 6: Section 36(1) Jan Vishwas Improvement Notice Builder & Pipeline Integration (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/notice_builder.py`.
- **Statutory Enactment:** Section 36(1) of the Legal Metrology Act, 2009, as amended by the *Jan Vishwas (Amendment of Provisions) Act, 2026* (effective May 1, 2026).
- **Decriminalized Reform:**
  - Strict statutory mandate: 15-day rectification / cure window prior to compounding or penalties.
  - Zero criminal or imprisonment terminology permitted in system output (`audit_text_decriminalization()`).
- **Notice Schema & Payload Structure:**
  - `ImprovementNoticePayload`: `recommended`, `act_provision`, `cure_period_days=15`, `statutory_grounds`, `compounding_authority`, `notice_title`, `notice_text`, `itemized_violations`.
  - Structured PDF metadata and eMaap sync mock payload (`build_emaap_sync_payload`).
- **Verification Suite:** `tests/rules/test_notice_builder.py` (6 tests passed in 0.27s).

### Chunk 7: Full 25-Case Statutory Regression Suite, Benchmarking & Fuzzing (VERIFIED)
- **Regression Suite:** `tests/rules/test_rules_engine.py` (25 distinct statutory test cases covering every sub-clause, 100% green).
- **CPU Benchmarking:** `tests/rules/test_benchmark_latency.py` (Mean 0.035ms, P95 0.045ms, Max 0.058ms; 500x faster than $< 20\text{ms}$ budget).
- **Anti-Hallucination Fuzzing:** `tests/rules/test_fuzzing.py` (200 randomized corrupted payloads, 0 unhandled exceptions).
- **Statutory Traceability:** `docs/17_CLAIMS/STATUTORY_TRACEABILITY.md` maps every codified rule to primary gazettes.

### Chunk 8 / Gate 8: Monorepo Integration & API Contracts (VERIFIED)
- **Integration Suite:** `tests/integration/test_engine_to_api.py` (3 tests passed).
- **Verification:** `StatutoryRuleEngine` -> `nirikshak_shared.models.contracts.RuleEvaluation` & `InspectionResult` -> `FastAPI /api/v1/inspections` roundtrip serialization.

### Buffer Task 1: FSSAI FOPNL & Dietary Display Checklist (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/fopnl.py`.
- **Statutory Authority:** Food Safety and Standards (Labelling and Display) Regulations, 2020 (Regulation 5(3), 5(4)) and draft Indian Nutrition Rating (INR) guidelines.
- **Verification:** `tests/rules/test_fopnl.py` (9 tests passed; $< 0.1\text{ms}$ latency).

### Buffer Task 2: Section 36(1) & 48/48A Multi-Year Recidivism & Penalty Auditor (VERIFIED)
- **Module:** `packages/rules-engine/src/nirikshak_rules_engine/penalties.py`.
- **Statutory Rules:** Section 36(1) fine escalation (1st: ₹10k–₹25k; 2nd: ₹25k–₹50k; 3rd: ₹50k–₹100k) with Section 48(2) 3-year lookback bar for compounding.
- **Verification:** `tests/rules/test_penalties.py` (7 tests passed; 100% decriminalized terminology guarantee).




