"""
Unit Tests for Evidentiary Custody Preserver and Section 63 BSA Envelope Vault
=============================================================================
Verifies cryptographic sealing, PBKDF2 stream encryption, HMAC authentication,
and tamper-detection mechanisms for judicial court evidence packages.
"""

import hashlib
import json
from pathlib import Path
import pytest

from apps.api.forensics.custody_preserver import (
    EvidentiaryCustodyPreserver,
    EvidenceEnvelope,
    ForensicCaptureMetadata,
)


@pytest.fixture
def sample_metadata() -> ForensicCaptureMetadata:
    return ForensicCaptureMetadata(
        device_make="Samsung",
        device_model="Galaxy S23 Enterprise Field Edition",
        sensor_serial_number="SEN-SN-9982314-IN",
        capture_timestamp_utc="2026-09-05T09:30:00.123456Z",
        gps_latitude=28.613939,
        gps_longitude=77.209021,
        gps_altitude_meters=216.5,
        lens_focal_length_mm=23.0,
        iso_speed=100,
        shutter_speed_seconds=0.002,
    )


@pytest.fixture
def sample_raw_image_bytes() -> bytes:
    return bytes([(i * 37 + 13) % 256 for i in range(1024)])


@pytest.fixture
def custody_preserver(tmp_path: Path) -> EvidentiaryCustodyPreserver:
    master_key = b"COURT_VAULT_TEST_SECRET_KEY_1234567890"
    return EvidentiaryCustodyPreserver(
        vault_master_key=master_key,
        vault_storage_dir=tmp_path / "vault",
    )


def test_seal_and_verify_evidence_integrity(
    custody_preserver: EvidentiaryCustodyPreserver,
    sample_metadata: ForensicCaptureMetadata,
    sample_raw_image_bytes: bytes,
):
    inspection_id = "insp-sec63-001"
    officer_badge = "LMO-MH-ZONE4-4029"

    envelope = custody_preserver.seal_evidence(
        inspection_id=inspection_id,
        officer_badge=officer_badge,
        raw_image_bytes=sample_raw_image_bytes,
        metadata=sample_metadata,
    )

    assert envelope.envelope_id.startswith("ENV-INSP-SEC")
    assert envelope.inspection_id == inspection_id
    assert envelope.custody_officer_badge == officer_badge
    assert envelope.raw_image_sha256 == hashlib.sha256(sample_raw_image_bytes).hexdigest()

    is_valid, unpacked_bytes, notes = custody_preserver.verify_and_unpack(envelope)

    assert is_valid is True
    assert unpacked_bytes == sample_raw_image_bytes
    assert any("Custody seal verified" in n for n in notes)


def test_tampered_metadata_detection(
    custody_preserver: EvidentiaryCustodyPreserver,
    sample_metadata: ForensicCaptureMetadata,
    sample_raw_image_bytes: bytes,
):
    envelope = custody_preserver.seal_evidence(
        inspection_id="insp-sec63-002",
        officer_badge="LMO-DL-ND-1002",
        raw_image_bytes=sample_raw_image_bytes,
        metadata=sample_metadata,
    )

    tampered_meta = ForensicCaptureMetadata(
        device_make=sample_metadata.device_make,
        device_model=sample_metadata.device_model,
        sensor_serial_number=sample_metadata.sensor_serial_number,
        capture_timestamp_utc=sample_metadata.capture_timestamp_utc,
        gps_latitude=19.0760,
        gps_longitude=72.8777,
        gps_altitude_meters=sample_metadata.gps_altitude_meters,
        lens_focal_length_mm=sample_metadata.lens_focal_length_mm,
        iso_speed=sample_metadata.iso_speed,
        shutter_speed_seconds=sample_metadata.shutter_speed_seconds,
    )

    tampered_envelope = EvidenceEnvelope(
        envelope_id=envelope.envelope_id,
        inspection_id=envelope.inspection_id,
        raw_image_sha256=envelope.raw_image_sha256,
        sealed_at_utc=envelope.sealed_at_utc,
        custody_officer_badge=envelope.custody_officer_badge,
        metadata=tampered_meta,
        envelope_digest_sha256=envelope.envelope_digest_sha256,
        hmac_seal_signature=envelope.hmac_seal_signature,
        encrypted_payload_b64=envelope.encrypted_payload_b64,
    )

    is_valid, unpacked_bytes, notes = custody_preserver.verify_and_unpack(tampered_envelope)
    assert is_valid is False
    assert unpacked_bytes is None
    assert any("corrupted or modified" in n for n in notes)


