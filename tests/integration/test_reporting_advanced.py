"""
Integration Tests for Advanced Reporting & Evidentiary Certification
====================================================================
Tests Section 63 BSA 2023 Legal Affidavit, Bilingual Typography,
Multi-Page Inspection Dossier, Digital Signature / RFC 3161 timestamps,
and multi-format e-Governance exports.
"""

import hashlib
import io
import json
import xml.etree.ElementTree as ET
from PIL import Image

import pytest
from packages.reporting.src.nirikshak_reporting.legal_affidavit import (
    LegalAffidavitCompiler,
    CertifyingOfficerInfo,
    ElectronicRecordEvidenceDetails,
)
from packages.reporting.src.nirikshak_reporting.bilingual_typography import (
    BilingualTypographyEngine,
    BilingualTerm,
)
from packages.reporting.src.nirikshak_reporting.multi_page_dossier import (
    MultiPageDossierCompiler,
    MultiPageDossierPayload,
    DossierEvidenceExhibit,
)
from packages.reporting.src.nirikshak_reporting.digital_signature import (
    DigitalSignatureManager,
    DigitalSignatureSeal,
)
from packages.reporting.src.nirikshak_reporting.export_formats import (
    ComplianceDossierExporter,
)


def _create_sample_jpeg_bytes() -> bytes:
    img = Image.new("RGB", (300, 200), color=(245, 245, 245))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Section 63 BSA 2023 Legal Affidavit Tests
# ---------------------------------------------------------------------------

def test_legal_affidavit_compilation():
    """Verify court-admissible Section 63 BSA 2023 Electronic Evidence Certificate generation."""
    compiler = LegalAffidavitCompiler(system_version="1.0.0-SIH26034")
    raw_img = _create_sample_jpeg_bytes()
    raw_hash = hashlib.sha256(raw_img).hexdigest()

    evidence = ElectronicRecordEvidenceDetails(
        inspection_id="INS-2026-TEST-001",
        timestamp_utc="2026-09-05T10:00:00Z",
        timestamp_ist="05-Sep-2026 15:30:00 IST",
        raw_image_sha256=raw_hash,
        raw_image_filename="biscuit_packet.jpg",
        raw_image_size_bytes=len(raw_img),
        derived_pdf_sha256=hashlib.sha256(b"SAMPLE_PDF").hexdigest(),
        ocr_observations_count=12,
        statutory_violations_detected=1,
        overall_verdict="NON_COMPLIANT",
    )

    officer = CertifyingOfficerInfo(
        officer_name="Shri Rajesh Kumar Sharma",
        badge_number="DL-LM-7842",
        designation="Senior Legal Metrology Inspector",
        district="South Delhi",
        state="Delhi",
    )

    pdf_bytes = compiler.generate_affidavit_pdf(evidence, officer)
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-")
    assert b"%%EOF" in pdf_bytes
    assert len(pdf_bytes) > 2000


# ---------------------------------------------------------------------------
# 2. Bilingual Typography Engine Tests
# ---------------------------------------------------------------------------

def test_bilingual_vocabulary_and_sanitization():
    """Verify dictionary lookups, Devanagari headings, and character sanitization."""
    mrp_term = BilingualTypographyEngine.get_term("mrp")
    assert mrp_term is not None
    assert "Maximum Retail Price" in mrp_term.english
    assert "अधिकतम खुदरा मूल्य" in mrp_term.hindi_devanagari
    assert mrp_term.statutory_rule_citation == "Rule 6(1)(e)"

    heading = mrp_term.format_heading(use_transliteration=True)
    assert "Maximum Retail Price" in heading
    assert "Adhiktam Khudrā Mūlya" in heading

    # Test currency and XML escaping
    dirty_text = "Special Offer: Price is ₹ 199.00 & Free Gift <Limited>!"
    cleaned = BilingualTypographyEngine.sanitize_for_pdf(dirty_text)
    assert "₹" not in cleaned
    assert "Rs." in cleaned
    assert "&amp;" in cleaned
    assert "&lt;" in cleaned
    assert "&gt;" in cleaned


# ---------------------------------------------------------------------------
# 3. Multi-Page Dossier Compiler Tests
# ---------------------------------------------------------------------------

