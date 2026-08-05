# PAA-002 — Platform Capability Gap Assessment

| Campo | Valore |
|---|---|
| Documento | Platform Capability Gap Assessment |
| Identificativo | PAA-002 |
| Progetto | Digital StarGate |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch di riferimento | `main` |
| Commit baseline | `c07a0863bc05851654a422297a23444dd6576c48` |
| Versione | 1.1 |
| Stato | Revised — ready for independent ARB review |
| Responsabile | Massimo Mainini |
| Data assessment originario | 30/07/2026 |
| Data revisione | 30/07/2026 |
| Documenti correlati | PAA-001, EA-001, EA-002, ADR-003 |

---

## 1. Scopo

Questo assessment verifica la copertura effettivamente dimostrabile delle capability della piattaforma Digital StarGate prima della produzione dell'Architecture Master Plan.

La revisione 1.1:

- corregge le classificazioni non sostenute da evidenza sufficiente;
- introduce un modello esplicito di evidenza;
- completa la matrice con Observatory Automation e Architecture Governance;
- distingue documentazione, configurazione, codice, integrazione e operatività;
- chiarisce la disposizione del flusso dati obsoleto contenuto in PAA-001;
- prepara un baseline package verificabile per una review ARB indipendente.

Il documento non autorizza nuovi Architecture Package, non certifica l'operatività runtime e non sostituisce il futuro Architecture Master Plan.

---

## 2. Baseline e metodo di verifica

### 2.1 Baseline autorevole

La baseline verificata è il branch `main` al commit:

```text
c07a0863bc05851654a422297a23444dd6576c48
```

Il commit è registrato per rendere ripetibile la review. Le modifiche successive richiedono una nuova verifica delle evidenze interessate.

### 2.2 Tipi di evidenza

| Codice | Tipo | Valore probatorio |
|---|---|---|
| DOC | Documentazione | Descrive intenzione, regole o procedure; non prova da sola l'esecuzione |
| CFG | Configurazione | Prova che una capability è configurata o prevista |
| SRC | Codice sorgente | Prova l'esistenza di implementazione sostanziale |
| TST | Test | Prova comportamento entro lo scope eseguito e registrato |
| INT | Integrazione | Prova collegamento tra producer, contract e consumer |
| OPS | Evidenza operativa | Prova esecuzione, freshness, health o risultati runtime |
| GOV | Evidenza di governance | Prova ownership, decisioni, lifecycle e quality gate |

### 2.3 Regole di classificazione

| Stato | Criterio minimo |
|---|---|
| Implemented | Evidenza SRC e almeno TST o INT; OPS richiesta quando si dichiara operatività reale |
| Partial | Implementazione o documentazione significativa, ma integrazione, validazione o operatività incomplete |
| Prepared | Contratti, interfacce o struttura concreta predisposti, senza capability completa |
| Planned | Presenza solo in roadmap, documentazione futura o configurazione disabilitata |
| Missing | Nessuna evidenza sufficiente nella baseline |

Una directory, una pagina generata o un flag di configurazione non dimostrano da soli una capability live end-to-end.

### 2.4 Artefatti principali esaminati

```text
docs/architecture/index.md
docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md
docs/architecture/assessments/EA-001-Environment-Repository-Assessment.md
docs/architecture/assessments/EA-002-Integrated-Repository-and-Warehouse-Assessment.md
docs/analytics/index.md
docs/analytics/dashboard-integrated.md
docs/status/index.md
docs/chapters/20-*.md
docs/chapters/26-monitoraggio-meteo-sicurezza-ambientale.md
docs/chapters/27-sistema-allsky.md
docs/chapters/29-reportistica-operativa-kpi.md
docs/chapters/33-roadmap-evolutiva.md
docs/chapters/34-*.md
docs/chapters/38-*.md
docs/chapters/42-*.md
dsg-analytics/config/platform.yml
dsg-analytics/dashboard/build_dashboard_v31.py
src/DigitalStarGate.Contracts/Ai/AiContracts.cs
mkdocs.yml
```

