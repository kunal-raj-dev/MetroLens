"""
Nirikshak Extraction: Parsing mandatory Legal Metrology Rule 6 declarations from OCR tokens.
"""

from typing import List, Dict
import re
from nirikshak_shared.models.contracts import OCRObservation, DeclarationField


class DeclarationExtractor:
    """Extracts statutory declaration entities from OCR observation tokens."""

    MANDATORY_FIELDS = [
        "mrp",
        "net_quantity",
        "mfg_date",
        "manufacturer_name",
        "country_of_origin",
        "consumer_care",
    ]

    def extract_declarations(self, observations: List[OCRObservation]) -> Dict[str, DeclarationField]:
        """
        Processes OCR tokens using regex patterns and heuristics to extract
        mandatory declaration fields.
        """
        extracted: Dict[str, DeclarationField] = {}
        full_text = " ".join(tok.text for tok in observations)

        # Baseline MRP extraction regex
        mrp_match = re.search(r"(?:MRP|M\.R\.P\.?|Rs\.?|₹)\s*(\d+(?:\.\d{2})?)", full_text, re.IGNORECASE)
        if mrp_match:
            val = float(mrp_match.group(1))
            extracted["mrp"] = DeclarationField(
                field_name="mrp",
                raw_text=mrp_match.group(0),
                normalized_value={"amount": val, "currency": "INR"},
                confidence=0.95,
                is_mandatory=True,
                is_present=True,
            )

        return extracted


__all__ = ["DeclarationExtractor", "DeclarationField"]
