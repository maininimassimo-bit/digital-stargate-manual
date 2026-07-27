# Runbook - Registry Recovery

| Campo | Valore |
|---|---|
| Runbook | Registry Recovery |
| Capability | CAP-003 Equipment Registry |
| Severity | Continuity / Governance |
| Owner | Documentation Owner / Engineering Owner / OPEN |

## Trigger

- Registry evidence is incomplete, inconsistent or unavailable.
- Duplicate equipment identifiers are discovered.
- Asset history, state or configuration cannot be trusted.
- Cross-reference with CAP-001 or CAP-002 is broken.

## Immediate Assessment

1. Identify impacted equipment records.
2. Determine whether issue affects active operations.
3. Freeze non-essential updates to impacted records.
4. Compare registry evidence with technical manuals and capability references.
5. Record recovery incident and owner.

## Recovery Steps

1. Reconstruct equipment identity from authoritative documentation evidence.
2. Reconcile duplicate or conflicting records without deleting history.
3. Restore last known verified configuration where evidence exists.
4. Set uncertain records to `Unknown` or `Registered` until verification.
5. Re-run `verify-equipment.md` for operational assets.
6. Update CAP-001/CAP-002 references if broken.
7. Record recovered state, unresolved gaps and follow-up decisions.

## Escalation

Escalate if:

- registry inconsistency affects safety-critical equipment;
- active session or schedule depends on uncertain asset state;
- historical evidence cannot be reconstructed;
- a governance change or ADR is required.

## Exit Criteria

- Impacted records have coherent state or explicit open issue.
- No uncertain equipment is marked available.
- Cross references with CAP-001/CAP-002 are restored or documented open.
- Recovery evidence is archived.

## Related Documents

- `../sop/update-equipment.md`
- `../sop/verify-equipment.md`
- `../traceability.md`
