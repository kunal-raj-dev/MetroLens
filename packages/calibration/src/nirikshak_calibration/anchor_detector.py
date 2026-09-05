"""
Nirikshak Calibration: Deterministic Metric Anchor Detection.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Responsibilities:
- Detects physical reference anchors (RBI Rs 10 coin and ISO/IEC 7810 ID-1 card).
- Uses deterministic contour extraction, geometric validation, and algebraic fit scoring.
- Ranks candidates deterministically using explainable evidence (never OpenCV order, never candidates[0]).
- Applies spatial non-maximum suppression (NMS) to eliminate stroke/concentric duplicate detections of the same object.
- Applies confidence gating before ambiguity evaluation (rejecting low-scoring noise).
- Dispatches cleanly across forced anchor modes (COIN_INR_10, ID1_CARD) and AUTO mode.
- Returns minimal, strongly-typed AnchorDetectionResult.
- Does NOT estimate metric scale factor (no scale fabrication, no is_calibrated assertion).
- Does NOT perform perspective rectification or homography unwarping (deferred to Phase 5).
"""

import math
from typing import Optional, Tuple, List, Union, Dict, Any, Set
import cv2
import numpy as np

from nirikshak_vision.quality import convert_to_grayscale
from .types import (
    AnchorType,
    AnchorDetectionStatus,
    EllipseGeometry,
    CardGeometry,
    ConcentricRingInfo,
    AnchorDetectorConfig,
    AnchorDetectionResult,
)


def order_quadrilateral_corners(
    pts: np.ndarray,
) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """
    Deterministically orders 4 quadrilateral vertices into standard orientation:
    (Top-Left, Top-Right, Bottom-Right, Bottom-Left).

    Ordering Algorithm:
    - Top-Left has the smallest (x + y) sum.
    - Bottom-Right has the largest (x + y) sum.
    - Top-Right has the smallest (y - x) difference.
    - Bottom-Left has the largest (y - x) difference.

    Returns:
        Structurally immutable 4-tuple of (x, y) float tuples.
    """
    points = pts.reshape(4, 2).astype(np.float64)

    # Sum of coordinates: s = x + y
    s = points.sum(axis=1)
    top_left = points[np.argmin(s)]
    bottom_right = points[np.argmax(s)]

    # Difference of coordinates: d = y - x
    d = points[:, 1] - points[:, 0]
    top_right = points[np.argmin(d)]
    bottom_left = points[np.argmax(d)]

    return (
        (float(top_left[0]), float(top_left[1])),
        (float(top_right[0]), float(top_right[1])),
        (float(bottom_right[0]), float(bottom_right[1])),
        (float(bottom_left[0]), float(bottom_left[1])),
    )


def compute_algebraic_ellipse_residual(
    cnt: np.ndarray,
    ell: Tuple[Tuple[float, float], Tuple[float, float], float],
) -> float:
    """
    Computes mean algebraic distance error from contour points to fitted ellipse.

    OpenCV cv2.fitEllipse() returns ((cx, cy), (width, height), angle_deg),
    where width and height are full axis diameters (2a and 2b).

    Mathematical Formulation:
    1. Center extraction: (cx, cy)
    2. Semi-axes: a = width / 2.0, b = height / 2.0
    3. Center translation: dx = x - cx, dy = y - cy
    4. Rotation into ellipse intrinsic frame:
       x' = dx * cos(theta) + dy * sin(theta)
       y' = -dx * sin(theta) + dy * cos(theta)
    5. Unit ellipse algebraic residual:
       residual = (1/N) * sum | (x'/a)^2 + (y'/b)^2 - 1 |

    Returns:
        Mean absolute algebraic residual (float).
    """
    (cx, cy), (width, height), angle_deg = ell
    a = width / 2.0
    b = height / 2.0

    if a <= 0.5 or b <= 0.5:
        return 999.0

    pts = cnt.reshape(-1, 2).astype(np.float64)
    dx = pts[:, 0] - cx
    dy = pts[:, 1] - cy

    rad = math.radians(angle_deg)
    cos_t = math.cos(rad)
    sin_t = math.sin(rad)

    x_rot = dx * cos_t + dy * sin_t
    y_rot = -dx * sin_t + dy * cos_t

    algebraic = (x_rot / a) ** 2 + (y_rot / b) ** 2 - 1.0
    return float(np.mean(np.abs(algebraic)))


