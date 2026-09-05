"""
Perceptual Hashing & Visual Deduplication Engine
================================================
Implements Average Hash (aHash), Difference Hash (dHash), and Discrete Cosine
Transform Perceptual Hash (pHash) for rapid visual similarity matching, packaging
deduplication, and two-tier OCR cache lookup in MetroLens AI.

Context:
    Standard cryptographic hashes (SHA-256) change completely if a single pixel
    or compression level changes. Perceptual hashes create invariant structural
    signatures that remain stable under JPEG recompression, minor rotations,
    and lighting variations, enabling sub-millisecond retrieval of cached OCR dossiers.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class PerceptualHashResult:
    """Multi-algorithm perceptual hash fingerprint of an image."""

    ahash_hex: str
    dhash_hex: str
    phash_hex: str
    ahash_int: int
    dhash_int: int
    phash_int: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ahash": self.ahash_hex,
            "dhash": self.dhash_hex,
            "phash": self.phash_hex,
        }

    def hamming_distance(self, other: PerceptualHashResult, hash_type: str = "phash") -> int:
        """Calculate the Hamming distance (number of bit differences) against another hash."""
        if hash_type == "ahash":
            return (self.ahash_int ^ other.ahash_int).bit_count()
        elif hash_type == "dhash":
            return (self.dhash_int ^ other.dhash_int).bit_count()
        elif hash_type == "phash":
            return (self.phash_int ^ other.phash_int).bit_count()
        else:
            raise ValueError(f"Unknown hash type: {hash_type}. Choose 'ahash', 'dhash', or 'phash'.")

    def similarity(self, other: PerceptualHashResult, hash_type: str = "phash") -> float:
        """Calculate normalized visual similarity score from 0.0 (completely distinct) to 1.0 (identical)."""
        dist = self.hamming_distance(other, hash_type=hash_type)
        return max(0.0, 1.0 - (dist / 64.0))


class PerceptualHasher:
    """
    High-performance image perceptual hash generator.
    """

    def __init__(self, dct_matrix_size: int = 32, hash_size: int = 8) -> None:
        self.dct_matrix_size = dct_matrix_size
        self.hash_size = hash_size
        # Precompute DCT-II transformation matrix for rapid execution
        self._dct_basis = self._generate_dct_basis(dct_matrix_size)

    def compute(self, image_input: Union[bytes, Image.Image]) -> PerceptualHashResult:
        """
        Compute aHash, dHash, and pHash for an image input.

        Args:
            image_input: Raw image bytes or a PIL Image instance.

        Returns:
            PerceptualHashResult containing hex and integer representations of all three hashes.
        """
        if isinstance(image_input, bytes):
            with Image.open(io.BytesIO(image_input)) as img:
                gray_img = img.convert("L")
        else:
            gray_img = image_input.convert("L")

        ahash_int = self._compute_ahash(gray_img)
        dhash_int = self._compute_dhash(gray_img)
        phash_int = self._compute_phash(gray_img)

        return PerceptualHashResult(
            ahash_hex=f"{ahash_int:016x}",
            dhash_hex=f"{dhash_int:016x}",
            phash_hex=f"{phash_int:016x}",
            ahash_int=ahash_int,
            dhash_int=dhash_int,
            phash_int=phash_int,
        )

    def _compute_ahash(self, gray_img: Image.Image) -> int:
        """Average Hash: 8x8 resize, compare each pixel to mean luminosity."""
        resized = gray_img.resize((self.hash_size, self.hash_size), Image.Resampling.BILINEAR)
        pixels = np.array(resized, dtype=np.float32)
        mean_val = np.mean(pixels)
        diff = pixels > mean_val
        hash_int = 0
        for bit in diff.flatten():
            hash_int = (hash_int << 1) | int(bit)
        return hash_int

    def _compute_dhash(self, gray_img: Image.Image) -> int:
        """Difference Hash: 9x8 resize, compare each pixel to its horizontal neighbor."""
        resized = gray_img.resize((self.hash_size + 1, self.hash_size), Image.Resampling.BILINEAR)
        pixels = np.array(resized, dtype=np.int32)
        # Compare column k with column k+1
        diff = pixels[:, 1:] > pixels[:, :-1]
        hash_int = 0
        for bit in diff.flatten():
            hash_int = (hash_int << 1) | int(bit)
        return hash_int

    def _compute_phash(self, gray_img: Image.Image) -> int:
        """
        Perceptual Hash (pHash):
        1. Resize to 32x32.
        2. Apply 2D Discrete Cosine Transform (DCT).
        3. Extract the top-left 8x8 low-frequency matrix (excluding DC coefficient at 0,0).
        4. Compare against median frequency coefficient.
        """
        n = self.dct_matrix_size
        resized = gray_img.resize((n, n), Image.Resampling.BILINEAR)
        pixels = np.array(resized, dtype=np.float32)

        # 2D DCT: D * pixels * D^T
        dct_2d = self._dct_basis @ pixels @ self._dct_basis.T

        # Extract 8x8 low frequencies
        low_freq = dct_2d[0 : self.hash_size, 0 : self.hash_size]

        # Calculate median of low frequencies excluding DC term at (0, 0)
        flat_coeffs = low_freq.flatten()[1:]
        median_val = float(np.median(flat_coeffs))

        diff = low_freq > median_val
        hash_int = 0
        for bit in diff.flatten():
            hash_int = (hash_int << 1) | int(bit)
        return hash_int

    def _generate_dct_basis(self, n: int) -> np.ndarray:
        """Generate orthonormal NxN DCT-II basis matrix."""
        basis = np.zeros((n, n), dtype=np.float32)
        for k in range(n):
            for i in range(n):
                if k == 0:
                    basis[k, i] = 1.0 / math.sqrt(n)
                else:
                    basis[k, i] = math.sqrt(2.0 / n) * math.cos((math.pi * (2 * i + 1) * k) / (2.0 * n))
        return basis
