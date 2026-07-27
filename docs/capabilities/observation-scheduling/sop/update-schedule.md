# SOP - Update Schedule

| Campo | Valore |
|---|---|
| SOP | Update Schedule |
| Capability | CAP-002 Observation Scheduling |
| Stato | Approved for capability baseline |
| Owner | Operations Owner / OPEN |

## Purpose

Definire come aggiornare una schedule esistente mantenendo tracciabilita, storico decisionale e coerenza con vincoli target, risorse, meteo e safety.

## Trigger

- Cambio finestra osservativa.
- Aggiornamento target o priorita.
- Risorsa non disponibile.
- Variazione meteo o safety.
- Correzione documentale governata.

## Preconditions

- Schedule esistente identificata.
- Stato corrente noto.
- Motivo aggiornamento documentato.

## Procedure

1. Identificare schedule e Scheduled Observation impattate.
2. Registrare motivo dell'aggiornamento.
3. Verificare se la schedule e gia `Published`.
4. Se pubblicata, valutare impatto su CAP-001 prima di modificare.
5. Rivalutare target, finestra, risorse, meteo e safety solo dove impattati.
6. Aggiornare Conflict Record se emergono nuovi conflitti.
7. Aggiornare Approval Record se cambia una decisione approvata.
8. Assegnare nuovo stato coerente: `Candidate`, `Conflict`, `Pending Approval`, `Approved`, `Published` o `Cancelled`.
9. Registrare storico minimo: chi, quando, cosa, perche, impatto.
10. Aggiornare riferimenti di tracciabilita.

## Outputs

- Schedule aggiornata.
- Storico decisionale minimo.
- Eventuali conflict, approval o cancellation record aggiornati.

## Controls

- Una modifica post-pubblicazione non deve invalidare silenziosamente il handover CAP-001.
- Safety unsafe richiede sospensione, cancellazione o recovery.
- Cambi sostanziali devono tornare ad approvazione.

## Related Documents

- `approve-schedule.md`
- `cancel-schedule.md`
- `../runbooks/resource-unavailable.md`
- `../runbooks/weather-window-lost.md`
