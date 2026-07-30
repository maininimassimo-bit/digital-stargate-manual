# AMP-001 — Digital StarGate Architecture Master Plan

| Campo | Valore |
|---|---|
| Documento | Architecture Master Plan |
| Identificativo | AMP-001 |
| Programma | Digital StarGate |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Autorità di pianificazione | Digital StarGate Architecture Office — Program Architect |
| Baseline certificata | ABC-001 — `CONDITIONALLY CERTIFIED` |
| Assessment di riferimento | PAA-002 v1.1 |
| Review indipendente | ARB-002 — `APPROVED WITH CONDITIONS`, 90/100 |
| Stato del piano | Proposed for independent ARB review |

---

## 1. Executive Summary

AMP-001 traduce la baseline architetturale certificata da ABC-001 in un piano evolutivo multi-release, dipendente dalle evidenze e orientato alla sicurezza.

Il piano non ridefinisce le capability esistenti e non autorizza automaticamente implementazioni, deployment o operatività. Mantiene come vincolanti le classificazioni di PAA-002 v1.1 e distingue cinque fasi diverse:

1. consolidamento architetturale e documentale;
2. implementazione;
3. integrazione;
4. deployment;
5. verifica operativa.

Le capability CAP-01…CAP-04 sono trattate come fondazioni repository/architecture già implementate, con i limiti dichiarati nell'Evidence Annex. Live Telemetry, AllSky e AI Assistant restano `Planned`; Observatory Automation, Local Safety Interlocks, Application Observability e Architecture Governance restano `Partial`; AI boundary contracts restano `Prepared`.

La priorità del programma è eliminare ambiguità e duplicazioni prima di introdurre nuove capability live. Il primo Architecture Package raccomandato è **AP-001 — Enterprise Metamodel and Repository Information Architecture**.

---

## 2. Mandato e limiti

AMP-001 è autorizzato esclusivamente come attività di pianificazione da ABC-001.

Il documento:

- usa il repository `main` come fonte autorevole;
- conserva il canonical data flow definito da EA-002, ADR-003 e PAA-002 v1.1;
- impedisce iniziative greenfield duplicate per Analytics, Historical Dashboard, Warehouse e Warehouse Metadata/Validation;
- definisce sequenza, dipendenze, quality gate, handoff e criteri di uscita;
- non certifica runtime, safety hardware, deployment, CI o operatività;
- non modifica la responsabilità degli interblocchi fisici e locali;
- non autorizza controllo remoto o AI tool execution.

Le pull request non integrate e gli artefatti esterni al repository sono esclusi dalla baseline.

---

## 3. Baseline certificata

### 3.1 Fonti autorevoli

| Fonte | Ruolo nel piano |
|---|---|
| EA-001 | Stato dell'ambiente e del repository |
| EA-002 | Stato integrato repository/Warehouse e data flow autorevole |
| ADR-003 | Decisione sull'engine e sul ruolo del Warehouse |
| PAA-002 v1.1 | Capability matrix, gap, rischi e dipendenze |
| ARB-002 | Review indipendente, condizioni e criteri di re-review |
| ABC-001 | Certificazione condizionata della baseline |
| ABC-001 Evidence Annex | Locator immutabili per CAP-01…CAP-04 |
| `mkdocs.yml` | Struttura di pubblicazione e navigazione corrente |

### 3.2 Stato capability vincolante

| Gruppo | Stato iniziale AMP-001 | Regola di avanzamento |
|---|---|---|
| CAP-01…CAP-04 | `Implemented` a livello repository/architecture | Nessuna promozione a operational senza evidenza OPS |
| CAP-05…CAP-07 | `Partial` | Richiedono integrazione e validazione verificabile |
| CAP-08 | `Planned` | Richiede contratti, ingestion, freshness e health |
| CAP-09…CAP-10 | `Missing` | Richiedono decisione architetturale e implementazione |
| CAP-11…CAP-14 | `Partial` | Richiedono servizio e osservabilità end-to-end |
| CAP-15 | `Planned` | Richiede integrazione immagini, metadati e health |
| CAP-16…CAP-17 | `Partial` | Richiedono boundary formali e safety evidence |
| CAP-18 | `Prepared` | Richiede policy, audit, authorization e versioning |
| CAP-19 | `Planned` | Prima release esclusivamente read-only |
| CAP-20…CAP-25 | `Missing` | Differiti fino a readiness dimostrata |
| CAP-26 | `Partial` | Richiede policy dati completa e ADR |
| CAP-27…CAP-30 | `Missing` | Backlog di consolidamento Warehouse/consumer |
| CAP-31…CAP-33 | `Partial` | Richiedono operating model e quality gate applicati |

