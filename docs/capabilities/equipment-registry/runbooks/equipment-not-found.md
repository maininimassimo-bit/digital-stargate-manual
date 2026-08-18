# Runbook - Equipment Not Found

| Campo | Valore |
|---|---|
| Runbook | Equipment Not Found |
| Capability | CAP-003 Equipment Registry |
| Severity | Operational |
| Owner | Engineering Owner / Operations Owner / OPEN |

## Trigger

- CAP-001 or CAP-002 references equipment not present in registry.
- Operator cannot identify asset needed for scheduling, session or maintenance.
- Existing manual references an asset without registry record.

## Immediate Assessment

1. Identify requested equipment name, role or reference.
2. Check whether it exists under different identifier or logical group.
3. Verify whether asset is retired, archived or not yet registered.
4. Assess impact on schedule, session, safety or maintenance.
5. Open missing equipment record if evidence is sufficient.

## Recovery Steps

1. If asset exists under another identifier, update cross-reference.
2. If asset is not registered, execute `register-equipment.md`.
3. If asset cannot be verified, keep state `Unknown` or `Registered`.
4. Prevent use in scheduling/session until verification completes.
5. Notify CAP-001/CAP-002 if impacted.
6. Record recovery evidence and owner.

## Escalation

Escalate if:

- asset is safety-critical;
- schedule or session is blocked;
- identity cannot be resolved;
- duplicate asset records are suspected.

## Exit Criteria

- Equipment identity is resolved or explicitly open.
- CAP-001/CAP-002 impact is recorded.
- No unavailable asset is treated as operational.

## Related Documents

- `../sop/register-equipment.md`
- `../sop/verify-equipment.md`
- `../traceability.md`
