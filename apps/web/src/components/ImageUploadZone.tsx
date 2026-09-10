"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import {
  UploadCloud,
  FileImage,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Trash2,
  Sparkles,
  ArrowRight,
  Shield,
  Layers,
  Sliders,
} from "lucide-react";
import { Button, Card, Badge, Alert, LoadingState } from "@/components/ui";
import {
  validateInspectionImage,
  formatFileSize,
  FileValidationResult,
  MAX_FILE_SIZE_BYTES,
} from "@/utils/validation";
import {
  IInspectionClient,
  InspectionClientError,
  defaultInspectionClient,
  createInspectionClient,
  InspectionClientMode,
} from "@/services";
import { FrontendInspectionModel } from "@/types/frontend";

export type UploadState =
  | "EMPTY"
  | "SELECTED"
  | "VALIDATING"
  | "READY"
  | "INSPECTING"
  | "SUCCESS"
  | "ERROR";

export interface ImageUploadZoneProps {
  onInspectionComplete?: (result: FrontendInspectionModel) => void;
  onFileCleared?: () => void;
  onFileReady?: (
    file: File,
    previewUrl: string,
    dimensions?: { width: number; height: number }
  ) => void;
  initialMode?: InspectionClientMode;
  allowUpload?: boolean;
  inspectionDisabled?: boolean;
  onFileChanging?: () => void;
  clientMode?: InspectionClientMode;
  onModeChange?: (mode: InspectionClientMode) => void;
  externalFile?: File | null;
  resetTrigger?: number;
  className?: string;
}

