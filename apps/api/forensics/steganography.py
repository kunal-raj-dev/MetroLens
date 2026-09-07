"""
Steganography & Ancillary Chunk Forensic Scanner
================================================
Detects hidden data, polyglot shellcode, Least Significant Bit (LSB) embedding,
anomalous text chunks, and trailing binary payloads in packaging photographs.

Security Context:
    Commercial packaging inspection gateways often receive images from untrusted
    field sources. Adversaries may attempt polyglot file injection (JPEG/PNG with
    embedded PHP/Bash/JavaScript), LSB steganography to exfiltrate unauthorized
    internal tokens, or oversized ancillary chunks designed to trigger buffer
    overflows in underlying C-libraries (libpng / libjpeg).
"""

from __future__ import annotations

import io
import math
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class DetectedChunkInfo:
    """Information about a parsed container chunk or marker."""

    chunk_type: str
    offset: int
    length: int
    is_critical: bool
    is_suspicious: bool
    suspicion_reason: Optional[str] = None
    crc_valid: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_type": self.chunk_type,
            "offset": self.offset,
            "length": self.length,
            "is_critical": self.is_critical,
            "is_suspicious": self.is_suspicious,
            "suspicion_reason": self.suspicion_reason,
            "crc_valid": self.crc_valid,
        }


@dataclass(frozen=True)
class ChunkSanitizationResult:
    """Result of stripping non-essential or suspicious chunks from an image."""

    original_size_bytes: int
    sanitized_size_bytes: int
    stripped_chunks_count: int
    stripped_chunk_types: List[str]
    sanitized_bytes: bytes


@dataclass(frozen=True)
class SteganographyScanResult:
    """Comprehensive result of steganography and chunk forensic scanning."""

    is_clean: bool
    suspicion_score: float  # 0.0 to 1.0
    detected_format: str
    trailing_payload_bytes: int
    lsb_entropy_r: float
    lsb_entropy_g: float
    lsb_entropy_b: float
    lsb_chi_square_p_value: float
    is_lsb_anomaly_detected: bool
    suspicious_chunks: List[DetectedChunkInfo] = field(default_factory=list)
    all_chunks: List[DetectedChunkInfo] = field(default_factory=list)
    embedded_payload_previews: List[str] = field(default_factory=list)
    forensic_alerts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_clean": self.is_clean,
            "suspicion_score": round(self.suspicion_score, 4),
            "detected_format": self.detected_format,
            "trailing_payload_bytes": self.trailing_payload_bytes,
            "lsb_entropy": {
                "r": round(self.lsb_entropy_r, 4),
                "g": round(self.lsb_entropy_g, 4),
                "b": round(self.lsb_entropy_b, 4),
            },
            "lsb_chi_square_p_value": round(self.lsb_chi_square_p_value, 4),
            "is_lsb_anomaly_detected": self.is_lsb_anomaly_detected,
            "suspicious_chunks_count": len(self.suspicious_chunks),
            "suspicious_chunks": [c.to_dict() for c in self.suspicious_chunks],
            "total_chunks_inspected": len(self.all_chunks),
            "embedded_payload_previews": self.embedded_payload_previews,
            "forensic_alerts": self.forensic_alerts,
        }


