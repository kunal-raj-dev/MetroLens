# Learning & Audit Module 1: Project Reality vs. Blueprint
**Generated On:** 2026-09-05 15:25:25 IST

---

## 1. Core Learning: The "Scaffold Illusion"
The most significant learning from Audit Module 1 is distinguishing between **Architectural Intent** and **Implementation Reality**. 

MetroLens AI has an extraordinarily robust, forward-looking architectural blueprint (over 30 documents outlining everything from statutory legal matrices to complex eMaap syncs). However, developers joining or reviewing the project must learn to recognize that **documentation of a feature does not mean the feature is coded**.

* **The Reality:** The system currently possesses a highly engineered, production-ready OCR text extraction engine. Everything else—the backend API, the web UI, the legal rule engine, the calibration computer vision—is a **hollow scaffold** (empty functions returning mocked Success responses).

## 2. Key Audit Discoveries
1. **The OCR is Hardened:** Member 1 has successfully packaged a direct ONNX inference engine (packages/ocr) that parses English and Devanagari Hindi text from images, entirely offline, using the CPU. It handles errors cleanly and routes scripts perfectly.
2. **The Pipeline is Broken By Design (Currently):** If you send an image to the FastAPI backend today, it will instantly return a fake "Compliant" PDF. The backend is not yet wired to the OCR engine.
3. **The Data Blockade (Path B):** There is not a single real photograph of an Indian retail package in the repository. The AI has been trained and benchmarked strictly on 8 synthetic test images. 
4. **The Legal Vacuum:** While the repository contains 74 authentic Indian Legal Metrology PDFs, the Python code that actually enforces these rules (packages/rules-engine) only has one placeholder function checking for an "MRP".

## 3. Engineering Operating Principles (Moving Forward)

To prevent further divergence between the documentation and the codebase, the team must adopt the following learnings immediately:

### A. Halt "Future State" Documentation
Do not write any more Architecture Decision Records (ADRs) or Master Blueprints for features that are more than 2 weeks out. The documentation is currently 10 steps ahead of the code, causing massive context bloat.

### B. Shift from Mock to Wire
The immediate engineering priority is not to add new features, but to connect the existing ones. The FastAPI endpoint must be wired to actually invoke the OCRService, even if the downstream Rules Engine still returns mocked data.

### C. Break the Data Blockade
No further optimization of the OCR should occur until **real physical packaging data** is captured. The system's robustness is currently a synthetic illusion.

## 4. Current State Subsystem Checklist
When assessing what to work on next, use this verified reality-check:

- [x] **OCR Subsystem:** IMPLEMENTED & TESTED
- [x] **Legal Research:** SOURCED & ARCHIVED
- [ ] **Computer Vision (Calibration):** EMPTY SCAFFOLD
- [ ] **Legal Rule Engine:** EMPTY SCAFFOLD
- [ ] **Backend API:** EMPTY SCAFFOLD (MOCKED)
- [ ] **Frontend UI:** EMPTY SCAFFOLD (STATIC)
- [ ] **Physical Dataset:** 0 IMAGES

## 5. Next Immediate Actions
1. **Member 6:** Take 35 physical photographs of retail packages (with a 10-Rupee coin for scale) and commit them to data/raw/real/.
2. **Member 2:** Implement the OpenCV logic to detect the 10-Rupee coin and calculate pixels-to-millimeters in packages/calibration.
3. **Member 3:** Write the Python logic to parse the ules/*.yaml files and execute real compliance checks against the OCR text.
