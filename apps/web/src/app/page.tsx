"use client";

import React, { useState } from "react";
import {
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Badge,
  StatusIndicator,
  Alert,
  EmptyState,
  Dialog,
  Tooltip,
  Skeleton,
} from "@/components/ui";
import {
  Camera,
  Scale,
  FileCheck2,
  Lock,
  Layers,
  Sparkles,
  Info,
  ArrowRight,
  ShieldCheck,
  ChevronRight,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Cpu,
  FileText,
  RotateCcw,
  Download,
  ToggleLeft,
  ToggleRight,
} from "lucide-react";
import { OverallVerdict } from "@/types/contract";
import { ImageUploadZone } from "@/components/ImageUploadZone";
import {
  FrontendInspectionModel,
  DeclarationModel,
  ReviewSubmissionInput,
  CaliperPoint,
} from "@/types/frontend";
import {
  ComplianceDashboard,
  EvidenceCanvas,
  DeclarationTable,
  InspectorReviewModal,
  SamplePackageSelector,
  SamplePackageItem,
} from "@/features/inspection";
import {
  defaultInspectionClient,
  defaultReportClient,
  InspectionClientMode,
} from "@/services";

export default function OfficerWorkstationPage() {
  const [isGuideOpen, setIsGuideOpen] = useState(false);
  const [activeVerdict, setActiveVerdict] =
    useState<OverallVerdict>("COMPLIANT");
  const [clientMode, setClientMode] = useState<InspectionClientMode>("mock");
  const [inspectionResult, setInspectionResult] =
    useState<FrontendInspectionModel | null>(null);
  const [uploadedImageSrc, setUploadedImageSrc] = useState<string | null>(null);
  const [imageDimensions, setImageDimensions] = useState<{
    width: number;
    height: number;
  } | null>(null);
  const [selectedTokenId, setSelectedTokenId] = useState<string | null>(null);
  const [selectedFieldName, setSelectedFieldName] = useState<string | null>(null);
  const [selectedSampleId, setSelectedSampleId] = useState<string | null>(null);
  const [externalFile, setExternalFile] = useState<File | null>(null);
  const [resetTrigger, setResetTrigger] = useState<number>(0);
  const [isGeneratingReport, setIsGeneratingReport] = useState<boolean>(false);
  const [reportError, setReportError] = useState<string | null>(null);
  const [reportSuccess, setReportSuccess] = useState<string | null>(null);
  const [reviewingDeclaration, setReviewingDeclaration] =
    useState<DeclarationModel | null>(null);
  const [isReviewModalOpen, setIsReviewModalOpen] = useState<boolean>(false);
  const [isSubmittingReview, setIsSubmittingReview] = useState<boolean>(false);
  const [isCaliperMode, setIsCaliperMode] = useState<boolean>(false);
  const [caliperPoints, setCaliperPoints] = useState<{
    pointA: CaliperPoint | null;
    pointB: CaliperPoint | null;
  }>({ pointA: null, pointB: null });

  // Handle Review Submission through service boundary
  const handleSubmitReview = async (input: ReviewSubmissionInput) => {
    setIsSubmittingReview(true);
    try {
      const result = await defaultInspectionClient.submitReview(input);

      if (inspectionResult) {
        const updatedDeclarations = { ...inspectionResult.declarations };
        if (updatedDeclarations[input.fieldName]) {
          updatedDeclarations[input.fieldName] = {
            ...updatedDeclarations[input.fieldName],
            reviewStatus: result.updatedReviewStatus,
            operatorNotes: result.operatorNotes || null,
          };
        }

        setInspectionResult({
          ...inspectionResult,
          declarations: updatedDeclarations,
        });
      }
      return result;
    } finally {
      setIsSubmittingReview(false);
    }
  };

  const handleViewEvidence = (decl: DeclarationModel) => {
    setSelectedFieldName(decl.fieldName);
    if (decl.sourceTokenIds && decl.sourceTokenIds.length > 0) {
      setSelectedTokenId(decl.sourceTokenIds[0]);
    }
  };

  const highlightedTokenIds = selectedFieldName
    ? inspectionResult?.declarations[selectedFieldName]?.sourceTokenIds || []
    : [];

  // 1. Reset complete inspection state (Session Reset)
  const handleStartNewInspection = () => {
    setInspectionResult(null);
    setUploadedImageSrc(null);
    setImageDimensions(null);
    setSelectedTokenId(null);
    setSelectedFieldName(null);
    setIsReviewModalOpen(false);
    setReviewingDeclaration(null);
    setCaliperPoints({ pointA: null, pointB: null });
    setIsCaliperMode(false);
    setSelectedSampleId(null);
    setExternalFile(null);
    setReportError(null);
    setReportSuccess(null);
    setResetTrigger((prev) => prev + 1);
  };

  // 2. Select benchmark sample package
  const handleSelectSample = (
    file: File,
    previewUrl: string,
    sample: SamplePackageItem
  ) => {
    // Clear old inspection result without clearing the incoming file
    setInspectionResult(null);
    setSelectedTokenId(null);
    setSelectedFieldName(null);
    setIsReviewModalOpen(false);
    setReviewingDeclaration(null);
    setCaliperPoints({ pointA: null, pointB: null });
    setIsCaliperMode(false);
    setReportError(null);
    setReportSuccess(null);

    setSelectedSampleId(sample.id);
    setExternalFile(file);
    setUploadedImageSrc(previewUrl);
    setImageDimensions({
      width: sample.resolution[0],
      height: sample.resolution[1],
    });
  };

  // 3. Mode Toggle (Strict state separation: resets state on switch)
  const handleModeToggle = (newMode: InspectionClientMode) => {
    if (newMode !== clientMode) {
      handleStartNewInspection();
      setClientMode(newMode);
    }
  };

  // 4. Download Assessment Report PDF
  const handleDownloadReport = async () => {
    if (!inspectionResult || isGeneratingReport) return;
    setIsGeneratingReport(true);
    setReportError(null);
    setReportSuccess(null);

    try {
      const res = await defaultReportClient.downloadAssessmentReport(
        inspectionResult.inspectionId,
        {
          officerNotes: "Official Legal Metrology Packaging Assessment Report.",
          includeRawImage: true,
        }
      );
      setReportSuccess(
        `Assessment report successfully compiled & downloaded (${(res.byteSize / 1024).toFixed(1)} KB).`
      );
    } catch (err: any) {
      setReportError(
        err?.message ||
          "Report generation unavailable: Backend report endpoint POST /api/v1/report/pdf is offline."
      );
    } finally {
      setIsGeneratingReport(false);
    }
  };

  return (
    <div className="space-y-16 pb-20 relative overflow-hidden">
      {/* Ghost Watermark Headline (Cream-on-Cream Background Layer) */}
      <div
        className="absolute top-4 left-1/2 -translate-x-1/2 pointer-events-none select-none text-[80px] sm:text-[120px] lg:text-[180px] font-black tracking-tighter text-canvas-muted/40 uppercase whitespace-nowrap -z-10"
        aria-hidden="true"
      >
        METROLENS
      </div>

      {/* Hero Section: Editorial Headline & Actions */}
      <section className="pt-4 sm:pt-8 max-w-4xl space-y-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-pill bg-white border border-black/[0.06] text-xs font-bold tracking-eyebrow uppercase text-slate-700 shadow-sm">
          <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
          SOVEREIGN REGULATORY SURVEILLANCE
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-medium tracking-headline text-ink leading-[1.08]">
          Automated legal metrology verification for pre-packaged commodities.
        </h1>

        <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal max-w-2xl">
          Transforming manual ruler-and-magnifier field audits into a mathematically verified,
          tamper-evident inspection completed in under 2.5 seconds under the Legal Metrology Rules, 2011.
        </p>

        <div className="flex flex-wrap items-center gap-4 pt-2">
          <Button
            variant="primary"
            size="md"
            onClick={() => {
              const el = document.getElementById("inspection-workspace");
              el?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            Start Package Audit
          </Button>

          <Button
            variant="secondary"
            size="md"
            onClick={() => setIsGuideOpen(true)}
          >
            <Info className="w-4 h-4 mr-1.5 text-slate-500" />
            Standard Operating Procedure
          </Button>
        </div>
      </section>

      {/* Signature Mastercard Constellation: Traced Orbital Arcs & Circular Service Hubs */}
      <section id="statutory-pillars" className="space-y-8 relative pt-6">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-eyebrow text-slate-500">
              <span className="w-1.5 h-1.5 rounded-full bg-signal-light" />
              THE METROLOGICAL CONSTELLATION
            </div>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-headline text-ink">
              Four verified stages of objective legal adjudication
            </h2>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            Zero Cloud AI in Adjudication
          </span>
        </div>

        {/* Constellation Container with Decorative Orbital Curve Lines */}
        <div className="relative">
          {/* Orbital connecting arc (SVG overlay on desktop) */}
          <svg
            className="hidden lg:block absolute top-28 left-0 w-full h-32 pointer-events-none -z-0"
            viewBox="0 0 1000 120"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M 160 50 Q 500 -30 840 50"
              className="orbital-arc"
            />
          </svg>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative z-10">
            {/* Circular Hub 1: Optical Quality Gate */}
            <div className="bg-canvas-lifted rounded-stadium p-8 border border-black/[0.06] shadow-halo flex flex-col items-center text-center space-y-5 group hover:shadow-deep transition-all duration-300">
              {/* Circular Portrait Mask with Attached Satellite CTA */}
              <div className="relative my-2">
                <div className="w-36 h-36 rounded-full bg-white border border-black/[0.06] flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform duration-300">
                  <div className="w-24 h-24 rounded-full bg-canvas flex items-center justify-center">
                    <Camera className="w-10 h-10 text-ink/80" />
                  </div>
                </div>
                {/* Attached Satellite Micro-CTA */}
                <div
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta cursor-pointer"
                  title="Explore Quality Gate"
                >
                  <ArrowRight className="w-4 h-4 text-signal-orange" />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="text-[11px] font-bold uppercase tracking-eyebrow text-slate-500">
                  • STAGE 01
                </div>
                <h3 className="text-xl font-medium tracking-headline text-ink">
                  Frame Quality Gate
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed font-normal">
                  Laplacian variance sharpness testing ($&gt;50.0$) and specular glare ratio checks
                  ensure zero false accusations on degraded camera frames.
                </p>
              </div>
            </div>

            {/* Circular Hub 2: Metric Scale Recovery */}
            <div className="bg-canvas-lifted rounded-stadium p-8 border border-black/[0.06] shadow-halo flex flex-col items-center text-center space-y-5 group hover:shadow-deep transition-all duration-300">
              <div className="relative my-2">
                <div className="w-36 h-36 rounded-full bg-white border border-black/[0.06] flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform duration-300">
                  <div className="w-24 h-24 rounded-full bg-[#FFF8EB] border border-amber-200 flex items-center justify-center">
                    <Scale className="w-10 h-10 text-amber-700" />
                  </div>
                </div>
                <div
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta cursor-pointer"
                  title="Explore Metric Scale"
                >
                  <ArrowRight className="w-4 h-4 text-signal-orange" />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="text-[11px] font-bold uppercase tracking-eyebrow text-slate-500">
                  • STAGE 02
                </div>
                <h3 className="text-xl font-medium tracking-headline text-ink">
                  Metric Scale Recovery
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed font-normal">
                  Planar homography calibration using standard 27.0mm ₹10 coin anchors or manual
                  2-point caliper lines locks physical mm/px scale.
                </p>
              </div>
            </div>

            {/* Circular Hub 3: Statutory Rule Engine */}
            <div className="bg-canvas-lifted rounded-stadium p-8 border border-black/[0.06] shadow-halo flex flex-col items-center text-center space-y-5 group hover:shadow-deep transition-all duration-300">
              <div className="relative my-2">
                <div className="w-36 h-36 rounded-full bg-white border border-black/[0.06] flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform duration-300">
                  <div className="w-24 h-24 rounded-full bg-[#EBF7F2] border border-emerald-200 flex items-center justify-center">
                    <FileCheck2 className="w-10 h-10 text-emerald-800" />
                  </div>
                </div>
                <div
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta cursor-pointer"
                  title="Explore Rule Engine"
                >
                  <ArrowRight className="w-4 h-4 text-signal-orange" />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="text-[11px] font-bold uppercase tracking-eyebrow text-slate-500">
                  • STAGE 03
                </div>
                <h3 className="text-xl font-medium tracking-headline text-ink">
                  Deterministic Rule Engine
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed font-normal">
                  Gazette clauses codified in pure deterministic Python. Audits Rule 6 mandatory
                  fields, Rule 7 font heights, and Rule 6(11) Unit Sale Price math.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Inspection Workstation (40px Stadium Container Panels) */}
      <section
        id="inspection-workspace"
        aria-labelledby="workstation-heading"
        className="space-y-6 pt-4"
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-black/[0.08] pb-4">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-eyebrow text-slate-500">
              <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
              OFFICER WORKSTATION
            </div>
            <h2 id="workstation-heading" className="text-2xl sm:text-3xl font-medium tracking-headline text-ink">
              Interactive Compliance & Evidence Dashboard
            </h2>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            {/* Mode Indicator Pill & Toggle */}
            <div className="flex items-center bg-white rounded-pill border border-black/[0.08] p-0.5 shadow-xs">
              <button
                type="button"
                onClick={() => handleModeToggle("mock")}
                className={`px-3 py-1 rounded-pill text-xs font-bold uppercase tracking-eyebrow transition-all flex items-center gap-1.5 ${
                  clientMode === "mock"
                    ? "bg-amber-100/80 text-amber-900 shadow-xs"
                    : "text-slate-500 hover:text-ink"
                }`}
                title="Switch to Synthetic Demo Mode (Offline Regression Sandbox)"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
                SYNTHETIC DEMO
              </button>

              <button
                type="button"
                onClick={() => handleModeToggle("live")}
                className={`px-3 py-1 rounded-pill text-xs font-bold uppercase tracking-eyebrow transition-all flex items-center gap-1.5 ${
                  clientMode === "live"
                    ? "bg-emerald-100/80 text-emerald-900 shadow-xs"
                    : "text-slate-500 hover:text-ink"
                }`}
                title="Switch to Live Inspection Mode (FastAPI Gateway)"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-700" />
                LIVE INSPECTION
              </button>
            </div>

            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-pill bg-white text-xs text-ink font-medium border border-black/[0.06] shadow-sm">
              <Lock className="w-3.5 h-3.5 text-emerald-600" />
              SHA-256 Custody Sealed
            </span>

            {/* Workstation Actions: Report & Reset */}
            {inspectionResult && (
              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant="primary"
                  onClick={handleDownloadReport}
                  disabled={isGeneratingReport}
                  title="Download verified Legal Metrology assessment dossier"
                >
                  <FileText className="w-3.5 h-3.5 mr-1" />
                  {isGeneratingReport ? "Compiling Report..." : "Download Report"}
                </Button>

                <Button
                  size="sm"
                  variant="secondary"
                  onClick={handleStartNewInspection}
                  title="Start a new packaging audit"
                >
                  <RotateCcw className="w-3.5 h-3.5 mr-1" />
                  New Inspection
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Benchmark Demonstration Packages Card */}
        <Card shape="stadium" variant="white" className="p-5 border border-black/[0.06] shadow-halo">
          <SamplePackageSelector
            selectedSampleId={selectedSampleId}
            onSelectSample={handleSelectSample}
            disabled={isGeneratingReport}
          />
        </Card>

        {/* Report Notifications */}
        {reportSuccess && (
          <Alert variant="success" title="Assessment Report Ready">
            <p className="text-xs leading-relaxed">{reportSuccess}</p>
          </Alert>
        )}

        {reportError && (
          <Alert variant="warning" title="Report Generation Notice">
            <p className="text-xs leading-relaxed">{reportError}</p>
          </Alert>
        )}

        {/* 2-Column Workstation Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Packaging Ingestion Zone (Stadium Frame) */}
          <div className="lg:col-span-5 space-y-6">
            <ImageUploadZone
              clientMode={clientMode}
              onModeChange={handleModeToggle}
              externalFile={externalFile}
              resetTrigger={resetTrigger}
              onFileReady={(file, previewUrl, dimensions) => {
                setUploadedImageSrc(previewUrl);
                setImageDimensions(dimensions || null);
                setSelectedTokenId(null);
              }}
              onInspectionComplete={(result) => {
                setInspectionResult(result);
                setActiveVerdict(result.verdict.status);
              }}
              onFileCleared={handleStartNewInspection}
            />

            <Alert variant="info" title="Sovereign Enforcement Advisory">
              Photographs must clearly include the Principal Display Panel (PDP) and any calibration
              anchor. Ingestion processes files locally through client adapters.
            </Alert>
          </div>

          {/* Right Column: Statutory Adjudication, Evidence Canvas & Declaration Table */}
          <div className="lg:col-span-7 space-y-6">
            {inspectionResult ? (
              <div className="space-y-6">
                {/* Multi-modal Compliance Dashboard */}
                <ComplianceDashboard
                  inspection={inspectionResult}
                  selectedTokenId={selectedTokenId}
                  onSelectToken={setSelectedTokenId}
                />

                {/* Interactive High-DPI Affine Evidence Canvas */}
                <EvidenceCanvas
                  imageSrc={
                    uploadedImageSrc ||
                    inspectionResult.imagePath ||
                    "/fixtures/SYNTH-01-ENG-FMCG.png"
                  }
                  imageWidth={imageDimensions?.width || 640}
                  imageHeight={imageDimensions?.height || 360}
                  tokens={inspectionResult.ocrTokens}
                  selectedTokenId={selectedTokenId}
                  highlightedTokenIds={highlightedTokenIds}
                  onSelectToken={setSelectedTokenId}
                  isSynthetic={inspectionResult.isSynthetic}
                  isCaliperMode={isCaliperMode}
                  onToggleCaliperMode={() => setIsCaliperMode((prev) => !prev)}
                  caliperPoints={caliperPoints}
                  onCaliperPointsChange={(pts) =>
                    setCaliperPoints({
                      pointA: pts.pointA,
                      pointB: pts.pointB,
                    })
                  }
                  onClearCaliperPoints={() =>
                    setCaliperPoints({ pointA: null, pointB: null })
                  }
                />

                {/* Statutory Declaration Table & Evidence Linking */}
                <DeclarationTable
                  declarations={inspectionResult.declarations}
                  selectedFieldName={selectedFieldName}
                  onSelectDeclaration={(fieldName) => {
                    setSelectedFieldName(fieldName);
                    const decl = inspectionResult.declarations[fieldName];
                    if (decl?.sourceTokenIds?.[0]) {
                      setSelectedTokenId(decl.sourceTokenIds[0]);
                    }
                  }}
                  onViewEvidence={handleViewEvidence}
                  onOpenReview={(decl) => {
                    setReviewingDeclaration(decl);
                    setIsReviewModalOpen(true);
                  }}
                  isSynthetic={inspectionResult.isSynthetic}
                />
              </div>
            ) : (
              /* Evidence Canvas Stadium Card Placeholder (Pre-Inspection State) */
              <div className="space-y-6">
                <StatusIndicator
                  verdict={activeVerdict}
                  summaryReason="Standby mode. Ingest packaging image on the left to verify statutory declarations."
                />

                <Card
                  shape="stadium"
                  variant="lifted"
                  className="min-h-[360px] flex flex-col justify-center items-center p-8 sm:p-12 text-center relative overflow-hidden"
                >
                  <div className="w-16 h-16 rounded-full bg-canvas flex items-center justify-center mb-4 border border-black/[0.06] shadow-sm">
                    <Layers className="w-7 h-7 text-slate-500" />
                  </div>
                  <div className="space-y-2 max-w-md">
                    <h3 className="text-xl font-medium tracking-headline text-ink">
                      Evidence Canvas Standby
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                      Ingest a package photograph on the left to trigger automated OCR extraction,
                      metric calibration, and statutory Rule 6/7 evaluation under Legal Metrology Rules, 2011.
                    </p>
                  </div>
                  <div className="mt-6 flex items-center gap-2">
                    <span className="text-[11px] font-mono text-slate-400">
                      Supports Member 1 Frozen OCR Quads (Original Image Pixel Space)
                    </span>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Design System & Statutory Verification Matrix (Interactive Showcase) */}
      <section
        id="design-tokens"
        aria-labelledby="design-tokens-heading"
        className="space-y-6 pt-10 border-t border-black/[0.08]"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-eyebrow text-slate-500">
              <span className="w-1.5 h-1.5 rounded-full bg-signal-orange" />
              MASTERCARD-INSPIRED DESIGN TOKENS
            </div>
            <h2 id="design-tokens-heading" className="text-2xl sm:text-3xl font-medium tracking-headline text-ink">
              Multi-Modal Statutory States & UI Primitives
            </h2>
          </div>
          <Badge variant="default" size="sm">
            M5-1 Foundation Certified
          </Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Statutory State Switcher Card */}
          <Card shape="stadium" variant="white" className="p-8 space-y-6">
            <div className="space-y-1.5">
              <h3 className="text-xl font-medium tracking-headline text-ink">
                Statutory Verdict State Matrix
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 font-normal">
                Click to inspect how each legal state communicates via Color + Icon + Label + Plain Language Explanation.
              </p>
            </div>

            <div className="flex flex-wrap gap-2.5">
              {(
                [
                  "COMPLIANT",
                  "NON_COMPLIANT",
                  "SUSPECT_REVIEW",
                  "INCONCLUSIVE",
                ] as OverallVerdict[]
              ).map((verdict) => (
                <Button
                  key={verdict}
                  size="sm"
                  variant={activeVerdict === verdict ? "primary" : "secondary"}
                  onClick={() => setActiveVerdict(verdict)}
                >
                  {verdict}
                </Button>
              ))}
            </div>

            <div className="pt-2">
              <StatusIndicator verdict={activeVerdict} size="compact" />
            </div>
          </Card>

          {/* Component Primitives Showcase */}
          <Card shape="stadium" variant="white" className="p-8 space-y-6">
            <div className="space-y-1.5">
              <h3 className="text-xl font-medium tracking-headline text-ink">
                Pill Buttons & Eyebrow Badges
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 font-normal">
                Extreme radii (20px, 24px, 40px, 999px) create a soft, high-trust sovereign magazine feel.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <Button variant="primary" size="sm">
                Primary Ink Pill
              </Button>
              <Button variant="secondary" size="sm">
                Outlined Pill
              </Button>
              <Button variant="signal" size="sm">
                Signal Consent
              </Button>
            </div>

            <div className="flex flex-wrap items-center gap-2.5 pt-1">
              <Badge variant="success">Rule 6 Pass</Badge>
              <Badge variant="danger">Rule Deficit</Badge>
              <Badge variant="warning">Manual Review</Badge>
              <Badge variant="info">Rule 26 Exemption</Badge>
              <Badge variant="outline">Uncalibrated</Badge>
            </div>

            <div className="pt-2 flex items-center gap-3 text-xs text-slate-500">
              <Skeleton className="w-12 h-12 rounded-full" />
              <div className="space-y-1.5 flex-1">
                <Skeleton className="h-3.5 w-3/4 rounded-pill" />
                <Skeleton className="h-3.5 w-1/2 rounded-pill" />
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Accessible Workstation SOP Dialog */}
      <Dialog
        isOpen={isGuideOpen}
        onClose={() => setIsGuideOpen(false)}
        title="MetroLens Inspection Protocol"
        description="Standard Operating Procedure for Legal Metrology Officers under LMPC Rules, 2011"
      >
        <div className="space-y-5 text-sm text-slate-700 leading-relaxed font-normal">
          <p>
            Under the Legal Metrology Act, 2009 and Packaged Commodities Rules, 2011,
            packaged commodities sold in the Republic of India must display mandatory declarations in
            specified formats and minimum numeral heights (Rule 7 Table-I).
          </p>
          <div className="p-5 rounded-2xl bg-canvas border border-black/[0.06] space-y-2">
            <h5 className="font-medium text-ink">Four Pillars of Automated Verification:</h5>
            <ul className="list-disc pl-5 space-y-1.5 text-xs text-slate-600 font-normal">
              <li><strong className="text-ink">Laplacian Quality Gate:</strong> Filters blurred or glare-occluded frames before legal evaluation.</li>
              <li><strong className="text-ink">Metric Scale Recovery:</strong> Homography calculation using 27.0mm ₹10 coin anchor or manual caliper.</li>
              <li><strong className="text-ink">Multilingual Scene OCR:</strong> PP-OCRv3 on CPU extracts English and Devanagari text.</li>
              <li><strong className="text-ink">Deterministic State Machine:</strong> Zero cloud AI. Gazette clauses evaluated mathematically with SHA-256 evidence chain.</li>
            </ul>
          </div>
          <div className="flex justify-end pt-2">
            <Button
              variant="primary"
              size="sm"
              onClick={() => setIsGuideOpen(false)}
            >
              Acknowledge Standard Operating Procedure
            </Button>
          </div>
        </div>
      </Dialog>

      {/* Inspector Manual Review Modal */}
      <InspectorReviewModal
        isOpen={isReviewModalOpen}
        declaration={reviewingDeclaration}
        inspectionId={inspectionResult?.inspectionId || "INSP-CURRENT"}
        onClose={() => {
          setIsReviewModalOpen(false);
          setReviewingDeclaration(null);
        }}
        onSubmitReview={handleSubmitReview}
        isSubmitting={isSubmittingReview}
        isMock={defaultInspectionClient.isMock}
        onToggleCaliperMode={() => setIsCaliperMode((prev) => !prev)}
        isCaliperActive={isCaliperMode}
        caliperPoints={caliperPoints}
        onClearCaliperPoints={() =>
          setCaliperPoints({ pointA: null, pointB: null })
        }
      />
    </div>
  );
}
