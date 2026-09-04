# INDIVIDUAL WORK PLAN: MEMBER 2
# Computer Vision, Optical Calibration & Physical Measurement Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Packages:** `packages/vision/`, `packages/calibration/` | **Secondary Role:** Data Ground Truth Sourcing

---

## 1. Member Role
**Member 2 — Computer Vision, Optical Calibration & Geometric Measurement Lead**

---

## 2. Mission
Solve the fundamental monocular scale ambiguity of smartphone camera uploads and deliver mathematically verifiable physical measurements. Member 2 is personally responsible for rejecting unusable packaging uploads via optical pre-flight quality filters (Laplacian blur $<100$ and HSV specular glare $>15\%$), detecting coplanar metric reference anchors (standard ₹10 coin or ISO card), recovering the metric scale factor ($S$ in mm/pixel) with $< 5.0\%$ error up to $15^\circ$ tilt, unwarping perspective distortion via planar homography ($3 \times 3$ matrix $H$), and calculating calibrated physical numeral stroke heights ($h_{\text{mm}} = h_{\text{px}} \times S$) with Mean Absolute Error (MAE) $< 0.15\text{mm}$ against 1200 DPI ground truth.

---

## 3. Ownership

### Primary Ownership:
- `packages/vision/quality.py`: Image pre-flight gate (Laplacian blur variance, HSV specular glare mask, contrast check).
- `packages/calibration/anchor_detector.py`: Ellipse fitting and contour detection for RBI standard ₹10 coin ($27.0\text{mm}$) and rectangular ISO/IEC 7810 ID-1 card ($85.60 \times 53.98\text{mm}$).
- `packages/calibration/homography.py`: Planar perspective rectification ($3 \times 3$ matrix $H$) generating orthorectified declaration panel crops.
- `packages/calibration/cylinder.py`: Right-cylinder vertical generator strip invariance module ($\cos\phi \ge 0.94$).
- `packages/calibration/font_measurer.py`: Mathematical conversion of OCR bounding boxes to calibrated physical millimeter heights ($h_{\text{mm}}$).
- `tests/unit/test_calibration.py` & `tests/unit/test_quality_gate.py`: Geometric unit test suite.

### Secondary Support:
- Support **Member 6 (QA Lead)** in acquiring physical packaging specimens and conducting flatbed optical scans for ground truth.
- Support **Member 5 (Frontend Lead)** with manual 2-point caliper scale override coordinates on the interactive web canvas.

---

## 4. Concrete Responsibilities
1. Implement high-speed ($< 50\text{ms}$) pre-flight quality filter in OpenCV:
   - Compute variance of Laplacian; reject frames with score $< 100$ with actionable advice: *"Image too blurry. Please stabilize your camera."*
   - Compute HSV specular saturation mask; reject frames with glare covering $> 15\%$ of the central panel with advice: *"Specular glare detected. Please angle light source away from shiny packaging foil."*
2. Detect the circular bimetallic ₹10 coin outer boundary via adaptive thresholding, morphological closing, and OpenCV `cv2.fitEllipse()`.
3. Compute metric scale factor $S = \frac{27.0\text{ mm}}{d_{\text{major}}\text{ px}}$ along the ellipse major axis (which remains invariant under perspective tilt up to $15^\circ$).
4. Implement ISO card 4-corner detection and compute planar homography matrix $H$ using `cv2.getPerspectiveTransform()` as a high-precision alternative anchor.
5. Apply homography unwarping to generate orthorectified, top-down planar crops of the declaration panel for Member 1's OCR engine.
6. Implement right-cylinder vertical generator strip projection for cans and bottles: measure numeral heights strictly along the vertical axis of minimum curvature where geometric distortion $\le 6\%$.
7. Convert pixel bounding boxes into millimeter font heights: $h_{\text{mm}} = h_{\text{px}} \times S$.
8. Implement graceful degradation: if no coin or card is detected, set `is_calibrated: false`, emit `scale_factor: null`, and allow text compliance rules to proceed while flagging font height checks as `NOT_IMAGE_VERIFIABLE`.

