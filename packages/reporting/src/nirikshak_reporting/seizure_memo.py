"""Render an unsigned draft inventory and search-record summary.

Supplied statements, identity, authority, witnesses, seals and custody require
independent verification; this renderer performs no seizure or custody transfer."""

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

logger = logging.getLogger("nirikshak_reporting.seizure_memo")


@dataclass
class SeizedStockItem:
    """Individual line-item entry in the Panchnama seizure inventory."""
    item_sno: int
    commodity_description: str
    brand_name: str
    batch_or_lot_no: str
    declared_net_quantity: str
    test_measured_quantity: str
    declared_mrp_inr: float
    units_seized_count: int
    security_seal_number: str
    contravention_alleged: str


@dataclass
class SeizureMemoPayload:
    """Complete data structure required to compile a assistive draft Seizure Memo."""
    seizure_memo_number: str
    inspection_id: str
    date_of_seizure: datetime.date
    time_commenced: str  # e.g. "11:30 AM"
    time_concluded: str  # e.g. "02:15 PM"
    place_of_search_address: str
    police_station_jurisdiction: str
    district: str
    state: str
    officer_name: str
    officer_designation: str
    officer_id_number: str
    occupier_name: str
    occupier_father_or_spouse: str
    occupier_designation: str  # e.g. "Store Manager / Proprietor"
    occupier_firm_name: str
    witness_1_name: str
    witness_1_age: int
    witness_1_father: str
    witness_1_address: str
    witness_1_id: str
    witness_2_name: str
    witness_2_age: int
    witness_2_father: str
    witness_2_address: str
    witness_2_id: str
    working_standard_weight_box_id: str
    working_standard_last_verified: datetime.date
    seized_items: List[SeizedStockItem]
    custodial_malkhana_destination: str
    remarks: str = ""


