"""
Nirikshak Reporting: Inspection Dossier generation and ReportLab PDF renderer.
"""

import io
from typing import Dict, Any
from nirikshak_shared.models.contracts import InspectionResult


class DossierGenerator:
    """Renders standardized inspection dossiers into PDF and structured JSON formats."""

    def generate_json_summary(self, result: InspectionResult) -> Dict[str, Any]:
        """Exports the immutable inspection result into a standardized summary dictionary."""
        return result.model_dump(mode="json", exclude_none=True)

    def generate_pdf_bytes(self, result: InspectionResult) -> bytes:
        """
        Generates a basic PDF dossier using ReportLab or fallback binary format.
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, f"NIRIKSHAK LEGAL METROLOGY INSPECTION DOSSIER")
            c.drawString(100, 730, f"Inspection ID: {result.inspection_id}")
            c.drawString(100, 710, f"Overall Verdict: {result.overall_verdict.value}")
            c.drawString(100, 690, f"Image SHA-256: {result.image_sha256[:16]}...{result.image_sha256[-16:]}")
            c.drawString(100, 670, f"Evaluations Count: {len(result.rule_evaluations)}")
            c.showPage()
            c.save()
            return buffer.getvalue()
        except ImportError:
            # Fallback text representation if reportlab is not installed
            return f"NIRIKSHAK DOSSIER: {result.inspection_id} - {result.overall_verdict.value}".encode("utf-8")


__all__ = ["DossierGenerator"]
