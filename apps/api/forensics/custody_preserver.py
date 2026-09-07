"""
Evidentiary Custody Preserver & Judicial Vault Engine
====================================================
Packages raw photographic evidence, forensic device telemetry, and hardware
sensor metadata into an encrypted, tamper-evident Evidence Envelope conforming
to Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (BSA).

Purpose:
    While web uploads strip EXIF/GPS for user privacy, judicial raids require
    preserving cryptographic proof of capture location, timestamp, and camera
    hardware identity within a secure air-gapped vault.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ForensicCaptureMetadata:
    """Hardware and geographic capture parameters."""

    device_make: str
    device_model: str
    sensor_serial_number: Optional[str]
    capture_timestamp_utc: str
    gps_latitude: Optional[float]
    gps_longitude: Optional[float]
    gps_altitude_meters: Optional[float]
    lens_focal_length_mm: Optional[float]
    iso_speed: Optional[int]
    shutter_speed_seconds: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_make": self.device_make,
            "device_model": self.device_model,
            "sensor_serial_number": self.sensor_serial_number,
            "capture_timestamp_utc": self.capture_timestamp_utc,
            "gps_latitude": self.gps_latitude,
            "gps_longitude": self.gps_longitude,
            "gps_altitude_meters": self.gps_altitude_meters,
            "lens_focal_length_mm": self.lens_focal_length_mm,
            "iso_speed": self.iso_speed,
            "shutter_speed_seconds": self.shutter_speed_seconds,
        }


@dataclass(frozen=True)
class EvidenceEnvelope:
    """Cryptographically sealed evidence container for court tendering."""

    envelope_id: str
    inspection_id: str
    raw_image_sha256: str
    sealed_at_utc: str
    custody_officer_badge: str
    metadata: ForensicCaptureMetadata
    envelope_digest_sha256: str
    hmac_seal_signature: str
    encrypted_payload_b64: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "inspection_id": self.inspection_id,
            "raw_image_sha256": self.raw_image_sha256,
            "sealed_at_utc": self.sealed_at_utc,
            "custody_officer_badge": self.custody_officer_badge,
            "metadata": self.metadata.to_dict(),
            "envelope_digest_sha256": self.envelope_digest_sha256,
            "hmac_seal_signature": self.hmac_seal_signature,
        }


class EvidentiaryCustodyPreserver:
    """
    Manages cryptographic sealing and verification of court evidence envelopes.
    """

    def __init__(
        self,
        vault_master_key: Optional[bytes] = None,
        vault_storage_dir: Optional[Path] = None,
    ) -> None:
        self.master_key = vault_master_key or os.environ.get(
            "METROLENS_VAULT_KEY", "METROLENS_COURT_VAULT_KEY_2026"
        ).encode("utf-8")
        self.storage_dir = vault_storage_dir or Path(
            os.environ.get("TEMP", "/tmp")
        ) / "metrolens_custody_vault"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def seal_evidence(
        self,
        inspection_id: str,
        officer_badge: str,
        raw_image_bytes: bytes,
        metadata: ForensicCaptureMetadata,
    ) -> EvidenceEnvelope:
        """
        Create a tamper-evident evidence envelope sealing image and telemetry.
        """
        raw_sha256 = hashlib.sha256(raw_image_bytes).hexdigest()
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        env_id = f"ENV-{inspection_id[:8].upper()}-{os.urandom(4).hex().upper()}"

        # Lightweight stream obfuscation / XOR cipher with derived key for vault storage
        salt = os.urandom(16)
        derived_key = hashlib.pbkdf2_hmac("sha256", self.master_key, salt, 10000)
        encrypted_bytes = self._xor_stream_cipher(raw_image_bytes, derived_key)
        payload_b64 = base64.b64encode(salt + encrypted_bytes).decode("ascii")

        # Canonical envelope digest
        meta_json = json.dumps(metadata.to_dict(), sort_keys=True)
        digest_base = f"{env_id}:{inspection_id}:{raw_sha256}:{now_utc}:{officer_badge}:{meta_json}".encode("utf-8")
        envelope_digest = hashlib.sha256(digest_base).hexdigest()

        # Sign with HMAC
        sig = hmac.new(self.master_key, envelope_digest.encode("ascii"), hashlib.sha256).hexdigest()

        envelope = EvidenceEnvelope(
            envelope_id=env_id,
            inspection_id=inspection_id,
            raw_image_sha256=raw_sha256,
            sealed_at_utc=now_utc,
            custody_officer_badge=officer_badge,
            metadata=metadata,
            envelope_digest_sha256=envelope_digest,
            hmac_seal_signature=sig,
            encrypted_payload_b64=payload_b64,
        )

        # Persist to disk vault
        self._write_envelope_to_vault(envelope)
        return envelope

    def verify_and_unpack(
        self, envelope: EvidenceEnvelope
    ) -> Tuple[bool, Optional[bytes], List[str]]:
        """
        Verify cryptographic seal and unpack raw bytes.

        Returns:
            Tuple of (is_verified, Optional[raw_image_bytes], verification_notes)
        """
        notes: List[str] = []

        # 1. Recompute envelope digest
        meta_json = json.dumps(envelope.metadata.to_dict(), sort_keys=True)
        digest_base = (
            f"{envelope.envelope_id}:{envelope.inspection_id}:{envelope.raw_image_sha256}:"
            f"{envelope.sealed_at_utc}:{envelope.custody_officer_badge}:{meta_json}"
        ).encode("utf-8")
        expected_digest = hashlib.sha256(digest_base).hexdigest()

        if expected_digest != envelope.envelope_digest_sha256:
            notes.append("Envelope metadata corrupted or modified after sealing.")
            return False, None, notes

        # 2. Verify HMAC signature
        expected_sig = hmac.new(
            self.master_key, expected_digest.encode("ascii"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, envelope.hmac_seal_signature):
            notes.append("HMAC cryptographic seal signature invalid (vault key mismatch or forged seal).")
            return False, None, notes

        # 3. Decrypt payload
        try:
            full_cipher = base64.b64decode(envelope.encrypted_payload_b64)
            salt = full_cipher[:16]
            encrypted_data = full_cipher[16:]
            derived_key = hashlib.pbkdf2_hmac("sha256", self.master_key, salt, 10000)
            raw_bytes = self._xor_stream_cipher(encrypted_data, derived_key)
        except Exception as exc:
            notes.append(f"Payload decryption failed: {str(exc)}")
            return False, None, notes

        # 4. Verify raw image SHA-256
        actual_sha = hashlib.sha256(raw_bytes).hexdigest()
        if actual_sha != envelope.raw_image_sha256:
            notes.append(f"Decrypted payload SHA-256 ({actual_sha}) mismatch with sealed hash ({envelope.raw_image_sha256}).")
            return False, None, notes

        notes.append("Custody seal verified: zero unauthorized tampering detected across image and telemetry.")
        return True, raw_bytes, notes

    def _xor_stream_cipher(self, data: bytes, key: bytes) -> bytes:
        """Symmetric key stream cipher."""
        out = bytearray(len(data))
        k_len = len(key)
        for i in range(len(data)):
            out[i] = data[i] ^ key[i % k_len]
        return bytes(out)

    def _write_envelope_to_vault(self, env: EvidenceEnvelope) -> None:
        target = self.storage_dir / f"{env.envelope_id}.json"
        target.write_text(json.dumps(env.to_dict(), indent=2), encoding="utf-8")
