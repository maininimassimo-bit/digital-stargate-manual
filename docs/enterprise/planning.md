# DSG-PLAN-001 - Enterprise Planning Framework

| Campo | Valore |
|---|---|
| Documento | Enterprise Planning Framework |
| Identificativo | `DSG-PLAN-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Questo documento consolida release strategy, milestone strategy, sprint strategy, Enterprise Roadmap 2026-2030, dependency matrix, risk matrix e KPI framework previsti da `DSG-MR-001`.

Non sostituisce la Master Roadmap: ne rende operative le sezioni di planning e mantiene la tracciabilita verso portfolio, registri, governance e release.

## 2. Ambito

Il planning copre release strategy, milestone strategy, sprint strategy, Enterprise Roadmap 2026-2030, dependency matrix, risk matrix e KPI framework.

I dettagli temporali trimestrali, soglie quantitative e ownership non confermati restano `TBD` o `Da validare`.

## 3. Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-PLAN-PRN-001` | Roadmap-first | Il planning deriva da `DSG-MR-001` |
| `DSG-PLAN-PRN-002` | Piccoli incrementi | Ogni sprint produce output verificabile |
| `DSG-PLAN-PRN-003` | Gate prima della release | Nessuna release senza controlli minimi |
| `DSG-PLAN-PRN-004` | Evidenza | Ogni avanzamento deve produrre file, log, checklist o review |

## 4. Release Strategy

| Tipo release | Scopo | Input | Output | Gate |
|---|---|---|---|---|
| Documentale | Pubblicare o aggiornare documenti MkDocs | Markdown, registry, link | Sito navigabile, release note | `QG-DOC`, `QG-SEC` |
| Architetturale | Aggiornare meta-modello, DSRA o ADR | Decisione, assessment, registry | ADR, architettura aggiornata | `QG-ARCH` |
| Dati/analytics | Aggiornare warehouse, KPI o dashboard | Dataset, schema, report | KPI validati | `QG-DATA` |
| Operations | Aggiornare SOP, safety o incident flow | Evidenze operative, DSRA | SOP e controlli | `QG-OPS` |
| Sperimentale | Preparare Live Operations o AI | Use case approvato, controlli | Prototipo documentato | `QG-AI`, `QG-SEC` |

Rollback: definito in [Release documentation](release-documentation.md). I rollback tecnici non documentati restano `Da validare`.

## 5. Milestone Strategy

| Milestone | Obiettivo | Deliverable | Stato |
|---|---|---|---|
| `M1 Foundation` | Baseline enterprise | Roadmap, EAM, DSRA, governance | Transition |
| `M2 Portfolio & Registry` | Tracciabilita programmi e registry | Portfolio, registri, governance estesa | Transition |
| `M3 Assessment & SOP` | Operativita e valutazione | Assessment, SOP, handbook | Transition |
| `M4 Planning & Knowledge` | Planning, indici e traceability | Planning, history, knowledge index | Transition |
| `M5 Live` | Stato live validato | Feed e dashboard live | TO-BE / Da validare |
| `M6 AI` | AI assistiva governata | Use case, audit, guardrail | TO-BE / TBD |

## 6. Sprint Strategy

| Campo | Regola |
|---|---|
| ID | `DSG-SPR-YYYY-NN` |
| Scope | Uno o pochi documenti correlati |
| Output | File Markdown, registry update, evidenza validazione |
| Gate | Link, YAML, contenuti sensibili, coerenza roadmap |
| Commit | Conventional Commit coerente |
| Stato | Proposed, In progress, Completed, Suspended |

Ogni sprint deve dichiarare cosa non viene modificato quando il rischio di duplicazione e alto.

## 7. Enterprise Roadmap 2026-2030

| Anno | Focus | Deliverable | Stato |
|---|---|---|---|
| 2026 | Foundation enterprise | Roadmap, portfolio, registri, governance, planning | Transition |
| 2027 | Data e operations hardening | Warehouse maturo, SOP rafforzate, asset/config registry | Da validare |
| 2028 | Live Operations controllate | Stato osservatorio validato, feed sicuri, dashboard live | TO-BE |
| 2029 | AI assistiva governata | Knowledge assistant, audit, casi d'uso non safety | TO-BE / TBD |
| 2030 | Piattaforma data-driven integrata | Osservatorio, dati, analytics, knowledge e governance unificati | TO-BE |

