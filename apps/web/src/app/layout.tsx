import React from "react";

export const metadata = {
  title: "Nirikshak — Legal Metrology Inspection Portal",
  description: "Automated verification system for pre-packaged commodities under Legal Metrology Rules, 2011.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-900 text-slate-100 antialiased font-sans">
        <header className="border-b border-slate-800 bg-slate-950/80 px-6 py-4 backdrop-blur">
          <div className="flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-3">
              <span className="text-xl font-bold tracking-tight text-emerald-400">NIRIKSHAK</span>
              <span className="text-xs bg-emerald-950/80 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded-full font-mono">
                SIH26034
              </span>
            </div>
            <span className="text-xs text-slate-400">Legal Metrology Packaged Commodities Enforcement</span>
          </div>
        </header>
        <main className="max-w-7xl mx-auto p-6">{children}</main>
      </body>
    </html>
  );
}
