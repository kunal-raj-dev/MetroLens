# INDIVIDUAL WORK PLAN: MEMBER 1
# AI & Multilingual OCR Pipeline Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Package:** `packages/ocr/` | **Secondary Role:** Backend OCR Service Integration

---

## 1. Member Role
**Member 1 — AI, Multilingual OCR & Scene Text Extraction Lead**

---

## 2. Mission
Deliver an ultra-reliable, high-accuracy scene text extraction engine running entirely on server CPU using Direct ONNX Runtime (`onnxruntime==1.29.0`) with `PP-OCRv3-ROUTED` architecture. Member 1 is personally responsible for detecting text polygons, isolating character bounding boxes, performing multilingual recognition (English alphanumeric + Devanagari Hindi via script routing), filtering low-confidence predictions, and emitting standardized character-level tokens in $< 800\text{ms}$ with a Character Error Rate (CER) target $< 6.0\%$ across the upcoming 35-SKU benchmark dataset, with zero dependence on external cloud AI APIs or unsupported third-party wrappers.

---

## 3. Ownership

### Primary Ownership:
- `packages/ocr/src/nirikshak_ocr/engine.py`: `OCREngine` facade and stage timing orchestration.
- `packages/ocr/src/nirikshak_ocr/detector.py`: DBNet++ text detector running direct ONNX inference (`ch_PP-OCRv3_det_infer.onnx`).
- `packages/ocr/src/nirikshak_ocr/recognizer.py`: SVTR text recognizer with greedy CTC decoding for Latin (`ch_PP-OCRv3_rec_infer.onnx`) and Devanagari (`rec.onnx`).
- `packages/ocr/src/nirikshak_ocr/router.py`: `ScriptRouter` heuristic confidence-gated script routing.
- `packages/ocr/src/nirikshak_ocr/preprocessing.py`: Multiples-of-32 resizing, ImageNet normalization, coordinate unscaling, and `ImagePreprocessHook`.
- `packages/ocr/src/nirikshak_ocr/types.py`: `OCRToken`, `OCRResult`, and `to_observation()` adapter.
- `packages/ocr/src/nirikshak_ocr/utils.py`: Perspective cropping, clockwise quadrilateral ordering, and reading-order sorting.
- `tests/unit/test_ocr_*.py`: OCR unit tests, offline execution validation, and synthetic fixture tests.
- `benchmarks/ocr/chunk2/`: Multi-thread CPU sweep, latency profiling, and memory stability harness.

### Secondary Support:
- Support **Member 4 (Backend)** in integrating the OCR engine into `apps/api/services/ocr_service.py`.
- Support **Member 3 (Rule Engine)** with raw text token bounding boxes and observations.

---

## 4. Concrete Responsibilities
1. Maintain and execute pre-trained PP-OCRv3 models (`ch_PP-OCRv3_det_infer.onnx`, `ch_PP-OCRv3_rec_infer.onnx`, `rec.onnx`) via direct `onnxruntime==1.29.0` with `CPUExecutionProvider`.
2. Implement optimized single-image batch inference with OpenMP / intra-op thread tuning (`intra_op_num_threads=4`) to enforce a sub-800ms CPU execution cap (empirically measured median ~107ms).
3. Extract rotated 4-point bounding polygons and calculate raw quadrilateral pixel height (`raw_pixel_height`) for every extracted numeral (explicitly decoupled from physical mm legal font height).
4. Filter background packaging noise by enforcing a strict token confidence review threshold ($c \ge 0.60$).
5. Route text crops to specialized Latin or Devanagari recognizers via confidence-gated routing.
6. Support future domain preprocessing hooks (`ImagePreprocessHook`) for dot-matrix inkjet expiration stamps.
7. Benchmark Character Error Rate (CER) across ground-truth crops when provided by Member 6.

---

## 5. What Member 1 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Deciding whether an extracted Net Quantity or MRP violates Legal Metrology Rules (owned strictly by Member 3).
- **NOT MY JOB:** Writing regex extraction rules for canonical Pydantic models (owned strictly by Member 3).
- **NOT MY JOB:** Computing optical metric scale factor $S$ or detecting coin/card reference anchors (owned strictly by Member 2).
- **NOT MY JOB:** Building React upload dropzones or UI bounding box viewers (owned strictly by Member 5).
- **NOT MY JOB:** Deploying Docker containers or configuring CI/CD pipelines (owned strictly by Member 6).

---