---

## 5. What Member 2 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Checking whether a measured $1.2\text{mm}$ numeral violates Rule 7 Table-I/II (owned strictly by Member 3).
- **NOT MY JOB:** Running OCR neural models or recognizing text strings (owned strictly by Member 1).
- **NOT MY JOB:** Developing FastAPI endpoints or multipart upload parsers (owned strictly by Member 4).
- **NOT MY JOB:** Designing React UI buttons or canvas overlays (owned strictly by Member 5).
- **NOT MY JOB:** Deploying Docker containers or writing GitHub Actions (owned strictly by Member 6).

---

## 6. Inputs Received
- **From API Gateway / Member 4:** Sanitized in-memory image array (`numpy.ndarray` in BGR/RGB).
- **From Member 1 (OCR):** Numeral bounding box coordinates and pixel heights ($h_{\text{px}}$).
- **From Member 6 (QA):** Calibration millimeter grid images, 15-SKU Day 1 test set, and physical caliper measurements.
- **Specification:** RBI ₹10 Coin outer diameter ($27.0\text{mm}$), ISO/IEC 7810 ID-1 standard ($85.60 \times 53.98\text{mm}$).

---

## 7. Concrete Outputs Delivered
- `packages/vision/quality.py`: Pre-flight image quality validator.
- `packages/calibration/`: Complete metric calibration, unwarping, and font height measurement suite.
- `MetricScaleResult` Dictionary: Emitted JSON structure containing $S$ (mm/px), detected anchor type, tilt angle, and rectified crops.
- `tests/unit/test_calibration.py`: Unit tests verifying scale accuracy within $5.0\%$ across 10 tilted test cases.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **Sanitized Image Array** | Member 4 | Raw NumPy array from upload ingestion | Day 1, 4:00 PM | Load local test images directly from `tests/fixtures/` using `cv2.imread()`. |
| **Millimeter Calibration Grid** | Member 6 | Baseline verification of scale factor $S$ | Day 1, 2:00 PM | Print standard 1mm grid sheet on office laser printer; verify with caliper. |
| **OCR Numeral BBoxes** | Member 1 | Pixel heights ($h_{\text{px}}$) for physical conversion | Day 2, 2:00 PM | Use mock bounding boxes defined in `tests/fixtures/mock_ocr_tokens.json`. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: Risk Spike — Prove Optical Metric Scale Recovery
- **Goal:** Prove ₹10 coin ellipse detection recovers $27.0\text{mm}$ diameter with $< 5.0\%$ error under $0^\circ\text{--}15^\circ$ tilt.
- **Tasks:** Set up OpenCV 4.x pipeline; write `scripts/benchmark/spike_calibration.py`; photograph ₹10 coin on 5 background surfaces at $0^\circ, 10^\circ, 20^\circ$ tilt; evaluate major-axis vs minor-axis scale.
- **Deliverables:** Standalone calibration script with documented error table across 10 trials.
- **Expected Time:** 7 hours.
- **Dependencies:** Physical ₹10 coin + digital caliper.
- **Checkpoint (Gate 1 - T+24h):** Scale recovery error $\le 5.0\%$ at $\le 15^\circ$ tilt verified against millimeter grid.
- **Risk:** Coin contour detection fails on dark wooden tables or patterned tablecloths.
- **Fallback:** Implement color segmentation in HSV for the brass-nickel outer ring of the ₹10 coin; add ISO card fallback.

### DAY 2: Quality Gate (Blur & Glare) & Vertical Slice 0 Support
- **Goal:** Deliver pre-flight quality filter and connect calibration to headless CLI pipeline.
- **Tasks:** Implement Laplacian variance blur filter ($< 100$ threshold); implement HSV glare saturation detector ($> 15\%$ area threshold); connect module into Vertical Slice 0 runner with Member 4.
- **Deliverables:** `packages/vision/quality.py` and passing unit tests in `tests/unit/test_quality_gate.py`.
- **Expected Time:** 6 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 2 - T+48h):** Vertical Slice 0 correctly accepts clear packaging and rejects artificially blurred images.
- **Risk:** Glare filter rejects shiny metallic pouches that are still readable.
- **Fallback:** Restrict glare analysis to the central $60\%$ region of interest.

