# Runbook - Scheduler Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-001` |
| Capability | Observation Session Management |
| Failure mode | Scheduler unavailable, inconsistent or incomplete |
| Related SOP | `OSM-SOP-001`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire fallimento o indisponibilita del Scheduler preservando tracciabilita della sessione e impedendo avvio non governato.

## Symptoms

- Observation Request assente o incompleta.
- Target non risolto o non coerente.
- Session plan non disponibile.
- Priorita, finestra o vincoli mancanti.

## Immediate Containment

1. Non avviare la sessione se intent, target o vincoli sono ambigui.
2. Marcare la sessione come `Deferred` o `Prepared with Gaps`.
3. Preservare eventuale richiesta manuale o note operatore.

## Recovery Steps

1. Verificare Target Registry o fonte target disponibile.
2. Ricostruire intent operativo minimo: target, finestra, profilo, obiettivo.
3. Validare equipment, weather e safety prima di procedere.
4. Se i dati minimi non sono disponibili, chiudere come `Deferred`.
5. Registrare open decision o maintenance follow-up se il problema e ricorrente.

## Evidence to Capture

- Timestamp failure.
- Target/request mancanti o incoerenti.
- Decisione operatore.
- Stato finale sessione.

## Escalation

Escalare a Operations Owner e Science Owner se target o priorita non possono essere confermati.
