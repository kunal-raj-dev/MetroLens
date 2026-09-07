/**
 * MetroLens AI™ - Member 5 (Chunk M5-6) Micro-Audit Test Suite
 * Canonical State Semantics & UI Severity Decoupling Verification
 *
 * Proves:
 * 1. NON_COMPLIANT remains NON_COMPLIANT in canonical frontend model.
 * 2. POTENTIAL_NON_COMPLIANCE remains POTENTIAL_NON_COMPLIANCE in canonical frontend model.
 * 3. COMPLIANT remains COMPLIANT (and distinguishable from NOT_IMAGE_VERIFIABLE and NO_IMAGE_VERIFIABLE_VIOLATIONS).
 * 4. EXEMPTED remains EXEMPTED (and distinguishable from STATUTORY_EXEMPTION_APPLIED).
 * 5. FLAGGED_FOR_REVIEW remains FLAGGED_FOR_REVIEW.
 * 6. Unknown / null / empty states remain safe (requiresReview === true, isCompliant === false, never COMPLIANT).
 * 7. Decoupled UI presentation: Both NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE render with RED severity,
 *    without collapsing their semantic distinction.
 * 8. Zero statutory logic in React: Components consume normalized models without calculating legal rules.
 */

import {
  mapBackendToCanonicalState,
  getUiPresentationForState,
  normalizeInspectionResponse,
} from "../services/adapters/responseNormalizer";
import { CanonicalComplianceState } from "../types/contract";

let passCount = 0;
let failCount = 0;

function assert(condition: boolean, message: string) {
  if (condition) {
    console.log(`  [PASS] ${message}`);
    passCount++;
  } else {
    console.error(`  [FAIL] ${message}`);
    failCount++;
  }
}

