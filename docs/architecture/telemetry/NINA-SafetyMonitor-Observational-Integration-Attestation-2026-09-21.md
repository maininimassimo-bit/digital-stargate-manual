# N.I.N.A. SafetyMonitor — Observational Integration Attestation

| Campo | Valore |
|---|---|
| Data | 2026-09-21 |
| Host | EAGLE30154 |
| Fonte | ASCOM.TS_Shelter.SafetyMonitor via N.I.N.A. Observatory Telemetry Exporter |
| Modalità | Read-only / observational |
| Stato | ACCEPTED — observational evidence |
| Safety Authority | Local physical interlocks and local Safety Monitor |

## Decisione

La fonte N.I.N.A. TS Shelter SafetyMonitor è integrata nel contratto observatory-status-v1 come evidenza osservativa separata.

Non è Safety Authority e non autorizza operazioni, scheduling, comandi hardware o remediation automatica.

## Evidenza runtime

Observation state: SAFE
Observation quality: CURRENT
IsSafe: True
SafetiesRaw: 0
Overall safety: UNKNOWN
Authority: LOCAL_SAFETY_AUTHORITY

## Semantica J6

PowerMask decimal: 1
PowerMask hex: 0x00000001

Bit 0 = 0: MAINS_PRESENT
Bit 0 = 1: MAINS_LOST

Errore COM, sorgente mancante, dato stale o proiezione malformata producono UNKNOWN.

## Verifiche

- SAFE/CURRENT verificato come evidenza osservativa;
- overall safety mantenuto UNKNOWN;
- authority mantenuta LOCAL_SAFETY_AUTHORITY;
- scenario stale degradato a UNKNOWN/STALE;
- command path assente;
- test permanente superato.

## Scope escluso

Questa attestazione non autorizza producer operativo, publisher, Scheduled Task, comandi hardware o sostituzione degli interlock fisici/locali.

Decision: ACCEPTED as read-only observational evidence.
Safety Authority promotion: NO_GO / not performed.
