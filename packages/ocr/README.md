# Nirikshak OCR Package (`nirikshak-ocr`)

## Purpose
Direct ONNX Runtime implementation of lightweight multilingual text detection (DBNet++) and script-routed character recognition (SVTR-LCNet / SVTR-Devanagari) to extract text tokens, bounding coordinates, and confidence scores from package labels. 100% local CPU execution without cloud APIs or third-party wrappers.

## Owner
Member 1: AI & Multilingual OCR Lead

## Interface Seams
- **Input**: Polymorphic image input (`np.ndarray`, `bytes`, `bytearray`, `str`, `Path`).
- **Output**: Canonical `List[OCRObservation]` (with pixel/normalized bounding coordinates, text strings, confidences, language codes) and `OCRResult`.
- **Error Hierarchy**: `OCRError`, `ModelLoadError`, `InvalidImageError`, `UnsupportedImageError`, `InferenceError`, `OCRServiceError`.

