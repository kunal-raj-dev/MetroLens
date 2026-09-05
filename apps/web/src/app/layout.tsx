import React from "react";
import "./globals.css";
import { Sofia_Sans } from "next/font/google";
import {
  Shield,
  Search,
  ExternalLink,
  Lock,
  ChevronDown,
  Scale,
  FileCheck2,
  Building2,
  HelpCircle,
} from "lucide-react";

const sofia = Sofia_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "700", "800"],
  variable: "--font-sofia",
  display: "swap",
});

export const metadata = {
  title: "MetroLens AI — Legal Metrology Inspection Workstation",
  description:
    "Automated statutory compliance verification and explainable evidence analysis for pre-packaged commodities under Legal Metrology Rules, 2011.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={sofia.variable}>
      <body className="min-h-screen bg-canvas text-ink antialiased font-sans flex flex-col selection:bg-signal-orange selection:text-white">
        {/* Skip link for keyboard accessibility */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-6 focus:z-50 focus:px-6 focus:py-2.5 focus:bg-ink focus:text-canvas focus:rounded-cta focus:shadow-halo"
        >
          Skip to main inspection workspace
        </a>

        {/* Floating Nav Pill (Docked ~20px below top) */}
        <div className="sticky top-5 z-50 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full pointer-events-none">
          <header className="pointer-events-auto bg-white/95 backdrop-blur-md rounded-pill px-6 sm:px-8 py-3.5 shadow-lift border border-black/[0.04] flex items-center justify-between transition-all duration-300">
            {/* Left: Brand Identity */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                {/* Two overlapping subtle circles paying homage to the dual-lens metrological vision */}
                <div className="relative flex items-center">
                  <div className="w-5 h-5 rounded-full bg-signal-orange/90 -mr-2" />
                  <div className="w-5 h-5 rounded-full bg-signal-light/80 mix-blend-multiply" />
                </div>
                <span className="text-xl font-bold tracking-tight text-ink">
                  Metro<span className="font-light text-slate-500">Lens</span>
                </span>
              </div>
              <span className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-pill bg-canvas text-ink text-[11px] font-bold tracking-eyebrow uppercase border border-black/[0.06]">
                <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
                SIH26034
              </span>
            </div>

            {/* Center: Primary Navigation Links */}
            <nav
              className="hidden lg:flex items-center gap-9 text-sm font-medium text-ink"
              aria-label="Primary Workstation Navigation"
            >
              <a
                href="#inspection-workspace"
                className="hover:text-signal-orange transition-colors"
              >
                Inspection
              </a>
              <a
                href="#statutory-pillars"
                className="text-slate-600 hover:text-ink transition-colors"
              >
                Statutory Pillars
              </a>
              <a
                href="#design-tokens"
                className="text-slate-600 hover:text-ink transition-colors"
              >
                Verification Matrix
              </a>
              <a
                href="#regulatory-framework"
                className="text-slate-600 hover:text-ink transition-colors"
              >
                PCR 2011 Rules
              </a>
            </nav>

            {/* Right: Officer Context Pill */}
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-pill bg-canvas text-xs text-ink/80 border border-black/[0.04]">
                <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse" />
                <span className="font-medium">Officer LMO-DL-42</span>
              </div>
              <button
                type="button"
                className="w-9 h-9 rounded-full bg-canvas hover:bg-canvas-muted text-ink flex items-center justify-center transition-colors focus-visible:ring-2 focus-visible:ring-ink"
                aria-label="Search regulations and gazette notices"
              >
                <Search className="w-4 h-4" />
              </button>
            </div>
          </header>
        </div>

        {/* Main Workspace Area */}
        <main id="main-content" className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-16">
          {children}
        </main>

        {/* Mastercard-Inspired Ink Black Editorial Footer */}
        <footer className="bg-ink text-white pt-16 sm:pt-20 pb-16 px-6 sm:px-12 lg:px-16 border-t border-black/10 mt-auto">
          <div className="max-w-7xl mx-auto space-y-16">
            {/* Conversational Editorial H2 */}
            <div className="max-w-3xl space-y-3">
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-eyebrow text-signal-light">
                <span className="w-2 h-2 rounded-full bg-signal-light" />
                MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION
              </div>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-medium tracking-headline text-white leading-tight">
                Protecting consumer trust and statutory packaging compliance across 780+ districts.
              </h2>
            </div>

            {/* 4-Column Editorial Link Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pt-6 border-t border-white/10">
              {/* Column 1 */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-eyebrow text-slate-400">
                  STATUTORY MANDATE
                </h4>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li>
                    <a href="#legal" className="hover:text-white transition-colors">
                      Legal Metrology Act, 2009
                    </a>
                  </li>
                  <li>
                    <a href="#rules" className="hover:text-white transition-colors">
                      Packaged Commodities Rules, 2011
                    </a>
                  </li>
                  <li>
                    <a href="#jan-vishwas" className="hover:text-white transition-colors">
                      Jan Vishwas (Amendment) Act, 2026
                    </a>
                  </li>
                  <li>
                    <a href="#schedule-ii" className="hover:text-white transition-colors">
                      Schedule II Font Height Tables
                    </a>
                  </li>
                </ul>
              </div>

              {/* Column 2 */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-eyebrow text-slate-400">
                  METROLOGICAL PILLARS
                </h4>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li className="flex items-center gap-2">
                    <Shield className="w-3.5 h-3.5 text-signal-light" />
                    <span>Laplacian Quality Gate</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Scale className="w-3.5 h-3.5 text-signal-light" />
                    <span>27.0mm Metric Scale Recovery</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <FileCheck2 className="w-3.5 h-3.5 text-signal-light" />
                    <span>Rule 6(11) Unit Sale Price Math</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Lock className="w-3.5 h-3.5 text-signal-light" />
                    <span>SHA-256 Tamper-Evident Dossiers</span>
                  </li>
                </ul>
              </div>

              {/* Column 3 */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-eyebrow text-slate-400">
                  NATIONAL E-GOVERNANCE
                </h4>
                <ul className="space-y-3 text-sm text-slate-300">
                  <li>
                    <a href="#emaap" className="inline-flex items-center gap-1 hover:text-white transition-colors">
                      National eMaap Portal Sync <ExternalLink className="w-3 h-3 text-slate-400" />
                    </a>
                  </li>
                  <li>
                    <a href="#consumer" className="inline-flex items-center gap-1 hover:text-white transition-colors">
                      National Consumer Helpline (NCH) <ExternalLink className="w-3 h-3 text-slate-400" />
                    </a>
                  </li>
                  <li>
                    <a href="#bis" className="inline-flex items-center gap-1 hover:text-white transition-colors">
                      Bureau of Indian Standards (BIS) <ExternalLink className="w-3 h-3 text-slate-400" />
                    </a>
                  </li>
                  <li>
                    <a href="#doca" className="inline-flex items-center gap-1 hover:text-white transition-colors">
                      Department of Consumer Affairs <ExternalLink className="w-3 h-3 text-slate-400" />
                    </a>
                  </li>
                </ul>
              </div>

              {/* Column 4 */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-eyebrow text-slate-400">
                  GOVERNANCE & AUDIT
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  MetroLens AI operates under the strict constitutional doctrine of objective, deterministic enforcement:
                  AI perceives, math validates, rules decide, and officers govern.
                </p>
                <div className="pt-2">
                  <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-pill bg-white/10 text-xs font-mono text-slate-300">
                    <Lock className="w-3 h-3 text-signal-light" />
                    Offline Edge Certified
                  </span>
                </div>
              </div>
            </div>

            {/* Bottom Row */}
            <div className="pt-10 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-6 text-xs text-slate-400">
              <div>
                © 2026 MetroLens AI. Developed for Smart India Hackathon (SIH26034).
              </div>

              {/* Pill-shaped country/jurisdiction selector */}
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-pill bg-white/5 border border-white/10 text-slate-300 text-xs">
                <span>🇮🇳</span>
                <span>Jurisdiction: Republic of India</span>
                <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
              </div>

              <div className="flex items-center gap-6 text-xs text-slate-400">
                <a href="#privacy" className="hover:text-white transition-colors">
                  Privacy Choices
                </a>
                <a href="#terms" className="hover:text-white transition-colors">
                  Terms of Enforcement
                </a>
                <a href="#evidence" className="hover:text-white transition-colors">
                  Chain of Custody
                </a>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
