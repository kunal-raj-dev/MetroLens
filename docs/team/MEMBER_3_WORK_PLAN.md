# INDIVIDUAL WORK PLAN: MEMBER 3
# Legal Rules, Domain Logic & Compliance Engine Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Package:** `packages/rules-engine/` | **Secondary Role:** Architecture & Legal Governance

---

## 1. Member Role
**Member 3 — Legal Rules, Domain Logic & Statutory Compliance Engine Lead**

---

## 2. Mission
Guard the core intellectual property and architectural integrity of MetroLens AI by delivering an unshakeable, 100% deterministic, audit-traceable statutory compliance engine. Member 3 is personally responsible for transforming raw OCR tokens into structured canonical entities via deterministic regex parsers, executing rule evaluation against the *Legal Metrology (Packaged Commodities) Rules, 2011* (incorporating the *Jan Vishwas (Amendment of Provisions) Act, 2026*), performing IEEE-754 verified Unit Sale Price (USP) arithmetic, enforcing the Rule 7 area-to-font-height matrix, and classifying inspections into the 5-State statutory taxonomy in $< 20\text{ms}$ with zero legal hallucination across a 25-case statutory test suite.

---

## 3. Ownership

### Primary Ownership:
- `packages/rules-engine/normalizer.py`: Deterministic regex token extractor converting raw OCR tokens into typed `CanonicalDeclaration` entities.
- `packages/rules-engine/rule_engine.py`: Statutory state machine executing Rules 6(1)(a)-(h), 6(11), 7, 8, and 26.
- `packages/rules-engine/schemas.py`: Canonical Pydantic schemas (`CanonicalDeclaration`, `RuleEvaluationRecord`, `ComplianceEvaluationResult`).
- `packages/rules-engine/usp_validator.py`: Unit Sale Price arithmetic auditor ($\text{Expected USP} = \frac{\text{MRP}}{\text{NetQty}}$ across standard units: ₹/g, ₹/kg, ₹/ml, ₹/l, ₹/piece).
- `packages/rules-engine/font_matrix.py`: Principal Display Panel area bracket matcher against Rule 7 Table-I (General) and Table-II (Food).
- `tests/rules/`: Complete 25-case statutory regression test suite covering every rule, sub-clause, and exception.

### Secondary Support:
- Support **Member 4 (Backend)** in integrating the rule engine into FastAPI routes and generating Section 36(1) Improvement Notice data.
- Maintain legal traceability between codified rules and authentic government gazettes in `METROLENS_LEGAL_SOURCE_PACK/`.

---

## 4. Concrete Responsibilities
1. Define and freeze the canonical Pydantic schemas on Day 1 (`docs/API_CONTRACT.md`), serving as the stable contract for the entire team.
2. Implement robust regex token extractors in `normalizer.py`:
   - MRP: Match currency symbols (`₹`, `Rs`, `INR`), decimal amounts, and the mandatory tax qualifier (`"inclusive of all taxes"`).
   - Net Quantity: Match numeric magnitudes and standard SI units (`g`, `kg`, `ml`, `l`, `m`, `cm`, `piece`), rejecting non-standard notation (`"Gms"`, `"Kgs"`, `"ML"`).
   - Dates: Match diverse packaging date formats (`MM/YY`, `MM/YYYY`, `Best Before X Months`, `Use By DD/MM/YYYY`).
   - Consumer Care: Extract telephone numbers (1800 toll-free or landline) and email addresses (`care@brand.com`).
   - Country of Origin: Identify statutory origin statements under Rule 6(1)(aa).
3. Codify Rule 3 & Rule 26 Statutory Exemption Gate:
   - Exclude wholesale industrial commodities ($> 25\text{kg}$ or $> 25\text{L}$) under Rule 3.
   - Apply Rule 26(a) small package exemptions ($\le 10\text{g}$ or $\le 10\text{ml}$), but **strictly enforce the statutory carve-outs for pan masala (G.S.R. 881(E)) and tobacco products**, which are never exempt.
4. Codify Rule 6(1)(a)-(h) Mandatory Completeness:
   - Evaluate the 8 mandatory declarations; assign specific gazette citations for every detected omission.
