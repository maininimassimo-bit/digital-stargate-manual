# TGT-ADR-001 - Authoritative Target Model

| Campo | Valore |
|---|---|
| ADR | `TGT-ADR-001` |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Accepted |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect |
| Related Architecture | EA Application/Data Architecture |

## Context

Digital StarGate needs stable target representation across scheduling, session management, data platform, knowledge graph, analytics and science publication. External catalogues provide identifiers and scientific evidence, but the platform needs a governed internal target model to avoid inconsistent target handling.

## Decision

CAP-TGT-001 Target Registry is the authoritative conceptual model for astronomical targets managed by Digital StarGate. It governs internal target identity, lifecycle, metadata, constraints and references to external catalogues.

External catalogues are referenced as evidence and identifiers. They do not replace the internal target model and no specific catalogue provider is selected by this ADR.

## Consequences

- CAP-SCH-001 consumes targets from the Target Registry for scheduling.
- CAP-OSM-001 consumes published target context for session management.
- Data Platform and Knowledge Graph can link observations to stable target identity.
- Future implementation must preserve this authority model or propose a governed ADR.
- Catalogue import, storage and provider choices remain open implementation decisions.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| Use external catalogue identifiers directly as internal authority | Creates provider dependency and weak governance for custom/moving targets. |
| Maintain target lists inside scheduling only | Duplicates target state and weakens session/data traceability. |
| Select a catalogue provider now | Unsupported by current repository evidence and outside documentation scope. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: data quality and operational risk context.
- Enterprise Architecture: Target Registry in Application/Data Architecture.
- Knowledge Framework: Target, Target Registry, Observation Catalog.
- CAP-000: `CAP-TGT-001`.
- REL-000: ADR artefact and readiness evidence.
