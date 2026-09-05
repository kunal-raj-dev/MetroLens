"""
Smoke test for nirikshak-reporting.
"""

from nirikshak_reporting import DossierGenerator
from nirikshak_shared.models.contracts import InspectionResult
from nirikshak_shared.models.primitives import InspectionStatus, OverallVerdict, CalibrationStatus


def test_generate_json_and_pdf():
    generator = DossierGenerator()
    dummy_sha = "c" * 64
    res = InspectionResult(
        inspection_id="insp_test_001",
        status=InspectionStatus.SUCCESS,
        image_sha256=dummy_sha,
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.CALIBRATED,
    )

    # Test JSON generation
    data = generator.generate_json_summary(res)
    assert data["inspection_id"] == "insp_test_001"
    assert data["overall_verdict"] == "COMPLIANT"

    # Test PDF bytes generation
    pdf_bytes = generator.generate_pdf_bytes(res)
    assert len(pdf_bytes) > 0
