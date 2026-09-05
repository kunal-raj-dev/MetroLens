/**
 * MetroLens AI™ - Live API Inspection Adapter
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Implements IInspectionClient targeting Member 4's FastAPI backend:
 * POST /api/v1/inspect (multipart/form-data)
 */

import {
  IInspectionClient,
  InspectionOptions,
  HealthCheckResult,
  InspectionClientError,
} from "../inspectionClient";
import {
  FrontendInspectionModel,
  ReviewSubmissionInput,
  ReviewSubmissionResult,
} from "@/types/frontend";
import { normalizeInspectionResponse } from "./responseNormalizer";
import { validateInspectionImage } from "@/utils/validation";

export class LiveApiAdapter implements IInspectionClient {
  readonly name = "LiveFastApiInspectionAdapter";
  readonly isMock = false;

  private readonly baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl =
      baseUrl ||
      process.env.NEXT_PUBLIC_API_URL ||
      "http://localhost:8000";
  }

  async inspect(
    file: File,
    options?: InspectionOptions
  ): Promise<FrontendInspectionModel> {
    // 1. Client-side validation check
    const validation = await validateInspectionImage(file);
    if (!validation.valid && validation.error) {
      throw new InspectionClientError(
        validation.error.message,
        validation.error.type as any,
        { remediationHint: validation.error.details }
      );
    }

    // 2. Prepare multipart request body (FastAPI expects 'file', legacy expects 'image')
    const formData = new FormData();
    formData.append("file", file, file.name);
    formData.append("image", file, file.name);

    if (options?.officerId) {
      formData.append("officer_id", options.officerId);
    }
    if (options?.brandName) {
      formData.append("brand_name", options.brandName);
    }
    if (options?.productType) {
      formData.append("product_type", options.productType);
    }

    // 3. Setup timeout controller
    const timeoutMs = options?.timeoutMs || 30000;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    const onCallerAbort = () => controller.abort();
    if (options?.signal) {
      options.signal.addEventListener("abort", onCallerAbort);
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/v1/inspect`, {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (!response.ok) {
        let errorDetail = `Server returned HTTP ${response.status} ${response.statusText}`;
        try {
          const errJson = await response.json();
          if (errJson?.detail) {
            errorDetail =
              typeof errJson.detail === "string"
                ? errJson.detail
                : JSON.stringify(errJson.detail);
          }
        } catch {
          // Fall back to HTTP status message if JSON body cannot be parsed
        }

        if (response.status === 400) {
          throw new InspectionClientError(
            `Inspection rejected by server: ${errorDetail}`,
            "HTTP_400",
            {
              statusCode: 400,
              remediationHint: "Check that image is a valid, uncorrupted front-panel packaging frame.",
            }
          );
        } else if (response.status === 422) {
          throw new InspectionClientError(
            `Invalid inspection parameters: ${errorDetail}`,
            "HTTP_422",
            {
              statusCode: 422,
              remediationHint: "Verify file parameters conform to OpenAPI contract.",
            }
          );
        } else if (response.status >= 500) {
          throw new InspectionClientError(
            `Statutory inspection pipeline failed: ${errorDetail}`,
            "HTTP_500",
            {
              statusCode: response.status,
              remediationHint: "The backend server encountered an error during inference or rule execution.",
            }
          );
        }

        throw new InspectionClientError(errorDetail, "UNKNOWN_ERROR", {
          statusCode: response.status,
        });
      }

      let payload: any;
      try {
        payload = await response.json();
      } catch (err: any) {
        throw new InspectionClientError(
          "Inspection server returned non-JSON response payload.",
          "INVALID_SERVER_RESPONSE",
          { remediationHint: err?.message }
        );
      }

      return normalizeInspectionResponse(payload, { isSynthetic: false });
    } catch (err: any) {
      clearTimeout(timer);

      if (err instanceof InspectionClientError) {
        throw err;
      }

      if (err.name === "AbortError") {
        throw new InspectionClientError(
          `Inspection timed out after ${timeoutMs / 1000}s without a response.`,
          "TIMEOUT",
          { remediationHint: "Ensure the backend pipeline and OCR models are responsive." }
        );
      }

      // Network unreachable or connection refused
      throw new InspectionClientError(
        `Unable to reach inspection server at ${this.baseUrl}.`,
        "NETWORK_ERROR",
        {
          remediationHint:
            "Member 4 backend is not running or network connection failed. You may switch to Mock Synthetic Mode for demonstration.",
        }
      );
    } finally {
      if (options?.signal) {
        options.signal.removeEventListener("abort", onCallerAbort);
      }
    }
  }

  async getHealth(): Promise<HealthCheckResult> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 2500);

    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: "GET",
        signal: controller.signal,
      });
      clearTimeout(timer);

      if (response.ok) {
        const data = await response.json().catch(() => ({}));
        return {
          status: "OK",
          service: data.service || "MetroLens Backend API",
          version: data.version || "0.1.0",
          isLive: true,
          message: "Connected to live FastAPI backend.",
        };
      }

      return {
        status: "DEGRADED",
        service: "MetroLens Backend API",
        version: "unknown",
        isLive: false,
        message: `HTTP ${response.status} from backend health check.`,
      };
    } catch (err: any) {
      clearTimeout(timer);
      return {
        status: "UNAVAILABLE",
        service: "MetroLens Backend API",
        version: "n/a",
        isLive: false,
        message: `Backend unreachable at ${this.baseUrl} (${err.message})`,
      };
    }
  }

  async submitReview(
    input: ReviewSubmissionInput
  ): Promise<ReviewSubmissionResult> {
    // Check if backend review route exists or is pending Member 4
    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/inspections/${encodeURIComponent(input.inspectionId)}/review`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(input),
        }
      );

      if (response.status === 404 || response.status === 405) {
        throw new InspectionClientError(
          "Review API pending Member 4 backend deployment. The review submission route is not yet hosted.",
          "REVIEW_API_NOT_IMPLEMENTED",
          {
            statusCode: response.status,
            remediationHint:
              "Backend Member 4 has not yet exposed /api/v1/inspections/{id}/review. Switch to Mock Synthetic Mode to test the review workflow.",
          }
        );
      }

      if (!response.ok) {
        throw new InspectionClientError(
          `Review submission rejected: HTTP ${response.status}`,
          "HTTP_500",
          { statusCode: response.status }
        );
      }

      const resJson = await response.json();
      return {
        success: true,
        isMock: false,
        fieldName: input.fieldName,
        updatedReviewStatus: input.decision,
        operatorNotes: input.notes || null,
        statusMessage:
          resJson.message ||
          `Review decision submitted successfully to backend.`,
        timestamp: resJson.timestamp || new Date().toISOString(),
      };
    } catch (err: any) {
      if (err instanceof InspectionClientError) throw err;

      // Unreachable or connection refused
      throw new InspectionClientError(
        "Live Review API unreachable or pending Member 4 backend deployment.",
        "REVIEW_API_NOT_IMPLEMENTED",
        {
          remediationHint:
            "Member 4 backend does not support review endpoints yet. Use Mock Synthetic Mode for demonstration.",
        }
      );
    }
  }
}