def _compute_edge_support_ellipse(
    gray: np.ndarray,
    ell: Tuple[Tuple[float, float], Tuple[float, float], float],
    n_samples: int = 48,
) -> float:
    """Computes fraction of perimeter sample points exhibiting strong image gradient."""
    (cx, cy), (width, height), angle_deg = ell
    a = width / 2.0
    b = height / 2.0
    h, w = gray.shape[:2]

    rad_rot = math.radians(angle_deg)
    cos_r, sin_r = math.cos(rad_rot), math.sin(rad_rot)

    supported_count = 0
    thetas = np.linspace(0, 2 * math.pi, n_samples, endpoint=False)

    for th in thetas:
        px = a * math.cos(th)
        py = b * math.sin(th)
        gx = int(round(cx + px * cos_r - py * sin_r))
        gy = int(round(cy + px * sin_r + py * cos_r))

        if 1 <= gx < w - 1 and 1 <= gy < h - 1:
            # Central difference gradient
            dx = float(gray[gy, gx + 1]) - float(gray[gy, gx - 1])
            dy = float(gray[gy + 1, gx]) - float(gray[gy - 1, gx])
            grad_mag = math.hypot(dx, dy)
            if grad_mag >= 15.0:
                supported_count += 1

    return float(supported_count / max(1, n_samples))


def _compute_edge_support_quadrilateral(
    gray: np.ndarray,
    corners: Tuple[Tuple[float, float], ...],
    samples_per_edge: int = 16,
) -> float:
    """Computes fraction of quadrilateral perimeter points exhibiting strong image gradient."""
    h, w = gray.shape[:2]
    supported_count = 0
    total_samples = len(corners) * samples_per_edge

    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]
        for alpha in np.linspace(0.1, 0.9, samples_per_edge):
            gx = int(round(p1[0] + alpha * (p2[0] - p1[0])))
            gy = int(round(p1[1] + alpha * (p2[1] - p1[1])))
            if 1 <= gx < w - 1 and 1 <= gy < h - 1:
                dx = float(gray[gy, gx + 1]) - float(gray[gy, gx - 1])
                dy = float(gray[gy + 1, gx]) - float(gray[gy - 1, gx])
                if math.hypot(dx, dy) >= 15.0:
                    supported_count += 1

    return float(supported_count / max(1, total_samples))


class _CandidateAnchor:
    """Internal candidate evaluation container for unified ranking."""

    def __init__(
        self,
        anchor_type: AnchorType,
        geometry: Union[EllipseGeometry, CardGeometry],
        score: float,
        fit_quality: float,
        edge_support: float,
        ring_info: Optional[ConcentricRingInfo] = None,
        glare_overlap: float = 0.0,
    ):
        self.anchor_type = anchor_type
        self.geometry = geometry
        self.score = score
        self.fit_quality = fit_quality
        self.edge_support = edge_support
        self.ring_info = ring_info
        self.glare_overlap = glare_overlap


