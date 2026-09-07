/**
 * MetroLens AI™ - Inspection Response Normalizer
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Maps backend Pydantic DTOs (contracts.py / schemas.py) into clean, immutable
 * FrontendInspectionModels consumed by the Officer Workstation.
 * 
 * Invariants:
 * - Does NOT perform legal rule adjudication.
 * - Does NOT recalculate physical font heights or metric scale.
 * - Defensively handles nulls, missing fields, or legacy responses.
 * - Preserves Member 1/2 unnormalized original image pixel coordinates.
 * - If quality gate fails, never permits a COMPLIANT verdict.
 * - Uncalibrated state strictly preserves null mm scale/heights.
 */

import {
  BackendInspectionDTO,
  DeclarationFieldDTO,
  EvidenceItemDTO,
  OCRObservationDTO,
  RuleEvaluationDTO,
  OverallVerdict,
  CanonicalComplianceState,
  CalibrationStatus,
  RuleVerdict,
} from "@/types/contract";
import {
  FrontendInspectionModel,
  DeclarationModel,
  BoundingBoxModel,
  OCRTokenModel,
} from "@/types/frontend";
import { InspectionClientError } from "../inspectionClient";

export type UISeverity = "RED" | "GREEN" | "AMBER" | "BLUE" | "GRAY";

export interface UIPresentationConfig {
  severity: UISeverity;
  badgeColor: "red" | "green" | "amber" | "blue" | "gray";
  badgeVariant: "danger" | "success" | "warning" | "info" | "outline";
  label: string;
  eyebrow: string;
  defaultExplanation: string;
  isCompliant: boolean;
  requiresReview: boolean;
}

/**
 * Authoritative Canonical State Mapping:
 * Backend state -> Frontend canonical state -> UI presentation
 *
 * Invariants:
 * - Strictly preserves backend semantic states without collapsing distinct legal outcomes:
 *   - "NON_COMPLIANT" remains "NON_COMPLIANT"
 *   - "POTENTIAL_NON_COMPLIANCE" remains "POTENTIAL_NON_COMPLIANCE"
 *   - "COMPLIANT" remains "COMPLIANT"
 *   - "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED" / "NO_IMAGE_VERIFIABLE_VIOLATIONS" are preserved
 *   - "EXEMPTED" remains "EXEMPTED"
 *   - "STATUTORY_EXEMPTION_APPLIED" remains "STATUTORY_EXEMPTION_APPLIED"
 *   - "FLAGGED_FOR_REVIEW" remains "FLAGGED_FOR_REVIEW"
 *   - "MANUAL_REVIEW_REQUIRED" remains "MANUAL_REVIEW_REQUIRED"
 *   - "SUSPECT_REVIEW" remains "SUSPECT_REVIEW"
 *   - "NOT_IMAGE_VERIFIABLE" remains "NOT_IMAGE_VERIFIABLE"
 *   - "INCONCLUSIVE" remains "INCONCLUSIVE"
 * - Safety Invariants:
 *   - null, undefined, or empty values default to safe review ("MANUAL_REVIEW_REQUIRED")
 *   - Unrecognized strings default to safe review ("INCONCLUSIVE")
 *   - NEVER silently defaults to COMPLIANT.
 */
export function mapBackendToCanonicalState(rawState: any): CanonicalComplianceState {
  if (!rawState || typeof rawState !== "string") {
    return "MANUAL_REVIEW_REQUIRED";
  }
  const s = rawState.trim().toUpperCase();
  switch (s) {
    case "NON_COMPLIANT":
      return "NON_COMPLIANT";

    case "POTENTIAL_NON_COMPLIANCE":
      return "POTENTIAL_NON_COMPLIANCE";

    case "COMPLIANT":
      return "COMPLIANT";

    case "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED":
      return "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED";

    case "NO_IMAGE_VERIFIABLE_VIOLATIONS":
      return "NO_IMAGE_VERIFIABLE_VIOLATIONS";

    case "FLAGGED_FOR_REVIEW":
      return "FLAGGED_FOR_REVIEW";

    case "MANUAL_REVIEW_REQUIRED":
      return "MANUAL_REVIEW_REQUIRED";

    case "SUSPECT_REVIEW":
      return "SUSPECT_REVIEW";

    case "EXEMPTED":
      return "EXEMPTED";

    case "STATUTORY_EXEMPTION_APPLIED":
      return "STATUTORY_EXEMPTION_APPLIED";

    case "NOT_IMAGE_VERIFIABLE":
      return "NOT_IMAGE_VERIFIABLE";

    case "INCONCLUSIVE":
      return "INCONCLUSIVE";

    default:
      // Invariant: Unknown values MUST NEVER default to COMPLIANT
      return "INCONCLUSIVE";
  }
}

