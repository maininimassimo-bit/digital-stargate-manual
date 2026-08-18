# SOP - Close Observation Session

| Campo | Valore |
|---|---|
| SOP | `OSM-SOP-005` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | Data Architecture, Knowledge Framework, Release Documentation |

## Purpose

Chiudere una sessione osservativa consolidando dati, manifest, log, archive readiness e aggiornamento conoscenza.

## Trigger

- Sequenza completata.
- Sessione abortita ma stabilizzata.
- Operatore decide chiusura per fine finestra, meteo o safety.

## Procedure

1. Confermare acquisizione completata, abortita o rinviata.
2. Verificare presenza raw images e log disponibili.
3. Aggiornare Session Manifest a `Verified` se possibile o registrare gap.
4. Registrare Session Result: outcome, conteggio immagini, stato qualita, archive state.
5. Preparare package per archive secondo regole disponibili.
6. Collegare sessione a Observation Catalog quando disponibile.
7. Aggiornare knowledge: runbook usati, incidenti, open decisions, maintenance activity.
8. Registrare acceptance o follow-up.
9. Marcare sessione `Archived`, `Closed with Gaps` o `Recovery Required`.

## Outputs

- Sessione chiusa.
- Manifest verificato o gap esplicito.
- Archive readiness documentata.
- Knowledge update registrato.

## Controls

- Non pubblicare prodotti senza metadata minimi.
- Non cancellare raw evidence durante chiusura.
- Gap e dati mancanti devono essere espliciti.
