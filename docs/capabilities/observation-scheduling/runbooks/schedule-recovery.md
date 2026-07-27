# Runbook - Schedule Recovery

| Campo | Valore |
|---|---|
| Runbook | Schedule Recovery |
| Capability | CAP-002 Observation Scheduling |
| Severity | Operational / Continuity |
| Owner | Operations Owner / OPEN |

## Trigger

- Schedule rimasta in stato incoerente.
- Evidenza incompleta dopo conflitto o cancellazione.
- Fonte esterna temporaneamente indisponibile.
- Handover verso CAP-001 non confermato.

## Immediate Assessment

1. Identificare schedule e stato corrente.
2. Verificare ultimo evento registrato.
3. Verificare se CAP-001 ha ricevuto schedule pubblicata.
4. Identificare evidenze mancanti: target, finestra, risorse, meteo, safety, approval.
5. Determinare se recovery e consentita o se serve cancellazione.

## Recovery Steps

1. Congelare ulteriori aggiornamenti non necessari sulla schedule.
2. Ricostruire catena Observation Request -> Scheduled Observation -> stato corrente.
3. Recuperare evidenza mancante dalle fonti autorevoli disponibili.
4. Se manca approval, riportare a `Pending Approval` o `Candidate`.
5. Se manca safety/weather evidence, impedire pubblicazione.
6. Se handover CAP-001 e ambiguo, coordinare con CAP-001 prima di ripubblicare.
7. Applicare update o cancellation SOP.
8. Registrare Recovery Record con causa, impatto, azione e owner.
9. Aggiornare traceability e knowledge evidence.

## Escalation

Escalare se:

- non e possibile ricostruire lo stato corretto;
- esiste rischio safety;
- la schedule ha prodotto azione operativa in CAP-001;
- la perdita di evidenza indica problema sistemico di repository o procedura.

## Exit Criteria

- Stato schedule coerente e documentato.
- Evidenza minima completa o cancellazione registrata.
- Nessuna duplicazione di Scheduled Observation attiva.
- Eventuali follow-up sono registrati come open decision o maintenance activity.

## Related Documents

- `../sop/update-schedule.md`
- `../sop/cancel-schedule.md`
- `../traceability.md`
