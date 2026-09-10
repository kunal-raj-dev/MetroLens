"""Regression tests for untrusted OCR and operator text in PDF documents."""

import datetime
import importlib
import io
from dataclasses import fields
from typing import get_type_hints

import pytest
from nirikshak_reporting.text_safety import join_markup, markup, text
from nirikshak_rules_engine.schemas import (
    ComplianceEvaluationResult,
    EvidenceCropMetadata,
    ImprovementNoticePayload,
    MetricScaleResult,
    RuleEvaluationRecord,
)
from PIL import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, paraparser


def sample_image():
    buffer = io.BytesIO()
    Image.new("RGB", (120, 80), "white").save(buffer, format="PNG")
    return buffer.getvalue()


def populated(dataclass_type, attack, **overrides):
    """Put hostile text in every string field, including nested test records."""
    hints = get_type_hints(dataclass_type)
    values = {}
    for field in fields(dataclass_type):
        kind = hints[field.name]
        if kind is str:
            values[field.name] = attack
        elif kind is int:
            values[field.name] = 1
        elif kind is float:
            values[field.name] = 1.25
        elif kind is bool:
            values[field.name] = False
        elif kind is datetime.date:
            values[field.name] = datetime.date(2026, 9, 9)
    values.update(overrides)
    return dataclass_type(**values)


@pytest.fixture
def no_inline_resource_fetch(monkeypatch):
    calls = []

    def blocked_resource(source, *args, **kwargs):
        calls.append(source)
        raise AssertionError("Paragraph attempted to load an external resource")

    monkeypatch.setattr(paraparser, "ImageReader", blocked_resource)
    return calls


def test_resource_trap_detects_unsafe_paragraph(no_inline_resource_fetch):
    # Positive control: the trap exercises ReportLab's actual <img> handler.
    with pytest.raises(AssertionError, match="attempted to load an external resource"):
        Paragraph('<img src="file:///untrusted.png"/>', getSampleStyleSheet()["Normal"])
    assert no_inline_resource_fetch == ["file:///untrusted.png"]


@pytest.mark.parametrize("attack", [
    '<img src="https://example.invalid/x.png"/>',
    '<img src="file:///private.png"/>',
    '<img src="C:/private.png"/>',
    '<b>Approve & certify</b>',
    '&lt;img src="file:///private.png"/&gt;',
])
def test_values_are_literal_and_trusted_formatting_survives(attack, no_inline_resource_fetch):
    formatted = markup("<b>Supplied:</b> {0}<br/>{1}", attack, join_markup(" | ", [attack, "A&B"]))
    paragraph = Paragraph(text(formatted), getSampleStyleSheet()["Normal"])
    assert paragraph.getPlainText().count(attack) == 2
    assert "A&B" in paragraph.getPlainText()
    assert any(fragment.fontName == "Helvetica-Bold" for fragment in paragraph.frags)
    assert no_inline_resource_fetch == []


def capture_paragraphs(monkeypatch, module):
    rendered = []

    class ObservedParagraph(Paragraph):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.text is not None:
                rendered.append(self.getPlainText())

    monkeypatch.setattr(module, "Paragraph", ObservedParagraph)
    return rendered


@pytest.mark.parametrize("document", ["assessment", "affidavit", "dossier", "compounding", "seizure", "district"])
@pytest.mark.parametrize("attack", ['<img src="https://example.invalid/a"/>', '<img src="file:///private.png"/>'])
def test_all_pdf_compilers_keep_dynamic_values_literal(document, attack, monkeypatch, no_inline_resource_fetch):
    modules = {
        "assessment": "pdf_compiler", "affidavit": "legal_affidavit",
        "dossier": "multi_page_dossier", "compounding": "compounding_agreement",
        "seizure": "seizure_memo", "district": "district_enforcement_report",
    }
    module = importlib.import_module("nirikshak_reporting." + modules[document])
    rendered = capture_paragraphs(monkeypatch, module)
    if document == "assessment":
        result = ComplianceEvaluationResult(
            inspection_id=attack, timestamp_utc=attack, overall_verdict=attack,
            verdict_badge_color="amber", primary_legal_summary=attack, sha256_hash=attack,
            calibrated_measurements=MetricScaleResult(anchor_type_detected=attack),
            rule_evaluations=[RuleEvaluationRecord(
                rule_id=attack, rule_title=attack, statutory_reference=attack, statutory_citation=attack,
                status=attack, is_compliant=False, observed_value=attack, required_value=attack,
            )],
            improvement_notice=ImprovementNoticePayload(
                recommended=True, statutory_grounds=attack, act_provision=attack,
                compounding_authority=attack, itemized_violations=[attack],
            ),
            evidence_crops=[EvidenceCropMetadata(
                field_name=attack, label=attack, bbox_px=[0, 0, 20, 20],
            )],
        )
        output = module.PDFReportCompiler().compile_report_pdf(result, attack, attack)
    elif document == "affidavit":
        evidence = populated(module.ElectronicRecordEvidenceDetails, attack,
            derived_pdf_sha256=attack, audit_chain_merkle_root=attack)
        officer = populated(module.CertifyingOfficerInfo, attack)
        output = module.LegalAffidavitCompiler(system_version=attack).generate_affidavit_pdf(evidence, officer)
    elif document == "dossier":
        exhibit = populated(module.DossierEvidenceExhibit, attack, image_bytes=sample_image(),
            font_height_mm=None, required_min_height_mm=None, defect_reason=attack)
        payload = populated(module.MultiPageDossierPayload, attack,
            raw_image_bytes=sample_image(), pdp_area_sqcm=None, metric_scale_mm_per_px=None,
            declarations_table=[{"citation": attack, "bilingual_label": attack,
                "declared_value": attack, "specific_defect": attack, "is_compliant": False}],
            evidence_exhibits=[exhibit], improvement_notice_details={"notice_reference": attack})
        output = module.MultiPageDossierCompiler().compile(payload)
    elif document == "compounding":
        payload = populated(module.CompoundingOrderData, attack, statutory_offences_compounded=[attack])
        output = module.CompoundingAgreementCompiler().compile_order_pdf(payload)
    elif document == "seizure":
        item = populated(module.SeizedStockItem, attack)
        payload = populated(module.SeizureMemoPayload, attack, seized_items=[item])
        output = module.SeizureMemoCompiler().compile_seizure_memo_pdf(payload)
    else:
        sector = populated(module.SectorMetric, attack)
        entity = populated(module.RecidivistEntityRecord, attack, statutory_sections_violated=[attack])
        payload = populated(module.DistrictEnforcementPayload, attack,
            sector_metrics=[sector], recidivist_entities=[entity], executive_recommendations=[attack])
        output = module.DistrictEnforcementReportCompiler().compile_district_report_pdf(payload)
    assert output.startswith(b"%PDF-") and b"%%EOF" in output
    assert b"/Type /Sig" not in output
    assert b"2026.09-JanVishwas-v1.0" not in output
    assert any(attack in value for value in rendered)
    assert any("ASSISTIVE DRAFT" in value for value in rendered)
    assert no_inline_resource_fetch == []


