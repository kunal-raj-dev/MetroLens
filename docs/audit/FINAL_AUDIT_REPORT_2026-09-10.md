# MetroLens local launch audit and remediation

Audit period: 8–10 September 2026. Repository: `kunal-raj-dev/MetroLens`. Baseline: `c436e3a7055b8f048018727df3ee3b34d0311bf1`. Work branch: `codex/launch-audit`.

Audit status: local remediation, automated checks and this report are complete. Final production-browser acceptance is blocked as described below. The report records the tested code and its limits; repository publication does not establish successful deployment or full PRD acceptance. See the [report index and next steps](README.md) for publication context.

## Overall assessment

The original public presentation overstated a partially implemented prototype. The most serious problems were unsafe evidence paths, unprotected or fabricated operational responses, invented OCR/compliance fallbacks, and unsafe dynamic PDF markup. These paths have been corrected locally and covered by regression checks.

The revised application is a single-image screening prototype for a trusted group. It can run actual local OCR, preserve uploaded evidence hashes, show uncertain results for human review, and generate a preliminary report. It is **not ready to be represented as a complete officer enforcement system or a fully delivered PRD**.

The initial audit was verified locally at the user's request because the deployed API host and Netlify production branch were unknown. The user subsequently authorized publishing the fixes to `main`. Production deployment and the exact hosted browser/API flow remain unverified; a repository push may trigger Netlify continuous deployment.

## Findings and fixes

Severity reflects the original reachable behavior under its deployment assumptions; it is not a formal CVSS score. Related issues are grouped to avoid counting one root cause repeatedly.

| Priority | Original issue and impact | Local correction | Verification |
| --- | --- | --- | --- |
| High | Caller-controlled inspection IDs reached evidence paths and expiration cleanup outside the spool. | Strict IDs, resolved-path containment, Windows device/reparse/junction checks, and validation on every read/write/delete and cached-path use. | Isolated traversal and symlink/junction regression tests; never tested destructive inputs against production. |
| High | Operational routes lacked reliable access control and ownership checks. Caller-supplied roles could obtain an officer token; a known fallback signing secret existed. | Strong configured service access required; retained records bound to the service principal; public officer-token issuance disabled; known signing-secret fallback removed. | Unauthorized, wrong-key, absent-configuration, record ownership, and token tests. This remains group access, not individual officer RBAC. |
| High | Missing/failed OCR and caller-selected live fixtures could produce invented declarations or apparently successful assessments. Unknown records and structured submissions could fabricate results. | Only real OCR contributes evidence; quality rejection precedes OCR; unavailable/failed/empty inference fails explicitly; only generated retained records are retrievable. | API regressions and a real-model local specimen run. |
| High | PDFs interpreted uploaded text as ReportLab markup, allowing unintended resource loading. | Central escaping and safe scalar conversion across reporting templates; bounded note input and a verified sanitized reference image. | Network/local-image payload traps with positive controls across report generators, plus normal rendering tests. |
| High | Image requests could allocate excessive memory before validation; a request header bypassed throttling and forwarded-address headers could spoof clients. | Pre-parse request cap, decoded-image dimension/pixel caps, one inference slot, no public bypass header, bounded limiter state, and disabled automatic proxy-header trust in local/container launch. | Oversize/malformed requests, image headers, burst limits, concurrency and spoofing regressions. Hosting still needs connection/resource quotas. |
| High | Reports and audit responses asserted verification without a genuine retained assessment; sanitized image bytes were labelled as original evidence. | Separate raw/sanitized bytes and hashes, genuine-record binding, tamper rejection, actual retained-file hash checks, and removal of simulated affidavit/portal success. | Original-hash, tamper, missing/expired record and report-binding checks; local specimen hashes matched. |
| Medium | Zero/negative quantities could establish exemptions; unknown geometry, weak OCR and absent text on a single panel could produce unjustified conclusions. A unit sale price was also being parsed as MRP. | Positive quantity guard, authoritative REVIEW propagation, conservative historical USP handling, low-confidence review and single-panel uncertainty. Fabricated PDP/glyph measurements removed. MRP extraction now requires an explicit English/Hindi MRP label. | Rule and API regressions for invalid quantities, missing measurements, weak OCR exemptions, incomplete panel evidence and unit-price/MRP separation. |
| Medium | Frontend showed a compliant idle result, mixed demonstrations with live uploads, invented confidence, treated crop labels as recognized text and advertised unsupported authority. | Honest empty state; explicit synthetic/live modes; actual OCR observations; unknown confidence shown as unavailable; unsupported certification/government claims removed; uncertain states preserved. | Frontend contract checks and browser inspection. |
| Medium | Reset/mode changes could leave stale uploads, review results or PDF downloads active. Dialog focus and mobile typography had defects. | Abort/generation guards, real disabled states, dialog focus/escape handling, responsive layout, local system fonts and reduced-motion support. | Frontend asynchronous-boundary tests and local UI checks. |
| Medium | Report notes and image option did nothing. An unused batch helper used the removed fixture argument, converted review/exempt outcomes to violations and invented penalties. | Reports include labelled unverified notes and optional sanitized reference; batch preserves outcome categories, omits invented penalties and bounds exact ZIP-member reads. | Reporting tests and 22 batch regressions. Batch remains unmounted. |
| Medium | Vulnerable dependencies and inconsistent deployment instructions increased launch risk. | Updated/pinned Python and web dependencies, reproducible web lockfile, explicit API configuration, security headers/CSP, Node 22 container/CI settings and root Netlify configuration. | Dependency advisory audits, frontend build/type/lint checks and dependency compatibility check. Container and hosted deployment not executed. |
| Low | Broken specification links and historical documents claimed authority over obsolete behavior. | Current API contract added, old contract marked historical, scope/test links corrected, README/security/deployment notes aligned with implementation. | Document-link and repository governance verification. |

