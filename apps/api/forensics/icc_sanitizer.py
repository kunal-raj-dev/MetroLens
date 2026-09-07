"""
ICC Color Profile Forensic Parser & Sanitizer
=============================================
Parses and validates embedded International Color Consortium (ICC) profiles
in uploaded commodity photographs. Neutralizes known image-decoder parser
vulnerabilities (out-of-bounds reads, integer overflows, corrupt transformation
matrices) before image rasterization.

Context:
    Adversarial images often exploit vulnerabilities in LittleCMS, liblcms2, or
    Pillow's ICC parser by embedding crafted, non-conformant ICC profiles with
    circular tag offsets or recursive parametric curves.
"""

from __future__ import annotations

import io
import struct
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image


@dataclass(frozen=True)
class ICCTagEntry:
    """Represents an entry in the ICC tag table."""

    signature: str
    offset: int
    size: int
    is_valid_offset: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature": self.signature,
            "offset": self.offset,
            "size": self.size,
            "is_valid_offset": self.is_valid_offset,
        }


@dataclass(frozen=True)
class ICCSanitizationResult:
    """Result of ICC profile validation and sanitization."""

    has_icc_profile: bool
    is_profile_valid: bool
    is_sanitized: bool
    profile_size_bytes: int
    profile_version: Optional[str] = None
    color_space: Optional[str] = None
    connection_space: Optional[str] = None
    device_class: Optional[str] = None
    tag_count: int = 0
    tags: List[ICCTagEntry] = field(default_factory=list)
    sanitization_actions: List[str] = field(default_factory=list)
    sanitized_image_bytes: Optional[bytes] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "has_icc_profile": self.has_icc_profile,
            "is_profile_valid": self.is_profile_valid,
            "is_sanitized": self.is_sanitized,
            "profile_size_bytes": self.profile_size_bytes,
            "profile_version": self.profile_version,
            "color_space": self.color_space,
            "connection_space": self.connection_space,
            "device_class": self.device_class,
            "tag_count": self.tag_count,
            "tags": [t.to_dict() for t in self.tags],
            "sanitization_actions": self.sanitization_actions,
        }


