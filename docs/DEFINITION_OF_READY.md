# DEFINITION OF READY (DoR) SPECIFICATION
# MetroLens AI™ — Automated Legal Metrology Inspection & Compliance System
### Ministry of Consumer Affairs, Food & Public Distribution | Problem Statement: SIH26034
**Document Status:** Authoritative Governance Standard | **Target Audience:** All MetroLens Engineering Teammates (M1–M6)  
**Standards Conformance:** RFC 2119 (MUST, SHOULD, MAY) | **Last Updated:** September 2026

---

## 📌 Executive Purpose

In high-velocity engineering teams under hackathon constraints, the single greatest source of wasted hours, merge conflicts, and buggy demos is **premature coding on underspecified tasks**.

When an engineer begins work on an ambiguous instruction (such as *"Bro, make the OCR work"* or *"Fix font height"*), several failures occur simultaneously:
1. The developer does not know when they are finished (missing acceptance criteria).
2. The developer builds features nobody asked for, introducing feature creep (missing scope boundaries).
3. The developer has no mechanism to verify correctness before opening a pull request (missing test strategy).
4. Multiple teammates accidentally touch the same modules, causing merge conflicts (missing single ownership).
5. The code deviates from authentic statutory mandates (missing legal or architectural anchors).

The **Definition of Ready (DoR)** serves as the mandatory, auditable intake gate in the MetroLens AI development lifecycle:

```text
Requirement / Bug / Legal Mandate
               │
               ▼
      Create GitHub Issue
               │
               ▼
    [ SPECIFYING STAGE ]
   Fill Required Fields & Boundaries
               │
               ▼
    DoR Verification Check
          ↙          ↘
     NOT READY        READY
        │               │
  Clarify Issue    Assign Primary Owner (M1–M6)
                        │
                        ▼
                 [ PHASE 2 START ]
            Create Branch & Implement Code
```

> **The Golden Rule of Phase 1:**  
> **NO TEAMMATE SHALL CREATE A BRANCH OR WRITE A SINGLE LINE OF CODE FOR A TASK THAT HAS NOT SATISFIED THE DEFINITION OF READY.**

---

## 1. The Core 10-Point Readiness Model

An issue is eligible to be marked **`status:ready`** if and only if all 10 criteria below are fully satisfied. Every criterion is explained in plain language for junior and senior teammates alike.

