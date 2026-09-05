# CHUNK 1: OCR MODEL RESEARCH & DISCOVERY LOG
**Document:** `AI_CONTEXT/RESEARCH/CHUNK_1_OCR_RESEARCH.md`  
**Author:** OCR & Document AI Specialist  
**Traceability:** Official Upstream Documentation & Model Repositories

---

## 1. Candidate Models Researched

### Candidate A: PaddleOCR PP-OCRv3 / PP-OCRv4 (Baidu / PaddlePaddle)
- **Official Source:** `https://github.com/PaddlePaddle/PaddleOCR`
- **Architecture:** Two-stage scene text pipeline:
  - Detection: DBNet++ (Real-time scene text detection with Differentiable Binarization).
  - Recognition: SVTR-LCNet (Lightweight Vision Transformer / MobileNetV3 CTC sequence recognizer).
  - Angle Classification: MobileNetV2 directional classifier (0° / 180° orientation).
- **Lightweight Model Size:** Detection ~2.32 MB; Recognition ~10.2 MB; Direction Classifier ~0.56 MB. Total: ~13 MB.
- **Language Support:** Chinese, English, Alphanumeric (`ppocr_keys_v1.txt`).
- **ONNX Runtime Support:** Official ONNX exports available via `paddle2onnx` and bundled in `rapidocr-onnxruntime`.
- **License:** Apache 2.0.

### Candidate B: Devanagari PP-OCRv3 (Baidu Multilingual / Community ONNX)
- **Official Source:** PaddleOCR Multi-language Model Zoo & `monkt/paddleocr-onnx` (Hugging Face).
- **Architecture:** DBNet++ detection (shared with Candidate A) + Devanagari-trained SVTR-LCNet recognition model.
- **Dictionary:** `dict.txt` containing 167 Devanagari Unicode characters, conjuncts, matras, and Hindi numerals.
- **Model Size:** 8.56 MB (`rec.onnx`).
- **Language Support:** Hindi, Marathi, Nepali, Sanskrit, and Arabic numerals.
- **License:** Apache 2.0.

### Candidate C: EasyOCR (JaidedAI)
- **Official Source:** `https://github.com/JaidedAI/EasyOCR`
- **Architecture:** CRAFT (Character Region Awareness for Text Detection) + PyTorch ResNet-LSTM-CTC recognizer.
- **Model Size:** CRAFT ~70 MB + Language Model ~100 MB.
- **Runtime Footprint:** Requires PyTorch (`torch`, `torchvision`, `scipy`) pulling $> 1.8\text{ GB}$ of dependencies.
- **Language Support:** Supports 80+ languages including English and Hindi simultaneously.
- **Evaluation Status:** **DISQUALIFIED for Lightweight CPU Baseline**. The massive 1.8GB disk footprint, heavy PyTorch memory allocation ($> 800\text{MB}$ RSS), and slow CPU inference latency ($> 2.0\text{s}$) make it operationally unfavorable for our synchronous sub-2.5s budget.

### Candidate D: Tesseract OCR (Google / HP)
- **Official Source:** `https://github.com/tesseract-ocr/tesseract`
- **Architecture:** Legacy Tesseract engine + LSTM neural sequence recognizer.
- **Language Support:** `eng` + `hin` traineddata.
- **Evaluation Status:** **DISQUALIFIED on Host Environment**. Requires external C++ `tesseract.exe` installer on Windows. `where tesseract` returned empty on host. Adding external OS installer dependencies violates hackathon reproducibility.

---

## 2. Model Architecture Strategy Comparison

| Strategy | Accuracy Potential | Latency on CPU | Operational Complexity | Memory Footprint | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: Single English/Chinese Model** | High on English; **Zero on Hindi** | Very Low ($< 300\text{ms}$) | Minimal | Low ($< 250\text{MB}$) | Insufficient for bilingual Indian retail packages. |
| **Option B: Dual-Model Language Routing** | High on English; High on Hindi | Low ($< 400\text{ms}$) | Moderate (Script router) | Low ($< 300\text{MB}$) | **RECOMMENDED PRIMARY FOUNDATION**. Shared detector + routed recognizers. |
| **Option C: EasyOCR Monolithic Multilingual** | Moderate across both | High ($> 1,800\text{ms}$) | High (PyTorch stack) | High ($> 850\text{MB}$) | Disqualified due to latency and size bloat. |
| **Option D: Primary Model + Cloud Fallback** | Maximum | Variable ($> 3.0\text{s}$) | High (Cloud API) | Variable | Disqualified by Inviolable Zero-Cloud-AI rule. |
