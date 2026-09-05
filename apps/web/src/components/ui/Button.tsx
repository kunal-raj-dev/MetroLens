import React, { ButtonHTMLAttributes, forwardRef } from "react";
import { ArrowRight } from "lucide-react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "signal" | "outline" | "ghost" | "satellite";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = "primary",
      size = "md",
      isLoading = false,
      disabled,
      className = "",
      ...props
    },
    ref
  ) => {
    // If it's a satellite circular CTA button
    if (variant === "satellite") {
      return (
        <button
          ref={ref}
          disabled={disabled || isLoading}
          className={`w-14 h-14 rounded-full bg-white text-ink border border-black/[0.06] shadow-halo satellite-cta flex items-center justify-center focus-visible:ring-2 focus-visible:ring-ink focus-visible:ring-offset-2 transition-all disabled:opacity-50 disabled:pointer-events-none group ${className}`}
          aria-label={props["aria-label"] || "Action CTA"}
          {...props}
        >
          {children || (
            <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-0.5 text-ink" />
          )}
        </button>
      );
    }

    const baseStyles =
      "inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ink focus-visible:ring-offset-2 focus-visible:ring-offset-canvas disabled:opacity-50 disabled:pointer-events-none select-none active:scale-[0.98]";

    const sizeStyles = {
      sm: "px-4 py-1.5 text-xs gap-1.5 rounded-cta",
      md: "px-6 py-2 text-sm gap-2 rounded-cta",
      lg: "px-8 py-3 text-base gap-2.5 rounded-cta",
    };

    const variantStyles = {
      primary:
        "bg-ink text-canvas hover:bg-black active:bg-ink shadow-sm border border-ink",
      secondary:
        "bg-white text-ink hover:bg-canvas active:bg-canvas-muted border-[1.5px] border-ink shadow-sm",
      signal:
        "bg-signal-orange text-white hover:bg-[#b83c00] active:bg-[#993200] rounded-consent px-7 py-2 text-xs font-bold tracking-eyebrow uppercase shadow-sm",
      outline:
        "border-[1.5px] border-black/20 text-ink hover:border-ink hover:bg-white active:bg-canvas",
      ghost:
        "text-slate-600 hover:text-ink hover:bg-black/[0.04] active:bg-black/[0.08]",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant as keyof typeof variantStyles]} ${className}`}
        {...props}
      >
        {isLoading && (
          <svg
            className="animate-spin -ml-0.5 h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
