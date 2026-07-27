# DOM-001 - Core Observatory Domain Blueprint

| Campo | Valore |
|---|---|
| Documento | Core Observatory Domain Blueprint |
| ID | `DOM-001` |
| Stato | Domain Blueprint Baseline |
| Versione | 0.1 |
| Owner | Enterprise Domain Architect |
| Fonte gerarchica | `DSG-MR-001` -> DSRA -> `EA-000` -> Knowledge Framework -> Design System -> `CAP-000` -> `REL-000` -> Domain Blueprints -> Capability Packages |
| Capability incluse | `CAP-OSM-001`, `CAP-SCH-001`, `CAP-EQR-001`, `CAP-TGT-001`, `CAP-WEA-001` |

## Purpose

Il Core Observatory Domain Blueprint consolida le capability documentate che governano il nucleo operativo dell'osservatorio Digital StarGate: target, equipment, weather monitoring, scheduling and observation session management.

Il blueprint non introduce nuova architettura, non ridefinisce confini capability e non crea capability aggiuntive. Rende esplicita la collaborazione tra capability gia approvate e documentate nel repository.

## Scope

Incluso:

- consolidamento del dominio Core Observatory;
- responsabilita e confini del dominio;
- capability gia documentate e loro maturity/readiness;
- collaborazione tra `CAP-TGT-001`, `CAP-SCH-001`, `CAP-EQR-001`, `CAP-WEA-001` and `CAP-OSM-001`;
- interazioni concettuali con Acquisition, Data Platform, Knowledge and Experience domains;
- interfacce concettuali del dominio;
- governance, KPI documentali and traceability.

Escluso:

- nuova architettura enterprise;
- nuovi servizi, API, database, frontend or backend;
- ridefinizione dei capability package esistenti;
- dettaglio interno di Acquisition, Data Platform, Knowledge or Experience domains;
- documentazione di Observatory Safety oltre al riferimento come evoluzione futura.

## Business Value

- Allinea target, equipment, weather, schedule and session come nucleo operativo unico.
- Riduce ambiguita tra capability gia documentate.
- Fornisce una vista di dominio per governance, release and traceability.
- Supporta futura implementazione capability-by-capability senza cambiare baseline.
- Rende evidente quali informazioni devono fluire prima dell'acquisizione dati.

## Domain Responsibilities

| Responsibility | Description | Owning Capability |
|---|---|---|
| Target governance | Gestione identita, catalog references, classification, constraints and lifecycle target. | `CAP-TGT-001` |
| Scheduling governance | Trasformazione di richieste e target in schedule approvate and pubblicate. | `CAP-SCH-001` |
| Equipment governance | Registro autorevole di asset fisici/logici, configuration, state and assignments. | `CAP-EQR-001` |
| Weather governance | Valutazione meteo operativa autorevole per schedule, session readiness, suspend/resume and safety evidence. | `CAP-WEA-001` |
| Session governance | Preparazione, esecuzione, recovery, chiusura and manifest della sessione osservativa. | `CAP-OSM-001` |
| Readiness evidence | Evidenza documentale che target, equipment, weather and schedule siano pronti per sessione. | Shared by included capabilities |
| Traceability | Collegamento tra target, schedule, equipment, weather, session and governance artefacts. | Shared by included capabilities |

## Domain Boundaries

### Belongs to Core Observatory

- Target identity and publication for operational use.
- Equipment identity, configuration and lifecycle state.
- Conceptual weather state, weather validation and operational weather decision support.
- Observation scheduling, priority, conflicts and publication.
- Observation session readiness, execution boundary, recovery and close evidence.
- Conceptual handoff from validated target, equipment, weather and schedule to observation session.

### Belongs to Other Domains

| Domain | Boundary |
|---|---|
| Acquisition Domain | Image acquisition execution, raw image creation and acquisition-specific data capture after session execution starts. |
| Data Platform Domain | Storage, cataloguing, lineage, archive and scientific product data governance after observation outputs exist. |
| Knowledge Domain | Semantic relationships, glossary, traceability matrix and knowledge graph model beyond Core Observatory flow. |
| Experience Domain | Portals, dashboards, navigation and UI patterns governed by Design System. |
| Observatory Safety Future Domain Extension | Broader safety orchestration, emergency policy and safety automation remain future governed capability work under `CAP-SAF-001`. |

