"""
Typed error hierarchy for Nirikshak OCR subsystem.
"""

from typing import Optional


class OCRError(Exception):
    """Base exception for all OCR subsystem errors."""
    def __init__(self, message: str, error_code: str = "OCR_ERROR"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class ConfigurationError(OCRError):
    """Raised when OCR configuration is invalid or missing required parameters."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_CONFIGURATION_ERROR")


class ModelLoadError(OCRError):
    """Raised when ONNX model files or character dictionaries cannot be loaded."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_MODEL_LOAD_ERROR")


class InvalidImageError(OCRError):
    """Raised when input image is None, empty, zero-sized, or has invalid data types."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_INVALID_IMAGE_ERROR")


class UnsupportedImageError(OCRError):
    """Raised when input image format, channels, or dimensions are not supported."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_UNSUPPORTED_IMAGE_ERROR")


class InferenceError(OCRError):
    """Raised when ONNX Runtime inference session fails during execution."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_INFERENCE_ERROR")


class GeometryError(OCRError):
    """Raised when polygon coordinates are degenerate, non-finite, or malformed."""
    def __init__(self, message: str):
        super().__init__(message, error_code="OCR_GEOMETRY_ERROR")


class OCRServiceError(OCRError):
    """Raised when high-level OCR service adapter encounters a processing failure."""
    def __init__(self, message: str, error_code: str = "OCR_SERVICE_ERROR", cause: Optional[Exception] = None):
        super().__init__(message, error_code=error_code)
        self.cause = cause
