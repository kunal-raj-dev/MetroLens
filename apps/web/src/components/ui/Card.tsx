import React, { HTMLAttributes, forwardRef } from "react";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  shape?: "stadium" | "rounded" | "pill";
  variant?: "lifted" | "white" | "canvas";
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      className = "",
      shape = "stadium",
      variant = "lifted",
      children,
      ...props
    },
    ref
  ) => {
    const shapeStyles = {
      stadium: "rounded-stadium",
      rounded: "rounded-3xl",
      pill: "rounded-pill",
    };

    const variantStyles = {
      lifted: "bg-canvas-lifted border border-black/[0.05] shadow-halo",
      white: "bg-white border border-black/[0.06] shadow-halo",
      canvas: "bg-canvas border border-black/[0.08]",
    };

    return (
      <div
        ref={ref}
        className={`${shapeStyles[shape]} ${variantStyles[variant]} text-ink transition-shadow duration-200 ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";

export const CardHeader = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className = "", children, ...props }, ref) => (
  <div
    ref={ref}
    className={`flex flex-col space-y-2 p-6 sm:p-8 border-b border-black/[0.04] ${className}`}
    {...props}
  >
    {children}
  </div>
));
CardHeader.displayName = "CardHeader";

export const CardTitle = forwardRef<
  HTMLHeadingElement,
  HTMLAttributes<HTMLHeadingElement>
>(({ className = "", children, ...props }, ref) => (
  <h3
    ref={ref}
    className={`text-xl sm:text-2xl font-medium tracking-headline text-ink ${className}`}
    {...props}
  >
    {children}
  </h3>
));
CardTitle.displayName = "CardTitle";

export const CardDescription = forwardRef<
  HTMLParagraphElement,
  HTMLAttributes<HTMLParagraphElement>
>(({ className = "", children, ...props }, ref) => (
  <p
    ref={ref}
    className={`text-sm text-slate-600 leading-relaxed ${className}`}
    {...props}
  >
    {children}
  </p>
));
CardDescription.displayName = "CardDescription";

export const CardContent = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className = "", children, ...props }, ref) => (
  <div ref={ref} className={`p-6 sm:p-8 ${className}`} {...props}>
    {children}
  </div>
));
CardContent.displayName = "CardContent";

export const CardFooter = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className = "", children, ...props }, ref) => (
  <div
    ref={ref}
    className={`flex items-center justify-between p-6 sm:p-8 pt-0 border-t border-black/[0.04] mt-4 ${className}`}
    {...props}
  >
    {children}
  </div>
));
CardFooter.displayName = "CardFooter";
