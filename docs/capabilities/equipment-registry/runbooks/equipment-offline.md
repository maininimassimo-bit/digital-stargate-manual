# Runbook - Equipment Offline

| Campo | Valore |
|---|---|
| Runbook | Equipment Offline |
| Capability | CAP-003 Equipment Registry |
| Severity | Operational / Safety when critical |
| Owner | Operations Owner / Engineering Owner / OPEN |

## Trigger

- Asset required for operation is offline.
- Health status changes to offline or degraded.
- CAP-001 reports equipment unavailable during preparation.
- CAP-002 cannot allocate required resource.

## Immediate Assessment

1. Identify equipment and current assignment.
2. Mark state `Offline` unless evidence supports `Degraded` or `Maintenance`.
3. Check active schedule and session impact.
4. Determine if equipment is safety-critical.
5. Record health evidence.

## Recovery Steps

1. Remove equipment from availability for scheduling.
2. Notify CAP-002 if future schedule is affected.
3. Notify CAP-001 if session preparation or execution is affected.
4. Check dependencies and logical groups.
5. If recoverable, create maintenance or recovery action.
6. After recovery, execute `verify-equipment.md`.
7. Restore state only when verification evidence is complete.

## Escalation

Escalate immediately if:

- equipment is safety-critical;
- active session is impacted;
- no replacement resource exists;
- offline state affects roof, power, network, weather or storage continuity.

## Exit Criteria

- Equipment is no longer advertised as available.
- Impacted capability owners are informed.
- Recovery, maintenance or retirement path is recorded.

## Related Documents

- `../sop/verify-equipment.md`
- `../sop/update-equipment.md`
- `registry-recovery.md`
