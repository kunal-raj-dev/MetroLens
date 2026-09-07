# MetroLens Current System Map

**Audited:** September 2026  
**Architecture:** Multi-Package Monorepo with FastAPI + Next.js  

---

## 1. Directory & Package Layout

```
MetroLens/
├── apps/
│   ├── api/                           # FastAPI Application Gateway (Port 8000)
│   │   ├── main.py                    # App entrypoint, CORS, lifespan
│   │   ├── routes/
│   │   │   ├── health.py              # Health check (/health)
│   │   │   ├── inspect.py             # Main inspection pipeline (/api/v1/inspect)
│   │   │   └── report.py              # PDF Dossier generation (/api/v1/report/pdf)
│   │   ├── middleware/                # Rate limiting, security headers
│   │   └── schemas/                   # Pydantic v2 request/response envelopes
│   └── web/                           # Next.js 16 Web Application (Port 3000)
│       ├── src/
│       │   ├── app/                   # App Router pages & layout
│       │   ├── components/            # React 19 UI components (Canvas, Dashboard)
│       │   ├── lib/api/               # Live & Mock API Adapters, normalizers
│       │   └── types/                 # TypeScript interfaces
│       └── tests/                     # 174 Vitest test suites
├── packages/
│   ├── calibration/                   # Member 2: Optical metric scale recovery
│   ├── evidence/                      # Member 4: SHA-256 evidence hashing
│   ├── extraction/                    # Member 1/3: Text field extraction & regex
│   ├── measurement/                   # Member 2: Metric dimension math
│   ├── ocr/                           # Member 1: RapidOCR ONNX inference engine
│   ├── reporting/                     # Member 4: ReportLab PDF dossier generator
│   ├── rules-engine/                  # Member 3: Legal Metrology (PCR 2011) rules
│   ├── shared/                        # Common contracts & Pydantic domain models
│   └── vision/                        # Member 2: OpenCV blur gate & transforms
├── data/
│   ├── real_world/                    # Dairy Milk Bubbly packaging specimen
│   └── synthetic/                     # SYNTH-01 to 08 regression specimens
├── tests/
│   ├── contracts/                     # 12 Cross-Member Contract Tests
│   ├── e2e/                           # 15 System E2E & 3 Playwright Browser Tests
│   └── integration/                   # Legacy vertical slice integration tests
└── docs/                              # Project charter, legal research, and audits
```

---

## 2. Port & Communication Map

| Port | Service | Protocol | Payload Type | Authentication / Access |
| :--- | :--- | :--- | :--- | :--- |
| **8000** | FastAPI API Gateway | HTTP/1.1 REST | JSON, multipart/form-data, application/pdf | Rate-limited (Token bucket) |
| **3000** | Next.js Frontend | HTTP/1.1 HTML/JS | React 19 Server/Client Components | Public Localhost |
