# STANDARDIZED PACKAGING OCR FAILURE TAXONOMY
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_ANALYSIS/FAILURE_TAXONOMY.md`  
**Standard:** Member 1 OCR Error Classification Standard v1.0  
**Evaluation Scope:** FMCG Retail Packaging (Evaluated on Synthetic Regression Baseline B0 + Real Packaging Target Specification)  

---

## 1. Classification Categories & Observed Distribution

| Error Category | Severity | Observed in Synthetic Harness (B0) | Synthetic Harness Proportion | Real-World Prevalence | Representative Example | Candidate Remedy |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **NUMERIC_CONFUSION** | CRITICAL | 3 / 8 synthetic specimens | 37.5% of synthetic suite | PENDING (0 real images) | `0` transcribed as `O`, `1` as `I`/`l`, missing `.` in `20.00` | Post-OCR numeric context validator; digit-biased vocabulary in statutory number zones. |
| **LOW_CONTRAST** | HIGH | 1 / 8 synthetic specimens | 12.5% of synthetic suite | PENDING (0 real images) | Faded grey expiry stamp on reflective silver foil (`SYNTH-08`) | Adaptive crop CLAHE in LAB color space (triggered when $\sigma_{\text{luma}} < 35$). |
| **SCRIPT_ROUTING** | HIGH | 1 / 8 synthetic specimens | 12.5% of synthetic suite | PENDING (0 real images) | Mixed-script packaging where English recognizer misses Devanagari words (`SYNTH-02`) | ScriptRouter confidence-gated fallback; language hint propagation from client. |
| **SMALL_TEXT** | MEDIUM | 1 / 8 synthetic specimens | 12.5% of synthetic suite | PENDING (0 real images) | Microscopic declarations below 1mm font height (`SYNTH-04`) | DBNet++ `max_side_len` high-res scaling (up to 1600px); Member 2 homography rectification. |
| **DOT_MATRIX** | HIGH | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | Fragmented inkjet batch numbers with disconnected ink dots | Morphological dilation filter with polarity-aware rectangular kernel ($2\times2$). |
| **GLARE** | CRITICAL | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | White specular reflection obliterating MRP on glossy laminate pouches | Upstream image quality gate rejection (`packages/vision`); retake prompt. |
| **CURVED_TEXT** | HIGH | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | Cylinder distortion on metal soda cans and round cosmetic bottles | Member 2 geometric unwarping / cylinder projection prior to OCR. |
| **BLUR / MOTION** | CRITICAL | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | Hand shake or out-of-focus smartphone camera capture | Laplacian variance sharpness gate ($< 100 \implies$ `RETAKE_REQUIRED`). |
| **DETECTION_FAILURE**| HIGH | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | Text region missed completely by DBNet++ | DBNet++ threshold tuning (`det_db_thresh = 0.25`, unclip ratio 1.8). |
| **RECOGNITION_FAIL** | MEDIUM | 0 / 8 synthetic specimens | 0.0% of synthetic suite | PENDING (0 real images) | Completely garbled CTC transcription | SVTR language model beam search decoding. |
| **PERFECT_MATCH** | NONE | 2 / 8 synthetic specimens | 25.0% of synthetic suite | PENDING (0 real images) | Blank frame correctly producing 0 tokens (`SYNTH-07`); clean label | Baseline raw pipeline (identity passthrough). |

> [!NOTE]
> **Denominator Integrity Note:** The percentages above describe the 8 controlled synthetic regression specimens only. They MUST NOT be extrapolated as market failure rates on real Indian FMCG retail packaging. Real-world validation remains BLOCKED awaiting physical retail packaging photography under Path B.


---

## 2. Deep-Dive: Critical Failure Modes

### A. NUMERIC_CONFUSION (Severity: CRITICAL)
- **Root Cause:** CTC greedy decoding has visual similarity between glyphs:
  - `0` (zero) vs `O` (capital letter O)
  - `1` (one) vs `I` (capital I) vs `l` (lowercase L)
  - `5` (five) vs `S` (capital S)
  - `.` (decimal point) lost in texture noise
- **Impact on MetroLens:** PCR 2011 compliance decisions depend on exact numeric values for MRP (Rule 6), Net Quantity (Rule 7), and Unit Sale Price (Rule 6(11)). A single digit flip turns a compliant package into a false non-compliance penalty notice.
- **Architectural Remedy:** Keep raw OCR output pure. Downstream Member 3 Legal Metrology rules engine applies statutory regex normalization with digit-bias when extracting currency and quantity declarations.

### B. LOW_CONTRAST (Severity: HIGH)
- **Root Cause:** Inkjet printing on metallic foil pouches (e.g. snack bags, crimp seals) suffers from specular sheen and low tonal separation between ink and substrate.
- **Empirical Finding:** Applying **Adaptive Crop CLAHE** boosts local luminance contrast without color shift, restoring edge boundaries for DBNet++ and SVTR.

### C. DOT_MATRIX (Severity: HIGH)
- **Root Cause:** Industrial inkjet printers generate characters as a matrix of detached dots (e.g. $5\times7$ grid). DBNet++ may break words into multiple isolated bounding boxes, or SVTR CTC decoders may miss disconnected dots.
- **Remedy:** Polarity-aware morphological dilation bridges adjacent dots into continuous character strokes.

### D. SCRIPT_ROUTING (Severity: HIGH)
- **Root Cause:** On bilingual packaging (e.g. Hindi + English), if a crop contains mixed characters, the heuristic confidence router may select the dominant script, causing characters of the alternate script to be dropped.
- **Remedy:** Confidence margin check ($|\text{conf}_{\text{lat}} - \text{conf}_{\text{dev}}| < 0.15 \implies$ dual candidate retention) and user language hint propagation.
