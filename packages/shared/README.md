# Nirikshak Shared Package (`nirikshak-shared`)

## Purpose
Provides the frozen, canonical data contracts, domain primitives, and serialization models that define the seams between all subsystems of the Nirikshak automated legal metrology inspection platform.

## Key Exports
- `nirikshak_shared.models.primitives`: `BoundingBox`, `CalibrationStatus`, `PanelName`, `RuleVerdict`, `OverallVerdict`, `InspectionStatus`
- `nirikshak_shared.models.contracts`:
  - `InspectionRequest`
  - `InspectionResult`
  - `OCRObservation`
  - `DeclarationField`
  - `MeasurementResult`
  - `RuleEvaluation`
  - `EvidenceItem`
  - `InspectionError`
