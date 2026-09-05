# AI Vision & Observation Pipeline Specification

## Purpose
Defines the computer vision architectures, OCR inference strategies, bounding box detectors, and geometric transformation modules utilized strictly as an observation layer.

## Scope
Covers all machine learning models, inference runtimes, hardware acceleration profiles, and observation outputs.

## Authoritative Inputs
- Project Anti-Hallucination Policy: AI is an observation layer only.
- ISO/IEC 19794 (Biometric & optical measurement frameworks).

## Assumptions
- Models run efficiently on CPU via ONNX Runtime, OpenVINO, or quantized PyTorch/Paddle weights.

## Open Questions
- Optimal quantized model size for edge deployment on low-spec field laptops [TBD — MEASURE].

## Dependencies
- `packages/vision/`
- `packages/ocr/`
- `models/`

## Verification Requirements
- All models must have corresponding model cards in `models/cards/`.
- No model output may directly set a legal verdict without passing through `packages/rules-engine/`.

---

## Architecture of the Observation Layer

The AI pipeline is strictly partitioned into specialized tasks:

```
                      [Input Image: I_raw]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
   [Text Detection]                     [Surface & PDP Analysis]
   DBNet / TextBoxes++                  Contour & Polygon Segmentation
   Output: Bounding Polygons            Output: PDP Mask, Cylinder Curvature
            │                                     │
            ▼                                     ▼
   [Text Recognition]                   [Dewarping & Rectification]
   SVTR / CRNN Multilingual             Cylinder Parametric Unrolling
   Output: Raw String Tokens            Output: Planar Rectified Crop
            │                                     │
            └──────────────────┬──────────────────┘
                               │
                               ▼
                [Field Extraction & Normalization]
                Regex, Token Clustering & LayoutLM
                Output: Extracted Declaration Entity Dict
```

### Critical Boundaries
1. **No Legal Hallucination:** The AI model never outputs `"VIOLATION"` or `"LEGAL"`. It outputs:
   - `detected_text: "Rs. 150.00"`
   - `confidence: 0.94`
   - `bounding_box: [x1, y1, x2, y2]`
2. **Confidence Routing:** Any token with confidence $< 0.60$ is flagged for human review.
3. **Curved Surface Handling:** For cylindrical cans and bottles, parametric dewarping normalizes curved text prior to font height estimation.
