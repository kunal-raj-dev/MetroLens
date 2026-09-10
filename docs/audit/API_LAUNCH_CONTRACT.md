# Current launch API contract (audit remediation)

This implementation note supersedes conflicting claims in older draft contracts. The generated FastAPI schema remains the field-level reference.

The machine-readable schema is available at `/openapi.json`. The CDN-dependent Swagger/ReDoc pages are disabled because the API's security policy allows only same-origin scripts. The service limiter retains at most 4096 peer buckets and fails closed for new peers while at capacity.

| Request | Current behavior |
| --- | --- |
| GET /health and /api/v1/health | Public minimal reachability; no unverified model or host-health claims. |
| POST /api/v1/inspect | Bearer service key; multipart `file` exactly once, optional `anchor_type` and `panel_type`. No fixtures in the live API. |
| GET /api/v1/inspections/{id} | Bearer service key; returns only retained completed records, 404 if unavailable. |
| POST /api/v1/report/pdf | Bearer service key; genuine retained result and matching image hashes required; preliminary PDF. |
| GET /api/v1/audit/verify/{id} | Bearer service key; actual retained image integrity checks, not legal certification. |
| GET /metrics | Bearer service key. |
| POST /api/v1/auth/token | 501: officer authentication is not implemented. |
| POST /api/v1/inspections | 501: fabricated structured inspection creation is unavailable. |
| POST /api/v1/audit/affidavit | 501: legal certification is not implemented. |
| POST /api/v1/emaap/mock-sync | 501: national portal synchronization is not implemented. |

Image limits: 16 MiB total request, 15 MiB image, 40 million pixels, 8000 pixels per side, minimum 800 × 600 after EXIF orientation. Quality or empty-text failures return 422; unavailable OCR returns 503. Missing/incorrect access returns 401/403, missing key configuration returns 503. Excess requests or a busy inference slot return 429. Tampered retained evidence returns 409 when generating a report.

`font_height_audit.status` and `usp_audit.status` carry `PASS`, `FAIL`, `REVIEW`, or `NOT_APPLICABLE`. Consumers must preserve these statuses rather than derive a verdict from `is_compliant`. A photographed panel is not proof of whole-package compliance or missing declarations elsewhere. Statutory action needs human and source verification.

The current store is per process (128 records / one hour), and one shared service principal owns all records created with its key. Changing the key makes earlier records inaccessible. Use a single API worker. This is not a multi-user evidence-management system.
