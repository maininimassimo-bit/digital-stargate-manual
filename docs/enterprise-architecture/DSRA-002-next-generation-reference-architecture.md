# DSRA-002 - Digital StarGate Next Generation Reference Architecture

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Next Generation Reference Architecture |
| Identificativo | DSRA-002 |
| Stato | Proposed |
| Versione | 0.1 |
| Baseline | Release 1.1 - Enterprise Software Architecture |
| Owner | Massimo Mainini |
| Data | 2026-07-28 |
| Ambito | Architettura target della piattaforma Digital StarGate |

## 1. Scopo

DSRA-002 definisce l'architettura target di Digital StarGate per la Release 1.1 e per le successive fasi di implementazione software.

Il documento estende la baseline enterprise esistente senza modificare l'autorità operativa dell'EAGLE e dei software astronomici. Digital StarGate opera come piattaforma superiore di osservabilità, raccolta dati, analisi, catalogazione, orchestrazione dei workflow scientifici e supporto decisionale.

## 2. Riferimenti

- [DSG-MR-001 - Digital StarGate Master Roadmap](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [DSRA-000 - Vision Target Architecture](DSRA-000-vision-target-architecture.md)
- [DSRA-001 - Reference Architecture](DSRA-001-reference-architecture.md)
- [DSG-EAM-001 - Enterprise Architecture Meta Model](DSG-EAM-001-enterprise-architecture-meta-model.md)
- [Enterprise Program Portfolio](../enterprise/program-portfolio.md)
- [Roadmap Release 1.1 Change Set](../enterprise-roadmap/DSG-MR-001-release-1-1-change-set.md)
- [ADR-005 - EAGLE Operational Authority](../enterprise/adr/ADR-005-eagle-operational-authority.md)
- [ADR-006 - Scientific Session Aggregate](../enterprise/adr/ADR-006-scientific-session-aggregate.md)
- [ADR-007 - Event-Driven Immutable Telemetry](../enterprise/adr/ADR-007-event-driven-immutable-telemetry.md)
- [ADR-008 - Logical Scientific Repository](../enterprise/adr/ADR-008-logical-scientific-repository.md)
- [ADR-009 - AI Advisory Boundary](../enterprise/adr/ADR-009-ai-advisory-boundary.md)

## 3. Executive Summary

Digital StarGate evolve da piattaforma documentale e di monitoraggio a piattaforma enterprise per il ciclo di vita completo dell'osservazione astronomica.

La piattaforma non sostituisce NINA, PHD2, CPWI, ASCOM o i servizi dell'EAGLE. Questi componenti mantengono il controllo diretto dell'osservatorio e degli strumenti. Digital StarGate raccoglie e normalizza telemetria e log, ricostruisce lo stato operativo, organizza le sessioni scientifiche, alimenta dashboard e analytics, conserva il patrimonio osservativo e fornisce assistenza AI.

Il principio guida è:

> **Observe - Understand - Preserve**

- **Observe**: acquisire eventi, log, telemetria, stato e dati scientifici.
- **Understand**: correlare i dati, ricostruire il contesto e produrre analisi comprensibili.
- **Preserve**: conservare immagini, metadati, configurazioni, report, elaborazioni e conoscenza.

## 4. Visione

Digital StarGate deve diventare il livello digitale e conoscitivo dell'osservatorio remoto: una piattaforma capace di mostrare cosa sta accadendo, spiegare cosa è accaduto, preservare ciò che è stato acquisito e supportare le decisioni successive.

La piattaforma è orientata a quattro risultati:

1. visibilità operativa in tempo quasi reale;
2. tracciabilità completa delle sessioni;
3. conservazione strutturata dei dati scientifici;
4. assistenza intelligente basata su evidenze.

## 5. Confini di responsabilità

### 5.1 EAGLE e software astronomici

Mantengono la responsabilità di:

- controllo diretto di montatura, cupola, camere, focheggiatori e accessori;
- esecuzione delle sequenze NINA;
- guida tramite PHD2;
- controllo montatura tramite CPWI e ASCOM;
- automazione locale e procedure di sicurezza;
- acquisizione dei file scientifici;
- continuità operativa locale anche in assenza di connettività esterna.

### 5.2 Digital StarGate

Assume la responsabilità di:

- raccolta di log, eventi e telemetria;
- parsing e normalizzazione;
- ricostruzione dello stato operativo;
- dashboard Mission Control;
- gestione delle Scientific Session;
- indicizzazione del repository scientifico;
- analytics, reportistica e quality assessment;
- orchestrazione dei workflow scientifici non safety-critical;
- assistenza AI e interrogazione dello storico;
- governance, audit e tracciabilità.

### 5.3 Vincolo di sicurezza

Digital StarGate non deve diventare autorità primaria per comandi safety-critical. Qualunque futura capacità di azione dovrà essere esplicitamente approvata tramite ADR, sottoposta a quality gate e mediata dai controlli locali dell'EAGLE.

## 6. Principi architetturali

### 6.1 Local First

Le funzioni essenziali dell'osservatorio devono rimanere disponibili localmente. La perdita della connettività verso PC Principale o cloud non deve compromettere acquisizione e sicurezza.

### 6.2 Safety First

La sicurezza fisica prevale su disponibilità, automazione, analytics e continuità del portale.

### 6.3 Event Driven

Le variazioni significative vengono rappresentate come eventi normalizzati e persistenti.

### 6.4 Immutable Telemetry

I dati grezzi acquisiti non vengono riscritti. Correzioni, arricchimenti e correlazioni producono nuove rappresentazioni derivate.

### 6.5 AI Assisted

L'AI analizza, spiega e suggerisce. Non esercita controllo diretto sull'osservatorio.

### 6.6 Scientific Integrity

I file scientifici originali sono preservati. Trasformazioni e processi devono essere tracciabili e riproducibili.

### 6.7 Storage Abstraction

Il repository scientifico è logico e non dipende da un singolo supporto fisico. I metadati restano separati dai file di grandi dimensioni.

### 6.8 Modular Platform

I componenti sono separati per responsabilità, contratti e ciclo di vita.

### 6.9 Observable Everything

Servizi, pipeline e integrazioni devono esporre stato, metriche, log e health check.

### 6.10 Open and Replaceable Integrations

Le integrazioni devono usare formati e contratti documentati, evitando dipendenze non sostituibili quando possibile.

## 7. Domini enterprise

| Dominio | Responsabilità principale |
|---|---|
| Observatory | Rappresentazione documentale e digitale dell'osservatorio reale |
| Telemetry | Raccolta, parsing, normalizzazione e persistenza dei dati operativi |
| Mission Control | Dashboard live, timeline, alert, health e session monitoring |
| Scientific Repository | Catalogazione di sessioni, immagini, calibration frame, log e prodotti |
| Scientific Workflow | Validazione, preparazione dataset, processing tracking e pubblicazione |
| Analytics | KPI, trend, qualità, performance e reporting |
| Observatory Intelligence | Analisi AI, assistenza, diagnostica e report automatici |
| Knowledge | Glossario, knowledge graph, casi, decisioni e storico interrogabile |
| Configuration | Baseline, versioni, profili, mapping e parametri |
| Security | Identità, accessi, segreti, audit e protezione dei dati |
| Community | Pubblicazione controllata e valorizzazione dei risultati |

## 8. I quattro pilastri

### 8.1 Mission Control

Mission Control è il punto di accesso operativo alla piattaforma.

Capacità target:

- stato corrente della sessione;
- stato dei dispositivi ricostruito dai dati disponibili;
- timeline degli eventi;
- alert e anomalie;
- metriche di guida, acquisizione, rete, meteo e storage;
- health della piattaforma;
- navigazione verso repository, analytics e AI Assistant.

### 8.2 Scientific Repository

Il Scientific Repository è l'archivio logico e indicizzato del patrimonio osservativo.

Comprende:

- Scientific Session;
- target e coordinate;
- file LIGHT, DARK, FLAT, BIAS e master;
- log e telemetria;
- configurazioni e profili;
- progetti PixInsight;
- report e metriche;
- immagini finali e prodotti pubblicabili.

### 8.3 Observatory Intelligence

Observatory Intelligence include i servizi AI e analitici avanzati.

Capacità target:

- analisi automatica dei log;
- spiegazione delle anomalie;
- report della notte;
- valutazione qualità della sessione;
- suggerimenti di troubleshooting;
- supporto alla preparazione dei dataset;
- assistenza PixInsight basata sui dati disponibili;
- ricerca in linguaggio naturale sullo storico;
- supporto alla manutenzione predittiva, previa validazione dei modelli.

### 8.4 Scientific Workflow Engine

Il Scientific Workflow Engine governa il ciclo di vita successivo all'acquisizione.

Flusso logico:

```text
Acquisition
    -> Validation
    -> Repository Registration
    -> Dataset Preparation
    -> Calibration and Processing Tracking
    -> Quality Assessment
    -> Publication
    -> Knowledge Update
```

Non esegue comandi safety-critical e non sostituisce il sequencer di acquisizione.

## 9. Scientific Session

La Scientific Session è l'aggregato principale del dominio.

### 9.1 Identità

Ogni sessione deve possedere:

- `session_id` univoco;
- data e intervallo temporale;
- osservatorio e sito;
- target principale e target secondari;
- stato del ciclo di vita;
- riferimenti ai dati grezzi e derivati.

### 9.2 Contenuto minimo

- setup ottico e strumentale;
- camera, filtri e profilo di acquisizione;
- coordinate e oggetto;
- log NINA, PHD2, CPWI, ASCOM e servizi EAGLE disponibili;
- condizioni meteo e ambientali;
- metriche di guida e qualità;
- file scientifici e calibration frame;
- eventi e anomalie;
- report automatici e manuali;
- stato del processing;
- prodotti finali.

### 9.3 Stati indicativi

```text
Planned
Acquiring
Acquired
Ingesting
Validated
ReadyForProcessing
Processing
Processed
Published
Archived
Failed
```

Gli stati definitivi saranno formalizzati nel modello di dominio e nei contratti software.

## 10. Macro-architettura logica

```text
+---------------------------------------------------------------+
|                  Digital StarGate Portal                       |
|                                                               |
| Mission Control | Repository | Analytics | AI Assistant        |
+-------------------------------+-------------------------------+
                                |
+---------------------------------------------------------------+
|                Application and Domain Services                 |
| Session | Telemetry | Repository | Workflow | AI | Reporting   |
+-------------------------------+-------------------------------+
                                |
+---------------------------------------------------------------+
|                  Data and Event Platform                       |
| Raw Logs | Normalized Events | Telemetry | Metadata | Indexes   |
+-------------------------------+-------------------------------+
                                |
+---------------------------------------------------------------+
|                    EAGLE Integration Layer                     |
| Collector | File Watcher | Parsers | Sync Agent | Health Agent  |
+-------------------------------+-------------------------------+
                                |
+---------------------------------------------------------------+
| NINA | PHD2 | CPWI | ASCOM | Weather | Network | Storage       |
+---------------------------------------------------------------+
```

## 11. Flusso dati principale

1. Un collector locale legge log, file di stato e directory autorizzate sull'EAGLE.
2. Il collector trasferisce record e riferimenti ai file senza alterare gli originali.
3. I parser trasformano i formati sorgente in record interpretabili.
4. Il normalizzatore produce eventi e misure conformi ai contratti Digital StarGate.
5. Lo State Engine ricostruisce lo stato corrente e la timeline.
6. Il Session Service correla dati e file con la Scientific Session.
7. Il Repository Service registra ubicazione, checksum, metadati e stato dei file.
8. Analytics e AI elaborano copie o viste derivate.
9. Mission Control presenta stato, eventi, alert e qualità.
10. Il Workflow Engine prepara e traccia le fasi successive all'acquisizione.

## 12. Modello di deployment target

### 12.1 EAGLE

Componenti leggeri e locali:

- Log Collector;
- File Watcher;
- Sync Agent;
- Local Queue;
- Health Agent;
- configurazione minima e segreti locali protetti.

### 12.2 PC Principale

Componenti principali della piattaforma:

- API e servizi applicativi;
- database operativo;
- indicizzazione repository;
- dashboard e portale;
- analytics;
- servizi AI locali o con provider configurabile;
- strumenti di amministrazione e governance.

### 12.3 Storage scientifico

Possibili supporti:

- disco locale dedicato;
- NAS;
- storage di rete;
- object storage compatibile;
- cloud, se approvato.

GitHub conserva codice, configurazioni, metadati selezionati, report, documentazione e automazioni, ma non è il repository primario dei dataset RAW di grandi dimensioni.

## 13. Servizi logici target

| Servizio | Responsabilità |
|---|---|
| Collector Service | Acquisizione locale di log, telemetria e riferimenti file |
| Parsing Service | Interpretazione dei formati sorgente |
| Normalization Service | Produzione di eventi e misure canoniche |
| Session Service | Gestione del ciclo di vita della Scientific Session |
| State Service | Ricostruzione dello stato corrente |
| Repository Service | Catalogo, checksum, ubicazioni, retention e dataset |
| Workflow Service | Orchestrazione delle fasi scientifiche |
| Analytics Service | KPI, trend, qualità e aggregazioni |
| AI Service | Analisi assistita, report e Q&A |
| Notification Service | Alert e comunicazioni |
| Identity Service | Autenticazione e autorizzazione |
| Configuration Service | Profili, mapping, feature flag e baseline |
| Health Service | Health check, metriche e dipendenze |

La decomposizione fisica in processi o microservizi non è ancora approvata. Nella prima implementazione è preferibile un'architettura modulare, evitando complessità distribuita prematura.

## 14. Dati e persistenza

Categorie principali:

- raw log records;
- normalized events;
- telemetry samples;
- session metadata;
- file catalog e checksum;
- derived metrics;
- alerts e incidents;
- AI reports e prompt evidence;
- workflow execution history;
- configuration baselines;
- audit records.

I file scientifici rimangono nello storage dedicato; il database mantiene riferimenti, metadati e integrità.

## 15. AI Observatory Assistant

### 15.1 Principi

- utilizza solo dati e documenti autorizzati;
- distingue evidenze, inferenze e suggerimenti;
- include riferimenti alla sessione e ai dati analizzati;
- non modifica i RAW;
- non invia comandi diretti ai dispositivi;
- registra modello, versione, input rilevanti e output;
- permette revisione umana.

### 15.2 Use case iniziali

1. sintesi automatica della notte;
2. individuazione di errori ricorrenti nei log;
3. correlazione tra guida, meteo e frame scartati;
4. spiegazione di interruzioni e recovery;
5. suggerimento dei controlli da eseguire;
6. interrogazione dello storico delle sessioni;
7. verifica della completezza del dataset per PixInsight.

## 16. Scientific Repository

### 16.1 Struttura logica indicativa

```text
ScientificRepository/
  Sessions/
    YYYY/
      YYYY-MM-DD_<target>_<session-id>/
        raw/
          light/
          dark/
          flat/
          bias/
        logs/
        telemetry/
        metadata/
        processing/
          pixinsight/
          masters/
          intermediate/
        reports/
        final/
```

La struttura fisica può variare; la struttura logica e i metadati canonici devono rimanere stabili.

### 16.2 Controlli minimi

- checksum;
- deduplicazione controllata;
- stato di sincronizzazione;
- presenza dei file attesi;
- gestione degli errori;
- retention configurabile;
- audit delle modifiche ai metadati;
- separazione tra originali e derivati.

## 17. Mission Control

Vista target:

- sessione corrente;
- stato piattaforma;
- stato delle fonti dati;
- timeline degli eventi;
- metriche principali;
- alert aperti;
- avanzamento acquisizione;
- stato repository e sincronizzazione;
- accesso al report AI;
- accesso allo storico.

Mission Control rappresenta dati osservati o ricostruiti. Ogni indicatore deve rendere evidente origine, timestamp e livello di affidabilità.

## 18. Requisiti non funzionali iniziali

| Categoria | Requisito iniziale |
|---|---|
| Availability | Il collector locale deve tollerare indisponibilità temporanea del PC Principale |
| Resilience | I dati non inviati devono essere accodati e ritrasmessi |
| Integrity | Checksum e audit per i file catalogati |
| Security | Least privilege, segreti protetti, autenticazione e audit |
| Performance | Dashboard aggiornata con latenza compatibile con il monitoraggio operativo |
| Scalability | Supporto a crescita pluriennale di sessioni, telemetria e immagini |
| Maintainability | Moduli separati, contratti versionati, test automatici |
| Portability | Deployment locale come baseline, cloud opzionale |
| Explainability | Output AI collegato a evidenze e sessioni |
| Recoverability | Backup e ripristino documentati per database e metadati |

I valori quantitativi saranno definiti nei documenti NFR e nelle solution architecture.

## 19. Sicurezza e governance

- nessun segreto nel repository Git;
- accessi separati per amministrazione, operazione e consultazione;
- audit delle modifiche;
- classificazione dei dati;
- backup verificati;
- retention documentata;
- AI Governance applicata a modelli, dati e output;
- change management per modifiche ai contratti;
- quality gate prima delle release.

## 20. Roadmap di implementazione

### Fase 1 - Telemetry Foundation

- collector EAGLE;
- parser iniziali;
- normalizzazione eventi;
- persistenza;
- health e diagnostica.

### Fase 2 - Scientific Session

- modello sessione;
- correlazione log e file;
- stato del ciclo di vita;
- prime API.

### Fase 3 - Mission Control

- dashboard live;
- timeline;
- alert;
- session monitor.

### Fase 4 - Scientific Repository

- catalogo file;
- checksum;
- struttura dataset;
- sincronizzazione e retention.

### Fase 5 - Analytics

- KPI;
- quality assessment;
- trend;
- reportistica.

### Fase 6 - Observatory Intelligence

- night report;
- log analyzer;
- Q&A sullo storico;
- suggerimenti assistiti.

### Fase 7 - Scientific Workflow

- dataset validation;
- PixInsight preparation;
- processing tracking;
- publication workflow.

## 21. Decisioni architetturali collegate

| ADR | Decisione |
|---|---|
| ADR-005 | L'EAGLE mantiene l'autorità operativa |
| ADR-006 | Scientific Session come aggregato principale |
| ADR-007 | Architettura event-driven e telemetria immutabile |
| ADR-008 | Repository scientifico logico e storage indipendente |
| ADR-009 | AI limitata a supporto, analisi e suggerimento |

## 22. Questioni aperte

- stack tecnologico definitivo;
- database operativo e motore di indicizzazione;
- formato canonico degli eventi;
- protocollo di sincronizzazione EAGLE-PC Principale;
- strategia di storage fisico;
- retention e backup dei RAW;
- provider e modelli AI;
- criteri quantitativi di qualità;
- integrazione PixInsight;
- autenticazione per accesso remoto.

Queste questioni saranno risolte in DSG-SW-001 e nei successivi documenti di solution architecture e ADR.

## 23. Criteri di accettazione

DSRA-002 può passare da `Proposed` ad `Approved` quando:

- i confini EAGLE/Digital StarGate sono approvati;
- la Scientific Session è accettata come entità principale;
- i quattro pilastri sono recepiti nella Master Roadmap;
- gli ADR-005/009 sono pubblicati;
- la navigazione MkDocs è aggiornata;
- `mkdocs build --strict` termina senza errori;
- il change set della Release 1.1 è tracciato nei registri.

## 24. Conclusione

Digital StarGate è una piattaforma di osservabilità, conoscenza e valorizzazione scientifica. Il suo compito non è sostituire il controllo locale dell'osservatorio, ma raccogliere ciò che accade, comprenderlo, conservarlo e renderlo utile nel tempo.
