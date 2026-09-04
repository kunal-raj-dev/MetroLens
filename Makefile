.PHONY: help verify verify-legal verify-rules verify-claims verify-datasets verify-integrity lint test test-unit docker-up docker-down

PYTHON ?= python

help:
	@echo "Nirikshak Build & Verification Automation"
	@echo "----------------------------------------"
	@echo "make verify           : Run all anti-hallucination verification scripts & integrity audit"
	@echo "make verify-legal     : Verify legal source records, hashes, and dates"
	@echo "make verify-rules     : Verify machine-readable rule schemas and provenance"
	@echo "make verify-claims    : Verify claims register against empirical evidence"
	@echo "make verify-datasets  : Verify dataset manifests, provenance, and licenses"
	@echo "make verify-integrity : Master repository integrity and lifecycle audit"
	@echo "make test             : Run full test suite"
	@echo "make docker-up        : Start local database via docker-compose"
	@echo "make docker-down      : Tear down docker containers"

verify: verify-legal verify-rules verify-claims verify-datasets verify-integrity

verify-legal:
	$(PYTHON) scripts/verification/verify_legal_sources.py

verify-rules:
	$(PYTHON) scripts/verification/verify_rule_registry.py

verify-claims:
	$(PYTHON) scripts/verification/verify_claims.py

verify-datasets:
	$(PYTHON) scripts/verification/verify_dataset_manifest.py

verify-integrity:
	$(PYTHON) scripts/verification/verify_repository_integrity.py

lint:
	ruff check .

test: test-unit

test-unit:
	pytest tests/unit

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
