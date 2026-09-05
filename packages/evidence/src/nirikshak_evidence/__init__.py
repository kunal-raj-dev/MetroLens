"""
Nirikshak Evidence: Forensic cryptographic DAG evidence node creation and chain-of-custody tracking.
"""

import hashlib
from typing import Optional
from nirikshak_shared.models.primitives import (
    BoundingBox,
    CalibrationStatus,
    PanelName,
    ObservedValue,
)
from nirikshak_shared.models.contracts import EvidenceItem


def compute_sha256(data: bytes) -> str:
    """Computes standard hexadecimal SHA-256 digest of raw byte stream."""
    return hashlib.sha256(data).hexdigest()


def create_evidence_item(
    evidence_id: str,
    image_sha256: str,
    bounding_box: BoundingBox,
    calibration_status: CalibrationStatus,
    observed_value: ObservedValue,
    panel_name: PanelName = PanelName.PRINCIPAL_DISPLAY_PANEL,
    physical_scale_mm_per_pixel: Optional[float] = None,
) -> EvidenceItem:
    """Creates a strictly validated evidence node conforming to rules/schema/evidence.schema.json."""
    return EvidenceItem(
        evidence_id=evidence_id,
        image_sha256=image_sha256,
        panel_name=panel_name,
        bounding_box=bounding_box,
        calibration_status=calibration_status,
        physical_scale_mm_per_pixel=physical_scale_mm_per_pixel,
        observed_value=observed_value,
    )


__all__ = ["compute_sha256", "create_evidence_item", "EvidenceItem"]
