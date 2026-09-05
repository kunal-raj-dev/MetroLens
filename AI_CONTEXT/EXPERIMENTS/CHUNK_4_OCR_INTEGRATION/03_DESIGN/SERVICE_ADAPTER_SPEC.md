# Chunk 4 — OCR Service Adapter Specification
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_4_OCR_INTEGRATION/03_DESIGN/SERVICE_ADAPTER_SPEC.md`  
**Author:** Member 1 (AI & Multilingual OCR Lead)  
**Date:** 2026-09-05T05:30:00+05:30  
**Phase:** Member 1 — Chunk 4  
**Status:** CANONICAL SPECIFICATION — IMPLEMENTED & VERIFIED  

---

## 1. Architectural Purpose & Decoupling

The `OCRService` acts as an architectural boundary between the raw, low-level ONNX Runtime inference engine (`OCREngine` in `nirikshak_ocr.engine`) and upstream consumption layers (Member 4 FastAPI application routes, inspection pipelines, and background test harnesses).

### Core Responsibilities
1. **Model Lifecycle Management:** Thread-safe singleton creation, engine initialization, session caching, and pre-flight warmup without requiring web request workers to manage model files.
2. **Polymorphic Input Normalization:** Transparently accepts raw binary image bytes (`bytes`, `bytearray`), filesystem paths (`str`, `Path`), and in-memory OpenCV images (`np.ndarray` with defensive copy to guarantee caller array immutability).
3. **Contract Marshalling:** Bridges internal `OCRResult` objects into the canonical `OCRObservation` Pydantic models defined in `nirikshak_shared.schemas`, as well as JSON-serializable API dictionaries.
4. **Concurrency Serialization:** Uses an explicit process-level re-entrant lock (`threading.Lock`) to serialize ONNX Runtime inference execution across concurrent FastAPI worker threads, preventing race conditions.
5. **Typed Error Translation:** Traps internal engine exceptions and translates them into structured `OCRServiceError` exceptions with machine-readable error codes (`INVALID_IMAGE`, `MODEL_NOT_FOUND`, `ENGINE_ERROR`, `INFERENCE_TIMEOUT`).
6. **Zero Asynchronous Infrastructure:** Enforces strictly synchronous CPU execution. Excludes Celery, Redis, and message queues in accordance with the Web MVP specification.

---

## 2. Service Architecture & Class Hierarchy

```text
+-----------------------------------------------------------------------+
|                            MEMBER 4 API                               |
|        (FastAPI Dependency Injection / Synchronous Route Handler)     |
+-----------------------------------------------------------------------+
                                   |
                                   | calls get_instance()
                                   v
+-----------------------------------------------------------------------+
|                      nirikshak_ocr.OCRService                         |
|  - _instance: Optional[OCRService]                                    |
|  - _engine_lock: threading.Lock                                       |
|  - engine: OCREngine                                                  |
|  -------------------------------------------------------------------  |
|  + get_instance(config) -> OCRService                                 |
|  + reset_instance() -> None                                           |
|  + warmup() -> Dict[str, Any]                                         |
|  + extract(image_input) -> OCRResult                                  |
|  + extract_observations(image_input) -> List[OCRObservation]          |
|  + extract_dict(image_input) -> Dict[str, Any]                        |
+-----------------------------------------------------------------------+
            |                                         |
            | validates & converts                    | serializes & normalizes
            v                                         v
+------------------------------------+   +------------------------------+
|       convert_image_input()        |   |   Canonical Shared Schemas   |
|  (bytes / Path / np.ndarray copy)  |   |   - OCRObservation           |
+------------------------------------+   |   - OCRResult (Pydantic/API) |
            |                            +------------------------------+
            v
+-----------------------------------------------------------------------+
|                       nirikshak_ocr.OCREngine                         |
|  - DBNet++ Text Detection (ONNX)                                      |
|  - Text Direction / Angle Classifier (ONNX)                           |
|  - Latin & Devanagari SVTR / CTC Recognition (ONNX)                   |
|  - Baseline B0 (Raw) / Provisional P-Adaptive Preprocessing           |
+-----------------------------------------------------------------------+
```

---

## 3. Method Specifications

### 3.1 Singleton Lifecycle
```python
@classmethod
def get_instance(cls, config: Optional[OCRConfig] = None) -> "OCRService":
    """
    Returns the process-wide OCRService singleton.
    Thread-safe double-checked locking ensures only one OCREngine is allocated in memory.
    """
