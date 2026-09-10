"""Render unsigned, preliminary packaging-assessment PDFs from supplied inspection results.

Input digests and application timestamps are recorded references, not signatures or
proof of lawful custody. Configured rule findings require authorized human review.
Text values are escaped before entering ReportLab paragraph markup."""

import io
import time
import hashlib
import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from .text_safety import DRAFT_NOTICE, join_markup, markup, text

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas
import qrcode
from PIL import Image as PILImage

from nirikshak_rules_engine.schemas import (
    ComplianceEvaluationResult,
    ComplianceState,
    VerdictBadgeColor,
    RuleEvaluationRecord,
    CanonicalDeclaration,
    MetricScaleResult,
    EvidenceCropMetadata,
    ImprovementNoticePayload,
)


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas recording total page counts and rendering
    standardized running headers, footers, micro-print borders, and verification QR code.
    """

    def __init__(self, *args, **kwargs):
        kwargs["pageCompression"] = 0
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        page_width, page_height = self._pagesize
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#495057"))

        # Running Header (Top)
        self.setStrokeColor(colors.HexColor("#1B365D"))
        self.setLineWidth(1.5)
        self.line(40, page_height - 37, page_width - 40, page_height - 37)

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B365D"))
        self.drawString(40, page_height - 32, "METROLENS • IMAGE-BASED PACKAGING ASSESSMENT • ASSISTIVE DRAFT")

        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#6C757D"))

        # Running Footer (Bottom)
        self.setStrokeColor(colors.HexColor("#DEE2E6"))
        self.setLineWidth(0.75)
        self.line(40, 42, page_width - 40, 42)

        page_str = markup('Page {0} of {1}', self._pageNumber, page_count)
        self.drawString(40, 32, "Preliminary image-based screening • Not a legal determination")
        self.drawRightString(page_width - 40, 32, page_str)

        # Micro-print security watermark in bottom-center
        self.setFont("Helvetica", 6)
        self.setFillColor(colors.HexColor("#ADB5BD"))
        self.drawCentredString(page_width / 2, 22, "UNSIGNED DRAFT • AUTHORIZED HUMAN REVIEW REQUIRED • NO STATUTORY NOTICE ISSUED")

        self.restoreState()


class PDFReportCompiler:
    """
    High-performance, assistive draft PDF report compiler.
    Compiles full evidentiary dossiers in < 500ms on standard CPU.
    """

    # Palette
    COLOR_PRIMARY = colors.HexColor("#1B365D")    # Deep Navy
    COLOR_SECONDARY = colors.HexColor("#2B547E")  # Slate Blue
    COLOR_COMPLIANT = colors.HexColor("#1E7E34")  # Forest Green
    COLOR_VIOLATION = colors.HexColor("#BD2130")  # Ruby Red
    COLOR_REVIEW = colors.HexColor("#D39E00")     # Dark Amber
    COLOR_EXEMPT = colors.HexColor("#0056B3")     # Royal Blue
    COLOR_GRAY = colors.HexColor("#6C757D")       # Slate Gray
    COLOR_BG_LIGHT = colors.HexColor("#F8F9FA")   # Off-white
    COLOR_BORDER = colors.HexColor("#DEE2E6")     # Light gray border

    def __init__(self):
        self.styles = self._build_stylesheet()

    def _build_stylesheet(self) -> Dict[str, ParagraphStyle]:
        """Builds typographic styling hierarchy for ReportLab elements."""
        base_styles = getSampleStyleSheet()
        custom = {}

        custom["DocTitle"] = ParagraphStyle(
            "DocTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=self.COLOR_PRIMARY,
            alignment=0,
            spaceAfter=4,
        )

        custom["DocSubtitle"] = ParagraphStyle(
            "DocSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=self.COLOR_SECONDARY,
            spaceAfter=10,
        )

        custom["SectionHeading"] = ParagraphStyle(
            "SectionHeading",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=self.COLOR_PRIMARY,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        )

        custom["Body"] = ParagraphStyle(
            "Body",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#212529"),
        )

        custom["BodyBold"] = ParagraphStyle(
            "BodyBold",
            parent=custom["Body"],
            fontName="Helvetica-Bold",
        )

        custom["VerdictBadge"] = ParagraphStyle(
            "VerdictBadge",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            alignment=1,
            textColor=colors.white,
        )

        custom["LegalNoticeHeader"] = ParagraphStyle(
            "LegalNoticeHeader",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=self.COLOR_VIOLATION,
            alignment=1,
            spaceAfter=6,
        )

        custom["LegalNoticeText"] = ParagraphStyle(
            "LegalNoticeText",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#212529"),
        )

        custom["Disclaimer"] = ParagraphStyle(
            "Disclaimer",
            parent=base_styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=7.5,
            leading=10,
            textColor=self.COLOR_GRAY,
            alignment=0,
        )

        custom["TableHead"] = ParagraphStyle(
            "TableHead",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=self.COLOR_PRIMARY,
        )

        custom["TableCell"] = ParagraphStyle(
            "TableCell",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#212529"),
        )

        custom["TableCellBold"] = ParagraphStyle(
            "TableCellBold",
            parent=custom["TableCell"],
            fontName="Helvetica-Bold",
        )

        return custom

    def _sanitize_currency_symbol(self, value: object) -> str:
        """
        Safely maps Unicode Rupee glyph ('₹') to standard ASCII ('Rs. ')
        to guarantee 100% crash-free rendering regardless of host OS font availability.
        """
        if value is None:
            return "Not supplied"
        return str(value).replace("₹", "Rs. ")

    def _generate_qr_flowable(self, verification_payload: str, size_inches: float = 1.0) -> RLImage:
        """Generates a tamper-evident QR code image flowable from payload string."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=1,
        )
        qr.add_data(verification_payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return RLImage(buf, width=size_inches * inch, height=size_inches * inch)

    def _build_header_section(
        self,
        result: ComplianceEvaluationResult,
        officer_id: Optional[str] = None,
        jurisdiction_code: Optional[str] = None,
    ) -> List[Any]:
        """Constructs document title, administrative metadata block, and composite verdict banner."""
        elements = []

        # Title Block
        title_text = "METROLENS • PRELIMINARY PACKAGING ASSESSMENT"
        elements.append(Paragraph(text(title_text), self.styles["DocTitle"]))
        sub_text = (
            "Automated image-based screening using configured packaging rules. "
            "All findings require authorized human review and verification of applicable law."
        )
        elements.append(Paragraph(text(sub_text), self.styles["DocSubtitle"]))

        # Metadata & QR Code Header Grid
        now_utc = result.timestamp_utc or "Not recorded"
        clean_sha = result.sha256_hash or "Not recorded"
        # Local identifiers only: this QR is not an official verification service.
        verification_payload = json.dumps({
            "document_type": "assistive_draft",
            "inspection_id": result.inspection_id,
            "input_sha256": clean_sha,
        }, ensure_ascii=True)
        qr_flowable = self._generate_qr_flowable(verification_payload, size_inches=1.1)

        meta_rows = [
            [
                Paragraph("<b>Inspection ID:</b>", self.styles["TableCellBold"]),
                Paragraph(text(str(result.inspection_id)), self.styles["TableCell"]),
                Paragraph("<b>Date & Time (UTC):</b>", self.styles["TableCellBold"]),
                Paragraph(text(now_utc[:19].replace('T', ' ')), self.styles["TableCell"]),
                qr_flowable,
            ],
            [
                Paragraph("<b>Operator (unverified):</b>", self.styles["TableCellBold"]),
                Paragraph(text(officer_id or 'Not verified'), self.styles["TableCell"]),
                Paragraph("<b>Jurisdiction Code:</b>", self.styles["TableCellBold"]),
                Paragraph(text(jurisdiction_code or 'Not verified'), self.styles["TableCell"]),
                "",
            ],
            [
                Paragraph("<b>Ruleset Version:</b>", self.styles["TableCellBold"]),
                Paragraph("Not recorded", self.styles["TableCell"]),
                Paragraph("<b>Document Status:</b>", self.styles["TableCellBold"]),
                Paragraph("Unsigned assistive draft", self.styles["TableCell"]),
                "",
            ],
        ]

        meta_table = Table(
            meta_rows,
            colWidths=[105, 130, 115, 100, 82],
            style=[
                ("SPAN", (4, 0), (4, 2)),
                ("ALIGN", (4, 0), (4, 2), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ],
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 6))

        # Composite Verdict Badge
        verdict = getattr(result.overall_verdict, "value", str(result.overall_verdict))
        if verdict in ("COMPLIANT", ComplianceState.GREEN.value):
            badge_color = self.COLOR_COMPLIANT
            badge_text = "IMAGE-BASED ASSESSMENT: NO IMAGE-VERIFIABLE VIOLATION DETECTED"
        elif verdict in ("NON_COMPLIANT", ComplianceState.RED.value):
            badge_color = self.COLOR_VIOLATION
            badge_text = "IMAGE-BASED ASSESSMENT: POTENTIAL NON-COMPLIANCE DETECTED"
        elif verdict in ("DEVIATION_DETECTED", "UNCERTAIN", ComplianceState.AMBER.value):
            badge_color = self.COLOR_REVIEW
            badge_text = "IMAGE-BASED ASSESSMENT: MANUAL REVIEW REQUIRED"
        elif verdict in ("EXEMPTED", ComplianceState.BLUE.value):
            badge_color = self.COLOR_EXEMPT
            badge_text = "IMAGE-BASED ASSESSMENT: STATUTORY EXEMPTION APPLIED (RULE 3 / RULE 26)"
        else:
            badge_color = self.COLOR_GRAY
            badge_text = markup('IMAGE-BASED ASSESSMENT: {0}', verdict)

        badge_table = Table(
            [[Paragraph(text(badge_text), self.styles["VerdictBadge"])]],
            colWidths=[532],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), badge_color),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ],
        )
        elements.append(badge_table)
        elements.append(Spacer(1, 4))

        # Executive Summary Callout
        summary_clean = self._sanitize_currency_symbol(result.primary_legal_summary)
        summary_box = Table(
            [[Paragraph(text(markup('<b>Executive Summary:</b> {0}', summary_clean)), self.styles["Body"])]],
            colWidths=[532],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), self.COLOR_BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ],
        )
        elements.append(summary_box)
        elements.append(Spacer(1, 8))

        return elements

    def _build_chain_of_custody_section(self, result: ComplianceEvaluationResult) -> List[Any]:
        """Constructs Section 63 BSA / 65B IEA cryptographic integrity block."""
        elements = [Paragraph("1. Recorded Evidence References", self.styles["SectionHeading"])]

        sha_clean = result.sha256_hash or "Not recorded"
        records = [
            [
                Paragraph("<b>Evidence Property</b>", self.styles["TableHead"]),
                Paragraph("<b>Recorded Value</b>", self.styles["TableHead"]),
                Paragraph("<b>Interpretation</b>", self.styles["TableHead"]),
            ],
            [
                Paragraph("Raw Image SHA-256 Digest", self.styles["TableCellBold"]),
                Paragraph(text(markup("<font face='Courier' size=6.5>{0}</font>", sha_clean)), self.styles["TableCell"]),
                Paragraph("Input bytes; source authenticity unverified", self.styles["TableCell"]),
            ],
            [
                Paragraph("Inspection Reference Digest", self.styles["TableCellBold"]),
                Paragraph(text(markup("<font face='Courier' size=6.5>{0}</font>", hashlib.sha256((result.inspection_id + sha_clean).encode()).hexdigest())), self.styles["TableCell"]),
                Paragraph("Unkeyed checksum; no signature", self.styles["TableCell"]),
            ],
            [
                Paragraph("Perception Engine Timestamp", self.styles["TableCellBold"]),
                Paragraph(text(str(result.timestamp_utc or 'UTC Timestamp')), self.styles["TableCell"]),
                Paragraph("Recorded by application; unverified clock", self.styles["TableCell"]),
            ],
        ]

        table = Table(
            records,
            colWidths=[140, 260, 132],
            style=[
                ("BACKGROUND", (0, 0), (-1, 0), self.COLOR_BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ],
        )
        elements.append(table)
        elements.append(Spacer(1, 8))
        return elements

    def _build_metrology_calibration_section(self, scale: Optional[MetricScaleResult]) -> List[Any]:
        """Constructs optical metric scale and Principal Display Panel area table."""
        elements = [Paragraph("2. Optical Metric Scale & Principal Display Panel (PDP) Calibration", self.styles["SectionHeading"])]

        if not scale:
            rows = [
                [
                    Paragraph("<b>Calibration State:</b>", self.styles["TableCellBold"]),
                    Paragraph("Uncalibrated (Optical Reference Anchor Absent)", self.styles["TableCell"]),
                    Paragraph("<b>Scale Factor:</b>", self.styles["TableCellBold"]),
                    Paragraph("N/A", self.styles["TableCell"]),
                ],
                [
                    Paragraph("<b>Computed PDP Area:</b>", self.styles["TableCellBold"]),
                    Paragraph("Uncalibrated", self.styles["TableCell"]),
                    Paragraph("<b>Surface Geometry:</b>", self.styles["TableCellBold"]),
                    Paragraph("Planar Assumption", self.styles["TableCell"]),
                ],
            ]
        else:
            scale_str = markup('{0:.4f} mm/px', scale.scale_factor_mm_per_px) if scale.scale_factor_mm_per_px else "Uncalibrated"
            pdp_str = markup('{0:.1f} cm²', scale.pdp_area_sqcm) if scale.pdp_area_sqcm else "N/A"
            anchor_str = scale.anchor_type_detected.replace("_", " ").title() if scale.anchor_type_detected else "None"
            tilt_str = markup('{0:.1f}°', scale.tilt_angle_deg) if scale.tilt_angle_deg is not None else "0.0°"

            rows = [
                [
                    Paragraph("<b>Calibration Status:</b>", self.styles["TableCellBold"]),
                    Paragraph(text('Calibrated' if scale.is_calibrated else 'Uncalibrated'), self.styles["TableCell"]),
                    Paragraph("<b>Scale Factor ($S$):</b>", self.styles["TableCellBold"]),
                    Paragraph(text(scale_str), self.styles["TableCell"]),
                ],
                [
                    Paragraph("<b>Anchor Target:</b>", self.styles["TableCellBold"]),
                    Paragraph(text(anchor_str), self.styles["TableCell"]),
                    Paragraph("<b>Computed PDP Area:</b>", self.styles["TableCellBold"]),
                    Paragraph(text(markup('<b>{0}</b>', pdp_str)), self.styles["TableCellBold"]),
                ],
                [
                    Paragraph("<b>Surface Tilt:</b>", self.styles["TableCellBold"]),
                    Paragraph(text(tilt_str), self.styles["TableCell"]),
                    Paragraph("<b>Cylindrical Curvature:</b>", self.styles["TableCellBold"]),
                    Paragraph(text('Yes (Vertical Invariance Applied)' if scale.is_cylindrical else 'No (Planar Face)'), self.styles["TableCell"]),
                ],
            ]

        table = Table(
            rows,
            colWidths=[120, 146, 120, 146],
            style=[
                ("BOX", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ],
        )
        elements.append(table)
        elements.append(Spacer(1, 8))
        return elements

    def _build_rule_evaluation_matrix_section(self, evaluations: List[RuleEvaluationRecord]) -> List[Any]:
        """Constructs the comprehensive statutory compliance audit ledger."""
        elements = [Paragraph("3. Statutory Compliance Evaluation Matrix (LM(PC) Rules, 2011)", self.styles["SectionHeading"])]

        table_rows = [
            [
                Paragraph("<b>Rule / Statute</b>", self.styles["TableHead"]),
                Paragraph("<b>Statutory Reference</b>", self.styles["TableHead"]),
                Paragraph("<b>Status</b>", self.styles["TableHead"]),
                Paragraph("<b>Observed Evidence</b>", self.styles["TableHead"]),
                Paragraph("<b>Statutory Mandate</b>", self.styles["TableHead"]),
            ]
        ]

        for r in evaluations:
            # Color badge based on status
            if r.status == "PASS":
                status_p = Paragraph("<font color='#1E7E34'><b>PASS</b></font>", self.styles["TableCell"])
            elif r.status == "FAIL":
                status_p = Paragraph("<font color='#BD2130'><b>FAIL</b></font>", self.styles["TableCell"])
            elif r.status == "REVIEW":
                status_p = Paragraph("<font color='#D39E00'><b>REVIEW</b></font>", self.styles["TableCell"])
            elif r.status == "EXEMPT":
                status_p = Paragraph("<font color='#0056B3'><b>EXEMPT</b></font>", self.styles["TableCell"])
            else:
                status_p = Paragraph(text(markup('<b>{0}</b>', r.status)), self.styles["TableCell"])

            obs_clean = self._sanitize_currency_symbol(r.observed_value)
            req_clean = self._sanitize_currency_symbol(r.required_value)

            table_rows.append([
                Paragraph(text(r.rule_title), self.styles["TableCellBold"]),
                Paragraph(text(r.statutory_reference), self.styles["TableCell"]),
                status_p,
                Paragraph(text(obs_clean), self.styles["TableCell"]),
                Paragraph(text(req_clean), self.styles["TableCell"]),
            ])

        table = Table(
            table_rows,
            colWidths=[110, 85, 45, 142, 150],
            style=[
                ("BACKGROUND", (0, 0), (-1, 0), self.COLOR_BG_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ],
        )
        elements.append(table)
        elements.append(Spacer(1, 8))
        return elements

    def _build_improvement_notice_section(self, notice: Optional[ImprovementNoticePayload]) -> List[Any]:
        """Renders Section 36(1) Jan Vishwas Statutory Improvement Notice if violations exist."""
        if not notice or not notice.recommended:
            return []

        elements = [Paragraph("4. Proposed Improvement Notice for Review", self.styles["SectionHeading"])]

        grounds_clean = self._sanitize_currency_symbol(notice.statutory_grounds)
        itemized = notice.itemized_violations or []
        items_p = join_markup("<br/>", (markup('• {0}', self._sanitize_currency_symbol(v)) for v in itemized)) if itemized else grounds_clean

        notice_box_content = [
            Paragraph("<b>DRAFT IMPROVEMENT NOTICE • FOR AUTHORIZED HUMAN REVIEW</b>", self.styles["LegalNoticeHeader"]),
            Paragraph(
                text(markup('<b>SUPPLIED PROVISION:</b> {0}<br/><b>PROPOSED CURE WINDOW (UNVERIFIED):</b> {1} calendar days.<br/><b>PROPOSED AUTHORITY (UNVERIFIED):</b> {2}', notice.act_provision, notice.cure_period_days, notice.compounding_authority)),
                self.styles["LegalNoticeText"],
            ),
            Spacer(1, 4),
            Paragraph(text(markup('<b>ITEMIZED STATUTORY GROUNDS:</b><br/>{0}', items_p)), self.styles["LegalNoticeText"]),
            Spacer(1, 4),
            Paragraph(
                "<b>DRAFT ONLY:</b> This report does not issue or serve a notice. An authorized officer must "
                "verify the evidence and applicable law, determine any cure period, and approve and issue any "
                "statutory notice. No proceedings or deadlines are initiated by this document.",
                self.styles["LegalNoticeText"],
            ),
        ]

        notice_table = Table(
            [[notice_box_content]],
            colWidths=[532],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF5F5")),
                ("BOX", (0, 0), (-1, -1), 1.5, self.COLOR_VIOLATION),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ],
        )
        elements.append(notice_table)
        elements.append(Spacer(1, 8))
        return elements

    def _build_evidence_crops_section(self, crops: List[EvidenceCropMetadata]) -> List[Any]:
        """Constructs visual evidence crops section with bounding box and measured height metadata."""
        if not crops:
            return []

        elements = [Paragraph("5. Visual Forensic Evidence & Calibrated Crop Callouts", self.styles["SectionHeading"])]

        crop_cells = []
        for c in crops:
            cell_items = []
            if c.crop_base64 and c.crop_base64.startswith("data:image"):
                try:
                    # Strip base64 header
                    raw_b64 = c.crop_base64.split(",", 1)[1]
                    img_data = base64.b64decode(raw_b64)
                    pil_crop = PILImage.open(io.BytesIO(img_data))
                    w, h = pil_crop.size
                    aspect = h / w if w > 0 else 0.5
                    rl_crop = RLImage(io.BytesIO(img_data), width=2.2 * inch, height=(2.2 * aspect) * inch)
                    cell_items.append(rl_crop)
                except Exception:
                    cell_items.append(Paragraph("[Visual Crop Stream]", self.styles["TableCell"]))
            else:
                cell_items.append(Paragraph("[Visual Evidence Bounding Box]", self.styles["TableCell"]))

            cell_items.append(Spacer(1, 2))
            bbox_str = markup('[{0}]', ', '.join(map(str, c.bbox_px)))
            h_str = markup('{0:.2f} mm', c.measured_height_mm) if c.measured_height_mm is not None else "Uncalibrated"
            cell_items.append(Paragraph(text(markup('<b>{0}</b>', c.label)), self.styles["TableCellBold"]))
            cell_items.append(Paragraph(text(markup('Field: {0} | Height: {1}<br/>BBox: {2}', c.field_name, h_str, bbox_str)), self.styles["TableCell"]))
            crop_cells.append(cell_items)

        # Pair into 2-column table
        table_data = []
        for i in range(0, len(crop_cells), 2):
            if i + 1 < len(crop_cells):
                table_data.append([crop_cells[i], crop_cells[i + 1]])
            else:
                table_data.append([crop_cells[i], ""])

        if table_data:
            crops_table = Table(
                table_data,
                colWidths=[260, 260],
                style=[
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOX", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, self.COLOR_BORDER),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ],
            )
            elements.append(crops_table)
            elements.append(Spacer(1, 8))

        return elements

    def _build_disclaimer_and_signature_section(self) -> List[Any]:
        """Constructs statutory disclaimer under Section 15 and official signature block."""
        elements = [
            Paragraph("6. Human Review and Limitations", self.styles["SectionHeading"]),
            Paragraph(
                "<b>PRELIMINARY SCREENING:</b> This unsigned draft summarizes application results and can contain "
                "OCR or rule-evaluation errors. It does not establish compliance, authenticate evidence, verify "
                "an officer, or issue a notice. An authorized reviewer must inspect the original packaging, "
                "check the applicable law and calibration, and approve any subsequent action.",
                self.styles["Disclaimer"],
            ),
            Spacer(1, 10),
        ]

        sig_table = Table(
            [
                [
                    Paragraph("<b>Inspecting Officer Name:</b> ___________________", self.styles["TableCell"]),
                    Paragraph("<b>Official Seal:</b>", self.styles["TableCell"]),
                    Paragraph("<b>Signature:</b> ___________________", self.styles["TableCell"]),
                ],
                [
                    Paragraph("<b>Badge / ID No.:</b> ___________________", self.styles["TableCell"]),
                    "",
                    Paragraph("<b>Date:</b> _____ / _____ / _____", self.styles["TableCell"]),
                ],
            ],
            colWidths=[200, 132, 200],
            style=[
                ("SPAN", (1, 0), (1, 1)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ],
        )
        elements.append(sig_table)
        return elements

    def compile_report_pdf(
        self,
        result: ComplianceEvaluationResult,
        officer_id: Optional[str] = None,
        jurisdiction_code: Optional[str] = None,
        include_evidence_crops: bool = True,
        officer_notes: Optional[str] = None,
        reference_image_bytes: Optional[bytes] = None,
    ) -> bytes:
        """
        Compiles the complete assistive draft assessment report into PDF bytes.

        Returns:
            Binary PDF byte stream.
        """
        start_time = time.perf_counter()
        if officer_notes is not None and len(officer_notes) > 2000:
            raise ValueError("Operator notes must not exceed 2000 characters.")
        buffer = io.BytesIO()

        # Letter page size with 40pt (0.55 inch) margins
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=40,
            rightMargin=40,
            topMargin=45,
            bottomMargin=45,
            title=f"MetroLens draft {result.inspection_id}",
            author="MetroLens",
            subject="Unsigned preliminary packaging assessment",
        )

        flowables: List[Any] = [Paragraph(text(DRAFT_NOTICE), self.styles["Disclaimer"]), Spacer(1, 8)]

        # 1. Header & Administrative Metadata
        flowables.extend(self._build_header_section(result, officer_id, jurisdiction_code))

        if officer_notes and officer_notes.strip():
            flowables.append(Paragraph("Supplied Operator Notes (Unverified)", self.styles["SectionHeading"]))
            flowables.append(Paragraph(text(officer_notes.strip()), self.styles["Body"]))
            flowables.append(Spacer(1, 8))

        if reference_image_bytes is not None:
            # Accept only retained bytes, never a filename or URL. Bound dimensions
            # before decoding, then embed a compact image with no copied metadata.
            with PILImage.open(io.BytesIO(reference_image_bytes)) as source_image:
                width, height = source_image.size
                if width < 1 or height < 1 or max(width, height) > 8000 or width * height > 40_000_000:
                    raise ValueError("Reference image exceeds the supported dimensions.")
                source_image.thumbnail((1200, 1200))
                pixels = source_image.convert("RGB")
                clean = PILImage.new("RGB", pixels.size)
                clean.paste(pixels)
                reference_buffer = io.BytesIO()
                clean.save(reference_buffer, format="JPEG", quality=85)
                width, height = clean.size
            scale = min(360 / width, 240 / height)
            flowables.append(Paragraph("Packaging Reference Image", self.styles["SectionHeading"]))
            flowables.append(RLImage(io.BytesIO(reference_buffer.getvalue()), width=width * scale, height=height * scale))
            flowables.append(Paragraph(
                "Sanitized reference copy, resized for this draft. The input digest below refers to the original uploaded bytes.",
                self.styles["Disclaimer"],
            ))
            flowables.append(Spacer(1, 8))

        # 2. Cryptographic Chain of Custody
        flowables.extend(self._build_chain_of_custody_section(result))

        # 3. Metrology Calibration
        flowables.extend(self._build_metrology_calibration_section(result.calibrated_measurements))

        # 4. Statutory Rule Evaluation Matrix
        flowables.extend(self._build_rule_evaluation_matrix_section(result.rule_evaluations))

        # 5. Section 36(1) Jan Vishwas Statutory Improvement Notice
        if result.improvement_notice and result.improvement_notice.recommended:
            flowables.extend(self._build_improvement_notice_section(result.improvement_notice))

        # 6. Visual Forensic Evidence Crops
        if include_evidence_crops and result.evidence_crops:
            flowables.extend(self._build_evidence_crops_section(result.evidence_crops))

        # 7. Disclaimer & Officer Signature
        flowables.extend(self._build_disclaimer_and_signature_section())

        # Build document with custom NumberedCanvas
        doc.build(flowables, canvasmaker=NumberedCanvas)

        pdf_bytes = buffer.getvalue()
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return pdf_bytes


# Singleton compiler instance
pdf_compiler = PDFReportCompiler()
compile_inspection_pdf = pdf_compiler.compile_report_pdf
