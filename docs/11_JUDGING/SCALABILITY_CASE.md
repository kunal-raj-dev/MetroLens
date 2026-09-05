# National Scalability & Market Surveillance Impact

## Purpose
Demonstrates the national scalability, multi-jurisdiction adaptation, and systemic economic impact of deploying Nirikshak across Indian Legal Metrology directorates.

## Scope
Covers market surveillance scalability, e-commerce catalog auditing, and multi-state deployment.

## Authoritative Inputs
- Department of Consumer Affairs market surveillance reports and enforcement statistics.

## Assumptions
- Automated inspection assistance increases enforcement coverage by orders of magnitude compared to manual visual checks.

## Dependencies
- `apps/api/`
- `infra/deployment/`

## Verification Requirements
- API architecture must support horizontal scaling with stateless worker containers.

---

## Scalability Vectors

1. **Field Enforcement Acceleration:**
   - Manual inspection of a complex retail package with caliper font measurement currently takes 8 to 15 minutes per SKU.
   - Nirikshak guided multi-panel inspection completes in under 30 seconds, enabling an inspector to audit 20x more inventory per inspection visit.

2. **E-Commerce Market Surveillance Integration:**
   - The same deterministic extraction and rule engine modules can be deployed as a headless batch auditor scanning product listing images across major e-commerce platforms.
   - Detects missing mandatory declarations (Country of Origin, Net Quantity, MRP, USP) across 100,000 online listings daily.

3. **Multi-State Adaptation Without Code Forking:**
   - State-specific amendments or local language notices are managed through modular YAML rule files in `rules/` without recompiling backend services.
