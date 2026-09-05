# Legal Test Cases

## TC-USP-001 (NORMAL)
**Input:** MRP = Rs 100.00, Net Quantity = 500g, Unit = g
**Expected Result:** PASS (USP = Rs 0.20 per g)
**Legal Basis:** Rule 6(11) (G.S.R. 226(E))

## TC-USP-002 (VIOLATION)
**Input:** MRP = Rs 100.00, Net Quantity = 500g, Declared USP = Rs 0.25 per g
**Expected Result:** POTENTIAL_NON_COMPLIANCE
**Legal Basis:** Rule 6(11) (G.S.R. 226(E))

## TC-USP-003 (BOUNDARY)
**Input:** Net Quantity = 10g
**Expected Result:** PASS (Validly exempt from USP or validly matches calculation)
**Legal Basis:** Rule 6(11) exception for <10g.

## TC-USP-004 (EXCEPTION)
**Input:** Wholesale package
**Expected Result:** NOT_APPLICABLE
**Legal Basis:** Rule 24 / Rule 3

## TC-USP-005 (MANUAL REVIEW)
**Input:** OCR fails to extract MRP clearly.
**Expected Result:** MANUAL_REVIEW
**Legal Basis:** Legal Uncertainty Policy
