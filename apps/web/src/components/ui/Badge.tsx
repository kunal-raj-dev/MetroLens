import React, { HTMLAttributes } from "react";

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "success" | "danger" | "warning" | "info" | "outline";
  size?: "sm" | "md";
  showDot?: boolean;
}

export function Badge({
  className = "",
  variant = "default",
  size = "md",
  showDot = true,
  children,
  ...props
}: BadgeProps) {
  const baseStyles =
    "inline-flex items-center font-bold tracking-eyebrow uppercase rounded-pill border select-none transition-colors";

  const sizeStyles = {
    sm: "px-2.5 py-0.5 text-[10px] gap-1.5",
    md: "px-3.5 py-1 text-xs gap-2",
  };

  const dotColors = {
    default: "bg-ink",
    success: "bg-emerald-600",
    danger: "bg-signal-orange",
    warning: "bg-amber-600",
    info: "bg-link-blue",
    outline: "bg-slate-500",
  };

  const variantStyles = {
    default: "bg-white text-ink border-black/[0.08] shadow-sm",
    success: "bg-verdict-compliant-bg text-verdict-compliant-text border-verdict-compliant-border",
    danger: "bg-verdict-noncompliant-bg text-verdict-noncompliant-text border-verdict-noncompliant-border",
    warning: "bg-verdict-review-bg text-verdict-review-text border-verdict-review-border",
    info: "bg-verdict-exemption-bg text-verdict-exemption-text border-verdict-exemption-border",
    outline: "bg-transparent text-slate-700 border-black/15",
  };

  return (
    <span
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {showDot && (
        <span
          className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${dotColors[variant]}`}
          aria-hidden="true"
        />
      )}
      <span>{children}</span>
    </span>
  );
}
