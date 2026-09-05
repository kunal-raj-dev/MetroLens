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
    assert data["service"] == "nirikshak-api"


def test_get_inspection_endpoint():
    response = client.get("/api/v1/inspections/insp_123")
    assert response.status_code == 200
    data = response.json()
    assert data["inspection_id"] == "insp_123"
    assert data["status"] == "SUCCESS"
