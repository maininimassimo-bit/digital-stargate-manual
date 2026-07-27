# WEA-ADR-001 - Authoritative Weather State

| Campo | Valore |
|---|---|
| ADR | `WEA-ADR-001` |
| Capability | `CAP-WEA-001` Weather Monitoring |
| Stato | Accepted |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect |
| Decision scope | Capability-specific |

## Context

Scheduling, Observation Session Management and Observatory Safety need a single governed interpretation of weather conditions. Repository evidence already references weather monitoring, AllSky, safety and session recovery, but the capability package must clarify where the authoritative operational weather state belongs.

## Decision

`CAP-WEA-001` is the authoritative conceptual source for operational weather state consumed by Core Observatory capabilities.

The authoritative state is a governed assessment derived from weather evidence, not a raw device reading and not a forecast. It may include `SAFE`, `CAUTION`, `UNSAFE`, `UNKNOWN` or equivalent approved states.

## Consequences

- `CAP-SCH-001` consumes published weather state for schedule approval and monitoring.
- `CAP-OSM-001` consumes current weather state for readiness, suspend, resume and close evidence.
- `CAP-EQR-001` remains authoritative for weather source asset identity and lifecycle.
- Weather Station and AllSky do not become direct authorities over operational state; they provide evidence.
- Missing, stale or conflicting evidence shall not be silently treated as safe.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Let Scheduling interpret raw weather evidence | Would duplicate safety logic and create inconsistent decisions. |
| Let Observation Session Management own weather state | Would make pre-session scheduling decisions depend on session execution context. |
| Treat each source as independently authoritative | Would create conflict ambiguity and weak traceability. |

## Open Decisions

| Decision | Reason |
|---|---|
| Final state vocabulary | Needs implementation-era confirmation with DSRA and SOP. |
| Multi-source arbitration | Requires source priority, confidence and conflict policy. |
| Publication interface | Future implementation decision; no API is defined here. |

## References

- `docs/capabilities/weather-monitoring/index.md`
- `docs/capabilities/weather-monitoring/architecture-mapping.md`
- `docs/capabilities/observation-scheduling/index.md`
- `docs/capabilities/observation-session-management/index.md`
- `docs/capabilities/equipment-registry/index.md`
- `docs/domains/DOM-001-core-observatory-domain.md`