## Included Capabilities

| Capability | Purpose | Responsibility | Current Maturity | Current Readiness | Dependencies |
|---|---|---|---|---|---|
| `CAP-TGT-001` Target Registry | Single conceptual source of truth for astronomical targets managed by Digital StarGate. | Target identity, catalogue references, coordinates, classifications, constraints, lifecycle. | Documented | Implementation Ready | Knowledge Framework, CAP-SCH-001, CAP-OSM-001, Data Platform. |
| `CAP-SCH-001` Observation Scheduling | Prepare and publish governed observation schedules. | Astronomical windows, resource availability, weather/safety checks, priority resolution, approval, publication. | Documented | Implementation Ready | CAP-TGT-001, CAP-EQR-001, CAP-WEA-001, Observatory Safety, CAP-OSM-001. |
| `CAP-EQR-001` Equipment Registry | Authoritative registry for physical and logical observatory assets. | Equipment identity, type, state, configuration, firmware, drivers, maintenance evidence, assignments. | Documented | Implementation Ready | CAP-SCH-001, CAP-OSM-001, CAP-WEA-001, Observatory Safety, Maintenance Portal, Engineering Portal. |
| `CAP-WEA-001` Weather Monitoring | Authoritative conceptual source for operational weather state. | Weather evidence validation, weather state publication, safety decision support, weather alert and historical weather evidence. | Documented | Implementation Ready | CAP-EQR-001, CAP-SCH-001, CAP-OSM-001, CAP-TGT-001, DSRA, Observatory Safety. |
| `CAP-OSM-001` Observation Session Management | Govern the observation session as the operational, informational and traceability unit. | Session preparation, readiness, execution boundary, manifest, recovery, close and knowledge update. | Documented | Implementation Ready | CAP-SCH-001, CAP-TGT-001, CAP-EQR-001, CAP-WEA-001, N.I.N.A., ASCOM, Data Platform, Weather/Safety. |

## Capability Collaboration

```mermaid
flowchart TD
    TGT[CAP-TGT-001 Target Registry]
    EQR[CAP-EQR-001 Equipment Registry]
    WEA[CAP-WEA-001 Weather Monitoring]
    SCH[CAP-SCH-001 Observation Scheduling]
    OSM[CAP-OSM-001 Observation Session Management]
    TGT -->|published target, constraints, priority| SCH
    EQR -->|availability, configuration, resource state| SCH
    EQR -->|weather source identity and status| WEA
    WEA -->|weather state, caution, unsafe, unknown| SCH
    SCH -->|approved scheduled observation| OSM
    TGT -->|target identity and coordinates| OSM
    EQR -->|verified equipment readiness| OSM
    WEA -->|current weather state and alerts| OSM
    OSM -->|session evidence and observation history| TGT
    OSM -->|equipment usage evidence| EQR
    OSM -->|weather impact evidence| WEA
```

## Domain Context

| External Domain | Interaction |
|---|---|
| Acquisition Domain | Receives an executable observation context from Observation Session Management and produces acquisition outputs. Core Observatory does not define image acquisition internals. |
| Data Platform Domain | Receives session, target, weather and acquisition evidence for catalogue, archive, lineage and data products. Core Observatory does not define storage or warehouse internals. |
| Knowledge Domain | Consumes governance and traceability evidence, and links target/equipment/weather/session concepts to documentation and knowledge graph. Core Observatory does not define graph implementation. |
| Experience Domain | Future UI surfaces may present targets, equipment, weather, schedules and sessions. Core Observatory does not define UI implementation and remains governed by Design System. |

## Domain Information Flow

```mermaid
flowchart TD
    TGT[Target Registry]
    SCH[Observation Scheduling]
    EQR[Equipment Registry]
    WEA[Weather Monitoring]
    OSM[Observation Session Management]
    TGT -->|target identity, constraints, priority| SCH
    EQR -->|resource availability and equipment state| SCH
    EQR -->|weather source context| WEA
    WEA -->|weather state and safety decision support| SCH
    SCH -->|approved schedule| OSM
    EQR -->|verified equipment readiness| OSM
    TGT -->|published target context| OSM
    WEA -->|current weather state and alerts| OSM
```

## Domain Interfaces

