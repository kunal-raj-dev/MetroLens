import React, { HTMLAttributes } from "react";
import { Info, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

export interface AlertProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "info" | "warning" | "success" | "error";
  title?: string;
}

export function Alert({
  variant = "info",
  title,
  children,
  className = "",
  ...props
}: AlertProps) {
  const configs = {
    info: {
      icon: Info,
      containerClass: "border-link-blue/30 bg-[#EDF2FF] text-ink",
      iconClass: "text-link-blue",
      dotClass: "bg-link-blue",
    },
    warning: {
      icon: AlertTriangle,
      containerClass: "border-amber-300 bg-[#FFF8EB] text-ink",
      iconClass: "text-amber-700",
      dotClass: "bg-amber-600",
    },
    success: {
      icon: CheckCircle2,
      containerClass: "border-emerald-300 bg-[#EBF7F2] text-ink",
      iconClass: "text-emerald-700",
      dotClass: "bg-emerald-600",
    },
    error: {
      icon: XCircle,
      containerClass: "border-signal-orange/30 bg-[#FFF1EB] text-ink",
      iconClass: "text-signal-orange",
      dotClass: "bg-signal-orange",
    },
  };

  const config = configs[variant];
  const Icon = config.icon;

  return (
    <div
      role="alert"
      className={`rounded-2xl border p-5 flex items-start gap-4 text-sm shadow-sm ${config.containerClass} ${className}`}
      {...props}
    >
      <div className={`p-1.5 rounded-full bg-white shadow-sm flex-shrink-0 mt-0.5 ${config.iconClass}`}>
        <Icon className="w-4 h-4" aria-hidden="true" />
      </div>
      <div className="space-y-1">
        {title && (
          <h5 className="font-medium text-ink tracking-tight flex items-center gap-1.5">
            <span className={`w-1.5 h-1.5 rounded-full ${config.dotClass}`} />
            {title}
          </h5>
        )}
        <div className="text-xs sm:text-sm text-slate-700 leading-relaxed font-normal">
          {children}
        </div>
      </div>
    </div>
  );
}
