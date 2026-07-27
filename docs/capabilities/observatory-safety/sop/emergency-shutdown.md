# SOP - Emergency Shutdown

| Campo | Valore |
|---|---|
| SOP | Emergency Shutdown |
| Capability | `CAP-SAF-001` |
| Stato | Baseline |

## Purpose

Define the governed conceptual procedure for emergency shutdown decision support. This SOP does not implement electrical, roof, mount, camera, PLC or device actions.

## Trigger

- Safety State is Emergency.
- Manual operator declares emergency stop.
- Roof, power, weather, communication or equipment condition requires immediate protective posture.

## Procedure

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm emergency trigger and context. | Emergency event. |
| 2 | Produce Abort Observation and Safe Mode outputs. | Safety Decision. |
| 3 | Produce Close Roof Request if roof/cupola protection is required. | Close Roof Request evidence. |
| 4 | Notify or hand off to responsible operator/OSM procedure. | Handoff record. |
| 5 | Record Emergency Action and Audit Event. | Audit Record. |
| 6 | Keep state Emergency or Recovery until validation permits change. | State transition record. |

## Controls

- Emergency response takes precedence over schedule or science goals.
- Operator decisions must be logged.
- This SOP creates decision and governance evidence only.

## Outputs

- Emergency Action.
- Abort Observation output.
- Safe Mode output.
- Audit Event.
