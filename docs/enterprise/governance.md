# DSG-GOV-001 - Enterprise Governance Framework

| Campo | Valore |
|---|---|
| Documento | Enterprise Governance Framework |
| Identificativo | `DSG-GOV-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy inclusa | Roadmap Freeze Policy |

## 1. Scopo

Questo documento definisce il framework di governance enterprise per Digital StarGate. Governa architettura, cambiamenti, configurazioni, dati, AI, quality gate, documentazione, release, sicurezza e Disaster Recovery in coerenza con `DSG-MR-001`.

La governance non introduce nuovi programmi o piattaforme: applica la roadmap congelata, il [Program Portfolio](program-portfolio.md), i [registri enterprise](registries/index.md), il meta-modello [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md) e la reference architecture [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md).

## 2. Ambito

La governance copre:

- Architecture Governance;
- Change Management;
- Configuration Management;
- Data Governance;
- AI Governance;
- Quality Gates;
- Documentation Governance;
- Release Governance;
- Security Governance;
- Disaster Recovery Governance.

Sono esclusi dettagli tecnici non documentati, configurazioni operative sensibili, credenziali, canali privati e responsabilità nominative non confermate.

## 3. Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-GOV-PRN-001` | Roadmap Freeze | `DSG-MR-001` è il perimetro approvato |
| `DSG-GOV-PRN-002` | No parallel structure | Si aggiornano fonti esistenti prima di creare nuovi documenti |
| `DSG-GOV-PRN-003` | AS-IS before TO-BE | Ogni evoluzione parte dallo stato documentato |
| `DSG-GOV-PRN-004` | Evidence-based review | Ogni controllo produce evidenza verificabile |
| `DSG-GOV-PRN-005` | Safety-first | Operations, Live Operations e AI rispettano safety boundary |
| `DSG-GOV-PRN-006` | TBD discipline | Dati non confermati restano `TBD` o `Da validare` |

## 4. DSG-GOV-001 Roadmap Freeze Policy

La Roadmap Freeze Policy stabilisce che `DSG-MR-001` è la fonte gerarchica primaria per programmi, piattaforme, capability e governance.

Regole:

| ID | Regola | Controllo |
|---|---|---|
| `DSG-FRZ-001` | Non introdurre nuovi programmi fuori roadmap | Verifica Program Registry |
| `DSG-FRZ-002` | Non introdurre nuove piattaforme fuori Platform Registry | Verifica Platform Registry |
| `DSG-FRZ-003` | Non duplicare documenti che hanno già fonte corretta | Review documentale |
| `DSG-FRZ-004` | Ogni nuova capability deve mappare a programma esistente | `DSG-EAM-001` e `DSRA-001` |
| `DSG-FRZ-005` | Le informazioni non confermate devono essere marcate | `TBD` o `Da validare` |
| `DSG-FRZ-006` | Le decisioni strutturali richiedono ADR | `QG-ARCH` |

Eccezioni: solo una roadmap successiva o una decisione approvata può modificare il perimetro congelato. Fino ad allora, le proposte restano `Proposto` o `TBD`.

## 5. Ruoli e responsabilità

| Attività | Owner | Contributor | Reviewer | Approver | Stato |
|---|---|---|---|---|---|
| Roadmap enterprise | Governance Owner | Documentation Owner | Architecture Owner | Massimo Mainini | Transition |
| Program Portfolio | Governance Owner | Program Owner | Architecture Owner | Massimo Mainini | Transition |
| Architettura | Architecture Owner | Data Owner | Reviewer tecnico | Massimo Mainini | Transition |
| Registry | Documentation Owner | Tutti gli owner | Governance Owner | Massimo Mainini | Transition |
| DSRA | Operations Owner | Infrastructure Owner | Governance Owner | Massimo Mainini | Transition |
| SOP | Operations Owner | Documentation Owner | Reviewer operativo | Massimo Mainini | Transition |
| Data governance | Data Owner | Architecture Owner | Governance Owner | Massimo Mainini | Da validare |
| AI governance | Governance Owner | Data Owner | Security Owner | Massimo Mainini | TBD |
| Security governance | Security Owner | Infrastructure Owner | Governance Owner | Massimo Mainini | Da validare |
| Disaster Recovery governance | Infrastructure Owner | Operations Owner | Governance Owner | Massimo Mainini | Da validare |
| Release | Release Owner | Documentation Owner | Reviewer | Massimo Mainini | Transition |

Gli owner funzionali sono ruoli di governance. Le assegnazioni nominative diverse da Massimo Mainini restano `Da validare`.

## 6. Processo decisionale

