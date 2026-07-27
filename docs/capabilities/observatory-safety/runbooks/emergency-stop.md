# Runbook - Emergency Stop

| Campo | Valore |
|---|---|
| Runbook | Emergency Stop |
| Capability | `CAP-SAF-001` |
| Severity | Critical safety |

## Trigger

Manual operator declares emergency stop or Safety State becomes Emergency.

## Immediate Position

Treat observation as not safe. Produce Emergency state, Abort Observation and Safe Mode decision support. Hardware actions are handled outside this runbook by governed operational procedures.

## Response Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm emergency trigger and affected session/schedule. | Safety Event. |
| 2 | Produce Abort Observation and Safe Mode outputs. | Safety Decision. |
| 3 | Hand off to OSM emergency procedure and operator. | Handoff record. |
| 4 | Record operator decision and audit event. | Audit Record. |
| 5 | Maintain Emergency or Recovery state until validated. | State record. |

## Exit Criteria

- Emergency condition is contained or operations remain held.
- Recovery validation is required before resume.
- Audit evidence exists.
