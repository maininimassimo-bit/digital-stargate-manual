# SOP - Abort Observation Session

| Campo | Valore |
|---|---|
| SOP | `OSM-SOP-003` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | DSRA, Observability Architecture, Security Architecture |

## Purpose

Interrompere una sessione in modo controllato quando meteo, safety, equipment o software rendono non sicura o non affidabile la continuazione.

## Trigger

- Weather unsafe.
- Roof, mount, camera, N.I.N.A., ASCOM o guiding failure critica.
- Remote access o power/network state non affidabile.
- Emergency stop richiesto dall'operatore.

## Procedure

1. Dichiarare stato sessione `Aborted` o `Abort Pending` se la chiusura e in corso.
2. Fermare acquisizione in modo controllato quando possibile.
3. Mettere mount/camera/sequence in stato sicuro secondo strumenti disponibili e SOP locali.
4. Gestire roof/safety secondo runbook specifico.
5. Preservare raw images gia acquisite, log ed evidenze disponibili.
6. Registrare causa, timestamp, sistemi impattati e azione eseguita.
7. Attivare Recover Session se serve ripristino tecnico.
8. Passare a Close Session quando la situazione e stabilizzata.

## Outputs

- Stato `Aborted` documentato.
- Safety state registrato.
- Evidenza preservata.
- Runbook o maintenance activity collegati.

## Controls

- Non privilegiare completamento scientifico rispetto a sicurezza.
- Non tentare recovery non documentato durante unsafe state.
- Non cancellare evidenza parziale di sessione.
