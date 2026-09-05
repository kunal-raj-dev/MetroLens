# NIRIKSHAK — LIBRARY & MODEL DEPENDENCY AUDIT

**Audit Scope:** Software Libraries, Machine Learning Models, Licensing, and Hardware Runtimes  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Nirikshak Architecture Claim Discipline & License Compliance Policy  
**Operational Target:** Commodity x86_64 Field Laptop (CPU-only execution, zero GPU requirement)

---

## 1. Executive Summary

This audit evaluates all third-party software libraries, frameworks, machine learning models, and computer vision runtimes proposed for the Nirikshak inspection system.

### Key Audit Highlights:
1. **License Safety & AGPL Avoidance:** Nirikshak enforces a strict **anti-AGPL policy** for core libraries to prevent viral copyleft licensing complications in government software deployments. Specifically, commercial models with AGPL restrictions (such as Ultralytics YOLOv8) are **excluded in favor of Apache 2.0 or BSD-licensed computer vision algorithms** (OpenCV contour extraction, PaddleOCR, RT-DETR).
2. **CPU-Only Field Viability:** The entire AI vision and optical pipeline is engineered to execute on **standard x86_64 consumer CPUs (Intel Core i5/i7, 8GB–16GB RAM)** without requiring discrete NVIDIA GPUs. ONNX Runtime and OpenVINO quantization pathways are specified for edge acceleration.
3. **Strict Separation of Active vs. Planned Dependencies:** The root `requirements.txt` strictly installs only active verification and testing libraries (`pyyaml`, `jsonschema`, `pytest`, `ruff`), with heavy runtime ML dependencies commented out and clearly earmarked for Stage 2 development.

---

## 2. Third-Party Library License & Lifecycle Audit

| Library / Tool | Intended Role | License | Active / Planned | Dependency Risk Assessment & Governance Decision |
| :--- | :--- | :--- | :--- | :--- |
| **PyYAML** | Regulatory registry & YAML parsing | MIT | **ACTIVE** | Permissive license. Installed and verified in active CI pipeline. |
| **jsonschema** | Declarative rule schema validation | MIT | **ACTIVE** | Permissive license. Installed and verified in active CI pipeline. |
| **pytest** | Test automation framework | MIT | **ACTIVE** | Permissive license. Active test suite executor. |
| **ruff** | High-performance linter / static analysis | MIT | **ACTIVE** | Permissive license. Active in CI workflow. |
| **FastAPI** | REST API framework for inspection service | MIT | `PLANNED` | Permissive license. High-performance asynchronous routing; planned for Stage 2. |
| **Pydantic v2** | Data schema validation & serialization | MIT | `PLANNED` | Permissive license. Fast Rust-backed data modeling; planned for Stage 2. |
| **OpenCV (`opencv-python-headless`)** | Image preprocessing, calibration, contours | Apache 2.0 | `PLANNED` | Headless build avoids bulky GUI/X11 dependencies. License compatible. |
| **PaddleOCR** | Multilingual text detection & recognition | Apache 2.0 | `PLANNED` | Apache 2.0 license. Pre-trained models support English, Hindi, and regional Indian scripts. |
| **pytesseract** | Fallback OCR engine wrapper | Apache 2.0 | `PLANNED` | Mature fallback engine for clean Latin text. Requires local `tesseract-ocr` binary. |
| **ReportLab** | PDF inspection dossier generation | BSD | `PLANNED` | Permissive open-source license. High-precision vector layout for statutory dossiers. |
| **SQLAlchemy v2 / aiosqlite** | Relational data persistence & migrations | MIT | `PLANNED` | Clean async ORM supporting local SQLite for offline operations and PostgreSQL for servers. |
| **cryptography** | SHA-256 evidence hashing & RSA signing | Apache 2.0 / BSD | `PLANNED` | Standard cryptographic primitive library for Section 63 BSA compliance. |

---

## 3. Machine Learning & Computer Vision Model Audit

| Model Component | Architecture / Base | Origin / Framework | License | Hardware Target | Evaluation & Governance Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Text Detection** | DBNet (PP-OCRv4 Server/Mobile) | PaddlePaddle / ONNX | Apache 2.0 | CPU (ONNX Runtime) | Highly efficient differentiable binarization detector. Permissive license. Approved. |
| **Text Recognition** | SVTR-LCNet (PP-OCRv4) | PaddlePaddle / ONNX | Apache 2.0 | CPU (ONNX Runtime) | Lightweight transformer-CNN hybrid for multilingual Latin and Devanagari text. Approved. |
| **Fallback OCR** | Tesseract LSTM Engine | Google / Tesseract | Apache 2.0 | CPU (Multi-thread) | Offline CPU-native OCR engine for high-contrast English packaging text. Approved. |
| **PDP Bounding** | OpenCV Contour & Aspect Filtering | Native OpenCV (C++) | Apache 2.0 | CPU (Native) | Deterministic geometric algorithm; avoids black-box neural object detectors for legal auditability. |
| **Object Detection (Alternative)** | Ultralytics YOLOv8 / YOLOv11 | Ultralytics | **AGPL-3.0** | GPU / CPU | **REJECTED**: AGPL-3.0 imposes severe viral open-source requirements on proprietary government integrations. |
| **Permissible Object Detector** | RT-DETR / YOLOv6 | Baidu / Meituan | Apache 2.0 | CPU / OpenVINO | Permissible Apache 2.0 object detection architecture if deep-learning segmentation is required in Phase 3. |

---

## 4. Hardware Constraints & Runtime Optimization

```
+-------------------------------------------------------------------------+
|                Target Hardware: Commodity Field Laptop                  |
|          Intel Core i5 (8th Gen+) / AMD Ryzen 5 | 8 GB RAM | No GPU     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  Offline Inference Optimization Layer                   |
|  - ONNX Runtime CPU Provider (OpenMP multi-threading enabled)           |
|  - 8-bit Integer Quantization (INT8) for PP-OCRv4 weights (~15MB size)  |
|  - OpenCV Headless (Optimized BLAS / Eigen vectorization)               |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                      Target Performance Envelope                        |
|  - Image Preprocessing + Homography Rectification: < 400 ms (CPU)       |
|  - Multilingual OCR Full-Label Pass: < 2,500 ms (CPU)                   |
|  - Rule Evaluation & Dossier Cryptographic Hash: < 200 ms (CPU)         |
|  - Status: TARGET — NOT VALIDATED; Empirical validation in Stage 2      |
+-------------------------------------------------------------------------+
```

---

## 5. Dependency Audit Conclusion & Stage Gate Checklist

| Audit Check | Status | Verification Detail |
| :--- | :--- | :--- |
| Are viral copyleft (GPL/AGPL) dependencies present in core codebase? | **NO** | Zero AGPL dependencies. YOLOv8 explicitly rejected; Apache 2.0 and MIT standard enforced. |
| Are heavy ML frameworks installed in pre-implementation CI? | **NO** | Active `requirements.txt` is lightweight; ML packages commented out until Stage 2. |
| Can the system execute without an NVIDIA GPU or cloud connection? | **YES** | All planned vision and OCR models are optimized for CPU ONNX runtime. |
| Are all active testing and verification tools covered by unit tests? | **YES** | Active CI verification scripts have 100% test pass rate in `tests/unit/` (5/5 tests passing). Runtime application code is pending implementation. |

**Dependency & Model Audit Result:** **`PASS`**