5. Codify Rule 6(11) Unit Sale Price (USP) Arithmetic:
   - Calculate expected USP: For packages $\le 1\text{kg/l}$, USP must be per gram or per milliliter; for packages $> 1\text{kg/l}$, USP must be per kilogram or per liter.
   - Verify that declared USP matches calculated USP within a strict $1.0\%$ rounding tolerance.
6. Codify Rule 7 (Tables I & II) Minimum Numeral Heights:
   - Match package Principal Display Panel (PDP) area ($A \text{ in cm}^2$) to statutory minimum numeral heights ($1.0\text{mm}$ to $6.0\text{mm}$).
   - Evaluate measured font height ($h_{\text{mm}}$); apply a $0.10\text{mm}$ benefit-of-doubt tolerance buffer before asserting non-compliance.
7. Classify into 5-State Taxonomy:
   - `COMPLIANT`, `NON_COMPLIANT`, `DEVIATION_DETECTED`, `UNCERTAIN`, `EXEMPTED`.
8. Produce Section 36(1) Improvement Notice data structure citing the 15-day rectification window under the *Jan Vishwas (Amendment of Provisions) Act, 2026*.

---

## 5. What Member 3 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Training neural networks or tuning PaddleOCR ONNX runtimes (owned strictly by Member 1).
- **NOT MY JOB:** Performing OpenCV contour detection, ellipse fitting, or homography unwarping (owned strictly by Member 2).
- **NOT MY JOB:** Building React dropzones, HTML canvas components, or CSS styles (owned strictly by Member 5).
- **NOT MY JOB:** Managing Docker builds, Nginx reverse proxies, or CI/CD pipelines (owned strictly by Member 6).
- **NOT MY JOB:** Modifying the synchronous sub-2.5s architecture without lead sign-off.

---

## 6. Inputs Received
- **From Member 1 (OCR):** Standardized list of `OCRToken` dictionaries containing text, coordinates, and confidences.
- **From Member 2 (CV/Calib):** `MetricScaleResult` containing scale factor $S$, PDP area ($\text{cm}^2$), and measured font heights ($h_{\text{mm}}$).
- **From Legal Research:** Primary gazette clauses in `METROLENS_LEGAL_SOURCE_PACK/01_PRIMARY_ACTS/` and `02_CURRENT_CONSOLIDATED_RULES/`.
- **Specification:** `docs/LEGAL_RULE_MATRIX.md` and `docs/PRODUCT_BLUEPRINT.md`.

---

## 7. Concrete Outputs Delivered
- `packages/rules-engine/`: Fully tested, deterministic statutory rule engine.
- `CanonicalDeclaration` and `ComplianceEvaluationResult` Pydantic models.
- `tests/rules/`: 25 passing statutory test cases validating all legal clauses.
- Section 36(1) Improvement Notice payload generator.
- `docs/17_CLAIMS/STATUTORY_TRACEABILITY.md`: Mapping each rule clause to its primary gazette notification.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **OCR Tokens Stream** | Member 1 | Raw text tokens to feed into regex normalizer | Day 2, 2:00 PM | Use mock OCR token fixtures from `tests/fixtures/mock_ocr_tokens.json`. |
| **Font Heights & PDP Area** | Member 2 | Calibrated millimeters for Rule 7 verification | Day 3, 12:00 PM | Use mock calibration fixtures with known font heights (1.15mm, 1.60mm). |
| **API Contract Alignment** | Member 4 | Agreement on FastAPI request/response schemas | Day 1, 12:00 PM | Use frozen schemas from `docs/API_CONTRACT.md`. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: Risk Spike — Schema Freezing & Statutory Logic Mapping
- **Goal:** Freeze all Pydantic data schemas and map Rules 6, 6(11), 7, and 26 into pure Python logic.
- **Tasks:** Author `packages/rules-engine/schemas.py`; distribute schemas to M1, M2, M4, M5, M6; write logic flowcharts for Unit Sale Price math and Rule 26 pan masala exemption carve-out.
- **Deliverables:** `schemas.py` and passing serialization tests in `tests/rules/test_schemas.py`.
- **Expected Time:** 6 hours.
- **Dependencies:** None (self-contained domain architecture).
- **Checkpoint (Gate 1 - T+24h):** Schemas frozen and accepted by all 6 team members.
- **Risk:** Disagreements on schema naming or optional field structures.
- **Fallback:** Lead Architect decides canonical schema structure unilaterally.

