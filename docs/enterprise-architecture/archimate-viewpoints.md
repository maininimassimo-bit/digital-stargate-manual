# DSG-EA-AVP-001 - ArchiMate Viewpoints

| Campo | Valore |
|---|---|
| Documento | ArchiMate Viewpoints |
| Stato | Proposed refinement |
| Versione | 0.1 |
| Data | 2026-07-27 |
| Fonte gerarchica | `DSG-MR-001` |

## Scopo

Organizzare l'Enterprise Architecture Digital StarGate secondo viewpoint ArchiMate adattati al dominio osservativo, senza introdurre strumenti o repository esterni. I viewpoint sono descrittivi e usano Mermaid/tabelle nei documenti Markdown.

## Viewpoint Catalog

| Viewpoint | Purpose | Primary document | Key elements | Traceability |
|---|---|---|---|---|
| Business | Mission, capability, servizi, stakeholder, value stream | [Business Architecture](business-architecture.md) | Business Actor, Role, Service, Function, Value Stream | Roadmap Operations/Data/Documentation; DSRA target/reference |
| Application | Servizi applicativi e dipendenze | [Application Architecture](application-architecture.md) | Application Component, Service, Interface, Data Object | ADR-001/002/003/004, SOP, manuals |
| Information | Oggetti informativi e relazioni dati | [Data Architecture](data-architecture.md) | Business Object, Data Object, Representation, Meaning | Data roadmap, DSRA data lineage, ADR-003 |
| Technology | Nodi, dispositivi, rete e deployment | [Technology Architecture](technology-architecture.md) | Node, Device, System Software, Communication Network, Artifact | DSRA PC/EAGLE separation, manuals 5-14, 21 |
| Security/Motivation | Driver, requisiti, vincoli e controlli | [Security Architecture](security-architecture.md), [Architecture Decision Catalog](architecture-decision-catalog.md) | Driver, Goal, Requirement, Constraint, Assessment | Governance, DSRA, ADR, open decisions |
| Integration/Cross-layer | Relazioni tra business, app, tecnologia e dati | [Integration Architecture](integration-architecture.md) | Serving, Access, Flow, Triggering | Integration catalog, manuals, SOP |
| Implementation & Migration | Plateau, gaps, roadmap e release evidence | [Repository Map](repository-map.md), [Observability Architecture](observability-architecture.md) | Work Package, Deliverable, Plateau, Gap | DSG-MR-001, assessments, release docs |

## Business Viewpoint

```mermaid
flowchart TD
    STK[Stakeholders] --> CAP[Business Capabilities]
    CAP --> VS[Value Streams]
    VS --> BS[Business Services]
    BS --> APP[Application Services]
```

Focus: Operate Observatory, Prepare Observation, Acquire Scientific Data, Calibrate Data, Process Images, Validate Results, Publish Results, Preserve Knowledge, Support Engineering, Support Scientific Research, Continuous Improvement.

## Application Viewpoint

```mermaid
flowchart TD
    SCH[Scheduler] --> OSM[Observation Session Manager]
    OSM --> OC[Observatory Control]
    OC --> NINA[N.I.N.A.]
    NINA --> ASCOM[ASCOM]
    NINA --> PHD2[PHD2]
    NINA --> ASTAP[ASTAP]
    OC --> DP[Data Platform]
    DP --> ANL[Analytics]
    DP --> KG[Knowledge Graph TBD]
    KG --> AI[AI Assistant TBD]
    DOC[Documentation Platform] --> PORTALS[Science / Engineering / Maintenance Portals]
```

Focus: application services and their provided/consumed services.

## Information Viewpoint

```mermaid
flowchart LR
    REQ[Observation Request] --> SES[Observation Session]
    SES --> RAW[Raw Images]
    RAW --> CAL[Calibration / Registration / Integration]
    CAL --> PROD[Scientific Products]
    SES --> MAN[Observation Manifest]
    MAN --> CAT[Observation Catalog]
    CAT --> KG[Knowledge Graph TBD]
    PROD --> PUB[Publication]
    CAT --> ARC[Archive]
```

Focus: lifecycle and relationships of data objects.

## Technology Viewpoint

```mermaid
flowchart TD
    OP[Remote Operator] --> VPN[VPN]
    VPN --> RUT[RUT955]
    RUT --> EAGLE[EAGLE / Windows]
    EAGLE --> APPS[N.I.N.A. / ASCOM / CPWI / PHD2 / ASTAP]
    APPS --> DEV[CGX-L / Cameras / Focusers / Filters]
    EAGLE --> PC[PC Principale]
    PC --> GH[GitHub / MkDocs / Pages]
    PC --> STG[NAS / Cloud Storage TBD]
```

Focus: nodes, devices, networks and artifacts.

## Motivation Viewpoint

```mermaid
flowchart TD
    DRV[Drivers: safety, lineage, knowledge] --> GOAL[Goals]
    GOAL --> REQ[Requirements]
    REQ --> CON[Constraints]
    CON --> DEC[ADR / OPEN Decisions]
    DEC --> CTRL[Controls / Quality Gates]
```

Focus: why architectural elements exist and which constraints govern them.

## Implementation & Migration Viewpoint

```mermaid
flowchart LR
    ASIS[AS-IS: manuals, EAGLE, MkDocs, analytics] --> TRANS[Transition: EA layers, manifest, catalog, observability]
    TRANS --> TOBE[TO-BE: KG, AI Assistant, scheduler governance]
    TRANS --> REL[Release Evidence]
    TRANS --> ASM[Assessments]
```

Focus: movement from AS-IS to Transition to TO-BE without bypassing roadmap freeze.

## Cross-Reference Matrix

| Element | Business | Application | Data | Technology | Security | Integration | Observability |
|---|---|---|---|---|---|---|---|
| Observation Session | Value stream | Session Manager | Manifest/metadata | EAGLE/N.I.N.A. | safety controls | N.I.N.A./ASCOM/PHD2 | logs/health checks |
| Raw Images | Acquire Scientific Data | Imaging Pipeline | Raw Image object | EAGLE/storage | backup protection | file sync | file count/hash |
| Weather Safety | Operate Observatory | Observatory Control | weather evidence | Weather Station/AllSky | UNKNOWN unsafe | sensor integration | alerts/recovery |
| Publication | Publish Results | Documentation/Portal | Scientific Product | GitHub/MkDocs | no secrets | GitHub/Pages | build/link evidence |
| Knowledge Graph | Preserve Knowledge | KG service TBD | graph object | storage TBD | data governance | KG/OpenAI TBD | provenance checks |

## No External Tooling Requirement

The viewpoint models are maintained as Markdown, Mermaid and tables. Any future adoption of ArchiMate tooling is an OPEN decision and cannot be required by this baseline.