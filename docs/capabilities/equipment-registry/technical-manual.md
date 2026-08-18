# CAP-003 - Technical Manual

## Purpose

Il manuale tecnico descrive responsabilita, interfacce, dipendenze, input, output, considerazioni operative e configuration governance dell'Equipment Registry. Non prescrive implementazione software.

## Responsibilities

| Area | Responsibility |
|---|---|
| Asset identity | Mantenere identificatore, nome, tipo, owner e posizione. |
| Configuration governance | Registrare configurazioni, firmware, driver, versioni e dipendenze. |
| State governance | Mantenere equipment state, health status and lifecycle state. |
| Assignment evidence | Collegare asset a scheduling, sessioni, maintenance o logical groups. |
| Maintenance evidence | Conservare record manutentivi e impatti. |
| Safety evidence | Evidenziare asset safety-critical e stati unsafe/offline. |
| Historical preservation | Conservare storico anche dopo retirement. |

## Interfaces

| Interface | Direction | Description |
|---|---|---|
| CAP-002 Observation Scheduling | Outbound | Disponibilita, constraint e resource assignment. |
| CAP-001 Observation Session Management | Outbound | Equipment readiness, configuration and health state. |
| Observatory Safety | Outbound | Safety-critical state and health evidence. |
| Maintenance Portal | Bidirectional | Maintenance record and lifecycle updates. |
| Engineering Portal | Outbound | Technical and configuration evidence. |
| Knowledge Framework | Bidirectional | Canonical entity and traceability alignment. |
| CAP-000 | Outbound | Status, readiness, version and artefact links. |
| REL-000 | Outbound | Release readiness evidence. |

## Dependencies

- Enterprise Architecture Application and Data Architecture for registry boundary.
- Knowledge Framework for Equipment, Configuration, Engineering Asset and Maintenance Activity concepts.
- CAP-001 and CAP-002 for consumption of equipment readiness.
- Observatory Safety for safety critical behavior.
- GitHub/MkDocs repository for authoritative documentation.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Equipment identity | Yes | Identifier, name, type and owner. |
| Location | Yes when applicable | Physical or logical location. |
| Configuration | Yes for operational assets | Versioned configuration evidence. |
| Firmware / Driver | Yes when applicable | Logical dependency evidence. |
| Health status | Yes for operational readiness | Unknown is allowed only before verification. |
| Maintenance evidence | Yes when maintenance occurs | Linked to lifecycle and state. |
| Assignment context | Yes when asset is consumed | Links to CAP-001, CAP-002 or other capability. |

## Outputs

| Output | Consumer |
|---|---|
| Equipment record | Engineering, Operations, Maintenance. |
| Verified configuration | CAP-001, CAP-002, Engineering. |
| Availability/health evidence | Scheduling and session preparation. |
| Configuration mismatch record | Engineering and recovery. |
| Maintenance record | Maintenance Portal, Safety and Engineering. |
| Retirement record | Knowledge Framework and audit. |

## Operational Considerations

- Equipment state `Unknown`, `Offline`, `Maintenance`, `Retired` or `Archived` must not be treated as available.
- Configuration mismatch blocks operational assignment until resolved or explicitly accepted by governed decision.
- Safety-critical equipment changes must be visible to Observatory Safety.
- Logical equipment groups must not hide individual asset health or lifecycle state.
- Driver and firmware records are evidence, not executable software artefacts.

## Configuration Governance

- Every active configuration has a version or effective reference.
- Updates preserve previous configuration evidence.
- Firmware and driver changes require verification before operational availability.
- Configuration changes affecting CAP-001 or CAP-002 require traceability update.
- Open decisions remain for future physical storage, identifier pattern and telemetry ingestion.

## Related Documents

- `business-process.md`
- `requirements.md`
- `data-model.md`
- `adr/EQR-ADR-001-authoritative-registry.md`
- `adr/EQR-ADR-002-equipment-state-model.md`
- `test-plan.md`
- `acceptance-criteria.md`
- `traceability.md`
