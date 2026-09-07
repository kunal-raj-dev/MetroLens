# MetroLens System Reproducibility & Execution Runbook

**Environment:** Windows 11 Enterprise (AMD64), Python 3.14.3, Node v25.6.1  
**Verification Date:** September 2026  

---

## 1. Prerequisites & Environment Setup

### 1.1 Python Environment
Ensure Python 3.11+ is installed. All packages in `packages/` must be installed in editable mode:
```powershell
# Install dependencies and editable monorepo packages
python -m pip install -e packages/shared
python -m pip install -e packages/vision
python -m pip install -e packages/calibration
python -m pip install -e packages/measurement
python -m pip install -e packages/ocr
python -m pip install -e packages/extraction
python -m pip install -e packages/rules-engine
python -m pip install -e packages/evidence
python -m pip install -e packages/reporting
python -m pip install -e apps/api

# Ensure runtime dependencies
python -m pip install qrcode playwright pytest pytest-asyncio
playwright install chromium
```

### 1.2 Frontend Environment
Ensure Node.js v20+ is installed:
```powershell
cd apps/web
npm install
```

---

## 2. Running Automated Verification Suites

### 2.1 Complete Python Monorepo Suite (807 Tests)
```powershell
python -m pytest
```

### 2.2 Cross-Member Contract Test Suite (12 Tests)
```powershell
python -m pytest tests/contracts/test_cross_member_contracts.py -v
```

### 2.3 System E2E Integration Suite (15 Tests)
```powershell
python -m pytest tests/e2e/test_system_integration.py -v
```

### 2.4 Browser Automation Workflow Suite (3 Tests)
Ensure Next.js is running on port 3000:
```powershell
python -m pytest tests/e2e/test_browser_workflow.py -v
```

### 2.5 Frontend Unit & Component Tests (174 Tests)
```powershell
cd apps/web
npm run test
```

---

## 3. Starting Local Development Servers

### 3.1 FastAPI API Gateway (Port 8000)
```powershell
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

### 3.2 Next.js Web Application (Port 3000)
```powershell
cd apps/web
npm run dev
```

Navigate to `http://localhost:3000` to interact with the Sovereign Inspector Dashboard.
