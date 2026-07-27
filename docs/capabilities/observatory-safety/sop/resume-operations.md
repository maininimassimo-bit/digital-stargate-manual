# SOP - Resume Operations

| Campo | Valore |
|---|---|
| SOP | Resume Operations |
| Capability | `CAP-SAF-001` |
| Stato | Baseline |

## Purpose

Define the procedure for determining whether operations may resume after Unsafe, Emergency, Unknown, Disabled, Maintenance or Recovery state.

## Preconditions

- Previous Safety State blocked or constrained operations.
- Fresh input evidence is available or gaps are explicitly recorded.
- OSM/Scheduling context is known when operations resume affects observation activity.

## Procedure

| Step | Action | Evidence |
|---|---|---|
| 1 | Collect fresh safety inputs. | Input set. |
| 2 | Re-evaluate Safety Policy. | Safety Assessment. |
| 3 | Confirm emergency/unsafe cause is resolved or mitigated. | Recovery Action. |
| 4 | Determine whether Recovery Allowed output can be produced. | Safety Decision. |
| 5 | Hand off to OSM/Scheduling for resume or reschedule decision. | Handoff record. |
| 6 | Record operator decision and audit event. | Audit Record. |

## Controls

- Resume cannot be based on elapsed time alone.
- Unknown remains not safe for unattended operation.
- Recovery Allowed does not directly restart hardware or sequences.

## Outputs

- Recovery Action.
- Recovery Allowed or continue hold decision.
- Audit Event.