export function ImageUploadZone({
  onInspectionComplete,
  onFileCleared,
  onFileReady,
  initialMode = "mock",
  allowUpload = true,
  inspectionDisabled = false,
  onFileChanging,
  clientMode: controlledClientMode,
  onModeChange,
  externalFile,
  resetTrigger,
  className = "",
}: ImageUploadZoneProps) {
  // State Machine
  const [state, setState] = useState<UploadState>("EMPTY");
  const [isDragOver, setIsDragOver] = useState(false);

  // File & Preview state
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileDimensions, setFileDimensions] = useState<{
    width: number;
    height: number;
  } | null>(null);

  // Error state
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [errorDetails, setErrorDetails] = useState<string | null>(null);

  // Inspection client mode state
  const [clientMode, setClientMode] = useState<InspectionClientMode>(
    controlledClientMode || initialMode
  );
  const [client, setClient] = useState<IInspectionClient>(() =>
    createInspectionClient(controlledClientMode || initialMode)
  );

  // Sync with controlled mode if provided
  useEffect(() => {
    if (controlledClientMode && controlledClientMode !== clientMode) {
      setClientMode(controlledClientMode);
      setClient(createInspectionClient(controlledClientMode));
    }
  }, [controlledClientMode, clientMode]);

  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);
  const fileVersion = useRef(0);
  const validFile = useRef(false);
  const previewUrlRef = useRef<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Safely manage Object URL cleanup to prevent memory leaks
  const cleanupPreviewUrl = useCallback(() => {
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current);
      previewUrlRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      fileVersion.current += 1;
      cleanupPreviewUrl();
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [cleanupPreviewUrl]);

  // Update client when mode changes
  const handleModeToggle = (mode: InspectionClientMode) => {
    setClientMode(mode);
    setClient(createInspectionClient(mode));
    onModeChange?.(mode);
  };

  // Reset ingestion zone
  const handleClear = useCallback(() => {
    fileVersion.current += 1;
    validFile.current = false;
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    cleanupPreviewUrl();
    setSelectedFile(null);
    setPreviewUrl(null);
    setFileDimensions(null);
    setErrorMessage(null);
    setErrorDetails(null);
    setState("EMPTY");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    onFileCleared?.();
  }, [cleanupPreviewUrl, onFileCleared]);

  // File ingestion & validation pipeline
  const processFile = async (file: File) => {
    const version = ++fileVersion.current;
    abortControllerRef.current?.abort();
    validFile.current = false;
    onFileChanging?.();
    cleanupPreviewUrl();
    setPreviewUrl(null);
    setFileDimensions(null);
    setSelectedFile(file);
    setErrorMessage(null);
    setErrorDetails(null);
    setState("VALIDATING");

    const validation: FileValidationResult = await validateInspectionImage(file);

    if (version !== fileVersion.current) return;
    if (!validation.valid && validation.error) {
      setState("ERROR");
      setErrorMessage(validation.error.message);
      setErrorDetails(validation.error.details || null);
      return;
    }

    validFile.current = true;
    // Allocate safe Object URL for thumbnail
    const url = URL.createObjectURL(file);
    previewUrlRef.current = url;
    setPreviewUrl(url);

    if (validation.dimensions) {
      setFileDimensions(validation.dimensions);
    }

    setState("READY");
    onFileReady?.(file, url, validation.dimensions);
  };

  const processFileRef = useRef(processFile);
  processFileRef.current = processFile;

  // Respond only to a newly selected file, using the current callbacks.
  useEffect(() => {
    if (externalFile) {
      processFileRef.current(externalFile);
    }
  }, [externalFile]);

  const prevResetTriggerRef = useRef(resetTrigger || 0);

  // Respond to resetTrigger
  useEffect(() => {
    if (resetTrigger && resetTrigger > prevResetTriggerRef.current) {
      handleClear();
    }
    prevResetTriggerRef.current = resetTrigger || 0;
  }, [resetTrigger, handleClear]);

  // Drag-and-drop handlers
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    // Only deactivate if leaving the container
    if (e.currentTarget.contains(e.relatedTarget as Node)) return;
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (state === "INSPECTING" || !allowUpload) return;

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  // File input change handler
  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  // Trigger inspection
  const handleInspect = async () => {
    if (!selectedFile || !validFile.current || inspectionDisabled || state === "INSPECTING") return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const currentAbort = new AbortController();
    abortControllerRef.current = currentAbort;

    setState("INSPECTING");
    setErrorMessage(null);
    setErrorDetails(null);

    try {
      const result = await client.inspect(selectedFile, {
        signal: currentAbort.signal,
      });

      if (currentAbort.signal.aborted) return;

      setState("SUCCESS");
      onInspectionComplete?.(result);
    } catch (err: any) {
      if (currentAbort.signal.aborted) return;

      setState("ERROR");
      if (err instanceof InspectionClientError) {
        setErrorMessage(err.message);
        setErrorDetails(err.remediationHint || `Error Code: ${err.code}`);
      } else {
        setErrorMessage("An unexpected error occurred during package inspection.");
        setErrorDetails(err?.message || "Unknown internal error");
      }
    }
  };

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="text-xs text-slate-600" role="status">{clientMode === "mock" ? "Prepared demonstration result · no live analysis" : "Live analysis · image sent to the configured service"}</div>

      {/* Main Upload Dropzone Stadium Card */}
      <Card
        shape="stadium"
        variant="lifted"
        className={`relative overflow-hidden p-6 sm:p-8 transition-all duration-300 border-2 ${
          isDragOver
            ? "border-signal-orange bg-signal-orange/5 shadow-deep scale-[1.01]"
            : state === "ERROR"
            ? "border-red-300 bg-red-50/20"
            : "border-black/[0.08] hover:border-black/20"
        }`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        role="region"
        aria-label="Packaging image upload zone"
      >
        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileInputChange}
          className="sr-only"
          id="officer-file-upload"
          aria-label="Select packaging photograph"
          disabled={!allowUpload || state === "INSPECTING"}
        />

        {/* State: EMPTY (Initial Drag-and-Drop View) */}
        {state === "EMPTY" && (
          <div
            onClick={() => { if (allowUpload) fileInputRef.current?.click(); }}
            onKeyDown={(e) => {
              if (allowUpload && (e.key === "Enter" || e.key === " ")) {
                e.preventDefault();
                fileInputRef.current?.click();
              }
            }}
            tabIndex={allowUpload ? 0 : -1}
            role="group"
            className="flex flex-col items-center justify-center text-center py-8 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal-orange rounded-stadium"
          >
            {/* Circular Portrait Icon with Attached Satellite micro-CTA */}
            <div className="relative my-2 group">
              <div className="w-24 h-24 rounded-full bg-white border border-black/[0.08] flex items-center justify-center shadow-halo group-hover:scale-105 transition-transform duration-300">
                <UploadCloud className="w-10 h-10 text-ink/80" />
              </div>
              <div
                className="absolute -bottom-1 -right-1 w-9 h-9 rounded-full bg-signal-orange text-white shadow-sm flex items-center justify-center satellite-cta"
                aria-hidden="true"
              >
                <ArrowRight className="w-4 h-4" />
              </div>
            </div>

            <div className="space-y-1.5 mt-4 max-w-sm">
              <h3 className="text-lg font-medium tracking-headline text-ink">
                {allowUpload ? "Upload Package Photograph" : "Choose a Demonstration Example"}
              </h3>
              <p
                id="upload-instructions"
                className="text-xs text-slate-500 leading-relaxed"
              >
                {allowUpload ? "Drag and drop a clear packaging image, or choose a file. " : "Select one of the examples above. Live Inspection is required for your own photographs. "}
                <span className="font-semibold text-slate-700">JPEG, PNG, WebP</span> (Max 15MB).
              </p>
            </div>

            <div className="mt-5">
              <Button
                type="button"
                variant="primary"
                size="sm"
                disabled={!allowUpload}
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
              >
                {allowUpload ? "Choose Image File" : "Choose an Example Above"}
              </Button>
            </div>
          </div>
        )}

        {/* State: VALIDATING */}
        {state === "VALIDATING" && (
          <div className="py-12 flex flex-col items-center justify-center text-center space-y-3">
            <LoadingState
              title="Validating Package Photograph"
              description="Testing file format, binary magic bytes, and raster integrity..."
              className="py-4 bg-transparent border-none p-4"
            />
          </div>
        )}

        {/* State: READY or SUCCESS or ERROR (Preview Mode) */}
        {(state === "READY" || state === "SUCCESS" || state === "ERROR") && selectedFile && (
          <div className="space-y-6">
            {/* Preview Frame with Aspect Ratio Preservation */}
            <div className="relative bg-white rounded-3xl p-4 border border-black/[0.06] shadow-sm flex flex-col sm:flex-row items-center gap-5">
              {/* Thumbnail Container */}
              <div className="w-full sm:w-44 h-40 rounded-2xl bg-canvas flex items-center justify-center overflow-hidden border border-black/[0.06] flex-shrink-0">
                {previewUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={previewUrl}
                    alt={`Preview of ${selectedFile.name}`}
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <FileImage className="w-12 h-12 text-slate-400" />
                )}
              </div>

              {/* Metadata & Details */}
              <div className="flex-1 min-w-0 space-y-3 text-left w-full">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="default" size="sm">
                      {selectedFile.type || "IMAGE"}
                    </Badge>
                    {fileDimensions && (
                      <span className="text-[11px] font-mono font-medium text-slate-500">
                        {fileDimensions.width} × {fileDimensions.height} px
                      </span>
                    )}
                  </div>
                  <h4
                    className="text-sm font-semibold text-ink truncate"
                    title={selectedFile.name}
                  >
                    {selectedFile.name}
                  </h4>
                  <p className="text-xs text-slate-500">
                    Size: {formatFileSize(selectedFile.size)} · Status:{" "}
                    <span className="font-medium">{validFile.current ? "Validated" : "Rejected"}</span>
                  </p>
                </div>

                {/* Actions: Replace / Remove */}
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => { if (allowUpload) fileInputRef.current?.click(); }}
                    disabled={!allowUpload}
                    aria-label="Replace package photograph"
                  >
                    <RefreshCw className="w-3.5 h-3.5 mr-1 text-slate-600" />
                    Replace
                  </Button>

                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={handleClear}
                    className="text-red-700 hover:bg-red-50 hover:border-red-200"
                    aria-label="Remove selected image"
                  >
                    <Trash2 className="w-3.5 h-3.5 mr-1 text-red-600" />
                    Remove
                  </Button>
                </div>
              </div>
            </div>

            {/* Error Message Box if in ERROR state */}
            {state === "ERROR" && errorMessage && (
              <Alert variant="error" title="Image Ingestion Rejected">
                <p>{errorMessage}</p>
                {errorDetails && (
                  <p className="text-xs mt-1 text-red-600 font-mono">
                    {errorDetails}
                  </p>
                )}
                {clientMode === "live" && (
                  <div className="mt-3 pt-2 border-t border-red-200/60">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => handleModeToggle("mock")}
                      className="bg-white hover:bg-red-50 text-red-900 border-red-300 text-xs font-semibold shadow-xs"
                    >
                      Switch to Synthetic Demo Mode
                    </Button>
                  </div>
                )}
              </Alert>
            )}

            {/* Primary Action: Inspect Package */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-black/[0.06]">
              <span className="text-xs text-slate-500">
                {clientMode === "mock" ? "Display the prepared result for this example." : inspectionDisabled ? "Configure live service access before inspecting." : "Ready for image-based assessment."}
              </span>

              <Button
                type="button"
                variant="signal"
                size="md"
                onClick={handleInspect}
                disabled={!selectedFile || !validFile.current || inspectionDisabled}
                className="w-full sm:w-auto"
              >
                <Sparkles className="w-4 h-4 mr-1.5" />
                Inspect Package
              </Button>
            </div>
          </div>
        )}

        {/* State: INSPECTING (Live Processing State) */}
        {state === "INSPECTING" && (
          <div className="py-10 flex flex-col items-center justify-center text-center space-y-4">
            <LoadingState
              title={
                clientMode === "mock"
                  ? "Inspecting Package (Synthetic Regression Sandbox)"
                  : "Submitting to Live Inspection Pipeline"
              }
              description={
                clientMode === "mock"
                  ? "Loading the prepared demonstration result..."
                  : "Uploading and analyzing your package photograph..."
              }
              stageName="Rule 6 & Rule 7 Verification"
              className="py-4 bg-transparent border-none p-4"
            />
            <p className="text-xs text-slate-500 max-w-sm">
              {clientMode === "mock" ? "Demonstration data does not establish real packaging compliance." : "Processing time depends on image size and server availability."}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
}
