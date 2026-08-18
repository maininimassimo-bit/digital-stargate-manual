# SOP - Recover Observation Session

| Campo | Valore |
|---|---|
| SOP | `OSM-SOP-004` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | Observability Architecture, Technical Manuals, Runbooks |

## Purpose

Ripristinare una sessione o consolidarne le evidenze dopo failure operativa, mantenendo safety e tracciabilita.

## Trigger

- Sessione abortita.
- Failure recuperabile durante preparazione o acquisizione.
- Log, immagini o manifest incompleti ma disponibili in forma parziale.

## Procedure

1. Confermare che la condizione unsafe sia risolta o contenuta.
2. Identificare runbook applicabile.
3. Classificare failure: scheduler, weather, roof, camera, mount, N.I.N.A., ASCOM, emergency.
4. Preservare log, raw images e screenshot/evidenze disponibili.
5. Verificare stato equipment e configurazione.
6. Decidere se riprendere, rinviare o chiudere la sessione.
7. Aggiornare Session Manifest o gap documentale.
8. Registrare maintenance activity se richiesta.
9. Passare a Execute Session se ripresa autorizzata o Close Session se chiusura necessaria.

## Outputs

- Recovery decision documentata.
- Evidenze preservate.
- Stato sessione aggiornato.
- Eventuale maintenance activity.

## Controls

- Recovery non deve bypassare weather/safety validation.
- Nessuna configurazione deve essere modificata senza evidenza.
- Decisioni non risolte diventano open decisions o maintenance follow-up.
