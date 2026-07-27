# Runbook - Weather Station Offline

| Campo | Valore |
|---|---|
| Runbook | Weather Station Offline |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Severity | Safety relevant |

## Trigger

The primary weather station is unavailable, stale, unreachable, not reporting or not trusted.

## Immediate Position

Do not assume the observatory is weather-safe. Publish `UNKNOWN` or degraded monitoring state until validated evidence is restored or manual review is approved.

## Impact

- Schedule approval may be blocked or require operator review.
- Active session may require hold, suspension or close through `CAP-OSM-001`.
- Safety assessment may require alternate evidence or manual verification.

## Diagnostic Steps

| Step | Action | Evidence |
|---|---|---|
| 1 | Confirm last known weather timestamp and source status. | Monitoring Status. |
| 2 | Check Equipment Registry context for weather station lifecycle/state. | Equipment reference. |
| 3 | Check whether AllSky or other governed evidence is available. | Alternate source reference. |
| 4 | Determine whether evidence is stale, missing or inconsistent. | Validation result. |
| 5 | Publish degraded/unknown weather state. | Weather Snapshot / Alert. |

## Recovery Steps

| Step | Action | Expected Result |
|---|---|---|
| 1 | Invoke engineering check for weather source availability. | Source status reviewed. |
| 2 | Use alternate evidence only if governance allows and source is traceable. | Manual/alternate evidence recorded. |
| 3 | Revalidate weather state after source returns. | Fresh snapshot produced. |
| 4 | Notify Scheduling/OSM of restored or still degraded state. | Decision support updated. |
| 5 | Record outage and recovery evidence. | Historical Weather Record. |

## Escalation

Escalate to Operations Owner and Engineering Owner when:

- outage persists through an active observing window;
- unsafe weather cannot be ruled out;
- weather station lifecycle or configuration appears inconsistent;
- manual review is required.

## Exit Criteria

- Weather state is restored to a validated state, or
- schedule/session is held, suspended or closed with evidence, and
- recovery record is linked to the affected schedule/session.

## Related Documents

- `docs/capabilities/weather-monitoring/sop/monitor-weather.md`
- `docs/capabilities/weather-monitoring/sop/validate-weather-state.md`
- `docs/capabilities/equipment-registry/runbooks/equipment-offline.md`
