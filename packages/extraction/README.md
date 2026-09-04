# Nirikshak Extraction Package (`nirikshak-extraction`)

## Purpose
Maps raw OCR text observations into canonical Rule 6 statutory declarations (MRP, net quantity, manufacturing date, expiry date, manufacturer identity/address, country of origin, consumer care coordinates).

## Owner
Extraction Lead

## Interface Seams
- **Input**: `List[OCRObservation]`.
- **Output**: `Dict[str, DeclarationField]`.
- **Error Codes**: `ERR_EXTRACTION_MISSING_MANDATORY`.
