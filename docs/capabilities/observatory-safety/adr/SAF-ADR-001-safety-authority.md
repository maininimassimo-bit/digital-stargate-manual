# SAF-ADR-001 - Safety Authority

| Campo | Valore |
|---|---|
| ADR | `SAF-ADR-001` |
| Capability | `CAP-SAF-001` Observatory Safety |
| Stato | Accepted |
| Data | 2026-07-27 |
| Scope | Capability-specific |

## Context

Core Observatory capabilities need a single conceptual authority for operational safety decisions. Weather Monitoring owns weather state; OSM owns session lifecycle; Scheduling owns schedule preparation; Equipment Registry owns equipment state. None of these should independently redefine the overall observatory safety decision.

## Decision

`CAP-SAF-001` is the authoritative conceptual safety policy capability for Core Observatory operations.

It evaluates safety inputs and produces safety outputs such as Allow Observation, Suspend Observation, Abort Observation, Close Roof Request, Safe Mode, Recovery Allowed, Operator Notification and Audit Event.

## Consequences

- Safety decision authority is centralized conceptually.
- Weather, equipment, schedule, target and session data remain owned by their source capabilities.
- OSM and Scheduling consume safety decisions but do not own the safety policy.
- Hardware and PLC behavior remain outside this ADR.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Let OSM own all safety decisions | Would couple safety policy to session lifecycle and weaken pre-session scheduling safety. |
| Let Weather Monitoring own safety decisions | Weather is only one safety input and cannot represent power, roof, communication or maintenance state alone. |
| Distributed safety decisions across capabilities | Would create inconsistent allow/suspend/abort behavior. |

## Open Decisions

- Final safety rule priority model.
- State publication interface.
- Operator override policy.
- Audit retention class.

## References

- `docs/capabilities/observatory-safety/index.md`
- `docs/capabilities/observatory-safety/architecture-mapping.md`
- `docs/domains/DOM-001-core-observatory-domain.md`
- `docs/reviews/REV-001-core-observatory-readiness-review.md`
