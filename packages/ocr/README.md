# Nirikshak OCR Package (`nirikshak-ocr`)

## Purpose
Wraps lightweight ONNX / RapidOCR multilingual text detection and character recognition models to extract text tokens, bounding coordinates, and confidence scores from package labels.

## Owner
AI / OCR Lead

## Interface Seams
- **Input**: Image numpy array, language list.
- **Output**: `List[OCRObservation]` (with normalized bounding boxes, text strings, confidences).
- **Error Codes**: `ERR_OCR_EMPTY`, `ERR_OCR_ENGINE_FAULT`.
