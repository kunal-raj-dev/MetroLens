"use client";

import React, { useEffect, useRef, useId } from "react";
import { X } from "lucide-react";

export interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export function Dialog({
  isOpen,
  onClose,
  title,
  description,
  children,
  className = "",
}: DialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);
  const titleId = useId();
  const descriptionId = useId();
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement;
      dialogRef.current?.focus();
      const previousOverflow = document.body.style.overflow;

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Escape") {
          onCloseRef.current();
        }
        if (e.key === "Tab") {
          const nodes = Array.from(dialogRef.current?.querySelectorAll<HTMLElement>(
            'button:not([disabled]), a[href], input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex="0"]'
          ) || []).filter(node => node.getClientRects().length > 0);
          const first = nodes[0];
          const last = nodes[nodes.length - 1];
          if (!first) { e.preventDefault(); return; }
          if (e.shiftKey && (document.activeElement === first || document.activeElement === dialogRef.current)) {
            e.preventDefault(); last.focus();
          } else if (!e.shiftKey && (document.activeElement === last || document.activeElement === dialogRef.current)) {
            e.preventDefault(); first.focus();
          }
        }
      };

      document.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";

      return () => {
        document.removeEventListener("keydown", handleKeyDown);
        document.body.style.overflow = previousOverflow;
        previousActiveElement.current?.focus();
      };
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/50 backdrop-blur-md animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={description ? descriptionId : undefined}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={dialogRef}
        tabIndex={-1}
        className={`relative w-full max-w-xl max-h-[90dvh] overflow-y-auto rounded-stadium border border-black/[0.08] bg-white p-6 sm:p-10 shadow-deep focus:outline-none ${className}`}
      >
        <div className="flex items-start justify-between gap-4 pb-6 border-b border-black/[0.06]">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-eyebrow text-signal-orange">
              <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
              IMAGE ASSESSMENT GUIDE
            </div>
            <h3 id={titleId} className="text-2xl font-medium tracking-headline text-ink">
              {title}
            </h3>
            {description && (
              <p
                id={descriptionId}
                className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal"
              >
                {description}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full bg-canvas hover:bg-canvas-muted text-ink flex items-center justify-center transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-ink"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        <div className="mt-6">{children}</div>
      </div>
    </div>
  );
}
