# PAA-002 — Platform Capability Gap Assessment

| Campo | Valore |
|---|---|
| Documento | Platform Capability Gap Assessment |
| Identificativo | PAA-002 |
| Progetto | Digital StarGate |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch di riferimento | `main` |
| Versione | 1.0 |
| Stato | Assessment completato — revisione ARB richiesta |
| Responsabile | Massimo Mainini |
| Data | 30/07/2026 |
| Documenti precedenti | PAA-001, EA-001, EA-002 |

---

## 1. Scopo

Questo assessment verifica la copertura reale del repository prima della produzione del Digital StarGate Architecture Master Plan.

L'obiettivo è distinguere in modo documentato:

- capacità già implementate;
- capacità parzialmente implementate;
- capacità predisposte ma non operative;
- capacità pianificate;
- capacità mancanti;
- duplicazioni da evitare nella futura roadmap.

L'assessment dedica particolare attenzione a:

- dashboard;
- monitoraggio live;
- telemetria;
- Analytics;
- Data Warehouse;
- Reporting;
- observability;
- AllSky;
- AI Assistant;
- AI Operations Copilot;
- predictive analytics e predictive maintenance.

Il documento non autorizza nuovi Architecture Package e non sostituisce il futuro Architecture Master Plan.

---

## 2. Baseline verificata

La baseline di verifica è il branch `main` del repository GitHub autorevole.

Sono stati esaminati almeno i seguenti artefatti:

```text
docs/architecture/index.md
docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md
docs/architecture/assessments/EA-001-Environment-Repository-Assessment.md
docs/architecture/assessments/EA-002-Integrated-Repository-and-Warehouse-Assessment.md
docs/analytics/index.md
docs/analytics/dashboard-integrated.md
docs/status/index.md
docs/chapters/26-monitoraggio-meteo-sicurezza-ambientale.md
docs/chapters/27-sistema-allsky.md
docs/chapters/29-reportistica-operativa-kpi.md
docs/chapters/33-roadmap-evolutiva.md
dsg-analytics/config/platform.yml
dsg-analytics/dashboard/build_dashboard_v31.py
src/DigitalStarGate.Contracts/Ai/AiContracts.cs
mkdocs.yml
```

---

## 3. Risultato esecutivo

Digital StarGate non è soltanto un manuale tecnico. Il repository contiene già elementi concreti di piattaforma dati e portale operativo.

Le seguenti capacità non devono essere riproposte nella roadmap come iniziative greenfield:

- Analytics pipeline;
- dashboard Analytics;
- pagina di stato dell'osservatorio;
- dataset meteo;
- Data Warehouse in formato Parquet;
- schema, metadati e controlli di qualità;
- portale MkDocs/GitHub Pages;
- contratti AI iniziali.

Le priorità reali sono il consolidamento, l'integrazione dei consumatori, l'alimentazione live, la telemetria, l'observability e l'introduzione controllata dell'AI.

---

## 4. Matrice di copertura

### 4.1 Scala di classificazione

| Stato | Significato |
|---|---|
| Implemented | Capacità presente con artefatti operativi o codice sostanziale |
| Partial | Capacità presente ma incompleta, non integrata o non certificata end-to-end |
| Prepared | Struttura o contratto predisposto, senza capacità operativa completa |
| Planned | Esplicitamente prevista nella configurazione o nella documentazione |
| Missing | Nessuna implementazione sufficiente rilevata |

### 4.2 Copertura rilevata

