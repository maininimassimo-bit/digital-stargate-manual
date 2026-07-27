# OSD-ADR-002 - Priority Resolution

| Campo | Valore |
|---|---|
| ADR | `OSD-ADR-002` |
| Capability | CAP-002 Observation Scheduling |
| Stato | Accepted with Open Policy Detail |
| Data | 2026-07-27 |
| Owner | Lead Solution Architect |
| Related Architecture | EA Business/Application Architecture |

## Context

Observation Scheduling deve risolvere conflitti tra richieste, finestre astronomiche, risorse disponibili, condizioni meteo e vincoli safety. Il repository non definisce ancora un modello numerico completo di scoring scientifico o operativo.

## Decision

La risoluzione delle priorita deve essere deterministica, documentata e auditabile. Safety e weather safe hanno precedenza assoluta rispetto alla priorita scientifica o operativa.

Quando il modello di scoring non e definito, la schedule resta in stato `Conflict` o `Pending Approval` e richiede decisione esplicita dell'owner autorizzato. La decisione deve produrre Approval Record o Conflict Record con razionale.

## Consequences

- Nessuna schedule unsafe puo essere approvata per effetto della priorita.
- Ogni conflitto richiede evidenza di risoluzione o cancellazione.
- Il modello di scoring dettagliato resta Open Architectural Decision finche non approvato.
- La futura implementazione dovra rendere visibile la motivazione della priorita.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| First-in first-out | Non rispetta necessariamente valore scientifico, finestre critiche o condizioni operative. |
| Scoring completamente automatico ora | Non supportato da evidenza repository sufficiente. |
| Priorita manuale non tracciata | Non soddisfa audit, knowledge e release governance. |

## Open Policy Detail

| Decision | Reason | Required Input |
|---|---|---|
| Final numerical scoring model | Non definito nei documenti approvati. | Science/Operations priority policy. |
| Tie-break hierarchy | Non ancora formalizzata. | Governed ADR or SOP update. |
| Alerting on high-priority conflict | Dipende da notification policy futura. | Operations decision. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: safety and continuity risk.
- Enterprise Architecture: Scheduler and Observability Architecture.
- Knowledge Framework: Requirements Repository and Traceability Matrix.
- CAP-000: `CAP-SCH-001`.
- REL-000: ADR artefact and readiness evidence.
