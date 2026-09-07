"""
Section 48 Statutory Compounding Deed & Discharge Order Generator
================================================================
Renders legally enforceable bilingual Compounding Agreements and Orders of Discharge
under Section 48 and Section 48A of the Legal Metrology Act, 2009.

Legal & Administrative Importance:
----------------------------------
When an offender admits to an initial contravention of Rule 6, 7, 18, or 26 of the
Legal Metrology (Packaged Commodities) Rules, 2011, and deposits the assessed compounding
fee into the Government Cyber Treasury (Head: 0435 - Weights & Measures), the Controller
or Authorized Officer issues a formal Order of Discharge.
This document operates as a statutory bar under Section 48(3) against subsequent criminal
prosecution for the specific offence compounded.
"""

from __future__ import annotations

import datetime
import io
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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

        story: List[Any] = []

        # 1. Official Seal & Emblem Header
        story.append(
            Paragraph(
                f"GOVERNMENT OF {data.state_government_name.upper()}<br/>DEPARTMENT OF CONSUMER AFFAIRS, FOOD & CIVIL SUPPLIES",
                self.styles["EmblemHeader"],
            )
        )
        story.append(
            Paragraph(
                f"LEGAL METROLOGY WING — CONTROLLER OF LEGAL METROLOGY<br/>DIVISION: {data.authorized_officer_station.upper()}",
                self.styles["SubEmblemHeader"],
            )
        )
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=12))

        # 2. Statutory Title
        story.append(
            Paragraph(
                "STATUTORY ORDER OF COMPOUNDING & DISCHARGE<br/>"
                "<u>UNDER SECTION 48 READ WITH SECTION 48A OF THE LEGAL METROLOGY ACT, 2009</u>",
                self.styles["DeedTitle"],
            )
        )

        # 3. Reference and Date Bar
        ref_table_data = [
            [
                Paragraph(f"<b>Order No:</b> {data.order_number}", self.styles["TableText"]),
                Paragraph(f"<b>Date of Order:</b> {data.date_of_order.strftime('%d-%b-%Y')}", self.styles["TableTextBold"]),
            ],
            [
                Paragraph(f"<b>Case Ref:</b> {data.case_reference}", self.styles["TableText"]),
                Paragraph(f"<b>Inspection Ref:</b> {data.inspection_id}", self.styles["TableText"]),
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
            f"<b>WHEREAS</b>, an inspection was conducted on <b>{data.date_of_offence_commission.strftime('%d-%m-%Y')}</b> "
            f"at the premises / establishment situated at <i>{data.inspection_location}</i>, wherein sample packaged commodities "
            f"manufactured / packed / offered for sale by <b>M/s {data.offender_entity_name}</b> (represented by its "
            f"Director/Proprietor <b>Shri/Smt. {data.director_or_proprietor_name}</b>) were inspected by the authorized "
            f"Legal Metrology Officer;<br/><br/>"
            f"<b>AND WHEREAS</b>, the said packaged commodities were found in contravention of the statutory provisions, "
            f"specifically: <b>{'; '.join(data.statutory_offences_compounded)}</b>, punishable under Section 36(1) / "
            f"Section 36(2) of the Legal Metrology Act, 2009;<br/><br/>"
            f"<b>AND WHEREAS</b>, the said offender has formally made an application in writing under Section 48(1) "
            f"of the Legal Metrology Act, 2009 admitting the commission of the said contravention, and requesting that "
            f"the offence be compounded without recourse to prosecution before the Judicial Magistrate;<br/><br/>"
            f"<b>AND WHEREAS</b>, verification of the statewide Central Compounding Ledger confirms that the offender has "
            f"<u>not</u> committed or compounded the same or similar offence within a period of three (3) years preceding "
            f"this date, and is consequently eligible for compounding under Section 48(2) of the said Act;"
        )
        story.append(Paragraph(preamble, self.styles["LegalBody"]))
        story.append(Spacer(1, 10))

        # 5. Treasury Payment Details Box
        story.append(Paragraph("<b>SCHEDULE OF COMPOUNDING FEE & CYBER TREASURY RECONCILIATION</b>", self.styles["LegalBodyBold"]))
        story.append(Spacer(1, 4))

        treasury_data = [
            [Paragraph("<b>Particulars</b>", self.styles["TableTextBold"]), Paragraph("<b>Details / Treasury Record</b>", self.styles["TableTextBold"])],
            [Paragraph("Offender Legal Name", self.styles["TableText"]), Paragraph(data.offender_entity_name, self.styles["TableTextBold"])],
            [Paragraph("CIN / Registration & GSTIN", self.styles["TableText"]), Paragraph(f"{data.offender_cin_or_reg} / {data.offender_gstin}", self.styles["TableText"])],
            [Paragraph("PAN Number", self.styles["TableText"]), Paragraph(data.offender_pan, self.styles["TableText"])],
            [Paragraph("Statutory Compounding Fee Assessed", self.styles["TableText"]), Paragraph(f"<b>₹ {data.compounding_fee_inr:,.2f}</b>", self.styles["TableTextBold"])],
            [Paragraph("Cyber Treasury e-Challan No.", self.styles["TableText"]), Paragraph(data.treasury_challan_number, self.styles["TableTextBold"])],
            [Paragraph("Bank UTR / Transaction Ref", self.styles["TableText"]), Paragraph(data.bank_utr_reference, self.styles["TableText"])],
            [Paragraph("Date of Treasury Realization", self.styles["TableText"]), Paragraph(data.treasury_payment_date.strftime('%d-%b-%Y'), self.styles["TableText"])],
            [Paragraph("Treasury Head of Account", self.styles["TableText"]), Paragraph(data.treasury_head_of_account, self.styles["TableText"])],
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
            f"<b><u>ORDER OF DISCHARGE UNDER SECTION 48(3)</u></b><br/>"
            f"NOW THEREFORE, in exercise of the powers conferred under Section 48(1) of the Legal Metrology Act, 2009, "
            f"the undersigned, having verified the realization of the full compounding fee of <b>₹{data.compounding_fee_inr:,.2f}</b> "
            f"into the Government Treasury, hereby <b>COMPOUNDS</b> the aforesaid offences. In terms of Section 48(3) of the said Act, "
            f"no further prosecution or legal proceeding shall be initiated against the said offender in respect of the "
            f"offences specified herein.<br/><br/>"
            f"<b>IMPORTANT STATUTORY CAUTION UNDER SECTION 48(2):</b><br/>"
            f"The offender is hereby formally put on notice that this compounding is recorded in the Central Legal Metrology "
            f"Ledger. If the offender commits the same or similar offence at any time within a period of <b>three (3) years</b> "
            f"from this date, the subsequent offence shall be <b>STRICTLY NON-COMPOUNDABLE</b>, and the offender shall be "
            f"mandatorily prosecuted before the Court of the Judicial Magistrate First Class with statutory imprisonment "
            f"and enhanced fines under Section 36 and Section 48A."
        )
        story.append(Paragraph(operative_order, self.styles["LegalBody"]))
        story.append(Spacer(1, 20))

        # 7. Signature & Seal Block
        sig_data = [
            [
                Paragraph("<b>ACCEPTED & UNDERTAKEN BY OFFENDER:</b><br/><br/><br/>(Authorized Signatory & Seal)<br/>M/s " + data.offender_entity_name, self.styles["TableText"]),
                Paragraph(f"<b>ORDER PASSED BY:</b><br/><br/><br/><b>({data.authorized_officer_name})</b><br/>{data.authorized_officer_designation}<br/>Office of Controller of Legal Metrology<br/>Seal of Office", self.styles["TableTextBold"]),
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
