# CAP-WEA-001 - Test Plan

## Purpose

This test plan defines verification scope for Weather Monitoring documentation and future implementation readiness. It does not implement tests or prescribe tooling.

## Test Strategy

| Test Area | Objective |
|---|---|
| Weather validation tests | Verify evidence freshness, availability and conflict handling. |
| Threshold tests | Verify threshold classification once threshold values are approved. |
| Recovery tests | Verify runbook paths for source outage, conflict and unsafe state. |
| Acceptance tests | Verify that capability evidence supports Scheduling, OSM and governance. |
| Regression tests | Verify changes do not break traceability or governance alignment. |

## Weather Validation Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `WEA-TST-001` | Fresh complete weather observation is available. | Weather Snapshot can be classified and published. |
| `WEA-TST-002` | Weather evidence timestamp exceeds approved freshness rule. | State is stale or `UNKNOWN`; not treated as safe. |
| `WEA-TST-003` | Primary weather source is unavailable. | Monitoring Status is degraded/offline and recovery runbook applies. |
| `WEA-TST-004` | Weather Station and AllSky evidence conflict. | Conflict is surfaced; state is `CAUTION` or `UNKNOWN` according to approved rules. |
| `WEA-TST-005` | Manual evidence is used during degraded monitoring. | Manual review evidence is recorded and traceable. |

## Threshold Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `WEA-TST-006` | Wind exceeds approved threshold. | Safety Decision prevents or suspends observation. |
| `WEA-TST-007` | Humidity exceeds approved threshold. | Safety Decision reflects caution/unsafe according to approved rule. |
| `WEA-TST-008` | Rain is detected. | State is unsafe unless future governance defines narrower handling. |
| `WEA-TST-009` | Lightning risk is present. | State is unsafe or caution according to approved safety rule. |
| `WEA-TST-010` | Cloud cover, seeing or transparency degrade quality. | Scheduling/session support receives quality-related state. |
| `WEA-TST-011` | Roof Safe State is false. | Observatory Weather State is not safe. |

## Recovery Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `WEA-TST-012` | Weather station offline during schedule approval. | Schedule approval is blocked, deferred or manually reviewed; evidence recorded. |
| `WEA-TST-013` | Weather state becomes unsafe during active session. | Suspend Observation SOP and unsafe runbook are invoked. |
| `WEA-TST-014` | Unsafe state clears. | Resume Observation SOP requires revalidation before session continuation. |
| `WEA-TST-015` | Monitoring recovers after outage. | Monitoring Status becomes recovered and historical evidence is updated. |
| `WEA-TST-016` | Conflict cannot be resolved. | State remains not safe for unattended progression. |

## Acceptance Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `WEA-TST-017` | CAP-SCH-001 requests schedule weather context. | Published Weather Snapshot or explicit `UNKNOWN` state is available. |
| `WEA-TST-018` | CAP-OSM-001 prepares a session. | Readiness includes weather state reference. |
| `WEA-TST-019` | CAP-OSM-001 closes a weather-impacted session. | Session evidence can reference weather snapshot, alert and decision. |
| `WEA-TST-020` | CAP-000 registry is reviewed. | CAP-WEA-001 fields are synchronized with package evidence. |
| `WEA-TST-021` | Documentation navigation is validated. | All Weather Monitoring pages are reachable from MkDocs nav. |

## Regression Tests

| ID | Scenario | Expected Result |
|---|---|---|
| `WEA-TST-022` | Requirement identifiers are scanned. | No duplicate `WEA-*` requirement IDs. |
| `WEA-TST-023` | Cross references are scanned. | Roadmap, DSRA, EA, Knowledge, DOM-001, CAP-000 and REL-000 references are present. |
| `WEA-TST-024` | Mermaid diagrams are reviewed. | Diagrams use valid Mermaid syntax. |
| `WEA-TST-025` | Governance constraints are reviewed. | No implementation, driver, database, API or UI is introduced. |

## Entry Criteria

- Capability package exists.
- ADR, SOP, runbooks, manual, requirements and acceptance criteria exist.
- CAP-000 includes CAP-WEA-001.
- DOM-001 includes Weather Monitoring as Core Observatory capability.

## Exit Criteria

- All test categories are documented.
- Acceptance criteria are measurable.
- Open threshold and arbitration decisions are listed.
- Validation result is recorded for release/governance review.