def test_multi_page_dossier_compilation():
    """Verify generation of formal 4-page statutory inspection dossier."""
    compiler = MultiPageDossierCompiler()
    raw_img = _create_sample_jpeg_bytes()

    declarations = [
        BilingualTypographyEngine.create_statutory_declaration_row(
            "mrp", "Rs. 45.00 (incl. of all taxes)", True
        ),
        BilingualTypographyEngine.create_statutory_declaration_row(
            "net_quantity", "200 gm", False, "Rule 26: Prohibited non-standard unit 'gm' (must use 'g')"
        ),
        BilingualTypographyEngine.create_statutory_declaration_row(
            "manufacturer", "M/s Britannia Industries Ltd, Kolkata", True
        ),
    ]

    exhibit = DossierEvidenceExhibit(
        title="Net Quantity Defect Panel",
        image_bytes=raw_img,
        declaration_type="Net Quantity",
        ocr_text="Net Qty: 200 gm",
        font_height_mm=1.8,
        required_min_height_mm=2.0,
        is_compliant=False,
        defect_reason="Height below 2.0mm minimum threshold and non-standard unit 'gm'",
    )

    payload = MultiPageDossierPayload(
        inspection_id="INS-MULTI-001",
        timestamp_ist="05-Sep-2026 15:30:00 IST",
        inspector_name="Inspector Amit Verma",
        badge_number="MH-LM-301",
        district="Mumbai Suburban",
        state="Maharashtra",
        overall_verdict="NON_COMPLIANT",
        raw_image_bytes=raw_img,
        raw_image_sha256=hashlib.sha256(raw_img).hexdigest(),
        commodity_category="Packaged Food (Biscuits)",
        pdp_area_sqcm=220.0,
        metric_scale_mm_per_px=0.125,
        declarations_table=declarations,
        evidence_exhibits=[exhibit],
        improvement_notice_details={
            "cure_period_days": 15,
            "notice_reference": "IN/LM/MUM/001",
            "compliance_deadline": "20-Sep-2026",
        },
    )

    pdf_bytes = compiler.compile(payload)
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-")
    assert b"%%EOF" in pdf_bytes
    # Must contain multiple pages
    assert pdf_bytes.count(b"/Page\n") >= 4 or pdf_bytes.count(b"/Type /Page") >= 4


# ---------------------------------------------------------------------------
# 4. Digital Signature & RFC 3161 Timestamp Tests
# ---------------------------------------------------------------------------

def test_digital_signature_sealing_and_verification():
    """Verify cryptographic sealing, RFC 3161 timestamping, and tamper detection."""
    manager = DigitalSignatureManager()
    doc_bytes = b"STATUTORY_INSPECTION_RECORD_DATA_BYTES_PAYLOAD"

    seal = manager.seal_document(doc_bytes, signer_name="Inspector S. K. Gupta")
    assert seal.is_valid is True
    assert seal.document_sha256 == hashlib.sha256(doc_bytes).hexdigest()
    assert seal.timestamp_token.message_imprint_algorithm == "SHA-256"

    # Verify untampered document
    is_valid, notes = manager.verify_seal(doc_bytes, seal)
    assert is_valid is True
    assert any("100% authentic" in n.lower() for n in notes)

    # Verify tamper detection on modified document
    tampered_bytes = doc_bytes + b"_ALTERED"
    is_tampered_valid, tamper_notes = manager.verify_seal(tampered_bytes, seal)
    assert is_tampered_valid is False
    assert any("document hash mismatch" in n.lower() for n in tamper_notes)


# ---------------------------------------------------------------------------
# 5. Multi-Format Exporter Tests (JSON-LD, NIC XML, CSV)
# ---------------------------------------------------------------------------

def test_compliance_dossier_exporters():
    """Verify JSON-LD, XML, and CSV generation."""
    sample_data = {
        "inspection_id": "INS-EXPORT-01",
        "timestamp_ist": "05-Sep-2026 15:30:00 IST",
        "overall_verdict": "NON_COMPLIANT",
        "raw_image_sha256": "abc123def456",
        "inspector_name": "Inspector Sharma",
        "badge_number": "DL-01",
        "district": "New Delhi",
        "state": "Delhi",
        "declarations_table": [
            {
                "term_key": "mrp",
                "citation": "Rule 6(1)(e)",
                "declared_value": "Rs. 99.00",
                "is_compliant": True,
            },
            {
                "term_key": "net_quantity",
                "citation": "Rule 6(1)(c)",
                "declared_value": "500 gm",
                "is_compliant": False,
                "specific_defect": "Non-standard unit 'gm'",
            },
        ],
        "improvement_notice_details": {
            "cure_period_days": 15,
            "notice_reference": "IN/001",
            "compliance_deadline": "20-Sep-2026",
        },
    }

    # 1. JSON-LD
    json_ld_str = ComplianceDossierExporter.to_json_ld(sample_data)
    parsed_json = json.loads(json_ld_str)
    assert parsed_json["@type"] == "metrology:LegalMetrologyAssessmentReport"
    assert parsed_json["inspectionId"] == "INS-EXPORT-01"

    # 2. NIC XML
    xml_str = ComplianceDossierExporter.to_nic_xml(sample_data)
    xml_root = ET.fromstring(xml_str)
    assert "MetroLensInspectionDocket" in xml_root.tag
    assert "INS-EXPORT-01" in xml_str

    # 3. CSV
    csv_row = ComplianceDossierExporter.to_csv_ledger_row(sample_data)
    assert "INS-EXPORT-01" in csv_row
    assert "NON_COMPLIANT" in csv_row