class SeizureMemoCompiler:
    """
    ReportLab PDF generator for Rule 29 Seizure Memos and on-site Panchnama records.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self) -> None:
        self.styles.add(
            ParagraphStyle(
                name="HeaderTitle",
                fontName="Helvetica-Bold",
                fontSize=13,
                leading=16,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#1A365D"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SubTitle",
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#742A2A"),
                spaceAfter=8,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="MemoText",
                fontName="Helvetica",
                fontSize=8.5,
                leading=12,
                alignment=TA_JUSTIFY,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="MemoTextBold",
                fontName="Helvetica-Bold",
                fontSize=8.5,
                leading=12,
                textColor=colors.HexColor("#1A202C"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="GridCell",
                fontName="Helvetica",
                fontSize=7.5,
                leading=10,
                textColor=colors.HexColor("#2D3748"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="GridCellBold",
                fontName="Helvetica-Bold",
                fontSize=7.5,
                leading=10,
                textColor=colors.HexColor("#1A202C"),
            )
        )

    def compile_seizure_memo_pdf(self, payload: SeizureMemoPayload) -> bytes:
        """Renders complete PDF bytes for the Seizure Memo & Panchnama."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=35,
            rightMargin=35,
            topMargin=35,
            bottomMargin=35,
        )

        story: List[Any] = [Paragraph(text(DRAFT_NOTICE), self.styles["MemoText"]), Spacer(1, 8)]

        # 1. State Emblem & Government Header
        header_text = (
            markup('METROLENS ASSISTIVE DRAFT — REGION: {0}<br/>DEPARTMENT OF LEGAL METROLOGY (WEIGHTS & MEASURES WING)<br/>DISTRICT: {1}', payload.state.upper(), payload.district.upper())
        )
        story.append(Paragraph(text(header_text), self.styles["HeaderTitle"]))
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                "FORM OF SEIZURE MEMO & PANCHNAMA<br/>"
                "<u>[Under Section 15 of Legal Metrology Act, 2009 read with Rule 29 of PCR, 2011 "
                "and Section 105 BNSS, 2023]</u>",
                self.styles["SubTitle"],
            )
        )
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=10))

        # 2. Key Procedural Data Block
        proc_data = [
            [
                Paragraph(text(markup('<b>Seizure Memo No:</b> {0}', payload.seizure_memo_number)), self.styles["GridCell"]),
                Paragraph(text(markup('<b>Date of Seizure:</b> {0}', payload.date_of_seizure.strftime('%d-%b-%Y'))), self.styles["GridCellBold"]),
            ],
            [
                Paragraph(text(markup('<b>Inspection Ref:</b> {0}', payload.inspection_id)), self.styles["GridCell"]),
                Paragraph(text(markup('<b>Time:</b> {0} to {1}', payload.time_commenced, payload.time_concluded)), self.styles["GridCell"]),
            ],
            [
                Paragraph(text(markup('<b>Police Station:</b> {0}', payload.police_station_jurisdiction)), self.styles["GridCell"]),
                Paragraph(text(markup('<b>Working Standard Box ID:</b> {0}', payload.working_standard_weight_box_id)), self.styles["GridCell"]),
            ],
            [
                Paragraph(text(markup('<b>Place of Search:</b> {0}', payload.place_of_search_address)), self.styles["GridCell"]),
                Paragraph(text(markup('<b>Occupier:</b> {0} ({1})', payload.occupier_name, payload.occupier_firm_name)), self.styles["GridCell"]),
            ],
        ]
        proc_table = Table(proc_data, colWidths=[260, 265])
        proc_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        story.append(proc_table)
        story.append(Spacer(1, 10))

        # 3. Panchnama Opening Narrative
        narrative = (
            markup('<b>SUPPLIED INSPECTION ACCOUNT — UNVERIFIED:</b><br/>Officer: {0}, {1}; date: {2}; premises: {3}, {4}; occupier: {5}; working-standard verification date supplied: {6}. This compiler does not establish that a search, measurement, seizure, or witness attestation occurred.', payload.officer_name, payload.officer_designation, payload.date_of_seizure.strftime('%d-%m-%Y'), payload.occupier_firm_name, payload.place_of_search_address, payload.occupier_name, payload.working_standard_last_verified.strftime('%d-%m-%Y'))
        )
        story.append(Paragraph(text(narrative), self.styles["MemoText"]))
        story.append(Spacer(1, 10))

        # 4. Seized Goods Inventory Grid
        story.append(Paragraph("<b>INVENTORY OF SEIZED PACKAGED COMMODITIES</b>", self.styles["MemoTextBold"]))
        story.append(Spacer(1, 4))

        inv_headers = [
            Paragraph("<b>S.No</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Commodity & Brand</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Batch No</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Decl. Qty</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Test Qty</b>", self.styles["GridCellBold"]),
            Paragraph("<b>MRP</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Seized</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Seal Tag No.</b>", self.styles["GridCellBold"]),
            Paragraph("<b>Offence Alleged</b>", self.styles["GridCellBold"]),
        ]
        inv_rows = [inv_headers]

        for item in payload.seized_items:
            inv_rows.append([
                Paragraph(text(str(item.item_sno)), self.styles["GridCell"]),
                Paragraph(text(markup('{0}<br/>({1})', item.commodity_description, item.brand_name)), self.styles["GridCell"]),
                Paragraph(text(item.batch_or_lot_no), self.styles["GridCell"]),
                Paragraph(text(item.declared_net_quantity), self.styles["GridCell"]),
                Paragraph(text(item.test_measured_quantity), self.styles["GridCellBold"]),
                Paragraph(text(markup('₹{0:.2f}', item.declared_mrp_inr)), self.styles["GridCell"]),
                Paragraph(text(str(item.units_seized_count)), self.styles["GridCellBold"]),
                Paragraph(text(item.security_seal_number), self.styles["GridCellBold"]),
                Paragraph(text(item.contravention_alleged), self.styles["GridCell"]),
            ])

        inv_table = Table(inv_rows, colWidths=[25, 80, 50, 45, 45, 40, 35, 75, 130])
        inv_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2F7")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#718096")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        story.append(inv_table)
        story.append(Spacer(1, 10))

        # 5. Custody & Sealing Recital
        closing_narrative = (
            markup('<b>PROPOSED CUSTODY DESTINATION:</b> {0}. Sealing, custody transfers, and receipt must be documented and verified by authorized people; no transfer or service is performed by this draft.', payload.custodial_malkhana_destination)
        )
        story.append(Paragraph(text(closing_narrative), self.styles["MemoText"]))
        story.append(Spacer(1, 12))

        # 6. Attestation & Signature Blocks (Panch Witnesses + Occupier + Officer)
        attest_data = [
            [
                Paragraph(
                    text(markup('<b>PANCH WITNESS 1:</b><br/>Name: {0} (Age: {1})<br/>S/o / D/o: {2}<br/>Address: {3}<br/>ID Proof: {4}<br/><br/>Signature: ______________________', payload.witness_1_name, payload.witness_1_age, payload.witness_1_father, payload.witness_1_address, payload.witness_1_id)),
                    self.styles["GridCell"],
                ),
                Paragraph(
                    text(markup('<b>PANCH WITNESS 2:</b><br/>Name: {0} (Age: {1})<br/>S/o / D/o: {2}<br/>Address: {3}<br/>ID Proof: {4}<br/><br/>Signature: ______________________', payload.witness_2_name, payload.witness_2_age, payload.witness_2_father, payload.witness_2_address, payload.witness_2_id)),
                    self.styles["GridCell"],
                ),
            ],
            [
                Paragraph(
                    text(markup('<b>OCCUPIER / PERSON IN-CHARGE:</b><br/>Receipt requires human acknowledgement.<br/>Name: {0}<br/>Firm: {1}<br/><br/>Signature / Thumb: _______________', payload.occupier_name, payload.occupier_firm_name)),
                    self.styles["GridCell"],
                ),
                Paragraph(
                    text(markup('<b>SEIZING OFFICER:</b><br/>Name: <b>{0}</b><br/>Designation: {1}<br/>ID / Gazette: {2}<br/><br/>Official Seal & Signature: ________', payload.officer_name, payload.officer_designation, payload.officer_id_number)),
                    self.styles["GridCellBold"],
                ),
            ],
        ]
        attest_table = Table(attest_data, colWidths=[260, 265])
        attest_table.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        story.append(KeepTogether(attest_table))

        # Build document
        doc.build(story)
        return buffer.getvalue()
