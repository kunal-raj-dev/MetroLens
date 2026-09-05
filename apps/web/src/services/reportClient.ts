/**
 * MetroLens AI™ - Report Client Interface & Implementation
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Provides an authoritative, tamper-evident assessment report retrieval
 * and download client targeting Member 4's FastAPI report endpoint:
 * POST /api/v1/report/pdf
 * 
 * INVIOLABLE PRINCIPLES:
 * 1. The frontend NEVER generates legal conclusions for the PDF.
 * 2. If the backend report endpoint is offline or unavailable, NO FAKE PDF is fabricated.
 * 3. All object URLs are explicitly revoked to prevent memory leaks.
 * 4. Stale report protection guarantees Report A never attaches to Inspection B.
 */

export type ReportStatus =
  | "IDLE"
  | "GENERATING"
  | "READY"
  | "UNAVAILABLE"
  | "ERROR";

export type ReportClientErrorCode =
  | "INVALID_INSPECTION_ID"
  | "ALREADY_GENERATING"
  | "ENDPOINT_UNAVAILABLE"
  | "NETWORK_ERROR"
  | "TIMEOUT"
  | "HTTP_400"
  | "HTTP_404"
  | "HTTP_422"
  | "HTTP_500"
  | "INVALID_CONTENT_TYPE"
  | "EMPTY_PAYLOAD"
  | "INVALID_PDF_SIGNATURE"
  | "CANCELED"
  | "UNKNOWN_ERROR";

export class ReportClientError extends Error {
  readonly code: ReportClientErrorCode;
  readonly statusCode?: number;
  readonly remediationHint?: string;

  constructor(
    message: string,
    code: ReportClientErrorCode,
    options?: { statusCode?: number; remediationHint?: string }
  ) {
    super(message);
    this.name = "ReportClientError";
    this.code = code;
    this.statusCode = options?.statusCode;
    this.remediationHint = options?.remediationHint;
    Object.setPrototypeOf(this, ReportClientError.prototype);
  }
}

export interface GenerateReportOptions {
  officerNotes?: string;
  includeRawImage?: boolean;
  signal?: AbortSignal;
  timeoutMs?: number;
}

export interface ReportDownloadResult {
  success: boolean;
  inspectionId: string;
  filename: string;
  byteSize: number;
  isSynthetic: boolean;
  downloadTriggered: boolean;
}

export interface IReportClient {
  /**
   * Generates and triggers the browser download of the official assessment report PDF.
   * Throws ReportClientError if the backend is unavailable or the response is invalid.
   */
  downloadAssessmentReport(
    inspectionId: string,
    options?: GenerateReportOptions
  ): Promise<ReportDownloadResult>;

  /**
   * Validates whether a given ArrayBuffer contains a valid %PDF- binary header.
   */
  validatePdfHeader(buffer: ArrayBuffer): boolean;

  /**
   * Sanitizes filenames to prevent path traversal or unsafe download strings.
   */
  sanitizeFilename(rawName: string, fallbackId: string): string;
}

export class ReportClient implements IReportClient {
  private readonly baseUrl: string;
  private activeInspectionId: string | null = null;
  private isGenerating = false;

  constructor(baseUrl?: string) {
    this.baseUrl =
      baseUrl ||
      process.env.NEXT_PUBLIC_API_URL ||
      "http://localhost:8000";
  }

  /**
   * Validates binary PDF magic bytes: %PDF- (0x25 0x50 0x44 0x46 0x2D)
   */
  validatePdfHeader(buffer: ArrayBuffer): boolean {
    if (!buffer || buffer.byteLength < 5) return false;
    const view = new Uint8Array(buffer, 0, 5);
    // ASCII codes for % P D F -
    return (
      view[0] === 0x25 && // %
      view[1] === 0x50 && // P
      view[2] === 0x44 && // D
      view[3] === 0x46 && // F
      view[4] === 0x2d    // -
    );
  }

  /**
   * Extracts or generates a safe, clean filename for download
   */
  sanitizeFilename(rawName: string, fallbackId: string): string {
    const cleanId = fallbackId.replace(/[^a-zA-Z0-9_-]/g, "_");
    if (!rawName) return `metrolens-inspection-${cleanId}.pdf`;

    // Remove path traversal and unsafe characters
    const safe = rawName
      .replace(/^.*[\\/]/, "")
      .replace(/[^a-zA-Z0-9._-]/g, "_");

    return safe.endsWith(".pdf") ? safe : `${safe}.pdf`;
  }

