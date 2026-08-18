# Runbook - Configuration Mismatch

| Campo | Valore |
|---|---|
| Runbook | Configuration Mismatch |
| Capability | CAP-003 Equipment Registry |
| Severity | Operational / Quality |
| Owner | Engineering Owner / OPEN |

## Trigger

- Recorded configuration differs from observed or expected setup.
- Firmware, driver or dependency version is inconsistent.
- Logical equipment group does not match member asset state.
- CAP-001 or CAP-002 detects incompatible equipment evidence.

## Immediate Assessment

1. Identify equipment and configuration record.
2. Determine mismatch type: firmware, driver, physical setup, dependency, assignment or logical group.
3. Check if asset is assigned to current or planned operation.
4. Set equipment state to `Degraded`, `Offline` or `Maintenance` if operational risk exists.
5. Record mismatch evidence.

## Recovery Steps

1. Compare current evidence with last verified configuration.
2. If documentation is wrong, update registry through `update-equipment.md`.
3. If equipment configuration is wrong, keep asset unavailable until corrected and verified.
4. If mismatch impacts scheduling, inform CAP-002.
5. If mismatch impacts session readiness, inform CAP-001.
6. Run `verify-equipment.md` after correction.
7. Close mismatch only with owner and evidence.

## Escalation

Escalate if:

- mismatch is safety-critical;
- driver or firmware issue blocks operation;
- asset is part of active schedule/session;
- repeated mismatch indicates governance gap.

## Exit Criteria

- Configuration is corrected or mismatch remains explicitly open.
- Asset availability is consistent with risk.
- Historical evidence is preserved.

## Related Documents

- `../sop/update-equipment.md`
- `../sop/verify-equipment.md`
- `../adr/EQR-ADR-002-equipment-state-model.md`
