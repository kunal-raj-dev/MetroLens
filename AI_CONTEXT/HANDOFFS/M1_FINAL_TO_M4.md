# Inter-Member Final Handoff: Member 1 (OCR) -> Member 4 (Backend & Infrastructure)

**From**: Member 1 — AI & Multilingual OCR Lead  
**To**: Member 4 — Backend, Infrastructure & API Lead  
**Date**: September 2026  
**Status**: **FROZEN & PRODUCTION READY**

---

## 1. Executive Summary & Integration Blueprint

Member 1 provides a clean, headless Python service `nirikshak_ocr.service.OCRService` ready for direct integration into Member 4's FastAPI application and inspection pipelines.

### FastAPI Integration Blueprint:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from nirikshak_ocr import OCRService
from nirikshak_ocr.service import UnsupportedImageError, CorruptedImageError, InvalidInputError

# Singleton Service Instance
_ocr_service: OCRService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _ocr_service
    # 1. Initialize and warmup on server startup
    _ocr_service = OCRService()
    _ocr_service.warmup()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/v1/ocr/extract")
async def extract_ocr(file: UploadFile = File(...)):
    raw_bytes = await file.read()
    try:
        # 2. Extract dict representation for immediate JSON response
        result = _ocr_service.extract_dict(raw_bytes, image_id=file.filename)
        return result
    except UnsupportedImageError as e:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(e))
    except CorruptedImageError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
```

---

## 2. Concurrency, Performance & Sizing Guidelines

1. **Thread-Safety**: `OCRService` uses an internal threading lock around ONNX sessions. Multiple async FastAPI worker threads can call `extract_dict()` or `extract_observations()` concurrently without race conditions.
2. **Warmup**: Always execute `service.warmup()` during FastAPI startup lifespan to eliminate cold-start jitters on the first user request.
3. **Memory Sizing**:
   - Model resident footprint: ~150 MB.
   - Recommended minimum container RAM: 2 GB (4 GB recommended for concurrent pipeline tasks).
4. **Offline Isolation**: Completely edge-native; no internet connection or external API keys needed.

---

## 3. Strict Boundary Rules for Member 4

1. **Member 4 Owns**:
   - HTTP transport, routers, authentication, request validation, rate limiting, and database persistence.
   - Orchestration pipeline integrating Member 1 (OCR), Member 2 (Rules), and Member 3 (Vision).
2. **Member 4 Must NOT**:
   - Bypass `OCRService` to access internal ONNX sessions directly.
   - Modify or rebuild any code in `packages/ocr/` (permanently frozen per `MEMBER_1_DO_NOT_REBUILD.md`).
