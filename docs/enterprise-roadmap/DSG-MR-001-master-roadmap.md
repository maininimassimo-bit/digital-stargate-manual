# DSG-MR-001 - Digital StarGate Master Roadmap

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Master Roadmap |
| Identificativo | `DSG-MR-001` |
| Stato | Approvata |
| Versione | 1.0 |
| Lingua | Italiano |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## Collegamenti alla documentazione esistente

La roadmap collega la visione enterprise ai contenuti MkDocs gia presenti:

- [Home del portale](../index.md)
- [Architettura Digital StarGate](../architecture/index.md)
- [Architettura del Warehouse](../architecture/warehouse/index.md)
- [Portale Analytics](../analytics/index.md)
- [Stato osservatorio](../status/index.md)
- [Roadmap evolutiva tecnica](../chapters/33-roadmap-evolutiva.md)
- [Gestione documentale e release](../chapters/34-gestione-documentale-release.md)
- [Requisiti e tracciabilita](../chapters/40-requisiti-tracciabilita.md)
- [Analisi rischi e FMEA](../chapters/41-analisi-rischi-fmea.md)
- [Baseline enterprise](../enterprise/index.md)

---

# PART I - Enterprise Foundation

## 1 Executive Summary

`DSG-MR-001` e la roadmap master enterprise di Digital StarGate. Il documento coordina osservatorio remoto, infrastruttura, operations, dati, repository scientifico, analytics, live operations, AI, documentazione, conoscenza, community, sicurezza, governance tecnica, asset e configurazioni.

La roadmap non sostituisce il manuale tecnico: lo governa. Le informazioni gia documentate sono trattate come AS-IS; le capacita in consolidamento sono Transition; le evoluzioni non ancora verificabili sono TO-BE e marcate `TBD` o `Da validare`.

## 2 Vision

Digital StarGate deve evolvere in una piattaforma enterprise personale, sicura e data-driven per governare un osservatorio astronomico remoto. La visione integra osservazione, automazione, documentazione, dati, analytics e conoscenza in un portale coerente e revisionabile.

La visione evita automatismi non dimostrati: nessuna funzione live o AI viene considerata operativa senza evidenze, controlli e governance.

## 3 Mission

La missione e rendere l'osservatorio remoto documentato, verificabile, mantenibile e progressivamente evolutivo. Ogni componente deve poter essere compreso, operato, verificato e migliorato senza perdere tracciabilita.

La missione operativa include safety, continuita, qualita dati, release documentali, gestione dei rischi e conservazione della conoscenza.

## 4 Core Values

| Valore | Applicazione |
|---|---|
| Sicurezza | Lo stato conservativo prevale su automazione e velocita |
| Verificabilita | Ogni dettaglio critico richiede fonte o stato `Da validare` |
| Tracciabilita | Requisiti, rischi, decisioni, controlli e release sono collegati |
| Continuita | Le evoluzioni non rompono manuale, procedure e pubblicazione |
| Semplicita operativa | Le procedure devono essere usabili durante attivita reali |
| Qualita documentale | MkDocs e GitHub restano la fonte governata |

## 5 Guiding Principles

| ID | Principio | Significato |
|---|---|---|
| `DSG-GP-001` | Docs-as-Code | Markdown e `mkdocs.yml` sono fonte primaria |
| `DSG-GP-002` | Safety-first | Meteo, park, copertura e accesso sicuro sono vincoli bloccanti |
| `DSG-GP-003` | AS-IS before TO-BE | Le evoluzioni partono dallo stato documentato |
| `DSG-GP-004` | Incrementalita | Ogni milestone produce evidenza verificabile |
| `DSG-GP-005` | Separazione domini | Operations, dati, analytics, AI e documentazione hanno confini distinti |
| `DSG-GP-006` | Evidenza minima | Log, checklist, commit, report o registro dimostrano il controllo |

## 6 Strategic Objectives

| ID | Obiettivo | Orizzonte | Evidenza |
|---|---|---|---|
| `DSG-SO-001` | Pubblicare la foundation enterprise | 2026 | Roadmap, registri, governance |
| `DSG-SO-002` | Consolidare dati, warehouse e analytics | 2026-2027 | Schemi e quality gate |
| `DSG-SO-003` | Rafforzare operations e safety | 2026-2028 | SOP, FMEA, incident log |
| `DSG-SO-004` | Abilitare live operations controllate | 2027-2029 | Feed validati e policy |
| `DSG-SO-005` | Preparare AI assistiva governata | 2028-2030 | AI governance e audit |
| `DSG-SO-006` | Costruire knowledge base e community | 2027-2030 | Glossari, handbook, materiali riusabili |

