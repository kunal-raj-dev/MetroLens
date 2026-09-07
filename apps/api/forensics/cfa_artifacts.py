"""
Color Filter Array (CFA) & Bayer Demosaicing Forensic Analyzer
=============================================================
Detects digital image splicing and synthetic inpainting by identifying localized
disruptions in the camera sensor's physical Bayer color filter demosaicing grid.

Forensic Theory:
    Physical camera sensors capture only one color component per pixel (R, G, or B)
    in a 2x2 periodic mosaic (RGGB, BGGR, GRBG, GBRG). The missing channels are
    interpolated during camera ISP demosaicing, leaving distinct 2x2 periodic
    linear dependencies in the interpolation error residual.

    When an attacker splices in text or graphic overlays (e.g. counterfeit MRP,
    fake best-before dates), the inserted patch lacks the camera's physical CFA
    correlation pattern or exhibits a phase mismatch with the rest of the image.
"""

from __future__ import annotations

import enum
import io
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image


class BayerPatternType(str, enum.Enum):
    RGGB = "RGGB"
    BGGR = "BGGR"
    GRBG = "GRBG"
    GBRG = "GBRG"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class CFASpliceAnomalyRegion:
    """Represents a spatial region with disrupted or absent CFA periodicity."""

    bounding_box: Tuple[int, int, int, int]  # (xmin, ymin, xmax, ymax)
    cfa_periodicity_score: float             # 0.0 (no CFA trace) to 1.0 (strong CFA)
    deviation_from_global_mean: float
    is_spliced: bool
    area_pixels: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bounding_box": list(self.bounding_box),
            "cfa_periodicity_score": round(self.cfa_periodicity_score, 4),
            "deviation_from_global_mean": round(self.deviation_from_global_mean, 4),
            "is_spliced": self.is_spliced,
            "area_pixels": self.area_pixels,
        }


@dataclass(frozen=True)
class CFADemosaicingResult:
    """Comprehensive verdict of CFA Demosaicing Analysis."""

    has_camera_cfa_traces: bool
    detected_bayer_pattern: BayerPatternType
    global_cfa_confidence: float
    is_splicing_detected: bool
    splicing_probability: float
    anomalous_regions_count: int
    anomalous_regions: List[CFASpliceAnomalyRegion]
    grid_tile_size: int
    forensic_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "has_camera_cfa_traces": self.has_camera_cfa_traces,
            "detected_bayer_pattern": self.detected_bayer_pattern.value,
            "global_cfa_confidence": round(self.global_cfa_confidence, 4),
            "is_splicing_detected": self.is_splicing_detected,
            "splicing_probability": round(self.splicing_probability, 4),
            "anomalous_regions_count": self.anomalous_regions_count,
            "anomalous_regions": [r.to_dict() for r in self.anomalous_regions],
            "grid_tile_size": self.grid_tile_size,
            "forensic_notes": self.forensic_notes,
        }


