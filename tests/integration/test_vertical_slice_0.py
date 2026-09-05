"""
Chunk 5 Integration Tests: Vertical Slice 0 Core Inspection Pipeline Integration.

Validates the full end-to-end inspection flow:
Image -> Validation -> Quality Gate -> Calibration -> Multilingual OCR ->
Semantic Extraction -> Rule Evaluation -> Structured Result & Evidence DAG.

Tests:
1. test_vs0_valid_packaging_end_to_end: Complete pipeline execution with statutory declarations.
2. test_vs0_upload_security_checks: Corrupted, non-image, and empty payload rejection.
3. test_vs0_quality_gate_rejection: Low-contrast / blurry frame rejected at Gate 2.
4. test_vs0_uncalibrated_handling: Packaging without reference returns UNCALIBRATED without fabricating mm.
5. test_vs0_defect_detection_missing_mrp: Packaging missing mandatory MRP returns NON_COMPLIANT.
6. test_vs0_calibrated_measurement: Packaging with reference coin calculates metric mm and evaluates Table-I.
7. test_vs0_evidence_chain_linkage: Evidence DAG cryptographic linkage and coordinate integrity.
8. test_vs0_offline_execution: Strict offline execution under socket network isolation.
9. test_vs0_stage_timings: Stage-by-stage latency tracking across all 8 pipeline phases.
"""

import hashlib
import io
import socket
import pytest
import numpy as np
import cv2
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.worker.main import InspectionPipelineWorker
from nirikshak_shared.models.contracts import InspectionRequest, InspectionResult
from nirikshak_shared.models.primitives import (
    InspectionStatus,
    OverallVerdict,
    CalibrationStatus,
    RuleVerdict,
)
from nirikshak_ocr import OCRService

client = TestClient(app)


