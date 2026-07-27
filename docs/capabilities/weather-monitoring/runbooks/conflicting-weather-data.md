# Runbook - Conflicting Weather Data

| Campo | Valore |
|---|---|
| Runbook | Conflicting Weather Data |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Severity | Safety relevant |

## Trigger

Two or more weather evidence sources disagree materially, or a source conflicts with manual observation or AllSky evidence.

## Immediate Position

Do not resolve conflict silently. Mark state `CAUTION` or `UNKNOWN` according to governance and require review before unattended progression.

## Impact

- Scheduling decisions may be deferred.
- Active sessions may require suspension or increased monitoring.
- Historical traceability must capture the conflicting evidence and resolution.

## Diagnostic Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Identify conflicting sources and timestamps. | Source comparison. |
| 2 | Check source status and freshness. | Monitoring Status. |
| 3 | Compare conflicting dimensions such as cloud, rain, wind or roof safe state. | Conflict record. |
| 4 | Review Equipment Registry for degraded source or known maintenance state. | Equipment reference. |
| 5 | Assign temporary state `CAUTION` or `UNKNOWN`. | Weather Snapshot / Alert. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Request operator/engineering review. | Review owner assigned. |
| 2 | Remove or downgrade untrusted evidence source only through governed review. | Source confidence updated conceptually. |
| 3 | Revalidate weather state once conflict is resolved. | Updated Safety Decision. |
| 4 | Inform Scheduling/OSM of final state. | Updated schedule/session context. |
| 5 | Record conflict and resolution. | Historical Weather Record. |

## Escalation

Escalate immediately when conflict involves rain, lightning, roof safe state or any condition that could endanger equipment.

## Exit Criteria

- Conflict is resolved and state is validated, or
- observation remains held/suspended with documented reason.

## Related Documents

- `docs/capabilities/weather-monitoring/adr/WEA-ADR-001-authoritative-weather-state.md`
- `docs/capabilities/weather-monitoring/sop/validate-weather-state.md`
- `docs/capabilities/weather-monitoring/data-model.md`
