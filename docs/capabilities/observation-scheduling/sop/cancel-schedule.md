# SOP - Cancel Schedule

| Campo | Valore |
|---|---|
| SOP | Cancel Schedule |
| Capability | CAP-002 Observation Scheduling |
| Stato | Approved for capability baseline |
| Owner | Operations Owner / OPEN |

## Purpose

Definire la cancellazione governata di una schedule quando target, finestra, risorse, meteo, safety o priorita non permettono piu una pianificazione valida.

## Trigger

- Weather window lost.
- Safety unsafe.
- Resource unavailable.
- Target non piu valido per la finestra.
- Decisione operativa o scientifica documentata.
- Conflitto non risolvibile.

## Preconditions

- Schedule identificata.
- Stato corrente noto.
- Motivo cancellazione disponibile o investigazione aperta.

## Procedure

1. Identificare schedule e Scheduled Observation impattate.
2. Verificare se CAP-001 ha gia ricevuto handover.
3. Se CAP-001 e impattata, coordinare con le SOP CAP-001 pertinenti.
4. Registrare motivo cancellazione.
5. Registrare owner della decisione.
6. Valutare impatto su target, risorse, finestra e archiviazione.
7. Impostare stato `Cancelled`.
8. Registrare eventuale necessita di recovery o ripianificazione.
9. Aggiornare traceability e knowledge evidence.
10. Archiviare cancellation record.

## Outputs

- Cancellation Record.
- Schedule in stato `Cancelled`.
- Recovery action o ripianificazione se richiesta.

## Controls

- Non cancellare senza motivazione.
- Non perdere evidenza della richiesta originaria.
- Non modificare manualmente Session Manifest CAP-001 da questa SOP.

## Related Documents

- `../runbooks/weather-window-lost.md`
- `../runbooks/resource-unavailable.md`
- `../runbooks/schedule-recovery.md`
