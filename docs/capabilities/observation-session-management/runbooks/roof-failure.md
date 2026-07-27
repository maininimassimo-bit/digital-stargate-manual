# Runbook - Roof Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-003` |
| Capability | Observation Session Management |
| Failure mode | Roof state unsafe, unknown or failed transition |
| Related SOP | `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire failure del tetto/cupola o stato roof non sicuro durante una sessione.

## Symptoms

- Stato roof open/closed/safe non confermato.
- Comando apertura/chiusura non riuscito.
- Sensore o evidenza safety incoerente.
- Meteo unsafe con roof non confermato chiuso.

## Immediate Containment

1. Interrompere acquisizione se la sessione e attiva.
2. Non muovere strumenti se puo aumentare il rischio.
3. Applicare procedura di emergenza osservatorio gia documentata.
4. Marcare sessione come `Aborted` o `Emergency`.

## Recovery Steps

1. Verificare stato roof tramite evidenze disponibili.
2. Verificare mount/camera safe state.
3. Preservare log, immagini e timestamp.
4. Se roof non e sicuro, non riprendere sessione.
5. Aprire maintenance activity se failure richiede intervento.
6. Chiudere sessione con gap e recovery evidence.

## Evidence to Capture

- Stato roof dichiarato e osservato.
- Meteo al momento della failure.
- Stato mount/camera.
- Azioni manuali o remote eseguite.

## Escalation

Escalare immediatamente a Operations Owner. La safety dell'osservatorio prevale su ogni output scientifico.