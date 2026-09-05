# CURRENT STATE: MEMBER 2 STATUS DOSSIER
**Generated:** 2026-09-05T17:00:00+05:30
**Role:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement Lead
**Project:** MetroLens AI / Nirikshak (SIH26034)
**Branch:** `member-2`
**Latest Commit:** `0dcd49f` (`feat(calibration): implement deterministic metric anchor detection`)
**Overall Monorepo Status:** 119/119 unit tests passing across all packages

---

## 1. Executive Summary & Ownership Boundary

Member 2 is personally responsible for:
1. Optical pre-flight quality filtering (rejecting blurry, glared, or washed-out images before OCR/rules ingestion).
2. Physical reference anchor detection (RBI standard ₹10 coin and ISO/IEC 7810 ID-1 card).
3. Monocular scale recovery and planar homography perspective rectification ($3 \times 3$ matrix $H$).
4. Physical font height conversion ($h_{\text{mm}} = h_{\text{px}} \times S$) for Rule 7 verification.
5. Cylindrical surface distortion compensation for cans and bottles.

### Strict Scope Boundary ("Not My Job")
- Member 2 does **NOT** run OCR neural networks (owned strictly by Member 1).
- Member 2 does **NOT** evaluate statutory compliance verdicts or legal penalties (owned strictly by Member 3).
- Member 2 does **NOT** write FastAPI endpoints or PDF report generators (owned strictly by Member 4).
- Member 2 does **NOT** build React UI components (owned strictly by Member 5).
- Member 2 does **NOT** deploy CI/CD pipelines (owned strictly by Member 6).

---

## 2. Chronological Phase Delivery Log (Phases 0–4)

### Phase 0: Repository Audit & Package Boundary Enforcement
- **Objective:** Establish isolated package structure and verify zero leaky abstractions across monorepo packages.
- **Actions:** Audited `packages/vision/` and `packages/calibration/`. Enforced clean unidirectional data flow: `apps/` &rarr; `packages/` (packages never import from `apps/` or peer feature packages).
- **Outcome:** Clean workspace ready for distributed multi-developer execution.

### Phase 1: Environment & Interface Contracts Audit
- **Objective:** Establish frozen, strongly typed data transfer objects (DTOs) with zero untyped dictionary dumping grounds.
- **Actions:** Audited package interface seams; eliminated circular dependencies; ensured Python 3.12+ type annotation standard; passed baseline smoke tests.
- **Git Commit:** `8a16ac8`

### Phase 2: Image Quality Gate (`packages/vision`)
- **Objective:** Prevent blurred, saturated, or low-contrast frames from entering downstream pipelines.
- **Deliverables:**
  - `packages/vision/src/nirikshak_vision/quality.py`
  - `packages/vision/src/nirikshak_vision/types.py`
  - `packages/vision/tests/test_quality_gate.py`
- **Algorithms & Criteria:**
  1. **Sharpness Gate:** Laplacian variance $\sigma^2(\nabla^2 I) \ge 100.0$. Rejection code: `ERR_IMAGE_BLUR`.
  2. **Specular Glare Gate:** HSV mask ($V \ge 250, S \le 30$) area percentage $\le 15.0\%$. Rejection code: `ERR_IMAGE_GLARE`.
  3. **Contrast Gate:** Luminance standard deviation $\sigma \ge 20.0$. Rejection code: `ERR_IMAGE_LOW_CONTRAST`.
- **Contract:** Immutable frozen dataclass `QualityGateResult` emitting structured failure codes and actionable user guidance.
- **Performance:** Median execution latency $< 25\text{ms}$ on CPU.
- **Git Commits:** `8a16ac8`, `e23b69a`

### Phase 3: Experimental Calibration Spike Benchmark
- **Objective:** Empirically evaluate whether a circular metric anchor (₹10 coin) can recover physical scale without prior camera calibration.
- **Deliverables:**
  - `scripts/benchmark/spike_calibration.py`
  - `benchmarks/results/spike_calibration_results.json`
  - `benchmarks/reports/spike_calibration_report.md`
- **Experimental Protocol:** 288-scene factorial matrix (8 viewing angles $0^\circ\text{--}45^\circ$, 3 distances $250\text{--}500\text{mm}$, 4 backgrounds, 3 lighting regimes) yielding 1,152 evaluation trials.
- **Key Discoveries & Mathematical Modeling:**
  1. **Major-Axis Invariance:** Major axis of perspective-projected circle is least foreshortened under moderate tilt.
  2. **Error Partitioning:** Major axis achieves **$3.03\%$ mean error** under nominal conditions (clean/diffuse, $\le 15^\circ$ tilt) and **$7.98\%$ mean error** across all combined conditions up to $15^\circ$ tilt.
  3. **Minor-Axis Foreshortening Physics:** Mathematical error of uncorrected minor-axis scale estimation rigorously established as:
     $$\text{Relative Error} = \frac{S_{\text{est}}}{S_{\text{true}}} - 1 = \frac{D / (D\cos\theta)}{Z / f} - 1 = \frac{1}{\cos\theta} - 1$$
