# CAP-SAF-001 - Test Plan

## Purpose

This test plan defines verification scope for Observatory Safety readiness. It does not implement tests or prescribe tooling.

## Test Areas

| Area | Objective |
|---|---|
| Safety Rule Tests | Verify conceptual safety rules and state transitions. |
| Emergency Tests | Verify emergency state, emergency shutdown and emergency stop handling. |
| Recovery Tests | Verify return from unsafe/emergency to recovery and safe/warning states. |
| Decision Consistency Tests | Verify consistent decisions across Scheduling, OSM, Weather and Equipment contexts. |
| Acceptance Tests | Verify readiness and governance completeness. |

## Safety Rule Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `SAF-TST-001` | All required inputs are trusted and no unsafe condition exists. | Safety State is `Safe`; Allow Observation may be produced. |
| `SAF-TST-002` | Weather state is `UNSAFE`. | Safety State is `Unsafe`; Suspend/Abort support is produced. |
| `SAF-TST-003` | Weather state is `UNKNOWN`. | Safety State is `Unknown` or `Warning`; unattended observation is not allowed. |
| `SAF-TST-004` | Equipment readiness is degraded. | Warning or Unsafe state is produced according to approved policy. |
| `SAF-TST-005` | Safety authority is disabled or unavailable. | Safety State is `Disabled` or `Unknown`; observation is blocked. |
| `SAF-TST-006` | Maintenance activity is active. | Safety State is `Maintenance`; normal observing is blocked unless governed exception exists. |

## Emergency Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `SAF-TST-007` | Manual emergency stop is requested. | Emergency state and emergency shutdown procedure apply. |
| `SAF-TST-008` | Roof is unsafe during active session. | Close Roof Request or safe mode support is produced; OSM receives suspend/abort decision. |
| `SAF-TST-009` | Power failure is detected. | Safe mode or emergency handling is invoked; audit event is recorded. |
| `SAF-TST-010` | Communications are lost during remote operation. | Fail-safe posture applies; operations are not treated as safe. |

## Recovery Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `SAF-TST-011` | Unsafe condition clears. | Recovery state is entered; resume requires validation. |
| `SAF-TST-012` | Emergency condition is contained. | Recovery Action is recorded before any resume. |
| `SAF-TST-013` | Recovery validation fails. | Operations remain blocked. |
| `SAF-TST-014` | Recovery validation succeeds. | Recovery Allowed output can be produced. |

## Decision Consistency Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `SAF-TST-015` | Scheduling requests approval during Warning state. | Decision requires operator review or policy-specific allow/block. |
| `SAF-TST-016` | OSM starts session without Safety allow state. | Start is blocked by governance. |
| `SAF-TST-017` | Weather and Equipment inputs conflict. | Safety state is not Safe until conflict resolution. |
| `SAF-TST-018` | Operator override is recorded. | Audit Record links operator decision to assessment. |

## Acceptance Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `SAF-TST-019` | Package completeness is reviewed. | All required artefacts exist. |
| `SAF-TST-020` | Requirement identifiers are reviewed. | 32 unique `SAF-*` requirements exist. |
| `SAF-TST-021` | Registry is reviewed. | CAP-000 marks `CAP-SAF-001` Documented / Implementation Ready. |
| `SAF-TST-022` | DOM-001 is reviewed. | `CAP-SAF-001` is included, not future evolution. |
| `SAF-TST-023` | REV-001 is reviewed. | Readiness decision reflects Safety package evidence. |
| `SAF-TST-024` | Navigation is reviewed. | MkDocs includes Observatory Safety package. |

## Exit Criteria

- Test plan covers rule, emergency, recovery, consistency and acceptance categories.
- Open decisions are explicit.
- No implementation is introduced by the test plan.
