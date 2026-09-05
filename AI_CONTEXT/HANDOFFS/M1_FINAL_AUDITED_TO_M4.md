# M1 FINAL AUDITED HANDOFF TO MEMBER 4 (API & SYSTEM ARCHITECTURE)

**From**: Member 1 (AI & Multilingual OCR Lead)  
**To**: Member 4 (Backend API, Microservices & Pipeline Architecture Lead)  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Primary Service Interface: `OCRService`
Member 4 integrates with Member 1 exclusively via `nirikshak_ocr.OCRService`:
```python
from nirikshak_ocr import OCRService

# Application lifespan initialization (e.g. FastAPI startup)
service = OCRService.get_instance()

# Warmup to prime ONNX Runtime CPU execution provider
warmup_latency_ms = service.warmup()

# Synchronous extraction (accepts file path, raw bytes, bytearray, or np.ndarray)
result = service.extract(file_bytes, image_id="request_123")

# Convenience dictionaries for HTTP responses
response_dict = service.extract_dict(file_bytes, image_id="request_123")
```

## 2. Lifecycle & Session Reuse
- **Singleton Accessor**: `OCRService.get_instance()` reuses existing ONNX sessions across all requests without reloading model weights.
- **Cold Load Latency**: ~350 ms.
- **Warmup Latency**: ~15 ms.
- **Session Isolation**: Unit tests can call `OCRService.reset_instance()` for isolated lifecycle testing.

## 3. Input Polymorphism & Caller Memory Safety
`OCRService.convert_image_input()` supports:
- Raw binary bytes / bytearray (e.g. `UploadFile.read()`)
- Filesystem path (`str` or `pathlib.Path`)
- Pre-loaded Numpy `ndarray` (BGR, BGRA, or Grayscale)
- **Memory Safety**: Makes a defensive copy of numpy arrays; caller source memory is **never** mutated in-place.
- **Decompression Bomb Guard**: Immediately rejects images exceeding 64 MP with `UnsupportedImageError` in < 0.1 ms.

## 4. Typed Error Hierarchy & Exception Translation
All exceptions inherit from `nirikshak_ocr.errors.OCRError`:
- `InvalidImageError`: None, empty array, or image < 8x8 px (translate to HTTP 400).
- `UnsupportedImageError`: Unsupported format, corrupted bytes, or >64 MP (translate to HTTP 400).
- `ModelLoadError`: Missing weights or corrupt ONNX graph (translate to HTTP 500).
- `InferenceError`: ONNX Runtime execution failure (translate to HTTP 500).
- `OCRServiceError`: High-level unexpected service failure (translate to HTTP 500).
- **CRITICAL**: Empty frames (no text detected) return `status="SUCCESS"` with `tokens=[]`. Do NOT treat 0 tokens as an HTTP 500 error.

## 5. Concurrency & Multi-Threading Architecture
- **Inference Locking**: Inference is serialized via `OCRService._engine_lock` to ensure thread safety across concurrent FastAPI workers.
- **Scalability**: For multi-core production scaling, configure multiple worker processes (e.g. `uvicorn main:app --workers 4`), where each process maintains an independent singleton session.

## 6. Offline & Edge Compliance
- 100% local weights; zero outbound socket calls.
- Suitable for local edge deployments, air-gapped forensic inspection stations, and Docker containers without internet access.
