# Security Testing & Vulnerability Assessment Protocol

## Purpose
Defines automated security scanning, penetration testing routines, dependency vulnerability checks, and input sanitization audits.

## Scope
Universal across code repositories, API endpoints, container images, and edge installations.

## Authoritative Inputs
- OWASP Application Security Verification Standard (ASVS).
- GitHub Security Advisories & CVE databases.

## Assumptions
- Continuous integration must fail if critical known vulnerabilities (CVEs) are detected in dependencies.

## Open Questions
- Departmental CERT-In security audit compliance certification protocol [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `tests/security/`
- `.github/workflows/`

## Verification Requirements
- `ruff`, `bandit`, and dependency vulnerability scans must pass without high/critical severity alerts.

---

## Security Test Regimen

1. **Static Application Security Testing (SAST):**
   - Bandit scan for Python security anti-patterns (e.g. hardcoded secrets, unsafe `pickle` or `yaml.load`).
   - Ruff linting for syntax and security violations.

2. **Fuzzing & Malicious Image Ingestion:**
   - Test injection of corrupt JPEG headers, zero-byte files, and 100-megapixel decompression bombs into the capture endpoint.
   - Assert graceful rejection with status code 400 Bad Request and zero server worker memory leak.

3. **RBAC & Privilege Escalation Testing:**
   - Execute test suite `tests/security/test_rbac.py` attempting unauthorized access with inspector tokens against admin endpoints.
