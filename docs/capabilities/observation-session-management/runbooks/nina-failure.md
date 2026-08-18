# Runbook - N.I.N.A. Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-006` |
| Capability | Observation Session Management |
| Failure mode | N.I.N.A. unavailable, sequence failure or application instability |
| Related SOP | `OSM-SOP-001`, `OSM-SOP-002`, `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire failure N.I.N.A. durante preparazione o acquisizione senza perdere evidenza di sessione.

## Symptoms

- N.I.N.A. non avvia o non risponde.
- Sequenza bloccata o incoerente.
- Device non connessi tramite N.I.N.A.
- Log non aggiornato o output incompleto.

## Immediate Containment

1. Valutare safety osservatorio e stato dispositivi.
2. Non forzare ripartenze se mount/roof/camera non sono sicuri.
3. Salvare o preservare log disponibili.

## Recovery Steps

1. Verificare se failure e applicativa, device o sistema operativo.
2. Verificare stato ASCOM, CPWI, PHD2 e camera.
3. Se safe, tentare ripristino secondo manuali esistenti.
4. Se sessione puo riprendere, registrare gap e continuare.
5. Se non puo riprendere, abortire e chiudere preservando evidenze.

## Evidence to Capture

- Log N.I.N.A.
- Stato sequenza.
- Device connessi/non connessi.
- Frame gia acquisiti.
- Decisione recovery/abort.

## Escalation

Escalare a Engineering Owner per failure ricorrenti o configurazioni corrotte.