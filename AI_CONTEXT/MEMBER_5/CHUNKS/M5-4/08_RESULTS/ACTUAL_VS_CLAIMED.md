# METROLENS AI — MEMBER 5 (CHUNK M5-4)
## Actual vs. Claimed Audit Matrix

| Item / Requirement | Claimed in Spec | Actual Verified State | Verification Method | Status |
|---|---|---|---|---|
| **Declaration Table View** | Desktop semantic table + mobile card stack | `DeclarationTable.tsx` implemented with both responsive views | Browser DOM inspection & automated tests | **MATCH** |
| **Mandatory Rule 6 Fields** | Render all 5 mandatory fields (MRP, Net Qty, USP, Date, Contact) | All 5 fields rendered with verbatim observed OCR text, badges, confidence | Browser snapshot & `m5_4_declaration_review.test.ts` | **MATCH** |
| **Evidence Linking** | Row click / "Canvas" click locates token on Evidence Canvas | Clicking "Canvas" highlights token with Royal Blue outline and centers viewport | Browser DevTools script & test suite | **MATCH** |
| **Multi-Token Grouping** | Bounding box union for multi-token declarations | `focusTokensUnion` calculates bounding rect + 40px margin | `EvidenceCanvas.tsx` implementation & test | **MATCH** |
| **Confidence Semantics** | Clearly labeled as Model / Extraction Confidence | Labeled as "CONFIDENCE" with percentage, disclaiming legal certainty | Visual inspection & component code | **MATCH** |
| **Missing Measurements** | Render "Not measured" / "N/A" without NaN or crash | `measuredHeightMm === null` safely renders "N/A" | Automated test & table DOM check | **MATCH** |
| **Unknown Legal Verdict** | Fallback to `INCONCLUSIVE` / `requiresReview` | `normalizeVerdict` maps unknown to `INCONCLUSIVE` | Automated test 7 | **MATCH** |
| **Review Workflow Modal** | Accessible modal answering 4 core inspection questions | `InspectorReviewModal.tsx` handles What, Why, Evidence, and Actions | Browser DevTools snapshot & test suite | **MATCH** |
| **Review Notes Validation** | 500 character limit with live counter | Textarea bounded at 500 chars with live counter; adapter rejects > 500 | Browser verification & test 9 | **MATCH** |
| **Backend Review Seam** | Honest handling of Member 4 pending endpoint | LiveAdapter returns `REVIEW_API_NOT_IMPLEMENTED`; MockAdapter simulates labeled synthetic demo | Tested in `m5_4_declaration_review.test.ts` | **MATCH** |
| **Manual Caliper Tool** | Two-point reference lines mapped to original image pixels | Toggled on canvas; points mapped via `canvasToImage`; displays optical distance | Browser DevTools point simulation & test 11 | **MATCH** |
| **Caliper Validation** | Reject duplicate clicks / < 2px distance | Distance < 2px rejected; out-of-bounds clamped | Tested in automated test 12 | **MATCH** |
| **Zero Client Legal Logic** | No client-side threshold or verdict calculations | Client purely renders backend verdicts | Architecture audit & tests 16-17 | **MATCH** |
| **Zero Client mm Math** | No client-side font height mm calculation | Only optical pixel distance reported on unscaled image | Architecture audit & tests 11, 17 | **MATCH** |
| **Git Safety** | NO git commit, NO git push, NO git add/reset/clean/stash | 0 git mutating commands run during session | Execution log audit | **MATCH** |