```
- Ensures multiple FastAPI requests share the exact same ONNX Runtime sessions (~150 MB RSS) without duplicate allocations.
- `reset_instance()` provides a clean teardown hook for test suites and memory release.

### 3.2 Pre-Flight Warmup
```python
def warmup(self) -> Dict[str, Any]:
    """
    Executes a dummy inference pass on a 64x64 synthetic canvas.
    Primes ONNX Runtime thread pools, memory allocators, and execution providers.
    """
```
- Called during FastAPI application startup lifespan event (`@asynccontextmanager`).
- Eliminates cold-start latency jitter (270 ms init) from first real inspection requests.

### 3.3 Polymorphic Input Normalization
```python
def convert_image_input(image_input: Any) -> np.ndarray:
    """
    Normalizes any supported input format into a valid uint8 BGR numpy ndarray.
    Supported:
      - bytes / bytearray (decoded via cv2.imdecode)
      - str / Path (resolved and loaded via cv2.imread)
      - np.ndarray (validated for 2D/3D uint8, defensively copied via .copy())
    """
```
- **Defensive Copy Guarantee:** Any `np.ndarray` supplied by a caller is defensively cloned (`image.copy()`) prior to internal operations, guaranteeing caller arrays are never mutated.

### 3.4 Extraction Entrypoints
1. `extract(image_input) -> OCRResult`: Returns the full-fidelity Member 1 domain result object containing raw tokens, execution timings, script routing flags, and engine metadata.
2. `extract_observations(image_input) -> List[OCRObservation]`: Returns standard `nirikshak_shared.schemas.OCRObservation` models. Each observation contains:
   - `text`: Verbatim string transcript.
   - `confidence`: Float `[0.0, 1.0]`.
   - `bounding_box`: 4-point list of `(x, y)` coordinate pairs in original image pixel space.
3. `extract_dict(image_input) -> Dict[str, Any]`: Formats the result as an HTTP/JSON-ready dictionary containing:
   - `status`: `"SUCCESS"`
   - `tokens`: List of serialized token records
   - `total_lines`: Integer line count
   - `processing_time_ms`: Float execution latency
   - `metadata`: Engine configuration, model manifest IDs, preprocessing mode

---

## 4. Concurrency & Thread Safety

- **Locking Mechanism:** `OCRService` encapsulates a private `threading.Lock` (`_engine_lock`).
- **Critical Section:** Inference execution (`self.engine.predict(image)`) is enclosed within `with self._engine_lock:`.
- **Rationale:** While ONNX Runtime C++ sessions support multi-threaded inference, sharing internal session buffers across Python threads can introduce memory contention or race conditions on CPUExecutionProvider with intra-op threading. Explicit serialization guarantees absolute stability under FastAPI concurrent worker threads with deterministic latency behavior.

---

## 5. Error Taxonomy & HTTP Status Code Mapping

`OCRServiceError` encapsulates all operational failures:

| Error Code | Root Cause | HTTP Status | Description |
| :--- | :--- | :--- | :--- |
| `INVALID_IMAGE` | Unparseable bytes, corrupt file, non-image format, zero dimensions | `400 Bad Request` | Client uploaded an unreadable or corrupt payload. |
| `IMAGE_NOT_FOUND`| File path does not exist on disk | `404 Not Found` | Specified file path is missing. |
| `MODEL_NOT_FOUND`| ONNX model weights or character dictionaries missing | `500 Internal Error`| Server filesystem missing required model assets. |
| `ENGINE_ERROR`   | Native ONNX Runtime inference error | `500 Internal Error`| Runtime failure during graph execution. |
| `INFERENCE_TIMEOUT`| Execution exceeded hard deadline | `504 Gateway Timeout`| Inference took longer than timeout budget. |

Empty results (e.g. blank images, solid colors, clean surfaces) return `status="SUCCESS"` with `tokens=[]` and `total_lines=0`, rather than raising an error. This preserves strict domain separation between OCR execution and semantic interpretation.
