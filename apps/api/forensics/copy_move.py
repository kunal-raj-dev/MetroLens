"""
Copy-Move Forgery Detection (CMFD) Engine
=========================================
Implements spatial block-based Discrete Cosine Transform (DCT) feature extraction,
lexicographical vector sorting, Euclidean distance thresholding, and shift-vector
clustering to detect duplicated packaging regions (e.g. duplicated MRP stamps,
cloned expiry dates, or digitally replicated legal declarations).

Algorithm:
    1. Grayscale luminance conversion and block partitioning (8x8 or 16x16 pixels).
    2. 2D DCT-II coefficient quantization and low-frequency feature vector reduction.
    3. Lexicographical sorting of feature vectors to place visually identical blocks adjacent.
    4. K-nearest neighbor shift-vector calculation: (dx, dy) = (x1 - x2, y1 - y2).
    5. Morphological clustering and displacement voting to eliminate random false matches.
    6. Minimum spatial distance guard to prevent matching neighboring smooth blocks.
"""

from __future__ import annotations

import collections
import io
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class ClonedRegionMatch:
    """Represents a pair of suspiciously identical image regions."""

    source_box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    target_box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    euclidean_distance_px: float
    feature_similarity: float  # 0.0 to 1.0 (1.0 = identical)
    shift_vector: Tuple[int, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_box": list(self.source_box),
            "target_box": list(self.target_box),
            "euclidean_distance_px": round(self.euclidean_distance_px, 2),
            "feature_similarity": round(self.feature_similarity, 4),
            "shift_vector": list(self.shift_vector),
        }


@dataclass(frozen=True)
class CopyMoveDetectionResult:
    """Comprehensive verdict of Copy-Move Forgery Analysis."""

    is_cloning_detected: bool
    forgery_probability: float
    detected_clones_count: int
    matching_pairs: List[ClonedRegionMatch]
    dominant_shift_vectors: List[Tuple[Tuple[int, int], int]]  # ((dx, dy), votes)
    analyzed_blocks_count: int
    block_size: int
    forensic_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_cloning_detected": self.is_cloning_detected,
            "forgery_probability": round(self.forgery_probability, 4),
            "detected_clones_count": self.detected_clones_count,
            "matching_pairs": [p.to_dict() for p in self.matching_pairs],
            "dominant_shift_vectors": [
                {"shift_dx": s[0][0], "shift_dy": s[0][1], "cluster_size": s[1]}
                for s in self.dominant_shift_vectors
            ],
            "analyzed_blocks_count": self.analyzed_blocks_count,
            "block_size": self.block_size,
            "forensic_notes": self.forensic_notes,
        }


