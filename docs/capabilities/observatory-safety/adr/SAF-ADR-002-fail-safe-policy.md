# SAF-ADR-002 - Fail-Safe Behaviour

| Campo | Valore |
|---|---|
| ADR | `SAF-ADR-002` |
| Capability | `CAP-SAF-001` Observatory Safety |
| Stato | Accepted with Open Inputs |
| Data | 2026-07-27 |
| Scope | Capability-specific |

## Context

Digital StarGate operates a remote automated observatory. Repository evidence requires safety and recovery controls, but this package must not define hardware implementation or PLC logic.

## Decision

Observatory Safety shall follow a fail-safe conceptual policy: if safety cannot be positively established, the capability shall not authorize unattended observation start or continuation.

`Unknown`, `Disabled`, `Unsafe` and `Emergency` are not safe states. They block start/continue and require governed suspension, safe mode, recovery or emergency handling as applicable.

## Consequences

- Missing evidence is treated conservatively.
- Loss of safety authority is not interpreted as safe.
- Operator override, if ever permitted, must be governed and auditable.
- Future implementation must not invert this policy without approved governance.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Assume safe until unsafe evidence appears | Unsafe for remote automated operations and inconsistent with DSRA posture. |
| Let each input decide fail-safe behavior independently | Produces fragmented safety posture. |
| Define hardware stop logic in this ADR | Out of scope; implementation and PLC logic are forbidden here. |

## Open Decisions

| Decision | Impact |
|---|---|
| Operator override policy | Determines whether Warning or Unknown can proceed under human decision. |
| Emergency escalation priority | Determines ordering between roof, power, communication and weather hazards. |
| Safety decision freshness | Determines maximum age of safety assessment. |
| Audit retention | Determines evidence retention for fail-safe decisions. |

## References

- `docs/capabilities/observatory-safety/requirements.md`
- `docs/capabilities/observatory-safety/sop/enter-safe-mode.md`
- `docs/capabilities/observatory-safety/runbooks/emergency-stop.md`
- `docs/enterprise/DSRA-risk-assessment.md`
