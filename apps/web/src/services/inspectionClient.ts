/**
 * MetroLens AI™ - Inspection Client Interface & Error Model
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Provides an authoritative abstraction separating UI components
 * from transport protocols, network calls, and backend architecture.
 */

import {
  FrontendInspectionModel,
  ReviewSubmissionInput,
  ReviewSubmissionResult,
} from "@/types/frontend";

export type InspectionClientErrorCode =
  | "FILE_INVALID"
  | "FILE_TOO_LARGE"
  | "UNSUPPORTED_TYPE"
  | "IMAGE_DECODE_FAILED"
  | "NETWORK_ERROR"
  | "TIMEOUT"
  | "HTTP_400"
  | "HTTP_422"
  | "HTTP_500"
  | "INVALID_SERVER_RESPONSE"
  | "REVIEW_API_NOT_IMPLEMENTED"
  | "UNKNOWN_ERROR";

export class InspectionClientError extends Error {
  readonly code: InspectionClientErrorCode;
  readonly statusCode?: number;
  readonly remediationHint?: string;

  constructor(
    message: string,
    code: InspectionClientErrorCode,
    options?: { statusCode?: number; remediationHint?: string }
  ) {
    super(message);
    this.name = "InspectionClientError";
    this.code = code;
    this.statusCode = options?.statusCode;
    this.remediationHint = options?.remediationHint;
    Object.setPrototypeOf(this, InspectionClientError.prototype);
  }
}

export interface InspectionOptions {
  officerId?: string;
  brandName?: string;
  productType?: string;
  signal?: AbortSignal;
  timeoutMs?: number;
}

export interface HealthCheckResult {
  status: "OK" | "UNAVAILABLE" | "DEGRADED";
  service: string;
  version: string;
  isLive: boolean;
  message?: string;
}

export interface IInspectionClient {
  readonly name: string;
  readonly isMock: boolean;

  /**
   * Submits a validated package photograph for statutory legal metrology inspection.
   */
  inspect(file: File, options?: InspectionOptions): Promise<FrontendInspectionModel>;

  /**
   * Probes backend health to determine whether live API connectivity is functional.
   */
  getHealth(): Promise<HealthCheckResult>;

  /**
   * Submits an inspector manual review decision (confirm or flag) with optional notes and reference points.
   */
  submitReview(input: ReviewSubmissionInput): Promise<ReviewSubmissionResult>;
}