| Capacità | Stato | Evidenza sintetica | Azione futura |
|---|---|---|---|
| Analytics pipeline | Implemented | area `dsg-analytics`, dataset normalizzati, validazioni e test | Stabilizzare contratti e versionamento |
| Historical Analytics Dashboard | Implemented | dashboard integrata e builder dedicato | Evoluzione controllata, non ricostruzione |
| Data Warehouse | Implemented | dataset Parquet sessions, targets, equipment, quality, weather | Consolidare query e consumer layer |
| Warehouse metadata and validation | Implemented | schema, lineage, row count, controlli e test | Certificare release e contratti |
| Reporting | Partial | materiale esistente, integrazione Warehouse non formalmente completata | Integrare senza duplicare pipeline |
| Observatory Status page | Partial | UI e generatori presenti, campi operativi esposti | Collegare sorgenti reali e freshness |
| Weather monitoring | Partial | modello dati e indicatori presenti | Certificare ingestion e safety status |
| Live telemetry | Prepared | percorso dati live presente, modulo disabilitato | Definire architettura e contratti canonici |
| Event streaming | Missing | nessun meccanismo end-to-end certificato | Valutare tramite ADR |
| Time-series storage | Missing | Warehouse storico presente, store live non formalizzato | Selezionare tecnologia e retention |
| Alerting and notifications | Partial | concetti operativi presenti nei capitoli | Definire servizio, severità e routing |
| Application observability | Missing | metriche, tracing e SLI non formalizzati | Creare architettura dedicata |
| Infrastructure monitoring | Partial | procedure manuali e indicatori previsti | Automatizzare health e availability |
| Network and VPN monitoring | Partial | topologia, failover e controlli documentati | Integrare telemetria e allarmi |
| AllSky integration | Planned | modulo configurato come futuro | Definire ingestion, immagini e health |
| AI boundary contracts | Prepared | `AiRequestContext` e `AiResultReference` | Completare governance e interfacce |
| AI Assistant | Planned | modulo centrale disabilitato | Prima release read-only |
| AI Operations Copilot | Missing | nessuna implementazione sufficiente | Dipendente da observability e audit |
| RAG / knowledge retrieval | Missing | non rilevato un sottosistema governato | Definire fonti, indicizzazione e citazioni |
| AI tool execution | Missing | nessuna capacità approvata | Introdurre solo con human approval |
| Predictive analytics | Missing | nessun modello operativo certificato | Attendere qualità e volume dati |
| Predictive maintenance | Missing | manutenzione futura ma non implementata | Dipendente da telemetria storica affidabile |
| Intelligent scheduling | Missing | non rilevato un motore AI governato | Separare raccomandazione da controllo |
| Data governance | Partial | principi presenti, retention e archival incompleti | Formalizzare ADR e policy |
| Incremental Warehouse build | Missing | indicato come non implementato | Inserire nel consolidation backlog |
| Delta update | Missing | indicato come non implementato | Inserire nel consolidation backlog |
| DuckDB/query access layer | Missing | indicato come non implementato | Creare consumer access layer |
| Dashboard SQL consumption | Missing | indicato come non implementato | Migrare gradualmente i consumer |

---

## 5. Architettura dati autorevole

Il flusso da preservare nella futura roadmap è:

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

Dashboard, Reporting e AI non devono accedere direttamente ai log grezzi o introdurre pipeline parallele non governate.

---

## 6. Incoerenze e debito documentale

### 6.1 Divergenza PAA-001 / EA-002

PAA-001 descrive un flusso target nel quale Reporting precede Warehouse e Analytics.

EA-002, supportato dall'implementazione più recente, stabilisce invece che:

- Analytics interpreta e valida le sorgenti;
- Warehouse consuma i dataset Analytics validati;
- Reporting, Dashboard e AI sono consumatori downstream.

La futura formalizzazione architetturale deve risolvere questa divergenza. Fino a tale decisione, il modello EA-002 e ADR-003 è considerato il riferimento tecnico più recente.

### 6.2 Stato dei documenti

PAA-001 è ancora marcato `Draft`, pur contenendo valutazioni e punteggi usati come riferimento.

Occorre stabilire se:

- approvarlo come snapshot storico;
- correggerlo;
- dichiararlo superseded da PAA-002 e dagli assessment successivi.

### 6.3 Nomenclatura live

La presenza di una pagina `Observatory Status` non prova da sola l'esistenza di monitoraggio live end-to-end.

