"""
Nirikshak API: Standardized Error Models, Exception Hierarchy & Exception Handlers.
Conforms strictly to docs/API_CONTRACT.md Section 4 error contract and taxonomy.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ConfigDict


class APIErrorBody(BaseModel):
    """Inner error payload strictly conforming to docs/API_CONTRACT.md Section 4."""
    code: str = Field(..., description="Standard machine-readable error code")
    message: str = Field(..., description="Human-readable explanation of error condition")
    details: Dict[str, Any] = Field(default_factory=dict, description="Diagnostic contextual metadata")
    remediation: str = Field(..., description="Actionable instruction guiding user remediation")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of occurrence",
    )

    model_config = ConfigDict(extra="ignore")


class APIErrorEnvelope(BaseModel):
    """Top-level error response envelope wrapping APIErrorBody."""
    error: APIErrorBody


class MetroLensAPIException(Exception):
    """Base exception for all domain and security errors in MetroLens API."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        remediation: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.remediation = remediation
        self.details = details or {}
        self.headers = headers
        super().__init__(self.message)

    def to_envelope(self) -> APIErrorEnvelope:
        return APIErrorEnvelope(
            error=APIErrorBody(
                code=self.code,
                message=self.message,
                details=self.details,
                remediation=self.remediation,
            )
        )


class InvalidImagePayloadError(MetroLensAPIException):
    """HTTP 400: Missing file stream or corrupted multipart form data."""
    def __init__(self, message: str = "The uploaded form data contains an invalid or missing image stream.", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_IMAGE_PAYLOAD",
            message=message,
            remediation="Select a valid image file and submit the multipart form again.",
            details=details,
        )


class ImageTooLargeError(MetroLensAPIException):
    """HTTP 413: Upload exceeds the 15.0 MB file size limit."""
    def __init__(self, file_size_bytes: int, max_allowed_bytes: int = 15 * 1024 * 1024):
        super().__init__(
            status_code=getattr(status, "HTTP_413_CONTENT_TOO_LARGE", 413),
            code="IMAGE_TOO_LARGE",
            message=f"The uploaded packaging image ({file_size_bytes:,} bytes) exceeds the 15.0 MB file size limit.",
            remediation="Please resize or compress your image under 15.0 MB and try again.",
            details={"file_size_bytes": file_size_bytes, "max_allowed_bytes": max_allowed_bytes},
        )


class UnsupportedMediaTypeError(MetroLensAPIException):
    """HTTP 415: Magic bytes do not match JPEG, PNG, or WebP."""
    def __init__(self, detected_mime: Optional[str] = None, detected_magic: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            code="UNSUPPORTED_MEDIA_TYPE",
            message="The uploaded file header does not match valid JPEG, PNG, or WebP magic bytes.",
            remediation="Upload a genuine, uncorrupted JPEG, PNG, or WebP packaging photograph.",
            details={"detected_mime": detected_mime or "unknown", "detected_magic": detected_magic or "unknown"},
        )


class DecompressionBombError(MetroLensAPIException):
    """HTTP 422: Image dimensions exceed 64 Megapixels (MAX_IMAGE_PIXELS)."""
    def __init__(self, width: int, height: int, total_pixels: int, max_pixels: int = 64_000_000):
        super().__init__(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            code="DECOMPRESSION_BOMB_DETECTED",
            message=f"Image dimension ({width}x{height} = {total_pixels:,} pixels) exceeds the 64 Megapixel safety cap.",
            remediation="Upload a standard smartphone or camera resolution photograph (under 64 Megapixels).",
            details={"width": width, "height": height, "total_pixels": total_pixels, "max_pixels": max_pixels},
        )


class ImageCorruptedError(MetroLensAPIException):
    """HTTP 422: Image decoder fails to parse raster pixel streams."""
    def __init__(self, reason: str = "Image stream truncated or corrupted"):
        super().__init__(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            code="IMAGE_CORRUPTED",
            message=f"The image decoder failed to parse the pixel data: {reason}.",
            remediation="Re-take photograph or re-export the image from your graphics application.",
            details={"reason": reason},
        )


