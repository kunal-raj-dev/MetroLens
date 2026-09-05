# CHUNK M5-5 CONTRACT AUDIT & INTERFACE DEFINITIONS
**Subsystem:** Member 5 (Web Frontend & User Experience)  
**Chunk:** M5-5 — Sample Package Workflow + Report/PDF Integration + Demo Mode  
**Date:** 2026-09-05  

---

## 1. Report Endpoint Contract Specification (`docs/API_CONTRACT.md` §3.3)
- **Method:** `POST`
- **Path:** `/api/v1/report/pdf`
- **Request Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "inspection_id": "INSP-20260905-8741",
    "officer_notes": "First inspection during wholesale market surveillance in Chandni Chowk.",
    "include_raw_image": true
  }
  ```
- **Response Headers (HTTP 200 OK):**
  - `Content-Type: application/pdf`
  - `Content-Disposition: attachment; filename="metrolens_report_{inspection_id}.pdf"`
- **Response Body:** Binary PDF stream (`%PDF-` magic header)

## 2. Review Submission Contract (`IInspectionClient.submitReview`)
- **Input:**
  ```typescript
  export interface ReviewSubmissionInput {
    inspectionId: string;
    fieldName: string;
    decision: "CONFIRMED" | "FLAGGED";
    notes?: string;
    caliperPoints?: {
      pointA: { x: number; y: number };
      pointB: { x: number; y: number };
      distancePixels: number;
    };
  }
  ```
- **Output:**
  ```typescript
  export interface ReviewSubmissionResult {
    success: boolean;
    isMock: boolean;
    statusMessage: string;
    fieldName: string;
    updatedReviewStatus: "CONFIRMED" | "FLAGGED";
    operatorNotes?: string | null;
    timestamp: string;
  }
  ```

## 3. Synthetic Fixtures Contract (`public/fixtures/manifest.json`)
- 8 Verified fixtures: `SYNTH-01` to `SYNTH-08`.
- Each fixture includes: `id`, `title`, `language`, `package_type`, `file_path`, `resolution`, `is_synthetic: true`, `disclaimer`, `ground_truth`.
- All marked with `isSynthetic = true` in normalized frontend model.
