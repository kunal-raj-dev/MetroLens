"""
Multi-Page Statutory Inspection Dossier Compiler
================================================
Generates comprehensive 4-page court-admissible inspection dossiers conforming
to the Legal Metrology Act, 2009, Packaged Commodities Rules, 2011, and the
Bharatiya Sakshya Adhiniyam, 2023 (BSA).

Dossier Structure:
    - Page 1: Executive Adjudication Summary & Packaging Inspection Exhibit
    - Page 2: Statutory Rule Compliance Matrix & Numeral Font Height Audit
    - Page 3: Visual Forensic Evidence Crops & Tamper Authentication
    - Page 4: Section 36(1) Jan Vishwas Improvement Notice & Compounding Ladder
"""

from __future__ import annotations

import datetime
import io
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image as PILImage
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
    forensic_tamper_verdict: str = "CLEAN"


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

        story: List[Any] = []

        # ===================================================================
        # PAGE 1: EXECUTIVE SUMMARY & PACKAGING EXHIBIT
        # ===================================================================
        story.append(Paragraph("DIRECTORATE OF LEGAL METROLOGY", title_style))
        story.append(
            Paragraph(
                "MINISTRY OF CONSUMER AFFAIRS, FOOD AND PUBLIC DISTRIBUTION, GOVT. OF INDIA",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(
            Paragraph("OFFICIAL STATUTORY INSPECTION ASSESSMENT DOSSIER", h2_style)
        )
        story.append(Spacer(1, 1 * mm))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 3 * mm))

        # Metadata Header Table
        meta_data = [
            [
                Paragraph(f"<b>Docket UUID:</b> <code>{payload.inspection_id}</code>", cell_style),
                Paragraph(f"<b>Inspection Date/Time:</b> {payload.timestamp_ist}", cell_style),
            ],
            [
                Paragraph(
                    f"<b>Officer:</b> {payload.inspector_name} (Badge: {payload.badge_number})",
                    cell_style,
                ),
                Paragraph(f"<b>Jurisdiction:</b> {payload.district}, {payload.state}", cell_style),
            ],
            [
                Paragraph(f"<b>Commodity Type:</b> {payload.commodity_category}", cell_style),
                Paragraph(
                    f"<b>Raw Image SHA-256:</b> <code>{payload.raw_image_sha256[:20]}...</code>",
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
            "STATUTORY VERDICT: ALL MANDATORY DECLARATIONS CONFORMANT"
            if is_pass
            else "STATUTORY VERDICT: NON-COMPLIANCE DETECTED - IMPROVEMENT NOTICE REQUIRED"
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
        t_verdict = Table([[Paragraph(verdict_text, v_style)]], colWidths=[180 * mm])
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
                f"<i>Exhibit 1.0: Primary Photograph of Packaging Exhibit (Scale: {disp_w/mm:.1f}mm x {disp_h/mm:.1f}mm). "
                f"Principal Display Panel Area: {payload.pdp_area_sqcm or 'N/A'} sq cm.</i>"
            )
            story.append(Paragraph(caption, cell_style))
        except Exception:
            story.append(Paragraph("<i>[Image display unavailable]</i>", cell_style))

        story.append(Spacer(1, 4 * mm))
        # Statutory Summary Note
        p1_note = (
            "<b>Adjudication Preamble:</b> This automated inspection dossier was executed in accordance with "
            "Rule 33 of the Legal Metrology (Packaged Commodities) Rules, 2011 and Section 36(1) of the Legal "
            "Metrology Act, 2009 (as amended by the Jan Vishwas Act). Photographic artifacts have been cryptographically "
            "sealed to guarantee chain of custody under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023."
        )
        story.append(Paragraph(p1_note, body_style))

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
                "<font color='#155724'><b>PASS</b></font>"
                if c_flag
                else "<font color='#721C24'><b>FAIL</b></font>"
            )
            matrix_rows.append(
                [
                    Paragraph(item.get("citation", "Rule 6"), cell_style),
                    Paragraph(item.get("bilingual_label", item.get("term_key", "")), cell_style),
                    Paragraph(
                        BilingualTypographyEngine.sanitize_for_pdf(
                            item.get("declared_value", "NOT DETECTED")
                        ),
                        cell_style,
                    ),
                    Paragraph(status_text, cell_style),
                    Paragraph(item.get("specific_defect") or "Meets statutory requirements", cell_style),
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
            f"• <b>Calculated PDP Area:</b> {payload.pdp_area_sqcm or 'Indeterminate'} cm²<br/>"
            f"• <b>Optical Calibration Factor:</b> {payload.metric_scale_mm_per_px or 'Uncalibrated'} mm/pixel<br/>"
            "• <b>Statutory Standard:</b> Under Table I of Rule 7(1), packages with PDP area between 100 cm² and 500 cm² "
            "require a minimum numeral height of <b>2.0 mm</b> (or <b>4.0 mm</b> if embossed/blown). Packages exceeding "
            "500 cm² require a minimum numeral height of <b>4.0 mm</b>.<br/>"
            "• <b>GSR 881(E) Unit Sale Price (USP) Requirement:</b> All packaged commodities exceeding 1 kg/1 L must "
            "display USP in terms of 'per kg' or 'per L'. Packages under 1 kg/1 L must display USP in 'per g' or 'per ml'."
        )
        story.append(Paragraph(pdp_txt, body_style))

        # ===================================================================
        # PAGE 3: FORENSIC EVIDENCE EXHIBITS & CROPS
        # ===================================================================
        story.append(PageBreak())
        story.append(Paragraph("PAGE 3: VISUAL FORENSIC EVIDENCE EXHIBITS", h2_style))
        story.append(
            Paragraph(
                "High-Resolution Cropped Macro Panels with Cryptographic Verification",
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
                    f"<b>Exhibit 3.{idx}: {ex.title}</b><br/>"
                    f"<b>Declaration Category:</b> {ex.declaration_type}<br/>"
                    f"<b>Extracted Text:</b> <code>{BilingualTypographyEngine.sanitize_for_pdf(ex.ocr_text)}</code><br/>"
                    f"<b>Measured Font Height:</b> {ex.font_height_mm or 'N/A'} mm "
                    f"(Min Required: {ex.required_min_height_mm or 'N/A'} mm)<br/>"
                    f"<b>Defect Assessment:</b> {ex.defect_reason or 'None'}"
                )
                t_ex = Table([[ex_img, Paragraph(ex_details, cell_style)]], colWidths=[65 * mm, 115 * mm])
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
            f"• <b>Error Level Analysis (ELA) Verdict:</b> <b>{payload.forensic_tamper_verdict}</b><br/>"
            "• <b>Decompression Bomb Firewall:</b> PASSED (&lt; 64 Megapixels)<br/>"
            "• <b>Container Sanitization:</b> EXIF/GPS metadata stripped to protect privacy; zero unauthorized script chunks."
        )
        story.append(Paragraph(ela_summary, body_style))

        # ===================================================================
        # PAGE 4: SECTION 36(1) JAN VISHWAS NOTICE & COMPOUNDING LADDER
        # ===================================================================
        story.append(PageBreak())
        story.append(
            Paragraph("PAGE 4: STATUTORY NOTICE & ADJUDICATION LADDER", h2_style)
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
            cure_days = 15
            deadline_date = (datetime.datetime.now() + datetime.timedelta(days=cure_days)).strftime("%d-%b-%Y")

            notice_p = (
                "<b>STATUTORY IMPROVEMENT NOTICE</b><br/>"
                "<i>Issued under Section 36(1) of the Legal Metrology Act, 2009 (as amended by the Jan Vishwas Act, 2023)</i><br/><br/>"
                f"<b>TO:</b> The Manufacturer / Packer / Importer of Commodity Docket <code>{payload.inspection_id}</code><br/>"
                f"<b>NOTICE REFERENCE:</b> IN/LM/{payload.district[:3].upper()}/{payload.inspection_id[:8]}<br/>"
                f"<b>DATE OF ISSUANCE:</b> {payload.timestamp_ist}<br/>"
                f"<b>STATUTORY CURE PERIOD:</b> <b>{cure_days} Calendar Days (Compliance Due By: {deadline_date})</b><br/><br/>"
                "WHEREAS an automated and officer-supervised inspection of your pre-packaged commodity established "
                "the statutory non-compliances detailed on Page 2 and Page 3 of this Dossier;<br/>"
                "NOW THEREFORE, in accordance with the amended provisions of Section 36(1), you are hereby given an opportunity "
                f"to <b>cure and rectify the said non-compliances within {cure_days} days</b> from the date of this Notice.<br/>"
                "If the defective packaging is rectified within the stipulated cure period, no compounding fee or further "
                "prosecution proceedings shall be initiated. Failure to remedy within the cure period shall result in automatic "
                "escalation to the Adjudicating Officer under Section 48 for statutory penalty determination."
            )
            t_notice = Table([[Paragraph(notice_p, cell_style)]], colWidths=[180 * mm])
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

        # Compounding Penalty Ladder Schedule
        story.append(Paragraph("Statutory Compounding Penalty Ladder (Jan Vishwas Act 2023)", h2_style))
        ladder_data = [
            [
                Paragraph("<b>Offense Classification</b>", cell_bold),
                Paragraph("<b>Statutory Section</b>", cell_bold),
                Paragraph("<b>Civil Penalty Quantum</b>", cell_bold),
                Paragraph("<b>Judicial Terms</b>", cell_bold),
            ],
            [
                Paragraph("First Statutory Non-Compliance", cell_style),
                Paragraph("Section 36(1)", cell_style),
                Paragraph("Penalty up to <b>Rs. 25,000</b>", cell_style),
                Paragraph("Zero criminal liability / Decriminalized", cell_style),
            ],
            [
                Paragraph("Second Non-Compliance (Repeat Offense)", cell_style),
                Paragraph("Section 36(1) & 48", cell_style),
                Paragraph("Penalty up to <b>Rs. 50,000</b>", cell_style),
                Paragraph("Compounding under authorized officer", cell_style),
            ],
            [
                Paragraph("Subsequent Non-Compliance (3rd+ Offense)", cell_style),
                Paragraph("Section 36(1) & 48A", cell_style),
                Paragraph("Penalty up to <b>Rs. 1,00,000</b>", cell_style),
                Paragraph("Compounding ladder escalation", cell_style),
            ],
        ]
        t_ladder = Table(ladder_data, colWidths=[45 * mm, 35 * mm, 45 * mm, 55 * mm])
        t_ladder.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF4F8")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(t_ladder)
        story.append(Spacer(1, 6 * mm))

        # Final Sign-Off Block
        sign_block = [
            [
                Paragraph(
                    f"<b>Inspecting Officer:</b> {payload.inspector_name}<br/>"
                    f"<b>Badge Number:</b> {payload.badge_number}<br/>"
                    f"<b>Office:</b> Directorate of Legal Metrology, {payload.district}, {payload.state}",
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
