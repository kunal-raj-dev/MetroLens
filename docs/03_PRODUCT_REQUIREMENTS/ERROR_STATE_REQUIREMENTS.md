# Error State Requirements & Failure Behavior

## Purpose
Defines the strict system behaviors, routing policies, and fallback actions when encountering corrupted inputs, edge cases, optical failures, or ambiguous legal applicability.

## Scope
Universal across vision pipeline, rule engine, storage, and user interface.

## Authoritative Inputs
- Project Anti-Hallucination Mandate.
- Legal Metrology standard operating procedures.

## Assumptions
- The system must ALWAYS prefer routing to human `REVIEW` or requesting a retake rather than fabricating a false certainty verdict.

## Open Questions
- Departmental escalation workflow for unresolved multi-panel conflicts [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/16_LIMITATIONS/KNOWN_FAILURES.md`

## Verification Requirements
- Every error state defined below must be tested via an adversarial test case in `tests/fixtures/`.

---

## Controlled Error States & Routing Table

| Failure Scenario | Trigger Condition | System Action & Routing | User-Facing Guidance | Dossier Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Severe Motion Blur** | Laplacian variance $\sigma^2 < 100.0$ | Halt pipeline. Reject frame. | "Image too blurry. Hold device steady and retake." | `REQUEST_RETAKE` |
| **Specular Glare on Text** | Brightness $> 250$ across $> 15\%$ of text ROI | Halt pipeline. Prompt angle tilt. | "Severe glare obscuring text. Tilt camera slightly." | `REQUEST_RETAKE` |
| **No Physical Calibration Marker** | Fiducial/reference object not detected | Disable mm conversion. Proceed with text OCR. | "No scale marker detected. Dimensional check will require manual verification." | `REVIEW` (on font & area) |
| **Conflicting Declarations Across Panels** | Net quantity on PDP ($500\text{ g}$) differs from rear panel ($450\text{ g}$) | Log both panels in evidence graph. Trigger conflict alert. | "Conflict detected: PDP and Rear panel state different quantities." | `REVIEW` / `FAIL` (Flagged) |
| **Low OCR Confidence Token** | OCR token confidence $< 0.60$ on mandatory field | Highlight bounding box with yellow border. | "Ambiguous text detected. Officer verification required." | `REVIEW` |
| **Unknown Commodity Applicability** | Commodity category not found in applicability matrix | Set statutory scope to `UNKNOWN`. Halt automated pass. | "Uncataloged commodity. Manual rule assignment needed." | `BLOCKED` / `REVIEW` |
| **Unverified Regulatory Provision** | Referenced rule has verification status `PRIMARY_SOURCE_REQUIRED` | Refuse automated enforcement. | "Rule currently unverified against Gazette. Cannot enforce." | `BLOCKED` |