class SteganographyScanner:
    """
    Forensic scanner for hidden payloads, LSB steganography, and container manipulation.
    """

    SUSPICIOUS_SIGNATURES: List[Tuple[bytes, str]] = [
        (b"<?php", "PHP script tag"),
        (b"#!/bin/", "Unix shell script header"),
        (b"<script", "JavaScript tag"),
        (b"eval(", "Code evaluation call"),
        (b"system(", "System shell invocation"),
        (b"base64_decode", "Base64 decoder invocation"),
        (b"powershell", "Windows PowerShell invocation"),
        (b"cmd.exe", "Windows command prompt invocation"),
        (b"PK\x03\x04", "Embedded ZIP archive header"),
        (b"\x7fELF", "Embedded Linux ELF binary"),
        (b"MZ", "Embedded DOS/PE Windows executable"),
    ]

    ALLOWED_PNG_CRITICAL: Set[str] = {"IHDR", "PLTE", "IDAT", "IEND"}
    BENIGN_PNG_ANCILLARY: Set[str] = {
        "bKGD", "cHRM", "gAMA", "hIST", "pHYs", "sBIT", "sRGB", "tIME"
    }

    def __init__(
        self,
        max_chunk_scan_depth: int = 1000,
        lsb_entropy_alert_threshold: float = 0.985,
        max_allowed_comment_length: int = 4096,
    ) -> None:
        self.max_chunk_scan_depth = max_chunk_scan_depth
        self.lsb_entropy_alert_threshold = lsb_entropy_alert_threshold
        self.max_allowed_comment_length = max_allowed_comment_length

    def scan(self, image_bytes: bytes) -> SteganographyScanResult:
        """
        Execute comprehensive steganography and container structure analysis.

        Args:
            image_bytes: Raw binary image payload.

        Returns:
            SteganographyScanResult detailing discovered anomalies.
        """
        if len(image_bytes) < 16:
            return SteganographyScanResult(
                is_clean=False,
                suspicion_score=1.0,
                detected_format="UNKNOWN",
                trailing_payload_bytes=0,
                lsb_entropy_r=0.0,
                lsb_entropy_g=0.0,
                lsb_entropy_b=0.0,
                lsb_chi_square_p_value=1.0,
                is_lsb_anomaly_detected=False,
                forensic_alerts=["File payload is too small to constitute a valid container."],
            )

        format_type = self._detect_format(image_bytes)
        chunks: List[DetectedChunkInfo] = []
        alerts: List[str] = []
        payload_previews: List[str] = []
        trailing_bytes = 0

        if format_type == "PNG":
            chunks, trailing_bytes, chunk_alerts, previews = self._inspect_png_chunks(image_bytes)
            alerts.extend(chunk_alerts)
            payload_previews.extend(previews)
        elif format_type == "JPEG":
            chunks, trailing_bytes, chunk_alerts, previews = self._inspect_jpeg_markers(image_bytes)
            alerts.extend(chunk_alerts)
            payload_previews.extend(previews)
        else:
            alerts.append(f"Container format '{format_type}' - standard chunk parsing bypassed.")

        # LSB bitplane statistical analysis
        lsb_r, lsb_g, lsb_b, chi_p, lsb_anomaly, lsb_alerts = self._analyze_lsb_planes(image_bytes)
        alerts.extend(lsb_alerts)

        # Calculate composite suspicion score
        suspicious_chunks = [c for c in chunks if c.is_suspicious]
        score = 0.0

        if trailing_bytes > 0:
            score += 0.35
            alerts.append(f"Detected {trailing_bytes} trailing payload bytes appended beyond legal EOF marker.")

        if suspicious_chunks:
            score += min(0.50, len(suspicious_chunks) * 0.25)

        if lsb_anomaly:
            score += 0.30

        if payload_previews:
            score += 0.40

        final_score = min(1.0, max(0.0, score))
        is_clean = final_score < 0.30 and len(suspicious_chunks) == 0 and trailing_bytes == 0

        return SteganographyScanResult(
            is_clean=is_clean,
            suspicion_score=final_score,
            detected_format=format_type,
            trailing_payload_bytes=trailing_bytes,
            lsb_entropy_r=lsb_r,
            lsb_entropy_g=lsb_g,
            lsb_entropy_b=lsb_b,
            lsb_chi_square_p_value=chi_p,
            is_lsb_anomaly_detected=lsb_anomaly,
            suspicious_chunks=suspicious_chunks,
            all_chunks=chunks,
            embedded_payload_previews=payload_previews,
            forensic_alerts=alerts,
        )

    def sanitize_png_chunks(self, image_bytes: bytes) -> ChunkSanitizationResult:
        """
        Strip non-essential ancillary and suspicious chunks from PNG stream.
        Preserves only IHDR, PLTE, IDAT, and IEND.
        """
        if not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            return ChunkSanitizationResult(
                original_size_bytes=len(image_bytes),
                sanitized_size_bytes=len(image_bytes),
                stripped_chunks_count=0,
                stripped_chunk_types=[],
                sanitized_bytes=image_bytes,
            )

        sanitized = bytearray(b"\x89PNG\r\n\x1a\n")
        offset = 8
        stripped_types: List[str] = []
        stripped_count = 0

        while offset + 8 <= len(image_bytes):
            length = struct.unpack(">I", image_bytes[offset : offset + 4])[0]
            chunk_type = image_bytes[offset + 4 : offset + 8].decode("latin-1", errors="replace")
            total_chunk_size = 4 + 4 + length + 4  # len + type + data + crc

            if offset + total_chunk_size > len(image_bytes):
                break

            if chunk_type in self.ALLOWED_PNG_CRITICAL:
                sanitized.extend(image_bytes[offset : offset + total_chunk_size])
            else:
                stripped_count += 1
                stripped_types.append(chunk_type)

            offset += total_chunk_size
            if chunk_type == "IEND":
                break

        return ChunkSanitizationResult(
            original_size_bytes=len(image_bytes),
            sanitized_size_bytes=len(sanitized),
            stripped_chunks_count=stripped_count,
            stripped_chunk_types=stripped_types,
            sanitized_bytes=bytes(sanitized),
        )

    def _detect_format(self, data: bytes) -> str:
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "PNG"
        if data.startswith(b"\xFF\xD8\xFF"):
            return "JPEG"
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return "WEBP"
        return "UNKNOWN"

    def _inspect_png_chunks(
        self, data: bytes
    ) -> Tuple[List[DetectedChunkInfo], int, List[str], List[str]]:
        chunks: List[DetectedChunkInfo] = []
        alerts: List[str] = []
        previews: List[str] = []

        offset = 8
        iend_offset: Optional[int] = None

        while offset + 8 <= len(data) and len(chunks) < self.max_chunk_scan_depth:
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            chunk_type = data[offset + 4 : offset + 8].decode("latin-1", errors="replace")
            total_chunk_size = 4 + 4 + length + 4

            if offset + total_chunk_size > len(data):
                alerts.append(f"PNG chunk '{chunk_type}' extends beyond end of file bounds.")
                break

            chunk_data = data[offset + 8 : offset + 8 + length]
            is_crit = chunk_type in self.ALLOWED_PNG_CRITICAL
            is_susp = False
            reason = None

            # Check for suspicious signatures in data
            for sig, sig_desc in self.SUSPICIOUS_SIGNATURES:
                if sig in chunk_data:
                    is_susp = True
                    reason = f"Contains forbidden executable signature: {sig_desc}"
                    previews.append(f"[{chunk_type}] {sig_desc}")
                    break

            # Check for abnormal text chunk lengths
            if chunk_type in {"tEXt", "zTXt", "iTXt"} and length > self.max_allowed_comment_length:
                is_susp = True
                reason = f"Oversized text chunk ({length} bytes) exceeds {self.max_allowed_comment_length} byte safety threshold."

            # Check unknown chunks
            if not is_crit and chunk_type not in self.BENIGN_PNG_ANCILLARY and not is_susp:
                if not chunk_type.isalpha():
                    is_susp = True
                    reason = f"Non-standard binary chunk identifier '{chunk_type}'."

            chunks.append(
                DetectedChunkInfo(
                    chunk_type=chunk_type,
                    offset=offset,
                    length=length,
                    is_critical=is_crit,
                    is_suspicious=is_susp,
                    suspicion_reason=reason,
                )
            )

            offset += total_chunk_size
            if chunk_type == "IEND":
                iend_offset = offset
                break

        trailing_bytes = 0
        if iend_offset is not None and iend_offset < len(data):
            trailing_bytes = len(data) - iend_offset
            trailing_slice = data[iend_offset : min(len(data), iend_offset + 256)]
            for sig, sig_desc in self.SUSPICIOUS_SIGNATURES:
                if sig in trailing_slice:
                    previews.append(f"[TRAILING] {sig_desc}")

        return chunks, trailing_bytes, alerts, previews

    def _inspect_jpeg_markers(
        self, data: bytes
    ) -> Tuple[List[DetectedChunkInfo], int, List[str], List[str]]:
        chunks: List[DetectedChunkInfo] = []
        alerts: List[str] = []
        previews: List[str] = []

        offset = 2
        eoi_offset: Optional[int] = None

        while offset < len(data) - 1:
            if data[offset] != 0xFF:
                offset += 1
                continue

            marker = data[offset + 1]
            if marker == 0x00 or marker == 0xFF:  # Byte stuffing or padding
                offset += 2
                continue

            # Standalone markers (no length)
            if marker in {0xD8, 0xD9, 0x01}:
                m_name = f"0x{marker:02X}"
                if marker == 0xD8:
                    m_name = "SOI"
                elif marker == 0xD9:
                    m_name = "EOI"
                    eoi_offset = offset + 2
                    chunks.append(
                        DetectedChunkInfo(
                            chunk_type=m_name,
                            offset=offset,
                            length=0,
                            is_critical=True,
                            is_suspicious=False,
                        )
                    )
                    break
                offset += 2
                continue

            # Markers with 16-bit length prefix
            if offset + 4 > len(data):
                break

            m_len = struct.unpack(">H", data[offset + 2 : offset + 4])[0]
            m_type = f"MARKER_0x{marker:02X}"
            if marker == 0xFE:
                m_type = "COM"
            elif 0xE0 <= marker <= 0xEF:
                m_type = f"APP{marker - 0xE0}"

            chunk_content = data[offset + 4 : min(len(data), offset + 2 + m_len)]
            is_susp = False
            reason = None

            for sig, sig_desc in self.SUSPICIOUS_SIGNATURES:
                if sig in chunk_content:
                    is_susp = True
                    reason = f"Contains suspicious payload: {sig_desc}"
                    previews.append(f"[{m_type}] {sig_desc}")
                    break

            if m_type == "COM" and m_len > self.max_allowed_comment_length:
                is_susp = True
                reason = f"Oversized comment marker ({m_len} bytes)."

            chunks.append(
                DetectedChunkInfo(
                    chunk_type=m_type,
                    offset=offset,
                    length=m_len,
                    is_critical=(marker in {0xC0, 0xC2, 0xC4, 0xDA, 0xDB}),
                    is_suspicious=is_susp,
                    suspicion_reason=reason,
                )
            )

            offset += 2 + m_len

        trailing_bytes = 0
        if eoi_offset is not None and eoi_offset < len(data):
            trailing_bytes = len(data) - eoi_offset

        return chunks, trailing_bytes, alerts, previews

    def _analyze_lsb_planes(
        self, image_bytes: bytes
    ) -> Tuple[float, float, float, float, bool, List[str]]:
        alerts: List[str] = []
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                rgb = img.convert("RGB")
                arr = np.array(rgb, dtype=np.uint8)
        except Exception:
            return 0.0, 0.0, 0.0, 1.0, False, ["Image decoding failed during LSB analysis."]

        # Extract least significant bit of each channel: arr & 1
        lsb_r = (arr[:, :, 0] & 1).flatten()
        lsb_g = (arr[:, :, 1] & 1).flatten()
        lsb_b = (arr[:, :, 2] & 1).flatten()

        ent_r = self._binary_entropy(lsb_r)
        ent_g = self._binary_entropy(lsb_g)
        ent_b = self._binary_entropy(lsb_b)

        # Chi-square analysis on red channel Pairs of Values (PoVs)
        chi_p = self._chi_square_povs(arr[:, :, 0].flatten())

        is_anomaly = False
        # Natural uncompressed photos generally have bitplane entropy < 0.985
        # Encrypted / compressed hidden payloads force bitplane entropy towards 1.000
        if (
            ent_r > self.lsb_entropy_alert_threshold
            and ent_g > self.lsb_entropy_alert_threshold
            and ent_b > self.lsb_entropy_alert_threshold
            and chi_p < 0.01
        ):
            is_anomaly = True
            alerts.append(
                f"Statistical LSB anomaly: all channels exhibit near-maximum bitplane entropy (R={ent_r:.4f}, G={ent_g:.4f}, B={ent_b:.4f}) and low chi-square p-value ({chi_p:.4f})."
            )

        return ent_r, ent_g, ent_b, chi_p, is_anomaly, alerts

    def _binary_entropy(self, bits: np.ndarray) -> float:
        """Calculate Shannon entropy of a binary bit stream in bits per symbol (max 1.0)."""
        if len(bits) == 0:
            return 0.0
        p1 = float(np.mean(bits))
        p0 = 1.0 - p1
        if p0 <= 0.0 or p1 <= 0.0:
            return 0.0
        return float(-p0 * math.log2(p0) - p1 * math.log2(p1))

    def _chi_square_povs(self, channel_bytes: np.ndarray) -> float:
        """
        Westfeld-Pfitzmann Chi-Square test for Pairs of Values (PoVs: 2k and 2k+1).
        Detects whether adjacent even/odd luminance pairs have been artificially balanced
        by sequential or random LSB overwriting.
        """
        if len(channel_bytes) < 1000:
            return 1.0

        # Sample up to 100,000 pixels for fast execution
        sample = channel_bytes[:100000]
        hist = np.bincount(sample, minlength=256)

        chi_sq = 0.0
        degrees_of_freedom = 0

        for k in range(128):
            count_even = hist[2 * k]
            count_odd = hist[2 * k + 1]
            total = count_even + count_odd
            if total > 5:
                expected = total / 2.0
                chi_sq += ((count_even - expected) ** 2) / expected
                chi_sq += ((count_odd - expected) ** 2) / expected
                degrees_of_freedom += 1

        if degrees_of_freedom <= 1:
            return 1.0

        # Approximate p-value from chi-square distribution via Wilson-Hilferty transformation
        d = float(degrees_of_freedom)
        z = ((chi_sq / d) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * d))) / math.sqrt(2.0 / (9.0 * d))
        # Standard normal CDF approximation
        p_val = 0.5 * math.erfc(z / math.sqrt(2.0))
        return float(max(0.0, min(1.0, p_val)))
