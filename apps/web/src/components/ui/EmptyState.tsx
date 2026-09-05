import React from "react";
import { UploadCloud, FileSearch, ShieldAlert, ArrowUpRight } from "lucide-react";
import { Button } from "./Button";

export interface EmptyStateProps {
  title?: string;
  description?: string;
  onActionClick?: () => void;
  actionText?: string;
  iconType?: "upload" | "search" | "alert";
  className?: string;
}

export function EmptyState({
  title = "Ready for Package Inspection",
  description = "Upload a high-resolution front Principal Display Panel (PDP) photograph. The system will evaluate frame quality, metric scale, multilingual declarations, and numeral heights.",
  onActionClick,
  actionText = "Select Package Image",
  iconType = "upload",
  className = "",
}: EmptyStateProps) {
  const icons = {
    upload: UploadCloud,
    search: FileSearch,
    alert: ShieldAlert,
  };

  const Icon = icons[iconType] || UploadCloud;

  return (
    <div
      className={`rounded-stadium border border-black/[0.06] bg-canvas-lifted p-8 sm:p-14 text-center flex flex-col items-center justify-center space-y-6 shadow-halo relative overflow-hidden ${className}`}
      role="region"
      aria-label="Empty Workspace State"
    >
      {/* Mastercard-Style Circular Focal Point with Satellite Moon CTA */}
      <div className="relative flex items-center justify-center my-2">
        {/* Main Circular Portrait Focal */}
        <div className="w-28 h-28 sm:w-32 sm:h-32 rounded-full bg-canvas border-2 border-black/[0.06] flex items-center justify-center shadow-sm relative z-10 transition-transform duration-300 hover:scale-105">
          <Icon className="w-10 h-10 text-ink/70" aria-hidden="true" />
        </div>

        {/* Attached White Satellite Micro-CTA docked bottom-right */}
        <div
          className="absolute -bottom-2 -right-2 z-20 w-12 h-12 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta cursor-pointer group"
          onClick={onActionClick}
          role="button"
          tabIndex={0}
          aria-label="Upload packaging photo"
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              onActionClick?.();
            }
          }}
        >
          <ArrowUpRight className="w-5 h-5 text-signal-orange transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </div>
      </div>

      {/* Eyebrow and Content */}
      <div className="space-y-2 max-w-lg">
        <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-eyebrow text-slate-500">
          <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
          PHOTOGRAPHIC INGESTION PORTAL
        </div>
        <h3 className="text-2xl sm:text-3xl font-medium tracking-headline text-ink">
          {title}
        </h3>
        <p className="text-sm text-slate-600 leading-relaxed max-w-md mx-auto pt-1 font-normal">
          {description}
        </p>
      </div>

      {/* Primary Ink Pill Button */}
      {onActionClick && (
        <div className="pt-2">
          <Button
            variant="primary"
            size="md"
            onClick={onActionClick}
          >
            {actionText}
          </Button>
        </div>
      )}
    </div>
  );
}
