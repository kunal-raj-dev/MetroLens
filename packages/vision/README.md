# Nirikshak Vision Package (`nirikshak-vision`)

## Purpose
Implements image quality gating (Laplacian variance sharpness and luminance glare analysis) and Principal Display Panel (PDP) segmentation.

## Owner
Computer Vision Lead

## Interface Seams
- **Input**: Raw image bytes or numpy array.
- **Output**: `QualityGateResult` (sharpness score, glare percentage, pass/fail flag) and PDP contour/polygon.
- **Error Codes**: `ERR_IMAGE_BLUR`, `ERR_IMAGE_GLARE`.
