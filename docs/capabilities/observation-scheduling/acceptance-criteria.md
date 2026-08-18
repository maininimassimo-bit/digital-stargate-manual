# CAP-002 - Acceptance Criteria

## Purpose

Gli acceptance criteria definiscono condizioni misurabili per considerare Observation Scheduling pronta alla futura implementazione. La baseline documentale soddisfa lo stato `Implementation Ready` quando questi criteri sono documentati e tracciabili.

## Criteria

| ID | Criterion | Measurement | Status |
|---|---|---|---|
| `OSD-AC-001` | Una Observation Request puo essere trasformata in Scheduled Observation tracciabile. | Link request -> schedule -> CAP-001 handover presente. | Defined |
| `OSD-AC-002` | Ogni Scheduled Observation contiene target, finestra, priorita, vincoli, risorse e stato. | Campi concettuali definiti in `data-model.md`. | Defined |
| `OSD-AC-003` | La schedule non puo essere pubblicata senza Approval Record. | Processo e SOP richiedono approvazione. | Defined |
| `OSD-AC-004` | Target non valido o assente impedisce approvazione senza sospensione motivata. | Target validation step presente. | Defined |
| `OSD-AC-005` | Risorsa indisponibile genera Conflict Record o recovery. | Runbook `resource-unavailable.md` presente. | Defined |
| `OSD-AC-006` | Stato safety unsafe prevale sempre su priorita scientifica. | Regola dichiarata in process, ADR e SOP. | Defined |
| `OSD-AC-007` | Perdita finestra meteo genera cancellazione, ripianificazione o recovery governata. | Runbook `weather-window-lost.md` presente. | Defined |
| `OSD-AC-008` | Conflitti multipli sono risolti con priorita documentata. | `OSD-ADR-002` e runbook conflitto presenti. | Defined |
| `OSD-AC-009` | Schedule update mantiene storico decisionale minimo. | SOP `update-schedule.md` presente. | Defined |
| `OSD-AC-010` | Schedule cancellation registra owner, motivazione e impatto. | SOP `cancel-schedule.md` presente. | Defined |
| `OSD-AC-011` | Ogni requisito CAP-002 ha identificatore unico. | 32 requisiti con prefisso `OSD`. | Defined |
| `OSD-AC-012` | CAP-000 registra status `Documented`, readiness `Implementation Ready`, version `0.1`. | CAP-000 aggiornato. | Pending update |
| `OSD-AC-013` | REL-000 contiene riferimento minimo al primo scheduling capability package. | REL-000 aggiornato senza cambio governance. | Pending update |
| `OSD-AC-014` | MkDocs rende raggiungibili tutti i documenti CAP-002. | Navigazione aggiornata. | Pending update |
| `OSD-AC-015` | Validation non segnala duplicati o link interni mancanti nel pacchetto. | Static validation o MkDocs strict. | Pending validation |

## Acceptance Notes

- Lo stato `Defined` indica criterio formalizzato, non implementazione eseguita.
- I criteri `Pending update` sono chiusi con aggiornamento di CAP-000, REL-000 e MkDocs.
- Ogni futura release dovra trasformare i criteri rilevanti in evidenze operative o test risultanti.
