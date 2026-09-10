"""Authenticated API integration fixtures; no fixture control is exposed over HTTP.

OCR model quality and image-quality scoring have dedicated component tests. These
tests inject their outputs, exercising the real upload validator, normalizer,
rules engine, record store and report renderer without model downloads.
"""

import importlib
import io
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from PIL import Image


API_KEY = "isolated-integration-test-key-" + "x" * 40


@pytest.fixture
def guarded_api(monkeypatch, tmp_path_factory):
    # Keep evidence+atomic PDF paths below Windows' legacy path length ceiling.
    tmp_path = tmp_path_factory.mktemp("api")
    monkeypatch.setenv("METROLENS_API_KEY", API_KEY)
    monkeypatch.setenv("METROLENS_SPOOL_DIR", str(tmp_path / "spool"))
    main = importlib.import_module("apps.api.main")
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    store_module = importlib.import_module("apps.api.services.inspection_store")
    from apps.api.middleware.rate_limit import rate_limiter
    from apps.api.routes import inspect, report, audit
    from apps.api.services.spool_service import SpoolService

    spool = SpoolService(base_dir=tmp_path / "evidence", auto_start_daemon=False)
    store = store_module.InspectionStore()
    monkeypatch.setattr(main, "spool_service", spool)
    monkeypatch.setattr(inspect.pipeline_orchestrator, "spooler", spool)
    monkeypatch.setattr(inspect, "inspection_store", store)
    monkeypatch.setattr(store_module, "inspection_store", store)
    monkeypatch.setattr(report, "spool_service", spool)
    monkeypatch.setattr(audit, "spool_service", spool)
    monkeypatch.setattr(module, "check_image_quality", lambda image: SimpleNamespace(
        passed=True, laplacian_variance=200.0, glare_ratio=0.0))
    # Throughput tests vary the server-side quota only in their isolated fixture.
    # The limiter itself is still exercised separately with its production limit.
    monkeypatch.setattr(rate_limiter, "requests_per_window", 1000)
    rate_limiter.reset_all()

    fixture_path = Path(__file__).parent / "fixtures" / "mock_ocr_tokens.json"
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))["fixtures"]

    def set_tokens(key="PKG-01-COMPLIANT-FMCG-CASHEWS"):
        tokens = [SimpleNamespace(**item) for item in fixtures[key]["tokens"]]
        monkeypatch.setattr(inspect.pipeline_orchestrator, "_get_ocr_service", lambda: SimpleNamespace(
            extract=lambda *args, **kwargs: SimpleNamespace(tokens=tokens)))
        return tokens

    set_tokens()
    buffer = io.BytesIO()
    Image.new("RGB", (800, 600), "gray").save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    client = TestClient(main.app, raise_server_exceptions=False)
    client.headers["Authorization"] = f"Bearer {API_KEY}"

    def upload():
        response = client.post("/api/v1/inspect", data={"anchor_type": "NONE"},
            files={"file": ("packaging.png", image_bytes, "image/png")})
        assert response.status_code == 200, response.text
        return response.json()

    yield SimpleNamespace(client=client, spool=spool, store=store,
        set_tokens=set_tokens, upload=upload, image_bytes=image_bytes)
    client.close()
    rate_limiter.reset_all()
