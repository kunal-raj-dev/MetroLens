/**
 * MetroLens AI™ - Evidence Canvas Coordinate Transform & Hit-Testing Utilities
 * Subsystem: Member 5 (Web Frontend)
 * 
 * INVARIANT:
 * Member 1 OCR coordinates are FROZEN in original input image pixel space.
 * This module provides pure, reversible affine coordinate transformations:
 * 
 * Forward:
 *   [x_c, y_c] = scale * [x_i, y_i] + [panX, panY]
 * 
 * Inverse:
 *   [x_i, y_i] = ([x_c, y_c] - [panX, panY]) / scale
 */

import { BoundingBoxModel } from "@/types/frontend";

export interface Point {
  x: number;
  y: number;
}

export interface CanvasTransform {
  scale: number;
  panX: number;
  panY: number;
}

/**
 * Transforms a point from original image pixel space to canvas rendering space.
 */
export function imageToCanvas(
  point: Point,
  transform: CanvasTransform
): Point {
  return {
    x: point.x * transform.scale + transform.panX,
    y: point.y * transform.scale + transform.panY,
  };
}

/**
 * Inversely transforms a point from canvas rendering space to original image pixel space.
 */
export function canvasToImage(
  point: Point,
  transform: CanvasTransform
): Point {
  if (transform.scale === 0) {
    return { x: 0, y: 0 };
  }
  return {
    x: (point.x - transform.panX) / transform.scale,
    y: (point.y - transform.panY) / transform.scale,
  };
}

/**
 * Computes an optimal fit-to-screen transform that centers the image
 * within the container while preserving aspect ratio.
 */
export function fitToScreen(
  imageWidth: number,
  imageHeight: number,
  containerWidth: number,
  containerHeight: number,
  padding: number = 24
): CanvasTransform {
  if (imageWidth <= 0 || imageHeight <= 0 || containerWidth <= 0 || containerHeight <= 0) {
    return { scale: 1, panX: 0, panY: 0 };
  }

  const availWidth = Math.max(containerWidth - padding * 2, 10);
  const availHeight = Math.max(containerHeight - padding * 2, 10);

  const scaleX = availWidth / imageWidth;
  const scaleY = availHeight / imageHeight;
  const scale = Math.min(scaleX, scaleY);

  const renderedWidth = imageWidth * scale;
  const renderedHeight = imageHeight * scale;

  const panX = (containerWidth - renderedWidth) / 2;
  const panY = (containerHeight - renderedHeight) / 2;

  return { scale, panX, panY };
}

/**
 * Zooms the canvas anchored at a specific canvas focal point (e.g. cursor position),
 * preventing the image from jumping away during mouse-wheel or pinch zoom.
 */
export function zoomAt(
  anchorPoint: Point,
  currentTransform: CanvasTransform,
  zoomFactor: number,
  minScale: number = 0.15,
  maxScale: number = 10.0
): CanvasTransform {
  const currentScale = currentTransform.scale;
  const targetScale = currentScale * zoomFactor;
  const clampedScale = Math.min(Math.max(targetScale, minScale), maxScale);

  if (clampedScale === currentScale) {
    return currentTransform;
  }

  // Anchor in image coordinates before zoom
  const imagePoint = canvasToImage(anchorPoint, currentTransform);

  // New pan coordinates anchoring imagePoint at anchorPoint
  const newPanX = anchorPoint.x - imagePoint.x * clampedScale;
  const newPanY = anchorPoint.y - imagePoint.y * clampedScale;

  return {
    scale: clampedScale,
    panX: newPanX,
    panY: newPanY,
  };
}

/**
 * Hit tests whether an image-space point lies inside an arbitrary polygon
 * using the standard ray-casting algorithm (Jordan curve theorem).
 */
export function pointInPolygon(
  point: Point,
  polygon: [number, number][]
): boolean {
  if (!polygon || polygon.length < 3) return false;

  let inside = false;
  const x = point.x;
  const y = point.y;
  const n = polygon.length;

  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = polygon[i][0];
    const yi = polygon[i][1];
    const xj = polygon[j][0];
    const yj = polygon[j][1];

    const intersect =
      yi > y !== yj > y &&
      x < ((xj - xi) * (y - yi)) / (yj - yi + Number.EPSILON) + xi;

    if (intersect) {
      inside = !inside;
    }
  }

  return inside;
}

/**
 * Hit tests whether an image-space point lies within an axis-aligned bounding box.
 */
export function pointInBBox(
  point: Point,
  bbox: BoundingBoxModel,
  tolerance: number = 0
): boolean {
  return (
    point.x >= bbox.xMin - tolerance &&
    point.x <= bbox.xMax + tolerance &&
    point.y >= bbox.yMin - tolerance &&
    point.y <= bbox.yMax + tolerance
  );
}

/**
 * Defensively validates and sanitizes polygon points.
 * If points are missing, NaN, or incorrect in count, safely falls back to bounding box.
 */
export function sanitizePolygon(
  polygon: any,
  fallbackBBox?: BoundingBoxModel | null
): [number, number][] {
  if (
    Array.isArray(polygon) &&
    polygon.length === 4 &&
    polygon.every(
      (pt) =>
        Array.isArray(pt) &&
        pt.length === 2 &&
        Number.isFinite(pt[0]) &&
        Number.isFinite(pt[1])
    )
  ) {
    return polygon as [number, number][];
  }

  if (fallbackBBox) {
    const { xMin, yMin, xMax, yMax } = fallbackBBox;
    return [
      [xMin, yMin],
      [xMax, yMin],
      [xMax, yMax],
      [xMin, yMax],
    ];
  }

  return [
    [0, 0],
    [10, 0],
    [10, 10],
    [0, 10],
  ];
}
