/**
 * MetroLens AI™ - Inspection Service Factory & Boundary
 * Subsystem: Member 5 (Web Frontend)
 */

import { IInspectionClient } from "./inspectionClient";
import { MockInspectionAdapter } from "./adapters/mockAdapter";
import { LiveApiAdapter } from "./adapters/liveApiAdapter";

export * from "./inspectionClient";
export * from "./adapters/mockAdapter";
export * from "./adapters/liveApiAdapter";
export * from "./adapters/responseNormalizer";
export * from "./reportClient";

export type InspectionClientMode = "auto" | "mock" | "live";

/**
 * Factory creating configured IInspectionClient instances
 */
export function createInspectionClient(
  mode: InspectionClientMode = "auto",
  baseUrl?: string
): IInspectionClient {
  if (mode === "mock") {
    return new MockInspectionAdapter();
  }

  if (mode === "live") {
    return new LiveApiAdapter(baseUrl);
  }

  // Auto mode: Default to Mock if NEXT_PUBLIC_USE_MOCK is set, otherwise Live with fallback capability
  const forceMock = process.env.NEXT_PUBLIC_USE_MOCK === "true";
  if (forceMock) {
    return new MockInspectionAdapter();
  }

  return new LiveApiAdapter(baseUrl);
}

// Export default singleton instance
export const defaultInspectionClient: IInspectionClient = new MockInspectionAdapter();
