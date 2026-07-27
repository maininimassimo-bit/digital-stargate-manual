# OSM-ADR-001 - Observation Session Governance Boundary

| Campo | Valore |
|---|---|
| ADR | `OSM-ADR-001` |
| Stato | Accepted |
| Capability | Observation Session Management |
| Data | 2026-07-27 |
| Fonte gerarchica | `DSG-MR-001` -> DSRA -> Enterprise Architecture -> Knowledge Framework -> Design System |
| Related enterprise ADR | `ADR-001 - Session Layer` |

## Context

Enterprise Architecture identifica `Observation Session Manager` come servizio applicativo di transizione e `Observation Session` come unita di tracciabilita. `ADR-001 - Session Layer` stabilisce che i metadati di sessione sono fonte autorevole per analytics, warehouse, dashboard e report.

La capability Observation Session Management deve produrre documentazione completa senza ridefinire l'architettura enterprise.

## Decision

Observation Session Management adotta la sessione osservativa come confine governato della capability.

Il confine include:

- readiness e preparazione sessione;
- validazione equipment, weather e safety;
- esecuzione tramite strumenti gia documentati;
- acquisizione immagini;
- consolidamento di log, metadata e manifest;
- chiusura, archive readiness e knowledge update.

Il confine non include:

- implementazione software;
- definizione di database;
- creazione di API;
- redesign UI;
- modifica di Enterprise Architecture, Knowledge Framework o Design System.

## Consequences

| Area | Consequence |
|---|---|
| Architecture | La capability consuma Application/Data/Technology/Observability Architecture senza modificarle. |
| Knowledge | Entita e stati derivano dal Domain Model e Canonical Information Model. |
| SOP | Procedure operative sono organizzate attorno al lifecycle della sessione. |
| Runbook | Recovery e failure mode sono collegati allo stato della sessione. |
| Future implementation | Ogni sviluppo futuro dovra implementare capability-by-capability sotto governance. |

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Gestire la sessione solo come cartella file | Gia insufficiente secondo ADR-001 per timezone, durata, stato e appartenenza file. |
| Definire un nuovo orchestration layer | Sarebbe nuova architettura e violerebbe l'obiettivo del task. |
| Spostare la capability nel Design System | Il Design System governa UI, non processo operativo e dati sessione. |

## Compliance

Questo ADR e conforme a:

- `docs/architecture/ADR-001-Session-Layer.md`;
- `docs/enterprise-architecture/EA-000-enterprise-architecture-baseline.md`;
- `docs/knowledge/domain-model.md`;
- `docs/design-system/DSG-DS-001-design-system-baseline.md`.
