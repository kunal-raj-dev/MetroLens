# BUG-001: Devanagari Recognizer Dictionary / Logit Dimension Discrepancy

**ID**: BUG-001  
**Area**: `packages/ocr/src/nirikshak_ocr/recognizer.py` (`CTCLabelDecoder` & `SVTRRecognizer`)  
**Severity**: HIGH  
**Owner**: Member 1 (AI & OCR Lead)  
**Status**: IDENTIFIED / PENDING FIX  

---

## 1. Symptom
`rec_hi` ONNX model (`models/weights/ocr/rec_hi/rec.onnx`) produces logits of shape `(batch, seq_len, 169)` (169 output classes).
However, `SVTRRecognizer.decoder.num_classes` is initialized with 168 classes.
Any model logit with argmax index = 168 (the 169th class) is dropped silently without being decoded or contributing to confidence.

## 2. Root Cause
In PaddleOCR CTC training convention (`use_space_char=True`):
The vocabulary is constructed as:
- Class 0: CTC blank token (`'blank'`)
- Class 1..N: Characters from dictionary file (`dict.txt`)
- Class N+1: Trailing space token (`' '`)

In `nirikshak_ocr/recognizer.py`, `CTCLabelDecoder.__init__` was implemented as:
```python
self.character_list = ["blank"] + list(character_list)
if " " not in self.character_list:
    self.character_list.append(" ")
self.num_classes = len(self.character_list)
```
Because line 1 of `models/weights/ocr/rec_hi/dict.txt` is an explicit space character (`' '`), `" " in self.character_list` evaluated to `True`. Consequently, the trailing space token was NOT appended, leaving `self.character_list` with 168 items instead of 169.

## 3. Impact
- High severity: Token decodings where the Devanagari CTC head predicts character class 168 have the token dropped or clipped.
- Discrepancy between ONNX graph output shape (`[..., 169]`) and CTC decoder vocabulary size (`168`).

## 4. Proposed Fix
In `SVTRRecognizer.__init__`:
Extract the output logit dimension from the ONNX session output:
`out_classes = self.session.get_outputs()[0].shape[-1]`
Pass `expected_classes` to `CTCLabelDecoder`.

In `CTCLabelDecoder.__init__`:
```python
def __init__(self, character_list: List[str], expected_classes: Optional[int] = None):
    self.character_list = ["blank"] + list(character_list)
    if expected_classes is not None and len(self.character_list) < expected_classes:
        while len(self.character_list) < expected_classes:
            self.character_list.append(" ")
    elif " " not in self.character_list:
        self.character_list.append(" ")
    self.num_classes = len(self.character_list)
```
This guarantees exact alignment with the ONNX output dimension without hardcoding.

## 5. Regression Test
`test_devanagari_dictionary_dimension_alignment`:
Assert `recognizer.decoder.num_classes == recognizer.session.get_outputs()[0].shape[-1]` for both Latin (6625) and Devanagari (169).
Verify that synthetic logit with argmax at index 168 successfully decodes to a space rather than being silently dropped.
