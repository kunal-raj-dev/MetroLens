# Technical Feasibility & Field Deployability Case

## Purpose
Demonstrates that Nirikshak is technically feasible, operates reliably within field hardware constraints, and does not depend on unrealistic connectivity or expensive specialized sensors.

## Scope
Covers compute resource consumption, hardware requirements, offline resilience, and operational cost.

## Authoritative Inputs
- Hardware specifications of standard government-issued enforcement tablets and field laptops.

## Assumptions
- Systems must run without external cloud GPUs or high-bandwidth 5G connections.

## Dependencies
- `apps/`
- `infra/docker/`

## Verification Requirements
- End-to-end execution must succeed on standard 4-core / 8-core CPU hardware without discrete GPU.

---

## Engineering Feasibility Highlights

1. **CPU-Optimized Inference:**
   - Neural models quantized to INT8 / FP16 via ONNX Runtime and OpenVINO.
   - Total model weight footprint $< 120\text{ MB}$, fitting comfortably into mobile flash memory.

2. **Zero Cloud Lock-In & Offline Autonomy:**
   - Complete pipeline runs locally on `localhost:8000`.
   - Inspection records stored in local SQLite database with AES-256 encryption.
   - Zero dependence on commercial pay-per-call cloud OCR APIs (Google Cloud Vision, AWS Rekognition).

3. **Ultra-Low Incremental Deployment Cost:**
   - Requires no expensive stereoscopic LIDAR or 3D laser scanners ($> ₹5,00,000$).
   - Uses standard smartphone camera optics paired with standardized physical reference stickers costing $< ₹0.10$.
