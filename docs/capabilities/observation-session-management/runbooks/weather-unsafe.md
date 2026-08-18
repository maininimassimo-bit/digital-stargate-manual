# Runbook - Weather Unsafe

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-002` |
| Capability | Observation Session Management |
| Failure mode | Weather unsafe or weather evidence unavailable |
| Related SOP | `OSM-SOP-001`, `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire condizioni meteo unsafe o non verificabili durante preparazione o sessione.

## Symptoms

- Weather Station indica unsafe.
- AllSky o fonte cielo indica rischio.
- Dato meteo assente, stale o incoerente.
- Safety state non confermabile.

## Immediate Containment

1. Bloccare avvio sessione o sospendere acquisizione.
2. Dare priorita a roof/mount/camera safe state secondo procedure esistenti.
3. Marcare sessione `Deferred`, `Aborted` o `Recovery`.

## Recovery Steps

1. Verificare fonte meteo primaria e secondaria se disponibile.
2. Confermare se unsafe e reale, non disponibile o falso positivo.
3. Se unsafe reale, non riprendere la sessione.
4. Se dato assente, trattare come unsafe finche non verificato.
5. Preservare log e raw images gia acquisite.
6. Aggiornare Session Manifest con Weather Snapshot e Safety State.

## Evidence to Capture

- Timestamp e fonte meteo.
- Stato safe/unsafe.
- Azione eseguita.
- Impatto su sessione e archive.

## Escalation

Escalare a Operations Owner se safety state non puo essere confermato.