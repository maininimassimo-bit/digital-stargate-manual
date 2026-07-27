# SOP - Create Schedule

| Campo | Valore |
|---|---|
| SOP | Create Schedule |
| Capability | CAP-002 Observation Scheduling |
| Stato | Approved for capability baseline |
| Owner | Operations Owner / OPEN |

## Purpose

Definire la procedura per creare una Observation Schedule a partire da una Observation Request tracciabile.

## Trigger

- Nuova Observation Request.
- Necessita di pianificare una finestra osservativa.
- Recovery che richiede nuova schedule candidata.

## Preconditions

- Observation Request disponibile.
- Target selezionabile o motivo di sospensione documentabile.
- Accesso a evidenza target, risorse, meteo e safety secondo repository.

## Procedure

1. Registrare identificatore della Observation Request.
2. Verificare target in Target Registry o registrare azione richiesta.
3. Definire planning horizon e finestra candidata.
4. Valutare vincoli astronomici noti.
5. Verificare disponibilita risorse con Equipment Registry.
6. Collegare evidenza meteo disponibile.
7. Collegare evidenza safety disponibile.
8. Assegnare priorita iniziale o marcare priorita `OPEN` se non definita.
9. Registrare eventuali conflitti.
10. Impostare stato `Candidate` o `Conflict`.
11. Salvare evidenza documentale e riferimenti.

## Outputs

- Observation Schedule in stato `Candidate` o `Conflict`.
- Scheduled Observation candidata.
- Conflict Record se necessario.

## Controls

- Non pubblicare schedule durante questa SOP.
- Non aprire sessione N.I.N.A. da CAP-002.
- Non modificare CAP-001 o Session Manifest.

## Related Documents

- `../business-process.md`
- `../data-model.md`
- `approve-schedule.md`
- `../runbooks/scheduling-conflict.md`
