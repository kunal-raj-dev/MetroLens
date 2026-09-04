# Role-Based Access Control (RBAC) Specification

## Purpose
Defines user roles, privilege matrices, authentication boundaries, and permission checking policies for Nirikshak.

## Scope
Universal across client UI views and API endpoints.

## Authoritative Inputs
- Legal Metrology Department organizational hierarchy (Inspector $\rightarrow$ Assistant Controller $\rightarrow$ Controller $\rightarrow$ Admin).

## Assumptions
- Least privilege must be strictly enforced. Field inspectors must not be able to modify statutory rules.

## Open Questions
- Departmental Single Sign-On (SSO) integration (e.g. Parichay / Jan Parichay government SSO) [TBD — PRIMARY SOURCE REQUIRED; NO FAKE INTEGRATIONS].

## Dependencies
- `apps/api/`

## Verification Requirements
- API test suite `tests/security/test_rbac.py` must assert 403 Forbidden when unauthorized roles attempt restricted actions.

---

## Role Definitions & Privileges

1. **`INSPECTOR` (Field Enforcement Officer):**
   - Permissions:
     - `inspection:create` (Capture images, run guided flow)
     - `inspection:read_own` (View own draft and submitted inspections)
     - `inspection:review` (Confirm or adjust bounding boxes/annotations)
     - `dossier:generate` (Generate draft inspection dossier)

2. **`SUPERVISOR` / `SENIOR_OFFICER` (Adjudicating Official):**
   - Inherits all `INSPECTOR` permissions, plus:
     - `inspection:read_all` (View inspections across all officers in jurisdiction)
     - `inspection:adjudicate` (Formally issue enforcement notice or compounding order)
     - `audit:read` (View cryptographic audit logs)

3. **`SYSTEM_ADMIN` (Standards & Technical Custodian):**
   - Permissions:
     - `users:manage` (Enroll officers and manage accounts)
     - `rules:update` (Deploy verified machine-readable rule updates)
     - `models:deploy` (Update OCR or vision model weight checkpoints)
     - `system:configure` (Manage thresholds and system parameters)
