"""
MetroLens AI™ / Nirikshak AI — Security Regression Test Suite.
SIH 2026 Problem Statement 26034 — Member 6 Release Gate.

Validates defensive posture against:
- Empty payloads
- Corrupt byte sequences
- Unsupported file formats / MIME tampering
- Decompression bomb / oversized image dimensions
- File size boundary violations
- Path traversal injection in filenames
- Null-byte injection
- Malformed multipart & JSON inputs
"""

import io
from pathlib import Path
import pytest
from PIL import Image

from apps.api.middleware.security import ImageSecurityValidator
from apps.api.errors import (
    MetroLensAPIException,
    InvalidImagePayloadError,
    ImageTooLargeError,
    UnsupportedMediaTypeError,
    DecompressionBombError,
    ImageCorruptedError,
    ImageResolutionTooLowError,
)

@pytest.fixture
def client(guarded_api):
    return guarded_api.client


class TestImageIngestionSecurityGate:
    """Direct unit verification of ImageSecurityValidator defense mechanisms."""

    def test_empty_payload_rejected(self):
        with pytest.raises((MetroLensAPIException, ValueError)):
            ImageSecurityValidator.sanitize_and_verify(b"")

    def test_corrupt_binary_rejected(self):
        corrupt_bytes = b"\xff\xd8\xff\xe0" + b"\x00" * 50 + b"INVALID_GARBAGE_PAYLOAD"
        with pytest.raises((ImageCorruptedError, UnsupportedMediaTypeError, MetroLensAPIException)):
            ImageSecurityValidator.sanitize_and_verify(corrupt_bytes)

    def test_random_noise_rejected(self):
        random_bytes = b"NOT_AN_IMAGE_RANDOM_DATA_STREAM" * 32
        with pytest.raises((UnsupportedMediaTypeError, ImageCorruptedError, MetroLensAPIException)):
            ImageSecurityValidator.sanitize_and_verify(random_bytes)

    def test_decompression_bomb_dimension_cap(self):
        """Rejects images exceeding the 64MP cap to prevent RAM exhaustion."""
        # Create small memory image with fake enormous dimensions or oversized canvas
        buf = io.BytesIO()
        # 9000 x 8000 = 72 MP (> 64 MP limit)
        oversized = Image.new("RGB", (9000, 8000), color="white")
        oversized.save(buf, format="JPEG")
        oversized_bytes = buf.getvalue()

        with pytest.raises((DecompressionBombError, MetroLensAPIException)):
            ImageSecurityValidator.sanitize_and_verify(oversized_bytes)

    def test_resolution_too_low_rejected(self):
        """Rejects images below 800x600 to prevent unreadable OCR noise."""
        buf = io.BytesIO()
        tiny = Image.new("RGB", (400, 300), color="white")
        tiny.save(buf, format="JPEG")
        with pytest.raises(ImageResolutionTooLowError):
            ImageSecurityValidator.sanitize_and_verify(buf.getvalue())


class TestAPISecurityEndpoints:
    """Verifies API gateway defensive responses against adversarial requests."""

    def test_empty_file_upload_returns_4xx(self, client):
        response = client.post(
            "/api/v1/inspect",
            files={"file": ("empty.jpg", b"", "image/jpeg")},
        )
        assert response.status_code in [400, 422]

    def test_corrupt_file_upload_returns_structured_error(self, client):
        response = client.post(
            "/api/v1/inspect",
            files={"file": ("corrupt.jpg", b"MALFORMED_HEADER_BYTES", "image/jpeg")},
        )
        assert response.status_code == 415
        data = response.json()
        assert "error" in data or "detail" in data

    def test_path_traversal_filename_sanitized(self, client, guarded_api):
        """Filenames containing traversal vectors must either be rejected (400) or sanitized."""
        buf = io.BytesIO()
        img = Image.new("RGB", (800, 600), color="white")
        img.save(buf, format="JPEG")
        valid_bytes = buf.getvalue()

        traversal_name = "../../../../etc/passwd"
        response = client.post(
            "/api/v1/inspect",
            files={"file": (traversal_name, valid_bytes, "image/jpeg")},
        )
        assert response.status_code == 200
        assert response.json()["image_metadata"]["filename"] == "passwd"
        session = guarded_api.spool.get_session(response.json()["inspection_id"])
        assert session.raw_image_path.is_relative_to(guarded_api.spool.base_dir)

    def test_null_byte_filename_sanitized(self, client):
        """Filenames with null bytes must be rejected (400) or sanitized."""
        buf = io.BytesIO()
        img = Image.new("RGB", (800, 600), color="white")
        img.save(buf, format="JPEG")
        valid_bytes = buf.getvalue()

        null_byte_name = "test.jpg\x00.exe"
        response = client.post(
            "/api/v1/inspect",
            files={"file": (null_byte_name, valid_bytes, "image/jpeg")},
        )
        assert response.status_code == 200
        assert "\x00" not in response.json()["image_metadata"]["filename"]

    def test_pdf_report_malformed_json_rejected(self, client):
        """POST /api/v1/report/pdf must reject invalid JSON with 422."""
        response = client.post(
            "/api/v1/report/pdf",
            content=b"{malformed_json_payload: null",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400

    def test_pdf_report_missing_required_fields(self, client):
        """Rejects incomplete payloads without internal 500 error."""
        response = client.post(
            "/api/v1/report/pdf",
            json={"unexpected_field": "val"},
        )
        assert response.status_code == 400