| Tipo decisione | Strumento | Criterio | Output |
|---|---|---|---|
| Architetturale | ADR | Impatta componenti, dati, deployment o confini di responsabilità | ADR e registry |
| Portfolio | Program Registry | Impatta programma o capability roadmap | Aggiornamento portfolio/registry |
| Operativa | SOP o capitolo manuale | Impatta avvio, chiusura, recovery o manutenzione | SOP e controllo |
| Documentale | Registro e PR | Impatta navigazione, struttura o template | Diff e change log |
| Release | Release documentation | Impatta readiness, rollback o comunicazione | Checklist release |
| Rischio | DSRA | Impatta safety, continuità, dati o sicurezza | Rischio, controllo, evidenza |
| Security | Security gate | Impatta accessi, segreti, dati sensibili | Finding e remediation |
| AI | AI Governance | Impatta uso AI, dati o decisioni operative | Use case, audit, guardrail |

## 7. Architecture Governance

| Campo | Valore |
|---|---|
| Scopo | Mantenere coerenza tra roadmap, meta-modello, target architecture e reference architecture |
| Ambito | Domini, componenti, capability, interazioni, AS-IS/Transition/TO-BE |
| Input | `DSG-MR-001`, `DSG-EAM-001`, `DSRA-000`, `DSRA-001`, ADR |
| Output | Decisioni, registri aggiornati, ADR, evidenze review |

Processo:

1. Identificare il cambiamento o la nuova esigenza.
2. Classificare stato AS-IS, Transition o TO-BE.
3. Verificare la conformità alla Roadmap Freeze Policy.
4. Aggiornare registri e documenti architetturali.
5. Redigere ADR se cambia una scelta strutturale.
6. Applicare `QG-ARCH`.

Controlli: `DSG-CTL-ADR-001`, `QG-ARCH`, verifica registry.

Rischi: duplicazione architetturale, nuovo dominio non approvato, stato TO-BE dichiarato come implementato.

KPI/evidenze: ADR aggiornati, componenti registrati, decisioni collegate a roadmap.

TBD: ownership nominale Architecture Owner.

## 8. Change Management

| Campo | Valore |
|---|---|
| Scopo | Governare modifiche documentali, tecniche e operative |
| Ambito | PR, change log, impatti, rollback, follow-up |
| Input | Richiesta modifica, issue, ADR, rischio, evidenza operativa |
| Output | Change log, documenti aggiornati, validazione, release note |

Processo:

1. Identificazione.
2. Classificazione per area: Architecture, Data, Operations, Security, Documentation, Release.
3. Valutazione impatti su roadmap, registry, DSRA e MkDocs.
4. Approvazione o marcatura `Da validare`.
5. Implementazione documentata.
6. Validazione statica o build.
7. Commit e PR.
8. Aggiornamento change log.

Controlli: `DSG-CTL-QA-001`, `DSG-CTL-DOC-001`, `QG-REL`.

Rischi: modifica non tracciata, drift documentale, rollback non definito.

KPI/evidenze: change log aggiornato, commit logici, PR con riepilogo.

TBD: modello formale di change request.

## 9. Configuration Management

| Campo | Valore |
|---|---|
| Scopo | Classificare, versionare e controllare configurazioni pubblicabili e sensibili |
| Ambito | MkDocs, portale, software astronomico, rete, warehouse, analytics, live, AI |
| Input | Configurazioni, template, capitoli tecnici, registry |
| Output | Configuration Registry, template sanitizzati, evidenze audit |

Regole:

- configurazioni pubblicabili possono vivere nel repository;
- configurazioni sensibili non devono essere pubblicate;
- template e valori fittizi devono essere chiaramente sanitizzati;
- ogni configurazione rilevante deve apparire nel Configuration Registry;
- parametri non confermati restano `Da validare`.

Controlli: `DSG-CTL-CFG-001`, `QG-SEC`, `QG-DOC`.

Rischi: credenziali pubblicate, configurazioni divergenti, parametri non verificati.

KPI/evidenze: configurazioni classificate, audit senza finding, registry aggiornato.

TBD: frequenza audit configurazioni e baseline completa asset/config.

## 10. Data Governance

| Campo | Valore |
|---|---|
| Scopo | Garantire lineage, qualità, definizione e pubblicabilità dei dati |
| Ambito | Session report, warehouse, reporting, analytics, repository immagini |
| Input | Log, report sessione, dataset, schema, metadata |
| Output | Dataset validati, KPI, anomalie, data registry |

Regole:

