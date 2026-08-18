# Runbook - Scheduling Conflict

| Campo | Valore |
|---|---|
| Runbook | Scheduling Conflict |
| Capability | CAP-002 Observation Scheduling |
| Severity | Operational |
| Owner | Operations Owner / OPEN |

## Trigger

- Due o piu richieste competono per la stessa finestra.
- Una risorsa e assegnata a piu Scheduled Observation.
- Vincoli target, finestra o priorita non sono compatibili.

## Immediate Assessment

1. Identificare schedule coinvolte.
2. Verificare stato di ciascuna schedule.
3. Verificare se una schedule e gia pubblicata verso CAP-001.
4. Identificare tipo conflitto: target, finestra, risorsa, meteo, safety, priorita.
5. Registrare Conflict Record.

## Recovery Steps

1. Applicare `OSD-ADR-002` per confermare safety precedence.
2. Se safety o weather sono unsafe, sospendere approvazione/pubblicazione.
3. Se il conflitto e risorsa, verificare alternativa in Equipment Registry.
4. Se il conflitto e finestra, rivalutare Observation Window.
5. Se il conflitto e priorita, richiedere decisione owner autorizzato.
6. Aggiornare schedule con stato `Conflict`, `Pending Approval`, `Approved` o `Cancelled`.
7. Se pubblicazione era gia avvenuta, coordinare handover/recovery con CAP-001.
8. Registrare risoluzione e motivazione.

## Escalation

Escalare a Operations Owner se:

- conflitto impatta schedule gia pubblicata;
- safety o meteo impediscono osservazione;
- non esiste priorita risolutiva documentata;
- la risorsa alternativa non e disponibile.

## Exit Criteria

- Ogni schedule ha stato coerente.
- Conflict Record e chiuso o esplicitamente ancora aperto.
- Priorita e decisione sono tracciate.
- CAP-001 e informata se il handover era gia avvenuto.

## Related Documents

- `../adr/OSD-ADR-002-priority-resolution.md`
- `../sop/update-schedule.md`
- `../sop/cancel-schedule.md`
