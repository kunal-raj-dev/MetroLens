# AI CONTEXT: MEMBER 5 — WEB FRONTEND & USER EXPERIENCE
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering, Web Application & User Experience Lead  
**Scope:** `apps/web/` (Next.js 14 App Router, React 18, TypeScript, Tailwind CSS, Lucide React)  

---

## 1. Subsystem Index & Directory Map

```text
AI_CONTEXT/MEMBER_5/
├── INDEX.md                     # Subsystem navigation & executive overview
├── PROJECT_CONTEXT.md           # Product invariants, visual language & non-goals
├── RUN_LOGS/                    # Chronological execution logs per chunk
│   ├── M5-1_RUN_LOG.md          # Chunk M5-1 execution log
│   ├── M5-2_RUN_LOG.md          # Chunk M5-2 execution log
│   ├── M5-3_RUN_LOG.md          # Chunk M5-3 execution log
│   ├── M5-4_RUN_LOG.md          # Chunk M5-4 execution log
│   └── M5-5_RUN_LOG.md          # Chunk M5-5 execution log
├── CHUNKS/                      # Step-by-step engineering records
│   ├── M5-1/                    # Foundation & Design System (COMPLETE & FROZEN)
│   ├── M5-2/                    # Upload Zone & Inspection Client (COMPLETE & FROZEN)
│   ├── M5-3/                    # Compliance Dashboard & Evidence Canvas (COMPLETE & FROZEN)
│   ├── M5-4/                    # Declaration Table & Inspector Review (COMPLETE & FROZEN)
│   ├── M5-5/                    # Sample Package Workflow + PDF + Demo Mode (COMPLETE & FROZEN)
│   └── M5-6/                    # Final QA, Accessibility & MVP Freeze (AWAITING PROMPT)
└── HANDOFFS/                    # Inter-subsystem handoff documentation
```

---

## 2. Inviolable Architectural Principles
1. **Separation of Perception, Measurement, Rules, and Presentation:**
   $$\text{M1 (OCR Perception)} \longrightarrow \text{M2 (Metric Calibration)} \longrightarrow \text{M3 (Statutory Rules)} \longrightarrow \text{M5 (Visual Presentation)}$$
2. **Authoritative Backend Truth:**
   The frontend displays compliance states delivered by the backend. The frontend never acts as a rule engine.
3. **Pixel Space Coordinate Fidelity:**
   Member 1’s OCR tokens remain in original-image pixel coordinates. The Evidence Canvas applies runtime affine transforms (`Image -> Canvas -> Screen`), never permanent percentage mutations.
4. **Adapter-Based Client:**
   `InspectionClient` encapsulates mock and live communication, exposing a stable `FrontendInspectionModel` to the UI.
5. **Multi-Modal Accessibility:**
   Every compliance status must be communicated via Color + Icon + Text Label + Plain Language Explanation.
6. **Honest Reporting & Sovereign Transparency:**
   No fake client PDFs or hidden mock fallbacks. The system clearly states operational mode (`SYNTHETIC DEMO` vs `LIVE INSPECTION`) and honest backend report availability.
