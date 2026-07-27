# SOP - Monitor Weather

| Campo | Valore |
|---|---|
| SOP | Monitor Weather |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Scope | Operational weather monitoring procedure |

## Purpose

Define the repeatable procedure for monitoring observatory weather state during planning, scheduling and active observation sessions.

## Preconditions

- Weather source context is available or explicitly marked unavailable.
- Equipment Registry references for relevant sources are known where applicable.
- Current schedule/session context is known when monitoring supports an active operation.

## Procedure

| Step | Action | Expected Evidence |
|---|---|---|
| 1 | Identify monitoring context: planning, schedule approval, active session or recovery. | Context recorded. |
| 2 | Check weather source availability and freshness. | Monitoring Status. |
| 3 | Collect current weather evidence from governed sources or manual observation if required. | Weather Observation. |
| 4 | Validate evidence using `validate-weather-state.md`. | Validation result. |
| 5 | Produce or confirm Weather Snapshot. | Snapshot ID/reference. |
| 6 | Review overall observatory weather state. | SAFE/CAUTION/UNSAFE/UNKNOWN state. |
| 7 | Publish state to Scheduling or OSM context as applicable. | Decision support reference. |
| 8 | Continue monitoring until schedule/session no longer requires weather context. | Monitoring log or historical record. |

## Controls

- Do not mark weather safe when source is offline, stale or unresolved.
- Escalate `UNSAFE` immediately to suspend/prevent observation process.
- Escalate `UNKNOWN` for manual review or recovery.
- Preserve timestamp and source evidence.

## Outputs

- Weather Snapshot.
- Monitoring Status.
- Weather Alert when required.
- Historical Weather Record when linked to schedule/session.

## Related Documents

- `docs/capabilities/weather-monitoring/sop/validate-weather-state.md`
- `docs/capabilities/weather-monitoring/runbooks/weather-station-offline.md`
- `docs/capabilities/weather-monitoring/runbooks/unsafe-weather-state.md`
