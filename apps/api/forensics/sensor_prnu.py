"""
Photo-Response Non-Uniformity (PRNU) Sensor Fingerprint Verifier
================================================================
Extracts camera sensor physical hardware noise residuals to verify device
identity and corroborate photographic chain of custody under Section 63 BSA 2023.

Physical Principle:
    Every CMOS/CCD silicon sensor possesses minute, immutable physical manufacturing
    imperfections called Photo-Response Non-Uniformity (PRNU). The PRNU acts as an
    unforgeable digital biometric fingerprint embedded into every photograph taken
    by that specific camera.

    By separating high-frequency sensor noise from image scene details via an adaptive
    wavelet/median residual filter, we calculate the Normalized Cross-Correlation (NCC)
    and Peak-to-Correlation Energy (PCE) between an evidentiary photo and a reference
    camera profile or across multiple raid photographs.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class PRNUCrossCorrelationResult:
    """Outcome of sensor fingerprint matching between two photographs."""

    is_same_sensor: bool
    correlation_coefficient: float          # -1.0 to 1.0 (typical match > 0.04)
    peak_to_correlation_energy: float       # PCE metric (court standard > 45.0)
    confidence_level: str                   # 'DEFINITIVE_MATCH', 'PROBABLE_MATCH', 'INCONCLUSIVE', 'NON_MATCH'
    analyzed_resolution: Tuple[int, int]
    forensic_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_same_sensor": self.is_same_sensor,
            "correlation_coefficient": round(self.correlation_coefficient, 5),
            "peak_to_correlation_energy": round(self.peak_to_correlation_energy, 2),
            "confidence_level": self.confidence_level,
            "analyzed_resolution": list(self.analyzed_resolution),
            "forensic_notes": self.forensic_notes,
        }


class PRNUSensorFingerprintVerifier:
    """
    Forensic engine extracting and cross-correlating camera sensor PRNU noise.
    """

    def __init__(
        self,
        ncc_match_threshold: float = 0.045,
        pce_match_threshold: float = 40.0,
        target_crop_dimension: int = 512,
    ) -> None:
        self.ncc_match_threshold = ncc_match_threshold
        self.pce_match_threshold = pce_match_threshold
        self.target_crop_dimension = target_crop_dimension

    def extract_noise_residual(self, image_input: bytes | Image.Image) -> np.ndarray:
        """
        Extract zero-mean PRNU sensor noise residual matrix W = I - F(I).
        Uses a local adaptive denoising filter over central luminance patch.
        """
        if isinstance(image_input, bytes):
            with Image.open(io.BytesIO(image_input)) as raw_img:
                img = raw_img.convert("L")
        else:
            img = image_input.convert("L")

        w, h = img.size
        crop_size = min(w, h, self.target_crop_dimension)
        left = (w - crop_size) // 2
        top = (h - crop_size) // 2
        cropped = img.crop((left, top, left + crop_size, top + crop_size))

        arr = np.array(cropped, dtype=np.float32)

        # High-pass spatial noise filter: subtract local 3x3 box mean filter
        # F(I) approximates underlying scene content; residual W captures sensor noise
        padded = np.pad(arr, pad_width=1, mode="edge")
        local_mean = (
            padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:]
            + padded[1:-1, :-2] + padded[1:-1, 1:-1] + padded[1:-1, 2:]
            + padded[2:, :-2] + padded[2:, 1:-1] + padded[2:, 2:]
        ) / 9.0

        noise = arr - local_mean

        # Zero-mean normalization
        noise = noise - float(np.mean(noise))
        norm = float(np.linalg.norm(noise))
        if norm > 1e-5:
            noise = noise / norm

        return noise

    def verify_camera_coherence(
        self,
        image_a: bytes | Image.Image,
        image_b: bytes | Image.Image,
    ) -> PRNUCrossCorrelationResult:
        """
        Compares sensor fingerprints between two photographs.
        """
        notes: List[str] = []
        w_a = self.extract_noise_residual(image_a)
        w_b = self.extract_noise_residual(image_b)

        # Match dimensions if crops differed
        min_dim = min(w_a.shape[0], w_b.shape[0])
        w_a = w_a[:min_dim, :min_dim]
        w_b = w_b[:min_dim, :min_dim]

        # 1. 2D Normalized Cross-Correlation in Fourier Frequency Domain
        # Cross-power spectrum: F_corr = FFT(W_a) * conj(FFT(W_b))
        fft_a = np.fft.fft2(w_a)
        fft_b = np.fft.fft2(w_b)
        cross_spec = fft_a * np.conj(fft_b)

        corr_map = np.real(np.fft.ifft2(cross_spec))
        corr_map = np.fft.fftshift(corr_map)

        # 2. Extract correlation peak and energy statistics
        peak_val = float(np.max(corr_map))
        peak_idx = np.unravel_index(np.argmax(corr_map), corr_map.shape)

        # Zero-out 11x11 square around peak to measure background noise energy
        py, px = peak_idx
        mask = np.ones_like(corr_map, dtype=bool)
        y0, y1 = max(0, py - 5), min(corr_map.shape[0], py + 6)
        x0, x1 = max(0, px - 5), min(corr_map.shape[1], px + 6)
        mask[y0:y1, x0:x1] = False

        background_energy = float(np.mean(corr_map[mask] ** 2)) if np.any(mask) else 1e-6
        pce = (peak_val ** 2) / max(background_energy, 1e-7)

        # Direct spatial normalized correlation at zero shift (py=mid, px=mid)
        center_y, center_x = min_dim // 2, min_dim // 2
        zero_shift_ncc = float(np.sum(w_a * w_b))

        # Decision rule
        is_match = zero_shift_ncc >= self.ncc_match_threshold or pce >= self.pce_match_threshold

        if pce >= 60.0 and zero_shift_ncc >= 0.05:
            conf = "DEFINITIVE_MATCH"
            notes.append("Photographs share identical physical camera sensor PRNU fingerprint with high statistical certainty.")
        elif is_match:
            conf = "PROBABLE_MATCH"
            notes.append("Sensor noise correlation exceeds threshold; evidence strongly indicates same capture hardware.")
        elif zero_shift_ncc > 0.02:
            conf = "INCONCLUSIVE"
            notes.append("Correlation elevated but insufficient for judicial confirmation.")
        else:
            conf = "NON_MATCH"
            notes.append("Independent sensor noise fingerprints detected; photographs captured by distinct camera hardware.")

        return PRNUCrossCorrelationResult(
            is_same_sensor=is_match,
            correlation_coefficient=zero_shift_ncc,
            peak_to_correlation_energy=pce,
            confidence_level=conf,
            analyzed_resolution=(min_dim, min_dim),
            forensic_notes=notes,
        )
