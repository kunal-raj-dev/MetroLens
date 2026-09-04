# MetroLens Rule Engine Specification

## RULE ID: LMPC-R6-11-USP
**Legal Source:** Rule 6(11), introduced by G.S.R. 779(E), amended by G.S.R. 226(E).
**Applicable Category:** All retail packages unless exempted.
**Applicability Condition:** Net Quantity >= 10g or 10ml. MRP != USP.
**Required Input:**
- `mrp_value` (float)
- `net_quantity_value` (float)
- `net_quantity_unit` (enum: g, kg, ml, L, cm, m, pc)
- `declared_usp_value` (float)
- `declared_usp_unit` (string)
**Calculation:**
1. Determine legal denominator:
   - If weight < 1kg -> denominator = 1g
   - If weight >= 1kg -> denominator = 1kg
   - If volume < 1L -> denominator = 1ml
   - If volume >= 1L -> denominator = 1L
2. Normalize Qty to legal denominator. 
3. Expected USP = `round(mrp_value / normalized_qty, 2)`.
**Validation:** `abs(Expected USP - declared_usp_value) < 0.01` (to account for strict 2-decimal rounding parity).
**Result States:**
- `PASS`: Matches expected.
- `POTENTIAL_NON_COMPLIANCE`: Mismatch.
- `MANUAL_REVIEW`: Missing OCR data.