## Verification evidence

The final CI-equivalent backend selection plus API smoke tests passed **882 tests with no skips**, two dependency deprecation warnings, in 69.57 seconds. Component counts below overlap and must not be added together as distinct tests.

The run used isolated spool/TEMP/TMP directories and one native-library worker via `OPENCV_FOR_THREADS_NUM`, `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` and `MKL_NUM_THREADS`. A preceding run encountered Windows WMI/OpenCV native exceptions and cascading failures (135 failed, 744 passed, 3 errors). After releasing the local OCR server and limiting native worker threads, the same selection passed without suppressing or skipping tests. These thread limits are documented in the README and CI. Logs remain under `.venv/full-suite/`.

- Frontend: all seven configured test scripts pass, including 27 launch-boundary checks. TypeScript checking and lint pass. The production build succeeds with a local API URL for testing.
- Reporting: 43 tests passed in the report-specific run (29 security-focused and 14 existing checks); see [report validation](REPORT_VALIDATION_2026-09-10.md) for the details and limits.
- Rules/storage/batch: a combined run passed 260 tests; 23 targeted tests passed after the final batch and shared-mapping correction. Two dependency deprecation warnings remain.
- Supplementary system/scenario coverage: 59 checks passed (17 API/component and 42 distinct packaging scenarios). These inject OCR/quality outputs into the real downstream flow; they are not camera or OCR accuracy benchmarks. The unchanged legacy helper/worker cases passed in the preceding supplementary run.
- Dependencies: npm reported zero known advisories; the final installed Python dependency audit reported zero known advisories, and `pip check` passed. These are advisory-database results, not proof that dependencies contain no vulnerabilities.
- Five repository governance scripts passed unchanged. They validate structure and honest status declarations; they do not authenticate every law or establish physical accuracy.

