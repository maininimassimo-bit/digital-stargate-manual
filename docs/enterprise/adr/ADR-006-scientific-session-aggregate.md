# ADR-006 - Scientific Session Aggregate

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | 2026-07-28 |
| Decisione | Scientific Session come aggregato principale |

## Contesto

Log, telemetria, immagini, metadati, report e processing devono essere correlati in modo stabile.

## Decisione

La Scientific Session è l'entità principale che collega l'intero ciclo osservativo e scientifico.

## Conseguenze

- ogni record deve poter essere associato a una sessione o marcato come non correlato;
- repository, dashboard, AI e workflow usano lo stesso identificativo di sessione;
- il modello dati deve preservare la cronologia degli stati.
