"""Render an unsigned electronic-record summary for authorized human review.

Supplied officer details, hashes, and statements are not independently verified.
The output is a draft and does not establish legal admissibility or certification."""

from __future__ import annotations

import datetime
import hashlib
import io
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .text_safety import DRAFT_NOTICE, join_markup, markup, text

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


@dataclass(frozen=True)
class CertifyingOfficerInfo:
    """Information regarding the authorized Legal Metrology Officer certifying the record."""

    officer_name: str
    badge_number: str
    designation: str = "Not supplied"
    district: str = "Not supplied"
    state: str = "Not supplied"
    jurisdiction_code: str = "Not supplied"
    station_address: str = "Not supplied"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "officer_name": self.officer_name,
            "badge_number": self.badge_number,
            "designation": self.designation,
            "district": self.district,
            "state": self.state,
            "jurisdiction_code": self.jurisdiction_code,
            "station_address": self.station_address,
        }


@dataclass(frozen=True)
class ElectronicRecordEvidenceDetails:
    """Evidentiary parameters and cryptographic hashes of the record under certification."""

    inspection_id: str
    timestamp_utc: str
    timestamp_ist: str
    raw_image_sha256: str
    raw_image_filename: str
    raw_image_size_bytes: int
    derived_pdf_sha256: Optional[str] = None
    audit_chain_merkle_root: Optional[str] = None
    ocr_observations_count: int = 0
    statutory_violations_detected: int = 0
    overall_verdict: str = "NOT_ASSESSED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inspection_id": self.inspection_id,
            "timestamp_utc": self.timestamp_utc,
            "timestamp_ist": self.timestamp_ist,
            "raw_image_sha256": self.raw_image_sha256,
            "raw_image_filename": self.raw_image_filename,
            "raw_image_size_bytes": self.raw_image_size_bytes,
            "derived_pdf_sha256": self.derived_pdf_sha256,
            "audit_chain_merkle_root": self.audit_chain_merkle_root,
            "ocr_observations_count": self.ocr_observations_count,
            "statutory_violations_detected": self.statutory_violations_detected,
            "overall_verdict": self.overall_verdict,
        }