### DAY 3: Planar Homography Unwarping ($3 \times 3$ Matrix $H$)
- **Goal:** Unwarp perspective tilt on packaging panels to produce orthorectified crops.
- **Tasks:** Implement ISO card 4-point corner detection; calculate homography matrix $H$ via `cv2.getPerspectiveTransform()`; apply `cv2.warpPerspective()`; generate rectified crops for Member 1's OCR.
- **Deliverables:** `packages/calibration/homography.py` with visual before/after unwarping verification.
- **Expected Time:** 7 hours.
- **Dependencies:** Card packaging test images from Member 6.
- **Checkpoint:** Orthorectified crops show zero angular distortion on rectangular packaging borders.
- **Risk:** Finding 4 corners of an ATM card fails under bad lighting.
- **Fallback:** Fall back to 10-Rupee coin single-scale affine unwarping.

### DAY 4: Right-Cylinder Vertical Generator Invariance Module
- **Goal:** Enable font height measurement on cylindrical cans and bottles.
- **Tasks:** Codify right-cylinder optical physics: identify vertical centerline of cylinder; project characters along vertical generator line where curvature distortion is negligible ($\cos\phi \ge 0.94$ within $\pm 20^\circ$ of center).
- **Deliverables:** `packages/calibration/cylinder.py` passing cylindrical test suite.
- **Expected Time:** 6 hours.
- **Dependencies:** 5 cylindrical beverage cans / bottles from Member 6.
- **Checkpoint:** Font height error on vertical text on a Coca-Cola can is $< 0.15\text{mm}$.
- **Risk:** Tapered or conical bottles distort vertical generator lines.
- **Fallback:** Flag non-standard tapered shapes as `MANUAL_REVIEW_REQUIRED — Non-Planar Curvature`.

### DAY 5: Numeral Stroke Height Measurement & Manual Override Fallback
- **Goal:** Convert OCR bounding boxes to verified physical heights ($h_{\text{mm}}$) and build 2-point manual caliper fallback.
- **Tasks:** Implement `font_measurer.py`: $h_{\text{mm}} = h_{\text{px}} \times S$; calculate Principal Display Panel (PDP) area in $\text{cm}^2$; build 2-point manual distance calculator for Member 5's web canvas.
- **Deliverables:** `font_measurer.py` passing unit tests with mock OCR bounding boxes.
- **Expected Time:** 6 hours.
- **Dependencies:** `OCRToken` bounding boxes from Member 1.
- **Checkpoint:** Measured font heights match physical caliper values within $\pm 0.15\text{mm}$ on 10 test packs.
- **Risk:** OCR bounding box includes whitespace padding, inflating $h_{\text{px}}$.
- **Fallback:** Apply vertical histogram projection profile across the cropped token to measure true ink stroke height.

### DAY 6: Formal Ground-Truth Calibration Benchmark
- **Goal:** Benchmark font height measurement accuracy against 1200 DPI flatbed optical ground truth.
- **Tasks:** Collaborate with Member 6 to run font height evaluation across 35 physical SKUs; compute Mean Absolute Error (MAE); analyze error distributions.
- **Deliverables:** `benchmarks/results/calibration_accuracy.json` proving $\text{MAE} < 0.15\text{mm}$.
- **Expected Time:** 6 hours.
- **Dependencies:** 1200 DPI ground-truth dataset from Member 6.
- **Checkpoint (Gate 6):** Font height MAE $\le 0.15\text{mm}$ validated across all planar benchmark packages.
- **Risk:** Flexible foil pouches with wrinkles produce local scale variance.
- **Fallback:** Document packaging deformation limitation; flag packages with surface wrinkling as `MANUAL_REVIEW_REQUIRED`.

