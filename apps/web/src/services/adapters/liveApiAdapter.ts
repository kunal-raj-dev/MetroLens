import { resolveApiBaseUrl, apiHeaders } from "../apiConfig";
/**
 * MetroLens AIâ„¢ - Live API Inspection Adapter
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
    this.baseUrl = resolveApiBaseUrl(baseUrl);
  }

  async inspect(
    file: File,
    options?: InspectionOptions
  ): Promise<FrontendInspectionModel> {
    if (!this.baseUrl) throw new InspectionClientError("Live inspection is not configured for this deployment.", "NETWORK_ERROR");
    if (options?.signal?.aborted) throw new InspectionClientError("Inspection canceled.", "TIMEOUT");
    // 1. Client-side validation check
    const validation = await validateInspectionImage(file);
    if (!validation.valid && validation.error) {
      throw new InspectionClientError(
        validation.error.message,
        validation.error.type as any,
        { remediationHint: validation.error.details }
      );
    }
    if (options?.signal?.aborted) throw new InspectionClientError("Inspection canceled.", "TIMEOUT");
    const dims = validation.dimensions;
    if (dims && dims.width > 0 && (dims.width < 800 || dims.height < 600 || Math.max(dims.width, dims.height) > 8000 || dims.width * dims.height > 40_000_000)) {
      throw new InspectionClientError("Use an image at least 800 × 600 pixels, at most 8000 pixels per side and 40 megapixels.", "HTTP_422");
    }

    // 2. Prepare multipart request body (FastAPI expects 'file', legacy expects 'image')
    const formData = new FormData();
    formData.append("file", file, file.name);

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
        headers: apiHeaders(),
        body: formData,
        signal: controller.signal,
      });

      if (!response.ok) {
        let errorDetail = `Server returned HTTP ${response.status} ${response.statusText}`;
        try {
          const errJson = await response.json();
          if (errJson?.error?.message) errorDetail = errJson.error.message;
          if (errJson?.detail) {
            errorDetail =
              typeof errJson.detail === "string"
                ? errJson.detail
                : JSON.stringify(errJson.detail);
          }
        } catch {
          // Fall back to HTTP status message if JSON body cannot be parsed
        }

        if ([401, 403].includes(response.status)) throw new InspectionClientError("Service access was rejected. Check the access key supplied by the deployment owner.", "HTTP_400", {statusCode: response.status});
        if (response.status === 429) throw new InspectionClientError("The service is busy or the request limit was reached. Please wait and try again.", "HTTP_400", {statusCode: 429});
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

      if (controller.signal.aborted) throw new DOMException("Aborted", "AbortError");
      if (!payload || typeof payload.inspection_id !== "string" ||
          !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(payload.inspection_id) ||
          typeof payload.state !== "string" || !payload.state.trim() ||
          !/^[a-f0-9]{64}$/i.test(payload.image_metadata?.sha256_hash || "") ||
          !Number.isFinite(Date.parse(payload.timestamp))) {
        throw new InspectionClientError("The service returned an incomplete inspection. No result was accepted.", "INVALID_SERVER_RESPONSE");
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
            "The inspection service is unreachable. Try again later or explore the clearly labeled demonstration examples.",
        }
      );
    } finally {
      clearTimeout(timer);
      if (options?.signal) {
        options.signal.removeEventListener("abort", onCallerAbort);
      }
    }
  }

  async getHealth(): Promise<HealthCheckResult> {
    if (!this.baseUrl) return {status: "UNAVAILABLE", service: "MetroLens", version: "unknown", isLive: false, message: "Live inspection is not configured for this deployment."};
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 5000);

    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: "GET",
        headers: apiHeaders(),
        signal: controller.signal,
      });
      if (response.ok) {
        const data = await response.json();
        if (data.status !== "ok" || data.service !== "metrolens-api") throw new Error("Unexpected health response");
        return {
          status: "OK",
          service: data.service || "MetroLens Backend API",
          version: data.version || "0.1.0",
          isLive: true,
          message: "Inspection service is reachable. Access is checked when an image is submitted.",
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
      return {
        status: "UNAVAILABLE",
        service: "MetroLens Backend API",
        version: "n/a",
        isLive: false,
        message: `Backend unreachable at ${this.baseUrl} (${err.message})`,
      };
    } finally {
      clearTimeout(timer);
    }
  }

  async submitReview(
    input: ReviewSubmissionInput
  ): Promise<ReviewSubmissionResult> {
    throw new InspectionClientError(
      "Live officer review is not implemented. No review decision has been saved.",
      "REVIEW_API_NOT_IMPLEMENTED",
      { remediationHint: "Record your review through your approved inspection process." }
    );
  }
}
