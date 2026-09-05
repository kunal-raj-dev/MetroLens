# Annotation Guidelines & Ground Truth Protocol

## Purpose
Standardizes labeling conventions for bounding boxes, character polygons, Principal Display Panel boundaries, and physical ground-truth measurements.

## Scope
Governs data labeling for `data/annotations/` and benchmark validation sets.

## Authoritative Inputs
- COCO annotation standard.
- Metrology manual for physical caliper measurements.

## Assumptions
- High-quality, consistent ground truth is required to evaluate OCR CER/WER and measurement uncertainty.

## Open Questions
- Protocol for annotating debossed or translucent text on clear plastic packaging [TBD — MEASURE].

## Dependencies
- Labeling tools (CVAT, Label Studio, or custom annotator).

## Verification Requirements
- Dual-annotator agreement (Cohen's Kappa $\ge 0.85$) on text transcription and $\text{IoU} \ge 0.90$ on bounding boxes.

---

## 1. Bounding Box & Polygon Rules

1. **Text Tokens:** Draw tight 4-point oriented bounding boxes or multi-point polygons hugging the character contour. Do not include excessive background margins.
2. **Principal Display Panel (PDP):** Annotate the full polygon enclosing the primary presented face of the container. For bottles/cans, annotate the 2D projected silhouette and mark curvature parameters.
3. **Reference Target:** Tight bounding box enclosing the circular/checkerboard reference marker.

---

## 2. Physical Ground Truth Measurement Protocol

1. **Tooling:** Mitutoyo / Insize digital vernier calipers ($\pm 0.02\text{ mm}$ accuracy).
2. **Font Height Measurement:** Measure the highest numeral in the Net Quantity declaration from bottom baseline to top cap height. Record 3 independent measurements and store the arithmetic mean.
3. **Panel Dimension Measurement:** Measure height ($H$) and width ($W$) of the carton face in millimetres.