Nessuno stato viene modificato da AMP-001.

---

## 4. Architettura target di riferimento

Il flusso dati autorevole da preservare è:

```text
Sorgenti dell'osservatorio
        |
        v
Ingestion / Collection
        |
        v
Analytics: interpretazione, normalizzazione e validazione
        |
        v
Dataset Analytics validati
        |
        v
Warehouse: persistenza curata, schema e lineage
        |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
Dashboard                Reporting                 AI
```

Dashboard, Reporting e AI devono usare contratti e access layer governati. Non devono accedere direttamente ai log grezzi o introdurre pipeline parallele.

La piattaforma live futura aggiungerà telemetry, eventi, health, observability e alerting senza sostituire né indebolire gli interblocchi locali.

---

## 5. Principi di programma

1. **Repository truth:** solo gli artefatti presenti nel repository costituiscono baseline.
2. **Evidence before status:** documentazione e configurazione non equivalgono a operatività.
3. **Safety independence:** gli interblocchi fisici e locali rimangono indipendenti da applicazione, portale, cloud e AI.
4. **No duplicate foundations:** le capability già implementate vengono consolidate, non ricostruite.
5. **Canonical contracts:** producer e consumer dipendono da contratti versionati e compatibili.
6. **Unknown is not safe:** dati stale, mancanti o health degradato non sono interpretati come stato sicuro.
7. **Read-only AI first:** la prima capability AI non esegue comandi sugli apparati.
8. **Incremental delivery:** ogni Architecture Package produce un incremento verificabile e reversibile.
9. **Independent approval:** il team che produce un package non approva il proprio lavoro.
10. **Operational claims require OPS:** runtime, freshness e reliability richiedono evidenza operativa.

---

## 6. Gap prioritizzati

| Priorità | Gap | Motivazione |
|---:|---|---|
| 1 | GAP-09 — Architecture Governance Evidence | Prerequisito per traceability, ownership e quality gate |
| 2 | GAP-08 — Data Governance | Prerequisito per contratti, retention, lineage e consumer |
| 3 | GAP-05 — Observatory Automation Boundary | Vincolo safety prima della piattaforma live |
| 4 | GAP-06 — Warehouse Consumer Layer | Evita accessi diretti e pipeline parallele |
| 5 | GAP-01 — Canonical Live Telemetry Model | Base semantica della piattaforma live |
| 6 | GAP-02 — Live Ingestion and Freshness | Necessario per stato live affidabile |
| 7 | GAP-04 — Observability | Necessario per operabilità e incident management |
| 8 | GAP-03 — Time-Series and Event Access | Necessario per telemetry ad alta frequenza |
| 9 | GAP-07 — AI Governance and Safety | Necessario prima di qualunque AI runtime |

---

## 7. Architecture Package roadmap

### Wave A — Governance and Data Consolidation

| Ordine | Package | Owner specialistico | Outcome principale |
|---:|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | Enterprise Architect + Documentation Governor | Tassonomia, identificatori, ownership, relazioni ed evidence chain |
| AP-002 | Data Governance and Canonical Data Contracts | Enterprise/Solution Architect | Policy dati, versioning, compatibility, retention e lineage |
| AP-003 | Analytics and Warehouse Contract Stabilization | Solution Architect | Contratti stabili tra Analytics e Warehouse |
| AP-004 | Incremental and Delta Warehouse Processing | Solution Architect | CAP-27 e CAP-28 implementate e testate |
| AP-005 | Warehouse Consumer and Query Layer | Solution Architect | Access layer SQL/DuckDB e query canoniche |
| AP-006 | Reporting and Historical Dashboard Integration | Solution Architect | Consumer migrati senza pipeline parallele |

### Wave B — Safe Observatory Automation and Live Platform

