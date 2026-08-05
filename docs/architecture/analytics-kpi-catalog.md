# ANA-KPI-001 — Analytics KPI Catalog

| Campo | Valore |
|---|---|
| Identificativo | ANA-KPI-001 |
| Package | AP-011 |
| Stato | Initial governed catalog |
| Data | 30/07/2026 |

## Governance rules

Ogni KPI deve avere identificatore, nome, scopo, formula, grain, dimensioni, unità, owner, sorgenti, quality dependencies, freshness, soglie, consumer, versione e stato.

Gli stati sono `candidate`, `proposed`, `approved`, `active`, `deprecated`, `retired`.

## Candidate KPI set

| ID | KPI | Formula / significato | Grain | Stato |
|---|---|---|---|---|
| KPI-001 | Observation Success Rate | sessioni completate / sessioni avviate | periodo, target, setup | Candidate |
| KPI-002 | Usable Exposure Rate | esposizioni accettate / esposizioni acquisite | sessione, filtro | Candidate |
| KPI-003 | Median FWHM | mediana FWHM su frame validi | sessione, target, filtro | Candidate |
| KPI-004 | Guiding RMS | RMS guida aggregato con copertura dichiarata | sessione | Candidate |
| KPI-005 | Weather Data Freshness | età dell'ultima misura valida | sorgente | Candidate |
| KPI-006 | Pipeline Success Rate | run pipeline riuscite / run totali | pipeline, periodo | Candidate |
| KPI-007 | Data Quality Pass Rate | record passati / record valutati | dataset, versione | Candidate |
| KPI-008 | Data Product Freshness | ritardo rispetto al target di pubblicazione | data product | Candidate |
| KPI-009 | Storage Growth Rate | variazione capacità usata nel periodo | storage class | Candidate |
| KPI-010 | Backup Age | tempo dall'ultimo backup valido | capability | Candidate |
| KPI-011 | Restore Evidence Age | tempo dall'ultimo restore verificato | capability | Candidate |
| KPI-012 | Equipment Alert Frequency | alert per tempo operativo | asset, severity | Candidate |

## Publication requirements

Ogni visualizzazione KPI mostra almeno:

- definizione e versione;
- intervallo temporale;
- ultimo aggiornamento e freshness;
- data quality status;
- record inclusi, esclusi o mancanti;
- unità e timezone;
- owner o contatto operativo.

## Safety restriction

I KPI descrivono stato storico o derivato. Non sono condizioni safety real-time, non autorizzano apertura/chiusura e non sostituiscono sensori o interlock.

## Open decisions

- owner dei KPI;
- formule finali e soglie;
- aggregazioni e percentile standard;
- gestione sessioni parziali;
- unità canoniche;
- target freshness e retention.