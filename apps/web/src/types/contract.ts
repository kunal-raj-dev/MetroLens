/**
 * Direct TypeScript definitions mirroring backend Pydantic contracts
 * Source: packages/shared/src/nirikshak_shared/models/contracts.py & primitives.py
 */

export type CalibrationStatus = "CALIBRATED" | "UNCALIBRATED" | "APPROXIMATE_ASSISTED";

export type PanelName =
  | "PRINCIPAL_DISPLAY_PANEL"
  | "TOP"
  | "BOTTOM"
  | "LEFT"
  | "RIGHT"
  | "BACK"
  | "UNKNOWN";

export type RuleVerdict = "PASS" | "FAIL" | "REVIEW" | "NOT_APPLICABLE";

export type OverallVerdict =
  | "COMPLIANT"
  | "NON_COMPLIANT"
  | "SUSPECT_REVIEW"
  | "INCONCLUSIVE";

export type InspectionStatus =
  | "SUCCESS"
  | "REJECTED_QUALITY"
  | "FAILED_PROCESSING"
  | "NEEDS_HUMAN_REVIEW";

export interface BoundingBoxDTO {
  x_min: number;
  y_min: number;
  x_max: number;
  y_max: number;
}

export interface ObservedValueDTO {
  raw_text?: string | null;
  normalized_value?: string | number | boolean | null;
  measured_font_height_mm?: number | null;
  measured_pdp_area_cm2?: number | null;
  ocr_confidence?: number | null;
}

export interface OperatorAnnotationDTO {
  reviewed_by?: string | null;
  confirmed?: boolean | null;
  notes?: string | null;
}

export interface OCRObservationDTO {
  token_id: string;
  text: string;
  confidence: number;
  bounding_box: BoundingBoxDTO;
  polygon?: [number, number][] | null;
  language?: string | null;
}

export interface DeclarationFieldDTO {
  field_name: string;
  raw_text: string;
  normalized_value?: any;
  confidence: number;
  source_token_ids: string[];
  bounding_box?: BoundingBoxDTO | null;
  is_mandatory: boolean;
  is_present: boolean;
}

export interface MeasurementResultDTO {
  feature_name: string;
  measured_pixels: number;
  scale_factor_mm_per_pixel?: number | null;
  measured_mm?: number | null;
  uncertainty_mm?: number | null;
  calibration_status: CalibrationStatus;
  bounding_box?: BoundingBoxDTO | null;
}

export interface RuleEvaluationDTO {
  rule_id: string;
  rule_title: string;
  verdict: RuleVerdict;
  statutory_reference: string;
  observed_summary: string;
  required_summary: string;
  evidence_ids: string[];
  uncertainty_flag: boolean;
  evaluation_notes?: string | null;
}

export interface EvidenceItemDTO {
  evidence_id: string;
  image_sha256: string;
  panel_name: PanelName;
  bounding_box: BoundingBoxDTO;
  calibration_status: CalibrationStatus;
  physical_scale_mm_per_pixel?: number | null;
  observed_value: ObservedValueDTO;
  operator_annotation?: OperatorAnnotationDTO | null;
}

export interface InspectionErrorDTO {
  error_code: string;
  stage: string;
  message: string;
  remediation_hint?: string | null;
  is_fatal: boolean;
}

export interface BackendInspectionDTO {
  inspection_id: string;
  status: InspectionStatus;
  image_sha256: string;
  overall_verdict: OverallVerdict;
  quality_gate_passed: boolean;
  calibration_status: CalibrationStatus;
  declarations: Record<string, DeclarationFieldDTO>;
  measurements: Record<string, MeasurementResultDTO>;
  rule_evaluations: RuleEvaluationDTO[];
  evidence_chain: EvidenceItemDTO[];
  ocr_observations?: OCRObservationDTO[];
  errors: InspectionErrorDTO[];
  dossier_pdf_path?: string | null;
  telemetry: Record<string, number>;
  created_at: string;
}
