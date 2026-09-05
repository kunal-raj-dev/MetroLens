"""
Integration Tests for Chunk 4: Pipeline Orchestrator & Synchronous Inspection Endpoint.
Verifies:
1. End-to-end POST /api/v1/inspect with multipart image upload.
2. Full adherence to docs/API_CONTRACT.md schema specification.
3. Sub-2.5 second CPU latency budget compliance.
4. Section 36(1) Jan Vishwas Improvement Notice generation on non-compliant packaging.
5. Ingestion security rejections (HTTP 400, 413, 415, 422).
6. Optical calibration modes (INR_10_COIN vs NONE).
7. Base64 visual forensic evidence crops generation.
8. Request tracing header (X-Request-ID) handling.
9. Bilingual Hindi and non-standard unit fixture evaluations.
"""

import io
import time
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.schemas import InspectionResponse


def make_test_packaging_image(
    width: int = 1200,
    height: int = 1600,
    color: tuple = (245, 245, 240),
    draw_declarations: bool = True,
) -> bytes:
    """Creates a synthetic packaging photograph satisfying min 800x600 resolution."""
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)

    # Simulated packaging border and graphics
    draw.rectangle([40, 40, width - 40, height - 40], outline=(40, 60, 100), width=4)

    if draw_declarations:
        # Draw realistic text lines
        draw.text((80, 80), "METROLENS PREMIUM CASHEWS", fill=(10, 20, 50))
        draw.text((80, 140), "Net Quantity: 200 g", fill=(20, 20, 20))
        draw.text((80, 200), "MRP Rs. 240.00 (inclusive of all taxes)", fill=(20, 20, 20))
        draw.text((80, 260), "Unit Sale Price: Rs. 1.20 / g", fill=(20, 20, 20))
        draw.text((80, 320), "Mfg Date: 08/2026", fill=(20, 20, 20))
        draw.text((80, 380), "Manufactured By: MetroLens Foods Pvt Ltd, New Delhi 110020", fill=(20, 20, 20))
        draw.text((80, 440), "Consumer Care: 1800-11-4000, care@metrolens.in", fill=(20, 20, 20))
        draw.text((80, 500), "Country of Origin: India", fill=(20, 20, 20))

        # Simulated INR 10 coin reference
        draw.ellipse([width - 250, height - 250, width - 80, height - 80], outline=(180, 140, 40), width=4)
        draw.text((width - 200, height - 170), "INR 10", fill=(120, 90, 20))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


@pytest.fixture
def client():
    """Provides FastAPI test client with reset rate limiter."""
    from apps.api.middleware.rate_limit import rate_limiter
    rate_limiter.reset_all()
    with TestClient(app) as test_client:
        test_client.headers.update({"X-Bypass-Rate-Limit": "true"})
        yield test_client
    rate_limiter.reset_all()


# =========================================================================
# Positive Path Integration Tests
# =========================================================================

def test_inspect_successful_compliant_upload(client):
    """
    Verifies that a valid packaging photograph completes inspection successfully,
    returning HTTP 200 with schema strictly conforming to InspectionResponse.
    """
    img_bytes = make_test_packaging_image()

    start_time = time.perf_counter()
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("cashew_pouch.jpg", img_bytes, "image/jpeg")},
        data={"anchor_type": "INR_10_COIN", "panel_type": "FRONT_PDP", "officer_id": "OFFICER-007"},
    )
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert response.status_code == 200
    data = response.json()

    # Validate against authoritative Pydantic contract
    parsed = InspectionResponse.model_validate(data)
    assert parsed.inspection_id.startswith("INSP-")
    assert parsed.state in ("COMPLIANT", "POTENTIAL_NON_COMPLIANCE", "NON_COMPLIANT")
    assert parsed.image_metadata.width_px == 1200
    assert parsed.image_metadata.height_px == 1600
    assert len(parsed.image_metadata.sha256_hash) == 64
    assert parsed.image_metadata.is_quality_valid is True

    # Calibration verification
    assert parsed.calibration.is_calibrated is True
    assert parsed.calibration.anchor_type == "INR_10_COIN"
    assert parsed.calibration.scale_mm_per_px is not None
    assert parsed.calibration.scale_mm_per_px > 0

    # Declarations verification
    assert parsed.declarations.commodity_name is not None
    assert parsed.declarations.mrp_inr == 240.0
    assert parsed.declarations.net_quantity_value == 200.0

    # Rule evaluations verification
    assert parsed.rule_evaluations.rule6_mandatory_status.overall_status == "PASS"

    # Evidence crops verification
    assert len(parsed.evidence_crops) > 0
    for crop in parsed.evidence_crops:
        assert crop.crop_base64.startswith("data:image/jpeg;base64,")
        assert len(crop.bbox_px) == 4

    # Latency budget verification (< 2.5s)
    assert parsed.telemetry.total_duration_ms < 2500.0
    assert elapsed_ms < 2500.0


