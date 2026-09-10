"""Render a multipage, unsigned draft from supplied packaging observations.

The document displays observations and images for human review. It does not
authenticate evidence, determine penalties, or issue statutory notices."""

from __future__ import annotations

import datetime
import io
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image as PILImage
from .text_safety import DRAFT_NOTICE, join_markup, markup, text

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .bilingual_typography import BilingualTypographyEngine
from .pdf_compiler import NumberedCanvas


@dataclass
class DossierEvidenceExhibit:
    """Represents a visual evidence crop exhibit."""

    title: str
    image_bytes: bytes
    declaration_type: str
    ocr_text: str
    font_height_mm: Optional[float]
    required_min_height_mm: Optional[float]
    is_compliant: bool
    defect_reason: Optional[str] = None


@dataclass
class MultiPageDossierPayload:
    """Complete data payload for multi-page inspection dossier generation."""

    inspection_id: str
    timestamp_ist: str
    inspector_name: str
    badge_number: str
    district: str
    state: str
    overall_verdict: str  # 'COMPLIANT', 'NON_COMPLIANT'
    raw_image_bytes: bytes
    raw_image_sha256: str
    commodity_category: str
    pdp_area_sqcm: Optional[float]
    metric_scale_mm_per_px: Optional[float]
    declarations_table: List[Dict[str, Any]]
    evidence_exhibits: List[DossierEvidenceExhibit]
    improvement_notice_details: Optional[Dict[str, Any]] = None
    forensic_ela_bytes: Optional[bytes] = None
    forensic_tamper_verdict: str = "NOT_ASSESSED"


