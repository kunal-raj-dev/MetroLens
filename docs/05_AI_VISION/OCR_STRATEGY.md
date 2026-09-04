# Optical Character Recognition (OCR) Strategy

## Purpose
Specifies the text detection and recognition architecture, multilingual handling, pre-processing filters, and token confidence scoring.

## Scope
Covers optical character extraction across retail cartons, flexible pouches, glass bottles, and aluminium cans.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (mandating English and Hindi/Devanagari numeral and script recognition).

## Assumptions
- Inference runs locally on CPU/iGPU with optimized neural runtimes (ONNX / OpenVINO).

## Open Questions
- Optimal font recognition model for embossed, dot-matrix, or laser-etched batch dates [TBD — MEASURE].

## Dependencies
- `packages/ocr/`
- `models/`

## Verification Requirements
- Accuracy must be evaluated using `benchmarks/protocols/PROTO_OCR_EVAL.md` on real package sets.

---

## 1. Engine Selection & Pipeline

The system uses a decoupled two-stage OCR pipeline:

```
[Pre-Processed Image / Crop]
             │
             ▼
[Text Detection: DBNet (Real-time Differentiable Binarization)]
  • Fast, accurate arbitrary-shape text localization
  • Outputs oriented polygon coordinates
             │
             ▼
[Text Recognition: Multilingual CRNN / SVTR]
  • Multilingual dictionary support (English, Hindi / Devanagari)
  • Outputs raw string tokens, character spans, and confidence scores
             │
             ▼
[Token Post-Processing & Heuristic Normalization]
  • Spell-correction bounded to legal metrology dictionaries
  • Currency symbol normalization (Rs., INR, ₹)
  • Metric unit normalization (g, kg, ml, l, cm, m, N)
```

### Supported Scripts:
1. **Latin (English):** Mandatory declarations, brand names, addresses.
2. **Devanagari (Hindi):** Bilingual packaging declarations and numerals (०, १, २, ३, ४, ५, ६, ७, ८, ९).

### Confidence Policy:
- Tokens with confidence $\ge 0.85$: Accepted for automated field parsing.
- Tokens with confidence between $0.60$ and $0.85$: Extracted with visual yellow highlight for officer verification.
- Tokens with confidence $< 0.60$: Flagged as ambiguous; rule engine routes associated checks to `REVIEW`.
