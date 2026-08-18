# CAP-003 - Test Plan

## Purpose

Il test plan definisce verifiche documentali e funzionali future per Equipment Registry. Non crea test automatici, codice o tooling.

## Test Scope

Incluso:

- registration tests;
- configuration validation tests;
- state transition tests;
- recovery tests;
- acceptance tests;
- regression tests documentali.

## Registration Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `EQR-RT-001` | Register physical equipment with mandatory fields. | `EQR-FR-001` | Equipment record created as Registered. |
| `EQR-RT-002` | Register logical group. | `EQR-FR-004` | Logical group linked to member assets. |
| `EQR-RT-003` | Register firmware and driver evidence. | `EQR-FR-004` | Logical dependency records linked to configuration. |
| `EQR-RT-004` | Reject duplicate equipment identifier. | `EQR-QR-001` | Duplicate is detected and not accepted. |

## Configuration Validation Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `EQR-CVT-001` | Verify configuration for operational asset. | `EQR-FR-005` | Configuration becomes Verified or mismatch is recorded. |
| `EQR-CVT-002` | Detect firmware/driver mismatch. | `EQR-OR-003` | Configuration Mismatch runbook applies. |
| `EQR-CVT-003` | Update configuration preserves previous version. | `EQR-OR-004` | Historical configuration remains traceable. |
| `EQR-CVT-004` | Safety-critical configuration change is auditable. | `EQR-SR-004` | Change record includes owner, reason and impact. |

## State Transition Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `EQR-STT-001` | Registered to Verified. | `EQR-OR-001` | Asset can move only after verification evidence. |
| `EQR-STT-002` | Verified to Available. | `EQR-QR-002` | Asset becomes assignable. |
| `EQR-STT-003` | Available to Offline. | `EQR-OR-002` | Asset removed from operational availability. |
| `EQR-STT-004` | Available to Retired. | `EQR-FR-008` | Asset no longer assignable; history preserved. |

## Recovery Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `EQR-REC-001` | Equipment not found during scheduling. | `EQR-AR-002` | Equipment Not Found runbook applies. |
| `EQR-REC-002` | Equipment offline during session preparation. | `EQR-OR-002` | Equipment Offline runbook applies and CAP-001/CAP-002 are informed. |
| `EQR-REC-003` | Registry record inconsistent. | `EQR-AR-002` | Registry Recovery runbook applies. |

## Acceptance Tests

| ID | Test | Acceptance Link | Expected Result |
|---|---|---|---|
| `EQR-AT-001` | End-to-end registration to verified available asset. | `EQR-AC-001` | Record is complete and usable by CAP-001/CAP-002. |
| `EQR-AT-002` | Configuration mismatch blocks assignment. | `EQR-AC-006` | Asset not marked available until resolved. |
| `EQR-AT-003` | Retirement preserves history. | `EQR-AC-010` | Retired asset remains archived. |
| `EQR-AT-004` | Registry and release evidence complete. | `EQR-AC-014` | CAP-000, REL-000 and MkDocs are updated. |

## Regression Tests

- CAP-001 and CAP-002 references remain valid.
- CAP-000 contains exactly one `CAP-EQR-001` registry entry.
- Requirement IDs with prefix `EQR` are unique.
- Mermaid diagrams use supported syntax.
- No implementation code, backend, frontend, API or database is introduced.

## Exit Criteria

- All requirement categories have tests or acceptance criteria.
- ADR, SOP and runbooks are linked in traceability.
- Open decisions are explicit and not implemented by assumption.
