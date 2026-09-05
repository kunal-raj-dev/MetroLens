# Image Quality Gate Specification

## Purpose
Defines the real-time image validation filters, mathematical thresholds, and user guidance cues used to reject degraded, blurry, or glared packaging captures before running OCR.

## Scope
Executes on the client or API immediately upon image acquisition.

## Authoritative Inputs
- Standard digital image processing principles (Laplacian variance, brightness histograms).

## Assumptions
- Rejecting bad frames early prevents spurious OCR hallucinations, reduces server compute waste, and supports high-trust downstream evidence.

## Open Questions
- Optimal dynamic threshold adaptation for low-light retail warehouse environments [TBD — MEASURE].

## Dependencies
- `packages/vision/`
- `tests/vision/`

## Verification Requirements
- Synthetic blurred images in `tests/fixtures/` must trigger `REQUEST_RETAKE` reliably on degraded frames (acceptance criteria: TARGET — NOT VALIDATED; Status: `TBD — MEASURE`).

---

## 1. Blur Detection (Laplacian Variance)

Blur is evaluated using the variance of the 2D Laplacian operator across the grayscale image $I$:
$$\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}$$
$$\text{Var}(\nabla^2 I) = \frac{1}{N} \sum_{x,y} \left( \nabla^2 I(x,y) - \mu_{\nabla^2} \right)^2$$

### Threshold Policy:
- $\text{Var}(\nabla^2 I) \ge 100.0$: **PASS** (Proceed to inference).
- $50.0 \le \text{Var}(\nabla^2 I) < 100.0$: **BORDERLINE** (Flag warning, ask officer to confirm sharpness).
- $\text{Var}(\nabla^2 I) < 50.0$: **FAIL / REJECT** (Trigger `REQUEST_RETAKE`).

---

## 2. Specular Glare & Reflection Detection

Packaging materials (laminated pouches, cellophane wraps, metallic foils) frequently suffer from blinding specular reflections that obliterate text.

### Glare Assessment Algorithm:
1. Identify pixels with intensity $Y \ge 250$ in the grayscale channel.
2. Form connected component masks of saturated regions.
3. Compute the intersection of glare masks with candidate text bounding boxes.
4. If $> 15\%$ of a mandatory declaration area is occluded by specular glare, flag `REQUEST_RETAKE` with message: *"Glare obscuring declarations. Please tilt camera or alter lighting angle."*

---

## 3. Illumination & Shadow Check

Images with mean intensity $\mu_Y < 40$ (under-exposed) or $> 220$ (over-exposed) are flagged with corrective on-screen prompts.
