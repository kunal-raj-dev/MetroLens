# MEMBER 5: MONOREPO SEAM CONTRACTS & SCHEMA MAPPING
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Document Status:** Technical Interface Mapping Reference  

---

## 1. Upstream Monorepo Seam Mappings

| Upstream Subsystem | Owner | Source Package / Code | Key Outputs Delivered to Frontend | Frontend Handling Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **OCR & Geometry** | **Member 1 (FROZEN)** | `packages/ocr` (`OCRToken`, `OCRObservation`) | • Original image pixel bounding box: `[xmin, ymin, xmax, ymax]`<br>• Clockwise 4-point polygon: `[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]`<br>• Text string & OCR confidence score<br>• Script category: `latin` vs `devanagari` | **Zero Coordinate Mutation:** Render directly via canvas affine transform. Retain raw coordinates for inspector crop zoom. |
| **Calibration & Scale** | **Member 2** | `packages/calibration` (`MeasurementResult`) | • `scale_factor_mm_per_pixel` ($S$)<br>• `calibration_status`: `CALIBRATED`, `UNCALIBRATED`<br>• `measured_mm`, `uncertainty_mm` | Display calibration state badge. If `UNCALIBRATED`, show "Uncalibrated Frame" warning and enable manual 2-point caliper tool. |
| **Rules & Adjudication** | **Member 3** | `packages/rules-engine` (`RuleEvaluation`, `OverallVerdict`) | • `overall_verdict`: `COMPLIANT`, `NON_COMPLIANT`, `SUSPECT_REVIEW`, `INCONCLUSIVE`<br>• List of `RuleEvaluation` items (verdict, statutory reference, required summary, observed summary) | Map directly into `ComplianceDashboard` multi-modal banner and line-item declaration rows in `DeclarationTable`. |
| **API Gateway & Worker** | **Member 4** | `apps/api/main.py`, `apps/worker/main.py` | • Endpoint: `POST /api/v1/inspect`<br>• Consumes: `multipart/form-data` (`file`, `anchor_type`, `officer_id`)<br>• Produces: `InspectionResult` Pydantic DTO | Consume via `LiveApiAdapter`. Pass through `responseNormalizer` to insulate UI components from backend schema changes. |

---

## 2. Backend DTO (`InspectionResult`) vs Frontend Model (`FrontendInspectionModel`)

### A. Live Backend Contract (`packages/shared/.../contracts.py`)
```python
class InspectionResult(BaseModel):
    inspection_id: str
    status: InspectionStatus                      # SUCCESS, REJECTED_QUALITY, FAILED_PROCESSING, NEEDS_HUMAN_REVIEW
    image_sha256: str                             # 64-char hex hash
    overall_verdict: OverallVerdict               # COMPLIANT, NON_COMPLIANT, SUSPECT_REVIEW, INCONCLUSIVE
    quality_gate_passed: bool
    calibration_status: CalibrationStatus         # CALIBRATED, UNCALIBRATED, APPROXIMATE_ASSISTED
    declarations: Dict[str, DeclarationField]     # mrp, net_quantity, mfg_date, etc.
    measurements: Dict[str, MeasurementResult]    # net_quantity_font_height
    rule_evaluations: List[RuleEvaluation]        # List of individual rule checks
    evidence_chain: List[EvidenceItem]            # SHA-256 linked evidence nodes
    errors: List[InspectionError]
    dossier_pdf_path: Optional[str]
    telemetry: Dict[str, float]                   # stage latencies in ms
    created_at: datetime
```

### B. Normalized Frontend Inspection Model (`apps/web/src/types/inspection.ts`)
```typescript
export interface FrontendInspectionModel {
  inspectionId: string;
  createdAt: string;
  verdict: {
    status: "COMPLIANT" | "NON_COMPLIANT" | "SUSPECT_REVIEW" | "INCONCLUSIVE";
    badgeText: string;
    summaryReason: string;
    statutoryNoticeRequired: boolean;
  };
  qualityGate: {
    passed: boolean;
    sharpnessScore?: number;
    glareRatio?: number;
  };
  calibration: {
    status: "CALIBRATED" | "UNCALIBRATED" | "APPROXIMATE_ASSISTED";
    scaleFactorMmPerPx?: number;
    anchorTarget?: string;
  };
  declarations: Record<string, {
    fieldName: string;
    rawText: string;
    normalizedValue?: any;
    confidence: number;
    isMandatory: boolean;
    isPresent: boolean;
    boundingBox?: { xMin: number; yMin: number; xMax: number; yMax: number };
    polygon?: [number, number][];
    measuredHeightMm?: number;
    statutoryMinimumMm?: number;
    evaluationVerdict?: "PASS" | "FAIL" | "REVIEW" | "NOT_APPLICABLE";
    evaluationNotes?: string;
  }>;
  evidenceItems: Array<{
    id: string;
    fieldName: string;
    boundingBox: { xMin: number; yMin: number; xMax: number; yMax: number };
    observedValueText?: string;
    confidence?: number;
  }>;
  telemetry: {
    totalDurationMs: number;
    stages: Record<string, number>;
  };
  errors: Array<{
    code: string;
    message: string;
    remediation?: string;
  }>;
}
```

---

## 3. InspectionClient Adapter Architecture
```typescript
// apps/web/src/services/inspectionClient.ts

export interface IInspectionClient {
  inspect(imageFile: File, options?: InspectionOptions): Promise<FrontendInspectionModel>;
  getHealth(): Promise<HealthStatus>;
  submitManualScaleOverride(override: CaliperOverridePayload): Promise<FrontendInspectionModel>;
}

export class InspectionClient implements IInspectionClient {
  private adapter: IInspectionClient;

  constructor(mode: "live" | "mock" = process.env.NEXT_PUBLIC_API_MODE === "live" ? "live" : "mock") {
    this.adapter = mode === "live" ? new LiveInspectionAdapter() : new MockInspectionAdapter();
  }

  async inspect(imageFile: File, options?: InspectionOptions) {
    return this.adapter.inspect(imageFile, options);
  }

  async getHealth() {
    return this.adapter.getHealth();
  }

  async submitManualScaleOverride(override: CaliperOverridePayload) {
    return this.adapter.submitManualScaleOverride(override);
  }
}
```
This architecture guarantees that UI development proceeds without interruption while the backend components stabilize.
