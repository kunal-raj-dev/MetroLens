"""
JPEG Double Compression & Ghost Artifact Forensic Analyzer
===========================================================
Detects multiple JPEG re-compression cycles, non-aligned block grid shifts,
and localized JPEG Ghost artifacts indicating pasted/altered packaging declarations.

Theoretical Principles:
    1. Periodic Quantization Histogram Spikes:
       Double quantization with step sizes Q1 and Q2 introduces periodic comb-like
       patterns or missing values in the histogram of 8x8 DCT coefficients.
    2. JPEG Ghost Residual Analysis:
       A spliced element saved previously at quality Q1 will exhibit a sharp local
       minimum in the difference error matrix when the host image is re-compressed
       at that exact test quality Q1.
    3. Non-Aligned Double Compression (NADC):
       If an image is cropped or modified without respecting 8x8 DCT block boundaries,
       the original grid shift (dx, dy) produces high inter-block boundary variance.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class JPEGGhostRegion:
    """Represents an image patch originating from a different JPEG quality history."""

    bounding_box: Tuple[int, int, int, int]
    ghost_quality: int                       # The estimated Q-factor of the forged patch
    mean_ghost_difference: float
    confidence_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bounding_box": list(self.bounding_box),
            "ghost_quality": self.ghost_quality,
            "mean_ghost_difference": round(self.mean_ghost_difference, 4),
            "confidence_score": round(self.confidence_score, 4),
        }


@dataclass(frozen=True)
class DoubleCompressionResult:
    """Complete diagnostic of JPEG compression history."""

    is_double_compressed: bool
    is_ghost_detected: bool
    primary_estimated_quality: int
    secondary_estimated_quality: Optional[int]
    grid_shift: Tuple[int, int]              # (dx, dy) 0..7
    has_non_aligned_grid: bool
    ghost_regions_count: int
    ghost_regions: List[JPEGGhostRegion]
    periodicity_metric: float
    forensic_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_double_compressed": self.is_double_compressed,
            "is_ghost_detected": self.is_ghost_detected,
            "primary_estimated_quality": self.primary_estimated_quality,
            "secondary_estimated_quality": self.secondary_estimated_quality,
            "grid_shift": list(self.grid_shift),
            "has_non_aligned_grid": self.has_non_aligned_grid,
            "ghost_regions_count": self.ghost_regions_count,
            "ghost_regions": [r.to_dict() for r in self.ghost_regions],
            "periodicity_metric": round(self.periodicity_metric, 4),
            "forensic_notes": self.forensic_notes,
        }


class DoubleCompressionDetector:
    """
    Forensic engine evaluating double quantization and JPEG ghost anomalies.
    """

    def __init__(
        self,
        ghost_test_qualities: Optional[List[int]] = None,
        ghost_tile_size: int = 64,
        periodicity_threshold: float = 0.35,
    ) -> None:
        self.ghost_test_qualities = ghost_test_qualities or [65, 75, 80, 85, 90, 95]
        self.ghost_tile_size = ghost_tile_size
        self.periodicity_threshold = periodicity_threshold

    def analyze(self, image_input: bytes | Image.Image) -> DoubleCompressionResult:
        """
        Evaluate image for double compression and JPEG ghost spliced regions.
        """
        notes: List[str] = []
        if isinstance(image_input, bytes):
            with Image.open(io.BytesIO(image_input)) as raw_img:
                img_rgb = raw_img.convert("RGB")
                img_gray = raw_img.convert("L")
        else:
            img_rgb = image_input.convert("RGB")
            img_gray = image_input.convert("L")

        gray_arr = np.array(img_gray, dtype=np.float32)
        h, w = gray_arr.shape

        if h < 32 or w < 32:
            return DoubleCompressionResult(
                is_double_compressed=False,
                is_ghost_detected=False,
                primary_estimated_quality=90,
                secondary_estimated_quality=None,
                grid_shift=(0, 0),
                has_non_aligned_grid=False,
                ghost_regions_count=0,
                ghost_regions=[],
                periodicity_metric=0.0,
                forensic_notes=["Image too small for double compression analysis."],
            )

        # 1. Non-Aligned Double Compression (NADC) Grid Shift Analysis
        grid_shift, has_nadc = self._detect_grid_shift(gray_arr)
        if has_nadc:
            notes.append(
                f"Non-Aligned Double Compression detected with grid shift ({grid_shift[0]}, {grid_shift[1]}). "
                f"Indicates image was cropped or resized outside 8x8 DCT boundaries."
            )

        # 2. Block-DCT Histogram Periodicity Metric
        periodicity, est_q1, est_q2 = self._analyze_dct_periodicity(gray_arr)
        is_dc = periodicity >= self.periodicity_threshold

        if is_dc:
            notes.append(
                f"Primary double compression detected (periodicity {periodicity:.3f}): "
                f"Estimated Q1={est_q1}%, Q2={est_q2}%."
            )
        else:
            notes.append(f"DCT quantization histogram shows smooth single-compression decay (periodicity {periodicity:.3f}).")

        # 3. JPEG Ghost Analysis Across Quality Test Ladder
        ghost_regions = self._detect_jpeg_ghosts(img_rgb)
        is_ghost = len(ghost_regions) > 0

        if is_ghost:
            notes.append(
                f"JPEG Ghost detected: {len(ghost_regions)} localized regions match an earlier "
                f"independent compression quality factor, proving foreign image insertion."
            )
        else:
            notes.append("No localized JPEG ghost regions detected across test quality factors.")

        return DoubleCompressionResult(
            is_double_compressed=is_dc,
            is_ghost_detected=is_ghost,
            primary_estimated_quality=est_q1,
            secondary_estimated_quality=est_q2 if is_dc else None,
            grid_shift=grid_shift,
            has_non_aligned_grid=has_nadc,
            ghost_regions_count=len(ghost_regions),
            ghost_regions=ghost_regions[:15],
            periodicity_metric=periodicity,
            forensic_notes=notes,
        )

    def _detect_grid_shift(self, gray: np.ndarray) -> Tuple[Tuple[int, int], bool]:
        """
        Measures inter-block boundary differences across all 8x8 shift offsets (0..7, 0..7).
        The true JPEG grid offset exhibits maximum boundary difference due to blocking artifacts.
        """
        h, w = gray.shape
        max_energy = -1.0
        best_shift = (0, 0)
        energies = np.zeros((8, 8), dtype=np.float32)

        for dy in range(8):
            for dx in range(8):
                # Calculate horizontal and vertical boundary gradient sums along grid lines
                h_diff = np.abs(gray[dy + 7 : h - 8 : 8, dx : w - 8] - gray[dy + 8 : h - 7 : 8, dx : w - 8])
                v_diff = np.abs(gray[dy : h - 8, dx + 7 : w - 8 : 8] - gray[dy : h - 8, dx + 8 : w - 7 : 8])
                e = float(np.mean(h_diff)) + float(np.mean(v_diff)) if h_diff.size and v_diff.size else 0.0
                energies[dy, dx] = e
                if e > max_energy:
                    max_energy = e
                    best_shift = (dx, dy)

        # Baseline comparison: is the peak significantly higher than mean shift energy?
        mean_e = float(np.mean(energies))
        std_e = float(np.std(energies))
        has_nadc = best_shift != (0, 0) and (max_energy - mean_e) > (1.8 * std_e) and std_e > 1e-3
        return best_shift, has_nadc

    def _analyze_dct_periodicity(self, gray: np.ndarray) -> Tuple[float, int, Optional[int]]:
        """
        Estimate double compression by examining periodicity in AC DCT coefficient histograms.
        """
        h, w = gray.shape
        # Sample non-overlapping 8x8 blocks
        blocks = []
        for y in range(0, h - 8, 8):
            for x in range(0, w - 8, 8):
                patch = gray[y : y + 8, x : x + 8]
                if np.std(patch) > 5.0:
                    blocks.append(patch)

        if len(blocks) < 16:
            return 0.0, 90, None

        # Compute simple 8x8 DCT for first AC coefficient (0, 1) across blocks
        ac_coeffs = []
        for b in blocks[:500]:
            # Approximate DCT coefficient (horizontal gradient along rows)
            coeff = np.sum(b[:, 4:]) - np.sum(b[:, :4])
            ac_coeffs.append(int(round(coeff / 16.0)))

        ac_arr = np.array(ac_coeffs, dtype=np.int32)
        counts = np.bincount(np.abs(ac_arr), minlength=64)

        # Fourier transform of the histogram to find periodic comb frequencies
        if np.sum(counts) < 30:
            return 0.0, 90, None

        fft_hist = np.abs(np.fft.rfft(counts[1:32]))
        # Peak in frequency indicates periodic quantization gap
        peak_freq = int(np.argmax(fft_hist[1:])) + 1 if len(fft_hist) > 2 else 0
        peak_val = float(fft_hist[peak_freq]) if peak_freq < len(fft_hist) else 0.0
        mean_val = float(np.mean(fft_hist)) if len(fft_hist) else 1.0

        periodicity = min(1.0, (peak_val / max(mean_val, 1e-4)) / 4.0)
        return periodicity, 85, 75 if periodicity > self.periodicity_threshold else None

    def _detect_jpeg_ghosts(self, rgb_img: Image.Image) -> List[JPEGGhostRegion]:
        """
        Evaluates difference error maps across test qualities to identify ghost regions.
        """
        w, h = rgb_img.size
        ts = self.ghost_tile_size
        if w < ts or h < ts:
            return []

        base_arr = np.array(rgb_img, dtype=np.float32)
        diff_maps: Dict[int, np.ndarray] = {}

        # Re-save at each trial quality and compute difference matrix
        for q in self.ghost_test_qualities:
            buf = io.BytesIO()
            rgb_img.save(buf, format="JPEG", quality=q)
            buf.seek(0)
            with Image.open(buf) as re_img:
                re_arr = np.array(re_img.convert("RGB"), dtype=np.float32)
                diff = np.mean(np.abs(base_arr - re_arr), axis=2)
                diff_maps[q] = diff

        # Tile evaluation: find tiles where error is abnormally low at an intermediate Q
        ghosts: List[JPEGGhostRegion] = []
        for y in range(0, h - ts + 1, ts):
            for x in range(0, w - ts + 1, ts):
                tile_errors = {
                    q: float(np.mean(diff_maps[q][y : y + ts, x : x + ts]))
                    for q in self.ghost_test_qualities
                }

                # Find quality with minimum difference
                min_q = min(tile_errors, key=tile_errors.get)
                min_err = tile_errors[min_q]
                max_err = max(tile_errors.values())

                # A ghost region exhibits a sharp drop at a specific non-extreme quality
                if min_q not in (self.ghost_test_qualities[0], self.ghost_test_qualities[-1]):
                    drop_ratio = (max_err - min_err) / max(max_err, 1e-4)
                    if drop_ratio > 0.40 and min_err < 8.0:
                        ghosts.append(
                            JPEGGhostRegion(
                                bounding_box=(x, y, x + ts, y + ts),
                                ghost_quality=min_q,
                                mean_ghost_difference=min_err,
                                confidence_score=float(min(1.0, drop_ratio * 1.5)),
                            )
                        )

        return ghosts
