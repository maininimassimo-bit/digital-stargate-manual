# Runbook - Invalid Coordinates

| Campo | Valore |
|---|---|
| Runbook | Invalid Coordinates |
| Capability | CAP-TGT-001 Target Registry |
| Severity | Operational / Data Quality |
| Owner | Science Owner / Operations Owner / OPEN |

## Trigger

- Coordinates are missing, malformed or outside valid ranges.
- Epoch or coordinate system is missing when required.
- Coordinates conflict with catalogue reference or target identity.
- Moving target lacks sufficient ephemeris reference for intended use.

## Immediate Assessment

1. Identify target and coordinate evidence.
2. Check whether target is static or moving.
3. Verify right ascension, declination, coordinate system and epoch where applicable.
4. Determine scheduling/session impact.
5. Block publication or mark target `Suspended` if already published.

## Recovery Steps

1. Record invalid coordinate finding.
2. Do not allow scheduling until corrected or accepted by governed decision.
3. Request corrected coordinate or ephemeris evidence.
4. Update target through `update-target.md`.
5. Re-run `validate-target.md`.
6. Notify CAP-SCH-001 and CAP-OSM-001 if published target was impacted.

## Escalation

Escalate if:

- target is linked to published schedule;
- target is part of active or planned session;
- moving target handling requires new ADR;
- coordinate conflict cannot be resolved.

## Exit Criteria

- Coordinates are validated or target remains unpublishable.
- Scheduling/session impacts are recorded.
- Historical evidence is preserved.

## Related Documents

- `../sop/update-target.md`
- `../sop/validate-target.md`
- `../data-model.md`