- **Git Commit:** `d687975`

### Phase 4: Deterministic Metric Anchor Detection (`packages/calibration`)
- **Objective:** Deterministically detect physical reference anchors (₹10 coin and ISO ID-1 card) without estimating scale or homography.
- **Deliverables:**
  - `packages/calibration/src/nirikshak_calibration/types.py`
  - `packages/calibration/src/nirikshak_calibration/anchor_detector.py`
  - `packages/calibration/src/nirikshak_calibration/__init__.py`
  - `packages/calibration/tests/test_anchor_detector.py`
- **Architectural & Algorithmic Highlights:**
  1. **Algebraic Ellipse Residual:** Normalized mean algebraic distance $\frac{1}{N}\sum |(x'/a)^2 + (y'/b)^2 - 1|$ in rotated coordinate frame.
  2. **Canonical Axis & Angle Normalization:** OpenCV `fitEllipse()` axis swapping when $d_1 < d_2$, adjusting $\theta = (\text{raw\_angle} + 90^\circ)\pmod{180^\circ}$ to guarantee $d_{\text{major}} \ge d_{\text{minor}}$.
  3. **Concentric Ring Pairing:** Outer brass rim ($27.0\text{mm}$) and inner nickel core ($19.6\text{mm}$, ratio $0.726 \pm 0.08$) paired, granting $+0.10$ bonus and absorbing the inner core into `ring_info`.
  4. **Spatial Non-Maximum Suppression (NMS):** Deduplicates coincident boundary strokes within $25\%$ of diameter, eliminating self-induced ambiguity.
  5. **Confidence Gating & Ambiguity Margin:** Hard gate at $0.50$; ambiguity triggered if two distinct candidates are both $\ge 0.50$ and score delta $< 0.08$.
  6. **Score Bounding Guarantee:** All heuristic scores strictly clamped to $[0.0, 1.0]$.
  7. **Testing Evidence:** 32 passing unit tests in `test_anchor_detector.py` covering geometry, tilt, glare, clutter, non-convex shapes, invalid inputs, non-finite floats, and latency ($<50\text{ms}$).
- **Git Commit:** `0dcd49f`

---

## 3. Metric & Testing Status

| Metric Category | Target Budget | Measured Performance | Verification Status |
|:---|:---|:---|:---:|
| **Quality Gate Latency** | $< 50\text{ ms}$ CPU | $\approx 22\text{ ms}$ | ✅ PASS |
| **Anchor Detector Latency** | $< 50\text{ ms}$ CPU | $\approx 28\text{ ms}$ | ✅ PASS |
| **Monorepo Unit Tests** | 100% passing | 119 / 119 passing | ✅ PASS |
| **Calibration Unit Tests** | 100% passing | 32 / 32 passing | ✅ PASS |
| **Diff Hygiene Check** | 0 errors | `git diff --check` clean | ✅ PASS |
| **Working Tree State** | Clean | `git status` clean | ✅ PASS |

---

## 4. Scientific Evidentiary Standard Notice

> [!IMPORTANT]
> **Anti-Hallucination Architectural Policy**:
> - The 32 deterministic automated tests verify software behavior, numerical stability, coordinate transforms, and edge-case handling against synthetic geometric test frames.
> - They do **NOT** certify real-world physical calibration accuracy under uncontrolled smartphone optical distortion.
> - Real-world physical accuracy remains strictly **PENDING** until Member 6 (QA Lead) acquires physical packaging specimens and 1200 DPI flatbed optical scans for ground-truth verification.

---

## 5. Next Steps: Phase 5 Roadmap

- **Phase 5 Target:** Planar Homography & Perspective Rectification (`packages/calibration/homography.py`).
- **Input:** `AnchorDetectionResult` from Phase 4.
- **Core Responsibilities:**
  1. Compute $3 \times 3$ planar homography matrix $H$ using card 4-corner correspondences or circular coin projection.
  2. Compute perspective-corrected metric scale factor $S = \text{mm/pixel}$.
  3. Generate top-down orthorectified declaration panel image crop for Member 1 OCR.
- **Phase Boundary:** Do **NOT** measure font heights or evaluate statutory rules in Phase 5.