class MultiPageDossierCompiler:
    """
    Compiles formal 4-page statutory inspection dossiers.
    """

    PAGE_WIDTH, PAGE_HEIGHT = A4

    def compile(self, payload: MultiPageDossierPayload) -> bytes:
        """
        Compile complete multi-page PDF dossier.

        Args:
            payload: MultiPageDossierPayload with all findings and exhibits.

        Returns:
            PDF bytes.
        """
        pdf_buf = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buf,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            pageCompression=0,
        )

        styles = getSampleStyleSheet()

        # Custom Typography Styles
        title_style = ParagraphStyle(
            "DossierTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            alignment=1,
            textColor=colors.HexColor("#0B2545"),
        )
        subtitle_style = ParagraphStyle(
            "DossierSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=1,
            textColor=colors.HexColor("#134074"),
        )
        h2_style = ParagraphStyle(
            "DossierH2",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#0B2545"),
        )
        body_style = ParagraphStyle(
            "DossierBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1A1A1A"),
        )
        body_bold = ParagraphStyle(
            "DossierBodyBold",
            parent=body_style,
            fontName="Helvetica-Bold",
        )
        cell_style = ParagraphStyle(
            "DossierCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=colors.HexColor("#222222"),
        )
        cell_bold = ParagraphStyle(
            "DossierCellBold",
            parent=cell_style,
            fontName="Helvetica-Bold",
        )

        story: List[Any] = [Paragraph(text(DRAFT_NOTICE), body_style), Spacer(1, 8)]

        # ===================================================================
        # PAGE 1: EXECUTIVE SUMMARY & PACKAGING EXHIBIT
        # ===================================================================
        story.append(Paragraph("METROLENS ASSISTIVE DRAFT", title_style))
        story.append(
            Paragraph(
                "Preliminary packaging assessment prepared by MetroLens",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(
            Paragraph("ASSISTIVE DRAFT INSPECTION ASSESSMENT DOSSIER", h2_style)
        )
        story.append(Spacer(1, 1 * mm))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 3 * mm))

        # Metadata Header Table
        meta_data = [
            [
                Paragraph(text(markup('<b>Docket UUID:</b> <code>{0}</code>', payload.inspection_id)), cell_style),
                Paragraph(text(markup('<b>Inspection Date/Time:</b> {0}', payload.timestamp_ist)), cell_style),
            ],
            [
                Paragraph(
                    text(markup('<b>Officer:</b> {0} (Badge: {1})', payload.inspector_name, payload.badge_number)),
                    cell_style,
                ),
                Paragraph(text(markup('<b>Jurisdiction:</b> {0}, {1}', payload.district, payload.state)), cell_style),
            ],
            [
                Paragraph(text(markup('<b>Commodity Type:</b> {0}', payload.commodity_category)), cell_style),
                Paragraph(
                    text(markup('<b>Raw Image SHA-256:</b> <code>{0}...</code>', payload.raw_image_sha256[:20])),
                    cell_style,
                ),
            ],
        ]
        t_meta = Table(meta_data, colWidths=[90 * mm, 90 * mm])
        t_meta.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(t_meta)
        story.append(Spacer(1, 4 * mm))

        # Overall Verdict Banner
        is_pass = payload.overall_verdict.upper() == "COMPLIANT"
        banner_bg = colors.HexColor("#D4EDDA") if is_pass else colors.HexColor("#F8D7DA")
        banner_fg = colors.HexColor("#155724") if is_pass else colors.HexColor("#721C24")
        verdict_text = (
            "IMAGE-BASED ASSESSMENT: ALL MANDATORY DECLARATIONS CONFORMANT"
            if is_pass
            else "IMAGE-BASED ASSESSMENT: NON-COMPLIANCE DETECTED - IMPROVEMENT NOTICE REQUIRED"
        )
        v_style = ParagraphStyle(
            "VerdictStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            alignment=1,
            textColor=banner_fg,
        )
        t_verdict = Table([[Paragraph(text(verdict_text), v_style)]], colWidths=[180 * mm])
        t_verdict.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), banner_bg),
                    ("BOX", (0, 0), (-1, -1), 1.0, banner_fg),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(t_verdict)
        story.append(Spacer(1, 4 * mm))

        # Packaging Image Display (Scaled)
        try:
            pil_img = PILImage.open(io.BytesIO(payload.raw_image_bytes))
            w, h = pil_img.size
            max_w, max_h = 160 * mm, 110 * mm
            ratio = min(max_w / w, max_h / h)
            disp_w, disp_h = w * ratio, h * ratio

            raw_buf = io.BytesIO(payload.raw_image_bytes)
            rl_img = Image(raw_buf, width=disp_w, height=disp_h)
            story.append(rl_img)
            story.append(Spacer(1, 1 * mm))
            caption = (
                markup('<i>Exhibit 1.0: Primary Photograph of Packaging Exhibit (Scale: {0:.1f}mm x {1:.1f}mm). Principal Display Panel Area: {2} sq cm.</i>', disp_w / mm, disp_h / mm, payload.pdp_area_sqcm or 'N/A')
            )
            story.append(Paragraph(text(caption), cell_style))
        except Exception:
            story.append(Paragraph("<i>[Image display unavailable]</i>", cell_style))

        story.append(Spacer(1, 4 * mm))
        # Statutory Summary Note
        p1_note = (
            markup('<b>Assessment scope:</b> This assistive draft summarizes supplied observations. It does not establish legal non-compliance, certify custody, or issue a notice.')
        )
        story.append(Paragraph(text(p1_note), body_style))

        # ===================================================================
        # PAGE 2: STATUTORY COMPLIANCE MATRIX & FONT AUDIT
        # ===================================================================
        story.append(PageBreak())
        story.append(Paragraph("PAGE 2: STATUTORY DECLARATION AUDIT MATRIX", h2_style))
        story.append(
            Paragraph(
                "Legal Metrology (Packaged Commodities) Rules, 2011 & GSR 881(E) Amendments",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 3 * mm))

        # Compliance Matrix Table
        matrix_headers = [
            Paragraph("<b>Rule / Citation</b>", cell_bold),
            Paragraph("<b>Mandatory Declaration</b>", cell_bold),
            Paragraph("<b>Declared Text on Package</b>", cell_bold),
            Paragraph("<b>Compliance Status</b>", cell_bold),
            Paragraph("<b>Defect / Statutory Finding</b>", cell_bold),
        ]
        matrix_rows = [matrix_headers]

        for item in payload.declarations_table:
            c_flag = item.get("is_compliant", False)
            status_text = (
                markup("<font color='#155724'><b>PASS</b></font>") if c_flag else markup("<font color='#721C24'><b>FAIL</b></font>")
            )
            matrix_rows.append(
                [
                    Paragraph(text(item.get('citation', 'Rule 6')), cell_style),
                    Paragraph(text(item.get('bilingual_label', item.get('term_key', ''))), cell_style),
                    Paragraph(
                        text(BilingualTypographyEngine.sanitize_for_pdf(item.get('declared_value', 'NOT DETECTED'))),
                        cell_style,
                    ),
                    Paragraph(text(status_text), cell_style),
                    Paragraph(text(item.get('specific_defect') or 'No explanation supplied; review required'), cell_style),
                ]
            )

        t_matrix = Table(
            matrix_rows, colWidths=[25 * mm, 45 * mm, 40 * mm, 20 * mm, 50 * mm]
        )
        t_matrix.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF4F8")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(t_matrix)
        story.append(Spacer(1, 5 * mm))

        # Numeral Font Height & PDP Audit Section
        story.append(Paragraph("Principal Display Panel (PDP) & Numeral Font Height Audit", h2_style))
        story.append(Spacer(1, 2 * mm))
        pdp_txt = (
            markup("• <b>Calculated PDP Area:</b> {0} cm²<br/>• <b>Optical Calibration Factor:</b> {1} mm/pixel<br/>• <b>Statutory Standard:</b> Under Table I of Rule 7(1), packages with PDP area between 100 cm² and 500 cm² require a minimum numeral height of <b>2.0 mm</b> (or <b>4.0 mm</b> if embossed/blown). Packages exceeding 500 cm² require a minimum numeral height of <b>4.0 mm</b>.<br/>• <b>GSR 881(E) Unit Sale Price (USP) Requirement:</b> All packaged commodities exceeding 1 kg/1 L must display USP in terms of 'per kg' or 'per L'. Packages under 1 kg/1 L must display USP in 'per g' or 'per ml'.", payload.pdp_area_sqcm or 'Indeterminate', payload.metric_scale_mm_per_px or 'Uncalibrated')
        )
        story.append(Paragraph(text(pdp_txt), body_style))

        # ===================================================================
        # PAGE 3: FORENSIC EVIDENCE EXHIBITS & CROPS
        # ===================================================================
        story.append(PageBreak())
        story.append(Paragraph("PAGE 3: VISUAL FORENSIC EVIDENCE EXHIBITS", h2_style))
        story.append(
            Paragraph(
                "Supplied image crops and observations; authenticity not certified",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 3 * mm))

        if payload.evidence_exhibits:
            for idx, ex in enumerate(payload.evidence_exhibits[:3], start=1):
                try:
                    ex_buf = io.BytesIO(ex.image_bytes)
                    ex_img = Image(ex_buf, width=60 * mm, height=35 * mm)
                except Exception:
                    ex_img = Paragraph("<i>[Exhibit image error]</i>", cell_style)

                ex_details = (
                    markup('<b>Exhibit 3.{0}: {1}</b><br/><b>Declaration Category:</b> {2}<br/><b>Extracted Text:</b> <code>{3}</code><br/><b>Measured Font Height:</b> {4} mm (Min Required: {5} mm)<br/><b>Defect Assessment:</b> {6}', idx, ex.title, ex.declaration_type, BilingualTypographyEngine.sanitize_for_pdf(ex.ocr_text), ex.font_height_mm or 'N/A', ex.required_min_height_mm or 'N/A', ex.defect_reason or 'None')
                )
                t_ex = Table([[ex_img, Paragraph(text(ex_details), cell_style)]], colWidths=[65 * mm, 115 * mm])
                t_ex.setStyle(
                    TableStyle(
                        [
                            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAFAFA")),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ]
                    )
                )
                story.append(t_ex)
                story.append(Spacer(1, 3 * mm))
        else:
            story.append(
                Paragraph(
                    "<i>No visual defect exhibits required; packaging conforms to statutory specifications.</i>",
                    body_style,
                )
            )

        # Forensic ELA & Tamper Authentication Section
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("Digital Media Authentication & Forensic Tamper Gate", h2_style))
        story.append(Spacer(1, 1 * mm))
        ela_summary = (
            markup('<b>Reported forensic assessment:</b> {0}<br/>This compiler does not independently verify capture authenticity, ingestion controls, or metadata sanitization.', payload.forensic_tamper_verdict)
        )
        story.append(Paragraph(text(ela_summary), body_style))

        # ===================================================================
        # PAGE 4: SECTION 36(1) JAN VISHWAS NOTICE & COMPOUNDING LADDER
        # ===================================================================
        story.append(PageBreak())
        story.append(
            Paragraph("PAGE 4: PROPOSED FOLLOW-UP FOR HUMAN REVIEW", h2_style)
        )
        story.append(
            Paragraph(
                "Under Section 36(1) and Section 48 of the Legal Metrology Act, 2009",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 3 * mm))

        if not is_pass:
            # Section 36(1) Formal Improvement Notice Box

            notice_p = (
                markup('<b>DRAFT IMPROVEMENT NOTICE — NOT ISSUED</b><br/>Inspection reference: {0}<br/>An authorized officer must verify the evidence and applicable law, determine any cure period, and approve and serve any notice. This document creates no deadline, penalty, or automatic escalation.', payload.inspection_id)
            )
            t_notice = Table([[Paragraph(text(notice_p), cell_style)]], colWidths=[180 * mm])
            t_notice.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E7")),
                        ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor("#D97706")),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            story.append(t_notice)
            story.append(Spacer(1, 4 * mm))

        story.append(Paragraph("Further Action Requires Authorized Review", h2_style))
        story.append(Paragraph(
            "This draft does not determine penalties, compounding eligibility, or statutory deadlines. "
            "An authorized reviewer must verify the evidence, jurisdiction, prior history and current "
            "applicable law before preparing or serving any notice.", body_style))
        story.append(Spacer(1, 6 * mm))

        # Final Sign-Off Block
        sign_block = [
            [
                Paragraph(
                    text(markup('<b>Supplied operator (unverified):</b> {0}<br/><b>Badge Number:</b> {1}<br/><b>Office:</b> Directorate of Legal Metrology, {2}, {3}', payload.inspector_name, payload.badge_number, payload.district, payload.state)),
                    cell_style,
                ),
                Paragraph(
                    "<b>SIGNATURE & OFFICIAL SEAL:</b><br/><br/>"
                    "_______________________________________<br/>"
                    "Authorized Inspector of Legal Metrology",
                    cell_style,
                ),
            ]
        ]
        t_sign = Table(sign_block, colWidths=[90 * mm, 90 * mm])
        t_sign.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(KeepTogether(t_sign))

        doc.build(story, canvasmaker=NumberedCanvas)
        return pdf_buf.getvalue()
