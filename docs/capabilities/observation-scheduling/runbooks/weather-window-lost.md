# Runbook - Weather Window Lost

| Campo | Valore |
|---|---|
| Runbook | Weather Window Lost |
| Capability | CAP-002 Observation Scheduling |
| Severity | Safety / Operational |
| Owner | Operations Owner / Safety Owner / OPEN |

## Trigger

- Weather Monitoring indica finestra non piu idonea.
- AllSky o Weather Station mostrano condizioni incompatibili.
- Safety state diventa unsafe prima del handover.
- Meteo cambia dopo approvazione o pubblicazione.

## Immediate Assessment

1. Verificare schedule e finestra impattate.
2. Confermare fonte meteo/safety disponibile.
3. Verificare se la schedule e `Approved`, `Published` o gia consegnata a CAP-001.
4. Registrare Weather Event o Safety Event rilevante.

## Recovery Steps

1. Bloccare nuova pubblicazione se meteo/safety non sono safe.
2. Se la schedule non e pubblicata, riportarla a `Candidate`, `Conflict` o `Cancelled`.
3. Se pubblicata, notificare CAP-001 per preparazione/recovery secondo confine `OSD-ADR-001`.
4. Cercare finestra alternativa solo se target e risorse restano validi.
5. Se non esiste finestra alternativa, cancellare secondo SOP.
6. Aggiornare Conflict/Cancellation Record con evidenza meteo.
7. Registrare eventuale necessita di ripianificazione.

## Escalation

Escalare immediatamente se:

- safety unsafe e la sessione potrebbe essere gia in preparazione;
- la schedule riguarda target ad alta priorita;
- la cancellazione impatta piu schedule pubblicate.

## Exit Criteria

- Nessuna schedule unsafe resta pubblicata senza evidenza di recovery.
- Weather/Safety evidence e collegata alla schedule.
- CAP-001 ha ricevuto comunicazione se impattato.
- Knowledge update e pronto per archivio.

## Related Documents

- `../sop/cancel-schedule.md`
- `../sop/update-schedule.md`
- `../architecture-mapping.md`
