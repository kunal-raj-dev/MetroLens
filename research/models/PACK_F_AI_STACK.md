# RESEARCH EVIDENCE PACK F — AI STACK, MODELS & VISION RUNTIMES

**Research Scope:** Computer Vision, OCR Models, Calibration Libraries, and Edge Inference Runtimes  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Anti-AGPL Licensing Compliance & CPU-Only Field Execution  
**Pack Status:** 🟠 HIGH (Verified secondary-source/model documentation; Nirikshak empirical benchmarks pending)

---

## 1. Executive Summary & Architecture Principles

To ensure practical utility for Legal Metrology officers operating in mandis, factories, and retail shops without reliable internet or specialized GPU workstations, Nirikshak's AI stack adheres to three principles:

1. **Strict Permissive Licensing (Anti-AGPL Policy):** Commercial software utilizing viral copyleft licenses (such as GNU AGPLv3 found in Ultralytics YOLOv8/YOLOv11) poses severe compliance and intellectual property risks for government deployments. Nirikshak **rejects AGPL models** in favor of **Apache 2.0, MIT, and BSD-licensed vision algorithms**.
2. **CPU-Native Edge Execution:** Models must execute within a reasonable latency envelope on commodity x86_64 laptops (Intel Core i5, 8GB RAM) using ONNX Runtime with INT8 quantization; discrete NVIDIA GPUs are optional accelerators, never hard dependencies.
3. **Deterministic Geometric Metrology:** Black-box deep neural networks are not used to judge font height compliance directly. Instead, deep learning is restricted to **observational text detection and recognition**, while statutory font height and PDP area compliance are computed via **deterministic, calibrated geometric equations** auditable in a court of law.

---

## 2. Model & Library Registry

### 2.1 PaddleOCR PP-OCRv4 (Primary Multilingual OCR)
- **Component:** Text Detection (DBNet) & Text Recognition (SVTR-LCNet)
- **Version:** PP-OCRv4 (PaddlePaddle v2.5+)
- **Paper / Repository:** `https://github.com/PaddlePaddle/PaddleOCR` / arXiv:2206.03001
- **Code License:** Apache License 2.0
- **Weights License:** Apache License 2.0
- **Supported Languages:** English, Hindi (Devanagari), Tamil, Telugu, and 80+ global scripts.
- **Hardware Requirements:** x86_64 CPU (AVX2 instructions supported); 2GB RAM minimum footprint.
- **Inference Constraints:** Pre-trained mobile model weights: ~15 MB total. Supports ONNX Runtime CPU provider and OpenVINO acceleration.
- **Benchmark Evidence:**
  - Standard ICDAR / MLT benchmarks report precision $> 85\%$ on scene text.
  - Nirikshak status: `TARGET — NOT VALIDATED; Status: TBD — MEASURE` on physical packaging label benchmark.
- **Governance Decision:** **`APPROVED`** (Primary detection and recognition engine).

---

### 2.2 Tesseract OCR v5 (Fallback Latin & Devanagari OCR)
- **Component:** Line Binarization & LSTM Character Sequence Recognition
- **Version:** Tesseract 5.3.x (`pytesseract` wrapper v0.3.10)
- **Paper / Repository:** `https://github.com/tesseract-ocr/tesseract` (Google / HP)
- **Code License:** Apache License 2.0
- **Weights License:** Apache License 2.0 (tessdata / tessdata_fast)
- **Supported Languages:** 100+ languages including English (`eng`), Hindi (`hin`), Marathi (`mar`), Bengali (`ben`).
- **Hardware Requirements:** Single-core CPU, $< 100\text{ MB}$ RAM footprint.
- **Inference Constraints:** Performs exceptionally well on high-contrast, non-skewed rectangular label crops; sensitive to perspective distortion, curved text, and complex backgrounds.
- **Benchmark Evidence:**
  - High accuracy on clean scanned text; degraded on curved cylindrical cans.
- **Governance Decision:** **`APPROVED`** (Secondary fallback OCR engine for cropped high-contrast declaration fields).

---

### 2.3 OpenCV 4.x (Computer Vision & Metrology Core)
- **Component:** Image Preprocessing, Camera Calibration, ArUco Fiducial Detection, Planar Homography, Connected Components
- **Version:** OpenCV 4.9.0 (`opencv-python-headless`)
- **Paper / Repository:** `https://github.com/opencv/opencv`
- **Code License:** Apache License 2.0
- **Weights License:** N/A (Algorithmic / Deterministic C++ implementation)
- **Supported Languages:** C++, Python, Java
- **Hardware Requirements:** CPU-native, multithreaded OpenMP/Eigen vectorization.
- **Inference Constraints:** Execution time $< 100\text{ ms}$ per megapixel on modern Intel Core i5.
- **Benchmark Evidence:** Standard ISO camera calibration and ArUco pose estimation benchmarks establish sub-millimeter geometric accuracy under planar rigid constraints.
- **Governance Decision:** **`APPROVED`** (Foundational metrological calibration and perspective correction engine).

---

### 2.4 RT-DETR (Permissible Real-Time Object & Panel Detector)
- **Component:** Real-Time Vision Transformer Object Detection
- **Version:** RT-DETR-L / RT-DETR-R18
- **Paper / Repository:** `https://github.com/lyuwenyu/RT-DETR` / Baidu (arXiv:2304.08069)
- **Code License:** Apache License 2.0
- **Weights License:** Apache License 2.0
- **Supported Languages:** Visual object classes.
- **Hardware Requirements:** CPU with ONNX Runtime or discrete GPU.
- **Inference Constraints:** Suitable for detecting panel boundaries, barcode regions, and warning symbols.
- **Benchmark Evidence:** Outperforms YOLO architectures on COCO object detection benchmark with faster CPU inference times.
- **Governance Decision:** **`APPROVED`** (Designated neural detector if deep-learning panel segmentation is required in Stage 3).

---

### 2.5 Ultralytics YOLOv8 / YOLOv11 (REJECTED Model)
- **Component:** Object Detection & Instance Segmentation
- **Version:** YOLOv8 / YOLOv11
- **Paper / Repository:** Ultralytics LLC (`https://github.com/ultralytics/ultralytics`)
- **Code License:** **GNU Affero General Public License v3.0 (AGPL-3.0)**
- **Weights License:** AGPL-3.0 (Commercial license requires paid subscription)
- **Governance Decision:** **`REJECTED — PROHIBITED BY POLICY`**
- **Rationale:** AGPL-3.0 contains viral network-trigger copyleft provisions that require anyone running the software over a network to release all proprietary integration code under AGPL. This is incompatible with government enterprise deployments and closed backend integrations.

---

### 2.6 ONNX Runtime & OpenVINO (Inference Acceleration Runtimes)
- **Component:** High-Performance Cross-Platform ML Inference Engine
- **Version:** ONNX Runtime v1.17.x / Intel OpenVINO 2024.x
- **Repository:** `https://github.com/microsoft/onnxruntime`
- **Code License:** MIT License (ONNX Runtime) / Apache License 2.0 (OpenVINO)
- **Hardware Requirements:** x86_64, ARM64 (CPU execution with AVX-512, AVX2, VNNI int8 vectorization).
- **Inference Constraints:** Enables 2x to 4x throughput improvement on CPU-only edge hardware via 8-bit integer quantization.
- **Benchmark Evidence:** Widely benchmarked across edge vision systems.
- **Governance Decision:** **`APPROVED`** (Standard runtime for all exported deep-learning models).
