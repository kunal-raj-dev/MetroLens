# Nirikshak Worker Service (`apps/worker`)

## Purpose
Orchestrates the multi-stage asynchronous inspection pipeline (Quality Gate -> Calibration -> OCR -> Extraction -> Measurement -> Rule Evaluation -> Evidence DAG -> Dossier Generation).

## Owner
Pipeline / Integration Lead

## Pipeline Flow
Consumes `InspectionRequest` tasks, invokes package APIs through their typed interfaces, constructs the immutable `InspectionResult`, and persists results to storage and the PostgreSQL database.