L'elenco identifica il nucleo della verifica, non sostituisce l'inventario completo del repository.

---

## 3. Risultato esecutivo

La baseline contiene fondazioni concrete per Analytics, Warehouse, dashboard storica, portale documentale e contratti AI iniziali. Queste capability non devono essere riproposte come iniziative greenfield.

La baseline non dimostra invece una piattaforma live integrata. In particolare:

- `future.telemetry: false` classifica la telemetria come futura e disabilitata;
- una pagina Observatory Status non prova ingestion live, heartbeat o freshness;
- la configurazione AllSky è futura e disabilitata;
- observability applicativa, SLI/SLO e tracing non risultano formalizzati end-to-end;
- le funzioni di automazione dell'osservatorio sono ampiamente documentate, ma non risultano certificate come capability software integrata nella baseline esaminata;
- la governance architetturale è distribuita tra ADR, assessment, roadmap e capitoli, ma non è dimostrato un operating model unitario e applicato end-to-end.

Le priorità reali sono quindi consolidamento dei contratti dati, integrazione dei consumer, telemetria live, observability, automazione governata e introduzione controllata dell'AI.

---

## 4. Matrice completa di copertura

| ID | Capability | Stato | Evidenza | Limite dell'evidenza | Azione futura |
|---|---|---|---|---|---|
| CAP-01 | Analytics pipeline | Implemented | SRC/TST: area `dsg-analytics`, normalizzazione, validazioni e test documentati | Operatività continua non certificata in questo assessment | Stabilizzare contratti e versionamento |
| CAP-02 | Historical Analytics Dashboard | Implemented | SRC/DOC: builder dedicato e dashboard integrata | Freshness e deployment runtime non certificati | Evoluzione controllata, non ricostruzione |
| CAP-03 | Data Warehouse | Implemented | SRC/DOC: dataset Parquet per sessioni, target, equipment, quality e weather | Consumer access layer incompleto | Consolidare query e contratti |
| CAP-04 | Warehouse metadata and validation | Implemented | SRC/TST/DOC: schema, lineage, row count e controlli | Evidenza di release certification assente | Certificare release e compatibilità |
| CAP-05 | Reporting | Partial | DOC/SRC: materiali e output esistenti | Integrazione canonica con Warehouse non completata | Integrare senza pipeline parallele |
| CAP-06 | Observatory Status page | Partial | SRC/DOC/CFG: pagina, generatori e percorso `docs/status` | Nessuna prova sufficiente di live ingestion e freshness | Collegare sorgenti reali e health |
| CAP-07 | Weather monitoring | Partial | DOC/CFG: modello e indicatori; modulo weather abilitato | Ingestion operativa e uso safety non certificati | Validare source, timestamp e safety status |
| CAP-08 | Live telemetry | Planned | CFG: `future.telemetry: false`; path live configurato | Path e flag futuro non costituiscono implementazione o contratto | Definire architettura e contratti canonici |
| CAP-09 | Event streaming | Missing | Nessun meccanismo end-to-end dimostrato | Nessuna evidenza INT/OPS | Valutare mediante ADR |
| CAP-10 | Time-series storage | Missing | Warehouse storico presente | Nessuno store live formalizzato | Selezionare tecnologia, retention e integrazione |
| CAP-11 | Alerting and notifications | Partial | DOC: concetti e procedure operative | Servizio, severità, routing e test non dimostrati | Definire servizio e matrice di escalation |
| CAP-12 | Application observability | Partial | DOC/SRC: logging e diagnostica presenti in forma distribuita | Tracing, SLI/SLO, metriche e correlation end-to-end non formalizzati | Definire observability architecture |
| CAP-13 | Infrastructure monitoring | Partial | DOC: procedure e indicatori infrastrutturali | Automazione health e disponibilità non certificata | Automatizzare health e availability |
| CAP-14 | Network and VPN monitoring | Partial | DOC: topologia, failover e controlli | Telemetria, alert e prove di failover non integrate | Integrare misure e allarmi |
| CAP-15 | AllSky integration | Planned | CFG/DOC: `future.allsky: false` e capitolo dedicato | Nessuna ingestion o health integrata dimostrata | Definire immagini, metadati e health |
| CAP-16 | Observatory Automation | Partial | DOC: procedure, apparati, sequenze e vincoli fail-safe descritti | Nessuna prova unica di orchestrazione integrata, contratti canonici e validation end-to-end | Separare safety locale, orchestration e supervisory control |
| CAP-17 | Local safety interlocks | Partial | DOC: requisiti fail-safe e indipendenza locale | Certificazione hardware/software e test di fault non inclusi | Definire evidenze e test di sicurezza |
| CAP-18 | AI boundary contracts | Prepared | SRC: `AiRequestContext` e `AiResultReference` | Contratti insufficienti per governance completa | Completare autorizzazioni, audit e versioning |
| CAP-19 | AI Assistant | Planned | CFG: `future.ai_assistant: false` | Nessuna capability runtime | Prima release read-only |
| CAP-20 | AI Operations Copilot | Missing | Nessuna implementazione sufficiente | Dipende da telemetry, observability e audit | Posticipare fino a readiness dimostrata |
| CAP-21 | RAG / knowledge retrieval | Missing | Nessun sottosistema governato rilevato | Fonti, indice e citazioni assenti | Definire architecture e source governance |
| CAP-22 | AI tool execution | Missing | Nessuna capacità approvata | Mancano policy e human approval | Introdurre solo dopo safety review |
| CAP-23 | Predictive analytics | Missing | Nessun modello operativo certificato | Dati e evaluation non dimostrati | Attendere dataset affidabili |
| CAP-24 | Predictive maintenance | Missing | Solo prospettiva futura | Dipende da telemetria storica affidabile | Definire readiness criteria |
| CAP-25 | Intelligent scheduling | Missing | Nessun motore governato rilevato | Nessuna separazione formalizzata tra consiglio e controllo | Progettare come recommendation-only |
| CAP-26 | Data governance | Partial | DOC: principi, schema e lineage | Retention, archival, immutabilità e privacy incomplete | Formalizzare policy e ADR |
| CAP-27 | Incremental Warehouse build | Missing | Indicato come non implementato | Nessuna evidenza SRC/TST | Inserire nel consolidation backlog |
| CAP-28 | Delta update | Missing | Indicato come non implementato | Nessuna evidenza SRC/TST | Inserire nel consolidation backlog |
| CAP-29 | DuckDB/query access layer | Missing | Nessun layer canonico rilevato | Consumer contract assente | Creare query access layer |
| CAP-30 | Dashboard SQL consumption | Missing | Dashboard non dimostrata come consumer SQL canonico | Migrazione non avviata | Migrare gradualmente i consumer |
| CAP-31 | Architecture Governance | Partial | GOV/DOC: ADR, assessment, roadmap, release e capitoli di governance | Autorità, lifecycle ed evidenze sono distribuiti; applicazione end-to-end non certificata | Consolidare operating model, traceability e review gates |
| CAP-32 | Documentation governance | Partial | DOC/CFG: MkDocs, navigazione e convenzioni | Metadati e cross-reference non uniformi | Standardizzare e automatizzare controlli |
| CAP-33 | Release quality governance | Partial | GOV/DOC: processi e note di release presenti | Evidenza uniforme dei gate non dimostrata | Collegare release, validation e approval |

