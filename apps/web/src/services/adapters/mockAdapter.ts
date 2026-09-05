/**
 * MetroLens AI™ - Mock Inspection Adapter
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Implements IInspectionClient using repository-verified synthetic fixtures.
 * NOTE: All outputs are synthetic regression/demo fixtures, not real-world retail data.
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
import { getSyntheticFixtureForFile } from "@/mocks/fixtures";
import { normalizeInspectionResponse } from "./responseNormalizer";
import { validateInspectionImage } from "@/utils/validation";

export class MockInspectionAdapter implements IInspectionClient {
  readonly name = "MockSyntheticInspectionAdapter";
  readonly isMock = true;

  private readonly simulatedDelayMs: number;

  constructor(simulatedDelayMs: number = 650) {
    this.simulatedDelayMs = simulatedDelayMs;
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

    // 2. Simulate statutory pipeline latency
    await new Promise((resolve, reject) => {
      const timer = setTimeout(resolve, this.simulatedDelayMs);

      if (options?.signal) {
        options.signal.addEventListener("abort", () => {
          clearTimeout(timer);
          reject(
            new InspectionClientError(
              "Inspection operation was canceled by the officer.",
              "TIMEOUT"
            )
          );
        });
      }
    });

    // 3. Resolve synthetic fixture based on file
    const fixture = getSyntheticFixtureForFile(file);

    // 4. Normalize fixture DTO into UI Model
    return normalizeInspectionResponse(fixture.data, {
      isSynthetic: true,
      packageTitle: fixture.title,
    });
  }

  async getHealth(): Promise<HealthCheckResult> {
    return {
      status: "OK",
      service: "MetroLens Synthetic Regression Sandbox",
      version: "1.0.0-synthetic",
      isLive: false,
      message: "Operating in synthetic regression / demo fixture mode.",
    };
  }

  async submitReview(
    input: ReviewSubmissionInput
  ): Promise<ReviewSubmissionResult> {
    if (!input.fieldName) {
      throw new InspectionClientError(
        "Declaration field name is required for review submission.",
        "FILE_INVALID"
      );
    }

    if (input.notes && input.notes.length > 500) {
      throw new InspectionClientError(
        "Reviewer notes must not exceed 500 characters.",
        "FILE_INVALID"
      );
    }

    // Simulate inspection review dispatch latency
    await new Promise((resolve) => setTimeout(resolve, 350));

    return {
      success: true,
      isMock: true,
      fieldName: input.fieldName,
      updatedReviewStatus: input.decision,
      operatorNotes: input.notes || null,
      statusMessage: `Inspector review decision (${input.decision}) recorded in audit trail [SYNTHETIC DEMO].`,
      timestamp: new Date().toISOString(),
    };
  }
}