class ImageResolutionTooLowError(MetroLensAPIException):
    """HTTP 422: Image resolution is below 800 x 600 pixels."""
    def __init__(self, width: int, height: int, min_width: int = 800, min_height: int = 600):
        super().__init__(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            code="IMAGE_RESOLUTION_TOO_LOW",
            message=f"Image resolution ({width}x{height} pixels) is below the minimum required {min_width}x{min_height} threshold.",
            remediation="Capture the packaging at higher resolution to allow automated legal metrology text verification.",
            details={"width": width, "height": height, "min_width": min_width, "min_height": min_height},
        )


class RateLimitExceededError(MetroLensAPIException):
    """HTTP 429: Client IP exceeded inspection rate limit."""
    def __init__(self, retry_after_seconds: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMIT_EXCEEDED",
            message="Client request rate exceeded the statutory threshold of 10 inspection requests per minute.",
            remediation=f"Please wait {retry_after_seconds} seconds before submitting subsequent inspection requests.",
            details={"retry_after_seconds": retry_after_seconds},
            headers={"Retry-After": str(retry_after_seconds)},
        )


class PipelineExecutionError(MetroLensAPIException):
    """HTTP 500: Internal runtime exception during processing."""
    def __init__(self, stage: str, details_msg: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="PIPELINE_EXECUTION_ERROR",
            message=f"An unexpected error occurred during pipeline stage '{stage}': {details_msg}",
            remediation="Please retry your request. If the issue persists, contact technical support with the timestamp.",
            details={"stage": stage, "details": details_msg},
        )


class ProcessingTimeoutError(MetroLensAPIException):
    """HTTP 504: Pipeline execution exceeded watchdog timeout."""
    def __init__(self, elapsed_seconds: float, timeout_limit_seconds: float = 5.0):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            code="PROCESSING_TIMEOUT",
            message=f"Processing exceeded the statutory watchdog limit of {timeout_limit_seconds}s (elapsed: {elapsed_seconds:.2f}s).",
            remediation="Upload a sharper, single-panel crop to reduce CPU inference load.",
            details={"elapsed_seconds": elapsed_seconds, "timeout_limit_seconds": timeout_limit_seconds},
        )


async def metrolens_exception_handler(request: Request, exc: MetroLensAPIException) -> JSONResponse:
    """FastAPI handler for domain-specific MetroLensAPIException instances."""
    envelope = exc.to_envelope()
    return JSONResponse(
        status_code=exc.status_code,
        content=envelope.model_dump(),
        headers=exc.headers or {},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """FastAPI handler converting FastAPI/Pydantic validation errors into standard error envelope."""
    error_details = [{"loc": list(err.get("loc", [])), "msg": err.get("msg", ""), "type": err.get("type", "")} for err in exc.errors()]
    envelope = APIErrorEnvelope(
        error=APIErrorBody(
            code="INVALID_IMAGE_PAYLOAD",
            message="Input validation failed for the requested endpoint parameters.",
            details={"validation_errors": error_details},
            remediation="Verify that all required form parameters are provided with expected types.",
        )
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=envelope.model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global catch-all exception handler returning standard HTTP 500 error envelope."""
    envelope = APIErrorEnvelope(
        error=APIErrorBody(
            code="PIPELINE_EXECUTION_ERROR",
            message=f"An unhandled internal server error occurred: {str(exc)}",
            details={"exception_type": type(exc).__name__},
            remediation="Please retry your request or contact the administrator.",
        )
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=envelope.model_dump(),
    )


def register_error_handlers(app: FastAPI) -> None:
    """Registers domain and validation exception handlers onto FastAPI application."""
    app.add_exception_handler(MetroLensAPIException, metrolens_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

