# Append-Only Audit Log Specification

## Purpose
Defines the schema, cryptographic linking, and tamper-detection mechanisms for the Nirikshak system audit log.

## Scope
Logs all user logins, image captures, quality gate overrides, officer manual adjustments, and dossier generations.

## Authoritative Inputs
- Principles of secure logging and tamper evidence (NIST SP 800-92).

## Assumptions
- Audit logs are append-only; update and delete database operations on log tables are prohibited at database trigger level.

## Open Questions
- Departmental archival period for historical inspection logs [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `infra/db/`
- `packages/evidence/`

## Verification Requirements
- Attempting to modify an existing log record in automated tests must trigger an immediate hash-chain failure.

---

## Hash-Chained Audit Record Schema

```json
{
  "log_entry_id": 1042,
  "timestamp_utc": "2026-09-04T12:30:45Z",
  "operator_id": "INSP-DL-0482",
  "event_type": "OFFICER_CONFIRMED_OVERLAY",
  "inspection_id": "8f7e2a9b-4c31-48f5-9a88-12c8b74f3910",
  "event_payload": {
    "rule_id": "LMPC-R7-TABLE-I",
    "action": "ACCEPTED_CALCULATED_FONT_HEIGHT",
    "measured_mm": 2.14,
    "confidence_interval_mm": [2.05, 2.23]
  },
  "previous_entry_sha256": "4b92ec1781...c82a1b",
  "entry_sha256": "9a38f712dc...f7823e"
}
```

### Hash Link Formula:
$$\text{EntryHash}_n = \text{SHA-256}\left( \text{EntryHash}_{n-1} + \text{Payload}_n + \text{Timestamp}_n + \text{OperatorID}_n \right)$$
Any unauthorized modification or deletion of record $k$ breaks the verification chain for all subsequent entries $k+1 \dots N$.