---

## 5. Registro delle evidenze principali

| Evidence ID | Artefatto | Tipo | Capability supportate | Osservazione |
|---|---|---|---|---|
| EV-001 | `dsg-analytics/config/platform.yml` | CFG | CAP-06, CAP-07, CAP-08, CAP-15, CAP-19 | Telemetry, AllSky e AI Assistant risultano future e disabilitate |
| EV-002 | `dsg-analytics/dashboard/build_dashboard_v31.py` | SRC | CAP-02 | Prova implementazione del builder, non operatività continua |
| EV-003 | `docs/analytics/dashboard-integrated.md` | DOC | CAP-02 | Descrive dashboard storica integrata |
| EV-004 | `docs/status/index.md` | DOC/SRC | CAP-06 | Prova pagina di stato, non live chain end-to-end |
| EV-005 | `EA-002-Integrated-Repository-and-Warehouse-Assessment.md` | DOC/GOV | CAP-01–CAP-05 | Supporta il flusso Analytics → Warehouse → consumer |
| EV-006 | `PAA-001-Project-Architecture-Assessment.md` | DOC/GOV | Baseline storica | Contiene flusso Reporting → Warehouse → Analytics, non più autorevole per il data flow corrente |
| EV-007 | `src/DigitalStarGate.Contracts/Ai/AiContracts.cs` | SRC | CAP-18 | Prova contratti iniziali, non AI capability completa |
| EV-008 | capitoli operativi e infrastrutturali | DOC | CAP-07, CAP-11–CAP-17 | Evidenza progettuale e procedurale, non certificazione runtime |
| EV-009 | ADR, roadmap e documentazione release | GOV/DOC | CAP-31–CAP-33 | Governance presente ma distribuita |
| EV-010 | `mkdocs.yml` | CFG | CAP-32 | Prova struttura di pubblicazione e navigazione |

