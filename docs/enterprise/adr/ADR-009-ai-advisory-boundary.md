# ADR-009 - AI Advisory Boundary

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | 2026-07-28 |
| Decisione | L'AI opera come supporto decisionale |

## Contesto

L'AI può analizzare log, sessioni e metriche, ma output probabilistici non devono diventare comandi operativi non verificati.

## Decisione

L'AI può spiegare, sintetizzare, classificare e suggerire. Non invia comandi diretti a dispositivi e non modifica i dati scientifici originali.

## Conseguenze

- ogni output AI deve distinguere evidenze e inferenze;
- modello, versione e sessione devono essere tracciati;
- è prevista revisione umana;
- azioni automatiche future richiederanno ADR e controlli specifici.