## 7 Enterprise Scope

L'ambito comprende osservatorio, infrastruttura, operations, dati, repository immagini/scientifico, analytics, live operations, AI, documentazione, conoscenza, community, sicurezza, engineering governance, asset e configurazioni.

Sono esclusi credenziali, segreti, configurazioni operative sensibili, certificazioni esterne non documentate e dettagli tecnici non verificabili.

## 8 Success Criteria

| ID | Criterio | Misura |
|---|---|---|
| `DSG-SC-001` | Roadmap pubblicata | Voce MkDocs attiva |
| `DSG-SC-002` | AS-IS, Transition e TO-BE distinti | Sezioni 11-13 |
| `DSG-SC-003` | Portfolio completo | Sezioni 17-30 |
| `DSG-SC-004` | Registri enterprise definiti | Sezioni 31-37 |
| `DSG-SC-005` | Governance completa | Sezioni 45-52 |
| `DSG-SC-006` | Dati mancanti espliciti | Uso di `TBD` e `Da validare` |

## 9 Governance Principles

La governance richiede owner, stato, evidenza e revisione per ogni elemento rilevante. Una modifica strutturale richiede ADR o decision log; un rischio medio o alto richiede controllo; una release richiede quality gate e rollback.

## 10 Roadmap Governance

La roadmap e un documento vivo. Viene aggiornata a ogni release significativa, modifica architetturale, incidente rilevante o introduzione di nuove capability. Le modifiche passano da GitHub e devono mantenere coerenza con `mkdocs.yml`.

---

# PART II - Enterprise Architecture

## 11 AS-IS

AS-IS indica cio che e gia documentato o operativo nel repository. Sono AS-IS il portale MkDocs, la struttura manuale, le sezioni su osservatorio, rete, software astronomico, procedure operative, analytics e warehouse documentato.

| Dominio | Stato | Riferimento |
|---|---|---|
| Manuale tecnico | AS-IS | Capitoli 1-44 |
| Portale MkDocs | AS-IS | `mkdocs.yml` |
| Osservatorio remoto | AS-IS documentato | Capitoli infrastruttura e sistema astronomico |
| Analytics | AS-IS/Transition | Sezione Analytics |
| Warehouse | Transition documentata | Sezione Warehouse |
| Live Operations | TO-BE | Roadmap evolutiva |
| AI | TO-BE | `TBD` |

## 12 Transition

Transition e la fase che trasforma il manuale tecnico in piattaforma governata. Include roadmap enterprise, registri, quality gate, collegamento tra dati e analytics, formalizzazione asset/configurazioni e preparazione di live operations.

Gli output Transition devono rimanere incrementali e revisionabili.

## 13 TO-BE

TO-BE descrive il modello target: osservatorio governato da SOP e registri, dati con schema e qualita, repository scientifico con metadati, analytics affidabili, live operations validate, AI assistiva controllata e knowledge base riusabile.

Tutti i dettagli non presenti nel repository restano `TBD` o `Da validare`.

## 14 Enterprise Platform Model

Il modello piattaforma e organizzato per layer: Observatory, Infrastructure, Operations, Data, Analytics, Live Operations, Knowledge, Documentation e Governance.

Ogni layer deve avere confini chiari, owner, interfacce, rischi e controlli collegati.

## 15 Capability Model

| Capability | AS-IS | Transition | TO-BE |
|---|---|---|---|
| Remote Observatory Control | Documentato | Rafforzamento controlli | Evidenze complete |
| Session Execution | Documentato | Lifecycle misurabile | Automazione governata |
| Safety and Recovery | Documentato | Registri incident | Governance matura |
| Data Collection | Presente | Normalizzazione | Contratti dati |
| Scientific Repository | Parziale | Modello metadati | Archivio governato |
| Analytics | Presente | Quality gate | KPI storici evoluti |
| Live Operations | Roadmap | Feed controllati | Stato live affidabile |
| AI Assistance | Non baseline | Governance | Supporto auditabile |
| Documentation | Presente | Roadmap enterprise | Knowledge base integrata |