def test_forged_hmac_signature_detection(
    custody_preserver: EvidentiaryCustodyPreserver,
    sample_metadata: ForensicCaptureMetadata,
    sample_raw_image_bytes: bytes,
):
    envelope = custody_preserver.seal_evidence(
        inspection_id="insp-sec63-003",
        officer_badge="LMO-KA-BLR-8831",
        raw_image_bytes=sample_raw_image_bytes,
        metadata=sample_metadata,
    )

    forged_sig = envelope.hmac_seal_signature[:-4] + "ffff"
    forged_envelope = EvidenceEnvelope(
        envelope_id=envelope.envelope_id,
        inspection_id=envelope.inspection_id,
        raw_image_sha256=envelope.raw_image_sha256,
        sealed_at_utc=envelope.sealed_at_utc,
        custody_officer_badge=envelope.custody_officer_badge,
        metadata=envelope.metadata,
        envelope_digest_sha256=envelope.envelope_digest_sha256,
        hmac_seal_signature=forged_sig,
        encrypted_payload_b64=envelope.encrypted_payload_b64,
    )

    is_valid, unpacked_bytes, notes = custody_preserver.verify_and_unpack(forged_envelope)
    assert is_valid is False
    assert unpacked_bytes is None
    assert any("signature invalid" in n for n in notes)


def test_wrong_vault_key_rejection(
    sample_metadata: ForensicCaptureMetadata,
    sample_raw_image_bytes: bytes,
    tmp_path: Path,
):
    preserver_author = EvidentiaryCustodyPreserver(
        vault_master_key=b"AUTHORIZED_AUTHOR_KEY_2026",
        vault_storage_dir=tmp_path / "v1",
    )
    preserver_intruder = EvidentiaryCustodyPreserver(
        vault_master_key=b"UNAUTHORIZED_INTRUDER_KEY_9999",
        vault_storage_dir=tmp_path / "v2",
    )

    envelope = preserver_author.seal_evidence(
        inspection_id="insp-sec63-004",
        officer_badge="LMO-TN-CHN-0042",
        raw_image_bytes=sample_raw_image_bytes,
        metadata=sample_metadata,
    )

    is_valid, unpacked_bytes, notes = preserver_intruder.verify_and_unpack(envelope)
    assert is_valid is False
    assert unpacked_bytes is None
    assert any("signature invalid" in n for n in notes)


def test_vault_storage_file_persistence(
    custody_preserver: EvidentiaryCustodyPreserver,
    sample_metadata: ForensicCaptureMetadata,
    sample_raw_image_bytes: bytes,
):
    envelope = custody_preserver.seal_evidence(
        inspection_id="insp-sec63-005",
        officer_badge="LMO-GJ-AHM-1984",
        raw_image_bytes=sample_raw_image_bytes,
        metadata=sample_metadata,
    )

    vault_file = custody_preserver.storage_dir / f"{envelope.envelope_id}.json"
    assert vault_file.exists()

    data = json.loads(vault_file.read_text(encoding="utf-8"))
    assert data["envelope_id"] == envelope.envelope_id
    assert data["inspection_id"] == "insp-sec63-005"
    assert data["custody_officer_badge"] == "LMO-GJ-AHM-1984"
    assert data["metadata"]["device_make"] == "Samsung"


def test_forensic_metadata_serialization_with_nones():
    meta = ForensicCaptureMetadata(
        device_make="Generic Camera",
        device_model="FieldCam v1",
        sensor_serial_number=None,
        capture_timestamp_utc="2026-09-05T12:00:00Z",
        gps_latitude=None,
        gps_longitude=None,
        gps_altitude_meters=None,
        lens_focal_length_mm=None,
        iso_speed=None,
        shutter_speed_seconds=None,
    )

    d = meta.to_dict()
    assert d["device_make"] == "Generic Camera"
    assert d["sensor_serial_number"] is None
    assert d["gps_latitude"] is None
