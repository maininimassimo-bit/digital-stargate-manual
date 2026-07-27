# CAP-TGT-001 - Technical Manual

## Purpose

Il manuale tecnico descrive responsabilita, interfacce, dipendenze, input, output, considerazioni operative e target governance del Target Registry. Non prescrive implementazione software.

## Responsibilities

| Area | Responsibility |
|---|---|
| Target identity | Mantenere canonical name, aliases and identity status. |
| Catalogue association | Collegare riferimenti esterni senza sostituire cataloghi. |
| Coordinate governance | Registrare coordinate, epoch and coordinate system where applicable. |
| Scientific classification | Governare target type, classification and metadata. |
| Observation constraints | Registrare constraints utili a scheduling and session preparation. |
| Publication status | Rendere disponibili solo target validati and approved. |
| Historical preservation | Conservare alias, updates, retirement and observation history references. |

## Interfaces

| Interface | Direction | Description |
|---|---|---|
| CAP-SCH-001 Observation Scheduling | Outbound | Target identity, constraints, priority and visibility profile. |
| CAP-OSM-001 Observation Session Management | Outbound | Published target context and coordinate evidence. |
| CAP-EQR-001 Equipment Registry | Indirect | Equipment compatibility evidence consumed through scheduling/session planning. |
| Data Platform / Observation Catalog | Bidirectional | Observation history and product references. |
| Knowledge Framework | Bidirectional | Canonical entity, glossary and traceability alignment. |
| External Catalogues | Inbound reference | Catalogue identifiers and scientific evidence. |
| CAP-000 | Outbound | Status, maturity, readiness, version and artefact links. |
| REL-000 | Outbound | Release readiness evidence. |

## Dependencies

- Enterprise Architecture Application and Data Architecture for Target Registry boundary.
- Knowledge Framework for Target, Target Registry and Observation Catalog concepts.
- CAP-SCH-001 for scheduling consumption.
- CAP-OSM-001 for session consumption.
- CAP-EQR-001 for equipment compatibility context.
- External catalogue evidence, without provider lock-in.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Proposed target name | Yes | Initial name or custom designation. |
| Catalogue reference | When available | Messier, NGC, IC or other reference. |
| Coordinates / ephemeris reference | Required where applicable | Static or moving target evidence. |
| Epoch/reference frame | Required with coordinates | Needed for unambiguous position. |
| Target type | Yes before publication | Controlled classification. |
| Observation constraints | When applicable | Used by scheduling. |
| Priority rationale | When applicable | Used by scheduling priority resolution. |
| Observation history | When available | Linked after observations exist. |

## Outputs

| Output | Consumer |
|---|---|
| Published Target record | CAP-SCH-001 and CAP-OSM-001. |
| Target Identity and aliases | Knowledge Framework and Data Platform. |
| Catalogue references | Science and analytics consumers. |
| Coordinates and epoch | Scheduling and session preparation. |
| Observation constraints | CAP-SCH-001. |
| Visibility profile | CAP-SCH-001. |
| Retirement record | Knowledge Framework and audit. |

## Operational Considerations

- Duplicate target risk is managed before publication.
- Invalid coordinates block scheduling use.
- External catalogue updates may require registry review but do not automatically rewrite internal identity.
- Moving targets require explicit handling and remain open for future implementation decisions.
- Custom targets must be clearly marked and traceable.

## Target Governance

- Canonical identity is governed by CAP-TGT-001.
- Catalogue references are evidence, not internal identity authority.
- Updates preserve previous names, aliases and coordinates where relevant.
- Publication requires validation and approval evidence.
- Retirement removes target from new scheduling but preserves history.

## Related Documents

- `business-process.md`
- `requirements.md`
- `data-model.md`
- `adr/TGT-ADR-001-authoritative-target-model.md`
- `adr/TGT-ADR-002-canonical-target-identity.md`
- `test-plan.md`
- `acceptance-criteria.md`
- `traceability.md`
