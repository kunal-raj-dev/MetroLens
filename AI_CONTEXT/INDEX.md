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
│   └── CHUNK_1_OCR_MODEL_SELECTION/
│       ├── 01_PLAN/             # Spike hypothesis, protocol, and constraints
│       ├── 02_MODEL_RESEARCH/   # Model discovery and candidate profiling
│       ├── 03_DATASET/          # Test images and ground truth metadata
│       ├── 04_RUNS/             # Execution scripts and raw outputs
│       ├── 05_RESULTS/          # Structured comparisons (CSV / Markdown)
│       ├── 06_ANALYSIS/         # Comprehensive spike analysis report
│       ├── 07_DECISION/         # Provisional model selection decision
│       └── 08_HANDOFF/          # Engineering handoff to Chunk 2
├── EVIDENCE/                    # Raw test outputs, execution logs, and benchmark traces
├── RUN_LOGS/                    # Chronological record of AI actions and experiments
└── HANDOFFS/                    # Inter-chunk and inter-member interface handoffs
    ├── CHUNK_1_TO_CHUNK_2.md             # Member 1 OCR Spike -> Chunk 2 Pipeline Handoff
    ├── MEMBER_2_PHASE_4_TO_PHASE_5.md    # Member 2 Anchor Detection -> Planar Homography Handoff
    ├── MEMBER_2_PHASE_5_6_7_TO_DOWNSTREAM.md # Member 2 Homography, Font & Cylinder -> Downstream
    └── MEMBER_2_PHASES_8_9_EVALUATION_HANDOFF.md # Member 2 Robustness & Evaluation Engine Handoff
```

## Workstream Index Links
- **Member 1 (OCR Lead):** `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/` & `CURRENT_STATE/CHUNK_1_STATUS.md`
- **Member 2 (CV & Optical Calibration Lead):**
  - Current Status: [`CURRENT_STATE/MEMBER_2_STATUS.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/CURRENT_STATE/MEMBER_2_STATUS.md)
  - Work Plan: [`docs/team/MEMBER_2_WORK_PLAN.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/docs/team/MEMBER_2_WORK_PLAN.md)
  - Phase 3 Calibration Spike Report: [`benchmarks/reports/spike_calibration_report.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/benchmarks/reports/spike_calibration_report.md)
  - Calibration Package Documentation: [`packages/calibration/README.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/packages/calibration/README.md)
  - Phase 4 &rarr; Phase 5 Handoff: [`AI_CONTEXT/HANDOFFS/MEMBER_2_PHASE_4_TO_PHASE_5.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/AI_CONTEXT/HANDOFFS/MEMBER_2_PHASE_4_TO_PHASE_5.md)
  - Phase 5, 6 & 7 Downstream Handoff: [`AI_CONTEXT/HANDOFFS/MEMBER_2_PHASE_5_6_7_TO_DOWNSTREAM.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/AI_CONTEXT/HANDOFFS/MEMBER_2_PHASE_5_6_7_TO_DOWNSTREAM.md)
  - Phases 8 & 9 Robustness & Evaluation Handoff: [`AI_CONTEXT/HANDOFFS/MEMBER_2_PHASES_8_9_EVALUATION_HANDOFF.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/AI_CONTEXT/HANDOFFS/MEMBER_2_PHASES_8_9_EVALUATION_HANDOFF.md)
  - Phase 9 Calibration Evaluation Report: [`benchmarks/reports/calibration_evaluation_report.md`](file:///c:/Users/admin/Documents/GitHub/MetroLens/benchmarks/reports/calibration_evaluation_report.md)