Dettagli trimestrali: `TBD`.

## 8. Dependency Matrix

| ID | Dipendenza | Impatta | Tipo | Stato | Mitigazione |
|---|---|---|---|---|---|
| `DSG-DEP-DOC-001` | `mkdocs.yml` coerente | Documentation, release | Tecnica | AS-IS | `QG-DOC` |
| `DSG-DEP-NET-001` | Connettivita remota | Operations, live | Operativa | Da validare periodicamente | SOP incident |
| `DSG-DEP-DATA-001` | Log e session report | Data, analytics | Dati | AS-IS / Transition | Data governance |
| `DSG-DEP-WHS-001` | Warehouse schema | Analytics, reporting | Dati | Transition | `QG-DATA` |
| `DSG-DEP-ACM-001` | Registro asset/config | Infrastructure, DR, security | Governance | Da consolidare | Registry |
| `DSG-DEP-SAF-001` | Safety state | Operations, live, AI | Safety | Critica | Safety-first |
| `DSG-DEP-AI-001` | AI governance | AI, knowledge | Governance | TBD | `QG-AI` |

## 9. Risk Matrix

| ID | Rischio | Impatto | Programmi | Mitigazione | Stato |
|---|---|---|---|---|---|
| `DSG-RISK-001` | Stato operativo non sicuro | Alto | Observatory, Operations, Live | SOP, FMEA, stato conservativo | Mitigato / Da validare |
| `DSG-RISK-002` | Dati incompleti o non confrontabili | Medio | Data, Warehouse, Reporting | Quality gate e metadata | In trattamento |
| `DSG-RISK-003` | Live Operations senza validazione | Alto | Live Operations, Dashboard Live | Feed solo dopo controllo e policy | TO-BE |
| `DSG-RISK-004` | AI usata oltre ambito | Alto | AI Platform, Knowledge | AI governance e divieto su safety non approvata | TBD |
| `DSG-RISK-005` | Documentazione divergente dal sistema | Medio | Documentation, Portal | Review, registri, release gate | Mitigato |
| `DSG-RISK-006` | Configurazioni sensibili pubblicate | Alto | Security, ACM | Security gate e template sanitizzati | Mitigato |

## 10. KPI Framework

| KPI | Dominio | Formula o criterio | Stato | Evidenza |
|---|---|---|---|---|
| Copertura documentale | Documentation | Documenti pubblicati / documenti pianificati | Transition | `mkdocs.yml`, registry |
| Link health | Documentation | Link validi / link totali | Transition | Verifica link |
| Rischi mitigati | Governance | Rischi con controllo / rischi totali | Transition | DSRA, registri |
| Sessioni completate | Operations | Sessioni completate / sessioni pianificate | Da validare | Log sessione |
| Qualita dati | Data | Dataset conformi / dataset elaborati | Transition | Report analytics |
| Uptime accesso remoto | Infrastructure | Tempo disponibile / tempo totale | Da validare | Registro test |
| Incident recurrence | Operations | Incidenti ricorrenti per periodo | Da validare | Post-mortem |
| AI assisted tasks | AI | Task assistiti con review / task totali | TBD | Audit AI |

## 11. Controlli

| Controllo | Applicazione |
|---|---|
| `DSG-CTL-PLAN-001` | Ogni milestone aggiorna deliverable e registry |
| `DSG-CTL-PLAN-002` | Ogni sprint ha output verificabile |
| `DSG-CTL-PLAN-003` | Ogni release passa da readiness checklist |
| `DSG-CTL-PLAN-004` | KPI privi di fonte restano `Da validare` |

## 12. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-PLAN-TBD-001` | Dettaglio trimestrale 2026-2030 | TBD |
| `DSG-PLAN-TBD-002` | Soglie quantitative KPI | Da validare |
| `DSG-PLAN-TBD-003` | Frequenze test rete, DR e asset audit | Da validare |
| `DSG-PLAN-TBD-004` | Use case AI e Live Operations approvati | TBD |

## 13. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Enterprise Program Portfolio](program-portfolio.md)
- [Enterprise Registry](registries/index.md)
- [Governance](governance.md)
- [Release documentation](release-documentation.md)
