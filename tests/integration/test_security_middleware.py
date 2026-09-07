"""
Integration & Security Tests for Chunk 1: Upload Security Middleware & Ingestion Gate.
Verifies:
1. Magic-byte verification across JPEG, PNG, and WebP formats.
2. Rejection of unsupported or polyglot file signatures with HTTP 415 (UNSUPPORTED_MEDIA_TYPE).
3. Rejection of uploads exceeding 15.0 MB file size limit with HTTP 413 (IMAGE_TOO_LARGE).
4. Rejection of 0-byte or empty uploads with HTTP 400 (INVALID_IMAGE_PAYLOAD).
5. Decompression bomb firewall (> 64 Megapixels) rejecting pre-decode with HTTP 422 (DECOMPRESSION_BOMB_DETECTED).
6. Low resolution rejection (< 800x600) with HTTP 422 (IMAGE_RESOLUTION_TOO_LOW).
7. Truncated or corrupted pixel streams with HTTP 422 (IMAGE_CORRUPTED).
8. Comprehensive EXIF and GPS privacy sanitization.
9. Uniform JSON error envelope conforming to docs/API_CONTRACT.md Section 4.
10. HTTP security headers (CSP, HSTS, X-Content-Type-Options, X-Frame-Options).
"""

import io
import struct
import pytest
from PIL import Image, ImageDraw
from fastapi import FastAPI, UploadFile, File
from fastapi.testclient import TestClient

from apps.api.middleware.security import (
    ImageSecurityValidator,
    validate_and_sanitize_image_upload,
    MAX_UPLOAD_SIZE_BYTES,
    MAX_DECOMPRESSION_PIXELS,
    MIN_IMAGE_WIDTH,
    MIN_IMAGE_HEIGHT,
)
from apps.api.middleware.headers import SecurityHeadersMiddleware
from apps.api.errors import (
    MetroLensAPIException,
    InvalidImagePayloadError,
    ImageTooLargeError,
    UnsupportedMediaTypeError,
    DecompressionBombError,
    ImageCorruptedError,
    ImageResolutionTooLowError,
    metrolens_exception_handler,
)


def create_test_image_bytes(
    width: int = 1000,
    height: int = 800,
    fmt: str = "JPEG",
    include_exif_gps: bool = False,
) -> bytes:
    """Helper to synthesize valid test images in memory with optional EXIF GPS metadata."""
    img = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, width - 50, height - 50], outline=(10, 80, 160), width=4)
    draw.text((100, 100), f"TEST PACKAGING SPECIMEN {width}x{height}", fill=(0, 0, 0))

    buf = io.BytesIO()
    if include_exif_gps and fmt == "JPEG":
        exif = img.getexif()
        # 0x010f = Make, 0x0110 = Model, 0x0131 = Software
        exif[0x010F] = "MetroLens Mobile Device"
        exif[0x0110] = "LMO-Field-Scanner-X1"
        exif[0x0131] = "Android 14 Test Suite"
        # GPS IFD is tag 0x8825 (34853)
        gps_ifd = exif.get_ifd(0x8825)
        gps_ifd[1] = "N"  # GPSLatitudeRef
        gps_ifd[2] = (28.0, 37.0, 12.0)  # GPSLatitude
        gps_ifd[3] = "E"  # GPSLongitudeRef
        gps_ifd[4] = (77.0, 12.0, 56.0)  # GPSLongitude
        img.save(buf, format=fmt, exif=exif)
    else:
        img.save(buf, format=fmt)

    return buf.getvalue()


@pytest.fixture
def valid_jpeg_bytes():
    return create_test_image_bytes(width=1200, height=900, fmt="JPEG")


@pytest.fixture
def valid_png_bytes():
    return create_test_image_bytes(width=1000, height=800, fmt="PNG")


@pytest.fixture
def valid_webp_bytes():
    return create_test_image_bytes(width=1000, height=800, fmt="WEBP")


# =========================================================================
# 1. Magic Bytes & Format Verification Tests
# =========================================================================

def test_magic_bytes_valid_jpeg(valid_jpeg_bytes):
    """Verifies that genuine JPEG magic bytes (FF D8 FF) are accepted."""
    fmt = ImageSecurityValidator.verify_magic_bytes(valid_jpeg_bytes[:16])
    assert fmt == "JPEG"


def test_magic_bytes_valid_png(valid_png_bytes):
    """Verifies that genuine PNG magic bytes (89 50 4E 47 0D 0A 1A 0A) are accepted."""
    fmt = ImageSecurityValidator.verify_magic_bytes(valid_png_bytes[:16])
    assert fmt == "PNG"


