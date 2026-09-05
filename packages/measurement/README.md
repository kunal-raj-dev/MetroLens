# Nirikshak Measurement Package (`nirikshak-measurement`)

## Purpose
Computes physical metrological measurements in millimeters and square centimeters:
- Font numeral height ($H_{\text{font}} = H_{\text{pixel}} \times S$)
- Principal Display Panel area ($A_{\text{pdp}}$ in $\text{cm}^2$)
- Minimum height threshold lookups against Schedule II of the Legal Metrology (Packaged Commodities) Rules, 2011.

## Owner
Metrology Lead

## Interface Seams
- **Input**: Pixel bounding boxes, calibration scale factor $S$.
- **Output**: `Dict[str, MeasurementResult]`.
- **Error Codes**: `ERR_MEASUREMENT_UNCALIBRATED`.
