"""
Smoke test for nirikshak-api FastAPI application.
"""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] in ["nirikshak-api", "metrolens-api"]


def test_get_inspection_endpoint():
    response = client.get("/api/v1/inspections/insp_123")
    assert response.status_code == 200
    data = response.json()
    assert data["inspection_id"] == "insp_123"
    assert data["status"] == "SUCCESS"


def test_inspect_upload_endpoint_valid_image():
    import cv2
    import numpy as np
    import io

    # Create synthetic test packaging image with realistic matte surface (no specular glare)
    img = np.full((300, 400, 3), 220, dtype=np.uint8)
    cv2.putText(img, "MRP Rs 150.00", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "Net Qty: 500 g", (30, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(img, "Mfg Date: 01/2026", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    success, enc = cv2.imencode(".png", img)
    assert success

    file_payload = ("test_pack.png", enc.tobytes(), "image/png")
    response = client.post(
        "/api/v1/inspect",
        files={"file": file_payload},
        data={"anchor_type": "AUTO", "officer_id": "TEST-OFFICER-42"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "inspection_id" in data
    assert data["quality_gate_passed"] is True
    assert "overall_verdict" in data
    assert "telemetry" in data


def test_inspect_upload_corrupt_payload():
    corrupt_bytes = b"NOT_A_VALID_IMAGE_HEADER_AT_ALL"
    response = client.post(
        "/api/v1/inspect",
        files={"file": ("bad.jpg", corrupt_bytes, "image/jpeg")},
    )
    assert response.status_code == 400
    assert "detail" in response.json()

