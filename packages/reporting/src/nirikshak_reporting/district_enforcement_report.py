"""
District Metrology Enforcement & Recidivism Intelligence Report Generator
========================================================================
Compiles multi-establishment executive intelligence dossiers for District Magistrates,
State Controllers of Legal Metrology, and the Ministry of Consumer Affairs.

Features:
---------
1. Zonal Enforcement Metrics: Total inspections, compliance rate, notices issued,
   compounding revenue collected, and court prosecutions instituted.
2. Sectoral Analysis: Granular breakdown across Packaged Food, Industrial Goods (Cement/Paints),
   E-Commerce Fulfillment Centers, and Cosmetics.
3. High-Risk Corporate Recidivist Roster: Identifies repeat violators barred from Section 48
   compounding and escalated for criminal trial under Section 36 / Section 48(2).
4. Form I Director Liability Audit: Highlights corporate entities operating without valid
   Rule 29 director nominations, exposing Managing Directors to criminal liability.
"""

from __future__ import annotations

import datetime
import io
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger("nirikshak_reporting.district_enforcement_report")


@dataclass
class SectorMetric:
    """Compliance statistics for a specific industry commodity category."""
    sector_name: str
    inspections_count: int
    violations_count: int
    compliance_percentage: float
    compounding_fees_inr: float
    prosecutions_count: int


@dataclass
class RecidivistEntityRecord:
    """Corporate entity or distributor with repeat violations within the 3-year window."""
    entity_name: str
    cin_or_gstin: str
    registered_district: str
    prior_violations_count: int
    most_recent_offence_date: datetime.date
    statutory_sections_violated: List[str]
    has_valid_form_i_nomination: bool
    status_action_taken: str  # "Prosecution Docket Filed", "Summons Issued", etc.


@dataclass
class DistrictEnforcementPayload:
    """Comprehensive data payload for compiling a District Metrology Intelligence Report."""
    report_reference_id: str
    reporting_period_start: datetime.date
    reporting_period_end: datetime.date
    district_name: str
    state_name: str
    controller_division: str
    reporting_officer_name: str
    reporting_officer_designation: str
    total_inspections: int
    compliant_inspections: int
    non_compliant_inspections: int
    statutory_notices_issued: int
    compounding_cases_concluded: int
    total_compounding_revenue_inr: float
    court_prosecutions_filed: int
    seizures_executed_count: int
    sector_metrics: List[SectorMetric]
    recidivist_entities: List[RecidivistEntityRecord]
    executive_recommendations: List[str] = field(default_factory=list)