La documentazione deve distinguere chiaramente:

- pagina generata;
- dato aggiornato periodicamente;
- near-real-time;
- real-time streaming;
- stato locale fail-safe.

---

## 7. Gap critici

### GAP-01 — Canonical Live Telemetry Model

Manca un modello canonico governato per stato, misure ed eventi di:

- cupola o tetto;
- interblocchi locali;
- montatura;
- camera;
- focheggiatore;
- alimentazione e UPS;
- meteo;
- rete, VPN e failover;
- EAGLE;
- AllSky;
- sessione osservativa.

### GAP-02 — Live Ingestion and Freshness

Mancano evidenze di una catena certificata con:

- source timestamp;
- ingestion timestamp;
- heartbeat;
- freshness;
- online/offline;
- degraded mode;
- gestione dei dati mancanti;
- retry e buffering.

### GAP-03 — Time-Series and Event Access

Il Warehouse storico non sostituisce necessariamente uno store per telemetria ad alta frequenza.

Deve essere presa una decisione architetturale su:

- persistenza live;
- retention;
- aggregazioni;
- query;
- eventi operativi;
- integrazione con Warehouse.

### GAP-04 — Observability

Non è ancora formalizzata una piattaforma per:

- log strutturati;
- metriche applicative;
- tracing;
- correlation e causation ID;
- health check;
- audit;
- SLI/SLO;
- alert routing.

### GAP-05 — Warehouse Consumer Layer

Mancano accesso SQL/DuckDB, query stabili e contratti per Dashboard, Reporting e AI.

### GAP-06 — AI Governance and Safety

I contratti AI iniziali non coprono ancora:

- autorizzazioni;
- audit delle richieste e risposte;
- fonti e citazioni;
- valutazione dei modelli;
- prompt and model versioning;
- data leakage;
- fallback;
- human approval;
- separazione tra consiglio e comando operativo.

### GAP-07 — Data Governance

Retention, archival, immutabilità, backup, checksum, privacy e versionamento dei dataset non sono completamente formalizzati.

---

## 8. Vincoli di sicurezza

La futura piattaforma deve rispettare i seguenti vincoli:

1. gli interblocchi fisici e locali restano indipendenti dal software applicativo;
2. la chiusura di sicurezza non dipende dal cloud, dal portale o dall'AI;
3. la perdita di rete non deve impedire le azioni locali fail-safe;
4. l'AI non deve comandare direttamente apparati nella prima fase;
5. ogni futura azione AI deve essere autorizzata, tracciata e reversibile dove tecnicamente possibile;
6. la dashboard non deve essere considerata fonte unica della verità per la sicurezza fisica.

---

## 9. Backlog dipendente dalle evidenze

Il backlog seguente non assegna ancora numeri AP definitivi.

### Wave A — Architecture and Data Consolidation

1. Enterprise Metamodel and Repository Information Architecture.
2. Architecture Index and authoritative current-state model.
3. Data Governance decision and policy.
4. Analytics and Warehouse contract stabilization.
5. Warehouse incremental and delta processing.
6. Warehouse query and consumer access layer.
7. Reporting integration.

### Wave B — Live Observatory Platform

1. Live Telemetry Architecture.
2. Device and Sensor Canonical Contracts.
3. Live Ingestion and Connectivity Resilience.
4. Time-Series and Event Storage decision.
5. Operational Health Model.
6. Live Dashboard evolution.
7. Alerting and Notification Architecture.
8. AllSky integration.

### Wave C — Observability and Operations

1. Application Observability.
2. Infrastructure and EAGLE Monitoring.
3. Network, VPN and Failover Monitoring.
4. Audit and Correlation Model.
5. Incident Detection.
6. Operational Runbook integration.

### Wave D — AI Foundation

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
6. Controlled operational actions, only after independent safety review.

---

## 10. Dipendenze principali

