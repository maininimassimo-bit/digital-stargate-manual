# CAP-WEA-001 - Acceptance Criteria

## Purpose

Acceptance criteria define measurable conditions for considering Weather Monitoring documentation ready for future implementation. They do not certify operational implementation.

## Capability Acceptance Criteria

| ID | Criterion | Verification |
|---|---|---|
| `WEA-ACC-001` | Capability overview defines purpose, value, scope, actors, stakeholders, dependencies, lifecycle and success criteria. | Review `index.md`. |
| `WEA-ACC-002` | Business process covers collection, validation, assessment, safety evaluation, decision support, publication, monitoring, recovery and historical recording. | Review `business-process.md`. |
| `WEA-ACC-003` | Requirements include 32 unique identifiers across required categories. | Review `requirements.md`. |
| `WEA-ACC-004` | Weather model covers wind, humidity, temperature, cloud cover, rain, sky quality, seeing, transparency, lightning, roof safe state and overall observatory weather state. | Review `index.md` and `data-model.md`. |
| `WEA-ACC-005` | Data model remains conceptual and avoids physical database design. | Review `data-model.md`. |
| `WEA-ACC-006` | Architecture mapping references CAP-OSM-001, CAP-SCH-001, CAP-EQR-001, CAP-TGT-001, DOM-001, Enterprise Architecture and Knowledge Framework. | Review `architecture-mapping.md`. |
| `WEA-ACC-007` | Capability ADRs are specific to Weather Monitoring and do not duplicate enterprise decisions. | Review ADR folder. |
| `WEA-ACC-008` | SOPs exist for monitor, validate, suspend and resume procedures. | Review SOP folder. |
| `WEA-ACC-009` | Runbooks exist for weather station offline, conflicting data, unsafe state and monitor recovery. | Review runbooks folder. |
| `WEA-ACC-010` | Technical manual documents responsibilities, interfaces, dependencies, inputs, outputs and operational considerations. | Review `technical-manual.md`. |
| `WEA-ACC-011` | Test plan covers weather validation, thresholds, recovery and acceptance tests. | Review `test-plan.md`. |
| `WEA-ACC-012` | Traceability maps all artefacts to Roadmap, DSRA, EA-000, Knowledge Framework, DOM-001, CAP-000, REL-000 and existing Core Observatory capabilities. | Review `traceability.md`. |
| `WEA-ACC-013` | CAP-000 registers CAP-WEA-001 as Documented, maturity Documented, readiness Implementation Ready, version 0.1. | Review `CAP-000`. |
| `WEA-ACC-014` | DOM-001 includes CAP-WEA-001 without redefining other capability boundaries. | Review `DOM-001`. |
| `WEA-ACC-015` | REL-000 contains only minimum governed reference to CAP-WEA-001. | Review `REL-000`. |
| `WEA-ACC-016` | MkDocs navigation includes Weather Monitoring package pages. | Review `mkdocs.yml`. |
| `WEA-ACC-017` | Validation reports MkDocs build or static validation result. | Review final validation report. |

## Non-Acceptance Conditions

The capability is not acceptable if it:

- introduces driver, sensor, forecasting, API, database, frontend or backend implementation;
- changes Roadmap, DSRA, EA-000, Knowledge Framework, Design System or release governance;
- treats `UNKNOWN` weather as safe without approved governance;
- omits traceability to Core Observatory capability packages;
- leaves required package artefacts outside MkDocs navigation.

## Acceptance Status

| Field | Value |
|---|---|
| Documentation readiness | Ready for review after validation |
| Implementation readiness | Implementation Ready after CAP-000 synchronization |
| Operational readiness | Not claimed |
| Open decisions | Threshold values, multi-source arbitration, state publication interface, retention |