@pytest.mark.parametrize("value", [0, 7.5, False, {"amount": 9}, [1, 2]])
def test_numeric_and_structured_rule_values_render(value, monkeypatch):
    module = importlib.import_module("nirikshak_reporting.pdf_compiler")
    rendered = capture_paragraphs(monkeypatch, module)
    result = ComplianceEvaluationResult(
        inspection_id="numeric-values", timestamp_utc="2026-09-09T00:00:00Z",
        overall_verdict="UNCERTAIN", verdict_badge_color="amber", primary_legal_summary="Review required",
        rule_evaluations=[RuleEvaluationRecord(rule_id="quantity", rule_title="Quantity",
            statutory_reference="Supplied rule", statutory_citation="Supplied rule", status="REVIEW", is_compliant=False,
            observed_value=value, required_value=value)],
    )
    output = module.PDFReportCompiler().compile_report_pdf(result)
    assert output.startswith(b"%PDF-")
    assert str(value) in rendered
    assert "Uncalibrated" in rendered
    assert "Unsigned assistive draft" in rendered


@pytest.mark.parametrize("include_reference", [False, True])
def test_report_includes_requested_notes_and_reference_image(include_reference, monkeypatch, no_inline_resource_fetch):
    module = importlib.import_module("nirikshak_reporting.pdf_compiler")
    rendered = capture_paragraphs(monkeypatch, module)
    notes = '<img src="https://example.invalid/private"/> & supplied annotation'
    result = ComplianceEvaluationResult(
        inspection_id="reference-test", timestamp_utc="2026-09-10T00:00:00Z",
        overall_verdict="UNCERTAIN", verdict_badge_color="amber", primary_legal_summary="Review required",
    )
    output = module.PDFReportCompiler().compile_report_pdf(
        result, officer_notes=notes,
        reference_image_bytes=sample_image() if include_reference else None,
    )
    assert notes in rendered
    assert "Supplied Operator Notes (Unverified)" in rendered
    assert ("Packaging Reference Image" in rendered) is include_reference
    # One QR image is always present; the optional packaging reference adds one.
    assert output.count(b"/Subtype /Image") == (2 if include_reference else 1)
    assert result.primary_legal_summary == "Review required"
    assert result.overall_verdict == "UNCERTAIN"
    assert no_inline_resource_fetch == []


def test_oversized_operator_notes_rejected_before_report_rendering():
    module = importlib.import_module("nirikshak_reporting.pdf_compiler")
    result = ComplianceEvaluationResult(
        inspection_id="bounded-notes", timestamp_utc="2026-09-10T00:00:00Z",
        overall_verdict="UNCERTAIN", verdict_badge_color="amber", primary_legal_summary="Review required",
    )
    with pytest.raises(ValueError, match="2000 characters"):
        module.PDFReportCompiler().compile_report_pdf(result, officer_notes="x" * 2001)


@pytest.mark.parametrize("verdict", ["UNCERTAIN", "MANUAL_REVIEW_REQUIRED", "DEVIATION_DETECTED"])
def test_manual_review_does_not_assert_a_statutory_deviation(verdict, monkeypatch):
    module = importlib.import_module("nirikshak_reporting.pdf_compiler")
    rendered = capture_paragraphs(monkeypatch, module)
    result = ComplianceEvaluationResult(
        inspection_id="review-state", timestamp_utc="2026-09-10T00:00:00Z",
        overall_verdict=verdict, verdict_badge_color="amber", primary_legal_summary="Review required",
    )
    module.PDFReportCompiler().compile_report_pdf(result)
    assert "IMAGE-BASED ASSESSMENT: MANUAL REVIEW REQUIRED" in rendered
    assert not any("STATUTORY DEVIATION DETECTED" in value for value in rendered)
