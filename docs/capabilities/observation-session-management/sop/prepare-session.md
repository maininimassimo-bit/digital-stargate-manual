# SOP - Prepare Observation Session

| Campo | Valore |
|---|---|
| SOP | `OSM-SOP-001` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | Enterprise Architecture, Knowledge Framework, Design System |

## Purpose

Preparare una sessione osservativa verificando richiesta, target, equipment, meteo, safety e readiness documentale prima dell'esecuzione.

## Trigger

- Observation Request approvata o intent operativo documentato.
- Finestra osservativa disponibile.
- Operatore remoto pronto alla verifica.

## Roles

| Role | Responsibility |
|---|---|
| Operator | Esegue checklist di preparazione. |
| Operations Owner | Definisce readiness operativa. |
| Engineering Owner | Supporta validazione equipment/configurazione. |
| Data Owner | Conferma requisiti manifest e archive readiness. |

## Procedure

1. Identificare Observation Request o intent operativo.
2. Confermare target e coordinate dalla Target Registry quando disponibile.
3. Confermare profilo osservativo e configurazione equipment.
4. Verificare stato EAGLE, N.I.N.A., ASCOM, CPWI, PHD2 e storage disponibile.
5. Acquisire Weather Snapshot e confermare stato `Weather Safe`.
6. Confermare Safety State: roof, mount, network, power e remote access.
7. Preparare Session Manifest in stato `Draft` o registrare decisione open se schema non disponibile.
8. Confermare runbook disponibili per failure principali.
9. Marcare sessione come `Prepared` o `Deferred`.

## Outputs

- Sessione in stato `Prepared` o `Deferred`.
- Evidenza di equipment/weather/safety validation.
- Manifest draft o gap documentato.
- Eventuali open issue operative.

## Controls

- Non avviare sessione se weather o safety sono unsafe.
- Non inventare dati mancanti.
- Non registrare credenziali o segreti nella documentazione di sessione.

## Related Runbooks

- Weather Unsafe
- Scheduler Failure
- N.I.N.A. Failure
- ASCOM Failure
- Emergency Stop