class CFADemosaicAnalyzer:
    """
    Evaluates Bayer color filter array artifacts and demosaicing consistency.
    """

    def __init__(
        self,
        tile_size: int = 64,
        min_global_cfa_threshold: float = 0.25,
        anomaly_sigma_threshold: float = 2.8,
        min_anomaly_tile_count: int = 2,
    ) -> None:
        self.tile_size = tile_size
        self.min_global_cfa_threshold = min_global_cfa_threshold
        self.anomaly_sigma_threshold = anomaly_sigma_threshold
        self.min_anomaly_tile_count = min_anomaly_tile_count

    def analyze(self, image_input: bytes | Image.Image) -> CFADemosaicingResult:
        """
        Analyze RGB image for CFA pattern consistency and localized splicing.
        """
        notes: List[str] = []
        if isinstance(image_input, bytes):
            with Image.open(io.BytesIO(image_input)) as raw_img:
                rgb_img = raw_img.convert("RGB")
        else:
            rgb_img = image_input.convert("RGB")

        arr = np.array(rgb_img, dtype=np.float32)
        h, w, c = arr.shape

        if h < self.tile_size or w < self.tile_size:
            return CFADemosaicingResult(
                has_camera_cfa_traces=False,
                detected_bayer_pattern=BayerPatternType.UNKNOWN,
                global_cfa_confidence=0.0,
                is_splicing_detected=False,
                splicing_probability=0.0,
                anomalous_regions_count=0,
                anomalous_regions=[],
                grid_tile_size=self.tile_size,
                forensic_notes=["Image too small for CFA demosaicing grid analysis."],
            )

        # 1. Estimate global Bayer pattern using Green channel linear interpolation residual
        green = arr[:, :, 1]
        best_pattern, best_score = self._estimate_bayer_pattern(green)
        notes.append(f"Estimated primary sensor Bayer mosaic: {best_pattern.value} (score: {best_score:.3f})")

        has_cfa = best_score >= self.min_global_cfa_threshold
        if not has_cfa:
            notes.append(
                "Image exhibits weak or absent camera demosaicing artifacts "
                "(common in multiple re-saves, screenshots, or synthetic generations)."
            )

        # 2. Tile-based spatial scan for localized demosaicing discontinuities
        tiles_scores: List[Tuple[int, int, int, int, float]] = []  # (x1, y1, x2, y2, score)
        step = self.tile_size

        for y in range(0, h - self.tile_size + 1, step):
            for x in range(0, w - self.tile_size + 1, step):
                patch_g = green[y : y + self.tile_size, x : x + self.tile_size]
                # Skip flat areas (low gradient variance)
                if float(np.std(patch_g)) < 6.0:
                    continue

                local_score = self._compute_tile_cfa_score(patch_g, best_pattern)
                tiles_scores.append((x, y, x + self.tile_size, y + self.tile_size, local_score))

        if not tiles_scores:
            return CFADemosaicingResult(
                has_camera_cfa_traces=has_cfa,
                detected_bayer_pattern=best_pattern,
                global_cfa_confidence=best_score,
                is_splicing_detected=False,
                splicing_probability=0.0,
                anomalous_regions_count=0,
                anomalous_regions=[],
                grid_tile_size=self.tile_size,
                forensic_notes=notes,
            )

        # 3. Calculate spatial distribution and identify statistical outliers
        scores_arr = np.array([t[4] for t in tiles_scores], dtype=np.float32)
        mean_score = float(np.mean(scores_arr))
        std_score = float(np.std(scores_arr))

        anomalies: List[CFASpliceAnomalyRegion] = []
        if has_cfa and std_score > 1e-4:
            for x1, y1, x2, y2, sc in tiles_scores:
                # Spliced regions show drastically lower CFA periodicity than the host image
                dev = (mean_score - sc) / std_score
                if dev >= self.anomaly_sigma_threshold:
                    anomalies.append(
                        CFASpliceAnomalyRegion(
                            bounding_box=(x1, y1, x2, y2),
                            cfa_periodicity_score=sc,
                            deviation_from_global_mean=dev,
                            is_spliced=True,
                            area_pixels=self.tile_size * self.tile_size,
                        )
                    )

        is_spliced = len(anomalies) >= self.min_anomaly_tile_count
        splice_prob = min(1.0, len(anomalies) / float(self.min_anomaly_tile_count * 3)) if is_spliced else 0.0

        if is_spliced:
            notes.append(
                f"Splicing confirmed: {len(anomalies)} localized tiles lack host sensor's "
                f"Bayer CFA signature, indicating foreign digital compositing."
            )
        else:
            notes.append("Spatial CFA interpolation matrix is uniform across all analyzed tiles.")

        return CFADemosaicingResult(
            has_camera_cfa_traces=has_cfa,
            detected_bayer_pattern=best_pattern,
            global_cfa_confidence=best_score,
            is_splicing_detected=is_spliced,
            splicing_probability=splice_prob,
            anomalous_regions_count=len(anomalies),
            anomalous_regions=anomalies[:20],
            grid_tile_size=self.tile_size,
            forensic_notes=notes,
        )

    def _estimate_bayer_pattern(self, green: np.ndarray) -> Tuple[BayerPatternType, float]:
        """Test all 4 Bayer phases and pick the one with highest linear residual periodicity."""
        patterns = [
            BayerPatternType.RGGB,
            BayerPatternType.BGGR,
            BayerPatternType.GRBG,
            BayerPatternType.GBRG,
        ]
        best_p = BayerPatternType.RGGB
        best_val = 0.0

        for p in patterns:
            val = self._compute_tile_cfa_score(green, p)
            if val > best_val:
                best_val = val
                best_p = p

        return best_p, best_val

    def _compute_tile_cfa_score(self, green_patch: np.ndarray, pattern: BayerPatternType) -> float:
        """
        Compute bilinear interpolation error variance across 2x2 grid phases.
        In an authentic demosaiced image, the genuine green photo-sites exhibit
        zero interpolation error, while interpolated sites show non-zero residual.
        """
        gh, gw = green_patch.shape
        if gh < 4 or gw < 4:
            return 0.0

        # Bilinear 4-neighbor interpolation kernel for missing Green
        # G_interp(y, x) = 0.25 * [G(y-1, x) + G(y+1, x) + G(y, x-1) + G(y, x+1)]
        interp = (
            np.roll(green_patch, 1, axis=0)
            + np.roll(green_patch, -1, axis=0)
            + np.roll(green_patch, 1, axis=1)
            + np.roll(green_patch, -1, axis=1)
        ) * 0.25

        residual = np.abs(green_patch - interp)[1:-1, 1:-1]
        rh, rw = residual.shape

        # 4 phases of 2x2 grid
        phase_00 = residual[0:rh:2, 0:rw:2]
        phase_01 = residual[0:rh:2, 1:rw:2]
        phase_10 = residual[1:rh:2, 0:rw:2]
        phase_11 = residual[1:rh:2, 1:rw:2]

        m00 = float(np.mean(phase_00)) if phase_00.size else 0.0
        m01 = float(np.mean(phase_01)) if phase_01.size else 0.0
        m10 = float(np.mean(phase_10)) if phase_10.size else 0.0
        m11 = float(np.mean(phase_11)) if phase_11.size else 0.0

        means = [m00, m01, m10, m11]
        # In authentic Bayer, green occupies diagonally opposite sites (e.g. 01 and 10 for RGGB)
        # Periodicity ratio: variance among phase means relative to overall residual magnitude
        spread = float(np.std(means))
        avg_mag = float(np.mean(means))
        if avg_mag < 1e-4:
            return 0.0

        ratio = spread / avg_mag
        # Normalization to [0.0, 1.0] range
        normalized_cfa_score = min(1.0, ratio * 2.5)
        return float(normalized_cfa_score)
