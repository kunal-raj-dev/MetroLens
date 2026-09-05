# Chunk 4 — Monorepo Integration & Service Implementation Record
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/04_IMPLEMENTATION/INTEGRATION_RECORD.md`  
**Author:** Member 1 (AI & Multilingual OCR Lead)  
**Date:** 2026-09-05T05:32:00+05:30  
**Phase:** Member 1 — Chunk 4  
**Status:** IMPLEMENTATION VERIFIED  

---

## 1. Executive Summary

Chunk 4 integrates the established direct ONNX Runtime OCR subsystem (`packages/ocr`) into the broader MetroLens monorepo architecture. The subsystem is now packaged as a standard Python package (`nirikshak-ocr`), importable across all monorepo domains without `sys.path` hacks, equipped with a production-grade service adapter (`OCRService`), aligned with shared Pydantic data contracts (`nirikshak_shared.schemas`), hardened against multi-threaded concurrency, and proven offline-ready.

---

## 2. Monorepo Package Integration

### 2.1 Pip Editable Installation
To eliminate manual `sys.path` modifications across tests, CLI utilities, and application entrypoints, both `packages/shared` and `packages/ocr` were registered into the active Python 3.14 virtual environment via editable installs:
```bash
pip install -e packages/shared -e packages/ocr --no-deps
```
This enables seamless, deterministic imports across all subsystems:
```python
from nirikshak_shared.schemas import OCRObservation, InspectionRequest
from nirikshak_ocr import OCRService, OCREngine, OCRConfig, OCRServiceError
```

### 2.2 Filesystem & CWD Independence (`packages/ocr/src/nirikshak_ocr/config.py`)
In earlier development iterations, relative model paths depended on the process current working directory (`os.getcwd()`), causing failures when tests or scripts were executed from subdirectories like `apps/api/` or `tests/integration/`.

`OCRConfig` was hardened with robust, layered root directory discovery:
1. `METROLENS_ROOT` environment variable (highest priority if set).
2. Upward directory traversal searching for marker files/directories (`packages`, `models/manifest.yaml`, `pyproject.toml`).
3. Fallback to package relative layout (`Path(__file__).resolve().parents[4]`).
4. Support for `METROLENS_MODELS_DIR` environment variable to relocate model weights independently.
5. Strict default configuration enforcement:
   ```python
   preprocessing_mode: str = "raw"       # B0 Baseline Raw is canonical default
   preprocess_target: str = "crop"       # Crop-level processing
   ```

---

## 3. Structured Errors & HTTP Mapping (`packages/ocr/src/nirikshak_ocr/errors.py`)

Added `error_code` attributes across the entire OCR exception hierarchy and introduced `OCRServiceError` for clean boundary translation into web API responses:
```python
class OCRError(Exception):
    error_code: str = "OCR_GENERIC_ERROR"

class ModelNotFoundError(OCRError):
    error_code: str = "MODEL_NOT_FOUND"

class ModelCorruptedError(OCRError):
    error_code: str = "MODEL_CORRUPTED"

class ImageDecodeError(OCRError):
    error_code: str = "INVALID_IMAGE"

class InvalidInputError(OCRError):
    error_code: str = "INVALID_IMAGE"

class InferenceError(OCRError):
    error_code: str = "ENGINE_ERROR"

class OCRServiceError(OCRError):
    """Raised by OCRService when handling upstream request errors."""
    def __init__(self, message: str, error_code: str = "ENGINE_ERROR", status_code: int = 500):
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code
```

---

## 4. Production Service Adapter (`packages/ocr/src/nirikshak_ocr/service.py`)

Implemented `OCRService` to provide an enterprise-grade facade over the underlying engine:

### 4.1 Thread-Safe Singleton Pattern
```python
class OCRService:
    _instance: Optional["OCRService"] = None
    _singleton_lock: threading.Lock = threading.Lock()

    @classmethod
    def get_instance(cls, config: Optional[OCRConfig] = None) -> "OCRService":
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = cls(config=config)
        return cls._instance
```

### 4.2 Polymorphic Input Normalization (`convert_image_input`)
- Accepts `bytes`, `bytearray`, file paths (`str`, `Path`), and in-memory `np.ndarray`.
- Detects non-image payloads, corrupt headers, and zero-dimension frames, raising `OCRServiceError("...", error_code="INVALID_IMAGE", status_code=400)`.
- Enforces caller array immutability via defensive copy (`image.copy()`).

### 4.3 Observation Marshalling (`extract_observations`)
Transforms raw token detections into canonical `OCRObservation` instances:
```python
obs = OCRObservation(
    text=token.text,
    confidence=float(token.confidence),
    bounding_box=[[float(pt[0]), float(pt[1])] for pt in token.polygon],
)
```
- Preserves verbatim 4-point clockwise quadrilateral polygon coordinates in original image pixel space.
- Guarantees compatibility with Member 2 (optical measurement/font calibration) and Member 3 (statutory normalization).

### 4.4 Engine Execution Lock
Inference execution is protected by an explicit thread serialization lock (`self._engine_lock`):
```python
with self._engine_lock:
    result = self.engine.predict(image)
```
This guarantees race-condition-free operation across multi-threaded web application servers (e.g. Uvicorn with multiple worker threads).

---

## 5. Architectural Boundary Preservation

In strict compliance with Member 1 ownership rules:
1. **No API Server Rewrites:** Member 1 did NOT modify `apps/api/main.py`, create FastAPI routes, or implement HTTP middleware. All API orchestration belongs exclusively to Member 4.
2. **No Asynchronous Queues:** Excluded Celery, Redis, and RabbitMQ. All execution is 100% synchronous and in-process.
3. **No Domain Leakage:**
   - Zero legal metrology rules (Rules 6, 7, 8, 9, 11, 26) implemented in OCR.
   - Zero mm physical calibration logic implemented in OCR.
   - Zero semantic statutory parsing implemented in OCR.