- ogni dataset deve avere fonte, periodo e stato qualità;
- ogni KPI deve avere definizione e sorgente;
- dati mancanti devono usare `N/D`, `TBD` o `Da validare` secondo contesto;
- schema e contratti dati devono essere versionati quando diventano baseline;
- immagini scientifiche e metadati restano governati ma lo schema finale è `TBD`.

Controlli: `DSG-CTL-DATA-001`, `QG-DATA`.

Rischi: KPI non confrontabili, dataset senza lineage, metadata incompleti.

KPI/evidenze: qualità dati, record esclusi, dashboard con fonte.

TBD: data catalog finale e scientific metadata model.

## 11. AI Governance

| Campo | Valore |
|---|---|
| Scopo | Governare AI assistiva senza superare limiti safety e security |
| Ambito | Knowledge search, sintesi, diagnosi documentale, supporto non safety |
| Input | Knowledge base approvata, registri, use case approvati |
| Output | Suggerimenti revisionati, audit output, decisioni umane |

Regole:

- nessun comando autonomo su funzioni safety;
- nessun accesso a segreti o configurazioni sensibili;
- ogni output AI deve essere revisionabile;
- i casi d'uso devono essere approvati prima dell'uso operativo;
- modello, strumenti, retention e privacy restano `TBD` finché non validati.

Controlli: `QG-AI`, `QG-SEC`, review umana.

Rischi: automazione non autorizzata, esposizione dati, suggerimenti non verificati.

KPI/evidenze: task assistiti con review, finding AI, audit output.

TBD: use case approvati, tooling, modello di audit.

## 12. Quality Gates

| Gate | Descrizione | Applicazione | Bloccante | Evidenza |
|---|---|---|---|---|
| `QG-DOC` | Link, navigazione, documenti raggiungibili | Documentazione | Si | Log controllo o build |
| `QG-SEC` | Assenza credenziali e dati sensibili | Tutti | Si | Scansione e review |
| `QG-ARCH` | ADR o decisione per scelte strutturali | Architettura | Quando applicabile | ADR/registry |
| `QG-DATA` | Fonte, schema e qualità dataset | Dati pubblicati | Si per dati pubblicati | Report validazione |
| `QG-OPS` | SOP e safety check | Operations/Live | Si | Checklist |
| `QG-REL` | Release notes, readiness e rollback | Release | Si | Checklist release |
| `QG-AI` | Guardrail, audit e human review | AI | Si per AI | Audit e use case |
| `QG-DR` | Recovery e rollback verificabili | DR | Si per release critiche | Test restore o piano |

TBD: soglie quantitative per alcuni gate.

## 13. Documentation Governance

| Campo | Valore |
|---|---|
| Scopo | Mantenere la documentazione coerente, navigabile e tracciabile |
| Ambito | Markdown, MkDocs, indici, registri, SOP, release |
| Input | Modifiche documentali, roadmap, registri |
| Output | Documenti aggiornati, `mkdocs.yml`, link, evidenze |

Regole:

- aggiornare fonti esistenti prima di creare nuovi file;
- evitare strutture parallele;
- usare lingua italiana tecnico-professionale;
- mantenere termini tecnici ufficiali in inglese quando consolidati;
- mantenere link relativi Markdown;
- aggiornare MkDocs solo con percorsi esistenti;
- marcare dati non confermati come `TBD` o `Da validare`.

Controlli: `DSG-CTL-DOC-001`, `DSG-CTL-QA-001`, `QG-DOC`.

Rischi: duplicazioni, link rotti, documento non raggiungibile, terminologia incoerente.

KPI/evidenze: link health, coverage documentale, build MkDocs.

TBD: automazione completa della verifica link nel runtime locale.

## 14. Release Governance

| Campo | Valore |
|---|---|
| Scopo | Garantire release tracciabili, reversibili e verificabili |
| Ambito | Milestone, commit, PR, release notes, rollback |
| Input | Deliverable, registry, validazioni, rischi residui |
| Output | Release documentation, readiness checklist, PR summary |

Regole:

- ogni release deve dichiarare scope, milestone e file principali;
- ogni release deve riportare validazioni eseguite e limiti noti;
- rollback deve essere documentato quando cambia navigazione o pubblicazione;
- follow-up non bloccanti devono essere separati dai blocchi;
- PR verso `main` solo quando richiesto o a completamento del workflow previsto.

Controlli: `DSG-CTL-REL-001`, `QG-REL`, `QG-DOC`, `QG-SEC`.

Rischi: release incompleta, evidenze mancanti, rollback non praticabile.

KPI/evidenze: checklist release, commit hash, log validazione.

