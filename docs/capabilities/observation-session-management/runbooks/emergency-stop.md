# Runbook - Emergency Stop

| Campo | Valore |
|---|---|
| Runbook | `OSM-RB-008` |
| Capability | Observation Session Management |
| Failure mode | Immediate safety-critical stop required |
| Related SOP | `OSM-SOP-003`, `OSM-SOP-004`, `OSM-SOP-005` |

## Purpose

Gestire arresto emergenziale della sessione quando la sicurezza dell'osservatorio, degli strumenti o delle operazioni remote e prioritaria.

## Triggers

- Meteo o safety event critico.
- Roof/mount state non sicuro.
- Perdita controllo remoto durante stato operativo rischioso.
- Rischio per equipment o integrita osservatorio.

## Immediate Containment

1. Interrompere acquisizione se possibile e sicuro.
2. Portare sistemi critici verso stato sicuro secondo SOP/manuali esistenti.
3. Non tentare ottimizzazioni scientifiche.
4. Marcare sessione `Emergency` o `Aborted`.
5. Preservare evidenza minima disponibile.

## Recovery Steps

1. Attendere conferma safe state.
2. Identificare causa primaria.
3. Applicare runbook specifico: weather, roof, mount, N.I.N.A., ASCOM, camera.
4. Non riprendere sessione senza nuova weather/safety validation.
5. Chiudere sessione con outcome e incident evidence.
6. Aprire maintenance activity o governance follow-up se necessario.

## Evidence to Capture

- Trigger emergenza.
- Stato osservatorio.
- Timestamp e sistemi impattati.
- Azioni eseguite.
- Stato finale e follow-up.

## Escalation

Escalazione immediata a Operations Owner. Se la causa riguarda equipment, coinvolgere Engineering Owner.