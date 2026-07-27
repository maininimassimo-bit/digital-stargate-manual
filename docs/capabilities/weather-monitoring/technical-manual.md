# CAP-WEA-001 - Technical Manual

## Purpose

This manual defines responsibilities, conceptual interfaces, dependencies, inputs, outputs and operational considerations for Weather Monitoring. It is documentation only and does not implement software.

## Responsibilities

| Area | Responsibility |
|---|---|
| Weather state authority | Maintain the conceptual source of truth for current observatory weather state. |
| Source governance | Use Equipment Registry evidence for weather-related sources and assets. |
| Validation | Evaluate freshness, availability and consistency of weather evidence. |
| Safety support | Provide decision support for safe, caution, unsafe and unknown state. |
| Session support | Provide weather context to schedule approval, session readiness, suspend, resume and close. |
| Evidence | Preserve traceable weather records for decisions, alerts and recovery. |

## Conceptual Interfaces

| Interface | Provider | Consumer | Input | Output |
|---|---|---|---|---|
| Weather Source Context | Equipment Registry | Weather Monitoring | Registered source identity and state | Source eligibility and status. |
| Weather Evidence Intake | Weather Source / Manual Evidence | Weather Monitoring | Environmental observations | Weather Observation. |
| Weather State Publication | Weather Monitoring | Scheduling, OSM, Safety | Validated observations and thresholds | Weather Snapshot and Safety Decision. |
| Weather Alert | Weather Monitoring | Operations, OSM, Safety | Unsafe, unknown, stale or conflicting condition | Weather Alert and recommended action. |
| Historical Record | Weather Monitoring | Data Platform / Knowledge | Published snapshot and decision evidence | Historical Weather Record. |

No API protocol, endpoint, database schema or event bus is defined by this manual.

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `CAP-EQR-001` Equipment Registry | Capability | Governs weather source identity, configuration and lifecycle. |
| `CAP-SCH-001` Observation Scheduling | Capability | Consumes weather state for scheduling decisions. |
| `CAP-OSM-001` Observation Session Management | Capability | Consumes weather state for readiness and operational actions. |
| `CAP-TGT-001` Target Registry | Capability | Provides target constraints influenced by sky quality. |
| DSRA | Governance | Provides environmental safety risk context. |
| Chapter 26 | Manual evidence | Existing monitoraggio meteo e sicurezza ambientale reference. |
| Chapter 27 | Manual evidence | Existing AllSky reference. |

## Inputs

| Input | Required? | Description |
|---|---|---|
| Weather source identity | Yes | Source registered or traceable through Equipment Registry. |
| Observation timestamp | Yes | Time of environmental evidence. |
| Condition values | Yes when available | Wind, humidity, temperature, cloud, rain, sky quality, seeing, transparency, lightning, roof safe state. |
| Source status | Yes | Available, degraded, offline or unknown. |
| Threshold reference | Yes before implementation | Governed threshold or qualitative rule. |
| Manual review evidence | Conditional | Used when automated source is unavailable or conflicting. |

## Outputs

| Output | Consumer | Description |
|---|---|---|
| Weather Snapshot | Scheduling, OSM, Safety | Authoritative point-in-time state. |
| Operational Assessment | Operations | Assessment against governed thresholds. |
| Safety Decision | Scheduling, OSM, Safety | Safe/caution/unsafe/unknown decision support. |
| Weather Alert | Operations, OSM | Alert evidence for degraded, unsafe or unknown state. |
| Historical Weather Record | Data Platform, Knowledge Framework | Retained evidence linked to schedule/session/recovery. |
| Monitoring Status | Engineering, Operations | Availability and health of monitoring sources and capability. |

## Operational Considerations

- `UNKNOWN` is not equivalent to `SAFE`.
- Stale data must be visible to Scheduling and OSM decisions.
- Conflicting data requires manual review or recovery procedure.
- Unsafe weather must be capable of stopping or suspending session progression through governed procedures.
- Resume requires fresh validation and review of any affected schedule or session state.
- Thresholds must be reviewed before implementation and before operational release.
- Any future UI surface must follow Design System and show status clearly for night operation.

## Configuration Governance

Configuration topics are governed, not implemented here:

| Topic | Governance status |
|---|---|
| Source list | Governed through Equipment Registry. |
| Threshold values | OPEN until approved through ADR/SOP governance. |
| Freshness limits | OPEN until approved. |
| Conflict arbitration | OPEN until approved. |
| Retention classes | OPEN until Data Platform/Backup governance confirms. |

## Failure Modes Covered

- Weather Station Offline.
- Conflicting Weather Data.
- Unsafe Weather State.
- Weather Monitor Recovery.

## Related SOP and Runbooks

- `docs/capabilities/weather-monitoring/sop/monitor-weather.md`
- `docs/capabilities/weather-monitoring/sop/validate-weather-state.md`
- `docs/capabilities/weather-monitoring/sop/suspend-observation.md`
- `docs/capabilities/weather-monitoring/sop/resume-observation.md`
- `docs/capabilities/weather-monitoring/runbooks/weather-station-offline.md`
- `docs/capabilities/weather-monitoring/runbooks/conflicting-weather-data.md`
- `docs/capabilities/weather-monitoring/runbooks/unsafe-weather-state.md`
- `docs/capabilities/weather-monitoring/runbooks/weather-monitor-recovery.md`
