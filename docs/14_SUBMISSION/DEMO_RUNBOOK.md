# Final Demonstration Runbook & Jury Presentation Guide

## Purpose
Provides the comprehensive operations manual for staging, booting, executing, and defending the Nirikshak live demonstration before hackathon judges.

## Scope
Covers terminal commands, pre-flight environment checks, physical package staging, and contingency fallbacks.

---

## 1. Pre-Flight Setup Checklist (T-Minus 15 Minutes)

1. **Hardware & Power:**
   - Demonstration laptop connected to power adapter.
   - External phone/webcam connected via USB with autofocus enabled.
2. **Physical Package Staging:**
   - Test Package A: Compliant rectangular carton (Biscuit box).
   - Test Package B: Non-compliant small font carton (Spice box).
   - Calibrated circular reference cards ($25.0\text{ mm}$ standard).
3. **Local Service Boot:**
   ```bash
   # Terminal 1: Database & Storage
   docker-compose up -d db

   # Terminal 2: API Service
   python -m uvicorn apps.api.main:app --host 0.0.0.0 --port 8000

   # Terminal 3: Web UI
   npm --prefix apps/web run dev
   ```
4. **Offline Mode Demonstration Readiness:**
   - Disable WiFi / Ethernet interface to demonstrate $100\%$ local execution.
   - Verify `localhost:3000` loads properly.

---

## 2. Live Demo Script Execution
Refer to `docs/11_JUDGING/DEMO_SCRIPT.md` for the exact minute-by-minute narrative and action cues.