def test_magic_bytes_valid_webp(valid_webp_bytes):
    """Verifies that genuine WebP magic bytes (RIFF....WEBP) are accepted."""
    fmt = ImageSecurityValidator.verify_magic_bytes(valid_webp_bytes[:16])
    assert fmt == "WEBP"


def test_magic_bytes_rejects_unsupported_formats():
    """Verifies that PDF, GIF, BMP, ZIP, and executable headers are rejected."""
    bad_payloads = [
        (b"%PDF-1.7\r\n...", "PDF file"),
        (b"GIF89a\x00\x00...", "GIF animation"),
        (b"BM\x00\x00\x00\x00...", "BMP bitmap"),
        (b"PK\x03\x04\x14\x00...", "ZIP / Polyglot archive"),
        (b"MZ\x90\x00\x03\x00...", "Windows PE executable"),
        (b"<html><body>...", "HTML string"),
        (b"{\x22key\x22: 123}", "JSON payload"),
    ]
    for raw_bytes, description in bad_payloads:
        with pytest.raises(UnsupportedMediaTypeError) as exc_info:
            ImageSecurityValidator.verify_magic_bytes(raw_bytes)
        assert exc_info.value.status_code == 415
        assert exc_info.value.code == "UNSUPPORTED_MEDIA_TYPE"


def test_disguised_extension_rejection():
    """Verifies that renaming an executable or text file to .jpg is caught by magic bytes."""
    disguised_file = b"MZ\x90\x00Fake executable disguised as photo"
    with pytest.raises(UnsupportedMediaTypeError) as exc_info:
        validate_and_sanitize_image_upload(disguised_file, filename="innocent_package.jpg")
    assert exc_info.value.status_code == 415
    assert exc_info.value.code == "UNSUPPORTED_MEDIA_TYPE"


# =========================================================================
# 2. File Size & Payload Limits Tests
# =========================================================================

def test_empty_payload_rejection():
    """Verifies that a 0-byte upload is rejected with HTTP 400 (INVALID_IMAGE_PAYLOAD)."""
    with pytest.raises(InvalidImagePayloadError) as exc_info:
        validate_and_sanitize_image_upload(b"", filename="empty.jpg")
    assert exc_info.value.status_code == 400
    assert exc_info.value.code == "INVALID_IMAGE_PAYLOAD"


def test_oversized_payload_rejection():
    """Verifies that a payload > 15.0 MB is rejected with HTTP 413 (IMAGE_TOO_LARGE)."""
    # Create fake payload just over 15MB
    large_size = MAX_UPLOAD_SIZE_BYTES + 1024
    fake_large_payload = b"\xff\xd8\xff" + b"\x00" * (large_size - 3)

    with pytest.raises(ImageTooLargeError) as exc_info:
        validate_and_sanitize_image_upload(fake_large_payload, filename="huge_photo.jpg")
    assert exc_info.value.status_code == 413
    assert exc_info.value.code == "IMAGE_TOO_LARGE"
    assert exc_info.value.details["file_size_bytes"] == large_size


# =========================================================================
# 3. Decompression Bomb & Resolution Gate Tests
# =========================================================================

def test_streaming_header_bomb_detection():
    """
    Verifies that a malicious PNG declaring > 64MP is caught by the
    streaming pre-decode header parser without allocating raster memory.
    """
    # Synthesize PNG IHDR declaring 10,000 x 10,000 pixels (100 Megapixels)
    header = b"\x89PNG\r\n\x1a\n"
    # IHDR chunk: length (13 bytes) + 'IHDR' + width + height + bitdepth + colortype + ...
    ihdr_payload = b"IHDR" + struct.pack(">IIBBBBB", 10000, 10000, 8, 2, 0, 0, 0)
    fake_bomb_png = header + struct.pack(">I", 13) + ihdr_payload + b"\x00" * 64

    with pytest.raises(DecompressionBombError) as exc_info:
        validate_and_sanitize_image_upload(fake_bomb_png, filename="bomb.png")
    assert exc_info.value.status_code == 422
    assert exc_info.value.code == "DECOMPRESSION_BOMB_DETECTED"
    assert exc_info.value.details["total_pixels"] == 100_000_000


