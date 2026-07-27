# SOP - Suspend Observation for Weather

| Campo | Valore |
|---|---|
| SOP | Suspend Observation |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Scope | Weather-driven suspension support |

## Purpose

Define the governed procedure for supporting observation suspension when weather state becomes unsafe or unknown.

## Preconditions

- Weather Monitoring has produced `UNSAFE`, `UNKNOWN` or unresolved `CAUTION` state.
- A schedule or observation session is active or pending.
- `CAP-OSM-001` remains responsible for session lifecycle actions.

## Procedure

| Step | Action | Expected Evidence |
|---|---|---|
| 1 | Confirm latest Weather Snapshot and Safety Decision. | Snapshot and decision reference. |
| 2 | Notify or hand off to Observation Session Management context. | Session/schedule impact reference. |
| 3 | Prevent new observation start or request session suspension according to OSM procedure. | Suspension evidence. |
| 4 | Preserve weather reason and state transition. | Weather Alert / Historical Record. |
| 5 | Continue monitoring until recovery or closure decision. | Monitoring updates. |
| 6 | If condition worsens or safety risk escalates, follow emergency/safety runbook. | Escalation evidence. |

## Controls

- Weather Monitoring does not directly implement hardware stop, roof closure or sequence control.
- `UNSAFE` and unresolved `UNKNOWN` are treated as blockers for unattended continuation.
- All suspension support must be traceable to snapshot, alert and decision evidence.

## Outputs

- Suspension support record.
- Weather Alert.
- Historical Weather Record.
- Handoff reference to `CAP-OSM-001`.

## Related Documents

- `docs/capabilities/observation-session-management/sop/abort-session.md`
- `docs/capabilities/weather-monitoring/runbooks/unsafe-weather-state.md`
- `docs/capabilities/weather-monitoring/sop/resume-observation.md`
