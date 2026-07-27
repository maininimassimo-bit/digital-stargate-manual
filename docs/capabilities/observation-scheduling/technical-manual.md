# CAP-002 - Technical Manual

## Purpose

Il manuale tecnico descrive responsabilita, interfacce, dipendenze, input, output e considerazioni operative della capability Observation Scheduling. Non prescrive implementazione software.

## Responsibilities

| Area | Responsibility |
|---|---|
| Schedule governance | Mantenere ciclo di vita, stato, owner e approvazioni della schedule. |
| Window evaluation | Documentare valutazione delle finestre astronomiche candidate. |
| Resource validation | Collegare disponibilita e vincoli dell'Equipment Registry. |
| Safety and weather gating | Verificare che meteo e safety siano valutati prima della pubblicazione. |
| Conflict handling | Identificare e registrare conflitti e risoluzione. |
| Handover | Consegnare solo schedule approvate e pubblicate a CAP-001. |
| Evidence | Conservare dati minimi per traceability, audit e knowledge update. |

## Interfaces

| Interface | Direction | Description |
|---|---|---|
| Observation Request | Inbound | Richiesta candidata da pianificare. |
| Target Registry | Inbound reference | Dati target e vincoli scientifici. |
| Equipment Registry | Inbound reference | Disponibilita, configurazione e manutenzione risorse. |
| Weather Monitoring | Inbound evidence | Meteo previsto/operativo e idoneita finestra. |
| Observatory Safety | Inbound gate | Stato safe/unsafe rilevante per pubblicazione. |
| CAP-001 Observation Session Management | Outbound | Scheduled Observation approvata e pubblicata. |
| Knowledge Framework | Bidirectional evidence | Entita, glossario, tracciabilita e knowledge update. |
| CAP-000 | Outbound registry evidence | Stato, readiness, versione e collegamenti capability. |
| REL-000 | Outbound release evidence | Readiness checklist e promotion evidence. |

## Dependencies

- Enterprise Architecture baseline for Scheduler and logical platform boundaries.
- Knowledge Framework for canonical entities and traceability vocabulary.
- Design System for any future UI surface.
- CAP-001 for session execution boundary.
- Weather Monitoring and Observatory Safety for go/no-go evidence.
- GitHub repository for authoritative documentation and release evidence.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Observation Request | Yes | Must include target reference or target selection action. |
| Target metadata | Yes | From Target Registry where available. |
| Equipment availability | Yes | From Equipment Registry or manual evidence. |
| Weather assessment | Yes before publication | Includes current or forecast suitability. |
| Safety assessment | Yes before publication | Cannot be bypassed by priority. |
| Priority rationale | Yes when conflicts exist | Must be auditable. |

## Outputs

| Output | Consumer |
|---|---|
| Observation Schedule | Operators, registry, knowledge repository. |
| Scheduled Observation | CAP-001. |
| Observation Window | Approval and session preparation. |
| Resource Allocation | CAP-001 and Engineering operations. |
| Conflict Record | Runbooks, audit, priority resolution. |
| Approval Record | Audit, traceability and release evidence. |
| Cancellation Record | Archive and knowledge update. |

## Operational Considerations

- Safety validation has precedence over scientific priority.
- Weather deterioration after publication triggers `weather-window-lost.md` runbook.
- Resource unavailability after publication triggers `resource-unavailable.md` runbook.
- Conflicting schedules must not be silently overwritten.
- Any future UI must show schedule state, conflict state and safety/weather gating clearly and consistently with Design System.
- Any future automation must preserve operator-visible evidence and traceability.

## Configuration Considerations

No configuration files are created by this package. Future implementation may require governed configuration for:

- scheduling horizon;
- priority policy;
- weather window thresholds;
- resource reservation semantics;
- notification or alert routing;
- retention of schedule evidence.

These remain implementation decisions unless already covered by ADR or future governance.

## Related Documents

- `index.md`
- `business-process.md`
- `requirements.md`
- `data-model.md`
- `adr/OSD-ADR-001-scheduling-boundary.md`
- `adr/OSD-ADR-002-priority-resolution.md`
- `test-plan.md`
- `acceptance-criteria.md`
- `traceability.md`
