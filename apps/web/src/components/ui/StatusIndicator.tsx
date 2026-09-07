import React from "react";
import { ShieldCheck, AlertTriangle, HelpCircle, FileQuestion, LucideIcon } from "lucide-react";
import { OverallVerdict } from "@/types/contract";

export interface StatusIndicatorProps {
  verdict: OverallVerdict;
  summaryReason?: string;
  className?: string;
  showExplanation?: boolean;
  size?: "compact" | "banner";
}

interface StateConfig {
  label: string;
  eyebrow: string;
  defaultExplanation: string;
  icon: LucideIcon;
  dotColor: string;
  containerClass: string;
  iconClass: string;
  compactClass: string;
}

const COMPLIANT_CONFIG: StateConfig = {
  label: "Compliant with Legal Metrology Standards",
  eyebrow: "COMPLIANT",
  defaultExplanation:
    "All mandatory declarations detected; measured numeral heights meet Rule 7 Table-I minimum thresholds under statutory surveillance.",
  icon: ShieldCheck,
  dotColor: "bg-emerald-600",
  containerClass:
    "border-verdict-compliant-border bg-verdict-compliant-bg text-ink",
  iconClass: "bg-white text-verdict-compliant border border-verdict-compliant-border shadow-sm",
  compactClass: "bg-verdict-compliant-bg text-verdict-compliant-text border-verdict-compliant-border",
};

const NO_IMAGE_VERIFIABLE_CONFIG: StateConfig = {
  label: "No Image-Verifiable Violations Detected",
  eyebrow: "NO IMAGE-VERIFIABLE VIOLATIONS",
  defaultExplanation:
    "All image-verifiable mandatory declarations strictly satisfy the Legal Metrology (Packaged Commodities) Rules, 2011 on this panel.",
  icon: ShieldCheck,
  dotColor: "bg-emerald-600",
  containerClass:
    "border-verdict-compliant-border bg-verdict-compliant-bg text-ink",
  iconClass: "bg-white text-verdict-compliant border border-verdict-compliant-border shadow-sm",
  compactClass: "bg-verdict-compliant-bg text-verdict-compliant-text border-verdict-compliant-border",
};

const NON_COMPLIANT_CONFIG: StateConfig = {
  label: "Statutory Non-Compliance Detected",
  eyebrow: "STATUTORY NON-COMPLIANCE",
  defaultExplanation:
    "One or more statutory requirements under Rule 6, Rule 7 font matrix, or Rule 6(11) Unit Sale Price fail statutory criteria. Section 36(1) review notice generated.",
  icon: AlertTriangle,
  dotColor: "bg-signal-orange",
  containerClass:
    "border-verdict-noncompliant-border bg-verdict-noncompliant-bg text-ink",
  iconClass: "bg-white text-signal-orange border border-verdict-noncompliant-border shadow-sm",
  compactClass: "bg-verdict-noncompliant-bg text-verdict-noncompliant-text border-verdict-noncompliant-border",
};

const POTENTIAL_NON_COMPLIANCE_CONFIG: StateConfig = {
  label: "Potential Statutory Non-Compliance Detected",
  eyebrow: "POTENTIAL NON-COMPLIANCE",
  defaultExplanation:
    "Potential statutory discrepancy detected requiring verification. Section 36(1) improvement notice recommended.",
  icon: AlertTriangle,
  dotColor: "bg-signal-orange",
  containerClass:
    "border-verdict-noncompliant-border bg-verdict-noncompliant-bg text-ink",
  iconClass: "bg-white text-signal-orange border border-verdict-noncompliant-border shadow-sm",
  compactClass: "bg-verdict-noncompliant-bg text-verdict-noncompliant-text border-verdict-noncompliant-border",
};

const REVIEW_CONFIG: StateConfig = {
  label: "Inspector Manual Review Required",
  eyebrow: "MANUAL REVIEW REQUIRED",
  defaultExplanation:
    "Automatic reference scale fiducial was absent or occluded, optical quality is degraded, or font measurement lies within statutory uncertainty bounds (±0.15mm).",
  icon: HelpCircle,
  dotColor: "bg-amber-600",
  containerClass:
    "border-verdict-review-border bg-verdict-review-bg text-ink",
  iconClass: "bg-white text-signal-clay border border-verdict-review-border shadow-sm",
  compactClass: "bg-verdict-review-bg text-verdict-review-text border-verdict-review-border",
};

const FLAGGED_FOR_REVIEW_CONFIG: StateConfig = {
  label: "Flagged for Officer Review",
  eyebrow: "FLAGGED FOR REVIEW",
  defaultExplanation:
    "Image quality gate check failed or optical ambiguity detected. Flagged for mandatory inspecting officer review.",
  icon: HelpCircle,
  dotColor: "bg-amber-600",
  containerClass:
    "border-verdict-review-border bg-verdict-review-bg text-ink",
  iconClass: "bg-white text-signal-clay border border-verdict-review-border shadow-sm",
  compactClass: "bg-verdict-review-bg text-verdict-review-text border-verdict-review-border",
};

