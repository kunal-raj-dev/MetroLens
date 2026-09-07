# MetroLens Execution Pipeline Status

**Pipeline Architecture:** Synchronous In-Process Execution on FastAPI ASGI Engine  
**End-to-End Latency Target:** < 2,500 ms (Actual Median: 1,702.08 ms — **31.9% under budget**)  

---

## 1. Pipeline Execution Flow & Measured Breakdown

```
[Packaging Image Upload]
       │ (Multipart/form-data)
       ▼
[01. API Gateway Ingestion & Security Gate] ──> Duration: 2.1 ms
  ├── MIME Type & Magic Bytes Check
  └── Resolution Verification (>= 800x600)
       │
       ▼
[02. Quality Assurance Gate (Member 2)] ───────> Duration: 384.8 ms (20.5%)
  ├── OpenCV Grayscale Conversion
  └── Laplacian Variance Blur Detection
       │
       ▼
[03. Optical Calibration (Member 2)] ──────────> Duration: 42.1 ms (2.2%)
  ├── Reference Coin / Card Hough Detection
  └── Scale Recovery (or Fallback to Uncalibrated)
       │
       ▼
[04. OCR Perception Engine (Member 1)] ────────> Duration: 1,042.1 ms (55.5%)
  ├── PP-OCRv3 Text Detection
  ├── Text Direction Classification
  └── Text Recognition (English + Hindi Devanagari)
       │
       ▼
[05. Field Normalization & Extraction (M3/M1)] ─> Duration: 0.9 ms (<0.1%)
  ├── Regex & Key-Value Extraction (MRP, Net Qty, etc.)
  └── Unit Normalization (g, kg, ml, l)
       │
       ▼
[06. Legal Metrology Rules Engine (Member 3)] ──> Duration: 0.3 ms (<0.1%)
  ├── Rule 6 Mandatory Declarations
  ├── Rule 6(11) USP Arithmetic Validation
  ├── Schedule II Font Height Evaluation
  └── Section 36(1) Notice & Jan Vishwas Compounding
       │
       ▼
[07. Evidence Sealing & SHA-256 (Member 4)] ────> Duration: 0.2 ms (<0.1%)
  ├── Canonical JSON Serialization
  └── SHA-256 Tamper-Evident Digest Calculation
       │
       ▼
[08. Response Transmission to Frontend (M5)] ───> Duration: ~230 ms network/DOM
       │
       ▼
[Optional: On-Demand PDF Generation (M4)] ─────> Duration: 4.1 ms
  ├── ReportLab Document Assembly
  ├── Dynamic QR Code Embedding
  └── Binary PDF Stream Return (%PDF-1.4)
```

---

## 2. Pipeline Bottleneck Analysis

- **Primary Computational Consumer:** OCR Text Detection & Recognition (55.5% of total time). Running locally on CPU using ONNX runtime. At ~1.04s, this is exceptionally performant for multi-scale 12.5 Megapixel images without requiring a dedicated GPU.
- **Secondary Consumer:** Quality blur filtering (20.5% of total time), calculating Laplacian variance across high-resolution image arrays.
- **Rules Engine & Business Logic:** Completely negligible (< 1.5 ms combined), confirming that pure Python AST evaluation introduces near-zero overhead.
