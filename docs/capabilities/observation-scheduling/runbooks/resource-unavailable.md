# Runbook - Resource Unavailable

| Campo | Valore |
|---|---|
| Runbook | Resource Unavailable |
| Capability | CAP-002 Observation Scheduling |
| Severity | Operational |
| Owner | Engineering Owner / Operations Owner / OPEN |

## Trigger

- Equipment Registry indica risorsa indisponibile.
- Manutenzione o guasto impedisce l'uso di una risorsa pianificata.
- Profilo strumenti non compatibile con la schedule candidata.
- CAP-001 segnala problema prima o durante handover.

## Immediate Assessment

1. Identificare risorsa e Scheduled Observation impattate.
2. Verificare stato della schedule.
3. Verificare se esistono risorse alternative compatibili.
4. Registrare Resource Allocation issue.
5. Valutare impatto su target, finestra e priorita.

## Recovery Steps

1. Se schedule non pubblicata, riportare stato a `Conflict` o `Candidate`.
2. Se esiste risorsa alternativa, rivalutare vincoli e finestra.
3. Se non esiste alternativa, cancellare o ripianificare.
4. Se la schedule e pubblicata, coordinare con CAP-001 prima di cambiare stato operativo.
5. Aggiornare Resource Allocation e Conflict Record.
6. Registrare owner della decisione e impatto.
7. Aggiornare Knowledge Framework evidence se la risorsa richiede manutenzione.

## Escalation

Escalare a Engineering Owner se:

- la risorsa e critica per piu schedule;
- indisponibilita indica problema di manutenzione;
- non esiste alternativa compatibile;
- la schedule e gia in handover CAP-001.

## Exit Criteria

- Resource Allocation e coerente con stato reale.
- Schedule non usa risorsa indisponibile.
- Eventuale cancellazione o recovery e documentata.
- CAP-001 e informata se necessario.

## Related Documents

- `../sop/update-schedule.md`
- `../sop/cancel-schedule.md`
- `../data-model.md`
