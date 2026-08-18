# Runbook - Roof Unsafe

| Campo | Valore |
|---|---|
| Runbook | Roof Unsafe |
| Capability | `CAP-SAF-001` |
| Severity | Critical operational safety |

## Trigger

Roof/cupola status is unsafe, unknown, conflicting or incompatible with current observation state.

## Immediate Position

Do not authorize unattended observation. Produce Unsafe or Emergency state according to severity and create Close Roof Request if protective posture is required.

## Diagnostic Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm roof status source and timestamp. | Roof status evidence. |
| 2 | Check Equipment Registry context for roof-related asset state. | Equipment reference. |
| 3 | Check active session status from OSM. | Session reference. |
| 4 | Evaluate weather state and risk context. | Weather/Safety input. |
| 5 | Determine Safety State and decision. | Safety Assessment. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Enter Safe Mode if unsafe or unknown state persists. | Safe Mode output. |
| 2 | Hand off to OSM/Operations for governed action. | Handoff evidence. |
| 3 | Revalidate roof and related safety inputs. | Recovery Action. |
| 4 | Allow recovery only after validation. | Recovery Allowed or hold decision. |

## Exit Criteria

- Roof state is validated safe, or operations remain held.
- Audit and safety event evidence are recorded.