class CopyMoveDetector:
    """
    Robust forensic analyzer detecting cloned or duplicated image regions.
    """

    def __init__(
        self,
        block_size: int = 16,
        dct_coefficients_retained: int = 10,
        similarity_threshold: float = 0.96,
        min_spatial_distance: float = 32.0,
        min_cluster_size: int = 4,
        max_image_dimension: int = 800,
    ) -> None:
        """
        Args:
            block_size: Tile width/height in pixels (typically 8 or 16).
            dct_coefficients_retained: Number of low-frequency zigzag DCT features.
            similarity_threshold: Normalized cosine similarity threshold (0-1).
            min_spatial_distance: Minimum Euclidean distance between block centers.
            min_cluster_size: Minimum number of parallel shift-vectors required to flag clone.
            max_image_dimension: Max width/height for forensic downscaling to maintain performance.
        """
        self.block_size = block_size
        self.dct_coefficients_retained = dct_coefficients_retained
        self.similarity_threshold = similarity_threshold
        self.min_spatial_distance = min_spatial_distance
        self.min_cluster_size = min_cluster_size
        self.max_image_dimension = max_image_dimension
        self._dct_basis = self._build_dct_basis(block_size)
        self._zigzag_indices = self._build_zigzag_order(block_size)[:dct_coefficients_retained]

    def analyze(self, image_input: bytes | Image.Image) -> CopyMoveDetectionResult:
        """
        Analyze an image for duplicate/cloned regions.
        """
        notes: List[str] = []
        if isinstance(image_input, bytes):
            with Image.open(io.BytesIO(image_input)) as raw_img:
                img = raw_img.convert("L")
        else:
            img = image_input.convert("L")

        # Downscale if exceeding max dimension while preserving aspect ratio
        w, h = img.size
        scale = 1.0
        if max(w, h) > self.max_image_dimension:
            scale = self.max_image_dimension / float(max(w, h))
            new_w = max(int(w * scale), self.block_size * 2)
            new_h = max(int(h * scale), self.block_size * 2)
            img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)
            notes.append(f"Image downscaled from {w}x{h} to {new_w}x{new_h} for block analysis.")

        img_arr = np.array(img, dtype=np.float32)
        height, width = img_arr.shape

        if height < self.block_size * 2 or width < self.block_size * 2:
            return CopyMoveDetectionResult(
                is_cloning_detected=False,
                forgery_probability=0.0,
                detected_clones_count=0,
                matching_pairs=[],
                dominant_shift_vectors=[],
                analyzed_blocks_count=0,
                block_size=self.block_size,
                forensic_notes=["Image dimensions too small for block-level copy-move analysis."],
            )

        # 1. Extract overlapping blocks and compute quantized DCT features
        blocks_data: List[Tuple[np.ndarray, int, int]] = []  # (feature_vector, x, y)
        step = max(1, self.block_size // 4)

        for y in range(0, height - self.block_size + 1, step):
            for x in range(0, width - self.block_size + 1, step):
                patch = img_arr[y : y + self.block_size, x : x + self.block_size]
                # Skip flat / uniform regions (variance near zero) to prevent false positives
                std_dev = float(np.std(patch))
                if std_dev < 4.0:
                    continue

                dct_2d = self._dct2(patch)
                features = np.array([dct_2d[r, c] for r, c in self._zigzag_indices], dtype=np.float32)
                # Normalize feature vector
                norm = np.linalg.norm(features)
                if norm > 1e-6:
                    features = features / norm
                blocks_data.append((features, x, y))

        total_blocks = len(blocks_data)
        if total_blocks < 4:
            return CopyMoveDetectionResult(
                is_cloning_detected=False,
                forgery_probability=0.0,
                detected_clones_count=0,
                matching_pairs=[],
                dominant_shift_vectors=[],
                analyzed_blocks_count=total_blocks,
                block_size=self.block_size,
                forensic_notes=["Insufficient non-uniform texture blocks found in image."],
            )

        # 2. Sort feature vectors lexicographically
        # Use first 4 principal coefficients for quick primary sort
        blocks_data.sort(key=lambda item: tuple(np.round(item[0][:4], 2)))

        # 3. Search adjacent neighbors in sorted list for feature similarity
        candidate_matches: List[ClonedRegionMatch] = []
        search_window = min(15, total_blocks - 1)
        shift_counter: collections.Counter = collections.Counter()

        for i in range(total_blocks):
            feat_i, xi, yi = blocks_data[i]
            for j in range(i + 1, min(i + search_window + 1, total_blocks)):
                feat_j, xj, yj = blocks_data[j]

                # Check spatial Euclidean distance
                dx = xj - xi
                dy = yj - yi
                spatial_dist = math.hypot(dx, dy)
                if spatial_dist < self.min_spatial_distance:
                    continue

                # Cosine similarity (already unit normalized)
                sim = float(np.dot(feat_i, feat_j))
                if sim >= self.similarity_threshold:
                    # Canonical shift vector (standardize direction)
                    shift = (dx, dy) if dx > 0 or (dx == 0 and dy > 0) else (-dx, -dy)
                    # Quantize shift to 8px bins to cluster similar movements
                    shift_bin = (round(shift[0] / 8) * 8, round(shift[1] / 8) * 8)
                    shift_counter[shift_bin] += 1

                    # Project coordinates back to original unscaled resolution
                    orig_x1 = int(xi / scale)
                    orig_y1 = int(yi / scale)
                    orig_x2 = int(xj / scale)
                    orig_y2 = int(yj / scale)
                    bs_orig = int(self.block_size / scale)

                    candidate_matches.append(
                        ClonedRegionMatch(
                            source_box=(orig_x1, orig_y1, orig_x1 + bs_orig, orig_y1 + bs_orig),
                            target_box=(orig_x2, orig_y2, orig_x2 + bs_orig, orig_y2 + bs_orig),
                            euclidean_distance_px=spatial_dist / scale,
                            feature_similarity=sim,
                            shift_vector=(int(dx / scale), int(dy / scale)),
                        )
                    )

        # 4. Filter matches by coherent shift vector clusters
        dominant_shifts = shift_counter.most_common(5)
        coherent_clusters = [s for s in dominant_shifts if s[1] >= self.min_cluster_size]

        confirmed_matches: List[ClonedRegionMatch] = []
        if coherent_clusters:
            top_shift_set = {s[0] for s in coherent_clusters}
            for m in candidate_matches:
                m_bin = (round(m.shift_vector[0] * scale / 8) * 8, round(m.shift_vector[1] * scale / 8) * 8)
                if m_bin in top_shift_set:
                    confirmed_matches.append(m)

        is_cloned = len(coherent_clusters) > 0 and len(confirmed_matches) >= self.min_cluster_size
        max_votes = coherent_clusters[0][1] if coherent_clusters else 0
        forgery_prob = min(1.0, max_votes / float(self.min_cluster_size * 4)) if is_cloned else 0.0

        if is_cloned:
            notes.append(
                f"Copy-Move duplication confirmed: {len(confirmed_matches)} cloned block pairs "
                f"aligned along dominant shift vector {coherent_clusters[0][0]}."
            )
        else:
            notes.append("No coherent shift-vector clustering detected; image free of cloned artifacts.")

        return CopyMoveDetectionResult(
            is_cloning_detected=is_cloned,
            forgery_probability=forgery_prob,
            detected_clones_count=len(confirmed_matches),
            matching_pairs=confirmed_matches[:25],
            dominant_shift_vectors=dominant_shifts,
            analyzed_blocks_count=total_blocks,
            block_size=self.block_size,
            forensic_notes=notes,
        )

    def _dct2(self, patch: np.ndarray) -> np.ndarray:
        """Compute 2D DCT using precalculated orthonormal basis matrices."""
        return self._dct_basis @ patch @ self._dct_basis.T

    def _build_dct_basis(self, n: int) -> np.ndarray:
        """Construct orthonormal 1D DCT-II matrix."""
        basis = np.zeros((n, n), dtype=np.float32)
        for k in range(n):
            alpha = math.sqrt(1.0 / n) if k == 0 else math.sqrt(2.0 / n)
            for i in range(n):
                basis[k, i] = alpha * math.cos((math.pi * (2 * i + 1) * k) / (2.0 * n))
        return basis

    def _build_zigzag_order(self, n: int) -> List[Tuple[int, int]]:
        """Construct zigzag traversal order for NxN matrix."""
        order = []
        for s in range(2 * n - 1):
            if s % 2 == 0:
                for i in range(min(s, n - 1), max(-1, s - n), -1):
                    j = s - i
                    if 0 <= i < n and 0 <= j < n:
                        order.append((i, j))
            else:
                for j in range(min(s, n - 1), max(-1, s - n), -1):
                    i = s - j
                    if 0 <= i < n and 0 <= j < n:
                        order.append((i, j))
        return order
