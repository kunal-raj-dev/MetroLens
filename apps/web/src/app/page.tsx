import React from "react";

export default function HomePage() {
  return (
    <div className="space-y-8 py-4">
      <div className="border-b border-slate-800 pb-5">
        <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
          Officer Inspection Workstation
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Upload packaged commodity photographs, inspect bounding-box detections, verify font heights, and issue auditable dossiers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="border border-slate-800 rounded-lg p-6 bg-slate-950/40">
          <h2 className="font-semibold text-slate-200">1. Photographic Ingestion</h2>
          <p className="text-xs text-slate-400 mt-2">
            Captures front PDP frame, secondary panels, and optical calibration fiducial marker.
          </p>
        </div>

        <div className="border border-slate-800 rounded-lg p-6 bg-slate-950/40">
          <h2 className="font-semibold text-slate-200">2. Optical Measurement</h2>
          <p className="text-xs text-slate-400 mt-2">
            Computes metric scale (mm/px) and evaluates numeral heights against Schedule II minimums.
          </p>
        </div>

        <div className="border border-slate-800 rounded-lg p-6 bg-slate-950/40">
          <h2 className="font-semibold text-slate-200">3. Immutable Dossier</h2>
          <p className="text-xs text-slate-400 mt-2">
            Generates cryptographically signed inspection report with full SHA-256 evidence chain.
          </p>
        </div>
      </div>
    </div>
  );
}
