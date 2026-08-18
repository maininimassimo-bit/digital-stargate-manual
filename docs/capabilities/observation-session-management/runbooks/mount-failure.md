# Runbook - Mount Failure

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-005` |
| Capability | Observation Session Management |
| Failure mode | Mount connection, slew, tracking, park or pointing failure |
| Related SOP | `OSM-SOP-002`, `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire failure montatura mantenendo sicurezza meccanica, tracciabilita e conservazione dati.

## Symptoms

- CPWI o ASCOM non connesso.
- Slew fallito o target non raggiunto.
- Tracking perso.
- Park/Unpark fallito.
- Pointing o plate solving incoerente.

## Immediate Containment

1. Fermare acquisizione se tracking o pointing sono non affidabili.
2. Evitare comandi ripetuti non documentati.
3. Valutare safe state mount/roof.
4. Attivare Abort Session se safety non e certa.

## Recovery Steps

1. Verificare stato CPWI e ASCOM.
2. Verificare mount state e posizione stimata.
3. Verificare connessione e alimentazione se documentabile.
4. Riprendere solo se pointing/tracking sono validati.
5. Se park non e confermabile, applicare procedura di emergenza esistente.
6. Registrare eventi e aggiornare Session Manifest.

## Evidence to Capture

- Stato mount prima/dopo failure.
- Errore CPWI/ASCOM/N.I.N.A.
- Target e coordinate coinvolte.
- Azione eseguita e stato finale.

## Escalation

Escalare a Operations Owner e Engineering Owner se mount safe state non e confermabile.