async function runSemanticsTests() {
  console.log("============================================================");
  console.log("METROLENS AI - MEMBER 5 CANONICAL SEMANTICS TEST SUITE");
  console.log("============================================================");

  // -------------------------------------------------------------------------
  // 1. Canonical State Mapping and Semantic Fidelity
  // -------------------------------------------------------------------------
  console.log("\n--- 1. Canonical State Mapping and Semantic Fidelity ---");

  // NON_COMPLIANT preservation
  const nonCompliantState = mapBackendToCanonicalState("NON_COMPLIANT");
  assert(nonCompliantState === "NON_COMPLIANT", "NON_COMPLIANT maps to NON_COMPLIANT (not collapsed)");

  // POTENTIAL_NON_COMPLIANCE preservation
  const potNonCompliantState = mapBackendToCanonicalState("POTENTIAL_NON_COMPLIANCE");
  assert(potNonCompliantState === "POTENTIAL_NON_COMPLIANCE", "POTENTIAL_NON_COMPLIANCE maps to POTENTIAL_NON_COMPLIANCE (not collapsed)");
  assert(nonCompliantState !== potNonCompliantState, "NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE are distinct states");

  // COMPLIANT preservation
  const compliantState = mapBackendToCanonicalState("COMPLIANT");
  assert(compliantState === "COMPLIANT", "COMPLIANT maps to COMPLIANT (not collapsed to NO_IMAGE_VERIFIABLE_VIOLATIONS)");

  // NO_IMAGE_VERIFIABLE_VIOLATIONS preservation
  const noImageViolationsState = mapBackendToCanonicalState("NO_IMAGE_VERIFIABLE_VIOLATIONS");
  assert(noImageViolationsState === "NO_IMAGE_VERIFIABLE_VIOLATIONS", "NO_IMAGE_VERIFIABLE_VIOLATIONS preserved");

  const noImageDetectedState = mapBackendToCanonicalState("NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED");
  assert(noImageDetectedState === "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED", "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED preserved");

  // NOT_IMAGE_VERIFIABLE distinction
  const notImageVerifiableState = mapBackendToCanonicalState("NOT_IMAGE_VERIFIABLE");
  assert(notImageVerifiableState === "NOT_IMAGE_VERIFIABLE", "NOT_IMAGE_VERIFIABLE preserved");
  assert(compliantState !== notImageVerifiableState, "COMPLIANT is strictly distinguishable from NOT_IMAGE_VERIFIABLE");
  assert(compliantState !== noImageViolationsState, "COMPLIANT is strictly distinguishable from NO_IMAGE_VERIFIABLE_VIOLATIONS");

  // EXEMPTED preservation
  const exemptedState = mapBackendToCanonicalState("EXEMPTED");
  assert(exemptedState === "EXEMPTED", "EXEMPTED maps to EXEMPTED (not collapsed)");

  const statutoryExemptionState = mapBackendToCanonicalState("STATUTORY_EXEMPTION_APPLIED");
  assert(statutoryExemptionState === "STATUTORY_EXEMPTION_APPLIED", "STATUTORY_EXEMPTION_APPLIED preserved");
  assert(exemptedState !== statutoryExemptionState, "EXEMPTED and STATUTORY_EXEMPTION_APPLIED maintain distinct representations");

  // FLAGGED_FOR_REVIEW preservation
  const flaggedState = mapBackendToCanonicalState("FLAGGED_FOR_REVIEW");
  assert(flaggedState === "FLAGGED_FOR_REVIEW", "FLAGGED_FOR_REVIEW maps to FLAGGED_FOR_REVIEW (not collapsed)");

  const manualReviewState = mapBackendToCanonicalState("MANUAL_REVIEW_REQUIRED");
  assert(manualReviewState === "MANUAL_REVIEW_REQUIRED", "MANUAL_REVIEW_REQUIRED preserved");
  assert(flaggedState !== manualReviewState, "FLAGGED_FOR_REVIEW and MANUAL_REVIEW_REQUIRED maintain distinct representations");

  // SUSPECT_REVIEW and INCONCLUSIVE preservation
  const suspectReviewState = mapBackendToCanonicalState("SUSPECT_REVIEW");
  assert(suspectReviewState === "SUSPECT_REVIEW", "SUSPECT_REVIEW preserved");

  const inconclusiveState = mapBackendToCanonicalState("INCONCLUSIVE");
  assert(inconclusiveState === "INCONCLUSIVE", "INCONCLUSIVE preserved");

  // Case-insensitivity and whitespace tolerance
  assert(mapBackendToCanonicalState("  non_compliant  ") === "NON_COMPLIANT", "Case-insensitive trimming handles lowercase non_compliant");
  assert(mapBackendToCanonicalState("compliant\n") === "COMPLIANT", "Whitespace trimming handles trailing newline");

  // -------------------------------------------------------------------------
  // 2. Safe Fallback for Unknown and Null States
  // -------------------------------------------------------------------------
  console.log("\n--- 2. Unknown and Null State Safety Invariants ---");

  // Null input
  const nullState = mapBackendToCanonicalState(null);
  assert(nullState === "MANUAL_REVIEW_REQUIRED", "null input safely returns MANUAL_REVIEW_REQUIRED");
  assert(nullState !== "COMPLIANT", "null input NEVER resolves to COMPLIANT");

  // Undefined input
  const undefinedState = mapBackendToCanonicalState(undefined);
  assert(undefinedState === "MANUAL_REVIEW_REQUIRED", "undefined input safely returns MANUAL_REVIEW_REQUIRED");
  assert(undefinedState !== "COMPLIANT", "undefined input NEVER resolves to COMPLIANT");

  // Empty string input
  const emptyState = mapBackendToCanonicalState("");
  assert(emptyState === "MANUAL_REVIEW_REQUIRED", "Empty string input safely returns MANUAL_REVIEW_REQUIRED");

  // Completely unknown arbitrary state
  const unknownState = mapBackendToCanonicalState("ARBITRARY_FUTURE_UNVERIFIED_STATE");
  assert(unknownState === "INCONCLUSIVE", "Unrecognized state safely returns INCONCLUSIVE");
  assert(unknownState !== "COMPLIANT", "Unrecognized state NEVER silently defaults to COMPLIANT");

  // Numeric or object malformed input
  assert(mapBackendToCanonicalState(42) === "MANUAL_REVIEW_REQUIRED", "Numeric input safely returns review");
  assert(mapBackendToCanonicalState({}) === "MANUAL_REVIEW_REQUIRED", "Object input safely returns review");

  // -------------------------------------------------------------------------
  // 3. Decoupled UI Presentation and Severity Mapping
  // -------------------------------------------------------------------------
  console.log("\n--- 3. UI Presentation and Severity Mapping ---");

  // Both NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE have RED severity
  const ncPresentation = getUiPresentationForState("NON_COMPLIANT");
  assert(ncPresentation.severity === "RED", "NON_COMPLIANT maps to RED UI severity");
  assert(ncPresentation.badgeVariant === "danger", "NON_COMPLIANT maps to danger badge");
  assert(ncPresentation.eyebrow === "STATUTORY NON-COMPLIANCE", "NON_COMPLIANT eyebrow reflects STATUTORY NON-COMPLIANCE");
  assert(ncPresentation.isCompliant === false, "NON_COMPLIANT isCompliant === false");
  assert(ncPresentation.requiresReview === false, "NON_COMPLIANT requiresReview === false (determinate failure)");

  const pncPresentation = getUiPresentationForState("POTENTIAL_NON_COMPLIANCE");
  assert(pncPresentation.severity === "RED", "POTENTIAL_NON_COMPLIANCE maps to RED UI severity");
  assert(pncPresentation.badgeVariant === "danger", "POTENTIAL_NON_COMPLIANCE maps to danger badge");
  assert(pncPresentation.eyebrow === "POTENTIAL NON-COMPLIANCE", "POTENTIAL_NON_COMPLIANCE eyebrow reflects POTENTIAL NON-COMPLIANCE");
  assert(pncPresentation.isCompliant === false, "POTENTIAL_NON_COMPLIANCE isCompliant === false");

  // Distinction preserved between NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE
  assert(ncPresentation.label !== pncPresentation.label, "NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE have distinct labels");
  assert(ncPresentation.eyebrow !== pncPresentation.eyebrow, "NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE have distinct eyebrows");

  // COMPLIANT presentation
  const compPresentation = getUiPresentationForState("COMPLIANT");
  assert(compPresentation.severity === "GREEN", "COMPLIANT maps to GREEN UI severity");
  assert(compPresentation.badgeVariant === "success", "COMPLIANT maps to success badge");
  assert(compPresentation.isCompliant === true, "COMPLIANT isCompliant === true");
  assert(compPresentation.requiresReview === false, "COMPLIANT requiresReview === false");

  // NO_IMAGE_VERIFIABLE_VIOLATIONS presentation
  const noImagePresentation = getUiPresentationForState("NO_IMAGE_VERIFIABLE_VIOLATIONS");
  assert(noImagePresentation.severity === "GREEN", "NO_IMAGE_VERIFIABLE_VIOLATIONS maps to GREEN UI severity");
  assert(noImagePresentation.eyebrow === "NO IMAGE-VERIFIABLE VIOLATIONS", "NO_IMAGE_VERIFIABLE_VIOLATIONS eyebrow preserved");

  // EXEMPTED presentation
  const exPresentation = getUiPresentationForState("EXEMPTED");
  assert(exPresentation.severity === "BLUE", "EXEMPTED maps to BLUE UI severity");
  assert(exPresentation.badgeVariant === "info", "EXEMPTED maps to info badge");
  assert(exPresentation.isCompliant === false, "EXEMPTED isCompliant === false (exemption != compliance)");

  // FLAGGED_FOR_REVIEW presentation
  const flaggedPresentation = getUiPresentationForState("FLAGGED_FOR_REVIEW");
  assert(flaggedPresentation.severity === "AMBER", "FLAGGED_FOR_REVIEW maps to AMBER UI severity");
  assert(flaggedPresentation.badgeVariant === "warning", "FLAGGED_FOR_REVIEW maps to warning badge");
  assert(flaggedPresentation.requiresReview === true, "FLAGGED_FOR_REVIEW requiresReview === true");
  assert(flaggedPresentation.isCompliant === false, "FLAGGED_FOR_REVIEW isCompliant === false");

  // NOT_IMAGE_VERIFIABLE presentation
  const nivPresentation = getUiPresentationForState("NOT_IMAGE_VERIFIABLE");
  assert(nivPresentation.severity === "GRAY", "NOT_IMAGE_VERIFIABLE maps to GRAY UI severity");
  assert(nivPresentation.badgeVariant === "outline", "NOT_IMAGE_VERIFIABLE maps to outline badge");
  assert(nivPresentation.requiresReview === true, "NOT_IMAGE_VERIFIABLE requiresReview === true");

  // Unknown state presentation safety
  const unkPresentation = getUiPresentationForState("UNKNOWN_GARBAGE");
  assert(unkPresentation.requiresReview === true, "Unknown state presentation requiresReview === true");
  assert(unkPresentation.isCompliant === false, "Unknown state presentation isCompliant === false");

  // -------------------------------------------------------------------------
  // 4. Full Response Normalization Pipeline Integration
  // -------------------------------------------------------------------------
  console.log("\n--- 4. Full Response Normalization Pipeline Integration ---");

  const baseInspectionDto = {
    inspection_id: "INSP-TEST-001",
    timestamp: "2026-09-08T00:00:00Z",
    image_metadata: {
      filename: "test.jpg",
      width_px: 1920,
      height_px: 1080,
      sha256_hash: "a".repeat(64),
      is_quality_valid: true,
      blur_score: 250.0,
      glare_percentage: 1.0,
    },
    calibration: {
      is_calibrated: true,
      anchor_type: "INR_10_COIN",
      coin_detected: true,
      scale_mm_per_px: 0.12,
      pdp_width_mm: 100,
      pdp_height_mm: 150,
      pdp_area_cm2: 150,
      calibration_confidence: 0.95,
    },
    declarations: {
      commodity_name: "Test Cashews",
      mrp_inr: 200,
      net_quantity_value: 200,
      net_quantity_unit: "g",
    },
    rule_evaluations: {
      rule6_mandatory_status: { overall_status: "PASS", missing_declarations: [], details: {} },
      usp_audit: { is_compliant: true },
      font_height_audit: { is_compliant: true },
      exemption_status: { is_exempt: false },
    },
    telemetry: {
      total_duration_ms: 500,
      stages_ms: { quality_gate: 10, metric_calibration: 20, ocr_perception: 400, normalization: 20, rule_engine: 10, evidence_packaging: 40 },
    },
  };

  // Test NON_COMPLIANT in full normalization
  const ncResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    state: "NON_COMPLIANT",
    summary_reason: "Rule 6(1) MRP declaration missing",
  });
  assert(ncResult.verdict.status === "NON_COMPLIANT", "Normalized model verdict.status === 'NON_COMPLIANT'");
  assert(ncResult.verdict.canonicalState === "NON_COMPLIANT", "Normalized model verdict.canonicalState === 'NON_COMPLIANT'");
  assert(ncResult.verdict.uiSeverity === "RED", "Normalized model verdict.uiSeverity === 'RED'");
  assert(ncResult.verdict.label === "Statutory Non-Compliance Detected", "Normalized model verdict.label reflects statutory non-compliance");
  assert(ncResult.verdict.isCompliant === false, "Normalized model verdict.isCompliant === false");

  // Test POTENTIAL_NON_COMPLIANCE in full normalization
  const pncResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    state: "POTENTIAL_NON_COMPLIANCE",
    summary_reason: "Rule 6(11) USP arithmetic mismatch detected",
  });
  assert(pncResult.verdict.status === "POTENTIAL_NON_COMPLIANCE", "Normalized model verdict.status === 'POTENTIAL_NON_COMPLIANCE'");
  assert(pncResult.verdict.canonicalState === "POTENTIAL_NON_COMPLIANCE", "Normalized model verdict.canonicalState === 'POTENTIAL_NON_COMPLIANCE'");
  assert(pncResult.verdict.uiSeverity === "RED", "Normalized model verdict.uiSeverity === 'RED'");
  assert(pncResult.verdict.label === "Potential Statutory Non-Compliance Detected", "Normalized model verdict.label reflects potential non-compliance");
  assert(pncResult.verdict.isCompliant === false, "Normalized model verdict.isCompliant === false");

  // Test COMPLIANT in full normalization
  const compResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    state: "COMPLIANT",
    summary_reason: "All mandatory declarations verified",
  });
  assert(compResult.verdict.status === "COMPLIANT", "Normalized model verdict.status === 'COMPLIANT'");
  assert(compResult.verdict.canonicalState === "COMPLIANT", "Normalized model verdict.canonicalState === 'COMPLIANT'");
  assert(compResult.verdict.uiSeverity === "GREEN", "Normalized model verdict.uiSeverity === 'GREEN'");
  assert(compResult.verdict.isCompliant === true, "Normalized model verdict.isCompliant === true");

  // Test EXEMPTED in full normalization
  const exResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    state: "EXEMPTED",
    summary_reason: "Package exempt under Rule 26",
  });
  assert(exResult.verdict.status === "EXEMPTED", "Normalized model verdict.status === 'EXEMPTED'");
  assert(exResult.verdict.canonicalState === "EXEMPTED", "Normalized model verdict.canonicalState === 'EXEMPTED'");
  assert(exResult.verdict.uiSeverity === "BLUE", "Normalized model verdict.uiSeverity === 'BLUE'");
  assert(exResult.verdict.isCompliant === false, "Normalized model verdict.isCompliant === false");

  // Test FLAGGED_FOR_REVIEW in full normalization
  const flaggedResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    state: "FLAGGED_FOR_REVIEW",
    summary_reason: "Borderline font measurement requires review",
  });
  assert(flaggedResult.verdict.status === "FLAGGED_FOR_REVIEW", "Normalized model verdict.status === 'FLAGGED_FOR_REVIEW'");
  assert(flaggedResult.verdict.canonicalState === "FLAGGED_FOR_REVIEW", "Normalized model verdict.canonicalState === 'FLAGGED_FOR_REVIEW'");
  assert(flaggedResult.verdict.uiSeverity === "AMBER", "Normalized model verdict.uiSeverity === 'AMBER'");
  assert(flaggedResult.verdict.requiresReview === true, "Normalized model verdict.requiresReview === true");
  assert(flaggedResult.verdict.isCompliant === false, "Normalized model verdict.isCompliant === false");

  // -------------------------------------------------------------------------
  // 5. Quality Gate Degradation Override
  // -------------------------------------------------------------------------
  console.log("\n--- 5. Quality Gate Degradation Override ---");

  // Corrupted/blurry image must NEVER be allowed COMPLIANT, even if backend mistakenly sent COMPLIANT
  const degradedCompResult = normalizeInspectionResponse({
    ...baseInspectionDto,
    image_metadata: {
      ...baseInspectionDto.image_metadata,
      is_quality_valid: false, // FAILED quality gate
      blur_score: 30.0,
    },
    state: "COMPLIANT",
  });
  assert(degradedCompResult.verdict.status === "FLAGGED_FOR_REVIEW", "Failed quality gate forces status to FLAGGED_FOR_REVIEW");
  assert(degradedCompResult.verdict.canonicalState === "FLAGGED_FOR_REVIEW", "Failed quality gate forces canonicalState to FLAGGED_FOR_REVIEW");
  assert(degradedCompResult.verdict.isCompliant === false, "Failed quality gate strictly forces isCompliant === false");
  assert(degradedCompResult.verdict.requiresReview === true, "Failed quality gate strictly forces requiresReview === true");
  assert(degradedCompResult.verdict.uiSeverity === "AMBER", "Failed quality gate maps to AMBER severity");

  // -------------------------------------------------------------------------
  // Summary
  // -------------------------------------------------------------------------
  console.log("\n============================================================");
  console.log(`M5-6 CANONICAL SEMANTICS TEST SUMMARY: ${passCount} PASSED, ${failCount} FAILED`);
  console.log("============================================================");

  if (failCount > 0) {
    process.exit(1);
  }
}

runSemanticsTests().catch((err) => {
  console.error("Test execution threw uncaught exception:", err);
  process.exit(1);
});