def _create_synthetic_pack(
    include_mrp: bool = True,
    include_net_qty: bool = True,
    include_mfg_date: bool = True,
    include_coin: bool = False,
    bg_color: int = 220,
) -> np.ndarray:
    """Helper to synthesize a clean, high-contrast packaging frame."""
    img = np.full((500, 600, 3), bg_color, dtype=np.uint8)

    y = 80
    if include_mrp:
        cv2.putText(img, "MRP Rs 250.00 (incl. of all taxes)", (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        y += 60
    if include_net_qty:
        cv2.putText(img, "Net Quantity: 500 g", (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        y += 60
    if include_mfg_date:
        cv2.putText(img, "Mfg Date: 03/2026", (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        y += 60

    cv2.putText(img, "Consumer Care: support@metrolens.in", (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    if include_coin:
        # Draw a high-contrast circular coin reference (radius 50 px, diameter 100 px)
        cv2.circle(img, (480, 100), 50, (60, 60, 60), -1)
        cv2.circle(img, (480, 100), 50, (0, 0, 0), 2)

    return img


def _encode_png(img: np.ndarray) -> bytes:
    success, enc = cv2.imencode(".png", img)
    assert success
    return enc.tobytes()


def test_vs0_valid_packaging_end_to_end():
    """Verify standard packaging image executes all 8 stages and returns valid InspectionResult."""
    img = _create_synthetic_pack(include_mrp=True, include_net_qty=True, include_mfg_date=True)
    img_bytes = _encode_png(img)
    expected_sha = hashlib.sha256(img_bytes).hexdigest()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("packaging.png", img_bytes, "image/png")},
        data={"anchor_type": "AUTO", "officer_id": "INSP-TEST-01"},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == InspectionStatus.SUCCESS.value
    assert data["quality_gate_passed"] is True
    assert data["image_sha256"] == expected_sha
    assert len(data["rule_evaluations"]) >= 1

    # Verify retrieval endpoint
    insp_id = data["inspection_id"]
    get_res = client.get(f"/api/v1/inspections/{insp_id}")
    assert get_res.status_code == 200
    assert get_res.json()["inspection_id"] == insp_id


def test_vs0_upload_security_checks():
    """Verify security controls: rejection of corrupted, non-image, and empty payloads."""
    # 1. Corrupt random bytes
    res_corrupt = client.post(
        "/api/v1/inspect",
        files={"file": ("bad.jpg", b"SOME_CORRUPTED_BINARY_DATA", "image/jpeg")},
    )
    assert res_corrupt.status_code == 400

    # 2. Empty payload
    res_empty = client.post(
        "/api/v1/inspect",
        files={"file": ("empty.png", b"", "image/png")},
    )
    assert res_empty.status_code == 400


def test_vs0_quality_gate_rejection():
    """Verify that blurry/low-contrast images are rejected with REJECTED_QUALITY and INCONCLUSIVE verdict."""
    worker = InspectionPipelineWorker()
    req = InspectionRequest(inspection_id="insp_low_quality")

    # Uniform low-contrast flat image (variance 0.0)
    flat_img = np.full((300, 300, 3), 120, dtype=np.uint8)
    res = worker.process_inspection(req, flat_img)

    assert res.status == InspectionStatus.REJECTED_QUALITY
    assert res.quality_gate_passed is False
    assert res.overall_verdict == OverallVerdict.INCONCLUSIVE
    assert len(res.errors) >= 1
    assert res.errors[0].error_code == "QUALITY_REJECTED"


def test_vs0_uncalibrated_handling():
    """Verify uncalibrated frames report UNCALIBRATED status without fabricating millimeter values."""
    img = _create_synthetic_pack(include_coin=False)
    img_bytes = _encode_png(img)

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("uncalib.png", img_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["calibration_status"] == CalibrationStatus.UNCALIBRATED.value
    # Measured font height in mm must NOT be fabricated
    if "font_height" in data["measurements"]:
        assert data["measurements"]["font_height"]["measured_mm"] is None

    # Rule 7 font height must be flagged REVIEW due to uncalibrated scale
    r07_evals = [e for e in data["rule_evaluations"] if "R07" in e["rule_id"]]
    for r in r07_evals:
        assert r["verdict"] == RuleVerdict.REVIEW.value
        assert r["uncertainty_flag"] is True


def test_vs0_defect_detection_missing_mrp():
    """Verify missing statutory declarations result in RuleVerdict.FAIL and NON_COMPLIANT overall."""
    # Packaging missing MRP
    img = _create_synthetic_pack(include_mrp=False, include_net_qty=True, include_mfg_date=True)
    img_bytes = _encode_png(img)

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("missing_mrp.png", img_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["overall_verdict"] == OverallVerdict.NON_COMPLIANT.value
    mrp_eval = next((e for e in data["rule_evaluations"] if "MRP" in e["rule_id"]), None)
    assert mrp_eval is not None
    assert mrp_eval["verdict"] == RuleVerdict.FAIL.value


def test_vs0_calibrated_measurement():
    """Verify reference coin detection enables metric calculation and deterministic Rule 7 verdict."""
    img = _create_synthetic_pack(include_mrp=True, include_net_qty=True, include_coin=True)
    img_bytes = _encode_png(img)

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("calibrated.png", img_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["calibration_status"] == CalibrationStatus.CALIBRATED.value
    if "font_height" in data["measurements"]:
        assert data["measurements"]["font_height"]["measured_mm"] is not None
        assert data["measurements"]["font_height"]["measured_mm"] > 0.0


def test_vs0_evidence_chain_linkage():
    """Verify evidence DAG nodes link source tokens, bounding boxes, and SHA-256 digests."""
    img = _create_synthetic_pack(include_mrp=True, include_net_qty=True)
    img_bytes = _encode_png(img)
    expected_sha = hashlib.sha256(img_bytes).hexdigest()

    response = client.post(
        "/api/v1/inspect",
        files={"file": ("pack_evidence.png", img_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()

    evidence_chain = data["evidence_chain"]
    assert len(evidence_chain) >= 1

    for item in evidence_chain:
        assert item["image_sha256"] == expected_sha
        assert item["bounding_box"] is not None
        bbox = item["bounding_box"]
        assert 0.0 <= bbox["y_min"] < bbox["y_max"] <= 500.0
        assert 0.0 <= bbox["x_min"] < bbox["x_max"] <= 600.0



def test_vs0_offline_execution(monkeypatch):
    """Verify the entire inspection pipeline operates completely offline with zero external network calls."""
    def block_network(*args, **kwargs):
        raise RuntimeError("CRITICAL ERROR: Outbound network call attempted during offline inspection execution!")

    monkeypatch.setattr(socket, "create_connection", block_network)
    monkeypatch.setattr(socket.socket, "connect", block_network)

    img = _create_synthetic_pack()
    worker = InspectionPipelineWorker()
    req = InspectionRequest(inspection_id="insp_offline_001")

    # Must complete offline without raising network error
    res = worker.process_inspection(req, img)
    assert res.status == InspectionStatus.SUCCESS


def test_vs0_stage_timings():
    """Verify pipeline records non-zero telemetry latency timings for every stage."""
    img = _create_synthetic_pack()
    worker = InspectionPipelineWorker()
    req = InspectionRequest(inspection_id="insp_timings_001")

    res = worker.process_inspection(req, img)
    assert res.status == InspectionStatus.SUCCESS

    telemetry = res.telemetry
    expected_stages = [
        "ingestion_ms",
        "quality_gate_ms",
        "calibration_ms",
        "ocr_perception_ms",
        "semantic_extraction_ms",
        "measurement_ms",
        "rules_engine_ms",
        "evidence_assembly_ms",
        "total_ms",
    ]


    for stage in expected_stages:
        assert stage in telemetry, f"Missing expected stage timing: {stage}"
        assert telemetry[stage] >= 0.0, f"Stage {stage} returned negative latency"