| Ordine | Package | Owner specialistico | Outcome principale |
|---:|---|---|---|
| AP-007 | Observatory Automation Boundary and Safety Model | Infrastructure Architect + Solution Architect | Separazione safety, control, orchestration, monitoring e override |
| AP-008 | Canonical Device, Sensor and State Contracts | Solution Architect | Contratti canonici per apparati, sensori e stati |
| AP-009 | Live Telemetry Architecture | Solution Architect + Infrastructure Architect | Modello telemetry, heartbeat, freshness e degraded mode |
| AP-010 | Live Ingestion and Connectivity Resilience | Infrastructure Architect | Ingestion, retry, buffering, VPN/network resilience |
| AP-011 | Time-Series and Event Storage Decision | Enterprise/Solution Architect | ADR su storage, retention, query ed eventi |
| AP-012 | Operational Health and Live Dashboard | Solution Architect | Health model e dashboard con freshness esplicita |
| AP-013 | Alerting and Notification Architecture | Infrastructure/Solution Architect | Severità, routing, escalation e test |
| AP-014 | AllSky Integration | Infrastructure/Solution Architect | Immagini, metadati, health e retention |

### Wave C — Observability and Operations

| Ordine | Package | Owner specialistico | Outcome principale |
|---:|---|---|---|
| AP-015 | Application Observability | Solution Architect | Logging, metriche, tracing, correlation e SLI/SLO |
| AP-016 | Infrastructure, EAGLE and Network Monitoring | Infrastructure Architect | Health infrastrutturale, VPN e failover |
| AP-017 | Audit and Correlation Model | Solution Architect | Audit trail e correlation/causation end-to-end |
| AP-018 | Incident Detection and Operational Runbooks | Infrastructure Architect + Release Governor | Detection, escalation, recovery e runbook verificati |

### Wave D — Governed AI Foundation

| Ordine | Package | Owner specialistico | Outcome principale |
|---:|---|---|---|
| AP-019 | AI Architecture Principles and Boundaries | Enterprise Architect | Principi, authorization, human approval e safety |
| AP-020 | AI Data Access and Citation Architecture | Solution Architect | Accesso governato, fonti e citazioni |
| AP-021 | Knowledge Retrieval / RAG Architecture | Solution Architect | Retrieval, indice, provenance e governance |
| AP-022 | Read-only Observatory Assistant | Solution Architect | Assistant read-only senza tool execution |
| AP-023 | AI Evaluation, Audit and Cost Governance | Release Governor + Solution Architect | Evaluation, audit, model/prompt versioning e cost control |

### Wave E — Advanced Intelligence

Questa wave non è autorizzata per implementazione da AMP-001. Potrà essere pianificata soltanto dopo evidenza operativa sufficiente per telemetry, observability, audit, data quality e safety.

Possibili package futuri:

- Incident Investigation Copilot;
- Session Analysis Assistant;
- Predictive Analytics;
- Predictive Maintenance;
- Intelligent Scheduling Recommendations;
- eventuali azioni operative controllate, solo dopo review safety indipendente.

---

## 8. Dependency map

```text
AP-001 Enterprise Metamodel and Repository IA
  |
  +--> AP-002 Data Governance and Canonical Data Contracts
  |       |
  |       +--> AP-003 Analytics/Warehouse Contract Stabilization
  |               |
  |               +--> AP-004 Incremental/Delta Warehouse
  |               +--> AP-005 Consumer Query Layer
  |                       |
  |                       +--> AP-006 Reporting/Dashboard Integration
  |                       +--> AP-020 AI Data Access
  |
  +--> AP-007 Automation Boundary and Safety Model
          |
          +--> AP-008 Device/Sensor/State Contracts
                  |
                  +--> AP-009 Live Telemetry Architecture
                          |
                          +--> AP-010 Live Ingestion and Resilience
                          +--> AP-011 Time-Series/Event Storage
                          +--> AP-012 Operational Health/Dashboard
                          +--> AP-013 Alerting
                          +--> AP-014 AllSky
                          +--> AP-015 Observability
                                  |
                                  +--> AP-016 Infrastructure Monitoring
                                  +--> AP-017 Audit/Correlation
                                          |
                                          +--> AP-018 Incident Operations
                                          +--> AP-019 AI Boundaries
                                                  |
                                                  +--> AP-020 AI Data Access
                                                          |
                                                          +--> AP-021 RAG
                                                                  |
                                                                  +--> AP-022 Read-only Assistant
                                                                          |
                                                                          +--> AP-023 AI Governance
```