### DAY 2: Canonical Normalizer Regex & Vertical Slice 0 Support
- **Goal:** Implement regex entity extractors and wire normalizer into Vertical Slice 0.
- **Tasks:** Implement `normalizer.py`: extract MRP, Net Quantity, Mfg Date, Address, and Consumer Care details from raw token stream; connect into headless CLI pipeline with Member 4.
- **Deliverables:** `normalizer.py` with 15 passing token normalization unit tests.
- **Expected Time:** 7 hours.
- **Dependencies:** None (develop against mock token fixtures).
- **Checkpoint (Gate 2 - T+48h):** Vertical Slice 0 successfully parses raw tokens into `CanonicalDeclaration`.
- **Risk:** Noisy OCR text confuses regex patterns (e.g. `MRP Rs. 10.00` extracted as `1000`).
- **Fallback:** Implement strict sanity bounds (e.g. retail FMCG MRP between ₹1 and ₹50,000; Net Qty $> 0$).

### DAY 3: Rule 6 Completeness & Rule 26 Exemption State Machine
- **Goal:** Codify mandatory declaration completeness and statutory exemption logic.
- **Tasks:** Implement `rule_engine.py`: evaluate presence of 8 mandatory declarations; codify Rule 3 wholesale exclusion ($> 25\text{kg/l}$); codify Rule 26 small pack exemptions with pan masala/tobacco overrides; assign gazette citations.
- **Deliverables:** Rule 6 and Rule 26 evaluation modules passing 10 statutory test cases.
- **Expected Time:** 6 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 3 - Day 3):** Correctly flags miniature pan masala sachet as NON-EXEMPT under G.S.R. 881(E).
- **Risk:** Rule 26 exemptions mistakenly applied to tobacco.
- **Fallback:** Default commodity category to non-exempt if category detection is uncertain.

### DAY 4: Rule 6(11) Unit Sale Price (USP) Arithmetic Auditor
- **Goal:** Build mathematically verified Unit Sale Price auditor across all statutory denominations.
- **Tasks:** Implement `usp_validator.py`: calculate expected USP based on declared MRP and Net Quantity; normalize units ($\text{g} \rightarrow \text{kg}$, $\text{ml} \rightarrow \text{l}$); verify declared USP matches within $1.0\%$ tolerance; flag missing USP on packs $> 100\text{g/ml}$.
- **Deliverables:** USP validator with 10 synthetic mathematical test cases.
- **Expected Time:** 6 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 4 - Day 4):** 100% pass on 10 synthetic USP tests, including edge cases (₹0.05/g, ₹450/kg).
- **Risk:** Floating-point rounding errors trigger false violation flags (e.g. $10 / 3 = 3.3333...$).
- **Fallback:** Use Python `decimal.Decimal` with standard `ROUND_HALF_UP` rounding to 2 decimal places.

### DAY 5: Rule 7 Area-to-Font Height Matrix & 5-State Adjudication
- **Goal:** Codify Rule 7 Tables I & II and implement unified 5-State compliance aggregator.
- **Tasks:** Implement `font_matrix.py`: match PDP area ($A \text{ cm}^2$) to minimum height thresholds; apply $0.10\text{mm}$ benefit-of-doubt buffer; integrate all rule outputs into `ComplianceEvaluationResult` with 5-State classification.
- **Deliverables:** Complete statutory rule engine passing 25 regression test cases.
- **Expected Time:** 7 hours.
- **Dependencies:** Measured font heights from Member 2.
- **Checkpoint (Gate 5 - Day 5):** 25-case statutory test suite passes with 100% accuracy in $< 20\text{ms}$.
- **Risk:** Ambiguous boundary conditions (e.g. PDP exactly $50\text{ cm}^2$).
- **Fallback:** Gazette specifies inclusive brackets ($\le 50$, $> 50$ to $\le 100$); follow exact gazette wording.