const EXEMPTION_CONFIG: StateConfig = {
  label: "Statutory Exemption Applied (Rule 26 / Rule 3)",
  eyebrow: "STATUTORY EXEMPTION APPLIED",
  defaultExplanation:
    "Package qualifies for statutory exemption under Rule 26 or Rule 3 of the Legal Metrology (Packaged Commodities) Rules, 2011. Standard declaration violation flags suppressed.",
  icon: ShieldCheck,
  dotColor: "bg-blue-600",
  containerClass: "border-blue-200 bg-blue-50/70 text-ink",
  iconClass: "bg-white text-blue-600 border border-blue-200 shadow-sm",
  compactClass: "bg-blue-50 text-blue-700 border-blue-200",
};

const EXEMPTED_CONFIG: StateConfig = {
  label: "Statutory Exemption (Rule 26 / Rule 3)",
  eyebrow: "EXEMPTED",
  defaultExplanation:
    "Package qualifies for statutory exemption under Rule 26 or Rule 3 of the Legal Metrology (Packaged Commodities) Rules, 2011.",
  icon: ShieldCheck,
  dotColor: "bg-blue-600",
  containerClass: "border-blue-200 bg-blue-50/70 text-ink",
  iconClass: "bg-white text-blue-600 border border-blue-200 shadow-sm",
  compactClass: "bg-blue-50 text-blue-700 border-blue-200",
};

const NOT_VERIFIABLE_CONFIG: StateConfig = {
  label: "Not Image Verifiable / Physical Audit Required",
  eyebrow: "NOT IMAGE VERIFIABLE",
  defaultExplanation:
    "Statutory check requires physical weighing scale audit (Rule 24), laboratory analysis, or cannot be determined reliably from 2D surface imagery.",
  icon: FileQuestion,
  dotColor: "bg-slate-500",
  containerClass:
    "border-verdict-inconclusive-border bg-verdict-inconclusive-bg text-ink",
  iconClass: "bg-white text-slate-600 border border-verdict-inconclusive-border shadow-sm",
  compactClass: "bg-verdict-inconclusive-bg text-verdict-inconclusive-text border-verdict-inconclusive-border",
};

const INCONCLUSIVE_CONFIG: StateConfig = {
  label: "Inconclusive Inspection",
  eyebrow: "INCONCLUSIVE",
  defaultExplanation:
    "Inspection could not reach a definitive legal verdict due to optical or frame conditions.",
  icon: FileQuestion,
  dotColor: "bg-slate-500",
  containerClass:
    "border-verdict-inconclusive-border bg-verdict-inconclusive-bg text-ink",
  iconClass: "bg-white text-slate-600 border border-verdict-inconclusive-border shadow-sm",
  compactClass: "bg-verdict-inconclusive-bg text-verdict-inconclusive-text border-verdict-inconclusive-border",
};

const VERDICT_CONFIGS: Record<OverallVerdict, StateConfig> = {
  COMPLIANT: COMPLIANT_CONFIG,
  NO_IMAGE_VERIFIABLE_VIOLATIONS: NO_IMAGE_VERIFIABLE_CONFIG,
  NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED: NO_IMAGE_VERIFIABLE_CONFIG,
  NON_COMPLIANT: NON_COMPLIANT_CONFIG,
  POTENTIAL_NON_COMPLIANCE: POTENTIAL_NON_COMPLIANCE_CONFIG,
  FLAGGED_FOR_REVIEW: FLAGGED_FOR_REVIEW_CONFIG,
  MANUAL_REVIEW_REQUIRED: REVIEW_CONFIG,
  SUSPECT_REVIEW: REVIEW_CONFIG,
  EXEMPTED: EXEMPTED_CONFIG,
  STATUTORY_EXEMPTION_APPLIED: EXEMPTION_CONFIG,
  NOT_IMAGE_VERIFIABLE: NOT_VERIFIABLE_CONFIG,
  INCONCLUSIVE: INCONCLUSIVE_CONFIG,
};

export function StatusIndicator({
  verdict,
  summaryReason,
  className = "",
  showExplanation = true,
  size = "banner",
}: StatusIndicatorProps) {
  const config = VERDICT_CONFIGS[verdict] || REVIEW_CONFIG;
  const Icon = config.icon;
  const explanation = summaryReason || config.defaultExplanation;

  if (size === "compact") {
    return (
      <span
        className={`inline-flex items-center gap-2 px-3.5 py-1 rounded-pill text-xs font-bold tracking-eyebrow uppercase border select-none ${config.compactClass} ${className}`}
        role="status"
        aria-label={`Compliance Status: ${config.label}`}
      >
        <span className={`w-1.5 h-1.5 rounded-full ${config.dotColor}`} />
        <Icon className="w-3.5 h-3.5 flex-shrink-0" aria-hidden="true" />
        <span>{config.eyebrow}</span>
      </span>
    );
  }

  return (
    <div
      className={`rounded-3xl border p-6 sm:p-7 shadow-lift transition-all ${config.containerClass} ${className}`}
      role="region"
      aria-label="Inspection Verdict Summary"
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-5">
        <div className="flex items-start gap-4">
          <div
            className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${config.iconClass}`}
            aria-hidden="true"
          >
            <Icon className="w-6 h-6" />
          </div>
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="inline-flex items-center gap-1.5 text-[11px] font-bold tracking-eyebrow uppercase text-slate-700">
                <span className={`w-1.5 h-1.5 rounded-full ${config.dotColor}`} />
                {config.eyebrow}
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-medium tracking-headline text-ink">
              {config.label}
            </h2>
            {showExplanation && (
              <p className="text-sm text-slate-700 leading-relaxed max-w-3xl pt-0.5">
                {explanation}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
