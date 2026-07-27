# Observation Session Management - Test Plan

| Campo | Valore |
|---|---|
| Test Plan | `OSM-TEST-001` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | Requirements, SOP, Runbooks, Architecture Mapping |

## Purpose

Definire test documentali e operativi per validare la capability Observation Session Management. Questo piano non crea test automatizzati o codice.

## Functional Tests

| ID | Test | Expected result | Requirement |
|---|---|---|---|
| `OSM-FT-001` | Creare una sessione da Observation Request documentata. | Sessione in stato `Planned` con target e intent. | `OSM-FR-001` |
| `OSM-FT-002` | Collegare target, equipment e configurazione a sessione. | Riferimenti presenti o gap open. | `OSM-FR-002`, `OSM-FR-003` |
| `OSM-FT-003` | Registrare Weather Snapshot e Safety State. | Stato safe/unsafe documentato. | `OSM-FR-004` |
| `OSM-FT-004` | Consolidare Session Manifest concettuale. | Manifest draft/verified/archived o open gap. | `OSM-FR-005` |
| `OSM-FT-005` | Collegare raw images alla sessione. | Raw image references presenti nel risultato. | `OSM-FR-006` |

## Operational Tests

| ID | Test | Expected result | SOP |
|---|---|---|---|
| `OSM-OT-001` | Eseguire Prepare Session SOP. | Sessione `Prepared` o `Deferred` con evidenza. | `OSM-SOP-001` |
| `OSM-OT-002` | Eseguire Execute Session SOP in scenario nominale. | Stato `Executing/Acquiring` e log eventi. | `OSM-SOP-002` |
| `OSM-OT-003` | Eseguire Close Session SOP. | Stato `Archived`, `Closed with Gaps` o `Recovery Required`. | `OSM-SOP-005` |
| `OSM-OT-004` | Verificare knowledge update post-sessione. | Catalog/notes/open decisions aggiornati. | `OSM-SOP-005` |

## Recovery Tests

| ID | Test | Expected result | Runbook |
|---|---|---|---|
| `OSM-RT-001` | Scheduler failure. | Sessione deferred o intent minimo documentato. | `OSM-RB-001` |
| `OSM-RT-002` | Weather unsafe. | Sessione abortita/deferred e safety preserved. | `OSM-RB-002` |
| `OSM-RT-003` | Roof failure. | Emergency/safety path documentato. | `OSM-RB-003` |
| `OSM-RT-004` | Camera failure. | Dati validi preservati e decisione recovery/abort. | `OSM-RB-004` |
| `OSM-RT-005` | Mount failure. | Mount safety valutata e sessione recuperata o abortita. | `OSM-RB-005` |
| `OSM-RT-006` | N.I.N.A. failure. | Log preservato e stato sessione coerente. | `OSM-RB-006` |
| `OSM-RT-007` | ASCOM failure. | Device state gestito e failure tracciata. | `OSM-RB-007` |
| `OSM-RT-008` | Emergency stop. | Safety prioritaria, evidenza minima preservata. | `OSM-RB-008` |

## Acceptance Tests

| ID | Test | Expected result |
|---|---|---|
| `OSM-AT-001` | Verificare package documentale completo. | Overview, process, requirements, mapping, data model, ADR, SOP, runbooks, manual, test plan, acceptance, traceability presenti. |
| `OSM-AT-002` | Verificare gerarchia governance. | Ogni documento richiama roadmap, DSRA, EA, Knowledge e Design System. |
| `OSM-AT-003` | Verificare nessun codice applicativo. | Solo Markdown e MkDocs navigation modificati. |
| `OSM-AT-004` | Verificare navigazione MkDocs. | Capability raggiungibile in `mkdocs.yml`. |

## Regression Tests

| ID | Test | Expected result |
|---|---|---|
| `OSM-GT-001` | ADR-001 still referenced. | Nessuna duplicazione o contraddizione. |
| `OSM-GT-002` | Enterprise Architecture baseline unchanged. | EA-000 e layer EA non modificati. |
| `OSM-GT-003` | Knowledge Framework unchanged. | Documenti knowledge non modificati. |
| `OSM-GT-004` | Design System unchanged. | Design System baseline non modificato. |
| `OSM-GT-005` | Runbook failure modes still covered. | 8/8 runbook richiesti presenti. |

## Test Evidence

Test evidence shall be recorded in future release notes or assessment documents. This plan defines what to validate, not how to automate validation.
