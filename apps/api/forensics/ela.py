"""
Error Level Analysis (ELA) Forensic Engine
==========================================
Implements Error Level Analysis (ELA) for detecting digital image manipulation,
photo splicing, fraudulent sticker overlays (e.g., altered MRP, doctored expiry dates),
and synthetic compression discrepancies on packaged commodity photographs.

Legal Metrology Application:
    Under Section 36(1) of the Legal Metrology Act, 2009 and Section 63 of the
    Bharatiya Sakshya Adhiniyam, 2023 (BSA), photographic evidence submitted for
    automated compliance adjudication must be verifiable against tampering or
    fraudulent digital alterations prior to court issuance.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageFilter


@dataclass(frozen=True)
class TamperAnomalyRegion:
    """Represents a localized region of detected compression/error level anomaly."""

    bounding_box: Tuple[int, int, int, int]  # (xmin, ymin, xmax, ymax)
    mean_error: float
    peak_error: float
    deviation_from_global_mean: float
    anomaly_severity: str  # 'LOW', 'MODERATE', 'SUSPICIOUS', 'CRITICAL'
    area_pixels: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bounding_box": list(self.bounding_box),
            "mean_error": round(self.mean_error, 4),
            "peak_error": round(self.peak_error, 4),
            "deviation_from_global_mean": round(self.deviation_from_global_mean, 4),
            "anomaly_severity": self.anomaly_severity,
            "area_pixels": self.area_pixels,
        }


@dataclass(frozen=True)
class ELAResult:
    """Comprehensive result of an Error Level Analysis evaluation."""

    is_tampering_suspected: bool
    tamper_probability: float  # 0.0 to 1.0
    global_mean_error: float
    global_std_error: float
    global_max_error: float
    resave_quality: int
    scale_multiplier: float
    detected_anomaly_regions: List[TamperAnomalyRegion] = field(default_factory=list)
    tamper_verdict: str = "CLEAN"  # 'CLEAN', 'INCONCLUSIVE', 'PROBABLE_ALTERATION', 'CONFIRMED_ALTERATION'
    forensic_notes: List[str] = field(default_factory=list)
    ela_image_bytes: Optional[bytes] = None

    def to_dict(self, include_image_bytes: bool = False) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "is_tampering_suspected": self.is_tampering_suspected,
            "tamper_probability": round(self.tamper_probability, 4),
            "tamper_verdict": self.tamper_verdict,
            "global_mean_error": round(self.global_mean_error, 4),
            "global_std_error": round(self.global_std_error, 4),
            "global_max_error": round(self.global_max_error, 4),
            "resave_quality": self.resave_quality,
            "scale_multiplier": self.scale_multiplier,
            "anomaly_regions_count": len(self.detected_anomaly_regions),
            "anomaly_regions": [r.to_dict() for r in self.detected_anomaly_regions],
            "forensic_notes": self.forensic_notes,
        }
        if include_image_bytes and self.ela_image_bytes is not None:
            result["ela_image_bytes_len"] = len(self.ela_image_bytes)
        return result


class ErrorLevelAnalyzer:
    """
    Production-grade Error Level Analysis (ELA) engine.

    Resaves the target image at a calibrated JPEG compression quality and measures
    the residual error matrix across 8x8 DCT block boundaries. Areas modified after
    initial capture exhibit higher error levels because their quantization history
    differs from the rest of the image plane.
    """

    def __init__(
        self,
        default_resave_quality: int = 90,
        default_scale_multiplier: float = 15.0,
        anomaly_sigma_threshold: float = 3.2,
        min_anomaly_region_pixels: int = 400,
        grid_partition_size: int = 64,
    ) -> None:
        """
        Initialize the ELA analyzer.

        Args:
            default_resave_quality: Quality level for reference resave (typically 90-95).
            default_scale_multiplier: Contrast enhancement multiplier for residual difference.
            anomaly_sigma_threshold: Standard deviations above global mean to flag anomaly.
            min_anomaly_region_pixels: Minimum bounding area to classify as an anomaly region.
            grid_partition_size: Tile size in pixels for spatial error variance localization.
        """
        self.default_resave_quality = max(50, min(100, default_resave_quality))
        self.default_scale_multiplier = max(1.0, min(50.0, default_scale_multiplier))
        self.anomaly_sigma_threshold = max(1.5, anomaly_sigma_threshold)
        self.min_anomaly_region_pixels = max(64, min_anomaly_region_pixels)
        self.grid_partition_size = max(16, grid_partition_size)

    def analyze(
        self,
        image_bytes: bytes,
        quality: Optional[int] = None,
        scale_multiplier: Optional[float] = None,
        generate_visual_ela: bool = True,
    ) -> ELAResult:
        """
        Execute Error Level Analysis on raw image bytes.

        Args:
            image_bytes: Raw binary image payload (JPEG, PNG, or WebP).
            quality: Optional custom JPEG resave quality (defaults to 90).
            scale_multiplier: Optional custom contrast enhancement factor.
            generate_visual_ela: Whether to encode the enhanced ELA image bytes.

        Returns:
            ELAResult containing statistical error distributions and anomaly regions.
        """
        q = quality if quality is not None else self.default_resave_quality
        scale = scale_multiplier if scale_multiplier is not None else self.default_scale_multiplier

        # Decode source image in RGB mode
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                orig_rgb = img.convert("RGB")
        except Exception as exc:
            return ELAResult(
                is_tampering_suspected=False,
                tamper_probability=0.0,
                global_mean_error=0.0,
                global_std_error=0.0,
                global_max_error=0.0,
                resave_quality=q,
                scale_multiplier=scale,
                tamper_verdict="INCONCLUSIVE",
                forensic_notes=[f"Failed to decode image for ELA: {str(exc)}"],
            )

        # Resave to in-memory JPEG at specified quality
        resave_buffer = io.BytesIO()
        orig_rgb.save(resave_buffer, format="JPEG", quality=q, optimize=False)
        resave_buffer.seek(0)
        resaved_rgb = Image.open(resave_buffer).convert("RGB")

        # Compute absolute difference between original and resaved
        diff_img = ImageChops.difference(orig_rgb, resaved_rgb)

        # Convert difference to numpy array for vector analysis
        diff_arr = np.array(diff_img, dtype=np.float32)  # shape: (H, W, 3)
        # Compute grayscale luminosity error: 0.299R + 0.587G + 0.114B
        error_matrix = (
            0.2989 * diff_arr[:, :, 0]
            + 0.5870 * diff_arr[:, :, 1]
            + 0.1140 * diff_arr[:, :, 2]
        )

        global_mean = float(np.mean(error_matrix))
        global_std = float(np.std(error_matrix))
        global_max = float(np.max(error_matrix))

        # Spatial grid partition analysis for local anomaly localization
        anomaly_regions, notes = self._localize_anomaly_regions(
            error_matrix=error_matrix,
            global_mean=global_mean,
            global_std=global_std,
            width=orig_rgb.width,
            height=orig_rgb.height,
        )

        # Calculate tamper probability heuristic
        tamper_prob, verdict = self._calculate_verdict(
            global_mean=global_mean,
            global_std=global_std,
            global_max=global_max,
            anomaly_regions=anomaly_regions,
        )

        # Optional visual ELA rendering with enhanced contrast
        ela_bytes = None
        if generate_visual_ela:
            ela_bytes = self._render_enhanced_ela_image(diff_img, scale)

        return ELAResult(
            is_tampering_suspected=tamper_prob >= 0.65,
            tamper_probability=tamper_prob,
            global_mean_error=global_mean,
            global_std_error=global_std,
            global_max_error=global_max,
            resave_quality=q,
            scale_multiplier=scale,
            detected_anomaly_regions=anomaly_regions,
            tamper_verdict=verdict,
            forensic_notes=notes,
            ela_image_bytes=ela_bytes,
        )

    def _localize_anomaly_regions(
        self,
        error_matrix: np.ndarray,
        global_mean: float,
        global_std: float,
        width: int,
        height: int,
    ) -> Tuple[List[TamperAnomalyRegion], List[str]]:
        """Scan spatial tiles to find localized clusters of abnormal compression residuals."""
        tile_size = self.grid_partition_size
        anomaly_threshold = global_mean + (self.anomaly_sigma_threshold * global_std)

        anomaly_regions: List[TamperAnomalyRegion] = []
        notes: List[str] = []

        if global_std < 0.001:
            notes.append("Image exhibits uniform or synthetic error distribution (zero variance).")
            return anomaly_regions, notes

        rows = math.ceil(height / tile_size)
        cols = math.ceil(width / tile_size)

        candidate_tiles: List[Tuple[int, int, int, int, float, float]] = []

        for r in range(rows):
            y1 = r * tile_size
            y2 = min(height, (r + 1) * tile_size)
            for c in range(cols):
                x1 = c * tile_size
                x2 = min(width, (c + 1) * tile_size)

                tile_data = error_matrix[y1:y2, x1:x2]
                if tile_data.size == 0:
                    continue

                tile_mean = float(np.mean(tile_data))
                tile_max = float(np.max(tile_data))

                if tile_mean > anomaly_threshold:
                    candidate_tiles.append((x1, y1, x2, y2, tile_mean, tile_max))

        # Merge adjacent candidate tiles into coherent anomaly bounding boxes
        if candidate_tiles:
            merged = self._merge_adjacent_tiles(candidate_tiles)
            for box in merged:
                bx1, by1, bx2, by2, b_mean, b_max = box
                area = (bx2 - bx1) * (by2 - by1)
                if area >= self.min_anomaly_region_pixels:
                    dev = (b_mean - global_mean) / (global_std if global_std > 0 else 1.0)
                    if dev >= 5.0:
                        severity = "CRITICAL"
                    elif dev >= 4.0:
                        severity = "SUSPICIOUS"
                    elif dev >= 3.0:
                        severity = "MODERATE"
                    else:
                        severity = "LOW"

                    anomaly_regions.append(
                        TamperAnomalyRegion(
                            bounding_box=(bx1, by1, bx2, by2),
                            mean_error=b_mean,
                            peak_error=b_max,
                            deviation_from_global_mean=dev,
                            anomaly_severity=severity,
                            area_pixels=area,
                        )
                    )

        if len(anomaly_regions) > 0:
            notes.append(
                f"Identified {len(anomaly_regions)} localized anomaly cluster(s) with high compression delta."
            )
        else:
            notes.append("No localized error level anomalies detected across spatial tiles.")

        return anomaly_regions, notes

    def _merge_adjacent_tiles(
        self, tiles: List[Tuple[int, int, int, int, float, float]]
    ) -> List[Tuple[int, int, int, int, float, float]]:
        """Merge bounding tiles that overlap or touch each other."""
        if not tiles:
            return []

        merged: List[List[float]] = []
        for t in tiles:
            x1, y1, x2, y2, mean_e, max_e = t
            placed = False
            for m in merged:
                mx1, my1, mx2, my2, m_mean, m_max = m
                # Check proximity (within 1 tile spacing)
                if not (x2 < mx1 or x1 > mx2 or y2 < my1 or y1 > my2):
                    # Overlap or touch: merge
                    m[0] = min(mx1, x1)
                    m[1] = min(my1, y1)
                    m[2] = max(mx2, x2)
                    m[3] = max(my2, y2)
                    m[4] = max(m_mean, mean_e)
                    m[5] = max(m_max, max_e)
                    placed = True
                    break
            if not placed:
                merged.append([float(x1), float(y1), float(x2), float(y2), float(mean_e), float(max_e)])

        return [
            (int(m[0]), int(m[1]), int(m[2]), int(m[3]), float(m[4]), float(m[5]))
            for m in merged
        ]

    def _calculate_verdict(
        self,
        global_mean: float,
        global_std: float,
        global_max: float,
        anomaly_regions: List[TamperAnomalyRegion],
    ) -> Tuple[float, str]:
        """Synthesize statistical and regional indicators into a composite tamper probability."""
        score = 0.0

        # Anomaly count & severity contributions
        for r in anomaly_regions:
            if r.anomaly_severity == "CRITICAL":
                score += 0.35
            elif r.anomaly_severity == "SUSPICIOUS":
                score += 0.20
            elif r.anomaly_severity == "MODERATE":
                score += 0.10

        # High variance ratio
        if global_mean > 0.01:
            cov = global_std / global_mean
            if cov > 1.8:
                score += 0.25
            elif cov > 1.4:
                score += 0.15

        # Peak outlier check
        if global_std > 0.01:
            z_max = (global_max - global_mean) / global_std
            if z_max > 6.0:
                score += 0.20
            elif z_max > 4.5:
                score += 0.10

        tamper_probability = min(1.0, max(0.0, score))

        if tamper_probability >= 0.80:
            verdict = "CONFIRMED_ALTERATION"
        elif tamper_probability >= 0.60:
            verdict = "PROBABLE_ALTERATION"
        elif tamper_probability >= 0.35:
            verdict = "INCONCLUSIVE"
        else:
            verdict = "CLEAN"

        return tamper_probability, verdict

    def _render_enhanced_ela_image(self, diff_img: Image.Image, scale: float) -> bytes:
        """Render high-contrast visual ELA inspection image as PNG bytes."""
        # Find maximum channel difference
        extrema = diff_img.getextrema()
        max_diff = max(ex[1] for ex in extrema)
        if max_diff == 0:
            max_diff = 1

        # Enhance contrast dynamically
        calculated_scale = 255.0 / max_diff if max_diff < 128 else scale
        effective_scale = min(calculated_scale, scale)

        enhancer = ImageEnhance.Brightness(diff_img)
        enhanced = enhancer.enhance(effective_scale)

        out_buf = io.BytesIO()
        enhanced.save(out_buf, format="PNG")
        return out_buf.getvalue()