TBD: integrazione completa con GitHub Actions.

## 15. Security Governance

| Campo | Valore |
|---|---|
| Scopo | Prevenire esposizione di segreti, accessi e dati sensibili |
| Ambito | Repository, configurazioni, rete, AI, Live Operations, pubblicazione |
| Input | Diff, configurazioni, documenti tecnici, registry |
| Output | Finding, remediation, security evidence |

Regole:

- nessuna credenziale o parametro sensibile nel repository;
- configurazioni operative solo in forma sanitizzata;
- Live Operations non deve pubblicare stato sensibile non approvato;
- AI non deve ricevere o produrre segreti;
- ogni finding security blocca la release finché non risolto o formalmente escluso.

Controlli: `QG-SEC`, `DSG-CTL-SEC-001`, review manuale.

Rischi: esposizione accessi remoti, dati sensibili, configurazioni operative.

KPI/evidenze: scansione senza finding, remediation chiuse, diff controllato.

TBD: tooling di scansione dedicato e policy retention security.

## 16. Disaster Recovery Governance

| Campo | Valore |
|---|---|
| Scopo | Governare continuità, backup, restore, rollback e ripristino operativo |
| Ambito | Repository, portale, dati, EAGLE, configurazioni, procedure conservative |
| Input | Backup, release notes, configurazioni, incident log |
| Output | Piano DR, test restore, evidenze recovery, azioni correttive |

Regole:

- ogni release deve avere criterio di rollback documentale;
- recovery operativo deve privilegiare stato conservativo;
- backup e restore devono produrre evidenza quando testati;
- RTO/RPO non confermati restano `Da validare`;
- incidenti ricorrenti devono aggiornare DSRA e registry.

Controlli: `QG-DR`, `DSG-CTL-DR-001`, `QG-OPS`, `QG-REL`.

Rischi: ripristino non testato, perdita dati, indisponibilità accesso remoto.

KPI/evidenze: test restore, tempo di ripristino, esito rollback.

TBD: RTO/RPO target e frequenza test DR.

## 17. Review e ciclo di riesame

| Oggetto | Frequenza minima | Evento straordinario | Evidenza |
|---|---|---|---|
| Roadmap | A ogni release | Cambio strategico | Diff roadmap |
| Portfolio | Ogni milestone enterprise | Nuova capability | Program Registry |
| Architecture | Ogni modifica strutturale | Nuovo dominio o componente | ADR/registry |
| DSRA | Semestrale | Incidente o near miss | Risk update |
| Registri | Ogni PR enterprise | Nuovo rischio, controllo o deliverable | Registry diff |
| SOP | Semestrale | Procedura fallita o cambiamento operativo | SOP update |
| Security | Ogni PR | Finding o esposizione dati | Security check |
| Disaster Recovery | Ogni release critica | Restore fallito o incidente | DR evidence |
| Release documentation | Ogni release | Rollback o hotfix | Release notes |

## 18. Criteri di accettazione

La governance è accettabile quando:

- tutti i domini di governance richiesti sono documentati;
- `DSG-MR-001` resta fonte gerarchica primaria;
- Portfolio e Registry sono collegati alla governance;
- quality gate e controlli hanno evidenze attese;
- AS-IS, Transition e TO-BE sono distinguibili dove pertinente;
- informazioni mancanti sono `TBD` o `Da validare`;
- non sono pubblicate credenziali o configurazioni sensibili.

## 19. Elementi TBD

| ID | Elemento | Stato | Ambito |
|---|---|---|---|
| `DSG-GOV-TBD-001` | Owner nominali per ruoli funzionali | Da validare | Tutti |
| `DSG-GOV-TBD-002` | Soglie quantitative dei quality gate | TBD | Quality Gates |
| `DSG-GOV-TBD-003` | Tooling automatico link/security/AI audit | TBD | Documentation, Security, AI |
| `DSG-GOV-TBD-004` | RTO/RPO e frequenza test restore | Da validare | Disaster Recovery |
| `DSG-GOV-TBD-005` | Data catalog e metadata scientifici finali | TBD | Data Governance |
| `DSG-GOV-TBD-006` | Policy privacy e retention AI | TBD | AI Governance |

## 20. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Enterprise Program Portfolio](program-portfolio.md)
- [Enterprise Registry](registries/index.md)
- [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md)
- [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md)
- [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md)
- [DSRA Risk Assessment](DSRA-risk-assessment.md)
- [SOP](sop.md)
- [Release documentation](release-documentation.md)
- [Assessment](assessment.md)
- [ADR-004](adr/ADR-004-enterprise-documentation-baseline.md)