### DAY 6: Section 36(1) Improvement Notice Generator & eMaap Payload
- **Goal:** Format statutory Improvement Notice data for PDF generation and eMaap sync.
- **Tasks:** Build notice draft generator citing Section 36(1) of Legal Metrology Act, 2009 (as amended by Jan Vishwas Act, 2026); structure legal notice text specifying 15-day cure period; build mock eMaap JSON payload for Member 4.
- **Deliverables:** Notice generation module in `packages/rules-engine/notice_builder.py`.
- **Expected Time:** 5 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 6):** Emitted notice payload includes exact legal section, violation clause, and cure window.
- **Risk:** Accidental inclusion of obsolete criminal penalty terminology.
- **Fallback:** Audit notice template against Jan Vishwas Act 2026 text; ensure zero mention of "imprisonment".

### DAY 7: Zero-Hallucination Audit & End-to-End Edge-Case Fuzzing
- **Goal:** Verify that rule engine is completely deterministic and mathematically impenetrable.
- **Tasks:** Fuzz rule engine with 200 randomly corrupted declaration payloads; verify zero unhandled exceptions; run anti-hallucination verification scripts in `scripts/verification/`.
- **Deliverables:** Anti-hallucination audit report proving 100% deterministic compliance decisions.
- **Expected Time:** 5 hours.
- **Dependencies:** Full pipeline integration from Member 4.
- **Checkpoint (Gate 7):** All verification scripts green; zero external API calls in code.
- **Risk:** Edge-case regex catastrophic backtracking on long text.
- **Fallback:** Enforce maximum string length caps on all input tokens before regex evaluation.

### DAY 8: Code Freeze & Statutory Defense Preparation
- **Goal:** Lock rule engine code; prepare legal arguments for jury Q&A.
- **Tasks:** Freeze `packages/rules-engine/`; write legal compliance section in `docs/06_RULE_ENGINE/`; train team on answering jury questions regarding Jan Vishwas 2026 amendments.
- **Deliverables:** Frozen code, passing tests, and jury Q&A defense document.
- **Expected Time:** 4 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Zero open PRs; all tests pass in CI.

### DAY 9: Buffer Day & Live Demo Adjudication Support
- **Goal:** Support live demo execution.
- **Tasks:** Verify that on-screen compliance findings match ground-truth statutory expectations during demo rehearsals; assist with technical legal explanations during jury questioning.
- **Expected Time:** As needed.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | Primary legal acts verified | `verify_legal_sources.py` passes | Check legal source pack |
| **CP-1** | T+24h | Canonical Pydantic schemas frozen | Schemas compile and serialize sample JSON | Architect resolves disputes |
| **CP-2** | T+48h | Regex normalizer operational | Correctly parses MRP and Net Qty on 10 fixtures | Refine regex tokens |
| **CP-3** | Day 3 | Rule 6 & 26 state machine ready | Flags pan masala non-exemption correctly | Review GSR 881(E) gazette clause |
| **CP-4** | Day 5 | Complete 25-case test suite passes | `pytest tests/rules/` passes 100% in $<20\text{ms}$ | Debug failing edge case |
| **CP-5** | Day 7 | Zero-hallucination audit complete | `verify_claims.py` and `verify_rule_registry.py` pass | Scrub unverified legal claims |
| **CP-6** | Day 8 | Final code freeze | Code locked; zero failing tests | Revert unverified changes |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **Normalizer** | Parses MRP, Net Qty, Dates from noisy tokens | `pytest tests/rules/test_normalizer.py` | 100% passing test report across 20 synthetic OCR outputs |
| **Rule 6 Completeness**| Flags missing mandatory declarations with gazette clause | `pytest tests/rules/test_rule_6.py` | Unit test assertions verifying exact statutory citations |
| **Rule 6(11) USP Math**| Correctly validates $\text{MRP}/\text{Qty}$ across 5 denominations | `pytest tests/rules/test_rule_6_11.py` | 10 passing mathematical test cases with decimal rounding |
| **Rule 7 Font Heights**| Matches PDP area to height matrix with $0.10\text{mm}$ buffer | `pytest tests/rules/test_rule_7.py` | Test report validating compliant, deficit, and review states |
| **Execution Latency** | Full statutory rule evaluation completes in $< 20\text{ms}$ | `pytest tests/rules/test_benchmark_latency.py`| Performance timing log on CPU |

---

