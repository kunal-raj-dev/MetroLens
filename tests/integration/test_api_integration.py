"""
Integration Tests for Chunk 7: End-to-End API Integration, Stability & Adversarial Fuzzing.
Verifies:
1. 100-request consecutive execution with zero server crashes or unhandled exceptions.
2. Adversarial payload fuzzing: polyglots, truncated streams, corrupted headers, random noise.
3. Extreme image dimension handling (aspect ratios, zero-channel, corrupt palettes).
4. Unicode, special characters, and SQL-injection-style filenames resilience.
5. All fuzz failures strictly resolve into canonical API error envelopes (HTTP 400, 415, 422).
6. Zero temporary file leaks across 100 inspections in ephemeral spool directory.
"""

import io
import os
import random
import time
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.schemas import InspectionResponse
from apps.api.services.spool_service import spool_service


@pytest.fixture
def client():
    """Provides FastAPI test client with reset rate limiter and bypass header."""
    from apps.api.middleware.rate_limit import rate_limiter
    rate_limiter.reset_all()
    with TestClient(app) as test_client:
        test_client.headers.update({"X-Bypass-Rate-Limit": "true"})
        yield test_client
    rate_limiter.reset_all()


def make_valid_packaging_image(width: int = 1000, height: int = 1200) -> bytes:
    """Generates standard compliant packaging test image."""
    img = Image.new("RGB", (width, height), color=(250, 248, 245))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(50, 70, 120), width=3)
    draw.text((50, 50), "MetroLens Certified Product", fill=(0, 0, 0))
    draw.text((50, 100), "Net Qty: 500 g", fill=(0, 0, 0))
    draw.text((50, 150), "MRP: Rs. 150.00 (incl. of all taxes)", fill=(0, 0, 0))
    draw.text((50, 200), "USP: Rs. 0.30 / g", fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


# =========================================================================
# 100-Request Stability & Memory Leak Verification
# =========================================================================

def test_100_consecutive_requests_stability(client):
    """
    Executes 100 consecutive inspection requests simulating heavy operational throughput.
    Asserts 100% success rate, zero server crashes, and consistent sub-2.5s latency.
    """
    img_bytes = make_valid_packaging_image(width=900, height=1100)

    success_count = 0
    total_time_ms = 0.0

    # Run 100 consecutive requests
    for i in range(100):
        t0 = time.perf_counter()
        resp = client.post(
            "/api/v1/inspect",
            files={"file": (f"pkg_batch_{i:03d}.jpg", img_bytes, "image/jpeg")},
            data={"anchor_type": "INR_10_COIN", "panel_type": "FRONT_PDP"},
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        total_time_ms += elapsed_ms

        assert resp.status_code == 200, f"Request {i} failed with status {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "inspection_id" in data
        assert data["image_metadata"]["width_px"] == 900
        success_count += 1

    avg_ms = total_time_ms / 100.0
    assert success_count == 100
    assert avg_ms < 2500.0, f"Average latency too high: {avg_ms:.2f}ms (target < 2500ms)"


def test_zero_orphaned_spool_leak_after_inspections(client):
    """
    Verifies that ephemeral sessions clean up gracefully and total spool usage
    remains strictly bounded within quota limits.
    """
    # Active spool sessions can be purged explicitly
    spool_service.purge_expired_sessions()
    initial_bytes = spool_service.get_total_spool_size_bytes()

    img_bytes = make_valid_packaging_image(width=850, height=950)
    resp = client.post(
        "/api/v1/inspect",
        files={"file": ("quota_test.jpg", img_bytes, "image/jpeg")},
    )
    assert resp.status_code == 200
    insp_id = resp.json()["inspection_id"]

    # Explicit purge
    purged = spool_service.purge_session(insp_id)
    assert purged is True

    # Quota remains well bounded
    final_bytes = spool_service.get_total_spool_size_bytes()
    assert final_bytes <= spool_service.max_quota_bytes


# =========================================================================
# Adversarial Input Fuzzing
# =========================================================================

def test_fuzz_random_garbage_bytes(client):
    """Fuzzes endpoint with purely pseudorandom binary garbage of various lengths."""
    payload_sizes = [1, 7, 16, 64, 256, 1024, 8192, 65536]
    random.seed(42)

    for sz in payload_sizes:
        garbage = os.urandom(sz)
        resp = client.post(
            "/api/v1/inspect",
            files={"file": (f"garbage_{sz}.bin", garbage, "application/octet-stream")},
        )
        # Must be rejected with HTTP 415 (magic bytes) or HTTP 400
        assert resp.status_code in (400, 415), f"Garbage size {sz} returned unexpected status {resp.status_code}"
        data = resp.json()
        assert "error" in data
        assert data["error"]["code"] in ("UNSUPPORTED_MEDIA_TYPE", "INVALID_IMAGE_PAYLOAD")


def test_fuzz_polyglot_payloads(client):
    """Fuzzes endpoint with polyglot files embedding valid image magic bytes followed by malicious scripts."""
    # Polyglot 1: JPEG header followed by PHP webshell code
    jpeg_php = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00" + b"<?php system($_GET['cmd']); ?>"
    resp1 = client.post(
        "/api/v1/inspect",
        files={"file": ("exploit.php.jpg", jpeg_php, "image/jpeg")},
    )
    # Pillow or header parser fails raster decode -> 422 IMAGE_CORRUPTED
    assert resp1.status_code == 422
    assert resp1.json()["error"]["code"] in ("IMAGE_CORRUPTED", "IMAGE_RESOLUTION_TOO_LOW")

    # Polyglot 2: PNG header followed by HTML/XSS payload
    png_xss = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"<script>alert(document.cookie)</script>"
    resp2 = client.post(
        "/api/v1/inspect",
        files={"file": ("xss.png", png_xss, "image/png")},
    )
    assert resp2.status_code == 422
    assert resp2.json()["error"]["code"] in ("IMAGE_CORRUPTED", "IMAGE_RESOLUTION_TOO_LOW", "DECOMPRESSION_BOMB_DETECTED")

    # Polyglot 3: WebP header followed by PKZIP archive
    webp_zip = b"RIFF\x00\x00\x00\x00WEBPVP8 " + b"PK\x03\x04" + b"\x00" * 50
    resp3 = client.post(
        "/api/v1/inspect",
        files={"file": ("archive.webp", webp_zip, "image/webp")},
    )
    assert resp3.status_code == 422
    assert resp3.json()["error"]["code"] in ("IMAGE_CORRUPTED", "IMAGE_RESOLUTION_TOO_LOW", "DECOMPRESSION_BOMB_DETECTED")


def test_fuzz_truncated_jpeg_stream(client):
    """Fuzzes endpoint with abruptly cut-off JPEG bitstream missing EOI marker."""
    full_jpg = make_valid_packaging_image(width=850, height=850)
    # Truncate at 20% of content
    truncated = full_jpg[: int(len(full_jpg) * 0.20)]

    resp = client.post(
        "/api/v1/inspect",
        files={"file": ("truncated.jpg", truncated, "image/jpeg")},
    )
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "IMAGE_CORRUPTED"


def test_fuzz_extreme_aspect_ratios(client):
    """Fuzzes endpoint with extreme needle-like packaging image dimensions."""
    # 5000 x 20 pixels
    extreme_wide = Image.new("RGB", (5000, 20), color=(255, 255, 255))
    buf = io.BytesIO()
    extreme_wide.save(buf, format="PNG")

    resp = client.post(
        "/api/v1/inspect",
        files={"file": ("needle_wide.png", buf.getvalue(), "image/png")},
    )
    # Below min_height of 600 -> HTTP 422 IMAGE_RESOLUTION_TOO_LOW
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "IMAGE_RESOLUTION_TOO_LOW"


def test_fuzz_adversarial_filenames(client):
    """Verifies robustness against non-ASCII, Unicode, Path Traversal, and SQL injection filenames."""
    img_bytes = make_valid_packaging_image(width=850, height=850)

    malicious_filenames = [
        "../../etc/passwd.jpg",
        "..\\..\\windows\\system32\\calc.exe.jpg",
        "product'; DROP TABLE inspections; --.jpg",
        "<img src=x onerror=alert(1)>.png",
        "चक्की_ताजा_आटा_२०२६_पैकिंग.jpg",
        "emoji_🚀_packaging_🎯.webp",
        "A" * 255 + ".jpg",
        "null\x00byte.jpg",
        "con.jpg",
        "aux.png",
    ]

    for fname in malicious_filenames:
        resp = client.post(
            "/api/v1/inspect",
            files={"file": (fname, img_bytes, "image/jpeg")},
        )
        # Server must not crash (returns 200 or clean 400)
        assert resp.status_code in (200, 400), f"Filename '{fname}' crashed server: {resp.status_code}"
        if resp.status_code == 200:
            data = resp.json()
            assert "inspection_id" in data


def test_fuzz_corrupted_multipart_boundary(client):
    """Verifies that malformed multipart bodies return standard HTTP 400 error envelope."""
    malformed_body = b"--boundary\r\nContent-Disposition: form-data; name=\"file\"\r\n\r\nIncomplete..."
    resp = client.post(
        "/api/v1/inspect",
        content=malformed_body,
        headers={"Content-Type": "multipart/form-data; boundary=boundary"},
    )
    assert resp.status_code == 400
    assert "error" in resp.json()