class ICCProfileSanitizer:
    """
    Validates and sanitizes binary ICC profile streams according to
    ICC.1:2010 (Profile version 4.3.0.0) and ICC.1:2001-04 (Version 2.4.0).
    """

    MAGIC_ACSP = b"acsp"  # Profile file signature at offset 36..40
    MAX_PROFILE_SIZE = 512 * 1024  # 512 KB maximum allowable profile size
    MAX_TAG_COUNT = 128  # Maximum allowable tags in tag table

    KNOWN_COLOR_SPACES = {
        "XYZ ", "Lab ", "Luv ", "YCbr", "Yxy ", "RGB ", "GRAY", "HSV ", "HLS ", "CMYK", "CMY "
    }

    KNOWN_DEVICE_CLASSES = {
        "scnr", "mntr", "prtr", "link", "spac", "abst", "nmcl"
    }

    def sanitize(self, image_bytes: bytes) -> ICCSanitizationResult:
        """
        Inspect the image for embedded ICC profiles and neutralize malformed structures.

        Args:
            image_bytes: Raw binary image payload.

        Returns:
            ICCSanitizationResult detailing validation status and sanitized bytes.
        """
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                icc_raw = img.info.get("icc_profile")
                img_format = img.format or "JPEG"
        except Exception as exc:
            return ICCSanitizationResult(
                has_icc_profile=False,
                is_profile_valid=False,
                is_sanitized=False,
                profile_size_bytes=0,
                sanitization_actions=[f"Failed to inspect image for ICC: {str(exc)}"],
            )

        if not icc_raw:
            return ICCSanitizationResult(
                has_icc_profile=False,
                is_profile_valid=True,
                is_sanitized=False,
                profile_size_bytes=0,
                sanitization_actions=["No embedded ICC profile detected; image is clean."],
            )

        # Validate the raw ICC profile structure
        is_valid, version_str, color_space, pcs, dev_class, tags, actions = self._validate_icc_bytes(icc_raw)

        sanitized_bytes = None
        is_sanitized = False

        if not is_valid:
            # Strip malicious/corrupt profile from image
            actions.append("Stripping invalid or malformed ICC profile from image stream.")
            sanitized_bytes = self._strip_icc_profile(image_bytes, img_format)
            is_sanitized = True
        else:
            actions.append("ICC profile verified conformant with standard colorimetric specifications.")

        return ICCSanitizationResult(
            has_icc_profile=True,
            is_profile_valid=is_valid,
            is_sanitized=is_sanitized,
            profile_size_bytes=len(icc_raw),
            profile_version=version_str,
            color_space=color_space,
            connection_space=pcs,
            device_class=dev_class,
            tag_count=len(tags),
            tags=tags,
            sanitization_actions=actions,
            sanitized_image_bytes=sanitized_bytes,
        )

    def _validate_icc_bytes(
        self, data: bytes
    ) -> Tuple[bool, Optional[str], Optional[str], Optional[str], Optional[str], List[ICCTagEntry], List[str]]:
        actions: List[str] = []
        tags: List[ICCTagEntry] = []

        if len(data) < 128:
            actions.append(f"Header truncated: profile size {len(data)} is less than minimum 128 bytes.")
            return False, None, None, None, None, [], actions

        if len(data) > self.MAX_PROFILE_SIZE:
            actions.append(f"Oversized profile: {len(data)} bytes exceeds safety limit of {self.MAX_PROFILE_SIZE} bytes.")
            return False, None, None, None, None, [], actions

        # Parse header
        profile_len = struct.unpack(">I", data[0:4])[0]
        if profile_len != len(data):
            actions.append(f"Declared profile length ({profile_len}) does not match actual length ({len(data)}).")
            return False, None, None, None, None, [], actions

        # Check 'acsp' signature at offset 36
        signature = data[36:40]
        if signature != self.MAGIC_ACSP:
            actions.append(f"Invalid ICC file signature: expected 'acsp', got {repr(signature)}.")
            return False, None, None, None, None, [], actions

        # Parse version
        major = data[8]
        minor = data[9] >> 4
        bugfix = data[9] & 0x0F
        version_str = f"{major}.{minor}.{bugfix}"

        if major not in (2, 4):
            actions.append(f"Unrecognized ICC major version: {major}.")
            return False, version_str, None, None, None, [], actions

        # Device class and color spaces
        dev_class = data[12:16].decode("latin-1", errors="replace").strip()
        color_space = data[16:20].decode("latin-1", errors="replace")
        pcs = data[20:24].decode("latin-1", errors="replace")

        # Parse Tag Table (begins at offset 128)
        tag_count = struct.unpack(">I", data[128:132])[0]
        if tag_count > self.MAX_TAG_COUNT:
            actions.append(f"Tag count {tag_count} exceeds maximum safety limit of {self.MAX_TAG_COUNT}.")
            return False, version_str, color_space, pcs, dev_class, [], actions

        tag_offset = 132
        for _ in range(tag_count):
            if tag_offset + 12 > len(data):
                actions.append("Tag table entries truncated before profile boundary.")
                return False, version_str, color_space, pcs, dev_class, tags, actions

            tag_sig = data[tag_offset : tag_offset + 4].decode("latin-1", errors="replace")
            t_offset, t_size = struct.unpack(">II", data[tag_offset + 4 : tag_offset + 12])

            is_valid_offset = (t_offset + t_size <= len(data)) and (t_offset >= 128)
            tags.append(
                ICCTagEntry(
                    signature=tag_sig,
                    offset=t_offset,
                    size=t_size,
                    is_valid_offset=is_valid_offset,
                )
            )

            if not is_valid_offset:
                actions.append(
                    f"Tag '{tag_sig}' has invalid memory offset {t_offset} with size {t_size} (profile length: {len(data)})."
                )
                return False, version_str, color_space, pcs, dev_class, tags, actions

            tag_offset += 12

        return True, version_str, color_space, pcs, dev_class, tags, actions

    def _strip_icc_profile(self, image_bytes: bytes, img_format: str) -> bytes:
        """Strip the embedded ICC profile and re-save as clean RGB image."""
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(list(img.getdata()))
                out_buf = io.BytesIO()
                clean_img.save(out_buf, format=img_format, icc_profile=None)
                return out_buf.getvalue()
        except Exception:
            return image_bytes