### 5.1 Evidenza non disponibile

Questo assessment non include:

- log runtime acquisiti durante la review;
- misure di freshness o heartbeat;
- esiti di fault injection sugli interblocchi;
- prove di failover rete/VPN;
- report CI aggiornati al commit baseline;
- certificazioni di safety o security indipendenti.

Le capability dipendenti da tali prove non possono essere classificate come pienamente operative.

---

## 6. Architettura dati autorevole

Il flusso corrente da preservare è:

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

Dashboard, Reporting e AI non devono accedere direttamente ai log grezzi né introdurre pipeline parallele non governate.

### 6.1 Disposizione di PAA-001

PAA-001 resta uno snapshot storico in stato Draft. Il suo flusso:

```text
Automation / Collection → Reporting → Warehouse → Analytics
```

è dichiarato **superseded esclusivamente per la rappresentazione del data flow** da EA-002, ADR-003 e PAA-002 v1.1.

Questa disposizione:

- non approva retroattivamente PAA-001;
- non rende obsolete le altre osservazioni ancora valide;
- impedisce che il vecchio flusso sia usato come architettura target;
- deve essere recepita in una futura manutenzione documentale di PAA-001 o nell'indice degli assessment.

---

## 7. Gap critici

### GAP-01 — Canonical Live Telemetry Model

Manca un modello canonico governato per stato, misure ed eventi di tetto/cupola, interblocchi, montatura, camera, focuser, alimentazione, meteo, rete, VPN, EAGLE, AllSky e sessione osservativa.

### GAP-02 — Live Ingestion and Freshness

Manca una catena certificata con source timestamp, ingestion timestamp, heartbeat, freshness, online/offline, degraded mode, retry, buffering e gestione dei dati mancanti.

### GAP-03 — Time-Series and Event Access

Il Warehouse storico non sostituisce uno store per telemetria ad alta frequenza. Persistenza live, retention, aggregazioni, query ed eventi richiedono una decisione architetturale.

### GAP-04 — Observability

Logging, metriche, tracing, correlation/causation ID, health check, audit, SLI/SLO e alert routing non formano ancora una capability end-to-end governata.

### GAP-05 — Observatory Automation Boundary

Devono essere formalmente separati:

- interblocchi e safety locale;
- device control;
- orchestration applicativa;
- supervisory monitoring;
- operazioni manuali e override;
- recovery e degraded modes.

### GAP-06 — Warehouse Consumer Layer

Mancano accesso SQL/DuckDB, query stabili e contratti canonici per Dashboard, Reporting e AI.

### GAP-07 — AI Governance and Safety

I contratti iniziali non coprono autorizzazioni, audit, fonti, citazioni, evaluation, prompt/model versioning, data leakage, fallback, human approval e separazione tra consiglio e comando.

### GAP-08 — Data Governance

Retention, archival, immutabilità, backup, checksum, privacy e versionamento dei dataset non sono completamente formalizzati.

### GAP-09 — Architecture Governance Evidence

