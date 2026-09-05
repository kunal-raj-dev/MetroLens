import { OverallVerdict, CalibrationStatus, RuleVerdict } from "./contract";

export type SemanticStatus =
  | "SUCCESS"
  | "NON_COMPLIANT"
  | "REVIEW"
  | "INCONCLUSIVE"
  | "NEUTRAL"
  | "INFO"
  | "ERROR";

export interface SemanticVerdictConfig {
  verdict: OverallVerdict;
  label: string;
  sublabel: string;
  explanation: string;
  accentColor: string;
  borderColor: string;
  bgColor: string;
  textColor: string;
  iconName: "ShieldCheck" | "AlertTriangle" | "HelpCircle" | "FileQuestion";
}

export interface BoundingBoxModel {
  xMin: number;
  yMin: number;
  xMax: number;
  yMax: number;
  width?: number;
  height?: number;
}

export interface OCRTokenModel {
  id: string; // canonical token_id
  text: string;
  confidence: number;
  boundingBox: BoundingBoxModel;
  polygon: [number, number][]; // 4-point clockwise vertices in original input image pixel space
  language?: string | null;
  script?: string | null; // e.g. "devanagari", "latin"
  fieldName?: string | null; // mapped declaration field key if matched
  requiresReview?: boolean;
}

export interface DeclarationModel {
  fieldName: string;
  label: string;
  rawText: string;
  normalizedValue?: any;
  confidence: number;
  isMandatory: boolean;
  isPresent: boolean;
  boundingBox?: BoundingBoxModel | null;
  polygon?: [number, number][] | null;
  measuredHeightMm?: number | null;
  statutoryMinimumMm?: number | null;
  verdict?: RuleVerdict;
  evaluationNotes?: string | null;
  ruleTitle?: string | null;
  statutoryReference?: string | null;
  requiredSummary?: string | null;
  sourceTokenIds?: string[];
  reviewStatus?: "NOT_REVIEWED" | "IN_REVIEW" | "CONFIRMED" | "FLAGGED" | "NOT_REQUIRED";
  operatorNotes?: string | null;
}

export type ReviewDecision = "CONFIRMED" | "FLAGGED";

export interface CaliperPoint {
  x: number;
  y: number;
}

export interface ReviewSubmissionInput {
  inspectionId: string;
  fieldName: string;
  decision: ReviewDecision;
  notes?: string;
  caliperPoints?: {
    pointA: CaliperPoint;
    pointB: CaliperPoint;
    distancePixels: number;
  };
}

export interface ReviewSubmissionResult {
  success: boolean;
  isMock: boolean;
  statusMessage: string;
  fieldName: string;
  updatedReviewStatus: "CONFIRMED" | "FLAGGED";
  operatorNotes?: string | null;
  timestamp: string;
}

export interface FrontendInspectionModel {
  inspectionId: string;
  createdAt: string;
  imageSha256: string;
  imagePath?: string | null;
  isSynthetic: boolean;
  syntheticDisclaimer?: string;
  packageTitle?: string;
  pdfUrl?: string | null;
  verdict: {
    status: OverallVerdict;
    label: string;
    summaryReason: string;
    isCompliant: boolean;
    requiresReview: boolean;
  };
  qualityGate: {
    passed: boolean;
    sharpnessScore?: number;
    glareRatio?: number;
  };
  calibration: {
    status: CalibrationStatus;
    scaleFactorMmPerPixel?: number | null;
    isCalibrated: boolean;
  };
  declarations: Record<string, DeclarationModel>;
  ocrTokens: OCRTokenModel[];
  evidenceItems: Array<{
    id: string;
    fieldName: string;
    boundingBox: BoundingBoxModel;
    observedValue?: string | null;
    confidence?: number | null;
  }>;
  telemetry: {
    totalDurationMs: number;
    stageTimings: Record<string, number>;
  };
  errors: Array<{
    code: string;
    stage: string;
    message: string;
    remediationHint?: string | null;
  }>;
}
