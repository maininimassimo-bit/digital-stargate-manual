# DSG-MR-001 - Release 1.1 Change Set

| Campo | Valore |
|---|---|
| Documento | Master Roadmap Release 1.1 Change Set |
| Identificativo | DSG-MR-001-CS-1.1 |
| Stato | Proposed |
| Versione | 0.1 |
| Data | 2026-07-28 |
| Branch | `docs/roadmap-ai-scientific-repository` |

## 1. Obiettivo

Questo change set formalizza le estensioni della Master Roadmap necessarie per rendere operativi gli ambiti AI, Live Operations e Image and Scientific Repository già previsti da DSG-MR-001.

Non introduce un sistema alternativo di controllo dell'osservatorio. L'EAGLE e i software astronomici mantengono l'autorità operativa.

## 2. Modifiche richieste alla visione

Integrare il principio:

> **Observe - Understand - Preserve**

Digital StarGate acquisisce dati ed eventi, li correla e interpreta, quindi preserva sessioni, file, metadati e conoscenza.

## 3. Estensione degli obiettivi strategici

Aggiungere:

| ID | Obiettivo | Stato iniziale |
|---|---|---|
| SO-06 | Definire la Software Enterprise Baseline Release 1.1 | In corso |
| SO-07 | Implementare Telemetry e Live Operations Foundation | Da pianificare |
| SO-08 | Definire Scientific Session e Scientific Repository | In corso |
| SO-09 | Definire Observatory Intelligence e AI Governance operativa | In corso |
| SO-10 | Definire Scientific Workflow e integrazione PixInsight | Da validare |

## 4. Estensione del capability model

Aggiungere le capability:

- log collection;
- event parsing and normalization;
- live state reconstruction;
- scientific session management;
- scientific file cataloguing;
- dataset completeness validation;
- scientific workflow orchestration;
- AI-assisted log analysis;
- automatic night reporting;
- natural-language historical query;
- processing traceability;
- repository integrity and retention.

## 5. Evoluzione dei programmi esistenti

### 5.1 Image and Scientific Repository

Da programma generico a programma strutturato con:

- Scientific Session Repository;
- Repository Manager;
- Metadata and Catalog Engine;
- checksum e integrity controls;
- storage abstraction;
- dataset organization;
- PixInsight project linkage;
- lifecycle e retention.

### 5.2 Live Operations

Estendere con:

- Mission Control;
- telemetry ingestion;
- state reconstruction;
- event timeline;
- health monitoring;
- alert management;
- session progress;
- synchronization status.

### 5.3 AI

Rinominare il programma operativo in **Observatory Intelligence**, mantenendo AI Governance come controllo trasversale.

Use case iniziali:

- Night Report Generator;
- Log Analyzer;
- Anomaly Explanation;
- Equipment Health Analysis;
- Scientific Assistant;
- PixInsight Dataset Assistant;
- Historical Session Q&A.

### 5.4 Data

Estendere con:

- raw log store;
- normalized event store;
- telemetry store;
- scientific metadata catalog;
- AI report store;
- workflow history;
- audit trail.

## 6. Nuovo programma: Scientific Workflow

Responsabilità:

- validazione della completezza delle sessioni;
- preparazione dataset;
- collegamento a PixInsight;
- tracciamento delle elaborazioni;
- quality assessment;
- pubblicazione dei risultati;
- aggiornamento della knowledge base.

Il programma non sostituisce NINA e non controlla dispositivi safety-critical.

## 7. Modello di piattaforma aggiornato

| Nodo | Responsabilità target |
|---|---|
| EAGLE | Controllo osservatorio, acquisizione, automazione locale, sicurezza, collector locale, file watcher e coda di sincronizzazione |
| PC Principale | API, database, Mission Control, repository catalog, analytics, AI, workflow, governance e sviluppo |
| Scientific Storage | Conservazione dei file scientifici originali e derivati |
| GitHub | Codice, configurazioni, documentazione, report selezionati, workflow e metadati versionabili |
| Cloud opzionale | Servizi approvati di backup, AI o pubblicazione, senza dipendenza obbligatoria |

## 8. Nuova sequenza temporale 2026-2030

| Periodo | Focus aggiornato | Stato |
|---|---|---|
| 2026 | Baseline documentale, DSRA-002 e Software Enterprise Baseline | In corso |
| 2027 | Telemetry Foundation, Scientific Session e Mission Control MVP | Da pianificare |
| 2028 | Scientific Repository, Analytics e Workflow scientifico | Da validare |
| 2029 | Observatory Intelligence e Knowledge Platform governate | Da validare |
| 2030 | Piattaforma integrata, consolidata e misurabile | TBD |

## 9. Deliverable Release 1.1

- DSRA-002 - Next Generation Reference Architecture;
- ADR-005 - EAGLE Operational Authority;
- ADR-006 - Scientific Session Aggregate;
- ADR-007 - Event-Driven Immutable Telemetry;
- ADR-008 - Logical Scientific Repository;
- ADR-009 - AI Advisory Boundary;
- DSG-SW-001 - Software Architecture;
- documentazione Scientific Repository;
- documentazione Telemetry and Live Operations;
- documentazione Observatory Intelligence;
- aggiornamento MkDocs, registri e release documentation.

## 10. Quality gate

- coerenza con DSG-MR-001;
- nessuna estensione implicita del controllo operativo;
- link relativi validi;
- navigazione MkDocs aggiornata;
- `mkdocs build --strict` superato;
- commit atomici;
- review prima del merge.