### DAY 7: Edge-Case Hardening, Robustness Testing & API Stability
- **Goal:** Guarantee vision pipeline never crashes regardless of malformed image inputs.
- **Tasks:** Fuzz calibration pipeline with extreme aspect ratios, inverted images, completely dark frames, and non-packaging photos; verify graceful fallback (`is_calibrated: false`).
- **Deliverables:** Robustness test suite in `tests/unit/test_vision_robustness.py`.
- **Expected Time:** 5 hours.
- **Dependencies:** None.
- **Checkpoint:** 100 corrupt/odd images processed with zero unhandled exceptions.
- **Risk:** Unhandled OpenCV `cv2.error` exception crashes the process.
- **Fallback:** Wrap all OpenCV operations in comprehensive try/except blocks returning structured fallback results.

### DAY 8: Code Freeze & Technical Architecture Defense
- **Goal:** Lock vision code; write computer vision methodology for technical jury.
- **Tasks:** Freeze `packages/vision/` and `packages/calibration/`; document coin detection math and cylinder projection formulas in `docs/05_AI_VISION/`; prepare physical caliper for jury table.
- **Deliverables:** Clean, frozen code; technical writeup; physical demo props ready.
- **Expected Time:** 4 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Zero open PRs; all tests passing.

### DAY 9: Buffer Day & Live Demonstration Support
- **Goal:** Support live stage demonstration.
- **Tasks:** Assist presenter with physical prop positioning on jury table; ensure lighting on the table avoids harsh specular glare; assist with jury Q&A on optical physics.
- **Expected Time:** As needed.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | OpenCV 4.x installed & working | `python -c "import cv2; print(cv2.__version__)"` succeeds | Fix local environment / virtualenv |
| **CP-1** | T+24h | Coin calibration spike functional | Scale error $< 5.0\%$ at $\le 15^\circ$ tilt on millimeter grid | Add ISO card fallback |
| **CP-2** | T+48h | Quality gate integrated into CLI | Rejects blurred images (Laplacian $<100$); passes clean packs | Adjust blur threshold to 80 |
| **CP-3** | Day 3 | Planar homography unwarper ready | Top-down rectified crops generated with zero perspective skew | Fall back to affine bounding box crop |
| **CP-4** | Day 5 | Font stroke measurer functional | Measured $h_{\text{mm}}$ matches caliper within $\pm 0.15\text{mm}$ | Apply ink-stroke histogram profiling |
| **CP-5** | Day 7 | 35-SKU calibration benchmark locked | $\text{MAE} < 0.15\text{mm}$ across ground truth | Document planar constraint; use review buffer |
| **CP-6** | Day 8 | Final code freeze | 100% tests green; zero OpenCV crashes on fuzz tests | Revert unverified changes |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **Blur Gate** | Flags image as blurry if Laplacian variance $< 100$ | `pytest tests/unit/test_quality_gate.py` | Unit test report verifying rejection of synthetic blurred frames |
| **Glare Gate** | Flags image if specular saturation covers $> 15\%$ | `pytest tests/unit/test_quality_gate.py` | Test report verifying glare detection on metallic foil images |
| **Scale Recovery** | Scale factor $S$ error $< 5.0\%$ vs RBI coin standard | `pytest tests/unit/test_calibration.py` | Calibration benchmark logs recording error percentages |
| **Font Measurement** | Numeral height MAE $< 0.15\text{mm}$ vs 1200 DPI scan | `pytest tests/benchmarks/test_calibration_benchmark.py` | Comparison table of optical vs flatbed scanned heights |
| **Graceful Fallback**| If coin absent, returns `is_calibrated: false` | `pytest tests/unit/test_calibration_fallback.py` | Pipeline runs to completion without error; flags scale as null |

---

