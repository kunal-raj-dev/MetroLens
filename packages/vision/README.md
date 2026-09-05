# Nirikshak Vision Package (`nirikshak-vision`)

**Package:** `packages/vision/`
**Namespace:** `nirikshak_vision`
**Role:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Standard Compliance:** SIH26034 / Nirikshak Anti-Hallucination Architectural Framework
**Current Phase Status:** Phase 2 (Image Quality Gate) **COMPLETED**

---

## 1. Package Purpose & Scope

The `nirikshak-vision` package serves as the optical pre-flight quality gate for the Nirikshak / MetroLens AI platform. Consumer smartphone photographs taken in retail environments frequently suffer from motion blur, out-of-focus optics, specular glare on laminated packaging foils, or extreme under/overexposure.

Allowing degraded frames to enter downstream optical character recognition (OCR) and metric calibration pipelines produces corrupted character stroke measurements, inaccurate bounding boxes, and unrepeatable legal compliance verdicts.

The pre-flight quality gate strictly enforces quality criteria before image arrays are admitted into downstream processing:
- **Sharpness Gate:** Rejects out-of-focus and motion-blurred images.
- **Specular Glare Gate:** Rejects images with reflective highlights obscuring mandatory declaration panels.
- **Contrast & Dynamic Range Gate:** Rejects washed-out or underexposed packaging captures.

---

## 2. Public API & Usage

```python
import cv2
from nirikshak_vision import assess_image_quality, QualityGateResult

# Load image (BGR numpy array)
image = cv2.imread("tests/fixtures/package_capture.jpg")

# Evaluate optical quality
result: QualityGateResult = assess_image_quality(image)

if result.is_valid:
    print("Pre-flight quality gate PASSED.")
    print(f"Sharpness score: {result.sharpness_score:.1f}")
    print(f"Glare percentage: {result.glare_percentage:.2f}%")
else:
    print("Pre-flight quality gate REJECTED.")
    print(f"Failure code: {result.failure_code}")
    print(f"Technical reason: {result.failure_reason}")
    print(f"Actionable user advice: {result.actionable_advice}")
```

---

## 3. Mathematical Quality Criteria & Thresholds

All thresholds are empirically derived heuristics designed to run in $< 50\text{ms}$ on commodity x86/ARM CPUs:

### A. Sharpness / Blur Filter (Laplacian Variance)
The image is converted to grayscale, convolved with a discrete $3 \times 3$ Laplacian kernel $\nabla^2$, and the sample variance of the second spatial derivatives is computed:
$$\text{Score}_{\text{sharpness}} = \sigma^2(\nabla^2 I)$$
- **Threshold:** $\text{Score}_{\text{sharpness}} \ge 100.0$.
- **Rejection Code:** `ERR_IMAGE_BLUR`.
- **Actionable Advice:** *"Image is too blurry. Please hold camera steady and tap package to focus."*

### B. Specular Glare Filter (HSV Saturation / Value Mask)
Highly reflective packaging films (laminates, metal foil, cellophane) reflect directional lighting directly into the camera lens, saturating camera sensor photodiodes:
1. Image is converted to the HSV (Hue-Saturation-Value) color space.
2. A binary glare mask identifies pixels where $V \ge 250$ and $S \le 30$.
3. Glare area percentage is calculated relative to total image area:
$$\text{Glare}_{\%} = \frac{\sum M_{\text{glare}}}{W \times H} \times 100\%$$
- **Threshold:** $\text{Glare}_{\%} \le 15.0\%$.
- **Rejection Code:** `ERR_IMAGE_GLARE`.
- **Actionable Advice:** *"Excessive specular glare detected. Please tilt package slightly away from direct light."*

### C. Contrast & Dynamic Range Filter
Low-contrast photographs (e.g. captured under heavy shadows or washed out by backlight) prevent edge detectors from discerning packaging contours:
$$\sigma_{\text{luminance}} = \text{std\_dev}(I_{\text{gray}})$$
- **Threshold:** $\sigma_{\text{luminance}} \ge 20.0$.
- **Rejection Code:** `ERR_IMAGE_LOW_CONTRAST`.
- **Actionable Advice:** *"Poor lighting contrast. Please ensure packaging is evenly illuminated."*

---

## 4. Architectural Contracts & DTOs (`types.py`)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class QualityGateResult:
    is_valid: bool
    sharpness_score: float
    glare_percentage: float
    contrast_score: float
    failure_code: Optional[str] = None
    failure_reason: Optional[str] = None
    actionable_advice: Optional[str] = None
```

- **Immutability:** Result objects are frozen dataclasses preventing state tampering.
- **Fail-Safe Robustness:** Non-array, empty, or single-color inputs fail gracefully returning structured failure codes without throwing unhandled exceptions.

---

## 5. Verification Suite & Test Evidence

The package is thoroughly verified by automated tests in `packages/vision/tests/test_quality_gate.py`:
- **Sharpness Tests:** Sharp synthetic edge patterns pass; Gaussian-blurred frames fail with `ERR_IMAGE_BLUR`.
- **Glare Tests:** Diffuse scenes pass; localized high-intensity specular patches fail with `ERR_IMAGE_GLARE`.
- **Contrast Tests:** Natural contrast passes; flat uniform gray or low-dynamic range frames fail with `ERR_IMAGE_LOW_CONTRAST`.
- **Input Robustness:** Empty arrays, non-array inputs, single-channel arrays, non-finite values handled gracefully.
- **Execution Latency:** Median runtime $< 25\text{ms}$ on CPU across standard 1080p frames.

```bash
# Execute vision unit tests
pytest packages/vision/tests/test_quality_gate.py -v
```
