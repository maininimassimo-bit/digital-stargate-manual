# ADR-007 - Event-Driven Immutable Telemetry

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | 2026-07-28 |
| Decisione | Eventi normalizzati e telemetria grezza immutabile |

## Contesto

La piattaforma deve poter ricostruire cosa è accaduto senza perdere il dato originale.

## Decisione

I record grezzi vengono conservati senza modifica. Parsing, normalizzazione e arricchimento generano dati derivati versionati.

## Conseguenze

- audit e riproducibilità migliorano;
- gli errori dei parser possono essere corretti senza alterare la fonte;
- aumenta il fabbisogno di storage e retention;
- i contratti evento devono essere versionati.
