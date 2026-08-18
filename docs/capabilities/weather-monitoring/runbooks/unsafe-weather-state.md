# Runbook - Unsafe Weather State

| Campo | Valore |
|---|---|
| Runbook | Unsafe Weather State |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Severity | Critical operational safety |

## Trigger

Weather Monitoring publishes or confirms an `UNSAFE` state, or detects rain, lightning, unsafe roof state, severe wind, critical humidity or other approved unsafe condition.

## Immediate Position

Protect observatory safety. Weather Monitoring provides safety decision support and handoff evidence; `CAP-OSM-001` and safety procedures govern session actions.

## Impact

- New observation starts are blocked.
- Active observation may be suspended, aborted or closed.
- Schedule may require cancellation or update.
- Weather alert and historical record are mandatory.

## Response Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm latest Weather Snapshot and unsafe trigger. | Snapshot and trigger. |
| 2 | Publish Weather Alert. | Alert record. |
| 3 | Notify/hand off to Observation Session Management. | Session handoff evidence. |
| 4 | Invoke Suspend Observation SOP. | Suspension support record. |
| 5 | Continue monitoring until safe or recovered state is validated. | Monitoring updates. |
| 6 | Record weather state, decision and affected schedule/session. | Historical Weather Record. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Wait for unsafe condition to clear and collect fresh evidence. | Fresh observation. |
| 2 | Validate weather state using SOP. | Validation result. |
| 3 | Confirm no unresolved stale/conflict condition exists. | Safety Decision. |
| 4 | If safe or caution, follow Resume Observation SOP with OSM/Scheduling review. | Resume recommendation. |
| 5 | Preserve complete event timeline. | Historical record. |

## Escalation

Escalate to Operations Owner and Safety Reviewer when:

- rain, lightning or roof-safe condition is involved;
- active session cannot be safely suspended through normal procedure;
- source confidence is uncertain;
- equipment may have been exposed to unsafe conditions.

## Exit Criteria

- Session/schedule action is documented, and
- weather state is no longer unsafe or the session remains closed/held, and
- alert is resolved or explicitly carried forward.

## Related Documents

- `docs/capabilities/weather-monitoring/sop/suspend-observation.md`
- `docs/capabilities/weather-monitoring/sop/resume-observation.md`
- `docs/capabilities/observation-session-management/sop/abort-session.md`
- `docs/capabilities/observation-session-management/runbooks/weather-unsafe.md`