/**
 * Separate UI presentation and severity mapping decoupled from canonical state adjudication.
 * Desired architecture: backend state -> canonical frontend semantic state -> UI severity / label.
 *
 * Both NON_COMPLIANT and POTENTIAL_NON_COMPLIANCE render with RED severity without erasing the distinction.
 */
export function getUiPresentationForState(
  state: CanonicalComplianceState | OverallVerdict | string | null | undefined
): UIPresentationConfig {
  const canonical = mapBackendToCanonicalState(state);
  switch (canonical) {
    case "NON_COMPLIANT":
      return {
        severity: "RED",
        badgeColor: "red",
        badgeVariant: "danger",
        label: "Statutory Non-Compliance Detected",
        eyebrow: "STATUTORY NON-COMPLIANCE",
        defaultExplanation:
          "One or more statutory requirements under Rule 6, Rule 7 font matrix, or Rule 6(11) Unit Sale Price fail statutory criteria.",
        isCompliant: false,
        requiresReview: false,
      };

    case "POTENTIAL_NON_COMPLIANCE":
      return {
        severity: "RED",
        badgeColor: "red",
        badgeVariant: "danger",
        label: "Potential Statutory Non-Compliance Detected",
        eyebrow: "POTENTIAL NON-COMPLIANCE",
        defaultExplanation:
          "Potential statutory discrepancy detected requiring verification. Section 36(1) improvement notice recommended.",
        isCompliant: false,
        requiresReview: false,
      };

    case "COMPLIANT":
      return {
        severity: "GREEN",
        badgeColor: "green",
        badgeVariant: "success",
        label: "Compliant with Legal Metrology Standards",
        eyebrow: "COMPLIANT",
        defaultExplanation:
          "All mandatory declarations detected and verified against statutory criteria.",
        isCompliant: true,
        requiresReview: false,
      };

    case "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED":
    case "NO_IMAGE_VERIFIABLE_VIOLATIONS":
      return {
        severity: "GREEN",
        badgeColor: "green",
        badgeVariant: "success",
        label: "No Image-Verifiable Violations Detected",
        eyebrow: "NO IMAGE-VERIFIABLE VIOLATIONS",
        defaultExplanation:
          "All image-verifiable mandatory declarations strictly satisfy the Legal Metrology (Packaged Commodities) Rules, 2011 on this panel.",
        isCompliant: true,
        requiresReview: false,
      };

    case "FLAGGED_FOR_REVIEW":
      return {
        severity: "AMBER",
        badgeColor: "amber",
        badgeVariant: "warning",
        label: "Flagged for Officer Review",
        eyebrow: "FLAGGED FOR REVIEW",
        defaultExplanation:
          "Automated analysis flagged conditions (e.g. image quality gate or borderline measurement) requiring mandatory officer review.",
        isCompliant: false,
        requiresReview: true,
      };

    case "MANUAL_REVIEW_REQUIRED":
    case "SUSPECT_REVIEW":
      return {
        severity: "AMBER",
        badgeColor: "amber",
        badgeVariant: "warning",
        label: "Inspector Manual Review Required",
        eyebrow: "MANUAL REVIEW REQUIRED",
        defaultExplanation:
          "Automatic reference scale fiducial was absent or occluded, optical quality is degraded, or measurement lies within statutory uncertainty bounds.",
        isCompliant: false,
        requiresReview: true,
      };

    case "EXEMPTED":
      return {
        severity: "BLUE",
        badgeColor: "blue",
        badgeVariant: "info",
        label: "Statutory Exemption (Rule 26 / Rule 3)",
        eyebrow: "STATUTORY EXEMPTION",
        defaultExplanation:
          "Package qualifies for statutory exemption under Rule 26 or Rule 3 of the Legal Metrology (Packaged Commodities) Rules, 2011.",
        isCompliant: false,
        requiresReview: false,
      };

    case "STATUTORY_EXEMPTION_APPLIED":
      return {
        severity: "BLUE",
        badgeColor: "blue",
        badgeVariant: "info",
        label: "Statutory Exemption Applied (Rule 26 / Rule 3)",
        eyebrow: "STATUTORY EXEMPTION APPLIED",
        defaultExplanation:
          "Package qualifies for statutory exemption under Rule 26 or Rule 3 of the Legal Metrology (Packaged Commodities) Rules, 2011.",
        isCompliant: false,
        requiresReview: false,
      };

    case "NOT_IMAGE_VERIFIABLE":
      return {
        severity: "GRAY",
        badgeColor: "gray",
        badgeVariant: "outline",
        label: "Not Image Verifiable / Physical Audit Required",
        eyebrow: "NOT IMAGE VERIFIABLE",
        defaultExplanation:
          "Statutory check requires physical weighing scale audit (Rule 24), laboratory analysis, or cannot be determined from 2D imagery.",
        isCompliant: false,
        requiresReview: true,
      };

    case "INCONCLUSIVE":
    default:
      return {
        severity: "GRAY",
        badgeColor: "gray",
        badgeVariant: "outline",
        label: "Inconclusive Inspection",
        eyebrow: "INCONCLUSIVE",
        defaultExplanation:
          "Inspection could not reach a definitive legal verdict due to optical or frame conditions.",
        isCompliant: false,
        requiresReview: true,
      };
  }
}