## 16 Platform Interaction

Le interazioni principali sono: osservatorio verso operations, operations verso dati, dati verso analytics, analytics verso documentazione, live operations verso portale, AI verso knowledge base e governance verso tutti i layer.

Regola bloccante: AI e live operations non comandano funzioni safety senza decisione approvata e controllo documentato.

---

# PART III - Program Portfolio

## 17 Observatory

Programma dedicato a cupola, montatura, ottiche, camere, treno ottico e sicurezza fisica. Lo stato e AS-IS documentato; le evoluzioni devono aggiornare asset, configurazioni, rischi e procedure.

Priorita: checklist safety, manutenzione, test sensori e integrazione futura con Live Operations.

## 18 Infrastructure

Programma dedicato a rete, accesso remoto, EAGLE, alimentazione, storage, backup e disaster recovery. Frequenze test failover, autonomia UPS e retention log sono `Da validare`.

## 19 Operations

Programma dedicato ad avvio, acquisizione, chiusura, manutenzione, incident response e post-mortem. Ogni procedura deve avere trigger, passi, output, criteri di controllo ed evidenza.

## 20 Data

Programma dedicato a log, report sessione, dataset, warehouse e qualita dati. Ogni dato pubblicato deve indicare fonte, periodo e stato. Schema finale data catalog: `TBD`.

## 21 Image and Scientific Repository

Capability dedicata a immagini, target, sessioni, strumenti, metadati e qualita scientifica. Lo stato attuale e parziale: session report presenti, modello repository immagini finale `Da validare`.

## 22 Analytics and Reporting

Programma dedicato a KPI, dashboard, reportistica e validazione storico. Deve separare calcolo, dataset, rendering e note di qualita.

## 23 Live Operations

Capability TO-BE per stato cupola, montatura, sequenza, meteo, AllSky, target e qualita guida. Tutti i feed live restano `Da validare` finche non esistono contratti dati, controlli safety e policy di pubblicazione.

## 24 AI

Programma TO-BE per assistenza documentale, ricerca conoscenza, diagnosi, sintesi post-mortem e analisi qualita. Modelli, strumenti, retention e casi d'uso restano `TBD`. L'AI non prende decisioni operative safety.

## 25 Documentation

Programma dedicato a MkDocs, navigazione, release, registri, handbook, SOP e ADR. Ogni pagina pubblicata deve essere raggiungibile e coerente con la struttura esistente.

## 26 Knowledge

Programma per trasformare manuale, SOP, ADR, registri, incidenti e release in conoscenza riusabile. Knowledge base AI-ready: `TBD`.

## 27 Community

Programma di lungo periodo per collaboratori, revisori, lettori e possibili contributori scientifici. Canali, policy contributive e apertura community sono `Da validare`.

## 28 Security

Programma dedicato a accessi remoti, segreti, esposizione dati, configurazioni sensibili, live operations e AI. Nessun segreto deve essere versionato. Ogni release e bloccata da credenziali esposte.

## 29 Engineering Governance

Programma che assicura disciplina tecnica tramite ADR, registri, quality gate, PR review, release notes, change log e assessment.

## 30 Asset and Configuration Management

Programma per asset fisici, software, configurazioni, versioni e obsolescenza. Registro asset completo, audit configurazioni e mapping asset-config-requisiti sono `Da validare`.

---

# PART IV - Enterprise Registry

## 31 Platform Registry

| ID | Piattaforma | Stato |
|---|---|---|
| `DSG-PLT-001` | Digital StarGate Portal | AS-IS |
| `DSG-PLT-002` | Remote Observatory | AS-IS |
| `DSG-PLT-003` | Data and Analytics Platform | Transition |
| `DSG-PLT-004` | Live Operations Platform | TO-BE |
| `DSG-PLT-005` | AI-assisted Knowledge Platform | `TBD` |

## 32 Program Registry

