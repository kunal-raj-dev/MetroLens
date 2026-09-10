import React from "react";
import "./globals.css";
import { Shield, Scale } from "lucide-react";

export const metadata = {
  title: "MetroLens — Packaging Assessment Prototype",
  description: "Image-based packaging declaration checks and evidence for human review. A project prototype, not a government certification service.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-canvas text-ink antialiased font-sans flex flex-col">
        <a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-4 focus:z-50 focus:p-3 focus:bg-white">Skip to main inspection workspace</a>
        <div className="sticky top-3 z-40 px-4 sm:px-6 max-w-7xl mx-auto w-full">
          <header className="bg-white/95 backdrop-blur-md rounded-3xl px-5 sm:px-8 py-4 shadow-lift border border-black/5 flex flex-wrap items-center justify-between gap-4">
            <a href="#main-content" className="flex items-center gap-2 text-xl font-bold" aria-label="MetroLens home"><Scale className="w-6 h-6 text-signal-orange" />Metro<span className="font-light text-slate-600">Lens</span></a>
            <nav className="flex flex-wrap gap-4 text-sm" aria-label="Primary navigation">
              <a href="#inspection-workspace">Inspection</a><a href="#statutory-pillars">How it works</a><a href="#scope">Scope</a><a href="#privacy">Image privacy</a>
            </nav>
            <span className="text-xs rounded-full bg-canvas px-3 py-1.5">Project prototype · SIH26034</span>
          </header>
        </div>
        <main id="main-content" className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-16">{children}</main>
        <footer className="bg-ink text-white py-12 px-6">
          <div className="max-w-7xl mx-auto space-y-6">
            <div className="flex items-center gap-2 text-signal-light text-sm"><Shield className="w-4 h-4" />Image evidence for human review</div>
            <p className="max-w-2xl text-slate-200">MetroLens is an independent project prototype. It does not represent a ministry, certify products, or issue enforcement decisions. OCR and measurements require verification.</p>
            <nav className="flex flex-wrap gap-6 text-sm text-slate-200" aria-label="Project information"><a href="#regulatory-framework">Legal context</a><a href="#privacy">Image handling</a><a href="#terms">Prototype use</a><a href="#evidence">Evidence and reports</a><a href="https://github.com/kunal-raj-dev/MetroLens">Source repository</a></nav>
            <p className="text-xs text-slate-300">© 2026 MetroLens · Single-image inspection assistance</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
