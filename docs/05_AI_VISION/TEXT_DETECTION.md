# Text Detection & Bounding Box Localization

## Purpose
Specifies the deep-learning architectures, polygon regression algorithms, and non-maximum suppression (NMS) routines used to detect words, lines, and character clusters.

## Scope
Applies to text localization across complex packaging trade dress, high-density ingredient tables, and isolated numeral declarations.

## Authoritative Inputs
- Academic literature on scene text detection (DBNet, CRAFT, TextBoxes++).

## Assumptions
- Text lines may be rotated, curved, or vertically stacked on package edges.

## Open Questions
- Optimal polygon corner count (4-point quad vs. 14-point polygon) for curved bottle labels [TBD — MEASURE].

## Dependencies
- `packages/vision/`
- `packages/ocr/`

## Verification Requirements
- Intersection-over-Union (IoU) on text bounding boxes must achieve $\ge 0.80$ on synthetic benchmark vector sets.

---

## Detection Architecture

1. **Feature Extraction:** Lightweight ResNet-18 or MobileNetV3 backbone optimized for mobile edge inference.
2. **Binarization Map:** Differentiable Binarization (DB) module predicting probability map and threshold map.
3. **Polygon Generation:** Dilation and polygon approximation generating tight bounding polygons around text lines.
4. **Orientation Normalization:** Perspective transform rotating oriented text boxes to horizontal axis prior to optical recognition.
