# Working Prototype Case Specification

## Criterion
Working Prototype & Live Functional Demonstrability

## What Judges Need to Believe
1. The project is not slideware or mock design; the prototype demonstrates end-to-end functionality from camera input to PDF dossier generation.
2. The prototype runs locally, handles real physical packages, and reliably reacts to environmental variations (blur, missing calibration).

## Evidence Required
- Live executable application (`apps/web/` + `apps/api/`).
- Automated verification tests passing in CI (`tests/unit/test_verification_pipeline.py`).

## Nirikshak Feature
1. **Interactive Guided Capture:** Real-time feedback for multi-panel capture.
2. **Real-Time Quality Gate:** Instant rejection of blurry or glared frames.
3. **Calibrated Measurement Engine:** Accurate millimetre scale extraction.
4. **PDF Inspection Dossier Export:** Standalone downloadable dossier.

## Demo Proof
Execution of the complete 5-step live runbook detailed in `docs/11_JUDGING/DEMO_SCRIPT.md` using physical test packages in front of the jury.

## Benchmark Proof
End-to-end execution latency on standard 8-core CPU hardware ($\le 5.0\text{ s}$ target; Status: `TBD — MEASURE`).

## Known Weakness
Web-based camera capture in a browser sandbox has higher latency than native Android camera SDK bindings (planned for production phase).

## Answer to Likely Judge Challenge
- **Judge Challenge:** *"Is this calling an online API like Google Cloud Vision behind the scenes?"*
- **Answer:** *"No. Nirikshak is designed for offline/local CPU execution without external cloud APIs — runtime implementation and physical latency benchmarking are scheduled for Stage 2. Model inference (PaddleOCR/CRNN), calibration geometry, and rule evaluation are architected to run entirely on local CPU hardware without external API calls or transmitting inspection imagery off-device."*
