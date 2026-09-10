"use client";

import React, { useState, useCallback, useEffect, useMemo, useRef } from "react";
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
  createInspectionClient,
  defaultReportClient,
  InspectionClientMode,
} from "@/services";

import { resolveApiBaseUrl, setApiAccessKey } from "@/services/apiConfig";

export default function OfficerWorkstationPage() {
  const [isGuideOpen, setIsGuideOpen] = useState(false);
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

  const inspectionClient = useMemo(() => createInspectionClient(clientMode), [clientMode]);
  const [accessKey, setAccessKey] = useState("");
  const [connectionMessage, setConnectionMessage] = useState<string | null>(null);
  const [checkingConnection, setCheckingConnection] = useState(false);
  const sessionVersion = useRef(0);
  const reportAbort = useRef<AbortController | null>(null);
  useEffect(() => () => { reportAbort.current?.abort(); setApiAccessKey(""); }, []);

  const checkConnection = async () => {
    setCheckingConnection(true);
    const health = await inspectionClient.getHealth();
    setConnectionMessage(health.message || health.status);
    setCheckingConnection(false);
  };

  // Keep review results bound to the inspection that initiated them.
  const handleSubmitReview = async (input: ReviewSubmissionInput) => {
    const version = sessionVersion.current;
    setIsSubmittingReview(true);
    try {
      const result = await inspectionClient.submitReview(input);
      if (version !== sessionVersion.current) return result;

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

  // Clear workstation inspection state without incrementing resetTrigger
  const handleFileCleared = useCallback(() => {
    sessionVersion.current += 1;
    reportAbort.current?.abort();
    setIsGeneratingReport(false);
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
  }, []);

  // 1. Reset complete inspection state (Session Reset)
  const handleStartNewInspection = useCallback(() => {
    handleFileCleared();
    setResetTrigger((prev) => prev + 1);
  }, [handleFileCleared]);

  // 2. Select benchmark sample package
  const handleSelectSample = (
    file: File,
    previewUrl: string,
    sample: SamplePackageItem
  ) => {
    sessionVersion.current += 1;
    reportAbort.current?.abort();
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
    if (!inspectionResult || inspectionResult.isSynthetic || isGeneratingReport) return;
    const version = sessionVersion.current;
    const controller = new AbortController();
    reportAbort.current = controller;
    setIsGeneratingReport(true);
    setReportError(null);
    setReportSuccess(null);

    try {
      const res = await defaultReportClient.downloadAssessmentReport(
        inspectionResult.inspectionId,
        {
          officerNotes: "Image-based packaging assessment; subject to human review.",
          signal: controller.signal,
          includeRawImage: true,
        }
      );
      if (version !== sessionVersion.current) return;
      setReportSuccess(
        `Assessment report successfully compiled & downloaded (${(res.byteSize / 1024).toFixed(1)} KB).`
      );
    } catch (err: any) {
      if (version !== sessionVersion.current) return;
      setReportError(
        err?.message ||
          "Report generation unavailable: Backend report endpoint POST /api/v1/report/pdf is offline."
      );
    } finally {
      if (version === sessionVersion.current) setIsGeneratingReport(false);
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
          PACKAGING ASSESSMENT PROTOTYPE
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-medium tracking-headline text-ink leading-[1.08]">
          Image-based packaging checks for human review.
        </h1>

        <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal max-w-2xl">
          Review visible packaging declarations with image evidence and deterministic checks.
          This prototype assists human review; it does not certify legal compliance or issue official notices.
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
              FROM PHOTOGRAPH TO EVIDENCE
            </div>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-headline text-ink">
              How image-based assessment works
            </h2>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            CPU-based OCR · Human review required
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
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta"
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
                  Blur and glare checks identify images that need to be retaken before assessment.
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
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta"
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
                  A visible reference can support scale estimation. Without verified panel geometry,
                  font-size compliance requires manual measurement.
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
                  className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white border border-black/[0.08] shadow-halo flex items-center justify-center satellite-cta"
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
                  Checks cover visible declarations and unit-sale-price arithmetic.
                  An inspector must verify uncertain text, missing panels, and applicable exemptions.
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
              ASSESSMENT WORKSPACE
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
                title="Explore demonstration results without uploading to a server"
                aria-pressed={clientMode === "mock"}
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
                title="Analyze an image with the configured backend"
                aria-pressed={clientMode === "live"}
              >
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-700" />
                LIVE INSPECTION
              </button>
            </div>

            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-pill bg-white text-xs text-ink font-medium border border-black/[0.06] shadow-sm">
              <Lock className="w-3.5 h-3.5 text-emerald-600" />
              {inspectionResult && !inspectionResult.isSynthetic ? "Image digest recorded" : "No evidence recorded"}
            </span>

            {/* Workstation Actions: Report & Reset */}
            {inspectionResult && (
              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant="primary"
                  onClick={handleDownloadReport}
                  disabled={isGeneratingReport || inspectionResult.isSynthetic}
                  title={inspectionResult.isSynthetic ? "Reports are available only for real inspections" : "Download image-based assessment"}
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

        {clientMode === "live" && (
          <Card className="p-5 space-y-3">
            <h3 className="font-semibold">Live service access</h3>
            <p className="text-sm text-slate-600">{resolveApiBaseUrl() ? "Enter the service access key supplied by the deployment owner. This grants service access; it does not verify an officer identity." : "Live analysis is not configured on this deployment. You can explore the synthetic examples below by selecting Synthetic Demo."}</p>
            {resolveApiBaseUrl() && <>
              <label htmlFor="service-access-key" className="block text-sm font-medium">Service access key</label>
              <input id="service-access-key" type="password" autoComplete="off" value={accessKey}
                className="rounded-xl border p-3 w-full max-w-md"
                onChange={(event) => { setAccessKey(event.target.value); setApiAccessKey(event.target.value); }} />
              <p className="text-xs text-slate-600">Kept in this tab&apos;s memory until cleared or closed. Images are sent to the configured inspection service when you click Inspect Package.</p>
              <div className="flex gap-2"><Button size="sm" onClick={checkConnection} disabled={checkingConnection}>{checkingConnection ? "Checking…" : "Check connection"}</Button>
                <Button size="sm" variant="secondary" onClick={() => { setAccessKey(""); setApiAccessKey(""); handleStartNewInspection(); }}>Clear access</Button></div>
              {connectionMessage && <p role="status" className="text-sm">{connectionMessage}</p>}
            </>}
          </Card>
        )}
        {clientMode === "mock" && <Alert variant="warning" title="Synthetic demonstration">
          These examples show prepared results. They do not analyze your photograph, establish compliance, or produce official reports. Select Live Inspection to analyze a real image.
        </Alert>}
        {/* Synthetic Demonstration Fixtures Card (8 Fixtures) */}
        {clientMode === "mock" && <Card shape="stadium" variant="white" className="p-5 border border-black/[0.06] shadow-halo">
          <SamplePackageSelector
            selectedSampleId={selectedSampleId}
            onSelectSample={handleSelectSample}
            disabled={isGeneratingReport}
          />
        </Card>}

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
              allowUpload={clientMode === "live"}
              inspectionDisabled={clientMode === "live" && (!resolveApiBaseUrl() || !accessKey)}
              onFileChanging={() => {
                sessionVersion.current += 1;
                reportAbort.current?.abort();
                setInspectionResult(null);
                setUploadedImageSrc(null);
                setImageDimensions(null);
                setSelectedTokenId(null);
                setSelectedFieldName(null);
                setIsReviewModalOpen(false);
                setReportError(null);
                setReportSuccess(null);
                setIsGeneratingReport(false);
              }}
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
              }}
              onFileCleared={handleFileCleared}
            />

            <Alert variant="info" title="Capture guidance">
              Photographs must clearly include the Principal Display Panel (PDP) and any calibration
              anchor on the same flat plane. Include other panels in a separate assessment when declarations are not visible. Actual contents and product quality cannot be verified from a photograph.
            </Alert>
          </div>

          {/* Right Column: Statutory Adjudication, Evidence Canvas & Declaration Table */}
          <div className="lg:col-span-7 space-y-6">
            {inspectionResult ? (
              <div className="space-y-6">
                {/* Enforcement Dossier Action Card */}
                <div className="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-signal-orange/10 flex items-center justify-center">
                      <FileText className="w-5 h-5 text-signal-orange" />
                    </div>
                    <div>
                      <div className="text-xs font-bold uppercase tracking-eyebrow text-slate-500">
                        IMAGE-BASED ASSESSMENT
                      </div>
                      <div className="text-sm font-semibold text-ink font-mono">
                        {inspectionResult.inspectionId}
                      </div>
                    </div>
                  </div>

                  <Button
                    variant="primary"
                    size="sm"
                    onClick={handleDownloadReport}
                    disabled={isGeneratingReport || inspectionResult.isSynthetic}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    {isGeneratingReport ? "Compiling PDF..." : "Download Assessment (PDF)"}
                  </Button>
                </div>

                {reportSuccess && (
                  <Alert variant="success" title="Dossier Compiled">
                    <p className="text-xs leading-relaxed">{reportSuccess}</p>
                  </Alert>
                )}

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
                <Alert variant="info" title="No inspection yet">Select a demonstration example or upload an image in Live Inspection. No compliance result has been issued.</Alert>

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
                      Results apply only to the visible image evidence.
                    </span>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </section>

      <section id="scope" className="space-y-5 pt-8 border-t border-black/10">
        <h2 className="text-2xl font-medium">Scope and limitations</h2>
        <p className="text-sm text-slate-700">This MVP assesses one JPEG, PNG, or WebP packaging image at a time. Live images must be at least 800 × 600 pixels, no larger than 8000 pixels per side or 40 megapixels, and under 15 MiB. English and Hindi OCR can make mistakes. Missing text on one panel is not proof that the complete package omits it.</p>
        <div className="grid sm:grid-cols-2 gap-5">
          <Card className="p-5 space-y-2" id="regulatory-framework"><h3 className="font-semibold">Human review and legal context</h3><p className="text-sm text-slate-600">Results identify possible discrepancies for review. Exemptions, effective legal amendments, package geometry, and physical measurements need independent verification. There is no live eMaap integration or government endorsement.</p></Card>
          <Card className="p-5 space-y-2" id="privacy"><h3 className="font-semibold">Image handling</h3><p className="text-sm text-slate-600">Demo examples stay in the browser. Live uploads are sent to temporary storage on the inspection backend. Assessment records expire after one hour or earlier on restart; image cleanup runs periodically while the service is active. Original photos can contain location metadata. Avoid uploading personal or confidential information.</p></Card>
          <Card className="p-5 space-y-2" id="evidence"><h3 className="font-semibold">Evidence and reports</h3><p className="text-sm text-slate-600">A SHA-256 digest checks whether retained image bytes changed. It is not a digital signature or proof of legal admissibility. Reports describe stored assessment results and require human verification.</p></Card>
          <Card className="p-5 space-y-2" id="terms"><h3 className="font-semibold">Prototype use</h3><p className="text-sm text-slate-600">MetroLens is a project prototype for inspection assistance. It does not make enforcement decisions, issue statutory notices, authenticate government officers, or certify products.</p></Card>
        </div>
      </section>

      {/* Accessible Workstation SOP Dialog */}
      <Dialog
        isOpen={isGuideOpen}
        onClose={() => setIsGuideOpen(false)}
        title="MetroLens Inspection Protocol"
        description="How to capture and review a packaging image"
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
              <li><strong className="text-ink">Metric Scale Recovery:</strong> Reference scale estimation; on-screen calipers show pixel distances only.</li>
              <li><strong className="text-ink">Multilingual Scene OCR:</strong> PP-OCRv3 on CPU extracts English and Devanagari text.</li>
              <li><strong className="text-ink">Deterministic State Machine:</strong> Deterministic checks assist human review; a digest records image integrity.</li>
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
        isMock={inspectionClient.isMock}
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
