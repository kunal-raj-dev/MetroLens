import React from "react";
import { Loader2 } from "lucide-react";

export interface LoadingStateProps {
  title?: string;
  description?: string;
  stageName?: string;
  className?: string;
}

export function LoadingState({
  title = "Analyzing Packaging Surface...",
  description = "Processing optical quality, reference scale, multilingual OCR, and statutory rules.",
  stageName,
  className = "",
}: LoadingStateProps) {
  return (
    <div
      className={`rounded-xl border border-surface-border bg-surface-card p-10 text-center flex flex-col items-center justify-center space-y-4 ${className}`}
      role="status"
      aria-live="polite"
    >
      <div className="relative flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-2 border-slate-800 border-t-emerald-500 animate-spin" />
        <Loader2 className="w-5 h-5 text-emerald-400 absolute animate-pulse" aria-hidden="true" />
      </div>
      <div className="space-y-1 max-w-md">
        <h4 className="text-base font-semibold text-white">{title}</h4>
        <p className="text-xs text-slate-400 leading-relaxed">{description}</p>
      </div>
      {stageName && (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px] font-mono text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
          Active: {stageName}
        </span>
      )}
    </div>
  );
}
