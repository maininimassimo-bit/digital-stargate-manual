# Runbook - Power Failure

| Campo | Valore |
|---|---|
| Runbook | Power Failure |
| Capability | `CAP-SAF-001` |
| Severity | Critical operational continuity |

## Trigger

Power status is failed, unstable, unknown, UPS-limited or otherwise incompatible with safe observation.

## Immediate Position

Observation is not considered safe unless approved evidence proves a safe operating state. Produce Unsafe, Emergency, Unknown or Recovery state according to policy.

## Response Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm power condition and affected infrastructure context. | Power status evidence. |
| 2 | Check active session and equipment dependencies. | OSM/EQR references. |
| 3 | Evaluate whether Safe Mode or Emergency posture is required. | Safety Assessment. |
| 4 | Produce Abort, Suspend, Safe Mode or Close Roof Request if needed. | Safety Decision. |
| 5 | Record safety event and audit evidence. | Audit Record. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Confirm stable power evidence. | Fresh power status. |
| 2 | Revalidate equipment and communication context. | Recovery evidence. |
| 3 | Re-evaluate safety state. | Safety Assessment. |
| 4 | Allow recovery only after validation. | Recovery Allowed or continued hold. |

## Exit Criteria

- Power condition is stable and validated, or operations remain in safe/held posture.
- Audit and recovery evidence are recorded.
