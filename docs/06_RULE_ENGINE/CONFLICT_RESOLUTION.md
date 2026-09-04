# Conflict Resolution & Contradiction Detection

## Purpose
Specifies the cross-panel correlation logic, multi-view discrepancy detection, and statutory conflict-handling protocols of the rule engine.

## Scope
Covers contradictory text across panels (e.g. MRP on carton differing from MRP on bottle cap) and competing statutory source interpretations.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (prohibiting dual or contradictory declarations).

## Assumptions
- Conflicting declarations on the same physical commodity constitute either deceptive packaging, tampering, or statutory non-compliance.

## Open Questions
- Departmental guidelines regarding sticker overlays on imported commodities correcting original overseas declarations [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/rules-engine/`
- `packages/extraction/`

## Verification Requirements
- Test fixtures in `tests/fixtures/conflicting_panels/` must reliably trigger conflict flags and route to `REVIEW`.

---

## 1. Multi-Panel Contradiction Detection

During guided capture, the system ingests multiple distinct surfaces of a single SKU. The conflict detection engine compares normalized field values across panels:

```
[Principal Display Panel (PDP)]       [Rear Information Panel]
Net Qty: 500 g                        Net Qty: 450 g
         │                                      │
         └───────────────┬──────────────────────┘
                         ▼
             [Conflict Detection Engine]
             Discrepancy: Δ = 50 g (10%)
                         │
                         ▼
        [Flag: CROSS_PANEL_CONTRADICTION]
        Verdict: REVIEW / POTENTIAL_DECEPTIVE_PACKAGING
        Evidence: Side-by-side visual crop comparison
```

### Monitored Cross-Panel Fields:
1. **Net Quantity Discrepancy:** Differences between front hero callout and technical declaration.
2. **MRP Discrepancy:** Multiple prices declared on carton vs. closure cap without clear statutory authorization.
3. **Date Discrepancy:** Manufacturing date on outer box post-dating expiry/best-before date on inner pouch.

---

## 2. Regulatory Source Conflict Policy

If two official documents offer competing interpretations without explicit statutory repeal language:
- The system **NEVER** guesses or prompts an LLM to resolve the ambiguity.
- The rule status is set to: `CONFLICTING`.
- Implementation status is set to: `BLOCKED`.
- The issue is escalated to the legal review backlog in `docs/14_SUBMISSION/LEGAL_VERIFICATION_BACKLOG.md`.