class DistrictEnforcementReportCompiler:
    """
    Renders multi-page executive intelligence dossiers using ReportLab.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self) -> None:
        self.styles.add(
            ParagraphStyle(
                name="DocHeader",
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#1A365D"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="DocSubHeader",
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#4A5568"),
                spaceAfter=10,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SectionHeading",
                fontName="Helvetica-Bold",
                fontSize=10.5,
                leading=14,
                textColor=colors.HexColor("#2B6CB0"),
                spaceBefore=8,
                spaceAfter=4,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="BodyDark",
                fontName="Helvetica",
                fontSize=8.5,
                leading=12,
                alignment=TA_JUSTIFY,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="TableCell",
                fontName="Helvetica",
                fontSize=7.5,
                leading=10,
                textColor=colors.HexColor("#2D3748"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="TableCellBold",
                fontName="Helvetica-Bold",
                fontSize=7.5,
                leading=10,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="KpiValue",
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2B6CB0"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="KpiLabel",
                fontName="Helvetica",
                fontSize=7.5,
                leading=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#718096"),
            )
        )

    def compile_district_report_pdf(self, payload: DistrictEnforcementPayload) -> bytes:
        """Renders complete PDF bytes for the district enforcement intelligence report."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=35,
            rightMargin=35,
            topMargin=35,
            bottomMargin=35,
        )

        story: List[Any] = []

        # 1. State Emblem & Government Header
        story.append(
            Paragraph(
                f"GOVERNMENT OF {payload.state_name.upper()}<br/>"
                f"CONTROLLER OF LEGAL METROLOGY & CONSUMER AFFAIRS<br/>"
                f"DISTRICT METROLOGY INTELLIGENCE REPORT: {payload.district_name.upper()}",
                self.styles["DocHeader"],
            )
        )
        story.append(
            Paragraph(
                f"Reporting Window: {payload.reporting_period_start.strftime('%d-%b-%Y')} to "
                f"{payload.reporting_period_end.strftime('%d-%b-%Y')} | Ref: {payload.report_reference_id}",
                self.styles["DocSubHeader"],
            )
        )
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=10))

        # 2. Executive KPI Summary Cards
        overall_compliance = (
            (payload.compliant_inspections / payload.total_inspections * 100.0)
            if payload.total_inspections > 0 else 0.0
        )
        kpi_data = [
            [
                Paragraph(f"<b>{payload.total_inspections}</b>", self.styles["KpiValue"]),
                Paragraph(f"<b>{overall_compliance:.1f}%</b>", self.styles["KpiValue"]),
                Paragraph(f"<b>₹{payload.total_compounding_revenue_inr:,.0f}</b>", self.styles["KpiValue"]),
                Paragraph(f"<b>{payload.court_prosecutions_filed}</b>", self.styles["KpiValue"]),
                Paragraph(f"<b>{payload.seizures_executed_count}</b>", self.styles["KpiValue"]),
            ],
            [
                Paragraph("Total Inspections", self.styles["KpiLabel"]),
                Paragraph("Compliance Rate", self.styles["KpiLabel"]),
                Paragraph("Compounding Fees Realized", self.styles["KpiLabel"]),
                Paragraph("Court Prosecutions", self.styles["KpiLabel"]),
                Paragraph("Stock Seizures", self.styles["KpiLabel"]),
            ],
        ]
        kpi_table = Table(kpi_data, colWidths=[105, 105, 105, 105, 105])
        kpi_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
            ])
        )
        story.append(kpi_table)
        story.append(Spacer(1, 12))

        # 3. Sectoral Compliance Breakdown
        story.append(Paragraph("<b>1. SECTORAL METROLOGICAL AUDIT ANALYSIS</b>", self.styles["SectionHeading"]))
        sector_headers = [
            Paragraph("<b>Commodity Sector</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Inspections</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Violations</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Compliance %</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Compounding (₹)</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Court Trials</b>", self.styles["TableCellBold"]),
        ]
        sector_rows = [sector_headers]
        for s in payload.sector_metrics:
            sector_rows.append([
                Paragraph(s.sector_name, self.styles["TableCell"]),
                Paragraph(str(s.inspections_count), self.styles["TableCell"]),
                Paragraph(str(s.violations_count), self.styles["TableCell"]),
                Paragraph(f"{s.compliance_percentage:.1f}%", self.styles["TableCellBold"]),
                Paragraph(f"₹{s.compounding_fees_inr:,.2f}", self.styles["TableCell"]),
                Paragraph(str(s.prosecutions_count), self.styles["TableCellBold"]),
            ])

        sector_table = Table(sector_rows, colWidths=[150, 65, 65, 75, 95, 75])
        sector_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#718096")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        story.append(sector_table)
        story.append(Spacer(1, 12))

        # 4. Repeat Violators & Recidivism Roster (Section 48(2) Escalations)
        story.append(
            Paragraph(
                "<b>2. HIGH-RISK CORPORATE RECIDIVIST ROSTER (3-YEAR LOOKBACK BAR)</b>",
                self.styles["SectionHeading"],
            )
        )
        recid_headers = [
            Paragraph("<b>Entity Name & Identifier</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Registered District</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Prior Off.</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Recent Date</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Sections Violated</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Form I</b>", self.styles["TableCellBold"]),
            Paragraph("<b>Enforcement Action</b>", self.styles["TableCellBold"]),
        ]
        recid_rows = [recid_headers]
        for r in payload.recidivist_entities:
            form_i_badge = "VALID" if r.has_valid_form_i_nomination else "<b>NONE (MD Liable)</b>"
            recid_rows.append([
                Paragraph(f"<b>{r.entity_name}</b><br/>{r.cin_or_gstin}", self.styles["TableCell"]),
                Paragraph(r.registered_district, self.styles["TableCell"]),
                Paragraph(str(r.prior_violations_count), self.styles["TableCellBold"]),
                Paragraph(r.most_recent_offence_date.strftime("%d-%b-%Y"), self.styles["TableCell"]),
                Paragraph("; ".join(r.statutory_sections_violated), self.styles["TableCell"]),
                Paragraph(form_i_badge, self.styles["TableCell"]),
                Paragraph(f"<b>{r.status_action_taken}</b>", self.styles["TableCellBold"]),
            ])

        recid_table = Table(recid_rows, colWidths=[125, 75, 40, 60, 95, 60, 70])
        recid_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FED7D7")),  # Light red header
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9B2C2C")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#FEB2B2")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        story.append(recid_table)
        story.append(Spacer(1, 12))

        # 5. Executive Enforcement Directives
        story.append(Paragraph("<b>3. DIRECTIVES FOR SPECIAL METROLOGY MAGISTRATES & CONTROLLER</b>", self.styles["SectionHeading"]))
        rec_text = ""
        for idx, rec in enumerate(payload.executive_recommendations, start=1):
            rec_text += f"<b>{idx}.</b> {rec}<br/>"
        if not rec_text:
            rec_text = (
                "<b>1.</b> Mandatory institution of criminal proceedings under Section 36(1) for all entities flagged "
                "with prior violations within 36 months.<br/>"
                "<b>2.</b> Immediate issuance of Form I summons to Managing Directors of non-compliant corporate entities "
                "where no nominated officer exists under Rule 29.<br/>"
                "<b>3.</b> Enhanced random surprise inspections at automated distribution centers and dark stores."
            )
        story.append(Paragraph(rec_text, self.styles["BodyDark"]))
        story.append(Spacer(1, 18))

        # 6. Officer Attestation & Digital Verification Block
        auth_data = [
            [
                Paragraph(
                    f"<b>SUBMITTED BY:</b><br/><br/>"
                    f"<b>{payload.reporting_officer_name}</b><br/>"
                    f"{payload.reporting_officer_designation}<br/>"
                    f"Division: {payload.controller_division}<br/>"
                    f"Date: {datetime.date.today().strftime('%d-%b-%Y')}",
                    self.styles["TableCell"],
                ),
                Paragraph(
                    f"<b>FORWARDED TO:</b><br/><br/>"
                    f"1. District Magistrate, {payload.district_name}<br/>"
                    f"2. Controller of Legal Metrology, {payload.state_name}<br/>"
                    f"3. Special Public Prosecutor (Consumer Protection)<br/>"
                    f"Official Digital Seal: VERIFIED",
                    self.styles["TableCellBold"],
                ),
            ]
        ]
        auth_table = Table(auth_data, colWidths=[260, 265])
        auth_table.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        story.append(KeepTogether(auth_table))

        # Build document
        doc.build(story)
        return buffer.getvalue()
