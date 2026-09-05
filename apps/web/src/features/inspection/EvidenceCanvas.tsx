"use client";

import React, {
  useRef,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Crosshair,
  Eye,
  AlertTriangle,
  Info,
  Check,
  ChevronDown,
  ChevronUp,
  Layers,
  Sparkles,
} from "lucide-react";
import { Button, Badge, Card, Tooltip } from "@/components/ui";
import { OCRTokenModel } from "@/types/frontend";
import {
  CanvasTransform,
  Point,
  imageToCanvas,
  canvasToImage,
  fitToScreen,
  zoomAt,
  pointInPolygon,
  pointInBBox,
  sanitizePolygon,
} from "./canvasTransform";

export interface EvidenceCanvasProps {
  imageSrc: string | null;
  imageWidth?: number;
  imageHeight?: number;
  tokens: OCRTokenModel[];
  selectedTokenId?: string | null;
  highlightedTokenIds?: string[];
  onSelectToken?: (tokenId: string | null) => void;
  isSynthetic?: boolean;
  isCaliperMode?: boolean;
  onToggleCaliperMode?: () => void;
  caliperPoints?: { pointA: Point | null; pointB: Point | null };
  onCaliperPointsChange?: (points: {
    pointA: Point | null;
    pointB: Point | null;
    distancePixels: number | null;
  }) => void;
  onClearCaliperPoints?: () => void;
  className?: string;
}