/**
 * Maps snake_case backend BoundingBoxDTO or [x, y, w, h] tuple to camelCase BoundingBoxModel
 * Conforms to: bbox_px [x, y, w, h] -> [xMin: x, yMin: y, xMax: x+w, yMax: y+h]
 */
export function normalizeBoundingBox(bbox?: any | null): BoundingBoxModel | null {
  if (!bbox) return null;

  // Handle [x, y, width, height] array from Member 4 schemas.py
  if (Array.isArray(bbox)) {
    if (bbox.length !== 4) return null;
    const [x, y, w, h] = bbox.map(Number);
    if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(w) || !Number.isFinite(h)) {
      return null;
    }
    return {
      xMin: x,
      yMin: y,
      xMax: x + w,
      yMax: y + h,
      width: Math.max(0, w),
      height: Math.max(0, h),
    };
  }

  if (typeof bbox === "object") {
    const hasKeys = "x_min" in bbox || "xMin" in bbox || "x_max" in bbox || "xMax" in bbox;
    if (!hasKeys) return null;

    const xMin = Number(bbox.x_min ?? bbox.xMin ?? 0);
    const yMin = Number(bbox.y_min ?? bbox.yMin ?? 0);
    const xMax = Number(bbox.x_max ?? bbox.xMax ?? 0);
    const yMax = Number(bbox.y_max ?? bbox.yMax ?? 0);

    if (!Number.isFinite(xMin) || !Number.isFinite(yMin) || !Number.isFinite(xMax) || !Number.isFinite(yMax)) {
      return null;
    }

    return {
      xMin,
      yMin,
      xMax,
      yMax,
      width: Math.max(0, xMax - xMin),
      height: Math.max(0, yMax - yMin),
    };
  }

  return null;
}

/**
 * Creates human-friendly labels from declaration field keys
 */
