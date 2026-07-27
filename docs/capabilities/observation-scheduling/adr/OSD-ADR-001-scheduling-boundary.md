# OSD-ADR-001 - Scheduling Boundary

| Campo | Valore |
|---|---|
| ADR | `OSD-ADR-001` |
| Capability | CAP-002 Observation Scheduling |
| Stato | Accepted |
| Data | 2026-07-27 |
| Owner | Lead Solution Architect |
| Related Architecture | EA Application Architecture / CAP-001 |

## Context

Observation Scheduling prepara schedule approvate e pubblicate. Observation Session Management governa preparazione, esecuzione, recovery e chiusura della sessione osservativa. Senza un confine esplicito, la futura implementazione rischierebbe di duplicare responsabilita, bypassare CAP-001 o introdurre controllo diretto non governato verso N.I.N.A. e dispositivi.

## Decision

CAP-002 e responsabile della pianificazione fino alla pubblicazione della Scheduled Observation. CAP-001 resta responsabile dell'esecuzione della sessione osservativa e del relativo Session Manifest.

CAP-002 non controlla direttamente N.I.N.A., ASCOM, Alpaca, CPWI, PHD2 o dispositivi. Queste interazioni restano nel perimetro operativo di CAP-001 e delle capability tecniche correlate.

## Consequences

- La schedule approvata e il confine di handover verso CAP-001.
- Session execution, abort, recovery e close non appartengono a CAP-002.
- CAP-002 puo usare evidenza di meteo, safety, target e risorse, ma non ne diventa owner.
- Qualsiasi futura automazione dovra preservare questo confine o proporre nuovo ADR governato.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| Scheduler controlla direttamente sessioni e dispositivi | Duplica CAP-001 e indebolisce la governance della sessione. |
| Scheduler produce solo lista target non approvata | Non genera evidenza sufficiente per handover e audit. |
| Scheduler ingloba Target/Equipment Registry | Sposta ownership dati fuori dai domini gia definiti. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: operational risk and safety constraints.
- Enterprise Architecture: Scheduler, Observation Session Manager, Integration Architecture.
- Knowledge Framework: Observation Request, Observation Session, Documentation Asset.
- CAP-000: `CAP-SCH-001`.
- REL-000: ADR artefact and readiness evidence.
