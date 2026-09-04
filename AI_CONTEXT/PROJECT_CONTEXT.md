# AI CONTEXT: PROJECT CONTEXT & ARCHITECTURAL INVARIANTS
**Project:** MetroLens AI (SIH26034)  
**Sponsoring Ministry:** Ministry of Consumer Affairs, Food & Public Distribution

## 1. Core Mission
Automate statutory compliance assessment for pre-packaged commodities under the *Legal Metrology (Packaged Commodities) Rules, 2011* and the *Jan Vishwas (Amendment of Provisions) Act, 2026*.

## 2. Inviolable Architectural Principles
1. **Zero Cloud AI in Adjudication:** No external generative LLMs (OpenAI, Claude, Gemini) may ever be used to determine legal compliance. All compliance decisions are 100% deterministic Python state machines codifying Gazette clauses.
2. **Local CPU Execution:** All computer vision and scene text OCR neural models must execute locally on consumer server/laptop CPUs without requiring discrete GPUs or per-query API costs.
3. **Synchronous Sub-2.5s Budget (ADR-012):** The inspection pipeline must complete in $< 2.5\text{s}$ wall-clock time from upload to UI render on standard CPU hardware.
4. **Separation of Perception from Law:**
   $$\text{AI Perceives (OCR)} \longrightarrow \text{Math Validates (Scale/USP)} \longrightarrow \text{Rules Decide (Gazette Law)} \longrightarrow \text{Humans Govern (Section 15)}$$
5. **Data Minimization & Ephemeral Storage (ADR-014):** In-memory processing with 60-minute TTL spooling for PDF generation. No permanent image database by default.