def _detect_coin_candidates(
    gray: np.ndarray,
    config: AnchorDetectorConfig,
    glare_mask: Optional[np.ndarray] = None,
) -> List[_CandidateAnchor]:
    """Detects and characterizes circular/elliptical coin candidates with spatial deduplication."""
    h, w = gray.shape[:2]
    frame_area = float(h * w)

    blurred = cv2.GaussianBlur(gray, (5, 5), 1.0)
    edges = cv2.Canny(blurred, 20, 60)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(closed_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not cnts:
        return []

    raw_candidates: List[dict] = []

    for cnt in cnts:
        if len(cnt) < 20:
            continue

        area = cv2.contourArea(cnt)
        if area < config.min_contour_area_px or area > (frame_area * config.max_contour_area_ratio):
            continue

        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull) + 1e-6
        solidity = area / hull_area
        if solidity < 0.80:
            continue

        try:
            ell = cv2.fitEllipse(cnt)
        except Exception:
            continue

        (cx, cy), (d1, d2), raw_angle_deg = ell
        # OpenCV fitEllipse returns ((cx, cy), (d1, d2), raw_angle_deg) where d1 is aligned with raw_angle_deg.
        # Normalize so major_axis is always max(d1, d2) and major_angle is strictly the major-axis orientation.
        if d1 >= d2:
            major_axis = d1
            minor_axis = d2
            major_angle = raw_angle_deg
        else:
            major_axis = d2
            minor_axis = d1
            major_angle = (raw_angle_deg + 90.0) % 180.0

        if minor_axis <= 1.0 or major_axis <= 1.0:
            continue

        aspect_ratio = minor_axis / major_axis
        if aspect_ratio < config.min_ellipse_aspect_ratio or aspect_ratio > config.max_ellipse_aspect_ratio:
            continue

        residual = compute_algebraic_ellipse_residual(cnt, ell)
        if residual > config.max_ellipse_residual:
            continue

        edge_supp = _compute_edge_support_ellipse(gray, ell)

        # Check glare overlap
        glare_overlap = 0.0
        if glare_mask is not None:
            cmask = np.zeros((h, w), dtype=np.uint8)
            cv2.ellipse(cmask, ell, 255, -1)
            c_area = np.count_nonzero(cmask)
            if c_area > 0:
                glare_overlap = float(np.count_nonzero(cmask & glare_mask) / c_area)

        # Border proximity check
        margin = 4
        on_border = (
            cx - major_axis / 2.0 < margin
            or cx + major_axis / 2.0 > w - margin
            or cy - major_axis / 2.0 < margin
            or cy + major_axis / 2.0 > h - margin
        )

        raw_candidates.append({
            "contour": cnt,
            "ell": ell,
            "cx": cx,
            "cy": cy,
            "major": major_axis,
            "minor": minor_axis,
            "angle": major_angle,
            "aspect_ratio": aspect_ratio,
            "area": area,
            "solidity": solidity,
            "residual": residual,
            "edge_support": edge_supp,
            "glare_overlap": glare_overlap,
            "on_border": on_border,
            "ring_info": None,
        })

    if not raw_candidates:
        return []

    # 1. Concentric Ring Pairing (RBI Rs 10 bimetallic core verification)
    # The inner nickel core is associated with the outer brass ring, NOT a competing distinct coin.
    subordinate_indices: Set[int] = set()
    if len(raw_candidates) >= 2:
        raw_candidates.sort(key=lambda x: x["area"], reverse=True)
        for i in range(len(raw_candidates)):
            c_outer = raw_candidates[i]
            for j in range(i + 1, len(raw_candidates)):
                if j in subordinate_indices:
                    continue
                c_inner = raw_candidates[j]
                dist_centers = math.hypot(c_outer["cx"] - c_inner["cx"], c_outer["cy"] - c_inner["cy"])
                if dist_centers < (config.concentric_center_dist_ratio * c_outer["major"]):
                    ratio = c_inner["major"] / (c_outer["major"] + 1e-6)
                    target = config.concentric_ring_ratio_target
                    tol = config.concentric_ring_ratio_tolerance
                    if abs(ratio - target) <= tol:
                        c_outer["ring_info"] = ConcentricRingInfo(
                            outer_major_px=round(c_outer["major"], 2),
                            inner_major_px=round(c_inner["major"], 2),
                            diameter_ratio=round(ratio, 4),
                            has_concentric_ring=True,
                        )
                        # Mark inner core as absorbed
                        subordinate_indices.add(j)
                        break
            if c_outer["ring_info"] is not None:
                break

    # Exclude absorbed inner core candidates from competing independently
    retained_candidates = [c for idx, c in enumerate(raw_candidates) if idx not in subordinate_indices]

    # Compute candidate scores (aligned 3-pillar geometric evidence: 45% shape, 30% edge, 25% regularity)
    scored_candidates: List[dict] = []
    for c in retained_candidates:
        fit_q = max(0.0, 1.0 - (c["residual"] / config.max_ellipse_residual))
        base_score = 0.45 * fit_q + 0.30 * c["edge_support"] + 0.25 * c["solidity"]

        # Auxiliary concentric ring bonus
        if c["ring_info"] is not None and c["ring_info"].has_concentric_ring:
            base_score = min(1.0, base_score + 0.10)

        # Glare and border penalties
        if c["glare_overlap"] > 0.10:
            base_score = base_score * max(0.2, 1.0 - c["glare_overlap"])
        if c["on_border"]:
            base_score = base_score * 0.70

        c["score"] = round(float(min(1.0, max(0.0, base_score))), 3)
        c["fit_q"] = round(fit_q, 3)
        scored_candidates.append(c)

    # 2. Spatial Non-Maximum Suppression (suppresses duplicate inner/outer edge strokes of same coin)
    scored_candidates.sort(key=lambda c: c["score"], reverse=True)
    suppressed: Set[int] = set()
    distinct_coins: List[_CandidateAnchor] = []

    for i in range(len(scored_candidates)):
        if i in suppressed:
            continue
        c1 = scored_candidates[i]
        for j in range(i + 1, len(scored_candidates)):
            c2 = scored_candidates[j]
            dist = math.hypot(c1["cx"] - c2["cx"], c1["cy"] - c2["cy"])
            # If centers are within 30% of major diameter, they belong to the same physical coin object
            if dist < (0.30 * max(c1["major"], c2["major"])):
                suppressed.add(j)

        geom = EllipseGeometry(
            center=(round(float(c1["cx"]), 2), round(float(c1["cy"]), 2)),
            major_axis_px=round(float(c1["major"]), 2),
            minor_axis_px=round(float(c1["minor"]), 2),
            angle_deg=round(float(c1["angle"]), 2),
            aspect_ratio=round(float(c1["aspect_ratio"]), 4),
        )

        distinct_coins.append(_CandidateAnchor(
            anchor_type=AnchorType.COIN_INR_10,
            geometry=geom,
            score=c1["score"],
            fit_quality=c1["fit_q"],
            edge_support=round(c1["edge_support"], 3),
            ring_info=c1["ring_info"],
            glare_overlap=round(c1["glare_overlap"], 3),
        ))

    return distinct_coins