## 12. Testing Responsibility
- **Unit Tests:** `tests/unit/test_calibration.py` (coin detection, card homography, scale computation).
- **Quality Gate Tests:** `tests/unit/test_quality_gate.py` (blur variance, glare mask, low contrast).
- **Integration Tests:** `tests/integration/test_calibration_to_rules.py` (verifies $S$ and font heights feed correctly to Member 3's rule engine).
- **Edge Cases:** Specular reflections on aluminum cans, dark backgrounds matching coin edges, extreme angles ($> 30^\circ$).
- **Failure Cases:** Uploading screenshots, photos of cars, completely blank white images (must return `is_calibrated: false` without throwing exceptions).

---

## 13. Handoff Protocol & Checklist

### Handoff to Member 1 (OCR), Member 3 (Rule Engine) & Member 4 (Backend API):
1. **Working Packages:** `packages/vision/` and `packages/calibration/`.
2. **Standard Output:** `MetricScaleResult` matching schema in `docs/API_CONTRACT.md`.
3. **Usage Documentation:**
   ```python
   from packages.vision.quality import check_image_quality
   from packages.calibration.anchor_detector import detect_metric_anchor
   from packages.calibration.font_measurer import measure_numeral_heights

   quality_pass, quality_reason = check_image_quality(image_np)
   scale_result = detect_metric_anchor(image_np)
   # returns MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.045, ...)
   ```
4. **Test Evidence:** Passing pytest execution log across all calibration test suites.
5. **Known Limitations:** Accurate automatic calibration requires surface tilt $\le 15^\circ$; extreme wrinkles on pouches require manual review.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** OpenCV contour detection crashing on specific image format $\rightarrow$ Consult Member 6 (DevOps) for NumPy/OpenCV version mismatch.
- **Blocked for 2 hours:** Scale recovery error exceeding $8\%$ on coin $\rightarrow$ Escalate to Member 3 (Rule Architect) to discuss prioritizing ISO card anchor.
- **Blocked for half-day:** Homography unwarping generating distorted crops $\rightarrow$ Trigger team triage; fall back to simple rotated bounding box crops without full perspective warp.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Coin Detection Fails on Dark Surface** | High | High | Ellipse fit error $> 8\%$ | Add ISO card ($85.60 \times 53.98\text{mm}$) rectangular corner detector | UI 2-point manual caliper scale override on canvas |
| **Glare Washes Out Package Text** | Med | Med | HSV saturation $> 15\%$ | Pre-flight rejection alert: "Tilt camera away from glare" | Adaptive CLAHE contrast enhancement |
| **Cylindrical Packaging Curvature** | Med | High | Compressed text boxes | Measure strictly along central vertical generator ($\cos\phi \ge 0.94$) | Flag as `MANUAL_REVIEW_REQUIRED — Curvature` |
| **Wrinkled Packaging Pouches** | High | Low | Inconsistent local scale | Compute scale at anchor plane; use review tolerance buffer | Route to Inspector Review toggle |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 2 DAILY STATUS (DATE: ________)
• DONE: [Algorithms implemented and tests passing]
• BLOCKED: [Any optical or CV blockers > 30 mins]
• TESTED: [Scale accuracy numbers / test commands]
• NEXT: [Tomorrow's geometric milestone]
• RISK: [Any concerns regarding lighting or surface physics]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. Python code is fully typed and implemented in `packages/vision/` and `packages/calibration/`.
2. Unit tests verify scale recovery error $< 5.0\%$ on test fixtures.
3. Quality gate rejects blurred and high-glare images with descriptive error messages.
4. Scale result validates against `MetricScaleResult` schema.
5. Integration confirmed with Member 1, Member 3, and Member 4.

---

## 18. AI Coding Workflow
$$\text{PLAN (Derive geometric equations)} \longrightarrow \text{PROMPT AI (OpenCV syntax)} \longrightarrow \text{REVIEW (Coordinate frame bounds)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Write boilerplate OpenCV matrix operations, contour sorting, and unit test mocks.
- **MEMBER MUST DECIDE:** Geometric projection formulas, error tolerance thresholds, anchor physical dimensions, and camera physics constraints.

---

## 19. Buffer Work
- **Primary:** Pre-flight filter, coin ellipse scale recovery, ISO card homography, font height measurer, 35-SKU accuracy benchmark.
- **Buffer Task 1:** Implement automatic Principal Display Panel (PDP) contour boundary segmentation for rectangular cartons.
- **Buffer Task 2:** Fine-tune ellipse eccentricity filtering to automatically calculate camera perspective tilt angle.