AP-001 e AP-007 sono entrambi prerequisiti di programma, ma AP-007 deve usare gli identificatori, ownership ed evidence rules definiti da AP-001.

---

## 9. Release roadmap

### Increment 1 — Governed Baseline

Scope: AP-001 e AP-002.

Exit outcome:

- repository information architecture definita;
- taxonomy e ownership approvate;
- evidence chain standardizzata;
- policy dati e contratti canonici definiti;
- nessuna modifica runtime richiesta.

### Increment 2 — Warehouse Consolidation

Scope: AP-003…AP-006.

Exit outcome:

- contratti Analytics/Warehouse stabilizzati;
- incremental e delta processing implementati;
- consumer access layer disponibile;
- Reporting e Dashboard integrati senza bypass.

### Increment 3 — Safe Live Foundation

Scope: AP-007…AP-011.

Exit outcome:

- safety boundary formalizzato e revisionato;
- contratti device/sensor/state approvati;
- telemetry e ingestion definite;
- decisione su time-series/event storage registrata;
- nessuna dipendenza della chiusura fail-safe da cloud o applicazione.

### Increment 4 — Operational Platform

Scope: AP-012…AP-018.

Exit outcome:

- health, dashboard live, alerting e observability integrati;
- network/VPN monitoring e runbook disponibili;
- evidenze runtime raccolte;
- re-review delle capability promosse.

### Increment 5 — Governed AI Foundation

Scope: AP-019…AP-023.

Exit outcome:

- boundary AI approvati;
- accesso dati e citazioni governati;
- RAG verificabile;
- assistant read-only valutato e auditabile;
- nessuna esecuzione diretta sugli apparati.

---

## 10. Quality gates comuni

Ogni Architecture Package deve soddisfare i gate applicabili:

| Gate | Evidenza minima |
|---|---|
| Scope e baseline | Branch, commit e artefatti identificati |
| Ownership | Sponsor, architect, reviewer e maintainer definiti |
| Traceability | Collegamenti a capability, gap, ADR, requisiti e release |
| Architecture consistency | Conformità al canonical data flow e ai boundary |
| Safety | Nessun indebolimento degli interblocchi locali |
| Security | Threats, authorization, secrets e data exposure valutati |
| Data | Schema, lineage, versioning e compatibility documentati |
| Testing | Comandi, esiti, data e scope registrati |
| Documentation | Navigazione, cross-reference e metadata aggiornati |
| Migration | Strategia incrementale e rollback quando applicabile |
| Operations | Health, alerting e runbook quando applicabili |
| Independent review | Decisione ARB o review specialistica indipendente |
| Release evidence | Commit, validation matrix e stato finale registrati |

`Implemented`, `Deployed` e `Operationally Verified` sono stati distinti e non intercambiabili.

---

## 11. Criteri di avanzamento capability

Una capability può avanzare soltanto quando dispone delle evidenze richieste:

| Transizione | Evidenza richiesta |
|---|---|
| `Missing` → `Planned` | Scope, owner, dipendenze e backlog approvati |
| `Planned` → `Prepared` | Contratti, interfacce o struttura concreta |
| `Prepared` → `Partial` | Implementazione sostanziale ma incompleta |
| `Partial` → `Implemented` | SRC e almeno TST o INT ripetibile |
| `Implemented` → `Deployed` | Evidenza di deployment e configurazione target |
| `Deployed` → `Operationally Verified` | OPS: health, freshness, reliability, runbook e osservazione runtime |

Le capability safety-critical richiedono inoltre evidenza hardware/software, fault testing e review indipendente.

---

## 12. Risk register di programma

