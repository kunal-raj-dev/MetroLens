# Reporting validation — 10 September 2026

This report covers the local reporting fixes on `codex/launch-audit`. It is a focused supplement to the launch audit, not a certification of the entire application or deployed site.

## Verified outcome

The PDF API renders a retained assessment for the authenticated service principal. It compares retained original and sanitized evidence against ingestion digests before producing a report. Unknown or expired records do not produce sample reports. PDFs describe themselves as unsigned preliminary drafts, do not invent an officer identity or ruleset version, and distinguish unverified annotations from assessment findings.

Two additional contract defects were corrected: `officer_notes` is now rendered as literal text with a 2,000-character limit, and `include_raw_image` now includes a resized **sanitized reference copy** of the actual retained packaging image. The legacy field name does not mean original metadata is embedded. The digest still refers to the original uploaded bytes. The reference read is bounded to its recorded length and its digest is checked again after reading. Setting the option to false omits the reference image and evidence crops.

## Findings corrected

| Issue | Corrected behavior |
| --- | --- |
| Dynamic ReportLab markup could interpret image tags in OCR, filenames or supplied officer fields | Text is escaped through `text_safety.py`; source templates retain intentional formatting |
| Numeric, boolean, list and dictionary rule values caused rendering failures, while zero/false became missing values | Values are converted to text without discarding zero or false |
| Uncalibrated results could imply physical measurements | Missing calibration and PDP values remain explicitly uncalibrated |
| An uncertain result badge asserted a statutory deviation | The PDF says manual review is required |
| Default officer jurisdiction, fixed ruleset version, certification and penalty claims | Defaults are unverified/not recorded; drafts do not issue deadlines, penalties, certificates or notices |
| Header text overlapped and canvas geometry assumed Letter everywhere | One clear running header and page-size-aware decorations |
| Report notes and requested packaging thumbnail were silently omitted | Bounded plain-text notes and verified sanitized thumbnail are included when requested |
| Unused Windows platform probing inside affidavit generation | Removed unnecessary machine probing |

## Validation evidence

Executed using the local Python 3.12 virtual environment:

```
python -m pytest tests/security/test_report_text_safety.py tests/integration/test_pdf_generation.py tests/integration/test_reporting_advanced.py tests/unit/test_advanced_reporting.py -q --disable-warnings
```

Result: **43 passed** (29 security regressions and 14 existing reporting tests). The security tests replace ReportLab's actual inline-image loader with a trap; a positive control proves an unsafe paragraph reaches that loader. HTTP and local-file image tags are passed through all six PDF compilers, and remain literal without resource loading. Tests also inspect generated PDF image objects, verify optional thumbnail inclusion, verify draft notices and absence of signature objects, exercise null calibration and non-string values, and confirm annotations cannot change assessment findings.

A synthetic two-page report was generated, parsed with pypdf, rendered with PDFium and both page images visually inspected. The package thumbnail, literal injection text, draft notice, zero numeric value and uncalibrated state were present; running headers and footers were readable without overlap. This visual check exposed the uncertain-state badge wording, which was then corrected and covered by three additional regressions. Synthetic rendering artifacts are local and ignored by Git under `benchmarks/runs/report-validation/`.

The original markup review covered 271 paragraph sites and 93 literal formatting templates with no unescaped dynamic inputs left. Later notes/reference additions use escaped notes and a static image label. Formatting checks passed for the changed files. API access/retention/tamper and option-forwarding assertions are maintained separately in `tests/security/test_launch_api.py`; the API owner separately verified that notes are forwarded, reference bytes match the sanitized evidence, the false option passes no reference, and oversized notes return the registered HTTP 400 validation envelope. The whole-application audit records the final combined run.

## Limits

- No live Python API host was provided, and this validation did not deploy or test a production PDF endpoint.
- A service access key identifies a trusted service operator, not an individually verified officer. The PDF does not authenticate an officer or jurisdiction.
- A local hash comparison is not proof of origin, an unbroken custody chain, a digital signature, or legal admissibility.
- Legacy digital-signature simulation and advanced document helpers remain library-only; real CMS signatures, trusted timestamps, officer approval, government synchronization and legal certification are not implemented by these changes.
- Rule citations, legal correctness and OCR accuracy across a representative real-world dataset require separate validation. Rendering tests do not validate those claims.
- Some historical repository documents contain aspirational contracts; current launch behavior and the overall audit take precedence.

Reviewed implementation: `apps/api/routes/report.py`, `apps/api/schemas.py` (report request only), `apps/api/services/inspection_store.py`, and `packages/reporting/src/nirikshak_reporting/`. Regression tests: `tests/security/test_report_text_safety.py`.
