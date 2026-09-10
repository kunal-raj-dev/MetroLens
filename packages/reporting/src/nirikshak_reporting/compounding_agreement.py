"""Render a draft compounding summary from supplied case and payment information.

This library does not verify payment, authority, statutory eligibility, or identity,
and does not issue an order or discharge."""

from __future__ import annotations

import datetime
import io
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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

logger = logging.getLogger("nirikshak_reporting.compounding_agreement")


@dataclass
class CompoundingOrderData:
    """Input payload for generating a Section 48 Discharge Order."""
    order_number: str
    case_reference: str
    inspection_id: str
    date_of_order: datetime.date
    state_government_name: str
    department_name: str
    authorized_officer_name: str
    authorized_officer_designation: str
    authorized_officer_station: str
    offender_entity_name: str
    offender_cin_or_reg: str
    offender_gstin: str
    offender_pan: str
    offender_address: str
    director_or_proprietor_name: str
    statutory_offences_compounded: List[str]
    date_of_offence_commission: datetime.date
    inspection_location: str
    compounding_fee_inr: float
    treasury_challan_number: str
    treasury_payment_date: datetime.date
    bank_utr_reference: str
    treasury_head_of_account: str = "0435 - Other Agricultural & Consumer Affairs (Weights & Measures)"
    panchnama_reference: Optional[str] = None
    remarks: str = ""


