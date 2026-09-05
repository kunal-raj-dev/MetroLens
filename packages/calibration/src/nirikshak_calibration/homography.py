"""
Nirikshak Calibration: Planar Homography & Perspective Rectification.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Responsibilities:
- Consumes planar quadrilateral geometry (e.g. from Phase 4 CardGeometry).
- Validates quadrilateral geometry rigorously (non-degeneracy, convexity, collinearity).
- Computes the 3x3 homography matrix H via cv2.getPerspectiveTransform().
- Warps perspective to generate orthorectified top-down planar crops via cv2.warpPerspective().
- Evaluates numerical reprojection residual error across all vertices.
- Returns minimal, strongly-typed RectificationResult.
- Does NOT perform anchor detection (Phase 4).
- Does NOT measure font heights (Phase 6).
- Does NOT perform cylindrical correction (Phase 7).
- Does NOT evaluate statutory compliance.
"""

import math
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union, Dict, Any
import cv2
import numpy as np

from .types import CardGeometry


class RectificationStatus(str, Enum):
    """Structured outcome status taxonomy for perspective rectification."""
    SUCCESS = "SUCCESS"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_POINT_COUNT = "INVALID_POINT_COUNT"
    NON_FINITE_COORDINATES = "NON_FINITE_COORDINATES"
    DUPLICATE_POINTS = "DUPLICATE_POINTS"
    DEGENERATE_QUADRILATERAL = "DEGENERATE_QUADRILATERAL"
    COLLINEAR_POINTS = "COLLINEAR_POINTS"
    NON_CONVEX_QUADRILATERAL = "NON_CONVEX_QUADRILATERAL"
    OUT_OF_IMAGE_BOUNDS = "OUT_OF_IMAGE_BOUNDS"
    INVALID_TARGET_DIMENSIONS = "INVALID_TARGET_DIMENSIONS"
    TRANSFORMATION_FAILED = "TRANSFORMATION_FAILED"


@dataclass(frozen=True)
class HomographyConfig:
    """
    Configurable geometric tolerances for quadrilateral validation and rectification.

    Evidentiary Status:
        Thresholds represent initial geometric validation heuristics.
        They must be treated as PROPOSED HEURISTICS rather than physical constants.
    """
    min_quadrilateral_area_px: float = 400.0       # Minimum area to prevent degenerate quad
    duplicate_point_tolerance_px: float = 2.0     # Minimum distance between distinct corners
    collinear_area_ratio_tolerance: float = 1e-4  # Triangle area / bounding box area threshold
    min_convex_cross_product: float = 1e-4        # Strictly positive cross-product threshold
    max_reprojection_error_px: float = 5.0        # Max allowable average corner reprojection error