Manca una vista unitaria e verificabile che colleghi authority, work item, Architecture Package, ADR, implementation evidence, review, approval, release e stato documentale.

---

## 8. Vincoli di sicurezza

1. Gli interblocchi fisici e locali restano indipendenti dal software applicativo.
2. La chiusura di sicurezza non dipende da cloud, portale, dashboard o AI.
3. La perdita di rete non impedisce le azioni locali fail-safe.
4. Monitoring e safety non sono sinonimi.
5. L'AI non comanda direttamente apparati nella prima fase.
6. Ogni futura azione automatizzata ad alto impatto deve essere autorizzata, tracciata e reversibile dove tecnicamente possibile.
7. Stato sconosciuto, dato stale o health degradato non possono essere interpretati come stato sicuro.
8. Manual override, recovery e audit devono essere espliciti per ogni capability di automazione.

---

## 9. Backlog dipendente dalle evidenze

### Wave A — Architecture and Data Consolidation

1. Enterprise Metamodel and Repository Information Architecture.
2. Architecture Index and authoritative current-state model.
3. Data Governance decision and policy.
4. Analytics and Warehouse contract stabilization.
5. Warehouse incremental and delta processing.
6. Warehouse query and consumer access layer.
7. Reporting integration.

### Wave B — Safe Observatory Automation and Live Platform

1. Observatory Automation boundary and safety model.
2. Canonical device, sensor and state contracts.
3. Live Telemetry Architecture.
4. Live Ingestion and Connectivity Resilience.
5. Time-Series and Event Storage decision.
6. Operational Health Model.
7. Live Dashboard evolution.
8. Alerting and Notification Architecture.
9. AllSky integration.

### Wave C — Observability and Operations

1. Application Observability.
2. Infrastructure and EAGLE Monitoring.
3. Network, VPN and Failover Monitoring.
4. Audit and Correlation Model.
5. Incident Detection and operational runbooks.

### Wave D — Governed AI Foundation

1. AI Architecture Principles.
2. AI Security, Safety and Human-Approval Boundaries.
3. AI Data Access and Citation Architecture.
4. Knowledge Retrieval / RAG Architecture.
5. Read-only Observatory Assistant.
6. AI Evaluation, Audit and Cost Governance.

### Wave E — Advanced Intelligence

1. Incident Investigation Copilot.
2. Session Analysis Assistant.
3. Predictive Analytics.
4. Predictive Maintenance.
5. Intelligent Scheduling Recommendations.
6. Controlled operational actions only after independent safety review.

---

## 10. Dipendenze principali

```text
Repository and Architecture Governance
        |
        v
Enterprise Metamodel and Capability Taxonomy
        |
        +--> Data Governance
        |       |
        |       +--> Analytics/Warehouse Contracts
        |               |
        |               +--> Consumer Query Layer
        |                       +--> Reporting
        |                       +--> Historical Dashboard
        |                       +--> Read-only AI
        |
        +--> Observatory Automation Boundary
                |
                +--> Canonical Device and Sensor Contracts
                        |
                        +--> Live Telemetry and Ingestion
                                |
                                +--> Time-Series/Event Access
                                +--> Live Dashboard
                                +--> Alerting
                                +--> Observability
                                +--> AI Operations Readiness
```

L'AI avanzata non deve precedere contratti stabili, qualità e lineage, observability, audit, autorizzazioni, safety review e dataset sufficienti.

---

## 11. Rischi