def test_low_resolution_rejection():
    """Verifies that images below 800 x 600 are rejected with HTTP 422 (IMAGE_RESOLUTION_TOO_LOW)."""
    small_image_bytes = create_test_image_bytes(width=640, height=480, fmt="JPEG")
    with pytest.raises(ImageResolutionTooLowError) as exc_info:
        validate_and_sanitize_image_upload(small_image_bytes, filename="thumbnail.jpg")
    assert exc_info.value.status_code == 422
    assert exc_info.value.code == "IMAGE_RESOLUTION_TOO_LOW"
    assert exc_info.value.details["width"] == 640
    assert exc_info.value.details["height"] == 480


def test_corrupted_image_stream_rejection():
    """Verifies that truncated or invalid pixel streams raise HTTP 422 (IMAGE_CORRUPTED)."""
    # Valid JPEG header followed by junk bytes
    corrupted_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00" + b"\xff" * 50
    with pytest.raises(ImageCorruptedError) as exc_info:
        validate_and_sanitize_image_upload(corrupted_bytes, filename="corrupt.jpg")
    assert exc_info.value.status_code == 422
    assert exc_info.value.code == "IMAGE_CORRUPTED"


# =========================================================================
# 4. Privacy Sanitization & EXIF Stripping Tests
# =========================================================================

def test_exif_gps_stripping_and_sanitization():
    """
    Verifies that all GPS coordinates and camera serial data are completely
    stripped from the output sanitized bytes.
    """
    gps_jpeg_bytes = create_test_image_bytes(width=1000, height=750, fmt="JPEG", include_exif_gps=True)

    record = validate_and_sanitize_image_upload(gps_jpeg_bytes, filename="field_capture.jpg")
    assert record.had_gps_data is True
    assert record.exif_tags_stripped > 0

    # Inspect the sanitized output with PIL
    sanitized_pil = Image.open(io.BytesIO(record.sanitized_bytes))
    exif_out = sanitized_pil.getexif()

    # The sanitized image must contain ZERO GPS or camera tags
    assert len(exif_out) == 0, f"Expected 0 EXIF tags in sanitized output, found {len(exif_out)}"
    assert 34853 not in exif_out, "GPSInfo tag was not stripped!"


def test_clean_image_sha256_reproducibility(valid_jpeg_bytes):
    """Verifies that raw SHA-256 hash is correctly calculated and matches hashlib."""
    import hashlib
    expected_hash = hashlib.sha256(valid_jpeg_bytes).hexdigest()

    record = validate_and_sanitize_image_upload(valid_jpeg_bytes, filename="package.jpg")
    assert record.raw_sha256 == expected_hash
    assert record.width == 1200
    assert record.height == 900
    assert record.format == "JPEG"


# =========================================================================
# 5. FastAPI Exception Handlers & Security Headers End-to-End Tests
# =========================================================================

@pytest.fixture
def test_app():
    """Creates an isolated FastAPI app wired with security middleware and error handlers."""
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_exception_handler(MetroLensAPIException, metrolens_exception_handler)

    @app.post("/test-upload")
    async def upload_endpoint(file: UploadFile = File(...)):
        content = await file.read()
        record = validate_and_sanitize_image_upload(content, filename=file.filename)
        return {
            "status": "success",
            "sha256": record.raw_sha256,
            "width": record.width,
            "height": record.height,
        }

    return app


def test_api_security_headers_present(test_app):
    """Verifies that all required HTTP security headers are injected into responses."""
    client = TestClient(test_app)
    response = client.post("/test-upload", files={"file": ("test.txt", b"not-an-image", "text/plain")})

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert "max-age=31536000" in response.headers["Strict-Transport-Security"]


def test_api_error_envelope_structure(test_app):
    """Verifies that HTTP exceptions return the canonical JSON error contract."""
    client = TestClient(test_app)
    response = client.post("/test-upload", files={"file": ("test.pdf", b"%PDF-1.7\r\n...", "application/pdf")})

    assert response.status_code == 415
    json_data = response.json()
    assert "error" in json_data
    err = json_data["error"]
    assert err["code"] == "UNSUPPORTED_MEDIA_TYPE"
    assert "JPEG, PNG, or WebP" in err["message"]
    assert "remediation" in err
    assert "timestamp" in err
    assert "details" in err


def test_api_successful_upload_roundtrip(test_app, valid_jpeg_bytes):
    """Verifies that a valid packaging image upload passes all gates and returns 200 OK."""
    client = TestClient(test_app)
    response = client.post(
        "/test-upload",
        files={"file": ("cashew_pouch.jpg", valid_jpeg_bytes, "image/jpeg")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["width"] == 1200
    assert data["height"] == 900
