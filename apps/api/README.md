# Nirikshak API Service (`apps/api`)

## Purpose
Provides the core REST API backend for ingesting inspection requests, querying inspection status, retrieving cryptographic dossiers, and managing officer reviews.

## Owner
Backend / Infra Lead

## Key Endpoints
- `GET /health` — Service health and readiness probe.
- `POST /api/v1/inspections` — Ingest new inspection image frame.
- `GET /api/v1/inspections/{inspection_id}` — Retrieve inspection result, evidence chain, and verdict.
- `GET /api/v1/inspections/{inspection_id}/dossier` — Download signed inspection dossier PDF.