def _detect_card_candidates(
    gray: np.ndarray,
    config: AnchorDetectorConfig,
) -> List[_CandidateAnchor]:
    """Detects and characterizes ISO/IEC 7810 ID-1 rectangular card candidates with spatial deduplication."""
    h, w = gray.shape[:2]
    frame_area = float(h * w)

    blurred = cv2.GaussianBlur(gray, (5, 5), 1.0)
    edges = cv2.Canny(blurred, 30, 90)

    cnts, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return []

    raw_cards: List[dict] = []

    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area < (config.min_contour_area_px * 3.0) or area > (frame_area * 0.85):
            continue

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)

        if len(approx) != 4:
            continue

        if not cv2.isContourConvex(approx):
            continue

        ordered_corners = order_quadrilateral_corners(approx)

        # Compute side lengths: TL->TR, TR->BR, BR->BL, BL->TL
        p_tl, p_tr, p_br, p_bl = ordered_corners
        top_w = math.hypot(p_tr[0] - p_tl[0], p_tr[1] - p_tl[1])
        bot_w = math.hypot(p_br[0] - p_bl[0], p_br[1] - p_bl[1])
        left_h = math.hypot(p_bl[0] - p_tl[0], p_bl[1] - p_tl[1])
        right_h = math.hypot(p_br[0] - p_tr[0], p_br[1] - p_tr[1])

        avg_w = (top_w + bot_w) / 2.0
        avg_h = (left_h + right_h) / 2.0

        if avg_w <= 1.0 or avg_h <= 1.0:
            continue

        longer = max(avg_w, avg_h)
        shorter = min(avg_w, avg_h)
        aspect_ratio = longer / shorter

        # Target: 85.60 / 53.98 ≈ 1.58577
        ar_diff = abs(aspect_ratio - config.card_aspect_ratio_target)
        if ar_diff > config.card_aspect_ratio_tolerance:
            continue

        # Corner angle validation (each interior angle should be close to 90 deg)
        angles: List[float] = []
        pts_list = [p_tl, p_tr, p_br, p_bl]
        valid_angles = True

        for i in range(4):
            prev_p = pts_list[(i - 1) % 4]
            curr_p = pts_list[i]
            next_p = pts_list[(i + 1) % 4]

            v1 = (prev_p[0] - curr_p[0], prev_p[1] - curr_p[1])
            v2 = (next_p[0] - curr_p[0], next_p[1] - curr_p[1])

            len1 = math.hypot(v1[0], v1[1])
            len2 = math.hypot(v2[0], v2[1])
            if len1 <= 1e-4 or len2 <= 1e-4:
                valid_angles = False
                break

            cos_ang = (v1[0] * v2[0] + v1[1] * v2[1]) / (len1 * len2)
            cos_ang = max(-1.0, min(1.0, cos_ang))
            ang_deg = math.degrees(math.acos(cos_ang))
            angles.append(ang_deg)

            if ang_deg < config.card_min_corner_angle_deg or ang_deg > config.card_max_corner_angle_deg:
                valid_angles = False
                break

        if not valid_angles:
            continue

        edge_supp = _compute_edge_support_quadrilateral(gray, ordered_corners)

        # Scoring: Aligned 3-pillar geometric evidence (45% shape, 30% edge, 25% regularity)
        ar_score = max(0.0, 1.0 - (ar_diff / config.card_aspect_ratio_tolerance))
        mean_ang_dev = float(np.mean([abs(a - 90.0) for a in angles]))
        ang_score = max(0.0, 1.0 - (mean_ang_dev / 30.0))

        score = 0.45 * ar_score + 0.30 * edge_supp + 0.25 * ang_score

        # Border proximity check
        margin = 4
        on_border = any(
            pt[0] < margin or pt[0] > w - margin or pt[1] < margin or pt[1] > h - margin
            for pt in ordered_corners
        )
        if on_border:
            score = score * 0.70

        final_score = round(float(min(1.0, max(0.0, score))), 3)

        raw_cards.append({
            "corners": ordered_corners,
            "width_px": avg_w,
            "height_px": avg_h,
            "aspect_ratio": aspect_ratio,
            "score": final_score,
            "ar_score": ar_score,
            "edge_supp": edge_supp,
            "cx": (p_tl[0] + p_br[0]) / 2.0,
            "cy": (p_tl[1] + p_br[1]) / 2.0,
        })

    if not raw_cards:
        return []

    # Spatial Non-Maximum Suppression (suppresses parallel stroke edges of same card)
    raw_cards.sort(key=lambda c: c["score"], reverse=True)
    suppressed_cards: Set[int] = set()
    distinct_cards: List[_CandidateAnchor] = []

    for i in range(len(raw_cards)):
        if i in suppressed_cards:
            continue
        c1 = raw_cards[i]
        for j in range(i + 1, len(raw_cards)):
            c2 = raw_cards[j]
            dist = math.hypot(c1["cx"] - c2["cx"], c1["cy"] - c2["cy"])
            # If centroids are within 25% of card width, they are duplicate contours of the same card
            if dist < (0.25 * max(c1["width_px"], c2["width_px"])):
                suppressed_cards.add(j)

        geom = CardGeometry(
            corners=(
                (round(c1["corners"][0][0], 2), round(c1["corners"][0][1], 2)),
                (round(c1["corners"][1][0], 2), round(c1["corners"][1][1], 2)),
                (round(c1["corners"][2][0], 2), round(c1["corners"][2][1], 2)),
                (round(c1["corners"][3][0], 2), round(c1["corners"][3][1], 2)),
            ),
            width_px=round(c1["width_px"], 2),
            height_px=round(c1["height_px"], 2),
            aspect_ratio=round(c1["aspect_ratio"], 4),
        )

        distinct_cards.append(_CandidateAnchor(
            anchor_type=AnchorType.ID1_CARD,
            geometry=geom,
            score=c1["score"],
            fit_quality=round(c1["ar_score"], 3),
            edge_support=round(c1["edge_supp"], 3),
        ))

    return distinct_cards