| ID | Programma | Orizzonte | Stato |
|---|---|---|---|
| `DSG-PRG-OBS` | Observatory | 2026-2030 | AS-IS/Transition |
| `DSG-PRG-INF` | Infrastructure | 2026-2030 | AS-IS/Transition |
| `DSG-PRG-OPS` | Operations | 2026-2030 | Transition |
| `DSG-PRG-DATA` | Data | 2026-2030 | Transition |
| `DSG-PRG-IMG` | Image and Scientific Repository | 2027-2030 | TO-BE |
| `DSG-PRG-ANL` | Analytics and Reporting | 2026-2030 | Transition |
| `DSG-PRG-LIVE` | Live Operations | 2027-2030 | TO-BE |
| `DSG-PRG-AI` | AI | 2028-2030 | `TBD` |
| `DSG-PRG-DOC` | Documentation | 2026-2030 | Transition |
| `DSG-PRG-SEC` | Security | 2026-2030 | Transition |

## 33 Component Registry

| ID | Componente | Dominio | Stato |
|---|---|---|---|
| `DSG-CMP-MKDOCS` | MkDocs Material portal | Documentation | AS-IS |
| `DSG-CMP-GITHUB` | GitHub repository and Pages | Release | AS-IS |
| `DSG-CMP-EAGLE` | PrimaLuceLab EAGLE | Infrastructure | AS-IS |
| `DSG-CMP-CGX-L` | Montatura Celestron CGX-L | Observatory | AS-IS |
| `DSG-CMP-NINA` | N.I.N.A. | Operations | AS-IS |
| `DSG-CMP-PHD2` | PHD2 | Operations | AS-IS |
| `DSG-CMP-CPWI` | CPWI | Operations | AS-IS |
| `DSG-CMP-WAREHOUSE` | Warehouse | Data | Transition |
| `DSG-CMP-ANALYTICS` | Dashboard analytics | Analytics | Transition |
| `DSG-CMP-LIVE` | Live Observatory | Live Operations | TO-BE |
| `DSG-CMP-AI` | AI assistant | AI | `TBD` |

## 34 Technology Registry

Tecnologie documentate: MkDocs Material, Markdown, GitHub, Python, ASCOM, N.I.N.A., PHD2, CPWI, warehouse tooling e analytics tooling. Tecnologia AI: `TBD`.

## 35 Asset Registry

Classi asset: struttura, energia, rete, computer, astronomia, dati e documentazione. Il registro asset finale deve essere consolidato con inventario e asset management; dettagli quantitativi non presenti sono `Da validare`.

## 36 Configuration Registry

Configurazioni: MkDocs, CSS/JS portale, software astronomico, router/VPN, warehouse schema, analytics configuration, live configuration e AI configuration. Configurazioni sensibili non devono essere pubblicate.

## 37 Knowledge Registry

Knowledge registry: manuale tecnico, ADR, SOP, rischi/FMEA, warehouse/analytics, incidenti, release notes e knowledge AI-ready. Stato AI-ready: `TBD`.

---

# PART V - Planning

## 38 Release Strategy

Le release sono documentali, architetturali, dati/analytics, operations, live e AI. Ogni release dichiara scope, file, milestone, validazioni, rischi residui, rollback e follow-up.

## 39 Milestone Strategy

| Milestone | Obiettivo | Output |
|---|---|---|
| `M1 Foundation` | Baseline enterprise | Roadmap e governance |
| `M2 Data` | Data/warehouse | Schemi e quality gate |
| `M3 Operations` | Safety e procedure | SOP e incident log |
| `M4 Live` | Stato live validato | Feed e policy |
| `M5 AI` | AI governance | Guardrail e audit |
| `M6 Community` | Knowledge condivisibile | Guide e template |

## 40 Sprint Strategy

Ogni sprint usa ID `DSG-SPR-YYYY-NN`, milestone collegata, scope limitato, output verificabile, quality gate e stato. Gli sprint non devono introdurre cambiamenti non tracciati.

## 41 Enterprise Roadmap 2026-2030

| Anno | Focus | Deliverable |
|---|---|---|
| 2026 | Foundation enterprise | Roadmap, registri, governance |
| 2027 | Data e operations hardening | Warehouse maturo, SOP rafforzate |
| 2028 | Live Operations controllate | Feed validati e dashboard live |
| 2029 | AI assistiva governata | Knowledge assistant e audit |
| 2030 | Piattaforma data-driven | Osservatorio, dati, analytics e governance integrati |

## 42 Dependency Matrix

