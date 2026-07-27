# Runbook - Camera Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-004` |
| Capability | Observation Session Management |
| Failure mode | Camera unavailable, exposure failure, download failure or inconsistent image output |
| Related SOP | `OSM-SOP-002`, `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire failure camera durante acquisizione preservando dati validi e session evidence.

## Symptoms

- Camera non connessa in N.I.N.A.
- Exposure non parte o non termina.
- Download image fallito.
- FITS/header mancanti o incoerenti.
- Sequenza bloccata su camera event.

## Immediate Containment

1. Sospendere sequenza se necessario.
2. Non cancellare immagini parziali o log.
3. Verificare che safety osservatorio resti valida.

## Recovery Steps

1. Verificare connessione camera in N.I.N.A. e driver ASCOM/native dove applicabile.
2. Verificare storage disponibile.
3. Verificare temperatura/cooling se rilevante.
4. Se recovery e sicuro, riprendere acquisizione registrando gap.
5. Se failure persiste, abortire sessione e passare a Close Session.
6. Registrare maintenance activity se failure e ricorrente.

## Evidence to Capture

- Frame riusciti e falliti.
- Log N.I.N.A. e messaggio errore.
- Stato camera/cooling se disponibile.
- Decisione ripresa/abort.

## Escalation

Escalare a Engineering Owner se connessione o hardware camera non sono ripristinabili.