@dataclass(frozen=True)
class RectificationResult:
    """
    Strongly-typed outcome of planar perspective rectification.

    Attributes:
        status: Specific outcome or failure reason code.
        success: True if perspective transformation succeeded.
        homography_matrix: 3x3 homography matrix represented as a 3-tuple of 3-tuples, or None.
        source_corners: Ordered 4-tuple of (x, y) source coordinates (TL, TR, BR, BL), or None.
        destination_corners: Ordered 4-tuple of (x, y) destination coordinates, or None.
        output_dimensions: (width_px, height_px) of the rectified target frame, or None.
        rectified_image: Rectified image array (NumPy ndarray) if an image was supplied, or None.
        reprojection_error_px: Mean Euclidean reprojection residual error in pixels, or None.
        message: Optional human-readable diagnostic message.
    """
    status: RectificationStatus
    success: bool
    homography_matrix: Optional[Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]] = None
    source_corners: Optional[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]] = None
    destination_corners: Optional[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]] = None
    output_dimensions: Optional[Tuple[int, int]] = None
    rectified_image: Optional[np.ndarray] = None
    reprojection_error_px: Optional[float] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into an inspectable dictionary."""
        h_list = None
        if self.homography_matrix is not None:
            h_list = [list(row) for row in self.homography_matrix]

        src_list = None
        if self.source_corners is not None:
            src_list = [list(pt) for pt in self.source_corners]

        dst_list = None
        if self.destination_corners is not None:
            dst_list = [list(pt) for pt in self.destination_corners]

        return {
            "status": self.status.value,
            "success": self.success,
            "homography_matrix": h_list,
            "source_corners": src_list,
            "destination_corners": dst_list,
            "output_dimensions": list(self.output_dimensions) if self.output_dimensions else None,
            "rectified_image_shape": list(self.rectified_image.shape) if self.rectified_image is not None else None,
            "reprojection_error_px": self.reprojection_error_px,
            "message": self.message,
        }


def _validate_points_structure(
    corners: Any,
) -> Tuple[bool, RectificationStatus, str, Optional[List[Tuple[float, float]]]]:
    """Validates raw input structure and parses 4 finite (x, y) float tuples."""
    if corners is None:
        return False, RectificationStatus.INVALID_INPUT, "Corners input cannot be None.", None

    if isinstance(corners, CardGeometry):
        raw_list = list(corners.corners)
    elif hasattr(corners, "__iter__"):
        try:
            raw_list = list(corners)
        except Exception:
            return False, RectificationStatus.INVALID_INPUT, "Corners input is not iterable.", None
    else:
        return False, RectificationStatus.INVALID_INPUT, "Corners input must be an iterable of 4 points or CardGeometry.", None

    if len(raw_list) != 4:
        return (
            False,
            RectificationStatus.INVALID_POINT_COUNT,
            f"Expected exactly 4 corners, received {len(raw_list)}.",
            None,
        )

    parsed_pts: List[Tuple[float, float]] = []
    for idx, pt in enumerate(raw_list):
        if pt is None or not hasattr(pt, "__len__") or len(pt) != 2:
            return (
                False,
                RectificationStatus.INVALID_INPUT,
                f"Corner at index {idx} must be a 2-element (x, y) coordinate pair.",
                None,
            )
        try:
            x_val = float(pt[0])
            y_val = float(pt[1])
        except (ValueError, TypeError):
            return (
                False,
                RectificationStatus.NON_FINITE_COORDINATES,
                f"Corner at index {idx} contains non-numeric values: ({pt[0]}, {pt[1]}).",
                None,
            )

        if not (math.isfinite(x_val) and math.isfinite(y_val)):
            return (
                False,
                RectificationStatus.NON_FINITE_COORDINATES,
                f"Corner at index {idx} contains non-finite values (NaN or Inf): ({x_val}, {y_val}).",
                None,
            )
        parsed_pts.append((x_val, y_val))

    return True, RectificationStatus.SUCCESS, "Valid points structure.", parsed_pts


def _compute_quadrilateral_area(pts: List[Tuple[float, float]]) -> float:
    """Computes signed area of polygon via Shoelace formula."""
    area = 0.0
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1]
        area -= pts[j][0] * pts[i][1]
    return 0.5 * area


def validate_quadrilateral_geometry(
    corners: Any,
    config: Optional[HomographyConfig] = None,
    image_shape: Optional[Tuple[int, ...]] = None,
) -> Tuple[bool, RectificationStatus, str, Optional[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]]]:
    """
    Rigorously evaluates the geometric validity of candidate quadrilateral source corners.

    Evaluations performed:
    1. Structure and point count (strictly 4 points).
    2. Finite coordinates (no NaN, Inf).
    3. Duplicate point detection (minimum pairwise distance threshold).
    4. Non-zero area & non-degeneracy (Shoelace area > min_area).
    5. Collinearity rejection (no 3 consecutive points collinear).
    6. Strict convexity verification (all 4 consecutive edge cross products have consistent sign).
    7. Image boundary verification (if image_shape is supplied).

    Returns:
        (is_valid, status, message, validated_corners_tuple)
    """
    cfg = config if config is not None else HomographyConfig()

    ok, status, msg, parsed_pts = _validate_points_structure(corners)
    if not ok or parsed_pts is None:
        return False, status, msg, None

    # 1. Duplicate point check (pairwise Euclidean distance)
    for i in range(4):
        for j in range(i + 1, 4):
            dx = parsed_pts[i][0] - parsed_pts[j][0]
            dy = parsed_pts[i][1] - parsed_pts[j][1]
            dist = math.hypot(dx, dy)
            if dist < cfg.duplicate_point_tolerance_px:
                return (
                    False,
                    RectificationStatus.DUPLICATE_POINTS,
                    f"Corners {i} and {j} are coincident (distance {dist:.2f}px < {cfg.duplicate_point_tolerance_px}px).",
                    None,
                )

    # 2. Collinearity & Convexity check via 2D cross products of consecutive edges
    cross_products: List[float] = []
    for i in range(4):
        p_prev = parsed_pts[(i - 1) % 4]
        p_curr = parsed_pts[i]
        p_next = parsed_pts[(i + 1) % 4]

        # Vector 1: p_prev -> p_curr
        v1_x = p_curr[0] - p_prev[0]
        v1_y = p_curr[1] - p_prev[1]
        # Vector 2: p_curr -> p_next
        v2_x = p_next[0] - p_curr[0]
        v2_y = p_next[1] - p_curr[1]

        cross = v1_x * v2_y - v1_y * v2_x
        len_prod = math.hypot(v1_x, v1_y) * math.hypot(v2_x, v2_y)

        # Check normalized triangle area for collinearity
        if len_prod > 0:
            sin_angle = abs(cross) / len_prod
            if sin_angle < cfg.collinear_area_ratio_tolerance:
                return (
                    False,
                    RectificationStatus.COLLINEAR_POINTS,
                    f"Consecutive vertices at index {i} are collinear (sin_angle {sin_angle:.6f} < {cfg.collinear_area_ratio_tolerance}).",
                    None,
                )

        cross_products.append(cross)

    # Convexity: all consecutive cross products must share the exact same sign
    has_pos = any(cp > cfg.min_convex_cross_product for cp in cross_products)
    has_neg = any(cp < -cfg.min_convex_cross_product for cp in cross_products)
    if has_pos and has_neg:
        return (
            False,
            RectificationStatus.NON_CONVEX_QUADRILATERAL,
            "Quadrilateral is non-convex or self-intersecting (cross-product signs differ).",
            None,
        )

    # 3. Polygon area & non-degeneracy
    signed_area = _compute_quadrilateral_area(parsed_pts)
    abs_area = abs(signed_area)
    if abs_area < cfg.min_quadrilateral_area_px:
        return (
            False,
            RectificationStatus.DEGENERATE_QUADRILATERAL,
            f"Quadrilateral area ({abs_area:.1f}px^2) is below minimum threshold ({cfg.min_quadrilateral_area_px}px^2).",
            None,
        )

    # 4. Image boundary validation (if image dimensions provided)
    if image_shape is not None and len(image_shape) >= 2:
        img_h, img_w = image_shape[0], image_shape[1]
        for idx, (px, py) in enumerate(parsed_pts):
            if px < -1.0 or px > img_w + 1.0 or py < -1.0 or py > img_h + 1.0:
                return (
                    False,
                    RectificationStatus.OUT_OF_IMAGE_BOUNDS,
                    f"Corner at index {idx} ({px:.1f}, {py:.1f}) is outside image domain [0, {img_w}] x [0, {img_h}].",
                    None,
                )

    result_tuple = (parsed_pts[0], parsed_pts[1], parsed_pts[2], parsed_pts[3])
    return True, RectificationStatus.SUCCESS, "Valid quadrilateral geometry.", result_tuple


def _derive_destination_dimensions(
    corners: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]],
    target_dimensions: Optional[Tuple[int, int]] = None,
) -> Tuple[bool, RectificationStatus, str, Optional[Tuple[int, int]]]:
    """Derives or validates target width and height in pixels."""
    if target_dimensions is not None:
        if not hasattr(target_dimensions, "__len__") or len(target_dimensions) != 2:
            return (
                False,
                RectificationStatus.INVALID_TARGET_DIMENSIONS,
                "Target dimensions must be a 2-tuple (width, height).",
                None,
            )
        try:
            tw = int(target_dimensions[0])
            th = int(target_dimensions[1])
        except (ValueError, TypeError):
            return (
                False,
                RectificationStatus.INVALID_TARGET_DIMENSIONS,
                f"Target dimensions must be numeric, received ({target_dimensions[0]}, {target_dimensions[1]}).",
                None,
            )

        if tw < 2 or th < 2:
            return (
                False,
                RectificationStatus.INVALID_TARGET_DIMENSIONS,
                f"Target dimensions must be >= 2px, received ({tw}, {th}).",
                None,
            )
        return True, RectificationStatus.SUCCESS, "Explicit target dimensions accepted.", (tw, th)

    # Deterministically derive target dimensions from source edge lengths:
    # Width = average of top (TL->TR) and bottom (BL->BR) edge lengths
    # Height = average of left (TL->BL) and right (TR->BR) edge lengths
    tl, tr, br, bl = corners
    w_top = math.hypot(tr[0] - tl[0], tr[1] - tl[1])
    w_bottom = math.hypot(br[0] - bl[0], br[1] - bl[1])
    h_left = math.hypot(bl[0] - tl[0], bl[1] - tl[1])
    h_right = math.hypot(br[0] - tr[0], br[1] - tr[1])

    derived_w = max(2, int(round(0.5 * (w_top + w_bottom))))
    derived_h = max(2, int(round(0.5 * (h_left + h_right))))

    return True, RectificationStatus.SUCCESS, "Target dimensions derived from source edge lengths.", (derived_w, derived_h)


def rectify_planar_quadrilateral(
    corners: Any,
    image: Optional[np.ndarray] = None,
    target_dimensions: Optional[Tuple[int, int]] = None,
    config: Optional[HomographyConfig] = None,
) -> RectificationResult:
    """
    Computes 3x3 homography matrix H and perspective-rectifies a planar quadrilateral crop.

    Algorithm:
    1. Validates input quadrilateral points for finiteness, non-degeneracy, collinearity, convexity.
    2. Validates or derives destination dimensions (width, height).
    3. Maps canonical source corners (TL, TR, BR, BL) to destination corners:
       TL -> (0, 0), TR -> (W-1, 0), BR -> (W-1, H-1), BL -> (0, H-1).
    4. Calculates 3x3 homography H via cv2.getPerspectiveTransform().
    5. Computes mean Euclidean reprojection error across all 4 corner coordinates.
    6. If an image array is supplied, performs cv2.warpPerspective() using linear interpolation.
    7. Returns minimal, strongly-typed RectificationResult.

    Args:
        corners: 4 ordered coordinates (TL, TR, BR, BL) or CardGeometry object.
        image: Optional NumPy ndarray to be perspective-rectified.
        target_dimensions: Optional (width, height) pixel dimensions for the rectified crop.
        config: Optional HomographyConfig with geometric tolerances.

    Returns:
        RectificationResult containing status, success flag, homography matrix, corners, and warped image.
    """
    cfg = config if config is not None else HomographyConfig()

    # Validate image properties if supplied
    image_shape = None
    if image is not None:
        if not isinstance(image, np.ndarray):
            return RectificationResult(
                status=RectificationStatus.INVALID_INPUT,
                success=False,
                message="Supplied image must be a numpy.ndarray.",
            )
        if image.size == 0 or image.ndim not in (2, 3):
            return RectificationResult(
                status=RectificationStatus.INVALID_INPUT,
                success=False,
                message="Supplied image array must be a non-empty 2D or 3D numpy array.",
            )
        image_shape = image.shape

    # Validate source quadrilateral geometry
    is_geom_valid, geom_status, geom_msg, valid_corners = validate_quadrilateral_geometry(
        corners=corners, config=cfg, image_shape=image_shape
    )
    if not is_geom_valid or valid_corners is None:
        return RectificationResult(
            status=geom_status,
            success=False,
            message=geom_msg,
        )

    # Derive destination frame dimensions
    dim_ok, dim_status, dim_msg, out_dims = _derive_destination_dimensions(
        corners=valid_corners, target_dimensions=target_dimensions
    )
    if not dim_ok or out_dims is None:
        return RectificationResult(
            status=dim_status,
            success=False,
            source_corners=valid_corners,
            message=dim_msg,
        )

    target_w, target_h = out_dims

    # Define canonical destination rectangle coordinates
    dst_corners = (
        (0.0, 0.0),
        (float(target_w - 1), 0.0),
        (float(target_w - 1), float(target_h - 1)),
        (0.0, float(target_h - 1)),
    )

    src_arr = np.array(valid_corners, dtype=np.float32)
    dst_arr = np.array(dst_corners, dtype=np.float32)

    try:
        h_mat = cv2.getPerspectiveTransform(src_arr, dst_arr)
    except Exception as exc:
        return RectificationResult(
            status=RectificationStatus.TRANSFORMATION_FAILED,
            success=False,
            source_corners=valid_corners,
            destination_corners=dst_corners,
            output_dimensions=out_dims,
            message=f"cv2.getPerspectiveTransform failed: {str(exc)}",
        )

    if h_mat is None or h_mat.shape != (3, 3) or not np.all(np.isfinite(h_mat)):
        return RectificationResult(
            status=RectificationStatus.TRANSFORMATION_FAILED,
            success=False,
            source_corners=valid_corners,
            destination_corners=dst_corners,
            output_dimensions=out_dims,
            message="Calculated homography matrix contains non-finite values or invalid shape.",
        )

    # Evaluate numerical reprojection error: p'_i = H * p_i
    reproj_errors: List[float] = []
    for i in range(4):
        p_src_h = np.array([valid_corners[i][0], valid_corners[i][1], 1.0], dtype=np.float64)
        p_proj = h_mat.dot(p_src_h)
        if abs(p_proj[2]) < 1e-12:
            return RectificationResult(
                status=RectificationStatus.TRANSFORMATION_FAILED,
                success=False,
                source_corners=valid_corners,
                destination_corners=dst_corners,
                output_dimensions=out_dims,
                message="Singular projective scale in corner reprojection.",
            )
        px_proj = p_proj[0] / p_proj[2]
        py_proj = p_proj[1] / p_proj[2]

        err = math.hypot(px_proj - dst_corners[i][0], py_proj - dst_corners[i][1])
        reproj_errors.append(err)

    mean_reproj_err = float(np.mean(reproj_errors))

    # Convert 3x3 matrix to immutable tuple representation
    h_tuple = (
        (float(h_mat[0, 0]), float(h_mat[0, 1]), float(h_mat[0, 2])),
        (float(h_mat[1, 0]), float(h_mat[1, 1]), float(h_mat[1, 2])),
        (float(h_mat[2, 0]), float(h_mat[2, 1]), float(h_mat[2, 2])),
    )

    # Enforce maximum reprojection error tolerance
    if mean_reproj_err > cfg.max_reprojection_error_px:
        return RectificationResult(
            status=RectificationStatus.TRANSFORMATION_FAILED,
            success=False,
            homography_matrix=h_tuple,
            source_corners=valid_corners,
            destination_corners=dst_corners,
            output_dimensions=out_dims,
            reprojection_error_px=mean_reproj_err,
            message=f"Mean reprojection error ({mean_reproj_err:.2f}px) exceeds tolerance ({cfg.max_reprojection_error_px:.2f}px).",
        )

    # Perform warp perspective if image array was provided
    warped_img = None
    if image is not None:
        try:
            warped_img = cv2.warpPerspective(
                image,
                h_mat,
                (target_w, target_h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )
        except Exception as exc:
            return RectificationResult(
                status=RectificationStatus.TRANSFORMATION_FAILED,
                success=False,
                homography_matrix=h_tuple,
                source_corners=valid_corners,
                destination_corners=dst_corners,
                output_dimensions=out_dims,
                reprojection_error_px=mean_reproj_err,
                message=f"cv2.warpPerspective failed: {str(exc)}",
            )

    return RectificationResult(
        status=RectificationStatus.SUCCESS,
        success=True,
        homography_matrix=h_tuple,
        source_corners=valid_corners,
        destination_corners=dst_corners,
        output_dimensions=out_dims,
        rectified_image=warped_img,
        reprojection_error_px=mean_reproj_err,
        message="Perspective transformation and planar rectification successful.",
    )
