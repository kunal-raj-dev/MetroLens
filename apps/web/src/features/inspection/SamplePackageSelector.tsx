"use client";

import React, { useState } from "react";
import {
  Sparkles,
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  AlertTriangle,
  FileCheck2,
  Layers,
  Info,
} from "lucide-react";
import { Card, Badge, Tooltip } from "@/components/ui";

export interface SamplePackageItem {
  id: string;
  title: string;
  packageType: string;
  language: string;
  tag: string;
  tagVariant: "success" | "danger" | "warning" | "info" | "outline";
  resolution: [number, number];
  imageSrc: string;
  disclaimer: string;
}

export const SAMPLE_PACKAGES: SamplePackageItem[] = [
  {
    id: "SYNTH-01-ENG-FMCG",
    title: "English Biscuit Pouch",
    packageType: "biscuit_pouch",
    language: "English",
    tag: "Rule 6 Pass",
    tagVariant: "success",
    resolution: [640, 360],
    imageSrc: "/fixtures/SYNTH-01-ENG-FMCG.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-02-HIN-FMCG",
    title: "Pure Hindi Atta Bag",
    packageType: "atta_bag",
    language: "Hindi (Devanagari)",
    tag: "Devanagari ₹ Pass",
    tagVariant: "success",
    resolution: [640, 360],
    imageSrc: "/fixtures/SYNTH-02-HIN-FMCG.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-03-MIXED-BILINGUAL",
    title: "Bilingual Snack Carton",
    packageType: "snack_carton",
    language: "Bilingual (En+Hi)",
    tag: "Bilingual Pass",
    tagVariant: "success",
    resolution: [640, 380],
    imageSrc: "/fixtures/SYNTH-03-MIXED-BILINGUAL.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-04-MICRO-FONT",
    title: "Shrinkflation Micro-Font",
    packageType: "confectionery_pouch",
    language: "English",
    tag: "Rule 7 Font Deficit",
    tagVariant: "danger",
    resolution: [640, 320],
    imageSrc: "/fixtures/SYNTH-04-MICRO-FONT.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-05-LIQUID-VOLUME",
    title: "Handwash Liquid Volume",
    packageType: "handwash_bottle",
    language: "English",
    tag: "Volume (ml) Metric Pass",
    tagVariant: "info",
    resolution: [640, 360],
    imageSrc: "/fixtures/SYNTH-05-LIQUID-VOLUME.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-06-PROHIBITED-UNITS",
    title: "Detergent Pluralized Units",
    packageType: "detergent_pouch",
    language: "English",
    tag: "Rule 12 'Gms' Deficit",
    tagVariant: "danger",
    resolution: [640, 320],
    imageSrc: "/fixtures/SYNTH-06-PROHIBITED-UNITS.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-07-BLANK-FRAME",
    title: "Blank / Texture Frame",
    packageType: "blank_cardboard",
    language: "None",
    tag: "Quality Gate Reject",
    tagVariant: "outline",
    resolution: [640, 320],
    imageSrc: "/fixtures/SYNTH-07-BLANK-FRAME.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
  {
    id: "SYNTH-08-LOW-CONTRAST-FADED",
    title: "Faded Thermal Stamp",
    packageType: "foil_crimp",
    language: "English",
    tag: "Suspect Review Case",
    tagVariant: "warning",
    resolution: [640, 320],
    imageSrc: "/fixtures/SYNTH-08-LOW-CONTRAST-FADED.png",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
  },
];

export interface SamplePackageSelectorProps {
  selectedSampleId?: string | null;
  onSelectSample: (file: File, previewUrl: string, sample: SamplePackageItem) => void;
  disabled?: boolean;
  className?: string;
}

export function SamplePackageSelector({
  selectedSampleId = null,
  onSelectSample,
  disabled = false,
  className = "",
}: SamplePackageSelectorProps) {
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const scrollContainerRef = React.useRef<HTMLDivElement>(null);

  const handleSelect = async (sample: SamplePackageItem) => {
    if (disabled || loadingId) return;
    setLoadingId(sample.id);

    try {
      // Fetch the actual verified static asset from public/fixtures/
      const response = await fetch(sample.imageSrc);
      if (!response.ok) {
        throw new Error(`Failed to load fixture asset: HTTP ${response.status}`);
      }

      const blob = await response.blob();
      const file = new File([blob], `${sample.id}.png`, {
        type: "image/png",
        lastModified: Date.now(),
      });

      onSelectSample(file, sample.imageSrc, sample);
    } catch (err) {
      console.error("[SamplePackageSelector] Failed to load sample fixture:", err);
    } finally {
      setLoadingId(null);
    }
  };

  const handleScroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = direction === "left" ? -320 : 320;
      scrollContainerRef.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  };

  return (
    <div className={`space-y-3.5 ${className}`}>
      {/* Header Bar with Synthetic Disclosure */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-full bg-signal-orange/10 flex items-center justify-center">
            <Sparkles className="w-3.5 h-3.5 text-signal-orange" />
          </div>
          <div>
            <h3 className="text-sm font-semibold tracking-headline text-ink">
              Benchmark Demonstration Packages
            </h3>
            <p className="text-[11px] text-slate-500 font-normal">
              Pre-loaded verified statutory packaging samples for evaluation & judging.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-pill bg-amber-500/10 border border-amber-500/30 text-[11px] font-bold tracking-eyebrow uppercase text-amber-800">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
            SYNTHETIC DEMO
          </div>

          <div className="hidden sm:flex items-center gap-1">
            <button
              type="button"
              onClick={() => handleScroll("left")}
              aria-label="Scroll samples left"
              className="p-1 rounded-full bg-white border border-black/[0.08] hover:bg-slate-50 text-slate-600 transition-colors shadow-sm"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={() => handleScroll("right")}
              aria-label="Scroll samples right"
              className="p-1 rounded-full bg-white border border-black/[0.08] hover:bg-slate-50 text-slate-600 transition-colors shadow-sm"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Horizontal Carousel Container */}
      <div
        ref={scrollContainerRef}
        role="listbox"
        aria-label="Benchmark demonstration packages"
        className="flex gap-3.5 overflow-x-auto pb-2 pt-1 no-scrollbar scroll-smooth snap-x snap-mandatory"
        style={{ scrollbarWidth: "thin" }}
      >
        {SAMPLE_PACKAGES.map((sample) => {
          const isSelected = selectedSampleId === sample.id;
          const isLoading = loadingId === sample.id;

          return (
            <div
              key={sample.id}
              role="option"
              aria-selected={isSelected}
              tabIndex={disabled ? -1 : 0}
              onClick={() => handleSelect(sample)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  handleSelect(sample);
                }
              }}
              className={`flex-shrink-0 w-64 snap-start rounded-2xl p-3 border transition-all duration-200 cursor-pointer text-left relative select-none ${
                isSelected
                  ? "bg-signal-orange/5 border-signal-orange shadow-deep ring-2 ring-signal-orange/30"
                  : "bg-white border-black/[0.08] hover:border-black/20 hover:shadow-sm"
              } ${disabled ? "opacity-50 cursor-not-allowed pointer-events-none" : ""}`}
            >
              {/* Thumbnail Frame */}
              <div className="relative w-full h-28 rounded-xl overflow-hidden bg-slate-100 border border-black/[0.04] mb-2.5">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={sample.imageSrc}
                  alt={sample.title}
                  className="w-full h-full object-cover"
                  loading="lazy"
                />
                <div className="absolute top-2 left-2">
                  <span className="font-mono text-[9px] font-bold px-1.5 py-0.5 rounded bg-black/70 text-white backdrop-blur-sm">
                    {sample.id.split("-").slice(0, 2).join("-")}
                  </span>
                </div>
                {isSelected && (
                  <div className="absolute top-2 right-2 w-5 h-5 rounded-full bg-signal-orange text-white flex items-center justify-center shadow-sm">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                )}
                {isLoading && (
                  <div className="absolute inset-0 bg-white/70 backdrop-blur-xs flex items-center justify-center text-xs font-semibold text-ink">
                    Loading...
                  </div>
                )}
              </div>

              {/* Metadata */}
              <div className="space-y-1">
                <div className="flex items-center justify-between gap-1">
                  <span className="text-xs font-semibold text-ink truncate">
                    {sample.title}
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span className="truncate">{sample.language}</span>
                  <Badge variant={sample.tagVariant} size="sm">
                    {sample.tag}
                  </Badge>
                </div>

                <div className="text-[10px] text-slate-400 font-mono pt-0.5 truncate">
                  Type: {sample.packageType.replace(/_/g, " ")} • {sample.resolution[0]}×{sample.resolution[1]}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