class LegalAffidavitCompiler:
    """
    Compiles a formal, assistive draft Certificate of Electronic Record
    under Section 63 of Bharatiya Sakshya Adhiniyam, 2023.
    """

    def __init__(self, system_version: str = "1.0.0-SIH26034") -> None:
        self.system_version = system_version

    def generate_affidavit_pdf(
        self,
        evidence: ElectronicRecordEvidenceDetails,
        officer: CertifyingOfficerInfo,
    ) -> bytes:
        """
        Render the formal legal certificate as an unsigned draft PDF document.

        Args:
            evidence: Evidence details including SHA-256 hashes and inspection UUID.
            officer: Information on the certifying Legal Metrology Officer.

        Returns:
            PDF file bytes suitable for filing in judicial or compounding proceedings.
        """
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CertTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            alignment=1,  # Center
            textColor=colors.HexColor("#0B2545"),
        )
        subtitle_style = ParagraphStyle(
            "CertSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            alignment=1,
            textColor=colors.HexColor("#134074"),
        )
        legal_body = ParagraphStyle(
            "CertBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#1A1A1A"),
        )
        legal_bold = ParagraphStyle(
            "CertBodyBold",
            parent=legal_body,
            fontName="Helvetica-Bold",
        )
        table_cell = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#222222"),
        )
        table_cell_bold = ParagraphStyle(
            "TableCellBold",
            parent=table_cell,
            fontName="Helvetica-Bold",
        )

        story: List[Any] = [Paragraph(text(DRAFT_NOTICE), legal_body), Spacer(1, 8)]

        # 1. State Emblem & Court Header
        story.append(
            Paragraph("METROLENS — ASSISTIVE DRAFT FOR HUMAN REVIEW", subtitle_style)
        )
        story.append(Spacer(1, 3 * mm))
        story.append(
            Paragraph(
                "DRAFT ELECTRONIC RECORD SUMMARY FOR REVIEW UNDER SECTION 63(4)<br/>OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023<br/>(READ WITH SECTION 65B OF THE INDIAN EVIDENCE ACT, 1872)",
                title_style,
            )
        )
        story.append(Spacer(1, 2 * mm))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545")))
        story.append(Spacer(1, 4 * mm))

        # 2. Preamble
        preamble_text = (
            markup('<b>Supplied officer details (unverified):</b> {0}, {1}; jurisdiction {2}; office {3}. Identity, authority, and the underlying statements must be independently verified before any certification.', officer.officer_name, officer.designation, officer.jurisdiction_code, officer.station_address)
        )
        story.append(Paragraph(text(preamble_text), legal_body))
        story.append(Spacer(1, 4 * mm))

        # 3. Clause 1: Identification of Electronic Record
        clause_1 = (
            markup('<b>1. IDENTIFICATION OF THE ELECTRONIC RECORD:</b><br/>This draft summarizes supplied information about to the electronic record generated during an automated inspection of a pre-packaged commodity, assigned unique Inspection Docket Identifier <b>{0}</b>, captured on <b>{1}</b>.', evidence.inspection_id, evidence.timestamp_ist)
        )
        story.append(Paragraph(text(clause_1), legal_body))
        story.append(Spacer(1, 3 * mm))

        # Evidence Hash Table
        evidence_data = [
            [
                Paragraph("<b>Evidence Parameter</b>", table_cell_bold),
                Paragraph("<b>Cryptographic / Technical Value</b>", table_cell_bold),
            ],
            [
                Paragraph("Inspection Docket UUID", table_cell),
                Paragraph(text(markup('<code>{0}</code>', evidence.inspection_id)), table_cell),
            ],
            [
                Paragraph("Original Image Filename", table_cell),
                Paragraph(text(evidence.raw_image_filename), table_cell),
            ],
            [
                Paragraph("Input Image SHA-256 Digest", table_cell),
                Paragraph(text(markup('<code>{0}</code>', evidence.raw_image_sha256)), table_cell),
            ],
            [
                Paragraph("Original Payload Size", table_cell),
                Paragraph(text(markup('{0:,} bytes', evidence.raw_image_size_bytes)), table_cell),
            ],
            [
                Paragraph("Generated Assessment PDF Hash", table_cell),
                Paragraph(
                    text(markup('<code>{0}</code>', evidence.derived_pdf_sha256 or 'Not supplied')),
                    table_cell,
                ),
            ],
            [
                Paragraph("Audit Chain Merkle Root", table_cell),
                Paragraph(
                    text(markup('<code>{0}</code>', evidence.audit_chain_merkle_root or 'Not supplied')),
                    table_cell,
                ),
            ],
            [
                Paragraph("OCR Observations Extracted", table_cell),
                Paragraph(text(str(evidence.ocr_observations_count)), table_cell),
            ],
            [
                Paragraph("Statutory Violations Count", table_cell),
                Paragraph(text(str(evidence.statutory_violations_detected)), table_cell),
            ],
            [
                Paragraph("Supplied Assessment Result", table_cell),
                Paragraph(text(markup('<b>{0}</b>', evidence.overall_verdict)), table_cell),
            ],
        ]

        t_evidence = Table(evidence_data, colWidths=[55 * mm, 115 * mm])
        t_evidence.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF4F8")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0C4DE")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(t_evidence)
        story.append(Spacer(1, 4 * mm))

        # 4. Clause 2: System Architecture & Computer Operation Certification
        clause_2 = (
            markup('<b>2. SYSTEM INFORMATION:</b><br/>Prepared by MetroLens build {0}. This compiler does not attest to device operation, lawful custody, clock accuracy, or the absence of alterations.', self.system_version)
        )
        story.append(Paragraph(text(clause_2), legal_body))
        story.append(Spacer(1, 3 * mm))

        # 5. Clause 3: Truthfulness & Chain of Custody
        clause_3 = (
            markup('<b>3. HASH REFERENCES:</b><br/>The supplied digests identify byte sequences for comparison. A hash alone does not establish authenticity, ownership, an unbroken chain of custody, or a digital signature.')
        )
        story.append(Paragraph(text(clause_3), legal_body))
        story.append(Spacer(1, 3 * mm))

        # 6. Clause 4: Statutory Affirmation
        clause_4 = (
            markup('<b>4. REVIEW REQUIRED:</b><br/>This unsigned draft does not certify compliance with evidentiary requirements. A competent authorized person must verify the record and determine whether any certificate is appropriate.')
        )
        story.append(Paragraph(text(clause_4), legal_body))
        story.append(Spacer(1, 8 * mm))

        # 7. Signature Block
        sig_data = [
            [
                Paragraph(text(markup('{0}{1}', markup('<b>Draft generated:</b> '), datetime.datetime.now(datetime.timezone.utc).strftime('%d-%b-%Y %H:%M:%S UTC'))), legal_body),
                Paragraph("<b>SIGNATURE NOT VERIFIED:</b>", legal_body),
            ],
            [
                Paragraph(text(markup('<b>Place:</b> {0}, {1}', officer.district, officer.state)), legal_body),
                Paragraph("<br/><br/>________________________________________", legal_body),
            ],
            [
                Paragraph("<b>Official Seal / Stamp:</b>", legal_body),
                Paragraph(
                    text(markup('<b>{0}</b><br/>{1}<br/>Badge No: {2}<br/>Supplied region: {3}; identity and authority unverified', officer.officer_name, officer.designation, officer.badge_number, officer.state)),
                    legal_body,
                ),
            ],
        ]

        t_sig = Table(sig_data, colWidths=[85 * mm, 85 * mm])
        t_sig.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]
            )
        )
        story.append(KeepTogether(t_sig))

        doc.build(story)
        return pdf_buffer.getvalue()
