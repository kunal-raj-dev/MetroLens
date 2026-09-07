"""
Multi-Format Statutory Compliance Exporters
==========================================
Exports MetroLens inspection dossiers into machine-readable e-Governance
formats conforming to national data exchange standards:
    1. W3C JSON-LD (Linked Data for Semantic Web & Judicial Discovery)
    2. National Informatics Centre (NIC) Legal Metrology XML Schema
    3. Flat CSV Compliance Ledger Row (for District & State Aggregation)
"""

from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from xml.dom import minidom


class ComplianceDossierExporter:
    """
    Serializes inspection assessments into JSON-LD, XML, and CSV.
    """

    @classmethod
    def to_json_ld(cls, dossier_data: Dict[str, Any]) -> str:
        """
        Export dossier findings as W3C JSON-LD.
        """
        json_ld: Dict[str, Any] = {
            "@context": {
                "schema": "http://schema.org/",
                "metrology": "https://consumeraffairs.nic.in/legal-metrology/schema/v1#",
                "inspectionId": "metrology:inspectionId",
                "timestamp": "schema:dateCreated",
                "overallVerdict": "metrology:complianceVerdict",
                "statutoryRule": "metrology:statutoryRule",
                "declarations": "metrology:mandatoryDeclarations",
                "improvementNotice": "metrology:improvementNotice",
            },
            "@type": "metrology:LegalMetrologyAssessmentReport",
            "@id": f"urn:metrolens:inspection:{dossier_data.get('inspection_id')}",
            "inspectionId": dossier_data.get("inspection_id"),
            "timestamp": dossier_data.get("timestamp_ist"),
            "overallVerdict": dossier_data.get("overall_verdict"),
            "evidence": {
                "rawImageSha256": dossier_data.get("raw_image_sha256"),
                "pdpAreaSqcm": dossier_data.get("pdp_area_sqcm"),
                "calibrationScale": dossier_data.get("metric_scale_mm_per_px"),
            },
            "declarations": dossier_data.get("declarations_table", []),
            "improvementNotice": dossier_data.get("improvement_notice_details"),
            "certifyingAuthority": {
                "officerName": dossier_data.get("inspector_name"),
                "badgeNumber": dossier_data.get("badge_number"),
                "jurisdiction": f"{dossier_data.get('district')}, {dossier_data.get('state')}",
            },
        }

        return json.dumps(json_ld, indent=2, ensure_ascii=False)

    @classmethod
    def to_nic_xml(cls, dossier_data: Dict[str, Any]) -> str:
        """
        Export dossier findings as National Informatics Centre (NIC) Legal Metrology XML.
        """
        root = ET.Element("MetroLensInspectionDocket", attrib={"version": "1.0", "xmlns": "http://nic.in/metrolens"})

        # Header
        header = ET.SubElement(root, "DocketHeader")
        ET.SubElement(header, "InspectionUUID").text = str(dossier_data.get("inspection_id", ""))
        ET.SubElement(header, "TimestampIST").text = str(dossier_data.get("timestamp_ist", ""))
        ET.SubElement(header, "OverallVerdict").text = str(dossier_data.get("overall_verdict", ""))
        ET.SubElement(header, "RawImageSHA256").text = str(dossier_data.get("raw_image_sha256", ""))

        # Officer
        officer = ET.SubElement(root, "CertifyingOfficer")
        ET.SubElement(officer, "Name").text = str(dossier_data.get("inspector_name", ""))
        ET.SubElement(officer, "BadgeNumber").text = str(dossier_data.get("badge_number", ""))
        ET.SubElement(officer, "District").text = str(dossier_data.get("district", ""))
        ET.SubElement(officer, "State").text = str(dossier_data.get("state", ""))

        # Declarations
        decls = ET.SubElement(root, "MandatoryDeclarations")
        for item in dossier_data.get("declarations_table", []):
            d_el = ET.SubElement(decls, "Declaration")
            ET.SubElement(d_el, "TermKey").text = str(item.get("term_key", ""))
            ET.SubElement(d_el, "Citation").text = str(item.get("citation", ""))
            ET.SubElement(d_el, "DeclaredValue").text = str(item.get("declared_value", ""))
            ET.SubElement(d_el, "IsCompliant").text = str(item.get("is_compliant", False)).lower()
            if item.get("specific_defect"):
                ET.SubElement(d_el, "DefectReason").text = str(item.get("specific_defect"))

        # Improvement Notice
        in_data = dossier_data.get("improvement_notice_details")
        if in_data:
            in_el = ET.SubElement(root, "Section36ImprovementNotice")
            ET.SubElement(in_el, "NoticeRequired").text = "true"
            ET.SubElement(in_el, "CurePeriodDays").text = str(in_data.get("cure_period_days", 15))
            ET.SubElement(in_el, "NoticeReference").text = str(in_data.get("notice_reference", ""))
            ET.SubElement(in_el, "ComplianceDeadline").text = str(in_data.get("compliance_deadline", ""))

        xml_str = ET.tostring(root, encoding="utf-8")
        parsed = minidom.parseString(xml_str)
        return parsed.toprettyxml(indent="  ")

    @classmethod
    def to_csv_ledger_row(cls, dossier_data: Dict[str, Any]) -> str:
        """
        Format a single CSV compliance ledger line.
        """
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")

        decls = dossier_data.get("declarations_table", [])
        fail_count = sum(1 for d in decls if not d.get("is_compliant", False))

        row = [
            dossier_data.get("inspection_id", ""),
            dossier_data.get("timestamp_ist", ""),
            dossier_data.get("district", ""),
            dossier_data.get("state", ""),
            dossier_data.get("inspector_name", ""),
            dossier_data.get("badge_number", ""),
            dossier_data.get("commodity_category", "FMCG"),
            dossier_data.get("overall_verdict", ""),
            fail_count,
            dossier_data.get("raw_image_sha256", "")[:16],
            dossier_data.get("metric_scale_mm_per_px", ""),
        ]
        writer.writerow(row)
        return out.getvalue()
