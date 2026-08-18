# Runbook - Unresolved Identifier

| Campo | Valore |
|---|---|
| Runbook | Unresolved Identifier |
| Capability | CAP-TGT-001 Target Registry |
| Severity | Data Quality |
| Owner | Science Owner / OPEN |

## Trigger

- Catalogue identifier cannot be confirmed.
- Target alias cannot be resolved to canonical identity.
- Custom target lacks sufficient identity evidence.

## Immediate Assessment

1. Identify unresolved designation or alias.
2. Check existing Target Registry aliases and catalogue references.
3. Check whether target is custom or moving target.
4. Determine if coordinates or metadata can support provisional identity.
5. Keep lifecycle state `Identity Pending` or `Proposed`.

## Recovery Steps

1. Record unresolved identifier and source.
2. Do not publish target for scheduling.
3. Add catalogue reference only as unconfirmed evidence.
4. Request Science Owner decision or additional evidence.
5. If resolved, update target identity and execute `validate-target.md`.
6. If not resolved, keep target unapproved or retire proposal.

## Escalation

Escalate if:

- unresolved identifier affects an approved Observation Request;
- target has high scientific priority;
- identifier ambiguity can create duplicate target;
- moving target identity needs ephemeris decision.

## Exit Criteria

- Identifier is resolved, explicitly unconfirmed or target proposal is retired.
- Target is not published unless validation passes.
- Evidence and owner are recorded.

## Related Documents

- `../sop/register-target.md`
- `../sop/validate-target.md`
- `duplicate-target.md`