export function EvidenceCanvas({
  imageSrc,
  imageWidth = 640,
  imageHeight = 360,
  tokens = [],
  selectedTokenId = null,
  highlightedTokenIds = [],
  onSelectToken,
  isSynthetic = false,
  isCaliperMode = false,
  onToggleCaliperMode,
  caliperPoints = { pointA: null, pointB: null },
  onCaliperPointsChange,
  onClearCaliperPoints,
  className = "",
}: EvidenceCanvasProps) {
  // DOM References
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageObjRef = useRef<HTMLImageElement | null>(null);

  // Interaction State
  const [transform, setTransform] = useState<CanvasTransform>({
    scale: 1,
    panX: 0,
    panY: 0,
  });
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [hoveredTokenId, setHoveredTokenId] = useState<string | null>(null);
  const [hoverTooltip, setHoverTooltip] = useState<{
    x: number;
    y: number;
    token: OCRTokenModel;
  } | null>(null);

  // Drag-to-Pan state tracking
  const isDraggingRef = useRef(false);
  const dragStartRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const dragDistanceRef = useRef(0);
  const [isPanning, setIsPanning] = useState(false);

  // Accessible evidence drawer toggle
  const [isEvidenceListOpen, setIsEvidenceListOpen] = useState(true);

  // Filter toggle for low-confidence tokens (display only)
  const [showOnlyReview, setShowOnlyReview] = useState(false);

  // Load and cache Image bitmap
  useEffect(() => {
    if (!imageSrc) {
      imageObjRef.current = null;
      setImageLoaded(false);
      setImageError(false);
      return;
    }

    const img = new Image();
    img.crossOrigin = "anonymous";

    img.onload = () => {
      imageObjRef.current = img;
      setImageLoaded(true);
      setImageError(false);

      // Perform initial fit to screen once container has dimensions
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          const initialT = fitToScreen(
            img.naturalWidth || imageWidth,
            img.naturalHeight || imageHeight,
            rect.width,
            rect.height,
            24
          );
          setTransform(initialT);
        }
      }
    };

    img.onerror = () => {
      imageObjRef.current = null;
      setImageLoaded(false);
      setImageError(true);
    };

    img.src = imageSrc;

    return () => {
      img.onload = null;
      img.onerror = null;
    };
  }, [imageSrc, imageWidth, imageHeight]);

  // Fit to screen helper
  const handleFitToScreen = useCallback(() => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const w = imageObjRef.current?.naturalWidth || imageWidth;
    const h = imageObjRef.current?.naturalHeight || imageHeight;
    const newT = fitToScreen(w, h, rect.width, rect.height, 24);
    setTransform(newT);
  }, [imageWidth, imageHeight]);

  // Handle Container Resizing
  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver(() => {
      // Re-render canvas on dimension resize
      renderCanvas();
    });

    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, []);

  // Filtered tokens for rendering
  const displayedTokens = useMemo(() => {
    if (!showOnlyReview) return tokens;
    return tokens.filter((t) => t.requiresReview);
  }, [tokens, showOnlyReview]);

  // Primary Canvas Render Loop
  const renderCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);

    if (width === 0 || height === 0) return;

    // Synchronize high-DPI backing buffer
    if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
    }

    ctx.save();
    ctx.scale(dpr, dpr);

    // Clear canvas with subtle cream canvas background
    ctx.fillStyle = "#F3F0EE";
    ctx.fillRect(0, 0, width, height);

    // Apply affine transform for image and polygon space
    ctx.translate(transform.panX, transform.panY);
    ctx.scale(transform.scale, transform.scale);

    // 1. Render Original Packaging Image
    if (imageObjRef.current && imageLoaded) {
      ctx.drawImage(
        imageObjRef.current,
        0,
        0,
        imageObjRef.current.naturalWidth,
        imageObjRef.current.naturalHeight
      );
    } else {
      // Fallback grid when image is loading or absent
      ctx.strokeStyle = "rgba(0, 0, 0, 0.05)";
      ctx.lineWidth = 1 / transform.scale;
      ctx.strokeRect(0, 0, imageWidth, imageHeight);
    }

    // 2. Render OCR Polygons in Original Image Pixel Space
    for (const token of displayedTokens) {
      const isSelected = token.id === selectedTokenId;
      const isLinked = !isSelected && highlightedTokenIds.includes(token.id);
      const isHovered = !isSelected && !isLinked && token.id === hoveredTokenId;
      const isReview = token.requiresReview;

      const poly = sanitizePolygon(token.polygon, token.boundingBox);

      ctx.beginPath();
      ctx.moveTo(poly[0][0], poly[0][1]);
      ctx.lineTo(poly[1][0], poly[1][1]);
      ctx.lineTo(poly[2][0], poly[2][1]);
      ctx.lineTo(poly[3][0], poly[3][1]);
      ctx.closePath();

      // Style determination
      if (isSelected) {
        // Selected: Vibrant Signal Orange with halo
        ctx.fillStyle = "rgba(207, 69, 0, 0.25)";
        ctx.fill();
        ctx.strokeStyle = "#CF4500";
        ctx.lineWidth = 2.5 / transform.scale;
        ctx.setLineDash([]);
        ctx.stroke();
      } else if (isLinked) {
        // Declaration-Linked Evidence: Vibrant Royal Blue highlight
        ctx.fillStyle = "rgba(37, 99, 235, 0.18)";
        ctx.fill();
        ctx.strokeStyle = "#2563EB";
        ctx.lineWidth = 2.2 / transform.scale;
        ctx.setLineDash([]);
        ctx.stroke();
      } else if (isHovered) {
        // Hovered: Signal Orange translucent highlight
        ctx.fillStyle = "rgba(207, 69, 0, 0.12)";
        ctx.fill();
        ctx.strokeStyle = "#CF4500";
        ctx.lineWidth = 2.0 / transform.scale;
        ctx.setLineDash([]);
        ctx.stroke();
      } else if (isReview) {
        // Low Confidence / Review: Dashed Amber Boundary
        ctx.fillStyle = "rgba(217, 119, 6, 0.08)";
        ctx.fill();
        ctx.strokeStyle = "#D97706";
        ctx.lineWidth = 1.5 / transform.scale;
        ctx.setLineDash([4 / transform.scale, 4 / transform.scale]);
        ctx.stroke();
      } else {
        // Default Evidence Token: Clean Orange Border
        ctx.fillStyle = "rgba(207, 69, 0, 0.03)";
        ctx.fill();
        ctx.strokeStyle = "rgba(207, 69, 0, 0.45)";
        ctx.lineWidth = 1.2 / transform.scale;
        ctx.setLineDash([]);
        ctx.stroke();
      }
    }

    // 3. Render Caliper Reference Points (Manual Reference Mode)
    if (isCaliperMode) {
      const { pointA, pointB } = caliperPoints;

      if (pointA) {
        // Point A Crosshair & Dot
        ctx.strokeStyle = "#059669";
        ctx.fillStyle = "#059669";
        ctx.lineWidth = 2.0 / transform.scale;
        ctx.setLineDash([]);

        const cross = 8 / transform.scale;
        ctx.beginPath();
        ctx.moveTo(pointA.x - cross, pointA.y);
        ctx.lineTo(pointA.x + cross, pointA.y);
        ctx.moveTo(pointA.x, pointA.y - cross);
        ctx.lineTo(pointA.x, pointA.y + cross);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(pointA.x, pointA.y, 3.5 / transform.scale, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = `bold ${11 / transform.scale}px monospace`;
        ctx.fillStyle = "#064E3B";
        ctx.fillText(`A (${pointA.x}, ${pointA.y})`, pointA.x + 6 / transform.scale, pointA.y - 6 / transform.scale);
      }

      if (pointB) {
        // Point B Crosshair & Dot
        ctx.strokeStyle = "#0284C7";
        ctx.fillStyle = "#0284C7";
        ctx.lineWidth = 2.0 / transform.scale;
        ctx.setLineDash([]);

        const cross = 8 / transform.scale;
        ctx.beginPath();
        ctx.moveTo(pointB.x - cross, pointB.y);
        ctx.lineTo(pointB.x + cross, pointB.y);
        ctx.moveTo(pointB.x, pointB.y - cross);
        ctx.lineTo(pointB.x, pointB.y + cross);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(pointB.x, pointB.y, 3.5 / transform.scale, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = `bold ${11 / transform.scale}px monospace`;
        ctx.fillStyle = "#0C4A6E";
        ctx.fillText(`B (${pointB.x}, ${pointB.y})`, pointB.x + 6 / transform.scale, pointB.y - 6 / transform.scale);
      }

      if (pointA && pointB) {
        // Connecting Reference Line
        ctx.strokeStyle = "#4F46E5";
        ctx.lineWidth = 2.0 / transform.scale;
        ctx.setLineDash([4 / transform.scale, 4 / transform.scale]);
        ctx.beginPath();
        ctx.moveTo(pointA.x, pointA.y);
        ctx.lineTo(pointB.x, pointB.y);
        ctx.stroke();
        ctx.setLineDash([]);

        const midX = (pointA.x + pointB.x) / 2;
        const midY = (pointA.y + pointB.y) / 2;
        const distPx = Math.hypot(pointB.x - pointA.x, pointB.y - pointA.y);

        ctx.font = `bold ${11 / transform.scale}px sans-serif`;
        const labelText = `${distPx.toFixed(1)} px (optical)`;
        const textWidth = ctx.measureText(labelText).width;

        ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
        ctx.fillRect(
          midX - textWidth / 2 - 4 / transform.scale,
          midY - 14 / transform.scale,
          textWidth + 8 / transform.scale,
          16 / transform.scale
        );

        ctx.fillStyle = "#FFFFFF";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(labelText, midX, midY - 6 / transform.scale);
        ctx.textAlign = "start";
        ctx.textBaseline = "alphabetic";
      }
    }

    ctx.restore();
  }, [
    transform,
    imageLoaded,
    imageWidth,
    imageHeight,
    displayedTokens,
    selectedTokenId,
    highlightedTokenIds,
    hoveredTokenId,
    isCaliperMode,
    caliperPoints,
  ]);

  // Request render when transform or selection changes
  useEffect(() => {
    let animId: number;
    const scheduleRender = () => {
      animId = requestAnimationFrame(renderCanvas);
    };
    scheduleRender();
    return () => cancelAnimationFrame(animId);
  }, [renderCanvas]);

  // Zoom Controls
  const handleZoomIn = () => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const center: Point = { x: rect.width / 2, y: rect.height / 2 };
    setTransform((prev) => zoomAt(center, prev, 1.25));
  };

  const handleZoomOut = () => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const center: Point = { x: rect.width / 2, y: rect.height / 2 };
    setTransform((prev) => zoomAt(center, prev, 0.8));
  };

  const handleReset = () => {
    handleFitToScreen();
  };

  // Center and focus on a specific token
  const focusToken = useCallback(
    (token: OCRTokenModel) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const poly = sanitizePolygon(token.polygon, token.boundingBox);
      const tokenCenterX = (poly[0][0] + poly[2][0]) / 2;
      const tokenCenterY = (poly[0][1] + poly[2][1]) / 2;

      // Target scale 2.2x for inspection
      const targetScale = Math.max(transform.scale, 1.8);
      const newPanX = rect.width / 2 - tokenCenterX * targetScale;
      const newPanY = rect.height / 2 - tokenCenterY * targetScale;

      setTransform({
        scale: targetScale,
        panX: newPanX,
        panY: newPanY,
      });

      onSelectToken?.(token.id);
    },
    [transform.scale, onSelectToken]
  );

  // Center and fit a union bounding box for multiple tokens
  const focusTokensUnion = useCallback(
    (targetTokens: OCRTokenModel[]) => {
      if (!containerRef.current || targetTokens.length === 0) return;
      const rect = containerRef.current.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      let minX = Infinity;
      let minY = Infinity;
      let maxX = -Infinity;
      let maxY = -Infinity;

      for (const t of targetTokens) {
        const poly = sanitizePolygon(t.polygon, t.boundingBox);
        for (const pt of poly) {
          if (pt[0] < minX) minX = pt[0];
          if (pt[1] < minY) minY = pt[1];
          if (pt[0] > maxX) maxX = pt[0];
          if (pt[1] > maxY) maxY = pt[1];
        }
      }

      if (!isFinite(minX)) return;

      const unionWidth = Math.max(maxX - minX, 30);
      const unionHeight = Math.max(maxY - minY, 30);
      const centerX = (minX + maxX) / 2;
      const centerY = (minY + maxY) / 2;

      // Fit with 48px padding
      const scaleX = (rect.width - 96) / unionWidth;
      const scaleY = (rect.height - 96) / unionHeight;
      const targetScale = Math.min(Math.max(Math.min(scaleX, scaleY), 1.0), 3.0);

      const newPanX = rect.width / 2 - centerX * targetScale;
      const newPanY = rect.height / 2 - centerY * targetScale;

      setTransform({
        scale: targetScale,
        panX: newPanX,
        panY: newPanY,
      });
    },
    []
  );

  // Auto-focus when highlightedTokenIds changes
  useEffect(() => {
    if (highlightedTokenIds && highlightedTokenIds.length > 0) {
      const matching = tokens.filter((t) => highlightedTokenIds.includes(t.id));
      if (matching.length === 1) {
        focusToken(matching[0]);
      } else if (matching.length > 1) {
        focusTokensUnion(matching);
      }
    }
  }, [highlightedTokenIds, tokens, focusToken, focusTokensUnion]);

  // Non-passive Wheel Zoom Listener (prevents page scroll without passive listener warning)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const cursorPoint: Point = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      setTransform((prev) => zoomAt(cursorPoint, prev, zoomFactor));
    };

    canvas.addEventListener("wheel", onWheel, { passive: false });
    return () => {
      canvas.removeEventListener("wheel", onWheel);
    };
  }, []);

  // Mouse Down (Pan or Click detection start)
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (e.button !== 0) return; // Left-click only
    isDraggingRef.current = true;
    dragStartRef.current = { x: e.clientX, y: e.clientY };
    dragDistanceRef.current = 0;
    setIsPanning(true);
  };

  // Mouse Move (Pan update & Token Hover detection)
  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const canvasPt: Point = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };

    if (isDraggingRef.current) {
      const dx = e.clientX - dragStartRef.current.x;
      const dy = e.clientY - dragStartRef.current.y;
      dragDistanceRef.current += Math.hypot(dx, dy);
      dragStartRef.current = { x: e.clientX, y: e.clientY };

      setTransform((prev) => ({
        ...prev,
        panX: prev.panX + dx,
        panY: prev.panY + dy,
      }));
      setHoverTooltip(null);
      return;
    }

    // Inverse transform to image space for hit-testing
    const imagePt = canvasToImage(canvasPt, transform);

    // Hit test tokens (checking in reverse to prefer top-rendered tokens)
    let foundToken: OCRTokenModel | null = null;
    for (let i = displayedTokens.length - 1; i >= 0; i--) {
      const t = displayedTokens[i];
      const poly = sanitizePolygon(t.polygon, t.boundingBox);
      if (pointInPolygon(imagePt, poly) || pointInBBox(imagePt, t.boundingBox, 2)) {
        foundToken = t;
        break;
      }
    }

    if (foundToken) {
      setHoveredTokenId(foundToken.id);
      setHoverTooltip({
        x: canvasPt.x,
        y: canvasPt.y,
        token: foundToken,
      });
    } else {
      setHoveredTokenId(null);
      setHoverTooltip(null);
    }
  };

  // Mouse Up / Click Selection
  const handleMouseUp = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDraggingRef.current) return;
    isDraggingRef.current = false;
    setIsPanning(false);

    // If mouse didn't drag significantly (< 5px), treat as selection click
    if (dragDistanceRef.current < 5) {
      const rect = e.currentTarget.getBoundingClientRect();
      const canvasPt: Point = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
      const imagePt = canvasToImage(canvasPt, transform);

      // Handle Caliper reference point placement when active
      if (isCaliperMode) {
        const imgW = imageObjRef.current?.naturalWidth || imageWidth;
        const imgH = imageObjRef.current?.naturalHeight || imageHeight;

        // Validation: reject coordinates outside image bounds
        if (imagePt.x < 0 || imagePt.x > imgW || imagePt.y < 0 || imagePt.y > imgH) {
          return;
        }

        const cleanPt: Point = {
          x: Math.round(imagePt.x * 10) / 10,
          y: Math.round(imagePt.y * 10) / 10,
        };

        if (!caliperPoints.pointA) {
          onCaliperPointsChange?.({
            pointA: cleanPt,
            pointB: null,
            distancePixels: null,
          });
        } else if (!caliperPoints.pointB) {
          // Check distance to Point A (reject if < 2px distance)
          const dist = Math.hypot(
            cleanPt.x - caliperPoints.pointA.x,
            cleanPt.y - caliperPoints.pointA.y
          );
          if (dist >= 2.0) {
            onCaliperPointsChange?.({
              pointA: caliperPoints.pointA,
              pointB: cleanPt,
              distancePixels: Math.round(dist * 10) / 10,
            });
          }
        } else {
          // Both points exist; clicking restarts with new Point A
          onCaliperPointsChange?.({
            pointA: cleanPt,
            pointB: null,
            distancePixels: null,
          });
        }
        return;
      }

      let clickedTokenId: string | null = null;
      for (let i = displayedTokens.length - 1; i >= 0; i--) {
        const t = displayedTokens[i];
        const poly = sanitizePolygon(t.polygon, t.boundingBox);
        if (pointInPolygon(imagePt, poly) || pointInBBox(imagePt, t.boundingBox, 2)) {
          clickedTokenId = t.id;
          break;
        }
      }

      onSelectToken?.(clickedTokenId);
    }
  };

  const handleMouseLeave = () => {
    isDraggingRef.current = false;
    setIsPanning(false);
    setHoveredTokenId(null);
    setHoverTooltip(null);
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Canvas Stadium Container */}
      <Card
        shape="stadium"
        variant="lifted"
        className="relative overflow-hidden p-0 border border-black/[0.08] shadow-halo"
      >
        {/* Floating Header Toolbar */}
        <div className="absolute top-4 left-4 right-4 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
          <div className="pointer-events-auto flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-pill bg-white/95 backdrop-blur-sm text-xs font-semibold text-ink border border-black/[0.08] shadow-sm">
              <span className="w-2 h-2 rounded-full bg-signal-orange" />
              Evidence Canvas
            </span>

            {isSynthetic && (
              <Badge variant="warning" size="sm">
                Synthetic Fixture
              </Badge>
            )}
          </div>

          {/* Canvas Navigation Pill Controls */}
          <div className="pointer-events-auto flex items-center gap-1 bg-white/95 backdrop-blur-sm px-2 py-1 rounded-pill border border-black/[0.08] shadow-sm">
            <Tooltip content="Fit package to viewport">
              <button
                type="button"
                onClick={handleFitToScreen}
                className="p-1.5 rounded-full hover:bg-slate-100 text-slate-700 transition-colors"
                aria-label="Fit image to screen"
              >
                <Maximize2 className="w-3.5 h-3.5" />
              </button>
            </Tooltip>

            <Tooltip content="Zoom in (+)">
              <button
                type="button"
                onClick={handleZoomIn}
                className="p-1.5 rounded-full hover:bg-slate-100 text-slate-700 transition-colors"
                aria-label="Zoom in"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
            </Tooltip>

            <span className="text-[11px] font-mono font-semibold text-slate-600 px-1.5 min-w-[42px] text-center select-none">
              {Math.round(transform.scale * 100)}%
            </span>

            <Tooltip content="Zoom out (-)">
              <button
                type="button"
                onClick={handleZoomOut}
                className="p-1.5 rounded-full hover:bg-slate-100 text-slate-700 transition-colors"
                aria-label="Zoom out"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
            </Tooltip>

            <Tooltip content="Reset viewport (100%)">
              <button
                type="button"
                onClick={handleReset}
                className="p-1.5 rounded-full hover:bg-slate-100 text-slate-700 transition-colors"
                aria-label="Reset viewport"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            </Tooltip>

            {onToggleCaliperMode && (
              <Tooltip content={isCaliperMode ? "Exit Reference Caliper" : "Manual 2-Point Caliper Tool"}>
                <button
                  type="button"
                  onClick={onToggleCaliperMode}
                  className={`p-1.5 rounded-full transition-colors flex items-center gap-1.5 px-2 text-xs font-semibold ${
                    isCaliperMode
                      ? "bg-indigo-600 text-white shadow-xs"
                      : "hover:bg-slate-100 text-slate-700"
                  }`}
                  aria-label="Toggle Caliper Tool"
                  aria-pressed={isCaliperMode}
                >
                  <Crosshair className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Caliper</span>
                </button>
              </Tooltip>
            )}
          </div>
        </div>

        {/* Caliper Reference Points Top Banner */}
        {isCaliperMode && (
          <div className="absolute top-16 left-4 right-4 z-20 flex flex-wrap items-center justify-between gap-3 bg-white/95 backdrop-blur-md px-4 py-2.5 rounded-stadium border border-indigo-200 shadow-md">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-600 animate-pulse" />
              <span className="text-xs font-bold uppercase tracking-eyebrow text-indigo-900">
                Manual Calibration / Reference Points Tool
              </span>
              <span className="text-[11px] text-slate-500 font-mono">
                {!caliperPoints.pointA
                  ? "Click canvas to place Point A"
                  : !caliperPoints.pointB
                  ? "Click canvas to place Point B"
                  : "Two Reference Points Defined"}
              </span>
            </div>

            <div className="flex items-center gap-3 text-xs">
              {caliperPoints.pointA && (
                <span className="font-mono text-[11px] bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200">
                  A: ({caliperPoints.pointA.x}, {caliperPoints.pointA.y})
                </span>
              )}
              {caliperPoints.pointB && (
                <span className="font-mono text-[11px] bg-sky-50 text-sky-800 px-2 py-0.5 rounded border border-sky-200">
                  B: ({caliperPoints.pointB.x}, {caliperPoints.pointB.y})
                </span>
              )}
              {caliperPoints.pointA && caliperPoints.pointB && (
                <span className="font-mono text-[11px] font-bold bg-indigo-50 text-indigo-900 px-2 py-0.5 rounded border border-indigo-200">
                  Distance: {Math.hypot(caliperPoints.pointB.x - caliperPoints.pointA.x, caliperPoints.pointB.y - caliperPoints.pointA.y).toFixed(1)} px (optical)
                </span>
              )}
              {(caliperPoints.pointA || caliperPoints.pointB) && (
                <button
                  type="button"
                  onClick={onClearCaliperPoints}
                  className="text-[11px] text-rose-600 hover:text-rose-800 font-semibold underline underline-offset-2 ml-1"
                >
                  Clear Points
                </button>
              )}
            </div>
          </div>
        )}

        {/* HTML5 Canvas Viewport Container */}
        <div
          ref={containerRef}
          className="relative w-full h-[380px] sm:h-[460px] bg-canvas overflow-hidden select-none"
          style={{ cursor: isCaliperMode ? "crosshair" : isPanning ? "grabbing" : hoveredTokenId ? "pointer" : "grab" }}
        >
          <canvas
            ref={canvasRef}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseLeave}
            className="w-full h-full block touch-none"
            aria-label="Interactive packaging evidence canvas with OCR polygons"
          />

          {/* Image Load Error Overlay */}
          {imageError && (
            <div className="absolute inset-0 flex flex-col items-center justify-center p-6 bg-canvas/90 backdrop-blur-sm text-center">
              <div className="w-12 h-12 rounded-full bg-rose-50 flex items-center justify-center border border-rose-200 mb-3">
                <AlertTriangle className="w-6 h-6 text-rose-600" />
              </div>
              <h4 className="text-sm font-semibold text-ink mb-1">
                Evidence Image Unavailable
              </h4>
              <p className="text-xs text-slate-500 max-w-xs">
                Could not load original packaging raster. Bounding polygons are rendered on the reference grid.
              </p>
            </div>
          )}

          {/* Hover Inspection Tooltip */}
          {hoverTooltip && (
            <div
              className="absolute pointer-events-none z-30 transition-transform duration-75"
              style={{
                left: `${hoverTooltip.x + 12}px`,
                top: `${hoverTooltip.y}px`,
              }}
            >
              <div className="bg-ink text-white px-3 py-2 rounded-xl shadow-deep text-xs space-y-0.5 border border-white/10 whitespace-nowrap">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-signal-orange">
                    [{hoverTooltip.token.id}]
                  </span>
                  <span className="text-[11px] text-slate-300 font-mono">
                    {(hoverTooltip.token.confidence * 100).toFixed(1)}% conf
                  </span>
                </div>
                <div className="font-mono text-slate-200 truncate max-w-[240px]">
                  {hoverTooltip.token.text}
                </div>
                {hoverTooltip.token.fieldName && (
                  <div className="text-[10px] text-amber-300 uppercase tracking-eyebrow font-medium">
                    Rule 6: {hoverTooltip.token.fieldName.replace(/_/g, " ")}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Bottom Canvas Footer Info Strip */}
          <div className="absolute bottom-3 left-4 right-4 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none text-[11px]">
            {/* Visual Legend */}
            <div className="pointer-events-auto flex items-center gap-3 bg-white/95 backdrop-blur-sm px-3 py-1 rounded-pill border border-black/[0.08] shadow-sm text-slate-600">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm border border-signal-orange/60 bg-signal-orange/10" />
                OCR Polygon
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm border-2 border-signal-orange bg-signal-orange/30" />
                Selected
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm border-2 border-blue-600 bg-blue-100" />
                Declaration Linked
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm border border-dashed border-amber-600 bg-amber-50" />
                Low Certainty
              </span>
            </div>

            <span className="pointer-events-auto bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-pill border border-black/[0.08] shadow-sm text-slate-500 font-mono">
              {isCaliperMode ? "Click 2 points on packaging feature" : "Scroll: Zoom • Drag: Pan • Click: Select"}
            </span>
          </div>
        </div>
      </Card>

      {/* Synchronized Accessible Evidence List (DOM Layer for Screen Readers & Keyboard Users) */}
      <Card shape="stadium" variant="lifted" className="p-5 sm:p-6 space-y-3">
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setIsEvidenceListOpen(!isEvidenceListOpen)}
            className="flex items-center gap-2 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal-orange rounded-lg"
            aria-expanded={isEvidenceListOpen}
          >
            <span className="text-xs font-bold uppercase tracking-eyebrow text-ink">
              Evidence Token Repository ({tokens.length} detected)
            </span>
            {isEvidenceListOpen ? (
              <ChevronUp className="w-4 h-4 text-slate-500" />
            ) : (
              <ChevronDown className="w-4 h-4 text-slate-500" />
            )}
          </button>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setShowOnlyReview(!showOnlyReview)}
              className={`text-xs px-2.5 py-1 rounded-pill border transition-all ${
                showOnlyReview
                  ? "bg-amber-100 text-amber-800 border-amber-300 font-semibold"
                  : "bg-white text-slate-600 border-black/[0.08] hover:text-ink"
              }`}
            >
              {showOnlyReview ? "Showing Review Only" : "Show All Tokens"}
            </button>
          </div>
        </div>

        {isEvidenceListOpen && (
          <div
            role="listbox"
            aria-label="Extracted packaging evidence tokens"
            className="space-y-1.5 max-h-64 overflow-y-auto pr-1 pt-1"
          >
            {displayedTokens.length === 0 ? (
              <div className="text-center py-6 text-xs text-slate-500">
                No tokens match the active filter criteria.
              </div>
            ) : (
              displayedTokens.map((t) => {
                const isSelected = t.id === selectedTokenId;
                return (
                  <div
                    key={t.id}
                    role="option"
                    aria-selected={isSelected}
                    tabIndex={0}
                    onClick={() => focusToken(t)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        focusToken(t);
                      }
                    }}
                    className={`flex items-center justify-between p-2.5 rounded-xl border transition-all cursor-pointer text-xs ${
                      isSelected
                        ? "bg-signal-orange/10 border-signal-orange shadow-sm text-ink"
                        : "bg-white border-black/[0.06] hover:border-black/20 text-slate-700"
                    }`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <span
                        className={`w-2 h-2 rounded-full flex-shrink-0 ${
                          isSelected
                            ? "bg-signal-orange"
                            : t.requiresReview
                            ? "bg-amber-500"
                            : "bg-emerald-500"
                        }`}
                      />
                      <div className="space-y-0.5 min-w-0">
                        <div className="font-semibold text-ink font-mono truncate">
                          {t.text}
                        </div>
                        <div className="text-[10px] text-slate-500 flex items-center gap-2">
                          <span>ID: {t.id}</span>
                          <span>•</span>
                          <span>Script: {t.script || "latin"}</span>
                          {t.fieldName && (
                            <>
                              <span>•</span>
                              <span className="text-signal-orange font-medium">
                                {t.fieldName.replace(/_/g, " ")}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className="font-mono text-[11px] font-semibold text-slate-600 bg-canvas px-2 py-0.5 rounded-md border border-black/[0.04]">
                        {(t.confidence * 100).toFixed(1)}%
                      </span>
                      {isSelected && (
                        <Check className="w-4 h-4 text-signal-orange" />
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}
      </Card>
    </div>
  );
}
