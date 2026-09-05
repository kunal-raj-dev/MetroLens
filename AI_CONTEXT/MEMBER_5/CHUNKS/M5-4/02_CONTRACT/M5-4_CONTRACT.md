# METROLENS AI — MEMBER 5 (CHUNK M5-4)
## Contract Seam & Review DTO Specification

### 1. Architectural Boundaries & Non-Invention Policy
Under the MetroLens AI architectural doctrine:
1. **Zero Client-Side Legal Logic**: The frontend performs zero threshold comparisons, zero penalty calculations, and zero verdict derivations. All rule decisions (`PASS`, `FAIL`, `INCONCLUSIVE`) originate from the backend deterministic rule engine.
2. **Zero Client-Side Physical Metric Calculations**: No millimeter math, font height conversions, or physical homography projections occur in the browser. Only optical pixel distances on the unscaled image coordinate system are tracked for human inspection reference.
3. **No Contract Invention**: The frontend consumes strictly defined schemas from Member 3 (DTOs) and Member 4 (FastAPI routes).

### 2. Declaration Model Normalization
Backend DTO (`RuleEvaluation` / `InspectionResponse`) maps cleanly to `DeclarationModel`:

```typescript
export interface DeclarationModel {
  fieldName: string;
  fieldLabel: string;
  isMandatory: boolean;
  rawText: string;
  normalizedValue: Record<string, any> | string | number | null;
  status: StatutoryVerdict;
  confidence: number;
  measuredHeightMm: number | null;
  minimumRequiredHeightMm: number | null;
  isHeightCompliant: boolean | null;
  sourceTokenIds: string[];
  evaluationNotes?: string | null;
  reviewStatus?: "PENDING" | "CONFIRMED" | "FLAGGED";
  operatorNotes?: string | null;
  ruleTitle?: string | null;
  statutoryReference?: string | null;
  requiredSummary?: string | null;
}
```

### 3. Review Submission Seam (`submitReview`)
Because Member 4 backend `/api/v1/inspections/{id}/review` is pending, Member 5 established a clear interface boundary:

```typescript
export type ReviewDecision = "CONFIRMED" | "FLAGGED";

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
  inspectionId: string;
  fieldName: string;
  updatedReviewStatus: "CONFIRMED" | "FLAGGED";
  operatorNotes?: string;
  submittedAt: string;
  isSynthetic: boolean;
}
```

### 4. Adapter Behaviors
- **MockInspectionAdapter (`mockAdapter.ts`)**: Simulates review dispatch with offline audit persistence labeled `SYNTHETIC DEMO`. Enforces max 500 characters on notes.
- **LiveApiAdapter (`liveApiAdapter.ts`)**: Recognizes that the backend endpoint is not yet implemented by Member 4. Raises `InspectionClientError` with code `REVIEW_API_NOT_IMPLEMENTED` and remediation hint directing alignment with Member 4 FastAPI roadmap. Does NOT invent fake HTTP requests.