| Interface | Provider | Consumer | Type | Description |
|---|---|---|---|---|
| Published Target Context | `CAP-TGT-001` | `CAP-SCH-001`, `CAP-OSM-001` | Conceptual information | Canonical target, coordinates, type, constraints, priority and lifecycle state. |
| Equipment Readiness Context | `CAP-EQR-001` | `CAP-SCH-001`, `CAP-OSM-001` | Conceptual information | Equipment identity, state, configuration, health, assignment and lifecycle. |
| Weather State Context | `CAP-WEA-001` | `CAP-SCH-001`, `CAP-OSM-001`, Observatory Safety | Conceptual information | Weather Snapshot, Operational Assessment, Safety Decision, Weather Alert and monitoring status. |
| Approved Schedule Context | `CAP-SCH-001` | `CAP-OSM-001` | Conceptual handoff | Scheduled Observation, observation window, priority, constraints and approval evidence. |
| Session Evidence Context | `CAP-OSM-001` | Data Platform, Knowledge Domain, CAP-TGT-001, CAP-EQR-001, CAP-WEA-001 | Conceptual evidence | Session result, manifest evidence, target usage, equipment usage and weather impact references. |
| Governance Evidence | All included capabilities | CAP-000, REL-000, Knowledge Framework | Documentation evidence | ADR, SOP, runbook, manual, test, acceptance and traceability links. |

## Governance

This domain blueprint derives from and must remain consistent with:

- `DSG-MR-001` Master Roadmap;
- DSRA;
- `EA-000` Enterprise Architecture Baseline;
- Knowledge Framework;
- `DSG-DS-001` Design System Baseline for any future experience surface;
- `CAP-000` Capability Registry;
- `REL-000` Release Management Baseline;
- capability packages `CAP-OSM-001`, `CAP-SCH-001`, `CAP-EQR-001`, `CAP-TGT-001`, `CAP-WEA-001`.

The blueprint does not change release rules or capability ownership. It only consolidates the newly documented Weather Monitoring package into the existing Core Observatory domain.

## KPIs

Governance KPIs only:

| KPI | Definition | Current Evidence |
|---|---|---|
| Capability Coverage | Included Core Observatory capability packages documented vs expected for this blueprint. | 5 / 5 documented. |
| Documentation Coverage | Required capability package artefacts present for included capabilities. | Overview, process, requirements, mapping, data model, ADR, SOP, runbooks, manual, tests, acceptance, traceability exist for included packages. |
| Traceability Coverage | Included capabilities trace to Roadmap, DSRA, EA, Knowledge, CAP-000 and REL-000. | Present in capability traceability documents. |
| Implementation Readiness | Included capabilities marked Implementation Ready in CAP-000. | 5 / 5 Implementation Ready. |
| Governance Alignment | Domain blueprint does not introduce new capability, architecture or implementation. | This document is consolidation only. |

## Traceability

| Capability | Package | Registry Reference | Release Reference | Domain Role |
|---|---|---|---|---|
| `CAP-TGT-001` Target Registry | `docs/capabilities/target-registry/` | `CAP-000` Target Registry entry | `REL-000` capability reference | Target identity and constraints source. |
| `CAP-SCH-001` Observation Scheduling | `docs/capabilities/observation-scheduling/` | `CAP-000` Observation Scheduling entry | `REL-000` capability reference | Schedule approval and publication. |
| `CAP-EQR-001` Equipment Registry | `docs/capabilities/equipment-registry/` | `CAP-000` Equipment Registry entry | `REL-000` capability reference | Equipment readiness and resource state. |
| `CAP-WEA-001` Weather Monitoring | `docs/capabilities/weather-monitoring/` | `CAP-000` Weather Monitoring entry | `REL-000` capability reference | Weather state, safety decision support and weather evidence. |
| `CAP-OSM-001` Observation Session Management | `docs/capabilities/observation-session-management/` | `CAP-000` Observation Session Management entry | `REL-000` lifecycle rules | Session lifecycle and handoff to acquisition/data. |

## Future Evolution

The following capability is already present in `CAP-000` and naturally extends the Core Observatory domain. It is not documented by this blueprint:

| Capability | CAP-000 Identifier | Note |
|---|---|---|
| Observatory Safety | `CAP-SAF-001` | Future domain extension candidate. |

Future extension must follow the approved governance chain and create capability/domain documentation only through governed release activity.