def detect_anchor(
    image: Optional[np.ndarray],
    anchor_type: Optional[Union[AnchorType, str]] = None,
    config: Optional[AnchorDetectorConfig] = None,
    color_format: str = "BGR",
) -> AnchorDetectionResult:
    """
    Detects and characterizes physical metric reference anchors in the image frame.

    Pipeline:
    1. Input Validation: Strict handling of None, empty arrays, non-finite values, and small shapes.
    2. Conversion: Zero-mutation conversion to grayscale via nirikshak_vision.
    3. Dispatch:
       - anchor_type = COIN_INR_10 -> evaluates coin candidates only.
       - anchor_type = ID1_CARD    -> evaluates card candidates only.
       - anchor_type = None / AUTO -> evaluates both coin and card candidates.
    4. Deterministic Candidate Ranking: Sorts all candidates by composite explainable score.
    5. Confidence Gating BEFORE Ambiguity: Filters out candidates below min_confidence_threshold.
    6. Ambiguity Resolution: Compares top candidates; if score separation < margin, returns AMBIGUOUS_ANCHOR.
    7. Minimal Contract: Emits typed AnchorDetectionResult without scale fabrication.

    Returns:
        AnchorDetectionResult
    """
    if config is None:
        config = AnchorDetectorConfig()

    # 1. Input Validation
    if image is None:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message="Input image is None.",
        )

    if not isinstance(image, np.ndarray):
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Input must be a numpy.ndarray, got {type(image).__name__}.",
        )

    if image.size == 0:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message="Input image array is empty (0 pixels).",
        )

    if np.issubdtype(image.dtype, np.floating):
        if np.isnan(image).any() or np.isinf(image).any():
            return AnchorDetectionResult(
                detected=False,
                anchor_type=None,
                status=AnchorDetectionStatus.INVALID_INPUT,
                confidence=0.0,
                message="Input image contains non-finite values (NaN or Inf).",
            )

    if image.ndim not in (2, 3):
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Invalid image dimensions: {image.ndim}D. Expected 2D or 3D array.",
        )

    if image.shape[0] < 10 or image.shape[1] < 10:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Image resolution too small ({image.shape[0]}x{image.shape[1]}). Minimum 10x10 required.",
        )

    if image.ndim == 3 and image.shape[2] not in (1, 3, 4):
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Unsupported color channels: {image.shape[2]}. Expected 1, 3, or 4.",
        )

    # 2. Grayscale Conversion
    try:
        gray = convert_to_grayscale(image, color_format=color_format)
    except Exception as exc:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Failed to convert image to grayscale: {str(exc)}",
        )

    # Specular glare candidate mask (used as glare-overlap detector)
    glare_mask = (gray >= 250)

    # 3. Mode Dispatch
    target_type: Optional[str] = None
    if anchor_type is not None:
        if isinstance(anchor_type, AnchorType):
            target_type = anchor_type.value
        else:
            target_type = str(anchor_type).upper()

    candidates: List[_CandidateAnchor] = []

    if target_type == AnchorType.COIN_INR_10.value:
        candidates = _detect_coin_candidates(gray, config, glare_mask)
    elif target_type == AnchorType.ID1_CARD.value:
        candidates = _detect_card_candidates(gray, config)
    elif target_type in (None, "AUTO", "NONE"):
        # Auto mode: both coin and card candidates compete
        coin_cands = _detect_coin_candidates(gray, config, glare_mask)
        card_cands = _detect_card_candidates(gray, config)
        candidates = coin_cands + card_cands
    else:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.INVALID_INPUT,
            confidence=0.0,
            message=f"Unknown anchor_type requested: '{anchor_type}'.",
        )

    # 4. Deterministic Candidate Ranking (never OpenCV contour order, never candidates[0])
    ranked = sorted(candidates, key=lambda c: c.score, reverse=True)

    # 5. Confidence Gating BEFORE Ambiguity Scoring
    credible = [c for c in ranked if c.score >= config.min_confidence_threshold]

    if len(credible) == 0:
        if len(ranked) > 0:
            top = ranked[0]
            # Check if rejection was due to glare interference
            if top.glare_overlap > config.max_glare_overlap_ratio:
                return AnchorDetectionResult(
                    detected=False,
                    anchor_type=top.anchor_type,
                    status=AnchorDetectionStatus.GLARE_INTERFERENCE,
                    confidence=top.score,
                    message=f"Specular glare overlap ({top.glare_overlap:.1%}) corrupted candidate geometry.",
                )
            return AnchorDetectionResult(
                detected=False,
                anchor_type=top.anchor_type,
                status=AnchorDetectionStatus.LOW_CONFIDENCE,
                confidence=top.score,
                message=f"Candidate confidence ({top.score:.2f}) below threshold ({config.min_confidence_threshold:.2f}).",
            )
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.NO_ANCHOR,
            confidence=0.0,
            message="No plausible reference anchor candidates detected in frame.",
        )

    # Exactly one credible candidate passes confidence gate
    if len(credible) == 1:
        winner = credible[0]
        return AnchorDetectionResult(
            detected=True,
            anchor_type=winner.anchor_type,
            status=AnchorDetectionStatus.SUCCESS,
            confidence=winner.score,
            geometry=winner.geometry,
            fit_quality=winner.fit_quality,
            ring_information=winner.ring_info,
            message="Metric reference anchor successfully detected.",
        )

    # 6. Ambiguity Resolution (multiple credible candidates compete)
    c1 = credible[0]
    c2 = credible[1]
    score_delta = c1.score - c2.score

    if score_delta < config.ambiguity_confidence_margin:
        return AnchorDetectionResult(
            detected=False,
            anchor_type=None,
            status=AnchorDetectionStatus.AMBIGUOUS_ANCHOR,
            confidence=c1.score,
            message=(
                f"Ambiguous anchor: top candidates have indistinguishable scores "
                f"({c1.score:.2f} vs {c2.score:.2f}, delta {score_delta:.3f} < margin {config.ambiguity_confidence_margin:.2f}). "
                "False calibration rejected."
            ),
        )

    # Winner clearly separates from runner-up
    return AnchorDetectionResult(
        detected=True,
        anchor_type=c1.anchor_type,
        status=AnchorDetectionStatus.SUCCESS,
        confidence=c1.score,
        geometry=c1.geometry,
        fit_quality=c1.fit_quality,
        ring_information=c1.ring_info,
        message="Metric reference anchor successfully detected after ambiguity resolution.",
    )
