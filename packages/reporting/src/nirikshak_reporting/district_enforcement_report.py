"""Render an unsigned draft summary of supplied district enforcement statistics.

The renderer does not verify the supplied records, perform enforcement actions,
or submit reports to government recipients."""

from __future__ import annotations

import datetime
import io
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .text_safety import DRAFT_NOTICE, join_markup, markup, text

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

        story: List[Any] = [Paragraph(text(DRAFT_NOTICE), self.styles["BodyDark"]), Spacer(1, 8)]

        # 1. State Emblem & Government Header
        story.append(
            Paragraph(
                text(markup('METROLENS ASSISTIVE DRAFT — REGION: {0}<br/>Supplied enforcement information; not an official government report<br/>DISTRICT METROLOGY INTELLIGENCE REPORT: {1}', payload.state_name.upper(), payload.district_name.upper())),
                self.styles["DocHeader"],
            )
        )
        story.append(
            Paragraph(
                text(markup('Reporting Window: {0} to {1} | Ref: {2}', payload.reporting_period_start.strftime('%d-%b-%Y'), payload.reporting_period_end.strftime('%d-%b-%Y'), payload.report_reference_id)),
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
                Paragraph(text(markup('<b>{0}</b>', payload.total_inspections)), self.styles["KpiValue"]),
                Paragraph(text(markup('<b>{0:.1f}%</b>', overall_compliance)), self.styles["KpiValue"]),
                Paragraph(text(markup('<b>₹{0:,.0f}</b>', payload.total_compounding_revenue_inr)), self.styles["KpiValue"]),
                Paragraph(text(markup('<b>{0}</b>', payload.court_prosecutions_filed)), self.styles["KpiValue"]),
                Paragraph(text(markup('<b>{0}</b>', payload.seizures_executed_count)), self.styles["KpiValue"]),
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
                Paragraph(text(s.sector_name), self.styles["TableCell"]),
                Paragraph(text(str(s.inspections_count)), self.styles["TableCell"]),
                Paragraph(text(str(s.violations_count)), self.styles["TableCell"]),
                Paragraph(text(markup('{0:.1f}%', s.compliance_percentage)), self.styles["TableCellBold"]),
                Paragraph(text(markup('₹{0:,.2f}', s.compounding_fees_inr)), self.styles["TableCell"]),
                Paragraph(text(str(s.prosecutions_count)), self.styles["TableCellBold"]),
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
            form_i_badge = 'VALID' if r.has_valid_form_i_nomination else markup('<b>NOT SUPPLIED</b>')
            recid_rows.append([
                Paragraph(text(markup('<b>{0}</b><br/>{1}', r.entity_name, r.cin_or_gstin)), self.styles["TableCell"]),
                Paragraph(text(r.registered_district), self.styles["TableCell"]),
                Paragraph(text(str(r.prior_violations_count)), self.styles["TableCellBold"]),
                Paragraph(text(r.most_recent_offence_date.strftime('%d-%b-%Y')), self.styles["TableCell"]),
                Paragraph(text('; '.join(r.statutory_sections_violated)), self.styles["TableCell"]),
                Paragraph(text(form_i_badge), self.styles["TableCell"]),
                Paragraph(text(markup('<b>{0}</b>', r.status_action_taken)), self.styles["TableCellBold"]),
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
        rec_text = join_markup("<br/>", (
            markup('<b>{0}.</b> {1}', idx, rec)
            for idx, rec in enumerate(payload.executive_recommendations, start=1)
        ))
        if not rec_text:
            rec_text = (
                markup('No recommendations supplied. Any enforcement action requires authorized human review of evidence and applicable law.')
            )
        story.append(Paragraph(text(rec_text), self.styles["BodyDark"]))
        story.append(Spacer(1, 18))

        # 6. Officer Attestation & Digital Verification Block
        auth_data = [
            [
                Paragraph(
                    text(markup('<b>SUPPLIED REPORTER (UNVERIFIED):</b><br/><br/><b>{0}</b><br/>{1}<br/>Division: {2}<br/>Date: {3}', payload.reporting_officer_name, payload.reporting_officer_designation, payload.controller_division, datetime.date.today().strftime('%d-%b-%Y'))),
                    self.styles["TableCell"],
                ),
                Paragraph(
                    text(markup('<b>PROPOSED RECIPIENTS (NOT SENT):</b><br/><br/>1. District Magistrate, {0}<br/>2. Controller of Legal Metrology, {1}<br/>3. Special Public Prosecutor (Consumer Protection)<br/>Unsigned draft; no digital seal verified', payload.district_name, payload.state_name)),
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