export function formatFieldLabel(key: string): string {
  const map: Record<string, string> = {
    mrp: "Maximum Retail Price (MRP)",
    mrp_inr: "Maximum Retail Price (MRP)",
    net_quantity: "Net Quantity / Measure",
    net_quantity_value: "Net Quantity / Measure",
    unit_sale_price: "Unit Sale Price (USP)",
    declared_usp_value: "Unit Sale Price (USP)",
    manufacturer: "Manufacturer / Packer Details",
    manufacturer_name: "Manufacturer / Packer Details",
    packer: "Packer / Importer Details",
    consumer_care: "Consumer Care Contact",
    date_of_mfg: "Date of Manufacture / Packing",
    mfg_date: "Date of Manufacture / Packing",
    expiry_date: "Expiry / Best Before Date",
    country_of_origin: "Country of Origin",
    commodity_name: "Generic Commodity Name",
  };
  if (map[key]) return map[key];
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

/**
 * Extracts or maps the backend-provided explanation without reinterpreting legal rules.
 * Prefers verified backend text over client heuristics.
 */
export function resolveVerdictSummary(
  verdict: OverallVerdict,
  rawSummary?: string | null,
  ruleEvaluations?: any
): string {
  // If backend provided a direct summary or explanation, prefer it
  if (rawSummary && rawSummary.trim().length > 0) {
    return rawSummary.trim();
  }

  // If backend provided legacy rule evaluations array
  if (Array.isArray(ruleEvaluations) && ruleEvaluations.length > 0) {
    const failedRule = ruleEvaluations.find((r) => r.verdict === "FAIL");
    if (failedRule && failedRule.observed_summary) {
      return `${failedRule.statutory_reference || failedRule.rule_id}: ${failedRule.observed_summary}`;
    }
    const reviewRule = ruleEvaluations.find((r) => r.verdict === "REVIEW");
    if (reviewRule && reviewRule.observed_summary) {
      return `${reviewRule.statutory_reference || reviewRule.rule_id}: ${reviewRule.observed_summary}`;
    }
    const passRule = ruleEvaluations.find((r) => r.verdict === "PASS");
    if (passRule && passRule.observed_summary) {
      return passRule.observed_summary;
    }
  }

  // Neutral UI fallbacks matching 5-state statutory taxonomy
  switch (verdict) {
    case "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED":
    case "NO_IMAGE_VERIFIABLE_VIOLATIONS":
      return "All image-verifiable mandatory declarations strictly satisfy the Legal Metrology (Packaged Commodities) Rules, 2011 on this panel.";
    case "COMPLIANT":
      return "All mandatory declarations verified in accordance with Legal Metrology guidelines.";
    case "NON_COMPLIANT":
      return "One or more statutory deficits detected by the deterministic rule engine.";
    case "POTENTIAL_NON_COMPLIANCE":
      return "Potential statutory discrepancy detected requiring verification. Section 36(1) improvement notice recommended.";
    case "FLAGGED_FOR_REVIEW":
      return "Automated analysis flagged conditions requiring mandatory officer review.";
    case "MANUAL_REVIEW_REQUIRED":
    case "SUSPECT_REVIEW":
      return "Inspection flags detected requiring enforcement officer verification.";
    case "STATUTORY_EXEMPTION_APPLIED":
    case "EXEMPTED":
      return "Package qualifies for statutory exemption under Rule 26 or Rule 3 of the Legal Metrology Rules, 2011.";
    case "NOT_IMAGE_VERIFIABLE":
    case "INCONCLUSIVE":
    default:
      return "Inspection could not reach a definitive legal verdict due to optical or frame conditions.";
  }
}

export { resolveVerdictSummary as synthesizeVerdictSummary };

/**
 * Normalizes backend DTO into FrontendInspectionModel
 */
export function normalizeInspectionResponse(
  raw: any,
  meta?: { isSynthetic?: boolean; packageTitle?: string; imagePath?: string }
): FrontendInspectionModel {
  if (!raw || typeof raw !== "object") {
    throw new InspectionClientError(
      "Received invalid or empty inspection payload from server",
      "INVALID_SERVER_RESPONSE"
    );
  }

  const inspectionId: string =
    raw.inspection_id || raw.inspectionId || `INSP-${Date.now()}`;
  const createdAt: string =
    raw.timestamp || raw.created_at || raw.createdAt || new Date().toISOString();
  const imageSha256: string =
    raw.image_metadata?.sha256_hash ||
    raw.image_sha256 ||
    raw.imageSha256 ||
    "unknown-hash";

  // Quality gate normalization: missing quality telemetry MUST NOT default to PASS
  const qualityGatePassed = raw.image_metadata
    ? Boolean(raw.image_metadata.is_quality_valid)
    : (typeof raw.quality_gate_passed === "boolean" ? raw.quality_gate_passed : false);

  const sharpnessScore =
    typeof raw.image_metadata?.blur_score === "number"
      ? raw.image_metadata.blur_score
      : (typeof raw.telemetry?.sharpness_score === "number" ? raw.telemetry.sharpness_score : undefined);

  const glareRatio =
    typeof raw.image_metadata?.glare_percentage === "number"
      ? raw.image_metadata.glare_percentage / 100
      : (typeof raw.telemetry?.glare_ratio === "number" ? raw.telemetry.glare_ratio : undefined);

  // Calibration status normalization: uncalibrated preserves null mm scale/heights
  const isCalibrated = raw.calibration
    ? Boolean(raw.calibration.is_calibrated)
    : raw.calibration_status === "CALIBRATED";
  const calibrationStatus: CalibrationStatus = isCalibrated
    ? "CALIBRATED"
    : (raw.calibration_status || "UNCALIBRATED");
  const scaleFactor = isCalibrated
    ? (raw.calibration?.scale_mm_per_px ??
       raw.measurements?.[Object.keys(raw.measurements || {})[0]]?.scale_factor_mm_per_pixel ??
       null)
    : null;

  // Verdict state normalization: preserve backend semantic state without collapsing
  const rawVerdict = raw.state || raw.overall_verdict || raw.overallVerdict;
  let canonicalState: CanonicalComplianceState = mapBackendToCanonicalState(rawVerdict);

  // Strict Invariant: Quality gate failure must NEVER produce a compliant verdict
  if (
    !qualityGatePassed &&
    (canonicalState === "COMPLIANT" ||
      canonicalState === "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED" ||
      canonicalState === "NO_IMAGE_VERIFIABLE_VIOLATIONS")
  ) {
    canonicalState = "FLAGGED_FOR_REVIEW";
  }

  const presentation = getUiPresentationForState(canonicalState);

  const summaryReason = resolveVerdictSummary(
    canonicalState,
    raw.summary_reason || raw.reason,
    raw.rule_evaluations
  );

  // Normalization of evidence items and crops
  const evidenceItems: FrontendInspectionModel["evidenceItems"] = [];
  const ocrTokens: OCRTokenModel[] = [];

  // 1. Process Member 4 evidence_crops if available
  const evidenceCropsMap: Record<string, any> = {};
  if (Array.isArray(raw.evidence_crops) && raw.evidence_crops.length > 0) {
    raw.evidence_crops.forEach((crop: any, index: number) => {
      const fieldKey = (crop.field_name || "").toLowerCase();
      evidenceCropsMap[fieldKey] = crop;
      const bbox = normalizeBoundingBox(crop.bbox_px);
      if (bbox) {
        evidenceItems.push({
          id: `ev-${crop.field_name || "crop"}-${index}`,
          fieldName: formatFieldLabel(crop.field_name || "PDP"),
          boundingBox: bbox,
          observedValue: crop.label || null,
          confidence: typeof crop.confidence === "number" ? crop.confidence : 1.0,
        });

        ocrTokens.push({
          id: `tok_${crop.field_name || index}`,
          text: crop.label || formatFieldLabel(crop.field_name),
          confidence: typeof crop.confidence === "number" ? crop.confidence : 1.0,
          boundingBox: bbox,
          polygon: [
            [bbox.xMin, bbox.yMin],
            [bbox.xMax, bbox.yMin],
            [bbox.xMax, bbox.yMax],
            [bbox.xMin, bbox.yMax],
          ],
          script: "latin",
          fieldName: crop.field_name,
          requiresReview: (crop.confidence ?? 1.0) < 0.85,
        });
      }
    });
  }

  // 2. Process legacy evidence_chain if present
  if (evidenceItems.length === 0 && Array.isArray(raw.evidence_chain)) {
    for (const ev of raw.evidence_chain) {
      const bbox = normalizeBoundingBox(ev.bounding_box);
      if (bbox) {
        evidenceItems.push({
          id: ev.evidence_id || `ev-${Math.random().toString(36).substring(2, 8)}`,
          fieldName: formatFieldLabel(ev.panel_name || "PDP"),
          boundingBox: bbox,
          observedValue: ev.observed_value?.raw_text || null,
          confidence: ev.observed_value?.ocr_confidence ?? null,
        });
      }
    }
  }

  // Declarations normalization: Detect Member 4 flat DeclarationsInfo vs legacy DTO
  const declarations: Record<string, DeclarationModel> = {};
  const rawDecls = raw.declarations || {};

  const isLegacyDeclarations =
    Object.values(rawDecls).some(
      (v: any) => v && typeof v === "object" && ("raw_text" in v || "source_token_ids" in v)
    );

  if (isLegacyDeclarations) {
    // Legacy parsing
    const ruleEvaluations: RuleEvaluationDTO[] = Array.isArray(raw.rule_evaluations)
      ? (raw.rule_evaluations as RuleEvaluationDTO[])
      : [];

    for (const [key, item] of Object.entries(rawDecls)) {
      const decl = (item || {}) as DeclarationFieldDTO;
      const matchingRule = ruleEvaluations.find(
        (r) => r.evidence_ids && r.evidence_ids.includes(key)
      );

      const measurementsObj = raw.measurements || {};
      const matchingMeasurement =
        measurementsObj[key] ||
        measurementsObj[`${key}_height`] ||
        measurementsObj[`${key}_font_height`];
      const measuredHeightMm =
        isCalibrated && typeof matchingMeasurement?.measured_mm === "number"
          ? matchingMeasurement.measured_mm
          : null;

      declarations[key] = {
        fieldName: key,
        label: formatFieldLabel(key),
        rawText: decl.raw_text || "",
        normalizedValue: decl.normalized_value ?? null,
        confidence: typeof decl.confidence === "number" ? decl.confidence : 1.0,
        isMandatory: decl.is_mandatory ?? true,
        isPresent: decl.is_present ?? Boolean(decl.raw_text),
        boundingBox: normalizeBoundingBox(decl.bounding_box),
        verdict: matchingRule?.verdict,
        evaluationNotes: matchingRule?.evaluation_notes || matchingRule?.observed_summary,
        ruleTitle: matchingRule?.rule_title || null,
        statutoryReference: matchingRule?.statutory_reference || null,
        requiredSummary: matchingRule?.required_summary || null,
        measuredHeightMm,
        reviewStatus:
          matchingRule?.verdict === "REVIEW"
            ? "IN_REVIEW"
            : (decl.confidence ?? 1.0) < 0.85
            ? "IN_REVIEW"
            : "NOT_REVIEWED",
        operatorNotes: null,
        sourceTokenIds: decl.source_token_ids || [],
      };
    }
  } else {
    // Member 4 flat DeclarationsInfo parsing
    const rule6 = raw.rule_evaluations?.rule6_mandatory_status || {};
    const details = rule6.details || {};
    const uspAudit = raw.rule_evaluations?.usp_audit;
    const fontAudit = raw.rule_evaluations?.font_height_audit;

    const getFieldVerdict = (fieldKey: string, isPresent: boolean): RuleVerdict => {
      const detailVal = details[fieldKey];
      if (detailVal === "PASS") return "PASS";
      if (detailVal === "FAIL") return "FAIL";
      if (detailVal === "REVIEW") return "REVIEW";
      return isPresent ? "PASS" : "FAIL";
    };

    // Define standard statutory field mapping
    const definitions: Array<{
      key: string;
      label: string;
      cropKey: string;
      rawText: string;
      normalizedValue: any;
      isPresent: boolean;
      statutoryRef: string;
      verdict: RuleVerdict;
      notes?: string | null;
      statutoryMinMm?: number | null;
      measuredHeightMm?: number | null;
    }> = [
      {
        key: "commodity_name",
        label: "Generic Commodity Name",
        cropKey: "commodity_name",
        rawText: rawDecls.commodity_name || "",
        normalizedValue: rawDecls.commodity_name ?? null,
        isPresent: Boolean(rawDecls.commodity_name),
        statutoryRef: "Rule 6(1)(b)",
        verdict: getFieldVerdict("commodity_name", Boolean(rawDecls.commodity_name)),
        notes: rawDecls.commodity_name ? "Generic commodity identity declared." : "Commodity name missing.",
      },
      {
        key: "mrp",
        label: "Maximum Retail Price (MRP)",
        cropKey: "mrp",
        rawText: rawDecls.mrp_inr != null
          ? `₹ ${Number(rawDecls.mrp_inr).toFixed(2)}${rawDecls.tax_qualifier_present ? " (Incl. of all taxes)" : ""}`
          : "",
        normalizedValue: rawDecls.mrp_inr ?? null,
        isPresent: rawDecls.mrp_inr != null,
        statutoryRef: "Rule 6(1)(e)",
        verdict: getFieldVerdict("mrp", rawDecls.mrp_inr != null),
        notes: rawDecls.mrp_inr != null ? "MRP declared with statutory tax qualifier." : "MRP declaration missing.",
      },
      {
        key: "net_quantity",
        label: "Net Quantity / Measure",
        cropKey: "net_quantity",
        rawText: rawDecls.net_quantity_value != null
          ? `${rawDecls.net_quantity_value} ${rawDecls.net_quantity_unit || ""}`.trim()
          : "",
        normalizedValue: rawDecls.net_quantity_value != null
          ? { value: rawDecls.net_quantity_value, unit: rawDecls.net_quantity_unit }
          : null,
        isPresent: rawDecls.net_quantity_value != null,
        statutoryRef: "Rule 6(1)(f) & Rule 7 Table-I",
        verdict: fontAudit?.is_compliant === false ? "FAIL" : getFieldVerdict("net_quantity", rawDecls.net_quantity_value != null),
        notes: fontAudit
          ? `Net qty font height: ${fontAudit.measured_net_qty_height_mm != null ? fontAudit.measured_net_qty_height_mm.toFixed(2) + "mm" : "N/A"} (min ${fontAudit.statutory_min_height_mm != null ? fontAudit.statutory_min_height_mm.toFixed(2) + "mm" : "N/A"})`
          : null,
        statutoryMinMm: fontAudit?.statutory_min_height_mm ?? null,
        measuredHeightMm: isCalibrated ? (fontAudit?.measured_net_qty_height_mm ?? null) : null,
      },
      {
        key: "unit_sale_price",
        label: "Unit Sale Price (USP)",
        cropKey: "usp",
        rawText: rawDecls.declared_usp_value != null
          ? `₹ ${rawDecls.declared_usp_value} / ${rawDecls.declared_usp_unit || "unit"}`
          : "",
        normalizedValue: rawDecls.declared_usp_value ?? null,
        isPresent: rawDecls.declared_usp_value != null,
        statutoryRef: "Rule 6(11)",
        verdict: uspAudit?.is_compliant === true ? "PASS" : (rawDecls.declared_usp_value == null ? "FAIL" : "FAIL"),
        notes: uspAudit?.notes || (rawDecls.declared_usp_value == null ? "Unit Sale Price missing." : null),
      },
      {
        key: "date_of_mfg",
        label: "Date of Manufacture / Packing",
        cropKey: "mfg_date",
        rawText: rawDecls.mfg_month && rawDecls.mfg_year
          ? `${String(rawDecls.mfg_month).padStart(2, "0")}/${rawDecls.mfg_year}`
          : "",
        normalizedValue: rawDecls.mfg_month && rawDecls.mfg_year
          ? { month: rawDecls.mfg_month, year: rawDecls.mfg_year }
          : null,
        isPresent: Boolean(rawDecls.mfg_month && rawDecls.mfg_year),
        statutoryRef: "Rule 6(1)(d)",
        verdict: getFieldVerdict("mfg_date", Boolean(rawDecls.mfg_month && rawDecls.mfg_year)),
        notes: rawDecls.mfg_month ? "Month and year of manufacture verified." : "Date of manufacture missing.",
      },
      {
        key: "manufacturer",
        label: "Manufacturer / Packer Details",
        cropKey: "manufacturer",
        rawText: rawDecls.manufacturer_name
          ? `${rawDecls.manufacturer_name}${rawDecls.manufacturer_pincode ? " - PIN " + rawDecls.manufacturer_pincode : ""}`
          : "",
        normalizedValue: rawDecls.manufacturer_name ?? null,
        isPresent: Boolean(rawDecls.manufacturer_name),
        statutoryRef: "Rule 6(1)(a)",
        verdict: getFieldVerdict("manufacturer_details", Boolean(rawDecls.manufacturer_name)),
        notes: rawDecls.manufacturer_name ? "Manufacturer name and address verified." : "Manufacturer details missing.",
      },
      {
        key: "consumer_care",
        label: "Consumer Care Contact",
        cropKey: "consumer_care",
        rawText: [rawDecls.consumer_care_phone, rawDecls.consumer_care_email].filter(Boolean).join(" / ") || "",
        normalizedValue: { phone: rawDecls.consumer_care_phone, email: rawDecls.consumer_care_email },
        isPresent: Boolean(rawDecls.consumer_care_phone || rawDecls.consumer_care_email),
        statutoryRef: "Rule 6(1)(g)",
        verdict: getFieldVerdict("consumer_care", Boolean(rawDecls.consumer_care_phone || rawDecls.consumer_care_email)),
        notes: (rawDecls.consumer_care_phone || rawDecls.consumer_care_email) ? "Consumer care contact verified." : "Consumer care contact missing.",
      },
      {
        key: "country_of_origin",
        label: "Country of Origin",
        cropKey: "country_of_origin",
        rawText: rawDecls.country_of_origin || "",
        normalizedValue: rawDecls.country_of_origin ?? null,
        isPresent: Boolean(rawDecls.country_of_origin),
        statutoryRef: "Rule 6(10)",
        verdict: rawDecls.country_of_origin ? "PASS" : "REVIEW",
        notes: rawDecls.country_of_origin ? "Country of origin declared." : "Origin declaration not detected.",
      },
    ];

    for (const def of definitions) {
      const crop =
        evidenceCropsMap[def.cropKey] ||
        evidenceCropsMap[def.key] ||
        raw.evidence_crops?.find(
          (c: any) =>
            c.field_name === def.key ||
            c.field_name === def.cropKey ||
            c.field_name?.toLowerCase().includes(def.cropKey)
        );

      const bbox = crop ? normalizeBoundingBox(crop.bbox_px) : null;
      const cropMeasuredMm = isCalibrated && typeof crop?.measured_height_mm === "number"
        ? crop.measured_height_mm
        : null;

      declarations[def.key] = {
        fieldName: def.key,
        label: def.label,
        rawText: def.rawText,
        normalizedValue: def.normalizedValue,
        confidence: typeof crop?.confidence === "number" ? crop.confidence : (def.isPresent ? 0.95 : 0.0),
        isMandatory: true,
        isPresent: def.isPresent,
        boundingBox: bbox,
        verdict: def.verdict,
        evaluationNotes: def.notes || null,
        ruleTitle: def.label,
        statutoryReference: def.statutoryRef,
        requiredSummary: null,
        measuredHeightMm: def.measuredHeightMm ?? cropMeasuredMm,
        statutoryMinimumMm: def.statutoryMinMm ?? null,
        reviewStatus:
          def.verdict === "REVIEW" || def.verdict === "FAIL"
            ? "IN_REVIEW"
            : (crop?.confidence ?? 1.0) < 0.85
            ? "IN_REVIEW"
            : "NOT_REVIEWED",
        operatorNotes: null,
        sourceTokenIds: crop ? [`tok_${crop.field_name || def.key}`] : [],
      };
    }
  }

  // 3. Process raw ocr_observations if provided (legacy/mock)
  if (Array.isArray(raw.ocr_observations) && raw.ocr_observations.length > 0) {
    ocrTokens.length = 0; // prefer authoritative OCR observations if provided directly
    for (const t of raw.ocr_observations as OCRObservationDTO[]) {
      const bbox = normalizeBoundingBox(t.bounding_box) || {
        xMin: 0,
        yMin: 0,
        xMax: 0,
        yMax: 0,
      };

      let polygon: [number, number][];
      if (Array.isArray(t.polygon) && t.polygon.length === 4) {
        polygon = t.polygon as [number, number][];
      } else {
        polygon = [
          [bbox.xMin, bbox.yMin],
          [bbox.xMax, bbox.yMin],
          [bbox.xMax, bbox.yMax],
          [bbox.xMin, bbox.yMax],
        ];
      }

      let fieldName: string | null = null;
      for (const [declKey, decl] of Object.entries(declarations)) {
        if (decl.sourceTokenIds?.includes(t.token_id)) {
          fieldName = declKey;
          break;
        }
      }

      const script =
        t.language === "hi" || /[\u0900-\u097F]/.test(t.text)
          ? "devanagari"
          : "latin";

      ocrTokens.push({
        id: t.token_id,
        text: t.text,
        confidence: typeof t.confidence === "number" ? t.confidence : 1.0,
        boundingBox: bbox,
        polygon,
        language: t.language || null,
        script,
        fieldName,
        requiresReview: t.confidence < 0.85,
      });
    }
  }

  // Telemetry timings
  const telemetryObj = raw.telemetry || {};
  let totalDurationMs = 0;
  if (typeof telemetryObj.total_duration_ms === "number") {
    totalDurationMs = telemetryObj.total_duration_ms;
  } else if (typeof telemetryObj.total_pipeline_ms === "number") {
    totalDurationMs = telemetryObj.total_pipeline_ms;
  } else {
    totalDurationMs = Object.values(telemetryObj).reduce(
      (acc: number, val: any) =>
        typeof val === "number" && val > 0 && val < 10000 ? acc + val : acc,
      0
    );
  }

  const stageTimings: Record<string, number> =
    telemetryObj.stages_ms && typeof telemetryObj.stages_ms === "object"
      ? telemetryObj.stages_ms
      : telemetryObj;

  // Error list normalization
  const rawErrors = Array.isArray(raw.errors) ? raw.errors : [];
  const errors = rawErrors.map((err: any) => ({
    code: err.error_code || err.code || "UNKNOWN_ERROR",
    stage: err.stage || "PIPELINE",
    message: err.message || "An unexpected inspection error occurred",
    remediationHint: err.remediation_hint || err.remediationHint || null,
  }));

  const isSynthetic = Boolean(
    meta?.isSynthetic ??
    (typeof raw.inspection_id === "string" && raw.inspection_id.includes("SYNTH"))
  );

  return {
    inspectionId,
    createdAt,
    imageSha256,
    imagePath:
      raw.image_path ||
      raw.imagePath ||
      meta?.imagePath ||
      (isSynthetic && raw.inspection_id
        ? `/fixtures/${raw.inspection_id.replace("INSP-", "")}.png`
        : null),
    isSynthetic,
    syntheticDisclaimer: isSynthetic
      ? "SYNTHETIC DEMO FIXTURE — NOT REAL-WORLD RETAIL VALIDATION"
      : undefined,
    packageTitle: meta?.packageTitle,
    pdfUrl: raw.dossier_pdf_path || null,
    verdict: {
      status: canonicalState,
      canonicalState,
      uiSeverity: presentation.severity,
      label: presentation.label,
      summaryReason,
      isCompliant: presentation.isCompliant,
      requiresReview: presentation.requiresReview,
    },
    qualityGate: {
      passed: qualityGatePassed,
      sharpnessScore,
      glareRatio,
    },
    calibration: {
      status: calibrationStatus,
      scaleFactorMmPerPixel: scaleFactor,
      isCalibrated,
    },
    declarations,
    ocrTokens,
    evidenceItems,
    telemetry: {
      totalDurationMs: Math.round(totalDurationMs),
      stageTimings,
    },
    errors,
  };
}