| ID | Rischio | Severità | Trattamento |
|---|---|---:|---|
| AMP-R01 | Ricostruzione di capability già esistenti | Alta | Inventory gate e AP-001 |
| AMP-R02 | Pipeline consumer parallele | Alta | AP-002, AP-005 e architecture compliance |
| AMP-R03 | Stato live dichiarato senza freshness | Alta | AP-009, health model ed evidenza OPS |
| AMP-R04 | Confusione tra monitoring e safety | Critica | AP-007 e independent safety review |
| AMP-R05 | Controllo remoto che indebolisce il fail-safe | Critica | Local interlocks indipendenti e re-review obbligatoria |
| AMP-R06 | Contract drift | Alta | Versioning e compatibility policy |
| AMP-R07 | Roadmap AI anticipata | Alta | Dipendenze hard verso data, observability, audit e safety |
| AMP-R08 | Governance documentata ma non applicata | Alta | AP-001 e quality gate verificabili |
| AMP-R09 | PR non integrate trattate come baseline | Alta | Esclusione esplicita e re-verifica post-merge |
| AMP-R10 | Build e test non eseguiti | Alta | Validation matrix obbligatoria per package implementativi |
| AMP-R11 | Dipendenze numerate ma non rispettate | Media | Program review prima dell'avvio di ogni package |
| AMP-R12 | Debito documentale e cross-reference incoerenti | Media | Documentation Governor e build strict |

---

## 13. Technical debt disposition

| Debito | Disposizione |
|---|---|
| PAA-001 contiene data flow storico | Conservare come snapshot Draft; marcare chiaramente la parte superseded |
| Governance distribuita | Consolidare in AP-001 senza duplicare documenti autorevoli |
| Wildcard negli evidence locator | Sostituire con locator puntuali nei package interessati |
| Test/build non osservati | Non convertire in evidenza positiva; eseguire nei package implementativi |
| Consumer access layer assente | Trattare con AP-005 |
| Incremental/delta Warehouse assenti | Trattare con AP-004 |
| Telemetry, AllSky e AI solo future flags | Restano `Planned` fino a implementazione verificata |
| Observability distribuita | Consolidare con AP-015 |
| Network/VPN failover non verificato | Trattare con AP-016 e prove operative |

---

## 14. Decision backlog

| ID | Decisione richiesta | Package |
|---|---|---|
| DEC-001 | Metamodel, taxonomy e identifier scheme | AP-001 |
| DEC-002 | Repository information architecture e authoritative indexes | AP-001 |
| DEC-003 | Data ownership, retention, archival e immutability | AP-002 |
| DEC-004 | Contract versioning e compatibility policy | AP-002 |
| DEC-005 | Automation/safety/control boundary | AP-007 |
| DEC-006 | Canonical telemetry envelope e freshness semantics | AP-009 |
| DEC-007 | Time-series ed event storage | AP-011 |
| DEC-008 | SLI/SLO e alert severity model | AP-015/AP-013 |
| DEC-009 | AI authorization e human-approval boundary | AP-019 |
| DEC-010 | RAG source governance e citation contract | AP-021 |

Le decisioni irreversibili o con impatto safety devono essere formalizzate tramite ADR e review indipendente.

---

## 15. Maturity KPIs

| KPI | Definizione |
|---|---|
| Capability evidence coverage | Percentuale capability con locator immutabili e validation status |
| Architecture package traceability | Percentuale package collegati a gap, capability, ADR, review e release |
| Contract compliance | Percentuale producer/consumer conformi ai contratti canonici |
| Validation reproducibility | Percentuale test con comando, commit, data ed esito registrati |
| Documentation build health | Esito `mkdocs build --strict` e link/cross-reference checks |
| Operational evidence coverage | Percentuale capability deployed con OPS corrente |
| Safety independence compliance | Numero deviazioni dalla separazione local interlock/application |
| Open architecture risk aging | Età media dei rischi High/Critical non trattati |
| Rework due to duplication | Package o componenti eliminati perché duplicati |
| Review lead time | Tempo tra package ready e decisione indipendente |

I target numerici saranno definiti dopo AP-001, quando ownership e measurement model saranno approvati.

---

## 16. AP-001 specialist handoff brief

### 16.1 Obiettivo

Definire il metamodel enterprise e l'information architecture del repository che colleghino capability, gap, Architecture Package, ADR, evidenza, review, release, documentazione e ownership.

### 16.2 Owner specialistico

- Lead: Digital StarGate Enterprise Architect.
- Co-owner: Documentation Governor.
- Reviewer: Architecture Review Board indipendente.
- Program coordination: Program Architect.

### 16.3 Input obbligatori

