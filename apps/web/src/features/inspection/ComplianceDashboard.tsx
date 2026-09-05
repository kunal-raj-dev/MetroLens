"use client";

import React from "react";
import {
  CheckCircle2,
  AlertTriangle,
  Scale,
  Clock,
  FileCheck2,
  Lock,
  Layers,
  Sparkles,
  Info,
  ShieldAlert,
  HelpCircle,
} from "lucide-react";
import { Card, Badge, Alert, StatusIndicator } from "@/components/ui";
import { FrontendInspectionModel, OCRTokenModel } from "@/types/frontend";

export interface ComplianceDashboardProps {
  inspection: FrontendInspectionModel | null;
  selectedTokenId?: string | null;
  onSelectToken?: (tokenId: string | null) => void;
  className?: string;
}

export function ComplianceDashboard({
  inspection,
  selectedTokenId,
  onSelectToken,
  className = "",
}: ComplianceDashboardProps) {
  if (!inspection) {
    return (
      <Card
        shape="stadium"
        variant="lifted"
        className={`p-8 text-center flex flex-col items-center justify-center space-y-3 min-h-[300px] ${className}`}
      >
        <div className="w-14 h-14 rounded-full bg-canvas flex items-center justify-center border border-black/[0.06]">
          <Layers className="w-6 h-6 text-slate-400" />
        </div>
        <h3 className="text-lg font-medium tracking-headline text-ink">
          Compliance Dashboard Standby
        </h3>
        <p className="text-xs text-slate-500 max-w-sm">
          Select or upload a packaging front panel photograph on the left to initiate statutory
          audit under the Legal Metrology Rules, 2011.
        </p>
      </Card>
    );
  }

  const selectedToken = selectedTokenId
    ? inspection.ocrTokens.find((t) => t.id === selectedTokenId)
    : null;

  const totalTokens = inspection.ocrTokens.length;
  const reviewTokens = inspection.ocrTokens.filter((t) => t.requiresReview).length;
  const declarationCount = Object.keys(inspection.declarations).length;

  return (
    <div className={`space-y-6 ${className}`}>
      {/* 1. Authoritative Multi-Modal Statutory Status Indicator */}
      <StatusIndicator
        verdict={inspection.verdict.status}
        summaryReason={inspection.verdict.summaryReason}
      />

      {/* 2. Synthetic Demo Warning Notice (Transparent Disclosure) */}
      {inspection.isSynthetic && (
        <Alert
          variant="warning"
          title="Synthetic Regression Demo Asset"
          className="border-amber-300 bg-amber-50/50"
        >
          <p className="text-xs text-slate-700 leading-relaxed">
            {inspection.syntheticDisclaimer ||
              "This output is generated from a synthetic regression fixture and must NOT be interpreted as real-world retail packaging validation."}
          </p>
        </Alert>
      )}

      {/* 3. Primary Metrics & Statutory Telemetry Grid */}
      <Card shape="stadium" variant="lifted" className="p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-black/[0.06] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold uppercase tracking-eyebrow text-slate-500">
                INSPECTION DOSSIER
              </span>
              <span className="font-mono text-xs font-semibold text-ink bg-canvas px-2 py-0.5 rounded-md border border-black/[0.06]">
                #{inspection.inspectionId}
              </span>
            </div>
            <h3 className="text-xl font-medium tracking-headline text-ink mt-0.5">
              {inspection.packageTitle || "Statutory Packaging Verification"}
            </h3>
          </div>

          <div className="flex items-center gap-2">
            <Badge
              variant={
                inspection.verdict.status === "COMPLIANT"
                  ? "success"
                  : inspection.verdict.status === "NON_COMPLIANT"
                  ? "danger"
                  : "warning"
              }
              size="sm"
            >
              {inspection.verdict.label}
            </Badge>

            {inspection.isSynthetic && (
              <Badge variant="outline" size="sm">
                Synthetic
              </Badge>
            )}
          </div>
        </div>

        {/* 4-Pillar Metric Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {/* Quality Gate */}
          <div className="bg-canvas p-3.5 rounded-2xl border border-black/[0.04] space-y-1">
            <div className="text-[10px] uppercase font-bold tracking-eyebrow text-slate-500">
              Quality Gate
            </div>
            <div className="text-sm font-semibold text-ink flex items-center gap-1.5">
              {inspection.qualityGate.passed ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                  <span>Passed</span>
                </>
              ) : (
                <>
                  <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
                  <span>Sub-optimal</span>
                </>
              )}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              Sharpness: {inspection.qualityGate.sharpnessScore?.toFixed(1) ?? "N/A"}
            </div>
          </div>

          {/* Metric Calibration */}
          <div className="bg-canvas p-3.5 rounded-2xl border border-black/[0.04] space-y-1">
            <div className="text-[10px] uppercase font-bold tracking-eyebrow text-slate-500">
              Calibration
            </div>
            <div className="text-sm font-semibold text-ink flex items-center gap-1.5">
              <Scale className="w-4 h-4 text-link-blue flex-shrink-0" />
              <span className="truncate">
                {inspection.calibration.status === "CALIBRATED"
                  ? "Calibrated"
                  : inspection.calibration.status === "APPROXIMATE_ASSISTED"
                  ? "Assisted"
                  : "Uncalibrated"}
              </span>
            </div>
            <div className="text-[10px] text-slate-500 font-mono truncate">
              {inspection.calibration.scaleFactorMmPerPixel
                ? `${inspection.calibration.scaleFactorMmPerPixel.toFixed(3)} mm/px`
                : "No anchor"}
            </div>
          </div>

          {/* Telemetry / Latency */}
          <div className="bg-canvas p-3.5 rounded-2xl border border-black/[0.04] space-y-1">
            <div className="text-[10px] uppercase font-bold tracking-eyebrow text-slate-500">
              Latency
            </div>
            <div className="text-sm font-semibold text-ink flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-slate-600 flex-shrink-0" />
              <span>{inspection.telemetry.totalDurationMs} ms</span>
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              {inspection.isSynthetic ? "Synthetic latency" : "Pipeline latency"}
            </div>
          </div>

          {/* OCR Evidence Tokens */}
          <div className="bg-canvas p-3.5 rounded-2xl border border-black/[0.04] space-y-1">
            <div className="text-[10px] uppercase font-bold tracking-eyebrow text-slate-500">
              Evidence Tokens
            </div>
            <div className="text-sm font-semibold text-ink flex items-center gap-1.5">
              <FileCheck2 className="w-4 h-4 text-signal-orange flex-shrink-0" />
              <span>{totalTokens} Extracted</span>
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              {reviewTokens > 0 ? (
                <span className="text-amber-600 font-medium">{reviewTokens} require review</span>
              ) : (
                <span className="text-emerald-700 font-medium">All high certainty</span>
              )}
            </div>
          </div>
        </div>

        {/* 4. Selected Token Detail Inspection Callout */}
        {selectedToken ? (
          <div className="p-4 rounded-2xl bg-signal-orange/5 border border-signal-orange/20 space-y-2">
            <div className="flex items-center justify-between">
              <div className="inline-flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-signal-orange animate-pulse" />
                <span className="text-xs font-bold uppercase tracking-eyebrow text-ink">
                  Selected Evidence Token [{selectedToken.id}]
                </span>
              </div>
              <button
                type="button"
                onClick={() => onSelectToken?.(null)}
                className="text-[11px] text-slate-500 hover:text-ink underline"
              >
                Clear Selection
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
              <div className="sm:col-span-2 space-y-0.5">
                <div className="text-[10px] uppercase tracking-eyebrow text-slate-500">Verbatim OCR Text</div>
                <div className="text-sm font-semibold text-ink font-mono bg-white p-2 rounded-lg border border-black/[0.06] select-all">
                  {selectedToken.text}
                </div>
              </div>

              <div className="space-y-1">
                <div className="text-[10px] uppercase tracking-eyebrow text-slate-500">Model Confidence</div>
                <div className="text-xs font-semibold text-ink">
                  {(selectedToken.confidence * 100).toFixed(1)}%{" "}
                  <span className="text-slate-500 font-normal">
                    ({selectedToken.script || "latin"})
                  </span>
                </div>
                {selectedToken.fieldName && (
                  <div className="text-[11px] text-signal-orange font-medium">
                    Mapped: {selectedToken.fieldName.replace(/_/g, " ")}
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="p-3.5 rounded-2xl bg-canvas border border-black/[0.04] text-center text-xs text-slate-500">
            Click any OCR polygon on the canvas below to inspect token geometry, confidence, and verbatim text.
          </div>
        )}

        {/* 5. Detected Declarations Chips */}
        {declarationCount > 0 && (
          <div className="space-y-2.5">
            <div className="text-xs font-bold uppercase tracking-eyebrow text-slate-500">
              Verified Rule 6 Declarations ({declarationCount})
            </div>
            <div className="flex flex-wrap gap-2">
              {Object.entries(inspection.declarations).map(([key, decl]) => (
                <div
                  key={key}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-pill bg-white border border-black/[0.08] shadow-sm text-xs"
                >
                  <span
                    className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      decl.verdict === "FAIL"
                        ? "bg-red-500"
                        : decl.verdict === "REVIEW"
                        ? "bg-amber-500"
                        : "bg-emerald-500"
                    }`}
                  />
                  <span className="font-semibold text-ink">{decl.label}:</span>
                  <span className="text-slate-600 font-mono truncate max-w-[180px]">
                    {decl.rawText || "Missing"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
