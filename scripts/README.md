# Nirikshak Scripts Directory Taxonomy

## Purpose
To avoid confusion during distributed development across multiple leads, scripts and tools are strictly organized by function:

| Script Domain | Canonical Location | Description |
| :--- | :--- | :--- |
| **Integrity & Verification** | `scripts/verification/` | CI/CD scripts enforcing repository invariants, source hash checks, rule safety, and claims verification. |
| **Legal Source Ingestion** | `tools/legal_sources/` | Web harvesters, official gazette PDF collectors, and gazette metadata parsers. |
| **Benchmark Execution** | `benchmarks/` | Optical metric accuracy, OCR character error rate (CER), and latency benchmarking harnesses. |
| **Dataset Preparation** | `data/` | Raw dataset ingestion, synthetic label rendering, and test split manifests. |
| **Reporting Tools** | `packages/reporting/` | Dossier generation and PDF rendering logic. |

Do not create ad-hoc script folders in `scripts/` without architectural consensus.