- EA-001;
- EA-002;
- PAA-002 v1.1;
- ARB-002;
- ABC-001 ed Evidence Annex;
- ADR e capability documentate;
- `docs/architecture/index.md`;
- `mkdocs.yml`;
- roadmap e release notes presenti nel repository.

### 16.4 Output richiesti

1. Enterprise metamodel con entità e relazioni.
2. Capability taxonomy e identifier policy.
3. Ownership/RACI per artefatti architetturali.
4. Repository information architecture target.
5. Authoritative index e navigation model.
6. Evidence and maturity model riutilizzabile.
7. Traceability matrix package-to-ADR-to-evidence-to-release.
8. Migration plan documentale senza duplicazioni.
9. Quality-gate checklist.
10. Specialist completion report per ARB.

### 16.5 Acceptance criteria

- ogni entità ha identificatore, owner, lifecycle e authoritative location;
- nessun nuovo documento duplica una fonte esistente senza disposition esplicita;
- CAP-01…CAP-33 sono mappabili nel metamodel;
- il modello supporta DOC, CFG, SRC, TST, INT, OPS e GOV;
- la navigazione MkDocs riflette l'information architecture approvata;
- sono definiti criteri per `Implemented`, `Deployed` e `Operationally Verified`;
- local safety interlocks sono rappresentati come authority indipendente;
- il package include validation matrix e `mkdocs build --strict` quando eseguibile;
- l'ARB emette decisione indipendente prima della chiusura.

### 16.6 Esclusioni

AP-001 non deve:

- implementare telemetry o automation;
- selezionare time-series technology;
- modificare runtime o hardware;
- promuovere stati capability;
- introdurre AI execution;
- approvare se stesso.

---

## 17. Program governance cadence

Per ogni Architecture Package:

1. il Program Architect verifica dipendenze e baseline;
2. lo specialist architect produce il package;
3. Documentation, Release e Quality Governors verificano gli aspetti di competenza;
4. l'ARB svolge review indipendente;
5. eventuali finding vengono risolti e tracciati;
6. il Release and Quality Governor registra gate, evidenze e decisione;
7. il Program Architect aggiorna il piano solo sulla base di risultati verificati.

Una re-review mirata è obbligatoria quando cambiano capability state, canonical data flow, safety boundary, remote control, AI tool execution o dipendenze operative critiche.

---

## 18. Exit criteria di AMP-001

AMP-001 può essere considerato approvato soltanto quando:

- è sottoposto a review ARB indipendente;
- la sequenza dei package è confermata o corretta;
- AP-001 dispone di sponsor e owner;
- i rischi High/Critical hanno owner e trattamento;
- le classificazioni PAA-002 restano inalterate salvo nuova evidenza;
- i riferimenti a ABC-001 e alle condizioni ARB sono verificati;
- la navigazione MkDocs include il documento;
- le validazioni eseguite e non eseguite sono registrate.

---

## 19. Validazioni eseguite per la redazione

- verifica del repository e del branch `main`;
- ispezione di PAA-002 v1.1;
- ispezione di ARB-002;
- ispezione di ABC-001;
- verifica della capability matrix, dei gap, delle dipendenze e dei rischi;
- verifica del canonical data flow;
- verifica della navigazione corrente in `mkdocs.yml`;
- verifica che AMP-001 non fosse già presente nella ricerca repository eseguita prima della creazione.

## 20. Validazioni non eseguite

- `mkdocs build --strict`;
- test Analytics/Warehouse;
- build o test .NET;
- lint e formatting automatizzati;
- GitHub Actions CI;
- runtime ingestion, heartbeat e freshness;
- health, metrics, tracing e alerting end-to-end;
- test rete, VPN e failover;
- test hardware, interlock e fault injection;
- deployment, rollback o recovery operativo.

Le validazioni non eseguite non sono trattate come evidenza positiva.

---

## 21. Decisione proposta

**AMP-001 è proposto per INDEPENDENT ARB REVIEW.**

Il primo Architecture Package raccomandato è:

**AP-001 — Enterprise Metamodel and Repository Information Architecture.**

Il package deve essere eseguito dall'Enterprise Architect con il Documentation Governor e sottoposto all'Architecture Review Board. Nessun package successivo che dipenda da taxonomy, ownership o evidence chain dovrebbe essere dichiarato completato prima dell'approvazione di AP-001.