Browser inspection confirmed the empty state, explicit demonstration mode, sample selection, demo assessment, disabled demo reports, review-dialog entry and live service-access form. At a 390 × 844 viewport there was no page-wide horizontal overflow; inspected internal navigation links resolved. The old custom-font variable was found to produce fallback typography and replaced with a local system-font stack. Automated approval review blocked starting the final production web server (`npm run start -- --hostname 127.0.0.1`) with only “blocked by policy,” so the final production browser upload/download and keyboard pass could not be completed. The optional historical Python Playwright suite was not executed; it requires separate browser tooling. This limitation does not negate the real API/PDF check below, but it prevents claiming full browser acceptance.

### Actual OCR → inspection → integrity check → PDF

Used the existing repository photograph `data/real_world/dairy_milk_bubbly/back_flat_01.jpg` (3072 × 4080), actual local models, and the loopback API. No mock OCR injection or production upload was used for this check.

| Check | Observed result |
| --- | --- |
| Inspect response | HTTP 200; `MANUAL_REVIEW_REQUIRED`; 30 actual OCR observations |
| Raw image digest | Matched SHA-256 of the uploaded original bytes |
| Retained raw and sanitized integrity | Both matched; API explicitly declined signature, officer identity and legal admissibility certification |
| PDF | HTTP 200; valid PDF header; 161,852 bytes |
| Observed timing | 5.657 seconds for inspection; 0.892 seconds for PDF |

This establishes one functioning local path, not language accuracy, package completeness, physical measurement accuracy, or a representative latency percentile. Machine load, model warm-up and image choice affect timing. Local test artifacts are in ignored `.venv/local-acceptance/`.

After the final backend corrections, the same specimen was tested again through the in-process HTTP test client with actual OCR models and isolated storage. It again returned 30 observations, `MANUAL_REVIEW_REQUIRED`, matching original/sanitized hashes and a valid PDF (161,758 bytes). Inspection took 5.809 seconds and PDF generation 0.555 seconds. This second run verifies the final backend code without opening another server; artifacts are in `.venv/local-acceptance-final/`.

## PRD and project scope alignment

The full requirement-by-requirement assessment is in [the scope matrix](SCOPE_ALIGNMENT_2026-09-09.md). The project aligns with its core theme—image-assisted packaging screening—but substantive requested capabilities remain partial or absent:

1. Guided multi-panel capture and reconciliation are absent; the active API assesses one image.
2. Automated package area and numeral glyph-height measurement are absent. A reference scale does not establish either measurement.
3. Historical, source-driven legal rule activation is incomplete. Source records remain partially verified, and conflicting references must be reconciled against primary sources.
4. Individual officer accounts, roles, durable review history, restart-safe inspection records, digital signing and trusted timestamps are absent.
5. A complete immutable evidence graph and portable, independently verifiable dossier are incomplete.
6. Representative physical packaging data, caliper ground truth, OCR accuracy and latency benchmarks are missing or explicitly blocked in repository records.
7. Government portal integration and official enforcement are not implemented; the revised UI and API now say so.

These are implementation/data prerequisites, not issues that can be honestly fixed by changing badges or marking manifests “verified.” No PRD-completion percentage is asserted without agreed acceptance weights and evidence.

## Remaining launch conditions and limits

For a demonstration, deploy the revised web build with an empty API URL so only clearly labelled synthetic examples are available. For a trusted-group pilot, deploy the Python API separately over HTTPS, set a strong private service key, restrict origins, use private bounded storage and one API worker, then test that exact hosted build and its error paths.

Before use as an operational officer system, complete the missing identity/persistence/review capabilities and verify the legal and physical measurement requirements above. Original images can contain location metadata and storage is not encrypted by this application. Hashes detect changes relative to this process; they do not establish who photographed a product or an external chain of custody.

This was a source review, local regression exercise and UI audit. It did not establish cloud-account configuration, production secrets/permissions, container execution, external penetration-test coverage, binary/model supply-chain integrity, all unused legacy subsystems, or exhaustive vulnerability absence. The [security finding draft](SECURITY_SCAN_DRAFT_2026-09-10.json) contains eight consolidated baseline findings with 25 exact source excerpts and partial coverage. Native scan tools became unavailable before canonical completion, so it remains explicitly unsealed; this report does not imply a sealed scan or a clean bill of health.