| # | Criterion | RFC 2119 Level | What It Means in Plain Language |
| :-: | :--- | :---: | :--- |
| **1** | **Clear Objective** | **MUST** | The desired outcome is stated in 1–2 unambiguous sentences. Anyone on the team can read it and instantly understand what will exist when the work is complete. |
| **2** | **Context & Problem Understood** | **MUST** | The background is explained: Why does this task exist? Is it fixing a defect, implementing a statutory mandate, improving performance, or creating an architectural foundation? |
| **3** | **Statutory or Architectural Anchor** | **MUST** | Grounded in project truth. Every change must reference a specific clause in the Legal Metrology Act/Rules (e.g., Rule 6, 7, 8, 26; Jan Vishwas Act, 2026), a section in [`docs/PRODUCT_BLUEPRINT.md`](PRODUCT_BLUEPRINT.md), an ADR in [`docs/DECISION_LOG.md`](DECISION_LOG.md), or a Traceability ID (TR-01 to TR-10 in [`docs/TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md)). |
| **4** | **Testable Acceptance Criteria** | **MUST** | A checklist of specific, binary (pass/fail) conditions that can be objectively tested. Vague criteria like "make it work" or "optimize" are strictly forbidden. |
| **5** | **In-Scope Boundary Defined** | **MUST** | An explicit list of what the developer **must** implement. Keeps the task focused and contained. |
| **6** | **Out-of-Scope Boundary Defined** | **MUST** | An explicit list of what the developer **will NOT** do in this issue. This is our primary defense against scope creep and delayed pull requests. |
| **7** | **Dependencies Identified & Confirmed** | **MUST** | Any prerequisite pull requests, base schemas, model weights, or dataset files must be identified. Prerequisites **must already be merged into `main`** before the task can be marked READY. |
| **8** | **Test Approach Understood** | **MUST** | The developer knows how they will verify their code *before* opening a PR. (e.g., Pytest unit tests, parameterized fixtures, benchmark scripts, or manual viewfinder checks). The test must execute locally and offline. |
| **9** | **Relevant Subsystem Identified** | **MUST** | The issue clearly tags the architectural module: CV, OCR, Rules, Frontend, Reporting, Data, Backend, Legal Pack, CI/CD, or Documentation. |
| **10** | **Exactly One Primary Owner Assigned** | **MUST** | Exactly one engineer (M1 through M6) is accountable. Shared primary ownership is forbidden. A secondary cross-support lead may be designated for pair review. |

---

## 2. READY vs NOT READY: Concrete MetroLens Examples

To eliminate subjectivity, review these side-by-side examples from actual MetroLens AI subsystems.

### Example A: AI & OCR Subsystem

#### ❌ NOT READY
> **Issue Title:** Improve OCR accuracy  
> **Body:**  
> "The Hindi OCR is making mistakes on biscuit packaging. Make it more accurate."  
> 
> **Why it Fails the DoR Gate:**
> - ❌ No quantitative target metric (how much accuracy?).
> - ❌ No dataset or test image fixture specified.
> - ❌ In-scope and out-of-scope boundaries absent.
> - ❌ No test approach defined.
> - ❌ No primary owner assigned.

#### ✅ READY
> **Issue Title:** `[FEAT]: Add Devanagari normalizer dictionary mapping for Hindi packaging declarations`  
> **Subsystem:** `sub:ocr` | **Priority:** `priority:P1-high` | **Primary Owner:** `M1 (AI & OCR Lead)`  
> **Statutory/Architectural Anchor:** LMPC Rules, 2011 Rule 6(1) (bilingual declarations in English or Hindi in Devanagari script); Traceability TR-02.  
> **Context:** Quantized PaddleOCR occasionally misreads specific Devanagari ligatures on curved surfaces (e.g., "शुद्ध मात्रा" read as "शद्ध मात्रा"). A post-OCR canonical normalizer dictionary can resolve common packaging entity keywords deterministically.  
> **In-Scope:**
> - Create `modules/normalizer/devanagari_dictionary.py` with 25 standard packaging term mappings (Net Qty, MRP, Mfg Date, Best Before, Consumer Care).
> - Implement regex-assisted token replacement on raw OCR output text.
> - Add unit test covering all 25 terms.  
> **Out-of-Scope:**
> - Retraining or fine-tuning neural network weights.
> - Handling non-Devanagari scripts (Tamil, Telugu, Bengali deferred).  
> **Acceptance Criteria:**
> - [ ] Resolves all 25 statutory keywords with 100% precision on synthetic text samples.
> - [ ] Normalizer processing latency $< 5\text{ms}$ per full image text block.
> - [ ] Does not alter English text tokens.
> - [ ] Unit test suite in `tests/test_devanagari_normalizer.py` passes 100%.  
> **Dependencies:** None; operates on raw string arrays.  
> **Test Approach:** Automated pytest unit tests with parametrized string inputs; runs offline.

---

### Example B: Backend & Rule Engine Subsystem

#### ❌ NOT READY
> **Issue Title:** Fix USP calculation  
> **Body:**  
> "Check the unit sale price according to the law."  
> 
> **Why it Fails the DoR Gate:**
> - ❌ Which law? Which rule? Which amendment?
> - ❌ How should denominations be rounded?
> - ❌ What is the expected behavior when Net Qty is given in milliliters vs grams?
> - ❌ What status code should be returned if USP is missing?

#### ✅ READY
> **Issue Title:** `[FEAT]: Implement Unit Sale Price (USP) arithmetic auditor under Rule 6(11)`  
> **Subsystem:** `sub:rules` | **Priority:** `priority:P1-high` | **Primary Owner:** `M3 (Backend & Rule Engine Lead)`  
> **Statutory/Architectural Anchor:** Legal Metrology (Packaged Commodities) Rules, 2011 Rule 6(11) (as amended); [`docs/LEGAL_RULE_MATRIX.md`](LEGAL_RULE_MATRIX.md) Section 3; Traceability TR-05.  
> **Context:** Under Rule 6(11), pre-packaged commodities must declare USP in standardized denominations (per gram/per g or kg if net qty $< 1\text{kg}$; per kilogram if net qty $> 1\text{kg}$; per ml/per 100ml if net qty $< 1\text{L}$; per liter if net qty $> 1\text{L}$). If declared USP differs by $> 1\%$ from $\text{MRP} / \text{NetQty}$, flag as non-compliant.  
> **In-Scope:**
> - Implement `modules/rules/rule_6_11_usp.py` with IEEE-754 guarded division.
> - Support unit conversions: grams $\leftrightarrow$ kilograms, milliliters $\leftrightarrow$ liters, count $\leftrightarrow$ per item.
> - Return `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` if valid within 1% margin.
> - Return `POTENTIAL_NON_COMPLIANCE` if arithmetic deviates $> 1\%$ or illegal denomination is used.  
> **Out-of-Scope:**
> - Multipack / wholesale packaging calculations under Rule 24.
> - Foreign currency conversions.  
> **Acceptance Criteria:**
> - [ ] Passes all 12 statutory denomination test cases specified in `docs/LEGAL_RULE_MATRIX.md`.
> - [ ] Flags omitted USP as `POTENTIAL_NON_COMPLIANCE` (Section 36(1) Notice recommendation).
> - [ ] Executes in $< 10\text{ms}$ on CPU.
> - [ ] Full test coverage in `tests/test_rule_6_11_usp.py`.  
> **Dependencies:** Pydantic canonical schema model merged into `main`.  
> **Test Approach:** Pytest parameterized test cases covering 15 standard and non-standard packaging samples.

---

### Example C: Computer Vision & Calibration Subsystem

#### ❌ NOT READY
> **Issue Title:** Coin detection bug  
> **Body:**  
> "The 10 rupee coin is not detected sometimes."  
> 
> **Why it Fails the DoR Gate:**
> - ❌ No reproduction steps.
> - ❌ No image fixture or environment details (camera resolution, angle, lighting).
> - ❌ No contrast between expected and actual behavior.
> - ❌ No scope on what detector adjustments are permitted.

#### ✅ READY
> **Issue Title:** `[BUG]: OpenCV HoughCircles fails to detect 10-Rupee coin when perspective tilt exceeds 15°`  
> **Subsystem:** `sub:cv` | **Priority:** `priority:P1-high` | **Primary Owner:** `M2 (Calibration & Geometry Lead)`  
> **Statutory/Architectural Anchor:** Master Blueprint v0.3 Section 3 (Planar Metric Scale Recovery $S = 27.0\text{mm} / d_{\text{major}}$); Traceability TR-04.  
> **Context:** When the smartphone camera is held at an oblique angle ($> 15^\circ$), the circular coin projects as an ellipse. `cv2.HoughCircles` fails because circularity is degraded. An ellipse fitting fallback is required.  
> **Steps to Reproduce:**
> 1. Run `python -m modules.cv.scale_calibration --image tests/fixtures/coin_tilt_20deg.jpg`.
> 2. Observe output: `ValueError: No valid circular contour detected`.  
> **Expected Behavior:** Detector recognizes elliptical contour, fits ellipse with `cv2.fitEllipse`, recovers major axis $d_{\text{major}}$, and computes scale factor $S$ within 5% error.  
> **Actual Behavior:** `HoughCircles` returns zero circles and pipeline terminates with uncaught exception.  
> **In-Scope Fix:**
> - Add adaptive thresholding contour detection fallback when `HoughCircles` yields zero candidates.
> - Use major axis of fitted ellipse ($d_{\text{major}}$) for scale factor $S = 27.0\text{mm} / d_{\text{major}}$.  
> **Out-of-Scope:**
> - Neural network keypoint detection (YOLO/RCNN).
> - Multi-coin support (5-Rupee, 2-Rupee).  
> **Acceptance Criteria:**
> - [ ] Successfully detects 10-Rupee coin at tilts between $0^\circ$ and $25^\circ$ across all 5 test fixture images.
> - [ ] Scale error remains $< 5\%$ compared to millimeter ground-truth grid.
> - [ ] Gracefully handles failure by returning `scale_recovered: false` instead of raising uncaught exception.  
> **Dependencies:** Existing test fixture images in `tests/fixtures/`.  
> **Test Approach:** `tests/test_scale_calibration.py` with 5 fixture images at $0^\circ, 10^\circ, 15^\circ, 20^\circ, 25^\circ$ tilt.

---

### Example D: Regulatory Exemption Subsystem

#### ❌ NOT READY
> **Issue Title:** Handle small packs  
> **Body:**  
> "Don't flag small packs because there is an exemption."  
> 
> **Why it Fails the DoR Gate:**
> - ❌ What is a "small pack"? What threshold?
> - ❌ Are there statutory exceptions to the exemption (e.g. tobacco / pan masala)?
> - ❌ What compliance badge should be displayed?

#### ✅ READY
> **Issue Title:** `[FEAT]: Implement Rule 26 statutory exemption switch with tobacco enforcement exception`  
> **Subsystem:** `sub:rules` | **Priority:** `priority:P2-medium` | **Primary Owner:** `M3 (Backend & Rule Engine Lead)`  
> **Statutory/Architectural Anchor:** Legal Metrology (Packaged Commodities) Rules, 2011 Rule 26(a) ($\le 10\text{g} / 10\text{ml}$ exemption); Gazette GSR 881(E) (exception for tobacco products); Traceability TR-06.  
> **Context:** Packages containing $\le 10\text{g}$ or $\le 10\text{ml}$ are exempt from general declaration requirements under Rule 26. However, tobacco and pan masala products are explicitly excluded from this exemption under GSR 881(E) and must always declare mandatory fields.  
> **In-Scope:**
> - Implement `modules/rules/rule_26_exemptions.py`.
> - Check commodity type and Net Quantity against $10\text{g} / 10\text{ml}$ threshold.
> - If exempt: return `STATUTORY_EXEMPTION_APPLIED` badge and suppress declaration omission warnings.
> - If tobacco/pan masala: override exemption and enforce full Rule 6 check.  
> **Out-of-Scope:**
> - Wholesale packaging exemptions ($> 25\text{kg}$ or $> 25\text{L}$) under Rule 26(b).  
> **Acceptance Criteria:**
> - [ ] Miniature hotel soap ($8\text{g}$) returns `STATUTORY_EXEMPTION_APPLIED`.
> - [ ] Pan masala sachet ($5\text{g}$) returns `POTENTIAL_NON_COMPLIANCE` if missing MRP or Net Qty.
> - [ ] Unit test covering 6 edge cases passes 100%.  
> **Dependencies:** None.  
> **Test Approach:** Automated pytest cases in `tests/test_rule_26.py`.

---

## 3. Issue Lifecycle & State Transition Gate

Every issue in the MetroLens repository moves through a disciplined, linear state machine:

```text
┌─────────────────┐
│     BACKLOG     │ Issue submitted; raw idea, reported bug, or legal notification
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SPECIFYING    │ Author & Lead drafting context, scope, acceptance criteria,
└────────┬────────┘ and test strategy
         │
         ▼
┌─────────────────┐
│  VERIFYING DoR  │ Checklist evaluated against the 10-Point Readiness Model
└────────┬────────┘
         ├──────────────────────────────────────────┐
         ▼                                          ▼
   [PASS: DoR MET]                         [FAIL: DoR INCOMPLETE]
         │                                          │
         ▼                                          ▼
┌─────────────────┐                        ┌─────────────────┐
│      READY      │                        │    NOT READY    │
│ Assigned to M*  │                        │ Returned to     │
└────────┬────────┘                        │ author to fix   │
         │                                 └─────────────────┘
         ▼
┌─────────────────┐
│ IN DEVELOPMENT  │ Phase 2 Begins: Local branch created, code written & tested
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    IN REVIEW    │ PR opened, linked to Issue (`Closes #12`), CI green, review active
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DONE / MERGED  │ PR squashed & merged into main; branch deleted; issue closed
└─────────────────┘
```

### Transition Rules

1. **`BACKLOG` $\rightarrow$ `SPECIFYING`:**
   - Any team member may file an issue.
   - Initial state applied automatically via issue template (`status:specifying`).

2. **`SPECIFYING` $\rightarrow$ `READY`:**
   - The issue author fills out all required fields in the issue form.
   - The primary owner (or M6/M3 during triage) reviews the issue against the 10-point checklist.
   - When all 10 criteria are met, the label is updated to `status:ready`.
   - **Only now may the developer create a git branch.**

3. **`SPECIFYING` $\rightarrow$ `NOT READY`:**
   - If any mandatory field is missing, vague, untestable, or missing dependencies, the reviewer adds a comment detailing the missing information.
   - The issue remains blocked. **No code may be written.**

4. **`READY` $\rightarrow$ `IN DEVELOPMENT`:**
   - The assigned engineer switches to `main`, pulls latest, and creates a feature branch (`git checkout -b <type>/<issue-number>-<slug>`).
   - The label is updated to `status:in-dev`.

5. **`IN DEVELOPMENT` $\rightarrow$ `IN REVIEW`:**
   - Developer completes local implementation, runs tests offline, verifies diff, and pushes branch.
   - Pull Request is opened using the official PR template and linked to the issue (`Closes #XY`).
   - The label is updated to `status:in-review`.

6. **`IN REVIEW` $\rightarrow$ `DONE`:**
   - PR passes all CI checks and receives formal maintainer approval (M3 or M6).
   - PR is squashed and merged into `main`. The feature branch is deleted.
   - GitHub automatically closes the issue; label updated to `status:done`.

---

## 4. Beginner Developer Quick-Start: "What do I do when I receive a task?"

If you are a new teammate joining MetroLens AI, follow this exact step-by-step checklist:

```text
STEP 1: Open GitHub Issues.
        Find or create the issue corresponding to your task.
        MUST use the appropriate Issue Form (.github/ISSUE_TEMPLATE/).

STEP 2: Inspect the Issue Fields.
        Does it have:
        [ ] A 1-2 sentence clear objective?
        [ ] An architectural or statutory reference?
        [ ] In-scope and out-of-scope boundaries?
        [ ] Testable acceptance criteria with pass/fail checkboxes?
        [ ] An offline test strategy?
        [ ] Are you assigned as the single primary owner?

STEP 3: The DoR Self-Check.
        If ANY item above is missing -> DO NOT CODE YET.
        Ask your subsystem lead or Project Lead (M6) to clarify.
        Update the issue until all 10 DoR criteria are satisfied.

STEP 4: Verify the Issue is Marked `status:ready`.
        Once ready, proceed to Phase 2:
        1. Open your terminal.
        2. git checkout main
        3. git pull --ff-only origin main
        4. git checkout -b feat/<issue-number>-<short-description>
        5. Start implementation!
```

---

## 5. Team Ownership Matrix (M1–M6) Alignment

To guarantee clear responsibility, every issue MUST be assigned to exactly one primary role:

| Member ID | Subsystem Domain | Primary Focus | GitHub Issue Assignment |
| :---: | :--- | :--- | :--- |
| **M1** | AI & Scene Text OCR | PaddleOCR ONNX runtime, CPU int8 quantization, Devanagari translation mappings, text box cropper. | Assigned to OCR / Multilingual parsing issues. |
| **M2** | Calibration & Geometry | Optical scale recovery ($S = 27.0\text{mm} / d_{\text{major}}$), coin/card contour detection, right-cylinder invariance, font stroke measurement. | Assigned to CV, camera geometry, and calibration issues. |
| **M3** | Backend & Rule Engine | FastAPI server, Pydantic schemas, deterministic LMPC state machine (Rules 6, 7, 8, 26), USP math auditor. | Assigned to backend architecture, rules, and calculation issues. |
| **M4** | Frontend & UX | Responsive Vite/React PWA, camera WebRTC viewfinder, 5-state compliance badges, evidence side-by-side viewer. | Assigned to UI, UX, styling, and PWA caching issues. |
| **M5** | Data & Benchmark | Physical packaging dataset curation (35+ SKUs), 1200 DPI ground-truth scans, automated CER/WER evaluation. | Assigned to dataset, benchmarking, and accuracy verification issues. |
| **M6** | Product, DevOps & Governance | Repository governance, GitHub CI/CD workflows, cryptographic SHA-256 PDF report generator, eMaap mock sync adapter. | Assigned to CI/CD, reporting, compliance audit, and repository infrastructure issues. |

---

## 6. Anti-Patterns to Avoid

| Anti-Pattern | Why It Is Dangerous | What Must Happen Instead |
| :--- | :--- | :--- |
| **"Bro, make the OCR thing"** | Informal task via chat; zero scope, untestable, forgotten within 24 hours. | File an official issue using `.github/ISSUE_TEMPLATE/feature.yml` with full context. |
| **Unbounded Scope** | "Implement all LMPC Rules" causes endless branches that cannot be merged before the deadline. | Split into atomic issues: Rule 6 declarations, Rule 6(11) USP, Rule 7 font table, Rule 26 exemptions. |
| **Untestable Criteria** | "Make the calibration good and fast" cannot be proven in a PR review. | "Scale estimation error $< 5\%$ at $<15^\circ$ tilt; execution time $< 100\text{ms}$ on CPU." |
| **Multiple Primary Assignees** | When two people own an issue, nobody owns it. Tasks stall and finger-pointing occurs. | Exactly one primary owner. Add secondary support lead in the secondary field. |
| **Coding Before Ready** | Developing on `status:specifying` issues leads to discarded code and rework. | Keep working on the specification until DoR passes; then branch. |
| **Fabricated Legal Rules** | Inventing statutory requirements from memory invalidates the system before the SIH jury. | Every legal rule MUST cite `METROLENS_LEGAL_SOURCE_PACK/` or `docs/LEGAL_RULE_MATRIX.md`. |

---

## 7. Auditing & Compliance Check

During weekly reviews and before milestone merges, maintainers (M3, M6) audit the repository:
1. Every merged Pull Request MUST link to an approved GitHub Issue.
2. Every closed Issue MUST have its DoR checklist fully marked.
3. Every commit on `main` MUST trace cleanly back to a requirement in [`docs/TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md).

By strictly upholding this Definition of Ready, MetroLens AI guarantees that every teammate operates with absolute clarity, maximum velocity, and zero wasted effort.
