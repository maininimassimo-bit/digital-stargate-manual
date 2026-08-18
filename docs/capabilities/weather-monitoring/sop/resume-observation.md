# SOP - Resume Observation after Weather Suspension

| Campo | Valore |
|---|---|
| SOP | Resume Observation |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Scope | Weather-driven resume support |

## Purpose

Define the governed procedure for supporting resume after weather-driven suspension. Resume is not automatic unless future governance explicitly approves automation rules.

## Preconditions

- Previous weather state caused suspension, prevention or manual hold.
- Fresh weather evidence is available or manual review has been performed.
- `CAP-OSM-001` owns session lifecycle decision and `CAP-SCH-001` owns schedule impact where applicable.

## Procedure

| Step | Action | Expected Evidence |
|---|---|---|
| 1 | Collect fresh weather evidence. | Weather Observation. |
| 2 | Validate state using `validate-weather-state.md`. | Validation result. |
| 3 | Confirm unsafe condition has cleared and no unresolved conflict remains. | Safety Decision. |
| 4 | Review schedule/session impact with responsible capability. | Schedule/session review evidence. |
| 5 | Publish new Weather Snapshot. | Snapshot reference. |
| 6 | Recommend resume, reschedule, continue hold or close based on state. | Recommendation record. |
| 7 | Record final decision and link to prior suspension. | Historical Weather Record. |

## Controls

- Resume requires fresh validation, not elapsed time alone.
- `CAUTION` requires operator review.
- `UNKNOWN` does not authorize unattended resume.
- Weather Monitoring provides decision support; OSM/Scheduling execute their governed lifecycle responsibilities.

## Outputs

- Updated Weather Snapshot.
- Resume recommendation.
- Historical Weather Record.
- Link to suspension evidence.

## Related Documents

- `docs/capabilities/weather-monitoring/sop/validate-weather-state.md`
- `docs/capabilities/observation-session-management/sop/recover-session.md`
- `docs/capabilities/observation-scheduling/sop/update-schedule.md`
