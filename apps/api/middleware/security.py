"""
Nirikshak Upload Security Middleware & Ingestion Gate.
Implements multi-layered defense-in-depth conforming to ADR-013, docs/API_CONTRACT.md,
and enterprise cybersecurity standards:
1. File size enforcement (< 15.0 MB -> HTTP 413).
2. Pure in-memory magic-byte inspection (JPEG, PNG, WebP -> HTTP 415).
3. Pre-decode streaming header dimension parser (Zero-allocation bomb defense -> HTTP 422).
4. Pillow decompression bomb limit (MAX_IMAGE_PIXELS = 64,000,000 -> HTTP 422).
5. Minimum resolution boundary check (>= 800x600 -> HTTP 422).
6. Complete EXIF / IPTC / XMP privacy sanitization (GPS & serial stripping).
7. Cryptographic SHA-256 integrity digest computation.
"""

import io
import struct
import hashlib
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from PIL import Image, ImageOps, UnidentifiedImageError

from apps.api.errors import (
    InvalidImagePayloadError,
    ImageTooLargeError,
    UnsupportedMediaTypeError,
    DecompressionBombError,
    ImageCorruptedError,
    ImageResolutionTooLowError,
)

# Statutory and Engineering Safety Limits
MAX_UPLOAD_SIZE_BYTES: int = 15 * 1024 * 1024  # 15.0 MB
MAX_DECOMPRESSION_PIXELS: int = 64_000_000     # 64 Megapixels (ADR-013)
MIN_IMAGE_WIDTH: int = 800                      # Minimum width for reliable OCR
MIN_IMAGE_HEIGHT: int = 600                     # Minimum height for reliable OCR

# Enforce globally in Pillow as safety backstop
Image.MAX_IMAGE_PIXELS = MAX_DECOMPRESSION_PIXELS


@dataclass(frozen=True)
class SanitizedImageRecord:
    """Immutable forensic record of a verified and sanitized packaging image."""
    raw_sha256: str
    sanitized_bytes: bytes
    format: str
    width: int
    height: int
    raw_size_bytes: int
    sanitized_size_bytes: int
    exif_tags_stripped: int
    had_gps_data: bool


