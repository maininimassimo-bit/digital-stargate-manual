# SOP - Approve Schedule

| Campo | Valore |
|---|---|
| SOP | Approve Schedule |
| Capability | CAP-002 Observation Scheduling |
| Stato | Approved for capability baseline |
| Owner | Operations Owner / OPEN |

## Purpose

Definire le condizioni per approvare e pubblicare una schedule, garantendo che sicurezza, meteo, target, risorse e priorita siano documentati.

## Trigger

- Schedule in stato `Pending Approval`.
- Conflitto risolto e pronto per decisione.
- Pianificazione pronta per handover CAP-001.

## Preconditions

- Observation Request tracciata.
- Target validato.
- Observation Window documentata.
- Resource Allocation valida.
- Weather Validation disponibile.
- Safety Validation safe o motivazione di non pubblicazione.
- Conflict Record chiusi o accettati con decisione esplicita.

## Procedure

1. Verificare completezza schedule.
2. Confermare target e finestra osservativa.
3. Confermare disponibilita risorse.
4. Confermare meteo accettabile per pubblicazione.
5. Confermare observatory safety in stato safe.
6. Verificare conflitti e priorita secondo `OSD-ADR-002`.
7. Registrare approvatore, timestamp, decisione e razionale.
8. Se approvata, impostare stato `Approved`.
9. Pubblicare per CAP-001 solo dopo approvazione.
10. Registrare handover evidence per Observation Session Management.

## Outputs

- Approval Record.
- Schedule in stato `Approved` o `Published`.
- Handover evidence per CAP-001.

## Controls

- Safety unsafe blocca approvazione/pubblicazione.
- Weather unsafe blocca pubblicazione salvo futura policy approvata.
- Priorita non puo sovrascrivere safety.
- Decisioni manuali devono essere motivate.

## Related Documents

- `../adr/OSD-ADR-001-scheduling-boundary.md`
- `../adr/OSD-ADR-002-priority-resolution.md`
- `../acceptance-criteria.md`