## 12. Testing Responsibility
- **Unit Tests:** `tests/rules/` (25 distinct statutory test cases covering every sub-clause).
- **Math Verification Tests:** `tests/rules/test_usp_arithmetic.py` (checks rounding, fractional grams, zero division).
- **Exemption Tests:** `tests/rules/test_rule_26_exemptions.py` (small packs, wholesale bulk, tobacco carve-outs).
- **Integration Tests:** `tests/integration/test_engine_to_api.py` (verifies compliance result serializes to API response).
- **Failure Cases:** Null inputs, negative MRP, zero Net Quantity, malformed dates (must return clean `UNCERTAIN` state without throwing exceptions).

---

## 13. Handoff Protocol & Checklist

### Handoff to Member 4 (Backend API) & Member 5 (Web UI):
1. **Working Package:** `packages/rules-engine/`.
2. **Standard Output:** `ComplianceEvaluationResult` matching schema in `docs/API_CONTRACT.md`.
3. **Usage Documentation:**
   ```python
   from packages.rules-engine.rule_engine import RuleEngine
   engine = RuleEngine()
   result = engine.evaluate(declarations, metric_scale_result)
   # returns ComplianceEvaluationResult(overall_verdict='POTENTIAL_NON_COMPLIANCE', ...)
   ```
4. **Test Evidence:** Attached pytest log showing 100% pass on 25 statutory test cases.
5. **Known Limitations:** Address physical existence cannot be verified by image alone; net contents weight requires physical scale.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** Schema disagreement with Member 4 $\rightarrow$ Refer to `docs/API_CONTRACT.md` as tie-breaker.
- **Blocked for 2 hours:** Legal ambiguity in gazette clause $\rightarrow$ Consult `METROLENS_LEGAL_SOURCE_PACK/` primary acts.
- **Blocked for half-day:** Complex regex backtracking causing timeout $\rightarrow$ Simplify regex; enforce character length bounds.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Floating-Point Arithmetic Error** | Med | High | Test fails on ₹0.333/g | Use `decimal.Decimal` with explicit rounding | Allow $\pm 1.0\%$ arithmetic tolerance |
| **Rule 26 Over-Exemption** | Low | High | Pan masala exempted | Codify strict commodity carve-out check (GSR 881(E)) | Default to non-exempt if uncertain |
| **Legal Wording Challenged** | Low | High | Obsolete fine cited | Align 100% with Jan Vishwas Act 2026 Section 36(1) | Presenter cites Section 15 screening |
| **Regex Parsing Failure on OCR Noise**| High | Med | Missing declaration | Multi-pattern regex matching + fallback heuristics | Flag field as `MANUAL_REVIEW_REQUIRED` |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 3 DAILY STATUS (DATE: ________)
• DONE: [Rules codified and statutory tests passing]
• BLOCKED: [Any legal or schema blockers > 30 mins]
• TESTED: [Number of statutory tests passing / 25]
• NEXT: [Tomorrow's domain milestone]
• RISK: [Any emerging statutory ambiguity]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. Python code is written with complete type annotations in `packages/rules-engine/`.
2. All 25 statutory rule test cases pass with 100% success rate.
3. Rule engine executes in $< 20\text{ms}$ on CPU.
4. Output conforms 100% to `ComplianceEvaluationResult` schema.
5. Handshake is verified with Member 4 (API) and Member 5 (Web UI).

---

## 18. AI Coding Workflow
$$\text{PLAN (Read Gazette Clause)} \longrightarrow \text{PROMPT AI (Pydantic / Regex)} \longrightarrow \text{REVIEW (Statutory Accuracy)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Write Pydantic boilerplate, parameterize pytest fixtures, and generate standard regex patterns.
- **MEMBER MUST DECIDE:** Legal interpretation, statutory thresholds, benefit-of-doubt buffers, and gazette citations.

---

## 19. Buffer Work
- **Primary:** Schemas, normalizer regex, Rules 6, 6(11), 7, 26, 25 statutory test cases, Improvement Notice data.
- **Buffer Task 1:** Codify FSSAI Front-of-Pack Nutritional Labeling (FOPNL) preliminary checklist.
- **Buffer Task 2:** Implement multi-year penalty calculation schedule for repeat offenders under Section 36(1).
