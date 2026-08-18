# Runbook - Registry Recovery

| Campo | Valore |
|---|---|
| Runbook | Registry Recovery |
| Capability | CAP-TGT-001 Target Registry |
| Severity | Continuity / Governance |
| Owner | Documentation Owner / Science Owner / OPEN |

## Trigger

- Target Registry evidence is incomplete, inconsistent or unavailable.
- Duplicate or unresolved identity affects multiple records.
- Cross-reference with CAP-SCH-001, CAP-OSM-001 or Data Platform is broken.
- Observation history cannot be mapped to canonical target identity.

## Immediate Assessment

1. Identify impacted target records.
2. Determine whether issue affects active scheduling or session preparation.
3. Freeze non-essential updates to impacted records.
4. Compare registry evidence with capability documents and observation history references.
5. Record recovery incident and owner.

## Recovery Steps

1. Reconstruct target identity from authoritative documentation evidence.
2. Reconcile duplicate or conflicting target records without deleting history.
3. Set uncertain records to `Proposed`, `Identity Pending` or `Suspended`.
4. Re-run `validate-target.md` for targets needed by scheduling or sessions.
5. Update CAP-SCH-001/CAP-OSM-001 references if broken.
6. Preserve observation history and product references.
7. Record recovered state, unresolved gaps and follow-up decisions.

## Escalation

Escalate if:

- active schedule or session depends on uncertain target identity;
- observation history cannot be reconstructed;
- moving target ephemeris requires governance decision;
- a new ADR is required.

## Exit Criteria

- Impacted records have coherent state or explicit open issue.
- No uncertain target is published.
- Cross references with CAP-SCH-001/CAP-OSM-001 are restored or documented open.
- Recovery evidence is archived.

## Related Documents

- `../sop/update-target.md`
- `../sop/validate-target.md`
- `../traceability.md`
