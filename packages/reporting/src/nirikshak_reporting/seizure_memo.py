"""
Statutory Rule 29 Seizure Memo & Panchnama Inventory Generator
=============================================================
Renders formal Search & Seizure Memos under Section 15 of the Legal Metrology
Act, 2009 and Rule 29 of the Legal Metrology (Packaged Commodities) Rules, 2011,
in strict compliance with Section 105 of the Bharatiya Nagarik Suraksha Sanhita, 2023.

Statutory Mandates:
-------------------
- Section 15(1)(c) of LM Act: Power of Legal Metrology Officer to seize any non-conforming
  packaged commodities, weights, measures, or relevant documents.
- Section 105 BNSS 2023 / Section 100 CrPC: Search and seizure must be conducted in the
  presence of two independent respectable witnesses of the locality.
- Mandatory Panchnama narrative: Detailed recording of locus, search procedure, voluntary
  witness attestations, serial numbers of security seal tags, and delivery of receipt.
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
    """Complete data structure required to compile a court-admissible Seizure Memo."""
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

        story: List[Any] = []

        # 1. State Emblem & Government Header
        header_text = (
            f"GOVERNMENT OF {payload.state.upper()}<br/>"
            f"DEPARTMENT OF LEGAL METROLOGY (WEIGHTS & MEASURES WING)<br/>"
            f"DISTRICT: {payload.district.upper()}"
        )
        story.append(Paragraph(header_text, self.styles["HeaderTitle"]))
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
                Paragraph(f"<b>Seizure Memo No:</b> {payload.seizure_memo_number}", self.styles["GridCell"]),
                Paragraph(f"<b>Date of Seizure:</b> {payload.date_of_seizure.strftime('%d-%b-%Y')}", self.styles["GridCellBold"]),
            ],
            [
                Paragraph(f"<b>Inspection Ref:</b> {payload.inspection_id}", self.styles["GridCell"]),
                Paragraph(f"<b>Time:</b> {payload.time_commenced} to {payload.time_concluded}", self.styles["GridCell"]),
            ],
            [
                Paragraph(f"<b>Police Station:</b> {payload.police_station_jurisdiction}", self.styles["GridCell"]),
                Paragraph(f"<b>Working Standard Box ID:</b> {payload.working_standard_weight_box_id}", self.styles["GridCell"]),
            ],
            [
                Paragraph(f"<b>Place of Search:</b> {payload.place_of_search_address}", self.styles["GridCell"]),
                Paragraph(f"<b>Occupier:</b> {payload.occupier_name} ({payload.occupier_firm_name})", self.styles["GridCell"]),
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
            f"We, the undersigned Panch witnesses, having been called upon by <b>{payload.officer_name}</b>, "
            f"{payload.officer_designation}, hereby state that today on <b>{payload.date_of_seizure.strftime('%d-%m-%Y')}</b>, "
            f"we accompanied the said Legal Metrology Officer to the premises of <b>M/s {payload.occupier_firm_name}</b> "
            f"situated at <i>{payload.place_of_search_address}</i>. In our presence and in the presence of the person in-charge, "
            f"<b>Shri/Smt. {payload.occupier_name}</b>, an inspection of packaged commodities stocked and offered for sale "
            f"was conducted. On verifying the sample packages using duly certified Working Standard Weights "
            f"(verified on {payload.working_standard_last_verified.strftime('%d-%m-%Y')}), the packages detailed below were found to "
            f"contravene the mandatory provisions of the Legal Metrology Act, 2009 and Packaged Commodities Rules, 2011, "
            f"and were consequently seized into official custody."
        )
        story.append(Paragraph(narrative, self.styles["MemoText"]))
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
                Paragraph(str(item.item_sno), self.styles["GridCell"]),
                Paragraph(f"{item.commodity_description}<br/>({item.brand_name})", self.styles["GridCell"]),
                Paragraph(item.batch_or_lot_no, self.styles["GridCell"]),
                Paragraph(item.declared_net_quantity, self.styles["GridCell"]),
                Paragraph(item.test_measured_quantity, self.styles["GridCellBold"]),
                Paragraph(f"₹{item.declared_mrp_inr:.2f}", self.styles["GridCell"]),
                Paragraph(str(item.units_seized_count), self.styles["GridCellBold"]),
                Paragraph(item.security_seal_number, self.styles["GridCellBold"]),
                Paragraph(item.contravention_alleged, self.styles["GridCell"]),
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
            f"The aforesaid seized articles have been duly packed and secured under official lead seal / security seal "
            f"tags bearing the numbers indicated above, in our presence. The sealed packages have been taken into official "
            f"custody and dispatched to <b>{payload.custodial_malkhana_destination}</b> for production before the Court "
            f"of the Judicial Magistrate First Class or authorized testing laboratory. A true copy of this Seizure Memo "
            f"was handed over on the spot to the occupier, who acknowledged receipt thereof."
        )
        story.append(Paragraph(closing_narrative, self.styles["MemoText"]))
        story.append(Spacer(1, 12))

        # 6. Attestation & Signature Blocks (Panch Witnesses + Occupier + Officer)
        attest_data = [
            [
                Paragraph(
                    f"<b>PANCH WITNESS 1:</b><br/>"
                    f"Name: {payload.witness_1_name} (Age: {payload.witness_1_age})<br/>"
                    f"S/o / D/o: {payload.witness_1_father}<br/>"
                    f"Address: {payload.witness_1_address}<br/>"
                    f"ID Proof: {payload.witness_1_id}<br/><br/>"
                    f"Signature: ______________________",
                    self.styles["GridCell"],
                ),
                Paragraph(
                    f"<b>PANCH WITNESS 2:</b><br/>"
                    f"Name: {payload.witness_2_name} (Age: {payload.witness_2_age})<br/>"
                    f"S/o / D/o: {payload.witness_2_father}<br/>"
                    f"Address: {payload.witness_2_address}<br/>"
                    f"ID Proof: {payload.witness_2_id}<br/><br/>"
                    f"Signature: ______________________",
                    self.styles["GridCell"],
                ),
            ],
            [
                Paragraph(
                    f"<b>OCCUPIER / PERSON IN-CHARGE:</b><br/>"
                    f"Received copy of this Seizure Memo.<br/>"
                    f"Name: {payload.occupier_name}<br/>"
                    f"Firm: {payload.occupier_firm_name}<br/><br/>"
                    f"Signature / Thumb: _______________",
                    self.styles["GridCell"],
                ),
                Paragraph(
                    f"<b>SEIZING OFFICER:</b><br/>"
                    f"Name: <b>{payload.officer_name}</b><br/>"
                    f"Designation: {payload.officer_designation}<br/>"
                    f"ID / Gazette: {payload.officer_id_number}<br/><br/>"
                    f"Official Seal & Signature: ________",
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
