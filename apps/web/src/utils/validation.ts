/**
 * MetroLens AI™ - Image Ingestion Validation Utilities
 * Subsystem: Member 5 (Web Frontend)
 * 
 * Enforces defensive client-side checks before network transmission:
 * - 15 MiB ceiling check (matching backend boundary)
 * - MIME type & file extension verification (JPEG, PNG, WebP)
 * - Client-side magic byte signature sniffing
 * - Browser raster decoding verification & dimension extraction
 * 
 * Invariant: Backend remains the authoritative security and validation boundary.
 */

export const MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024; // 15 MiB (15,728,640 bytes)

export const ALLOWED_MIME_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
] as const;

export type AllowedMimeType = (typeof ALLOWED_MIME_TYPES)[number];

export const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"] as const;

export type FileValidationErrorType =
  | "FILE_TOO_LARGE"
  | "UNSUPPORTED_TYPE"
  | "INVALID_SIGNATURE"
  | "IMAGE_DECODE_FAILED"
  | "FILE_EMPTY";

export interface FileValidationResult {
  valid: boolean;
  error?: {
    type: FileValidationErrorType;
    message: string;
    details?: string;
  };
  dimensions?: {
    width: number;
    height: number;
  };
  detectedFormat?: string;
}

/**
 * Formats byte size into human-readable representation (e.g. 3.4 MB, 450 KB)
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  const val = parseFloat((bytes / Math.pow(k, i)).toFixed(2));
  return `${val} ${sizes[i]}`;
}

/**
 * Sniffs the magic byte header of a file to detect genuine image format.
 * Returns the detected MIME type or null if unrecognized.
 */
export async function detectMagicBytes(file: File): Promise<string | null> {
  if (file.size < 12) return null;

  const headerSlice = file.slice(0, 12);
  const buffer = await headerSlice.arrayBuffer();
  const bytes = new Uint8Array(buffer);

  // JPEG: FF D8 FF
  if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) {
    return "image/jpeg";
  }

  // PNG: 89 50 4E 47 0D 0A 1A 0A
  if (
    bytes[0] === 0x89 &&
    bytes[1] === 0x50 &&
    bytes[2] === 0x4e &&
    bytes[3] === 0x47 &&
    bytes[4] === 0x0d &&
    bytes[5] === 0x0a &&
    bytes[6] === 0x1a &&
    bytes[7] === 0x0a
  ) {
    return "image/png";
  }

  // WebP: RIFF (bytes 0..3) ... WEBP (bytes 8..11)
  // 'R' 'I' 'F' 'F' -> 0x52, 0x49, 0x46, 0x46
  // 'W' 'E' 'B' 'P' -> 0x57, 0x45, 0x42, 0x50
  if (
    bytes[0] === 0x52 &&
    bytes[1] === 0x49 &&
    bytes[2] === 0x46 &&
    bytes[3] === 0x46 &&
    bytes[8] === 0x57 &&
    bytes[9] === 0x45 &&
    bytes[10] === 0x42 &&
    bytes[11] === 0x50
  ) {
    return "image/webp";
  }

  return null;
}

/**
 * Validates raster image decode capability in the browser.
 * Extracts natural pixel dimensions and verifies the image stream is intact.
 */
export function validateImageDecode(
  file: File
): Promise<{ width: number; height: number }> {
  return new Promise((resolve, reject) => {
    // Only attempt in browser environment
    if (typeof window === "undefined" || typeof Image === "undefined") {
      resolve({ width: 0, height: 0 });
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    const img = new Image();

    img.onload = () => {
      URL.revokeObjectURL(objectUrl);
      if (img.naturalWidth > 0 && img.naturalHeight > 0) {
        resolve({
          width: img.naturalWidth,
          height: img.naturalHeight,
        });
      } else {
        reject(
          new Error("Image decoded with zero dimensions or corrupt canvas frame")
        );
      }
    };

    img.onerror = () => {
      URL.revokeObjectURL(objectUrl);
      reject(new Error("Browser failed to decode image raster stream"));
    };

    img.src = objectUrl;
  });
}

/**
 * Comprehensive client-side image validation.
 * Performs size, MIME, magic-byte, and raster decode tests.
 */
export async function validateInspectionImage(
  file: File
): Promise<FileValidationResult> {
  // 1. Check empty file
  if (!file || file.size === 0) {
    return {
      valid: false,
      error: {
        type: "FILE_EMPTY",
        message: "The selected file is empty (0 bytes).",
        details: "Please provide a valid package photograph.",
      },
    };
  }

  // 2. Size boundary check (15 MiB)
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return {
      valid: false,
      error: {
        type: "FILE_TOO_LARGE",
        message: `File exceeds the maximum allowable size of ${formatFileSize(
          MAX_FILE_SIZE_BYTES
        )}.`,
        details: `Your file is ${formatFileSize(
          file.size
        )}. Please reduce the image resolution before submitting.`,
      },
    };
  }

  // 3. MIME and Extension check
  const lowerName = file.name.toLowerCase();
  const hasValidExtension = ALLOWED_EXTENSIONS.some((ext) =>
    lowerName.endsWith(ext)
  );

  const isValidMime = ALLOWED_MIME_TYPES.includes(file.type as AllowedMimeType);

  if (!isValidMime && !hasValidExtension) {
    return {
      valid: false,
      error: {
        type: "UNSUPPORTED_TYPE",
        message: "Unsupported file format. Only JPEG, PNG, and WebP are accepted.",
        details: `Detected type: ${file.type || "unknown"}, filename: ${file.name}. Documents (PDF) and vector graphics (SVG) are prohibited under Rule 6 inspection procedures.`,
      },
    };
  }

  // 4. Magic bytes sniffing
  try {
    const magicMime = await detectMagicBytes(file);
    if (!magicMime) {
      return {
        valid: false,
        error: {
          type: "INVALID_SIGNATURE",
          message: "File signature header is corrupt or unrecognized.",
          details:
            "The file claims to be an image but does not begin with standard JPEG, PNG, or WebP binary magic bytes.",
        },
      };
    }
  } catch (err: any) {
    // If ArrayBuffer fails, treat as corrupted file
    return {
      valid: false,
      error: {
        type: "INVALID_SIGNATURE",
        message: "Unable to read binary header of the selected file.",
        details: err?.message,
      },
    };
  }

  // 5. Browser raster decode verification
  try {
    const dims = await validateImageDecode(file);
    return {
      valid: true,
      dimensions: dims,
      detectedFormat: file.type || "image/jpeg",
    };
  } catch (err: any) {
    return {
      valid: false,
      error: {
        type: "IMAGE_DECODE_FAILED",
        message: "Corrupted image file: browser cannot decode raster stream.",
        details: err?.message,
      },
    };
  }
}
