# AI CONTEXT MANAGEMENT INDEX
**Project:** MetroLens AI (SIH26034)  
**Purpose:** Persistent repository of AI research, decisions, experiments, benchmark runs, and cross-session handoffs.

```text
AI_CONTEXT/
├── INDEX.md                     # Master index and context navigation
├── PROJECT_CONTEXT.md           # High-level product and technical invariants
├── DECISIONS/                   # Formal architectural and algorithmic decision records
├── RESEARCH/                    # Upstream documentation and technical research notes
├── EXPERIMENTS/                 # Isolated engineering spikes and benchmark runs
│   ├── CHUNK_1_OCR_MODEL_SELECTION/
│   │   ├── 01_PLAN/             # Spike hypothesis, protocol, and constraints
│   │   ├── 02_MODEL_RESEARCH/   # Model discovery and candidate profiling
│   │   ├── 03_DATASET/          # Test images and ground truth metadata
│   │   ├── 04_RUNS/             # Execution scripts and raw outputs
│   │   ├── 05_RESULTS/          # Structured comparisons (CSV / Markdown)
│   │   ├── 06_ANALYSIS/         # Comprehensive spike analysis report
│   │   ├── 07_DECISION/         # Provisional model selection decision
│   │   └── 08_HANDOFF/          # Engineering handoff to Chunk 2
│   ├── CHUNK_2_OCR_ENGINE/
│   │   ├── 01_PLAN/             # Chunk 2 execution plan and microstep protocol
│   │   ├── 02_RESEARCH/         # Runtime compatibility decision & PP-OCRv5 currency check
│   │   ├── 03_DESIGN/           # Pipeline architecture & coordinate specifications
│   │   ├── 04_IMPLEMENTATION/   # Modular engine, detector, recognizer, router
│   │   ├── 05_TESTS/            # 22 unit, integration, and offline isolation tests
│   │   ├── 06_RESULTS/          # Thread sweep, memory stability, and specimen metrics
│   │   ├── 07_REVIEW/           # Final hostile review and chunk report
│   │   └── 08_HANDOFF/          # Downstream handoff to Chunk 3
│   ├── CHUNK_3_REAL_DATA/
│   │   ├── 01_PLAN/             # Chunk 3 hypothesis, constraints, and protocol
│   │   ├── 02_DATA/             # Real data audit, provenance & zero-leakage split protocol
│   │   ├── 02_ANALYSIS/         # Failure taxonomy and error classification
│   │   ├── 03_BASELINE/         # Baseline B0 measurement without preprocessing
│   │   ├── 04_PREPROCESSING/   # CLAHE, bilateral, unsharp, dilation experiments
│   │   ├── 05_BENCHMARK/       # Machine-readable evaluation harness & results
│   │   ├── 06_ANALYSIS/         # Empirical comparison, CER/WER, latency & memory
│   │   ├── 07_DECISION/         # Final Chunk 3 report & adaptive policy selection
│   │   └── 08_HANDOFF/          # Engineering handoffs to Chunk 4, Member 2 & Member 6
│   ├── CHUNK_4_OCR_INTEGRATION/
│   │   ├── 01_PLAN/             # Chunk 4 execution plan and monorepo packaging
│   │   ├── 02_AUDIT/            # Monorepo repository audit & scope boundaries
│   │   ├── 03_DESIGN/           # Service adapter specification (OCRService facade)
│   │   ├── 04_IMPLEMENTATION/   # Packaging, path independence, error taxonomy & service
│   │   ├── 05_TESTS/            # 16-test integration suite & full 89-test matrix
│   │   ├── 06_RESULTS/          # Integration benchmark, adapter overhead & concurrency
│   │   └── 07_REVIEW/           # Final 24-section Chunk 4 integration report
│   ├── CHUNK_5_VERTICAL_SLICE/
│   │   ├── 01_PLAN/             # Chunk 5 execution plan and scope boundaries
│   │   ├── 02_AUDIT/            # Actual vs Documented & Target vs Actual analysis
│   │   ├── 05_TESTS/            # 9-test end-to-end integration suite & 98-test matrix
│   │   ├── 06_RESULTS/          # Vertical Slice 0 benchmark & stage latency profile
│   │   └── 07_REVIEW/           # Final 24-section Chunk 5 integration report
│   └── CHUNK_6_7_MEMBER_1_FINAL/
│       ├── 01_PLAN/             # Member 1 final plan and microstep protocol
│       ├── 02_BASELINE/         # Baseline environment snapshot and asset inventory
│       ├── 05_TESTS/            # Definitive M1-001–M1-018 test matrix and hardening tests
│       ├── 06_AUDIT/            # 35-question independent forensic audit report
│       ├── 07_DEBUG/            # Historical defect register & forensic resolution log
│       ├── 08_VALIDATION/       # Requirements validation matrix and limitations doc
│       ├── 09_DOCUMENTATION/    # Final M1 architecture blueprint and flowcharts
│       └── 11_FREEZE/           # Changelog, freeze manifest, and 31-section report
├── MEMBER_5_WEB_FRONTEND/       # Member 5 Web Frontend Subsystem (Audit, Plan, Boundaries, Contracts)
├── EVIDENCE/                    # Raw test outputs, execution logs, and benchmark traces
├── RUN_LOGS/                    # Chronological record of AI actions and experiments
└── HANDOFFS/                    # Inter-chunk and inter-member interface handoffs
```


