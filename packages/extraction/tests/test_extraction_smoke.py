"""
Smoke test for nirikshak-extraction.
"""

from nirikshak_extraction import DeclarationExtractor
from nirikshak_shared.models.contracts import OCRObservation
from nirikshak_shared.models.primitives import BoundingBox


def test_mrp_extraction_baseline():
    extractor = DeclarationExtractor()
    tokens = [
        OCRObservation(
            token_id="t1",
            text="MRP Rs. 149.00 (Incl. of all taxes)",
            confidence=0.95,
            bounding_box=BoundingBox(x_min=0, y_min=0, x_max=10, y_max=10),
        )
    ]
    res = extractor.extract_declarations(tokens)
    assert "mrp" in res
    assert res["mrp"].normalized_value["amount"] == 149.0