```text
Enterprise Metamodel
        |
        +--> Data Governance
        |
        +--> Canonical Contracts
                    |
                    +--> Live Telemetry
                    |       |
                    |       +--> Live Dashboard
                    |       +--> Alerting
                    |       +--> Observability
                    |
                    +--> Warehouse Consumer Layer
                            |
                            +--> Reporting
                            +--> Historical Dashboard
                            +--> Read-only AI Assistant
                                      |
                                      +--> AI Copilot
                                      +--> Predictive Analytics
                                      +--> Predictive Maintenance
```

L'AI avanzata non deve precedere:

- contratti dati stabili;
- qualità e lineage;
- observability;
- audit;
- autorizzazioni;
- dataset storici sufficienti.

---

## 11. Rischi

| ID | Rischio | Severità | Trattamento |
|---|---|---:|---|
| R-01 | Duplicazione di Analytics o Dashboard già esistenti | Alta | Usare inventario e current-state come gate |
| R-02 | Uso improprio del termine live | Alta | Definire livelli di aggiornamento e freshness |
| R-03 | AI collegata direttamente agli apparati | Critica | Read-only first e human approval |
| R-04 | Pipeline parallele che bypassano Analytics/Warehouse | Alta | Contratti e architecture compliance |
| R-05 | Data contract drift | Alta | Versionamento, schema validation e compatibility policy |
| R-06 | Dashboard basata su dati stale senza evidenza | Alta | Timestamp, freshness e source health |
| R-07 | Confusione tra safety e monitoring | Critica | Interblocchi locali indipendenti |
| R-08 | Predictive analytics su dati insufficienti | Media | Readiness criteria e model evaluation |
| R-09 | Reporting migrato senza inventario | Alta | Consolidamento controllato e non distruttivo |
| R-10 | Roadmap numerata prima di validare dipendenze | Media | Master Plan solo dopo revisione PAA-002 |

---

## 12. Quality gates per il futuro Master Plan

La roadmap definitiva può essere prodotta solo quando:

- PAA-002 è stato sottoposto a revisione indipendente ARB;
- è stata risolta la divergenza PAA-001 / EA-002;
- ogni capacità è classificata come Implemented, Partial, Prepared, Planned o Missing;
- sono state identificate le dipendenze obbligatorie;
- sono stati esclusi package duplicati;
- è stata definita la relazione tra il repository Architecture Office e il repository prodotto;
- la sicurezza locale fail-safe è esplicitamente protetta;
- il primo package successivo è autorizzato dallo Sponsor.

---

## 13. Raccomandazione del Program Architect

Il prossimo package resta:

**Enterprise Metamodel and Repository Information Architecture**.

Il suo scope deve essere ampliato affinché definisca anche la tassonomia delle capacità di piattaforma e le relazioni tra:

- fonti operative;
- Analytics;
- Warehouse;
- dashboard;
- Reporting;
- telemetria;
- observability;
- AI;
- documentazione;
- ADR;
- Architecture Package.

Subito dopo devono essere avviati, nell'ordine:

1. Data Governance and Canonical Data Contracts;
2. Warehouse Consumer and Query Layer;
3. Live Telemetry Architecture;
4. Operational Dashboard Evolution;
5. Observability Architecture;
6. Read-only AI Observatory Assistant.

La roadmap con numerazione AP definitiva deve essere prodotta soltanto dopo la revisione indipendente di questo assessment.

---

## 14. Stato di completamento

| Attività | Stato |
|---|---|
| Repository verificato | Completato |
| Dashboard e Analytics mappati | Completato |
| Warehouse mappato | Completato |
| Live monitoring verificato | Completato con gap rilevati |
| AI foundation verificata | Completato con capacità solo predisposte |
| Gap classificati | Completato |
| Backlog dipendente dalle evidenze | Completato |
| Roadmap AP definitiva | Non ancora autorizzata |
| Revisione indipendente ARB | Richiesta |

**Esito:** PASS WITH REQUIRED ARCHITECTURE CONSOLIDATION AND ARB REVIEW.