## 6. Inputs Received
- **From Member 2 (CV/Calib):** Rectified image crops (`numpy.ndarray`) and optical pre-flight quality confirmation.
- **From Member 3 (Legal):** Statutory keyword checklist (English & Hindi) for priority detection focus.
- **From Member 6 (QA):** 15-SKU Day 1 test images and 35-SKU ground-truth text annotations.
- **Specification:** `docs/API_CONTRACT.md` (`OCRToken` schema).

---

## 7. Concrete Outputs Delivered
- `packages/ocr/`: Fully tested, local, quantized ONNX scene text extraction pipeline.
- `OCRToken` Dictionary Stream: Standardized list of tokens with coordinates and confidences.
- `tests/benchmarks/test_ocr_benchmark.py`: Automated CER evaluation script.
- `benchmarks/results/ocr_performance.json`: Measured latency and CER on real test packaging.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **Rectified Packaging Image** | Member 2 | Perspective-unwarped crop for accurate font OCR | Day 2, 2:00 PM | Use raw unrectified image directly; apply local affine approximation. |
| **15-SKU Ground-Truth Data** | Member 6 | Verification of CPU latency and CER | Day 1, 6:00 PM | Use 5 synthetic generated packaging images (`tests/fixtures/sample_packages/`). |
| **Pydantic Token Schema** | Member 3 | Target schema definition for extracted tokens | Day 1, 12:00 PM | Use frozen `OCRToken` schema from `docs/API_CONTRACT.md`. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: Risk Spike — Prove Local ONNX Inference on CPU
- **Goal:** Prove PaddleOCR ONNX executes on consumer laptop CPU in $< 1,200\text{ms}$ with $\text{CER} < 8\%$.
- **Tasks:** Set up `onnxruntime`; download PaddleOCR v4 mobile weights; write headless inference test script `scripts/benchmark/spike_ocr_cpu.py`; run on 5 sample packaging images.
- **Deliverables:** Working standalone script emitting raw text and latency timings.
- **Expected Time:** 6 hours.
- **Dependencies:** Sample packaging images from `tests/fixtures/`.
- **Checkpoint (Gate 1 - T+24h):** CPU inference $\le 1,200\text{ms}$ verified on host hardware.
- **Risk:** High latency ($> 2.0\text{s}$) on CPU.
- **Fallback:** Downsample input images to max dimension $1280\text{px}$; restrict detection area.

### DAY 2: Bounding Box Extraction & Vertical Slice 0 Support
- **Goal:** Extract rotated bounding boxes, character heights ($h_{\text{px}}$), and wire into Vertical Slice 0.
- **Tasks:** Implement polygon-to-box conversion; compute numeral pixel heights; emit `OCRToken` list matching `docs/API_CONTRACT.md`; collaborate with Member 4 on CLI runner.
- **Deliverables:** `packages/ocr/engine.py` and passing `test_ocr_engine.py`.
- **Expected Time:** 7 hours.
- **Dependencies:** None (self-contained).
- **Checkpoint (Gate 2 - T+48h):** Vertical Slice 0 CLI processes sample image and prints valid tokens.
- **Risk:** Inaccurate bounding box coordinates on angled text.
- **Fallback:** Clamp bounding boxes to image boundaries; use minimum area rotated rectangles.

### DAY 3: Multilingual Recognition (Hindi Devanagari) & Keyword Tuning
- **Goal:** Validate bilingual recognition of statutory terms across English and Hindi.
- **Tasks:** Integrate multilingual recognition dict; write keyword normalization mapping (`अधिकतम खुदरा मूल्य` $\rightarrow$ `MRP`, `निवल मात्रा` $\rightarrow$ `Net Qty`); test on 10 bilingual retail packs.
- **Deliverables:** `packages/ocr/multilingual.py` passing bilingual unit tests.
- **Expected Time:** 6 hours.
- **Dependencies:** Bilingual sample images from Member 6.
- **Checkpoint:** Correctly extracts `MRP` and `Net Qty` from 5 bilingual packages.
- **Risk:** Devanagari character recognition accuracy drops below $80\%$.
- **Fallback:** Rely on mandatory English declarations (Rule 8 mandates English or Hindi; interstate goods include English).

### DAY 4: Image Preprocessing Pipeline & Noise Filters
- **Goal:** Improve text clarity on noisy, low-contrast, or metallic packaging wrappers.
- **Tasks:** Implement `packages/ocr/preprocessor.py`: contrast-limited adaptive histogram equalization (CLAHE), bilateral denoising, and unsharp masking.
- **Deliverables:** Preprocessing filter module with automated before/after quality comparisons.
- **Expected Time:** 6 hours.
- **Dependencies:** Noisy packaging images from Member 6.
- **Checkpoint:** CER improves by $\ge 15\%$ on metallic foil test cases.
- **Risk:** Preprocessing adds $> 300\text{ms}$ latency.
- **Fallback:** Apply preprocessing selectively only if raw image contrast is $< 40$.

