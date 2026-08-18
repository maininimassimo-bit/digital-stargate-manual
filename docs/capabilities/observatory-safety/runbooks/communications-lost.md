# Runbook - Communications Lost

| Campo | Valore |
|---|---|
| Runbook | Communications Lost |
| Capability | `CAP-SAF-001` |
| Severity | Safety relevant |

## Trigger

Communication status is lost, stale, degraded or insufficient to confirm safe remote operation.

## Immediate Position

Do not assume the observatory is safe for unattended continuation. Safety State becomes Unknown, Warning, Unsafe or Disabled according to approved policy.

## Response Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm communication loss scope and timestamp. | Communication status. |
| 2 | Identify affected session, schedule and equipment context. | Impact reference. |
| 3 | Evaluate whether safe monitoring/control can be maintained. | Safety Assessment. |
| 4 | Produce suspend, safe mode or block decision if required. | Safety Decision. |
| 5 | Record audit event and recovery owner. | Audit Record. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Restore or verify communication evidence. | Fresh status. |
| 2 | Re-evaluate safety policy. | Updated Safety State. |
| 3 | If valid, permit Recovery Allowed output. | Recovery Action. |
| 4 | Hand off to OSM/Scheduling for resume or reschedule. | Handoff record. |

## Exit Criteria

- Communication status is validated or operations remain held.
- Recovery evidence is recorded.