| ID | Rischio | Severità | Trattamento |
|---|---|---:|---|
| R-01 | Duplicazione di Analytics o Dashboard esistenti | Alta | Usare inventario e current-state come gate |
| R-02 | Uso improprio del termine live | Alta | Definire heartbeat, freshness e livelli di aggiornamento |
| R-03 | AI collegata direttamente agli apparati | Critica | Read-only first e human approval |
| R-04 | Pipeline parallele che bypassano Analytics/Warehouse | Alta | Contratti e architecture compliance |
| R-05 | Data contract drift | Alta | Versionamento e compatibility policy |
| R-06 | Dashboard basata su dati stale | Alta | Timestamp, freshness e source health |
| R-07 | Confusione tra safety e monitoring | Critica | Interblocchi locali indipendenti |
| R-08 | Predictive analytics su dati insufficienti | Media | Readiness criteria ed evaluation |
| R-09 | Reporting migrato senza inventario | Alta | Consolidamento controllato |
| R-10 | Roadmap numerata prima delle dipendenze | Media | Master Plan dopo ARB |
| R-11 | Documentazione interpretata come prova operativa | Alta | Applicare il modello di evidenza |
| R-12 | Governance dichiarata ma non tracciata end-to-end | Alta | Evidence chain e quality gate verificabili |
| R-13 | Automazione remota che indebolisce il fail-safe locale | Critica | Safety boundary e independent review |

---

## 12. Quality gate per Architecture Master Plan

L'Architecture Master Plan può essere prodotto solo quando:

- PAA-002 v1.1 ha superato una review ARB indipendente;
- la disposizione del data flow PAA-001 è accettata;
- la matrice capability è giudicata completa o le esclusioni sono esplicite;
- ogni classificazione critica è collegata a evidenza ripetibile;
- sono identificate le dipendenze obbligatorie;
- sono esclusi package duplicati;
- la safety locale fail-safe è protetta;
- Observatory Automation e Architecture Governance sono incluse nel modello;
- il primo package successivo è autorizzato dallo Sponsor.

---

## 13. Raccomandazione

Il primo package successivo resta **Enterprise Metamodel and Repository Information Architecture**, con scope sufficiente a definire:

- tassonomia delle capability;
- relazioni tra fonti operative, automation, Analytics, Warehouse, consumer, telemetry, observability e AI;
- identificatori e ownership;
- evidenze richieste per i maturity state;
- collegamenti tra Architecture Package, ADR, review, release e documentazione.

Ordine raccomandato successivo:

1. Data Governance and Canonical Data Contracts;
2. Observatory Automation Boundary and Safety Model;
3. Warehouse Consumer and Query Layer;
4. Live Telemetry Architecture;
5. Operational Dashboard Evolution;
6. Observability Architecture;
7. Read-only AI Observatory Assistant.

La numerazione AP definitiva resta subordinata all'ARB.

---

## 14. Matrice di tracciabilità della revisione

| Finding della review precedente | Correzione v1.1 | Sezione |
|---|---|---|
| Capability matrix incompleta | Aggiunte Observatory Automation, safety interlocks, Architecture Governance, Documentation e Release Governance | 4 |
| Telemetria sovrastimata | Riclassificata da Prepared a Planned sulla base di `future.telemetry: false` | 4, EV-001 |
| Observability troppo assoluta | Riclassificata Partial, distinguendo elementi distribuiti da capability end-to-end | 4, GAP-04 |
| Nessuna current-main lineage proof | Aggiunto commit baseline e registro evidenze | 2, 5 |
| Nessun evidence model | Introdotti tipi, criteri e limiti probatori | 2 |
| Tracciabilità insufficiente | Aggiunti Evidence ID, capability ID e matrice findings-to-fix | 4, 5, 14 |
| PAA-001 non disposto | Dichiarato superseded per il solo data flow, mantenuto come snapshot storico Draft | 6.1 |
| Architecture Governance assente | Aggiunta CAP-31 e GAP-09 | 4, 7 |

---

## 15. Stato di completamento

| Attività | Stato |
|---|---|
| Baseline commit identificato | Completato |
| Modello di evidenza definito | Completato |
| Capability matrix completata | Completato per lo scope dichiarato |
| Telemetria riclassificata | Completato |
| Observability riclassificata | Completato |
| Observatory Automation inclusa | Completato |
| Architecture Governance inclusa | Completato |
| Disposizione PAA-001 definita | Completato nel presente assessment |
| Runtime/CI validation | Non eseguita in questa revisione documentale |
| Revisione indipendente ARB | Richiesta |
| Roadmap AP definitiva | Non autorizzata |

**Esito:** READY FOR INDEPENDENT ARB REVIEW — operational claims remain subject to runtime evidence.