# CURRENT STATE: MEMBER 5 — FILE MAP
**Project:** MetroLens AI™ (SIH26034)  
**Package:** `apps/web/`  
**Last Updated:** 2026-09-05T18:25:00+05:30  
**Phase:** Chunk M5-5 (Complete)

---

## Target Directory Map for Member 5 Subsystem

```text
apps/web/
├── package.json                          # Node manifest and dependencies
├── next.config.mjs                       # Next.js 14 configuration
├── tsconfig.json                         # TypeScript configuration & path aliases
├── postcss.config.js                     # PostCSS plugins (Tailwind, Autoprefixer)
├── tailwind.config.ts                    # Semantic theme tokens and typography
├── public/
│   └── fixtures/                         # [M5-5] Verified static benchmark package assets
│       ├── SYNTH-01-ENG-FMCG.png         # English biscuit pouch (Rule 6 Pass)
│       ├── SYNTH-02-HIN-FMCG.png         # Pure Hindi atta bag (Devanagari ₹ Pass)
│       ├── SYNTH-03-BIL-FMCG.png         # Bilingual snack carton (Bilingual Pass)
│       ├── SYNTH-04-MICRO-FONT.png       # Shrinkflation micro-font (Rule 7 Deficit)
│       ├── SYNTH-05-LIQUID-VOLUME.png    # Handwash bottle (Volume ml Pass)
│       ├── SYNTH-06-PROHIBITED-UNITS.png # Detergent pouch (Rule 12 'gms' Deficit)
│       ├── SYNTH-07-BLANK-FRAME.png      # Blank cardboard (Quality Gate Reject)
│       └── SYNTH-08-LOW-CONTRAST-FADED.png # Low contrast foil (Suspect Review Case)
└── src/
    ├── app/
    │   ├── layout.tsx                    # Root HTML shell & global providers
    │   ├── page.tsx                      # Officer Workstation landing page & dual mode workstation
    │   └── globals.css                   # Semantic design tokens and Mastercard palette
    ├── components/
    │   ├── ui/
    │   │   ├── Button.tsx                # Accessible interactive button
    │   │   ├── Card.tsx                  # Structural panel card (stadium / lifted)
    │   │   ├── Badge.tsx                 # Compact status and metadata pill
    │   │   ├── StatusIndicator.tsx       # 4-state multi-modal verdict banner
    │   │   ├── Dialog.tsx                # Accessible modal dialog with focus trap
    │   │   ├── Tooltip.tsx               # Contextual hover helper
    │   │   ├── Alert.tsx                 # Warning, info, error callout
    │   │   ├── Skeleton.tsx              # Pulse loading placeholder
    │   │   └── Input.tsx                 # Text and file input primitive
    │   └── ImageUploadZone.tsx           # [M5-2/M5-5] Ingestion dropzone & validation
    ├── features/
    │   └── inspection/
    │       ├── ComplianceDashboard.tsx   # [M5-3] Macro verdict & telemetry
    │       ├── EvidenceCanvas.tsx        # [M5-3] HTML5 original-pixel viewer & affine canvas
    │       ├── DeclarationTable.tsx      # [M5-4/M5-5] Extracted fields & Rule 6/7 checks
    │       ├── InspectorReviewModal.tsx  # [M5-4/M5-5] Human-in-the-loop review panel
    │       ├── SamplePackageSelector.tsx # [M5-5] Benchmark package carousel
    │       ├── canvasTransform.ts        # [M5-3] Affine matrix & coordinate math
    │       └── index.ts                  # Public feature barrel exports
    ├── services/
    │   ├── index.ts                      # Services barrel export
    │   ├── inspectionClient.ts           # [M5-2] Client interface & factory
    │   ├── reportClient.ts               # [M5-5] Statutory report PDF client
    │   └── adapters/
    │       ├── mockAdapter.ts            # [M5-2] In-memory mock adapter
    │       ├── liveApiAdapter.ts         # [M5-2/M5-5] Live FastAPI HTTP adapter
    │       └── responseNormalizer.ts     # [M5-2] Backend DTO -> Frontend Model
    ├── types/
    │   ├── contract.ts                   # Direct mirroring of backend API schemas
    │   └── frontend.ts                   # Normalized UI consumption models
    ├── utils/
    │   ├── validation.ts                 # [M5-2] Client-side image validation
    │   └── canvasTransform.ts            # Canvas transform utilities
    ├── mocks/
    │   └── fixtures.ts                   # [M5-2/M5-5] Synthetic demo payloads (SYNTH-01..08)
    └── __tests__/
        ├── canvas_transform.test.ts          # [M5-3] 20 unit tests for affine math & ray casting
        ├── m5_2_verification.test.ts         # [M5-2] 34 regression tests for validation & normalizer
        ├── m5_3_integration.test.ts          # [M5-3] 6 integration test suites for coordinate contracts
        ├── m5_4_declaration_review.test.ts  # [M5-4] 31 unit tests for declarations, review flow & caliper & dashboard
        └── m5_5_verification.test.ts     # [M5-5] 92 tests for sample workflow, PDF, and review
```
