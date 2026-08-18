# Observation Session Management - Acceptance Criteria

| Campo | Valore |
|---|---|
| Documento | Acceptance Criteria |
| Capability | `DSG-CAP-OSM-001` |
| Stato | Controlled Baseline |
| Fonte | Requirements, SOP, Runbooks, Test Plan |

## Purpose

Definire criteri misurabili per accettare la capability documentation package come riferimento per future capability.

## Capability Package Acceptance

| ID | Criteria | Measurement | Required result |
|---|---|---|---|
| `OSM-AC-001` | Complete package exists. | File inventory. | 1 overview, 1 process, 1 requirements, 1 architecture mapping, 1 data model, 2 ADR, 5 SOP, 8 runbooks, 1 manual, 1 test plan, 1 acceptance, 1 traceability. |
| `OSM-AC-002` | No implementation created. | Repository change review. | No software code, backend, frontend, API or database created. |
| `OSM-AC-003` | Governance hierarchy preserved. | Document metadata and traceability. | All documents derive from roadmap -> DSRA -> EA -> Knowledge -> Design System. |
| `OSM-AC-004` | Capability is navigable. | `mkdocs.yml` review. | All key documents reachable from Capability Documentation section. |
| `OSM-AC-005` | ADRs do not duplicate enterprise decisions. | ADR review. | ADRs reference ADR-001 and open decisions without replacing them. |

## Operational Acceptance

| ID | Criteria | Measurement | Required result |
|---|---|---|---|
| `OSM-AC-006` | Process covers all requested steps. | Business process review. | 11/11 steps documented from Observation Request to Knowledge Update. |
| `OSM-AC-007` | SOP coverage complete. | SOP inventory. | Prepare, Execute, Abort, Recover and Close SOPs present. |
| `OSM-AC-008` | Runbook coverage complete. | Runbook inventory. | Scheduler, Weather, Roof, Camera, Mount, N.I.N.A., ASCOM and Emergency Stop covered. |
| `OSM-AC-009` | Failure handling prioritizes safety. | Runbook review. | Weather/safety/roof/mount failures contain containment and escalation. |
| `OSM-AC-010` | Evidence preservation is explicit. | SOP/runbook review. | Logs, raw images, manifest and session result are preserved where possible. |

## Data Acceptance

| ID | Criteria | Measurement | Required result |
|---|---|---|---|
| `OSM-AC-011` | Conceptual data model covers required objects. | Data model review. | Session, manifest, equipment configuration, status, weather, safety, result documented. |
| `OSM-AC-012` | No database design introduced. | Data model review. | No table, API, storage engine or physical schema defined. |
| `OSM-AC-013` | Open data decisions remain open. | ADR/data model review. | Manifest schema, session ID and quality scale listed as open. |

## Quality Acceptance

| ID | Criteria | Measurement | Required result |
|---|---|---|---|
| `OSM-AC-014` | Requirements are categorized. | Requirements review. | Business, Functional, Operational, Security, Performance, Availability, Quality, Traceability present. |
| `OSM-AC-015` | Test plan covers required categories. | Test plan review. | Functional, Operational, Recovery, Acceptance and Regression tests present. |
| `OSM-AC-016` | Design System respected. | UI/design review. | Documentation only; future UI references Design System patterns. |
| `OSM-AC-017` | Static validation passes. | Validation report. | Navigation, links, references, hierarchy and traceability pass. |

## Acceptance Summary

The capability documentation package is accepted when all mandatory criteria `OSM-AC-001` through `OSM-AC-017` are satisfied or any exception is recorded as an open decision with owner and impact.