class CompoundingAgreementCompiler:
    """
    Renders statutory bilingual Section 48 Compounding Agreements and Discharge Orders.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:
        self.styles.add(
            ParagraphStyle(
                name="EmblemHeader",
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#1A365D"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SubEmblemHeader",
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#2D3748"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="DeedTitle",
                fontName="Helvetica-Bold",
                fontSize=12,
                leading=16,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#742A2A"),
                spaceAfter=10,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="LegalBody",
                fontName="Helvetica",
                fontSize=9,
                leading=13,
                alignment=TA_JUSTIFY,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="LegalBodyBold",
                fontName="Helvetica-Bold",
                fontSize=9,
                leading=13,
                alignment=TA_LEFT,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="TableText",
                fontName="Helvetica",
                fontSize=8,
                leading=11,
                textColor=colors.HexColor("#2D3748"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="TableTextBold",
                fontName="Helvetica-Bold",
                fontSize=8,
                leading=11,
                textColor=colors.HexColor("#1A202C"),
            )
        )

    def compile_order_pdf(self, data: CompoundingOrderData) -> bytes:
        """Renders complete PDF bytes for the Section 48 discharge deed."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        story: List[Any] = [Paragraph(text(DRAFT_NOTICE), self.styles["LegalBody"]), Spacer(1, 8)]

        # 1. Official Seal & Emblem Header
        story.append(
            Paragraph(
                text(markup('METROLENS ASSISTIVE DRAFT — REGION: {0}<br/>Prepared by MetroLens; no government endorsement or issue', data.state_government_name.upper())),
                self.styles["EmblemHeader"],
            )
        )
        story.append(
            Paragraph(
                text(markup('LEGAL METROLOGY WING — CONTROLLER OF LEGAL METROLOGY<br/>DIVISION: {0}', data.authorized_officer_station.upper())),
                self.styles["SubEmblemHeader"],
            )
        )
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=12))

        # 2. Statutory Title
        story.append(
            Paragraph(
                "DRAFT COMPOUNDING & DISCHARGE FORM<br/>"
                "<u>UNDER SECTION 48 READ WITH SECTION 48A OF THE LEGAL METROLOGY ACT, 2009</u>",
                self.styles["DeedTitle"],
            )
        )

        # 3. Reference and Date Bar
        ref_table_data = [
            [
                Paragraph(text(markup('<b>Order No:</b> {0}', data.order_number)), self.styles["TableText"]),
                Paragraph(text(markup('<b>Date of Order:</b> {0}', data.date_of_order.strftime('%d-%b-%Y'))), self.styles["TableTextBold"]),
            ],
            [
                Paragraph(text(markup('<b>Case Ref:</b> {0}', data.case_reference)), self.styles["TableText"]),
                Paragraph(text(markup('<b>Inspection Ref:</b> {0}', data.inspection_id)), self.styles["TableText"]),
            ],
        ]
        ref_table = Table(ref_table_data, colWidths=[260, 250])
        ref_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        story.append(ref_table)
        story.append(Spacer(1, 12))

        # 4. Narrative Recital (Whereas clauses)
        preamble = (
            markup('<b>DRAFT CASE SUMMARY:</b><br/>Supplied inspection date: {0}; location: {1}; entity: {2}; representative: {3}.<br/>Alleged provisions: {4}.<br/>These statements, officer authority, admission, and eligibility for compounding require independent verification.', data.date_of_offence_commission.strftime('%d-%m-%Y'), data.inspection_location, data.offender_entity_name, data.director_or_proprietor_name, '; '.join(data.statutory_offences_compounded))
        )
        story.append(Paragraph(text(preamble), self.styles["LegalBody"]))
        story.append(Spacer(1, 10))

        # 5. Treasury Payment Details Box
        story.append(Paragraph("<b>SCHEDULE OF COMPOUNDING FEE & CYBER TREASURY RECONCILIATION</b>", self.styles["LegalBodyBold"]))
        story.append(Spacer(1, 4))

        treasury_data = [
            [Paragraph("<b>Particulars</b>", self.styles["TableTextBold"]), Paragraph("<b>Details / Treasury Record</b>", self.styles["TableTextBold"])],
            [Paragraph("Offender Legal Name", self.styles["TableText"]), Paragraph(text(data.offender_entity_name), self.styles["TableTextBold"])],
            [Paragraph("CIN / Registration & GSTIN", self.styles["TableText"]), Paragraph(text(markup('{0} / {1}', data.offender_cin_or_reg, data.offender_gstin)), self.styles["TableText"])],
            [Paragraph("PAN Number", self.styles["TableText"]), Paragraph(text(data.offender_pan), self.styles["TableText"])],
            [Paragraph("Statutory Compounding Fee Assessed", self.styles["TableText"]), Paragraph(text(markup('<b>₹ {0:,.2f}</b>', data.compounding_fee_inr)), self.styles["TableTextBold"])],
            [Paragraph("Cyber Treasury e-Challan No.", self.styles["TableText"]), Paragraph(text(data.treasury_challan_number), self.styles["TableTextBold"])],
            [Paragraph("Bank UTR / Transaction Ref", self.styles["TableText"]), Paragraph(text(data.bank_utr_reference), self.styles["TableText"])],
            [Paragraph("Date of Treasury Realization", self.styles["TableText"]), Paragraph(text(data.treasury_payment_date.strftime('%d-%b-%Y')), self.styles["TableText"])],
            [Paragraph("Treasury Head of Account", self.styles["TableText"]), Paragraph(text(data.treasury_head_of_account), self.styles["TableText"])],
        ]
        t_table = Table(treasury_data, colWidths=[180, 330])
        t_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#718096")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        story.append(t_table)
        story.append(Spacer(1, 12))

        # 6. Operative Order & Statutory Discharge
        operative_order = (
            markup('<b>PROPOSED COMPOUNDING — NO ORDER ISSUED:</b><br/>Supplied amount: Rs. {0:,.2f}. Payment realization, statutory eligibility, and any disposition require authorized human verification. This draft does not record a discharge, update a government ledger, or prevent or initiate proceedings.', data.compounding_fee_inr)
        )
        story.append(Paragraph(text(operative_order), self.styles["LegalBody"]))
        story.append(Spacer(1, 20))

        # 7. Signature & Seal Block
        sig_data = [
            [
                Paragraph(text(markup('{0}{1}', markup('<b>PROPOSED SIGNATORY (UNVERIFIED):</b><br/><br/><br/>(Authorized Signatory & Seal)<br/>M/s '), data.offender_entity_name)), self.styles["TableText"]),
                Paragraph(text(markup('<b>PROPOSED OFFICER (UNVERIFIED):</b><br/><br/><br/><b>({0})</b><br/>{1}<br/>Office of Controller of Legal Metrology<br/>Seal of Office', data.authorized_officer_name, data.authorized_officer_designation)), self.styles["TableTextBold"]),
            ]
        ]
        sig_table = Table(sig_data, colWidths=[255, 255])
        sig_table.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ])
        )
        story.append(KeepTogether(sig_table))

        # Build document
        doc.build(story)
        return buffer.getvalue()
