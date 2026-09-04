# CURRENT STATE: REPOSITORY SNAPSHOT
**Snapshot Date:** 2026-09-05T03:02:35+05:30  
**Repository Root:** `c:\Users\kunal\Desktop\MetroLens`

## 1. Directory Tree & Architecture Layout
```text
c:\Users\kunal\Desktop\MetroLens\
├── AI_CONTEXT/                     # Persistent working context, research, and decisions
├── CURRENT_STATE/                  # Current-state system and environment snapshots
├── METROLENS_LEGAL_SOURCE_PACK/    # 74 primary government legal source PDFs & registry
├── apps/
│   ├── api/                        # FastAPI gateway (scaffold)
│   ├── web/                        # React frontend (scaffold)
│   └── worker/                     # Worker directory (scaffold)
├── packages/
│   ├── calibration/                # Metric scale & rectification (scaffold)
│   ├── evidence/                   # Evidence packaging (scaffold)
│   ├── extraction/                 # Entity extraction (scaffold)
│   ├── measurement/                # Measurement math (scaffold)
│   ├── ocr/                        # OCR engine (scaffold)
│   ├── reporting/                  # PDF reporting (scaffold)
│   ├── rules-engine/               # Statutory rule engine (scaffold)
│   ├── shared/                     # Shared models & utilities (scaffold)
│   └── vision/                     # Quality filters (scaffold)
├── data/
│   ├── annotations/                # Empty
│   ├── benchmark/                  # Empty
│   ├── manifests/                  # manifest.yaml
│   ├── processed/                  # Empty
│   ├── raw/                        # Empty (0 real package images)
│   └── synthetic/                  # Empty
├── docs/
│   ├── API_CONTRACT.md             # Frozen OpenAPI 3.1 & Pydantic schemas
│   ├── ARCHITECTURE.md             # Authoritative web architecture specification
│   ├── LEGAL_RULE_MATRIX.md        # PCR 2011 & Jan Vishwas 2026 rules
│   ├── METROSETU_PROJECT_DETAILS.md# Plain-language project guide
│   ├── PRODUCT_BLUEPRINT.md        # Master product blueprint v1.0
│   ├── TEAM_RESPONSIBILITIES.md    # 6-Member ownership matrix
│   ├── TECHNICAL_DECISIONS.md      # ADR-001 through ADR-015
│   ├── TESTING_STRATEGY.md         # 5-Tier testing pyramid
│   └── team/                       # Member 1–6 work plans & checklists
├── scripts/
│   └── verification/               # 6 Python verification scripts
└── tests/
    └── unit/test_verification_pipeline.py
```

## 2. Code vs. Document Ratio
- Total documentation files in `docs/`: 26 files
- Total tests: 1 test file (`tests/unit/test_verification_pipeline.py`)
- Total application source code in `apps/` and `packages/`: 0 python files (scaffold only)
- Real image dataset status: **0 physical images currently on disk in `data/`**
