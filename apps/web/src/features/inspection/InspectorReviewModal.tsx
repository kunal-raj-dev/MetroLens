"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Dialog,
  Button,
  Badge,
  Alert,
} from "@/components/ui";
import {
  Sliders,
  CheckCircle2,
  AlertTriangle,
  FileCheck2,
  Scale,
  ShieldCheck,
  RotateCcw,
} from "lucide-react";
import {
  DeclarationModel,
  ReviewSubmissionInput,
  ReviewSubmissionResult,
  ReviewDecision,
} from "@/types/frontend";

export interface InspectorReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  declaration: DeclarationModel | null;
  inspectionId: string;
  onSubmitReview: (input: ReviewSubmissionInput) => Promise<ReviewSubmissionResult | void>;
  isSubmitting?: boolean;
  isMock?: boolean;
  onToggleCaliperMode?: () => void;
  isCaliperActive?: boolean;
  caliperPoints?: { pointA: any; pointB: any };
  onClearCaliperPoints?: () => void;
}

export function InspectorReviewModal({
  isOpen,
  onClose,
  declaration,
  inspectionId,
  onSubmitReview,
  isSubmitting = false,
  isMock = true,
  onToggleCaliperMode,
  isCaliperActive = false,
  caliperPoints,
  onClearCaliperPoints,
}: InspectorReviewModalProps) {
  const [decision, setDecision] = useState<ReviewDecision>("CONFIRMED");
  const [notes, setNotes] = useState("");
  const [status, setStatus] = useState<"IDLE" | "SUBMITTING" | "SUCCESS" | "ERROR">("IDLE");
  const [resultMessage, setResultMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const reviewVersion = useRef(0);

  // Reset state whenever a new declaration is opened
  useEffect(() => {
    reviewVersion.current += 1;
    if (isOpen) {
      setDecision("CONFIRMED");
      setNotes(declaration?.operatorNotes || "");
      setStatus("IDLE");
      setResultMessage(null);
      setErrorMessage(null);
    }
    return () => { reviewVersion.current += 1; };
  }, [isOpen, declaration, inspectionId]);

  if (!declaration) return null;

  const handleSubmit = async () => {
    if (!isMock || status === "SUBMITTING" || isSubmitting) return;
    const version = reviewVersion.current;
    setStatus("SUBMITTING");
    setErrorMessage(null);

    try {
      const result = await onSubmitReview({
        inspectionId,
        fieldName: declaration.fieldName,
        decision,
        notes: notes.trim() || undefined,
      });

      if (version !== reviewVersion.current) return;
      setStatus("SUCCESS");
      setResultMessage(
        result?.statusMessage || "Demonstration review updated in this browser session."
      );
    } catch (err: any) {
      if (version !== reviewVersion.current) return;
      setStatus("ERROR");
      setErrorMessage(err?.message || "Failed to submit inspector review.");
    }
  };

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title={`Inspector Review: ${declaration.label || declaration.fieldName}`}
      description={isMock ? "Practice reviewing extracted declarations. Changes last only in this browser session." : "Inspect the extracted evidence. Saving a live officer review is not available yet."}
      className="max-w-xl"
    >
      <div className="space-y-5 pt-2">
        {/* Synthetic Mode Disclosure */}
        {isMock && (
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-pill bg-amber-500/10 border border-amber-500/20 text-xs text-amber-800 font-semibold">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            SYNTHETIC DEMO REVIEW DISPATCH
          </div>
        )}

        {/* Declaration Context Card */}
        <div className="p-4 rounded-2xl bg-canvas border border-black/[0.06] space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-mono text-slate-500">
              Inspection Dossier: #{inspectionId}
            </span>
            <span className="text-[11px] font-mono text-slate-500">
              Confidence: {declaration.confidence == null ? "Not supplied" : `${(declaration.confidence * 100).toFixed(1)}%`}
            </span>
          </div>

          <div className="space-y-1">
            <div className="text-[10px] uppercase font-bold tracking-eyebrow text-slate-500">
              Verbatim Extracted Text
            </div>
            <div className="p-3 rounded-xl bg-white border border-black/[0.06] font-mono text-xs text-ink break-all">
              {declaration.rawText || <span className="text-red-500 italic">No text extracted</span>}
            </div>
          </div>

          <div className="text-[11px] text-slate-600 space-y-1">
            <div>
              <strong className="text-ink">Statutory Clause:</strong>{" "}
              {declaration.statutoryReference || "Rule 6(1), Legal Metrology Rules, 2011"}
            </div>
            {declaration.evaluationNotes && (
              <div>
                <strong className="text-ink">Pipeline Note:</strong> {declaration.evaluationNotes}
              </div>
            )}
          </div>
        </div>

        {/* Adjudication Decision Selection */}
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-eyebrow text-slate-700">
            Review Finding
          </label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              aria-pressed={decision === "CONFIRMED"}
              onClick={() => setDecision("CONFIRMED")}
              className={`p-3 rounded-xl border text-left flex items-start gap-2.5 transition-all ${
                decision === "CONFIRMED"
                  ? "bg-emerald-50/80 border-emerald-500 ring-2 ring-emerald-500/20"
                  : "bg-white border-black/[0.08] hover:border-black/20"
              }`}
            >
              <CheckCircle2 className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                decision === "CONFIRMED" ? "text-emerald-600" : "text-slate-400"
              }`} />
              <div className="space-y-0.5">
                <div className="text-xs font-semibold text-ink">Confirm Pass</div>
                <div className="text-[10px] text-slate-500">Mark extraction as reviewed</div>
              </div>
            </button>

            <button
              type="button"
              aria-pressed={decision === "FLAGGED"}
              onClick={() => setDecision("FLAGGED")}
              className={`p-3 rounded-xl border text-left flex items-start gap-2.5 transition-all ${
                decision === "FLAGGED"
                  ? "bg-red-50/80 border-red-500 ring-2 ring-red-500/20"
                  : "bg-white border-black/[0.08] hover:border-black/20"
              }`}
            >
              <AlertTriangle className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                decision === "FLAGGED" ? "text-red-600" : "text-slate-400"
              }`} />
              <div className="space-y-0.5">
                <div className="text-xs font-semibold text-ink">Flag Deficit</div>
                <div className="text-[10px] text-slate-500">Flag for further checking</div>
              </div>
            </button>
          </div>
        </div>

        {/* Inspector Notes Area */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <label htmlFor="inspector-notes" className="font-bold uppercase tracking-eyebrow text-slate-700">
              Officer Audit Notes
            </label>
            <span className="text-[10px] text-slate-400 font-mono">
              {notes.length}/500 chars
            </span>
          </div>
          <textarea
            id="inspector-notes"
            rows={3}
            maxLength={500}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Enter reason for confirmation or citation of non-compliance..."
            className="w-full p-3 rounded-xl border border-black/[0.1] text-xs font-mono focus:outline-none focus:ring-2 focus:ring-signal-orange focus:border-signal-orange transition-all resize-none"
          />
        </div>

        {/* Status Alerts */}
        {status === "SUCCESS" && (
          <Alert variant="success" title="Review Decision Recorded">
            <p className="text-xs leading-relaxed">{resultMessage}</p>
          </Alert>
        )}

        {status === "ERROR" && (
          <Alert variant="error" title="Review Dispatch Failed">
            <p className="text-xs leading-relaxed">{errorMessage}</p>
          </Alert>
        )}

        {/* Modal Footer Controls */}
        <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-black/[0.06]">
          <Button
            variant="secondary"
            size="sm"
            onClick={onClose}
            disabled={status === "SUBMITTING"}
          >
            {status === "SUCCESS" ? "Close" : "Cancel"}
          </Button>

          {status !== "SUCCESS" && (
            <Button
              variant="primary"
              size="sm"
              onClick={handleSubmit}
              disabled={!isMock || isSubmitting || status === "SUBMITTING"}
            >
              {status === "SUBMITTING" ? "Updating demo..." : isMock ? "Update Demo Review" : "Live review unavailable"}
            </Button>
          )}
        </div>
      </div>
    </Dialog>
  );
}