class ImageSecurityValidator:
    """
    High-performance, memory-safe validator for incoming image streams.
    Operates 100% in memory with zero intermediate disk leaks.
    """

    @classmethod
    def verify_magic_bytes(cls, header_bytes: bytes) -> str:
        """
        Inspects leading binary signatures to confirm genuine image encoding.

        Signatures:
        - JPEG: \\xFF\\xD8\\xFF
        - PNG:  \\x89PNG\\r\\n\\x1a\\n (\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A)
        - WebP: RIFF at byte 0, WEBP at byte 8 (RIFF....WEBP)

        Returns:
            Canonical format string ('JPEG', 'PNG', 'WEBP')
        Raises:
            UnsupportedMediaTypeError if magic bytes do not match.
        """
        if len(header_bytes) < 12:
            raise UnsupportedMediaTypeError(
                detected_mime="insufficient_bytes",
                detected_magic=header_bytes.hex()
            )

        # JPEG verification
        if header_bytes[:3] == b"\xff\xd8\xff":
            return "JPEG"

        # PNG verification
        if header_bytes[:8] == b"\x89PNG\r\n\x1a\n":
            return "PNG"

        # WebP verification: 'RIFF' + 4-byte chunk size + 'WEBP'
        if header_bytes[:4] == b"RIFF" and header_bytes[8:12] == b"WEBP":
            return "WEBP"

        raise UnsupportedMediaTypeError(
            detected_mime="unrecognized_binary",
            detected_magic=header_bytes[:12].hex()
        )

    @classmethod
    def parse_dimensions_from_stream_headers(cls, data: bytes, fmt: str) -> Optional[Tuple[int, int]]:
        """
        Lightweight streaming header parser that extracts image dimensions
        WITHOUT allocating raster pixel buffers in memory.
        Acts as pre-decode firewall against decompression bombs.
        """
        try:
            if fmt == "PNG":
                # PNG IHDR chunk is located at bytes 12 to 28
                # Offset 16..20 is width (big-endian 32-bit), 20..24 is height
                if len(data) >= 24 and data[12:16] == b"IHDR":
                    width, height = struct.unpack(">II", data[16:24])
                    return width, height

            elif fmt == "JPEG":
                # Scan JPEG markers for Start Of Frame (SOF0 = 0xFFC0, SOF1 = 0xFFC1, SOF2 = 0xFFC2)
                offset = 2
                while offset < len(data) - 9:
                    if data[offset] != 0xFF:
                        offset += 1
                        continue
                    marker = data[offset + 1]
                    # SOF markers: C0, C1, C2, C3, C5, C6, C7, C9, CA, CB, CD, CE, CF
                    if marker in [0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF]:
                        # Marker structure: [FF marker] [2-byte length] [1-byte precision] [2-byte height] [2-byte width]
                        height, width = struct.unpack(">HH", data[offset + 5: offset + 9])
                        return width, height
                    else:
                        # Skip this marker's segment
                        if offset + 3 >= len(data):
                            break
                        seg_len = struct.unpack(">H", data[offset + 2: offset + 4])[0]
                        offset += 2 + seg_len

            elif fmt == "WEBP":
                # WebP VP8, VP8L, or VP8X header parsing
                if len(data) >= 30:
                    chunk_header = data[12:16]
                    if chunk_header == b"VP8 ":
                        # Simple lossy VP8
                        # 3 bytes start code at offset 23: 0x9D 0x01 0x2A
                        if data[23:26] == b"\x9d\x01\x2a":
                            w_raw = struct.unpack("<H", data[26:28])[0]
                            h_raw = struct.unpack("<H", data[28:30])[0]
                            return (w_raw & 0x3FFF), (h_raw & 0x3FFF)
                    elif chunk_header == b"VP8L":
                        # Lossless VP8L: width and height encoded in 14-bit bitfield
                        if data[20] == 0x2F:
                            b1, b2, b3, b4 = struct.unpack("4B", data[21:25])
                            width = 1 + (((b2 & 0x3F) << 8) | b1)
                            height = 1 + (((b4 & 0xF) << 10) | (b3 << 2) | ((b2 & 0xC0) >> 6))
                            return width, height
                    elif chunk_header == b"VP8X":
                        # Extended WebP format: 24-bit canvas width and height at offset 24
                        w_raw = struct.unpack("<I", data[24:27] + b"\x00")[0]
                        h_raw = struct.unpack("<I", data[27:30] + b"\x00")[0]
                        return w_raw + 1, h_raw + 1
        except Exception:
            # If fast header parsing encounters an irregular segment, fall back to PIL
            return None
        return None

    @classmethod
    def sanitize_and_verify(
        cls,
        file_bytes: bytes,
        filename: Optional[str] = None,
    ) -> SanitizedImageRecord:
        """
        Executes comprehensive 7-stage security validation and sanitization.

        Args:
            file_bytes: Raw binary bytes received from HTTP upload.
            filename: Original filename submitted in multipart form.

        Returns:
            SanitizedImageRecord containing sanitized bytes, metadata, and SHA-256 digest.

        Raises:
            InvalidImagePayloadError: If stream is empty or invalid.
            ImageTooLargeError: If size > 15MB.
            UnsupportedMediaTypeError: If magic bytes are invalid.
            DecompressionBombError: If pixels > 64MP.
            ImageCorruptedError: If pixel stream is invalid/unparseable.
            ImageResolutionTooLowError: If width < 800 or height < 600.
        """
        raw_size = len(file_bytes)

        # Stage 1: Payload Size Boundary
        if raw_size == 0:
            raise InvalidImagePayloadError("The uploaded file payload is empty (0 bytes).")
        if raw_size > MAX_UPLOAD_SIZE_BYTES:
            raise ImageTooLargeError(file_size_bytes=raw_size, max_allowed_bytes=MAX_UPLOAD_SIZE_BYTES)

        # Stage 2: Cryptographic Raw Hash
        raw_sha256 = hashlib.sha256(file_bytes).hexdigest()

        # Stage 3: Magic Bytes Verification
        fmt = cls.verify_magic_bytes(file_bytes[:16])

        # Stage 4: Pre-Decode Streaming Dimension Bounds (Bomb Firewall)
        fast_dims = cls.parse_dimensions_from_stream_headers(file_bytes, fmt)
        if fast_dims:
            w_fast, h_fast = fast_dims
            total_px_fast = w_fast * h_fast
            if total_px_fast > MAX_DECOMPRESSION_PIXELS:
                raise DecompressionBombError(
                    width=w_fast,
                    height=h_fast,
                    total_pixels=total_px_fast,
                    max_pixels=MAX_DECOMPRESSION_PIXELS,
                )

        # Stage 5: Pillow Load & Raster Decoding
        try:
            with Image.open(io.BytesIO(file_bytes)) as pil_img:
                width, height = pil_img.size
                total_pixels = width * height

                # Double check decompression bomb limit
                if total_pixels > MAX_DECOMPRESSION_PIXELS:
                    raise DecompressionBombError(
                        width=width,
                        height=height,
                        total_pixels=total_pixels,
                        max_pixels=MAX_DECOMPRESSION_PIXELS,
                    )

                # Stage 6: Minimum Resolution Verification
                if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                    raise ImageResolutionTooLowError(
                        width=width,
                        height=height,
                        min_width=MIN_IMAGE_WIDTH,
                        min_height=MIN_IMAGE_HEIGHT,
                    )

                # Stage 7: Privacy Sanitization (EXIF & Metadata Stripping)
                # First, honor EXIF orientation so rotated images remain right-side up
                had_gps = False
                exif_tag_count = 0
                try:
                    exif_data = pil_img.getexif()
                    if exif_data:
                        exif_tag_count = len(exif_data)
                        # GPSInfo tag ID is 0x8825 (34853)
                        had_gps = 34853 in exif_data or 0x8825 in exif_data
                    sanitized_img = ImageOps.exif_transpose(pil_img)
                except Exception:
                    sanitized_img = pil_img

                # Convert to clean RGB if Palette or other mode
                if sanitized_img.mode not in ("RGB", "RGBA"):
                    sanitized_img = sanitized_img.convert("RGB")

                # Re-encode to clean in-memory buffer without EXIF metadata
                out_buffer = io.BytesIO()
                if fmt == "PNG":
                    sanitized_img.save(out_buffer, format="PNG", optimize=True)
                elif fmt == "WEBP":
                    sanitized_img.save(out_buffer, format="WEBP", quality=95)
                else:
                    # JPEG default
                    sanitized_img.save(out_buffer, format="JPEG", quality=95)

                sanitized_bytes = out_buffer.getvalue()

                return SanitizedImageRecord(
                    raw_sha256=raw_sha256,
                    sanitized_bytes=sanitized_bytes,
                    format=fmt,
                    width=width,
                    height=height,
                    raw_size_bytes=raw_size,
                    sanitized_size_bytes=len(sanitized_bytes),
                    exif_tags_stripped=exif_tag_count,
                    had_gps_data=had_gps,
                )

        except (UnidentifiedImageError, ValueError, OSError) as err:
            if isinstance(err, (DecompressionBombError, ImageResolutionTooLowError, ImageTooLargeError, UnsupportedMediaTypeError)):
                raise
            raise ImageCorruptedError(reason=str(err))


validate_and_sanitize_image_upload = ImageSecurityValidator.sanitize_and_verify
UploadSecurityGate = ImageSecurityValidator

__all__ = [
    "ImageSecurityValidator",
    "UploadSecurityGate",
    "SanitizedImageRecord",
    "validate_and_sanitize_image_upload",
    "MAX_UPLOAD_SIZE_BYTES",
    "MAX_DECOMPRESSION_PIXELS",
    "MIN_IMAGE_WIDTH",
    "MIN_IMAGE_HEIGHT",
]