### DAY 5: Dot-Matrix Inkjet & Expiration Stamp Edge-Case Handling
- **Goal:** Solve dot-matrix expiration and batch date parsing failures.
- **Tasks:** Implement morphological dilation filter specifically targeting fragmented inkjet dots on package crimps; tune character segmentation.
- **Deliverables:** Inkjet date detection module with test suite.
- **Expected Time:** 5 hours.
- **Dependencies:** Faded inkjet sample images.
- **Checkpoint:** Correctly parses date on 4 out of 5 dot-matrix test packages.
- **Risk:** Dot-matrix dates remain fragmented.
- **Fallback:** Emit token with flag `is_faded_inkjet: true` and route to Member 3 for `MANUAL_REVIEW_REQUIRED`.

### DAY 6: Formal 35-SKU Benchmark Execution & Tuning
- **Goal:** Measure Character Error Rate (CER) and Word Error Rate (WER) on full 35-SKU dataset.
- **Tasks:** Run `tests/benchmarks/test_ocr_benchmark.py` across all 35 ground-truth SKUs with Member 6; profile CPU bottlenecks; tune thread count.
- **Deliverables:** `benchmarks/results/ocr_benchmark_report.json` showing $\text{CER} < 6.0\%$.
- **Expected Time:** 6 hours.
- **Dependencies:** Complete 35-SKU ground truth from Member 6.
- **Checkpoint (Gate 6):** Formal benchmark locked with zero fabricated figures.
- **Risk:** CER on small pouches exceeds $6.0\%$.
- **Fallback:** Optimize crop resolution on small text ROIs.

### DAY 7: Memory Profiling, Model Caching & Integration Hardening
- **Goal:** Guarantee zero memory leaks and fast warm-start inference in FastAPI.
- **Tasks:** Profile memory footprint under 50 consecutive inference calls; verify memory stays $< 450\text{MB}$; verify model weights remain warm in RAM.
- **Deliverables:** Leak-free OCR service integration in `apps/api/`.
- **Expected Time:** 5 hours.
- **Dependencies:** FastAPI backend from Member 4.
- **Checkpoint:** 50 consecutive requests execute with zero memory growth and latency $< 800\text{ms}$.
- **Risk:** RAM usage balloons under repeated calls.
- **Fallback:** Explicitly invoke Python garbage collector `gc.collect()` after each session.

### DAY 8: Code Freeze & Technical Documentation for Jury
- **Goal:** Lock all OCR code; write technical jury defense documentation.
- **Tasks:** Freeze `packages/ocr/`; write architecture explainability section in `docs/05_AI_VISION/`; participate in jury Q&A drills.
- **Deliverables:** Frozen code, passing tests, and jury Q&A notes.
- **Expected Time:** 4 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Zero open PRs; all tests green.

### DAY 9: Buffer Day & Live Demo Support
- **Goal:** Support live demo execution and stagecraft rehearsals.
- **Tasks:** Stand by during 3-minute pitch rehearsals; assist with live camera capture lighting; handle emergency bugfixes if triggered.
- **Expected Time:** As needed.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | ONNX models downloaded & verified | File hashes match official PaddleOCR release | Re-download via verified mirror |
| **CP-1** | T+24h | CPU inference script executes | Latency $\le 1200\text{ms}$, $\text{CER} < 8\%$ on 5 packs | Downsample input image to $1280\text{px}$ |
| **CP-2** | T+48h | Bounding box token generator ready | Vertical Slice 0 CLI prints valid `OCRToken` list | Clamp bounding boxes to image frame |
| **CP-3** | Day 3 | Multilingual Hindi parser works | Correctly reads Devanagari MRP on 5 packs | Drop Hindi; enforce English-only |
| **CP-4** | Day 5 | Preprocessing & dot-matrix tuning | Passes 8 difficult foil/inkjet cases | Flag difficult cases as `MANUAL_REVIEW` |
| **CP-5** | Day 7 | 35-SKU benchmark passes DoD | $\text{CER} < 6.0\%$, Latency $< 800\text{ms}$ documented | Profile thread pool; document limitations |
| **CP-6** | Day 8 | Final code freeze | Zero failing tests; git branch locked | Revert last unverified change |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **ONNX Runtime** | Ingests image, emits tokens in $< 800\text{ms}$ on CPU | `pytest tests/unit/test_ocr_engine.py` | Terminal test report: 100% pass, runtime $< 800\text{ms}$ |
| **Token Accuracy** | Character Error Rate $< 6.0\%$ on 35 SKUs | `pytest tests/benchmarks/test_ocr_benchmark.py` | Generated JSON report with exact CER percentages |
| **Token Schema** | Emits fields conforming 100% to `OCRToken` | `pytest tests/unit/test_ocr_schema.py` | Pydantic validation passes with zero schema errors |
| **Memory Ceiling** | Process RSS memory $< 500\text{MB}$ during 50 runs | `python scripts/benchmark/profile_memory.py` | Memory trace log showing flat line after warm-up |

