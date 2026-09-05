# Curved Surface Processing & Cylinder Dewarping

## Purpose
Specifies the mathematical models, edge projection algorithms, and parametric dewarping techniques used to rectify text and measurements on cylindrical or deformed packaging.

## Scope
Covers cans, beverage bottles, jars, aerosols, and flexible tubular packaging.

## Authoritative Inputs
- Project Anti-Hallucination Policy: No unsupported claims of dewarping performance without empirical benchmarking.

## Assumptions
- The package surface can be modeled locally as a right circular cylinder with radius $R$ and height $H$.

## Open Questions
- Accuracy degradation of 3D cylinder parametric estimation from a single 2D monocular frame [TBD — MEASURE].

## Dependencies
- `packages/vision/`
- `experiments/dewarping/`

## Verification Requirements
- All unrolling algorithms must be experimentally benchmarked in `experiments/dewarping/`.

---

## Parametric Cylinder Dewarping Model

When a cylindrical package is viewed by a perspective camera, surface points suffer non-linear horizontal compression towards the outer silhouette edges.

Let $x_{\text{proj}}$ be the horizontal coordinate in the 2D camera image, and $\theta$ be the angle around the cylinder cylinder axis:
$$x_{\text{proj}} = R \cdot \sin(\theta)$$
$$\theta = \arcsin\left(\frac{x_{\text{proj}}}{R}\right)$$

The true unrolled arc length $s$ on the cylinder surface is:
$$s = R \cdot \theta = R \cdot \arcsin\left(\frac{x_{\text{proj}}}{R}\right)$$

### Processing Steps:
1. **Silhouette Edge Detection:** Hough transform or edge contours locate the vertical left and right boundaries of the cylinder.
2. **Radius & Axis Estimation:** The cylinder center line $x_0$ and apparent radius $R_{\text{px}}$ are calculated.
3. **Inverse Mapping Grid:** A non-linear remap grid rectifies compressed pixels near the limb back to linear arc length space.
4. **Rectified Planar Crop:** Downstream OCR and font height measurement execute on the rectified planar representation.
