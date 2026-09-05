"use client";

import React from "react";
import {
  FileCheck2,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Eye,
  Sliders,
  Sparkles,
  Search,
} from "lucide-react";
import { Badge, Button, Card, Tooltip } from "@/components/ui";
import { DeclarationModel } from "@/types/frontend";
import { RuleVerdict } from "@/types/contract";

export interface DeclarationTableProps {
  declarations: Record<string, DeclarationModel>;
  selectedFieldName?: string | null;
  selectedDeclarationKey?: string | null;
  onSelectDeclaration?: (key: string) => void;
  onViewEvidence?: (declaration: DeclarationModel) => void;
  onFocusCanvasTokens?: (tokenIds: string[]) => void;
  onOpenReview?: (declaration: DeclarationModel) => void;
  onOpenReviewModal?: (declaration: DeclarationModel) => void;
  isSynthetic?: boolean;
  className?: string;
}

export function DeclarationTable({
  declarations,
  selectedFieldName = null,
  selectedDeclarationKey = null,
  onSelectDeclaration,
  onViewEvidence,
  onFocusCanvasTokens,
  onOpenReview,
  onOpenReviewModal,
  isSynthetic = false,
  className = "",
}: DeclarationTableProps) {
  const activeKey = selectedFieldName || selectedDeclarationKey;
  const entries = Object.entries(declarations);

  if (entries.length === 0) {
    return (
      <Card shape="stadium" variant="lifted" className={`p-6 text-center text-slate-500 text-xs ${className}`}>
        No statutory declarations extracted from this packaging frame.
      </Card>
    );
  }

  const getVerdictBadge = (verdict?: RuleVerdict, isPresent?: boolean) => {
    if (!isPresent) {
      return <Badge variant="danger">Missing</Badge>;
    }
    switch (verdict) {
      case "PASS":
        return <Badge variant="success">Rule 6 Pass</Badge>;
      case "FAIL":
        return <Badge variant="danger">Statutory Deficit</Badge>;
      case "REVIEW":
        return <Badge variant="warning">Requires Review</Badge>;
      default:
        return <Badge variant="default">Verified Present</Badge>;
    }
  };

  return (
    <Card shape="stadium" variant="lifted" className={`p-6 sm:p-8 space-y-5 ${className}`}>
      {/* Table Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-black/[0.06] pb-4">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-eyebrow text-slate-500">
            <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
            STATUTORY DECLARATION AUDIT TABLE
          </div>
          <h3 className="text-xl font-medium tracking-headline text-ink mt-0.5">
            Rule 6 Mandatory Declarations Matrix
          </h3>
        </div>
        <div className="text-xs text-slate-500 font-mono">
          {entries.length} statutory fields evaluated
        </div>
      </div>

      {/* Desktop / Tablet Table View (Hidden on mobile < 768px) */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-black/[0.08] text-[11px] uppercase tracking-eyebrow text-slate-500 font-bold">
              <th scope="col" className="py-3 px-3">Mandatory Field</th>
              <th scope="col" className="py-3 px-3">Observed OCR Text</th>
              <th scope="col" className="py-3 px-3">Legal Status</th>
              <th scope="col" className="py-3 px-3">Confidence</th>
              <th scope="col" className="py-3 px-3">Metric Numeral</th>
              <th scope="col" className="py-3 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-black/[0.04]">
            {entries.map(([key, decl]) => {
              const isSelected = activeKey === key;
              return (
                <tr
                  key={key}
                  className={`transition-colors ${
                    isSelected ? "bg-signal-orange/5" : "hover:bg-slate-50/70"
                  }`}
                >
                  <td className="py-3.5 px-3 font-semibold text-ink whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <span
                        className={`w-2 h-2 rounded-full flex-shrink-0 ${
                          decl.verdict === "FAIL"
                            ? "bg-red-500"
                            : decl.verdict === "REVIEW"
                            ? "bg-amber-500"
                            : "bg-emerald-500"
                        }`}
                      />
                      <span>{decl.label || decl.fieldName}</span>
                    </div>
                  </td>

                  <td className="py-3.5 px-3 max-w-[220px]">
                    <div className="font-mono text-slate-700 truncate" title={decl.rawText}>
                      {decl.rawText || <span className="text-red-500 font-sans italic">Not Detected</span>}
                    </div>
                    {decl.normalizedValue && typeof decl.normalizedValue === "object" && (
                      <div className="text-[10px] text-slate-500 font-mono">
                        Norm: {JSON.stringify(decl.normalizedValue)}
                      </div>
                    )}
                  </td>

                  <td className="py-3.5 px-3 whitespace-nowrap">
                    {getVerdictBadge(decl.verdict, decl.isPresent)}
                  </td>

                  <td className="py-3.5 px-3 whitespace-nowrap font-mono text-slate-600">
                    {(decl.confidence * 100).toFixed(1)}%
                  </td>

                  <td className="py-3.5 px-3 whitespace-nowrap font-mono text-slate-600">
                    {decl.measuredHeightMm ? (
                      <span className={decl.statutoryMinimumMm && decl.measuredHeightMm < decl.statutoryMinimumMm ? "text-red-600 font-semibold" : "text-emerald-700"}>
                        {decl.measuredHeightMm.toFixed(2)} mm
                        {decl.statutoryMinimumMm && ` (min: ${decl.statutoryMinimumMm.toFixed(1)}mm)`}
                      </span>
                    ) : (
                      <span className="text-slate-400">N/A</span>
                    )}
                  </td>

                  <td className="py-3.5 px-3 whitespace-nowrap text-right space-x-2">
                    {decl.sourceTokenIds && decl.sourceTokenIds.length > 0 && (
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => {
                          onSelectDeclaration?.(key);
                          if (onViewEvidence) onViewEvidence(decl);
                          if (onFocusCanvasTokens) onFocusCanvasTokens(decl.sourceTokenIds || []);
                        }}
                        title="Locate token on evidence canvas"
                      >
                        <Eye className="w-3.5 h-3.5 mr-1 text-slate-500" />
                        Canvas
                      </Button>
                    )}

                    <Button
                      size="sm"
                      variant="primary"
                      onClick={() => {
                        if (onOpenReview) onOpenReview(decl);
                        if (onOpenReviewModal) onOpenReviewModal(decl);
                      }}
                    >
                      <Sliders className="w-3.5 h-3.5 mr-1" />
                      Review
                    </Button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Mobile Card List View (< 768px) */}
      <div className="md:hidden space-y-3">
        {entries.map(([key, decl]) => {
          const isSelected = activeKey === key;
          return (
            <div
              key={key}
              className={`p-4 rounded-2xl border transition-all ${
                isSelected
                  ? "bg-signal-orange/5 border-signal-orange shadow-sm"
                  : "bg-white border-black/[0.08]"
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="font-semibold text-sm text-ink flex items-center gap-1.5">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      decl.verdict === "FAIL"
                        ? "bg-red-500"
                        : decl.verdict === "REVIEW"
                        ? "bg-amber-500"
                        : "bg-emerald-500"
                    }`}
                  />
                  <span>{decl.label || decl.fieldName}</span>
                </div>
                {getVerdictBadge(decl.verdict, decl.isPresent)}
              </div>

              <div className="text-xs font-mono bg-canvas p-2.5 rounded-xl border border-black/[0.04] text-slate-700 mb-3 break-all">
                {decl.rawText || <span className="text-red-500 italic">Not Detected</span>}
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-500 mb-3 font-mono">
                <div>Confidence: {(decl.confidence * 100).toFixed(1)}%</div>
                <div>Height: {decl.measuredHeightMm ? `${decl.measuredHeightMm.toFixed(2)} mm` : "N/A"}</div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-1 border-t border-black/[0.06]">
                {decl.sourceTokenIds && decl.sourceTokenIds.length > 0 && (
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => {
                      onSelectDeclaration?.(key);
                      if (onViewEvidence) onViewEvidence(decl);
                      if (onFocusCanvasTokens) onFocusCanvasTokens(decl.sourceTokenIds || []);
                    }}
                  >
                    <Eye className="w-3.5 h-3.5 mr-1" />
                    Canvas
                  </Button>
                )}
                <Button
                  size="sm"
                  variant="primary"
                  onClick={() => {
                    if (onOpenReview) onOpenReview(decl);
                    if (onOpenReviewModal) onOpenReviewModal(decl);
                  }}
                >
                  <Sliders className="w-3.5 h-3.5 mr-1" />
                  Review
                </Button>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
