# Runbook - ASCOM Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-007` |
| Capability | Observation Session Management |
| Failure mode | ASCOM/Alpaca device integration failure |
| Related SOP | `OSM-SOP-001`, `OSM-SOP-002`, `OSM-SOP-003`, `OSM-SOP-004` |

## Purpose

Gestire failure del layer ASCOM/Alpaca che impedisce controllo o stato affidabile dei dispositivi.

## Symptoms

- Driver ASCOM non raggiungibile.
- Device state non coerente.
- Timeout comandi.
- N.I.N.A. non connette dispositivi tramite ASCOM.
- Stato Alpaca non disponibile dove previsto.

## Immediate Containment

1. Interrompere avvio o acquisizione se device state non e affidabile.
2. Non inviare comandi ripetuti senza conferma stato.
3. Valutare safety di mount/roof/camera.

## Recovery Steps

1. Identificare device impattato.
2. Verificare se failure e driver, rete, applicazione o hardware.
3. Controllare manuale tecnico del device interessato.
4. Riprendere solo se stato device torna validato.
5. Se failure persiste, abortire sessione o rinviare.
6. Registrare open issue tecnica se ricorrente.

## Evidence to Capture

- Device impattato.
- Messaggi errore ASCOM/Alpaca/N.I.N.A.
- Timestamp e stato sessione.
- Esito recovery.

## Escalation

Escalare a Engineering Owner per driver, configurazioni o rete ASCOM/Alpaca.