| Dipendenza | Impatta | Stato |
|---|---|---|
| `mkdocs.yml` coerente | Documentation/release | AS-IS |
| Connettivita remota | Operations/live | Da validare periodicamente |
| Log sessione | Data/analytics | AS-IS |
| Warehouse schema | Analytics/reporting | Transition |
| Registro asset | Configuration/maintenance | Da consolidare |
| Safety state | Operations/live/AI | Critico |
| AI governance | AI/knowledge | `TBD` |

## 43 Risk Matrix

| ID | Rischio | Impatto | Mitigazione |
|---|---|---|---|
| `DSG-RISK-001` | Stato operativo non sicuro | Alto | SOP, FMEA, stato conservativo |
| `DSG-RISK-002` | Dati incompleti | Medio | Quality gate e metadati |
| `DSG-RISK-003` | Live operations non validate | Alto | Policy e feed controllati |
| `DSG-RISK-004` | AI oltre ambito | Alto | AI governance e audit |
| `DSG-RISK-005` | Documentazione divergente | Medio | Review e registri |
| `DSG-RISK-006` | Segreti pubblicati | Alto | Security gate |

## 44 KPI Framework

| KPI | Dominio | Stato |
|---|---|---|
| Copertura documentale | Documentation | Transition |
| Link health | Documentation | Transition |
| Rischi mitigati | Governance | Transition |
| Sessioni completate | Operations | Da validare |
| Qualita dati | Data | Transition |
| Uptime accesso remoto | Infrastructure | Da validare |
| Incident recurrence | Operations | Da validare |
| AI assisted tasks | AI | `TBD` |

---

# PART VI - Governance

## 45 Architecture Governance

Ogni cambiamento architetturale dichiara AS-IS, Transition o TO-BE, impatti, owner, rischi, controlli e ADR quando la scelta e strutturale.

## 46 Change Management

Il change management segue richiesta, classificazione, impatto, approvazione, implementazione, validazione, release e aggiornamento registri.

## 47 Configuration Management

Le configurazioni sono pubblicabili, template sanitizzati, operative sensibili o `Da validare`. I segreti non entrano nel repository.

## 48 Data Governance

Ogni dataset deve avere fonte, periodo, qualita e schema quando applicabile. I dati mancanti usano `N/D`; gli schemi contrattuali devono essere versionati.

## 49 AI Governance

AI governance richiede casi d'uso approvati, audit output, esclusione segreti, nessun comando safety autonomo, separazione tra suggerimento e decisione. Policy privacy e retention: `TBD`.

## 50 Quality Gates

| Gate | Descrizione | Bloccante |
|---|---|---|
| `QG-DOC` | Link, navigazione, marcatori aperti | Si |
| `QG-SEC` | Assenza segreti | Si |
| `QG-ARCH` | ADR per scelte strutturali | Quando applicabile |
| `QG-DATA` | Fonte, schema e qualita dati | Per dati pubblicati |
| `QG-OPS` | SOP e safety check | Per operations |
| `QG-REL` | Release notes e rollback | Per release |
| `QG-AI` | Guardrail e audit | Per AI |

## 51 Documentation Governance

La documentazione mantiene struttura MkDocs coerente, link verificati, terminologia stabile, documenti correlati, registri aggiornati e marcatori `TBD` o `Da validare` per dettagli non verificati.

## 52 Release Governance

Ogni release dichiara scope, file modificati, milestone, validazioni, rischi residui, rollback e follow-up non bloccanti.

---

# PART VII - Long-Term Vision

## 53 Vision 2030

Entro il 2030 Digital StarGate mira a integrare osservatorio, dati, analytics, knowledge base e governance in una piattaforma data-driven con live operations validate e AI assistiva controllata.

## 54 Vision 2035

La visione 2035 e un ecosistema osservativo e conoscitivo maturo, con automazioni predittive controllate, repository scientifico evoluto, community e AI knowledge assistant avanzato. Tutte le direttrici restano `TBD` finche non approvate.

## 55 Continuous Evolution

L'evoluzione continua segue il ciclo: osservare, documentare, validare, governare, automatizzare solo quando sicuro, misurare e riesaminare.

## 56 Conclusion

`DSG-MR-001` stabilisce la Master Roadmap enterprise di Digital StarGate. Il documento distingue AS-IS, Transition e TO-BE, collega la roadmap alla documentazione esistente e definisce portfolio, registri, pianificazione, governance e visione di lungo periodo.

La roadmap e completa come baseline approvata; i dettagli non verificati restano esplicitamente `TBD` o `Da validare`.
