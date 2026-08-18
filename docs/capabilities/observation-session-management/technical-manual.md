# Observation Session Management - Technical Manual

| Campo | Valore |
|---|---|
| Manuale | `OSM-MAN-001` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte gerarchica | `DSG-MR-001` -> DSRA -> Enterprise Architecture -> Knowledge Framework -> Design System |

## Purpose

Questo manuale descrive responsabilita, interfacce, integrazioni, configurazione, dipendenze e note operative della capability. Non e una guida di implementazione software.

## Responsibilities

| Responsibility | Description | Owner |
|---|---|---|
| Session readiness | Confermare request, target, equipment, weather e safety. | Operations Owner |
| Session execution evidence | Collegare eventi, acquisizione, log e stato. | Operations Owner |
| Manifest governance | Gestire manifest come evidence binder concettuale. | Data Owner |
| Equipment readiness | Confermare configurazioni e asset disponibili. | Engineering Owner |
| Recovery coordination | Applicare runbook e registrare failure. | Operations/Engineering Owner |
| Knowledge update | Aggiornare catalogo, gap, incidenti e riferimenti documentali. | Knowledge Architect |

## Interfaces

| Interface | Direction | Data exchanged | Governance reference |
|---|---|---|---|
| Scheduler | Inbound | Observation Request, target, plan, constraints. | Application Architecture |
| Target Registry | Inbound | Target identity, coordinates, priority. | Data Architecture, Knowledge Framework |
| Equipment Registry | Inbound | Equipment profile, configuration, status. | Application/Data Architecture |
| N.I.N.A. | Outbound/inbound | Sequence execution, image acquisition, logs. | Integration Architecture, ADR-001 |
| ASCOM/Alpaca | Outbound/inbound | Device state and commands. | Integration Architecture |
| CPWI | Outbound/inbound | Mount state and control. | Technology/Integration Architecture |
| PHD2 | Inbound/outbound | Guiding state and events. | Integration Architecture |
| Weather Station / AllSky | Inbound | Weather and sky state evidence. | Observability Architecture |
| Data Platform | Outbound | Manifest, metadata, raw image references, session result. | Data Architecture |
| Documentation Platform | Outbound | SOP/runbook/test/release evidence. | Repository Map |

## Integrations

| Integration | Operational note |
|---|---|
| N.I.N.A. | Primary session execution context. Failures use N.I.N.A. runbook. |
| ASCOM/Alpaca | Device abstraction layer. Failure affects readiness and execution. |
| CPWI | Mount control context. Mount state must be known before acquisition. |
| PHD2 | Guiding context. Guiding failure affects image quality and session continuation. |
| ASTAP | Plate solving support where present in workflow. |
| PixInsight | Downstream processing integration after session closure. |
| AllSky | Visual sky-state evidence; supports weather/safety validation. |
| Weather Station | Weather safe/unsafe source; stale or missing data is treated as risk. |
| Cloud Storage/NAS | Archive and backup target according to architecture decisions. |
| GitHub/MkDocs | Capability documentation and release evidence. |

## Configuration

Configuration is conceptual and governed by existing manuals and registries.

| Configuration type | Description | Source |
|---|---|---|
| Equipment profile | Instrument, camera, mount, filter and guider context. | Equipment Registry / manuals. |
| Software profile | N.I.N.A., ASCOM, CPWI, PHD2, ASTAP configuration references. | Technical manuals. |
| Session profile | Target, exposure, filter, sequence and constraints. | Scheduler / Observation Request. |
| Safety profile | Weather, roof, mount, power, network and remote access readiness. | Observability/Security Architecture. |
| Archive profile | Destination and preservation rules. | Data/Technology Architecture. |

## Dependencies

- Enterprise Architecture Baseline `EA-000`.
- ADR-001 Session Layer.
- Data Architecture information objects.
- Knowledge Framework domain model and traceability matrix.
- Design System for future UI representation.
- Existing operational manuals for N.I.N.A., ASCOM, CPWI, PHD2, EAGLE and observatory operations.

## Operational Notes

- Safety state is authoritative over acquisition objective.
- Missing weather evidence is operational risk, not success.
- Partial sessions remain valid evidence if preserved and documented.
- Manifest schema remains open; procedures refer to manifest states conceptually.
- No credentials, tokens or secrets may be recorded in session documentation.
- Future UI must use session cards, weather cards, equipment cards, alerts and dashboard patterns from the Design System.

## Maintenance

Capability documentation must be reviewed when:

- ADR-001 is superseded;
- Session Manifest schema is approved;
- Scheduler or registry decisions are approved;
- observatory equipment or control software changes materially;
- incident post-mortem identifies procedure or runbook gaps;
- Design System changes affect session UI patterns.