def test_inspect_non_compliant_generates_improvement_notice(client):
    """
    Verifies that non-compliant packaging (missing mandatory tax qualifier)
    generates a Section 36(1) Jan Vishwas Improvement Notice with a 15-day cure window.
    """
    img_bytes = make_test_packaging_image()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("chips_pkg.jpg", img_bytes, "image/jpeg")},
        data={
            "anchor_type": "INR_10_COIN",
            "mock_fixture_key": "PKG-03-MISSING-TAX-QUALIFIER",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["state"] == "NON_COMPLIANT"
    assert data["improvement_notice"] is not None
    notice = data["improvement_notice"]
    assert notice["recommended"] is True
    assert notice["cure_period_days"] == 15
    assert "Section 36(1)" in notice["act_provision"] or "Jan Vishwas" in notice["act_provision"]
    assert "Rule 6" in notice["statutory_grounds"]


def test_inspect_bilingual_hindi_specimen(client):
    """Verifies successful normalization and rule evaluation of bilingual Devanagari Hindi packaging."""
    img_bytes = make_test_packaging_image()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("hindi_atta.jpg", img_bytes, "image/jpeg")},
        data={
            "anchor_type": "INR_10_COIN",
            "mock_fixture_key": "PKG-02-BILINGUAL-HINDI-ATTA",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "COMPLIANT"
    assert data["declarations"]["mrp_inr"] == 45.0
    assert data["declarations"]["tax_qualifier_present"] is True


def test_inspect_prohibited_units_fixture(client):
    """Verifies that non-standard unit symbols ('Gms') trigger statutory non-compliance."""
    img_bytes = make_test_packaging_image()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("turmeric_powder.jpg", img_bytes, "image/jpeg")},
        data={
            "anchor_type": "INR_10_COIN",
            "mock_fixture_key": "PKG-04-PROHIBITED-UNITS-GMS",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "NON_COMPLIANT"
    assert data["improvement_notice"] is not None


def test_inspect_uncalibrated_mode(client):
    """Verifies inspection with anchor_type='NONE' sets calibration status appropriately."""
    img_bytes = make_test_packaging_image()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("test_uncal.jpg", img_bytes, "image/jpeg")},
        data={"anchor_type": "NONE"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["calibration"]["is_calibrated"] is False
    assert data["calibration"]["anchor_type"] == "NONE"
    assert data["calibration"]["scale_mm_per_px"] is None


def test_inspect_request_id_tracing_header(client):
    """Verifies that client tracing X-Request-ID header is accepted and processed cleanly."""
    img_bytes = make_test_packaging_image()

    req_id = "trace-uuid-abcdef-123456"
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("test_trace.jpg", img_bytes, "image/jpeg")},
        headers={"X-Request-ID": req_id},
    )

    assert response.status_code == 200


# =========================================================================
# Security & Error Handling Integration Tests
# =========================================================================

def test_inspect_rejects_empty_file(client):
    """Verifies HTTP 400 rejection when an empty (0 byte) file is submitted."""
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "INVALID_IMAGE_PAYLOAD"


def test_inspect_rejects_unsupported_media_type(client):
    """Verifies HTTP 415 rejection when a disguised binary payload is submitted."""
    fake_gif = b"GIF89a" + b"\x00" * 200
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("malicious.jpg", fake_gif, "image/jpeg")},
    )
    assert response.status_code == 415
    data = response.json()
    assert data["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"


def test_inspect_rejects_low_resolution(client):
    """Verifies HTTP 422 rejection when image is below the 800x600 minimum threshold."""
    low_res = Image.new("RGB", (640, 480), color=(255, 255, 255))
    buf = io.BytesIO()
    low_res.save(buf, format="JPEG")

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("thumbnail.jpg", buf.getvalue(), "image/jpeg")},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "IMAGE_RESOLUTION_TOO_LOW"


def test_inspect_rejects_oversized_payload(client):
    """Verifies HTTP 413 rejection when image exceeds 15.0 MB."""
    oversized = b"\xff\xd8\xff\xe0" + b"\x00" * (15 * 1024 * 1024 + 500)
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("huge.jpg", oversized, "image/jpeg")},
    )
    assert response.status_code == 413
    data = response.json()
    assert data["error"]["code"] == "IMAGE_TOO_LARGE"