---

## 12. Testing Responsibility
- **Unit Tests:** `tests/unit/test_ocr_engine.py` (model loading, image input formats, token generation).
- **Integration Tests:** `tests/integration/test_ocr_to_normalizer.py` (verifies tokens pass seamlessly to M3 normalizer).
- **Edge Cases:** Rotated packaging ($90^\circ, 180^\circ$), metallic foil glare, crumpled pouches, faded dot-matrix printing.
- **Failure Cases:** Blank images, pure white frames, images with no text (must return empty token list gracefully without 500 error).

---

## 13. Handoff Protocol & Checklist

### Handoff to Member 3 (Rule Engine) & Member 4 (Backend API):
1. **Working Module:** `packages/ocr/` installable via local package or import.
2. **Standard Output:** `List[OCRToken]` matching schema in `docs/API_CONTRACT.md`.
3. **Usage Documentation:** Single-line invocation:
   ```python
   from packages.ocr.engine import OCREngine
   engine = OCREngine()
   tokens = engine.extract_tokens(image_np)
   ```
4. **Test Evidence:** Attached test log showing 100% passing tests on `tests/unit/test_ocr_engine.py`.
5. **Known Limitations:** Text smaller than $12\text{px}$ stroke height has degraded CER; dot-matrix text flagged for review.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** Cannot load ONNX model or OpenCV DLL $\rightarrow$ Ping Member 6 (DevOps) for environment check.
- **Blocked for 2 hours:** Latency exceeds $1,500\text{ms}$ on CPU $\rightarrow$ Escalate to Member 3 (Backend) to discuss resolution downsampling.
- **Blocked for half-day:** OCR accuracy catastrophically failing on benchmark $\rightarrow$ Trigger team triage; evaluate reducing benchmark scope to clear printed panels.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **CPU Latency $> 1,200\text{ms}$** | Med | High | Inference timer logs | Quantize to ONNX int8; tune OpenMP threads | Resize image to $1280\text{px}$ before OCR |
| **Devanagari OCR Errors** | Med | Med | CER on Hindi $> 15\%$ | Add Hindi keyword dictionary lookup | Fall back to mandatory English declarations |
| **Inkjet Date Failure** | High | Low | Date missing from tokens | Apply morphological dilation filter | Mark Rule 6(1)(d) as `MANUAL_REVIEW` |
| **Memory Bloat in Uvicorn** | Low | High | Server RAM $> 1\text{GB}$ | Avoid re-instantiating ONNX session | Singleton session pattern + manual `gc.collect()` |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 1 DAILY STATUS (DATE: ________)
• DONE: [What was built and committed today]
• BLOCKED: [Any technical blockers > 30 mins]
• TESTED: [Test commands run and pass rates]
• NEXT: [Tomorrow's primary milestone]
• RISK: [Any emerging performance or accuracy concern]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. Python code is written with full type annotations in `packages/ocr/`.
2. Unit tests pass with $\ge 90\%$ branch coverage.
3. Latency is measured at $< 800\text{ms}$ on CPU demo hardware.
4. Extracted tokens validate against `OCRToken` Pydantic schema.
5. Handshake is verified with Member 3 and Member 4.

---

## 18. AI Coding Workflow
$$\text{PLAN (Define inputs/outputs)} \longrightarrow \text{PROMPT AI (Boilerplate)} \longrightarrow \text{REVIEW (Memory \& types)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Generate OpenCV filter boilerplate, numpy array manipulation, and pytest parameterization.
- **MEMBER MUST DECIDE:** Model selection, confidence thresholds, bounding box coordinate math, and final accuracy sign-off.

---

## 19. Buffer Work
- **Primary:** PaddleOCR ONNX CPU pipeline, bounding box extractor, multilingual tokenizer, 35-SKU benchmark.
- **Buffer Task 1:** Implement oriented bounding box (OBB) deskewing for labels captured at an angle.
- **Buffer Task 2:** Fine-tune morphological kernel sizes specifically for dot-matrix expiry date fonts.