  /**
   * Extracts filename from Content-Disposition header if available
   */
  private extractFilenameFromHeader(header: string | null, fallbackId: string): string {
    if (!header) return this.sanitizeFilename("", fallbackId);
    const match = header.match(/filename\*?=(?:UTF-8'')?"?([^";]+)"?/i);
    const raw = match ? match[1] : "";
    return this.sanitizeFilename(decodeURIComponent(raw), fallbackId);
  }

  /**
   * Requests PDF stream from backend, validates payload, and executes safe browser download.
   */
  async downloadAssessmentReport(
    inspectionId: string,
    options?: GenerateReportOptions
  ): Promise<ReportDownloadResult> {
    if (!inspectionId || !inspectionId.trim()) {
      throw new ReportClientError(
        "A valid inspection identifier is required to generate a report.",
        "INVALID_INSPECTION_ID",
        { remediationHint: "Perform an inspection before requesting an assessment report." }
      );
    }

    // Anti-double-click guard
    if (this.isGenerating && this.activeInspectionId === inspectionId) {
      throw new ReportClientError(
        "A report generation request for this inspection is already in progress.",
        "ALREADY_GENERATING"
      );
    }

    this.isGenerating = true;
    this.activeInspectionId = inspectionId;

    const timeoutMs = options?.timeoutMs || 30000;
    const controller = new AbortController();
    const timeoutTimer = setTimeout(() => controller.abort(), timeoutMs);

    const onCallerAbort = () => controller.abort();
    if (options?.signal) {
      options.signal.addEventListener("abort", onCallerAbort);
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/v1/report/pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/pdf, application/json",
        },
        body: JSON.stringify({
          inspection_id: inspectionId,
          officer_notes: options?.officerNotes || "Legal Metrology Officer packaging audit report.",
          include_raw_image: options?.includeRawImage ?? true,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutTimer);

      // Stale report protection: if user navigated away to another inspection, discard
      if (this.activeInspectionId !== inspectionId) {
        throw new ReportClientError(
          "Report generation superseded by subsequent inspection.",
          "CANCELED"
        );
      }

      if (!response.ok) {
        if (response.status === 404 || response.status === 405 || response.status === 501) {
          throw new ReportClientError(
            "Backend report generation service is not currently available at POST /api/v1/report/pdf.",
            "ENDPOINT_UNAVAILABLE",
            {
              statusCode: response.status,
              remediationHint:
                "The Member 4 backend report route has not been deployed. Report generation requires backend PDF compiler.",
            }
          );
        }

        let detail = `HTTP ${response.status} ${response.statusText}`;
        try {
          const errBody = await response.json();
          if (errBody?.detail) detail = String(errBody.detail);
        } catch {
          // ignore parsing error
        }

        throw new ReportClientError(
          `Report generation failed: ${detail}`,
          response.status === 400
            ? "HTTP_400"
            : response.status === 422
            ? "HTTP_422"
            : "HTTP_500",
          { statusCode: response.status }
        );
      }

      // 1. Validate Content-Type
      const contentType = response.headers.get("content-type") || "";
      if (!contentType.toLowerCase().includes("application/pdf")) {
        throw new ReportClientError(
          `Invalid server response: Expected application/pdf but received '${contentType}'.`,
          "INVALID_CONTENT_TYPE",
          {
            remediationHint:
              "Backend returned a non-PDF MIME type. The report generator might have returned an unhandled error message.",
          }
        );
      }

      // 2. Fetch blob & buffer
      const blob = await response.blob();
      if (!blob || blob.size === 0) {
        throw new ReportClientError(
          "The server returned an empty (0 byte) PDF payload.",
          "EMPTY_PAYLOAD",
          { remediationHint: "Check backend PDF generator logs." }
        );
      }

      // 3. Inspect binary signature (%PDF-)
      const buffer = await blob.slice(0, 8).arrayBuffer();
      if (!this.validatePdfHeader(buffer)) {
        throw new ReportClientError(
          "Server response did not begin with valid PDF signature (%PDF-).",
          "INVALID_PDF_SIGNATURE",
          {
            remediationHint:
              "The returned binary stream is corrupt or not a standardized PDF document.",
          }
        );
      }

      // 4. Resolve filename
      const disposition = response.headers.get("content-disposition");
      const filename = this.extractFilenameFromHeader(disposition, inspectionId);

      // 5. Trigger browser download safely and revoke URL
      let downloadTriggered = false;
      if (typeof window !== "undefined" && typeof document !== "undefined") {
        const objectUrl = URL.createObjectURL(blob);
        try {
          const link = document.createElement("a");
          link.href = objectUrl;
          link.download = filename;
          link.style.display = "none";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          downloadTriggered = true;
        } finally {
          // Explicit cleanup to prevent memory leaks
          setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
        }
      }

      return {
        success: true,
        inspectionId,
        filename,
        byteSize: blob.size,
        isSynthetic: false,
        downloadTriggered,
      };
    } catch (err: any) {
      clearTimeout(timeoutTimer);
      if (err instanceof ReportClientError) throw err;

      if (err?.name === "AbortError") {
        throw new ReportClientError(
          "Assessment report request was canceled or timed out.",
          "TIMEOUT"
        );
      }

      // Catch fetch network errors (e.g., ECONNREFUSED)
      throw new ReportClientError(
        `Unable to contact report service: ${err?.message || "Network error"}`,
        "NETWORK_ERROR",
        {
          remediationHint:
            "Verify that the backend API gateway is online at " + this.baseUrl,
        }
      );
    } finally {
      if (options?.signal) {
        options.signal.removeEventListener("abort", onCallerAbort);
      }
      this.isGenerating = false;
      this.activeInspectionId = null;
    }
  }
}

export const defaultReportClient = new ReportClient();
