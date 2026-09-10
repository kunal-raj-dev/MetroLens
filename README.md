# MetroLens — image-based packaging assessment prototype

MetroLens assists review of visible packaging declarations using local CPU OCR, image quality checks, declaration parsing, and rule calculations. It is an independent SIH26034 project prototype. It does not certify legal compliance, authenticate government officers, issue statutory notices, or synchronize with a government portal.

The web application is **Next.js 15 / React 18**; the API is **FastAPI on Python 3.12**. The default web experience uses clearly labeled prepared demonstration examples. Live inspection requires a separately running API and a service access key.

## Current capabilities and limits

- One JPEG, PNG, or WebP image per inspection: up to 15 MiB, 40 megapixels, 8000 pixels on either side, minimum 800 × 600 after orientation.
- Quality rejection occurs before OCR. Missing models, failed OCR, and empty results return errors rather than invented declarations.
- OCR and reference scale estimates are preliminary. The current pipeline does not establish package PDP area or numeral glyph height; those checks require manual review.
- Reports use a retained assessment and original image hash. They are preliminary reports, without a digital signature or verified officer identity.
- One configured service key grants access to a trusted group; individual accounts and per-officer authorization are not implemented.
- Original and sanitized images are retained temporarily. Original images may contain location metadata. Storage is not encrypted by this application. Inspection records expire after one hour, earlier on eviction or restart; disk cleanup is periodic.
- Multi-panel aggregation, camera capture, persistent officer review, historical rule selection, certified accuracy, and production benchmarks remain incomplete. See the [scope audit](docs/audit/SCOPE_ALIGNMENT_2026-09-09.md).

## Run locally

Install Python 3.12 and Node.js 22 LTS. From the repository root:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install -r requirements.txt
$env:METROLENS_API_KEY = (.venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(48))")
$env:METROLENS_SPOOL_DIR = Join-Path (Get-Location) '.venv/local-spool'
$env:PYTHONPATH = (Get-Content pytest.ini | Where-Object { $_ -match '^    ' } | ForEach-Object { $_.Trim() }) -join ';'
.venv/Scripts/python.exe -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --no-proxy-headers
```

In another terminal:

```powershell
cd apps/web
npm ci
npm run dev -- --hostname 127.0.0.1
```

Open `http://localhost:3000`. Select **Live Inspection** and enter your local service key. Keep it private; never store it in a `NEXT_PUBLIC_*` variable. A health response confirms reachability only; authorization is checked on operational requests.

Models are loaded from `models/weights/ocr` by default. `METROLENS_MODELS_DIR` can point to a different model root. Missing or invalid model files fail closed. Public HTTPS hosting must use an HTTPS API URL.

Docker users can copy `.env.example` to `.env`, set a strong private `METROLENS_API_KEY`, and run `docker compose up --build`. This is a local, single-process setup. The previous unused PostgreSQL container and misleading storage settings have been removed.

## Tests

```powershell
$env:OPENCV_FOR_THREADS_NUM = '1'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
.venv/Scripts/python.exe -m pytest tests/unit tests/integration tests/rules tests/contracts tests/security tests/benchmarks packages -q
cd apps/web
npm test
npm run typecheck
npm run lint
npm run build
npm audit
```

Use a dedicated `METROLENS_SPOOL_DIR` for tests. Browser workflows are verified separately; the historical Python Playwright test needs its own optional environment. Passing structural legal-source checks is not proof that all sources or statutory interpretations are verified.

## Deployment

`netlify.toml` builds `apps/web`. Set `NEXT_PUBLIC_API_URL` **before the web build** to the separate API's HTTPS URL; leave it empty for a demo-only hosted site. Do not publish a development server or place service secrets in web build variables. Set `METROLENS_API_KEY`, explicit `METROLENS_CORS_ORIGINS`, and a private spool directory on the API host. Use one API worker while inspection records and limits are in process memory.

A production launch additionally requires deployment-level TLS, resource and request limits, private storage permissions, authenticated operator accounts if needed, verified rule sources, and measured real-package evaluation. Local fixes do not update an existing Netlify deployment automatically.

## Specifications

The original product goals remain in [PRODUCT_BLUEPRINT.md](docs/PRODUCT_BLUEPRINT.md), [MVP_SCOPE.md](docs/00_PROJECT_CHARTER/MVP_SCOPE.md), and [SCOPE.md](docs/00_PROJECT_CHARTER/SCOPE.md). They describe intended capabilities; use the audit and [current API notes](docs/audit/API_LAUNCH_CONTRACT.md) for implementation status and changed security behavior.
