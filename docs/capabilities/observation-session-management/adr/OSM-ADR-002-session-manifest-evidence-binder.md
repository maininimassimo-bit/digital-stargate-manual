# OSM-ADR-002 - Session Manifest as Evidence Binder

| Campo | Valore |
|---|---|
| ADR | `OSM-ADR-002` |
| Stato | Accepted with Open Schema Decision |
| Capability | Observation Session Management |
| Data | 2026-07-27 |
| Fonte gerarchica | `DSG-MR-001` -> DSRA -> Enterprise Architecture -> Knowledge Framework -> Design System |
| Related decisions | `ADR-001`, `EA-OAD-004`, `OSM-ODD-001` |

## Context

Data Architecture identifica `Observation Manifest` / `Session Manifest` come oggetto informativo che collega sessione, raw images, log, metadata, catalogo e archive. Il Knowledge Framework conferma `Session Manifest` come entita canonica, ma lo schema finale resta open.

La capability deve poter definire procedure e test senza inventare uno schema database o un formato finale.

## Decision

Observation Session Management usa il Session Manifest come evidence binder concettuale della sessione.

Il manifest shall bind, at conceptual level:

- session identifier;
- observation request or operator intent;
- target reference;
- equipment configuration reference;
- weather snapshot;
- safety state;
- raw image references;
- logs and execution events;
- session result;
- archive and knowledge update status.

Il formato, lo storage e lo schema esatto restano open e devono essere definiti tramite decisione architetturale futura.

## Consequences

| Area | Consequence |
|---|---|
| SOP | Le procedure possono richiedere manifest draft/verified/archived senza definire formato tecnico. |
| Runbook | Recovery deve preservare o ricostruire evidenze manifest quando possibile. |
| Data | Catalogo e archive consumano il manifest come riferimento logico. |
| Tests | Acceptance tests verificano presenza e coerenza concettuale, non formato implementativo. |
| Open decisions | `EA-OAD-004` e `OSM-ODD-001` restano aperte. |

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Definire schema manifest completo ora | Violerebbe il vincolo di non inventare dettagli implementativi. |
| Non usare manifest | Contraddirebbe Data Architecture, Domain Model e ADR-001. |
| Usare solo report testuali | Non garantisce tracciabilita completa di file, log, metadata e archive. |

## Open Decision

| ID | Decision | Owner | Required input |
|---|---|---|---|
| `OSM-ODD-001` | Final Session Manifest schema | Data Owner | Schema, identifier convention, storage decision, checksum policy. |

## Compliance

Questo ADR preserva la baseline enterprise e non modifica decisioni esistenti.