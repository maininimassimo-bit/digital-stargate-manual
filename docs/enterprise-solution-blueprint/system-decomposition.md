# DSG-ESB-002 - System Decomposition and Container Architecture

| Campo | Valore |
|---|---|
| Documento | System Decomposition and Container Architecture |
| Identificativo | `DSG-ESB-002` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Data | 2026-07-26 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Identificare i domini applicativi principali di Digital StarGate e, per ciascun dominio, i container logici previsti. Un container in questo documento e una unita architetturale di responsabilita, non un container Docker implementato.

## Regole di decomposizione

- Ogni dominio deve avere confini chiari e responsabilita verificabili.
- I domini TO-BE non sono dichiarati implementati.
- I container locali su EAGLE non devono aggirare le regole safety e operative documentate.
- Le interfacce sono descritte come contratti logici o protocolli suggeriti, non come API implementate.
- I dati persistenti sono indicati come classi informative, non come schema database definitivo.

## Vista sintetica dei domini

| ID | Dominio | Responsabilita primaria | Nodo prevalente | Stato |
|---|---|---|---|---|
| `DSG-DOM-OBS` | Observatory | Asset fisici, stato osservatorio, strumenti e sessione | EAGLE / campo | AS-IS / Transition |
| `DSG-DOM-AUT` | Automation | Sequenze operative, controlli e recovery | EAGLE | Transition |
| `DSG-DOM-IMG` | Imaging | Acquisizione, calibrazione, elaborazione e prodotti immagine | EAGLE + PC Principale | Transition |
| `DSG-DOM-SCH` | Scheduler | Pianificazione osservazioni e priorita | PC Principale + EAGLE | TO-BE |
| `DSG-DOM-AI` | AI | Analisi assistita e knowledge support | PC Principale / Cloud | TO-BE / TBD |
| `DSG-DOM-ANL` | Analytics | KPI, dashboard e reporting | PC Principale | Transition |
| `DSG-DOM-DP` | Data Platform | Storage, catalogo, warehouse e lineage | PC Principale / Storage | Transition |
| `DSG-DOM-KG` | Knowledge Graph | Relazioni semantiche tra documenti, dati e decisioni | PC Principale / Cloud | TO-BE / TBD |
| `DSG-DOM-DOC` | Documentation | Manuale, SOP, ADR, registri e release evidence | GitHub / PC Principale | AS-IS / Transition |
| `DSG-DOM-UP` | User Portal | Accesso utente a documentazione, dashboard e stato | GitHub Pages / Cloud | Transition |
| `DSG-DOM-API` | API Gateway | Contratti di esposizione controllata tra domini | Cloud / PC Principale | TO-BE / TBD |
| `DSG-DOM-IAM` | Identity & Access | Accessi, ruoli, VPN, segreti e autorizzazioni | RUT955 / GitHub / Cloud | Transition |
| `DSG-DOM-NOT` | Notification | Alert operativi, esiti job, anomalie e promemoria | PC Principale / Cloud | TO-BE |
| `DSG-DOM-MON` | Monitoring | Metriche di salute, disponibilita e readiness | EAGLE + PC Principale | Transition |
| `DSG-DOM-LOG` | Logging | Log applicativi, eventi, audit trail e correlazione | EAGLE + PC Principale | Transition |
| `DSG-DOM-BRC` | Backup & Recovery | Backup, restore, archiviazione e continuita | Storage locale + remoto | Transition |

## Decomposizione per dominio

### `DSG-DOM-OBS` - Observatory

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Rappresentare e governare asset fisici, stato osservatorio, montatura, camere, ottiche, cupola/tetto, alimentazioni e sensori locali. |
| Confini | Include dispositivi e stato operativo locale; esclude analytics, pubblicazione e governance documentale. |
| Dipendenze | EAGLE, ASCOM, CPWI, N.I.N.A., PHD2, rete locale, alimentazioni, sensori meteo e AllSky. |
| Interfacce | ASCOM/driver, USB, seriale o rete locale, desktop remoto approvato, eventuali endpoint locali da validare. |
| Dati gestiti | Stato dispositivi, configurazioni operative, log hardware, mapping USB/alimentazioni, stato Park, stato sicurezza. |
| Servizi offerti | Disponibilita asset, controllo strumenti, readiness fisica, evidenze di sessione e stato osservatorio. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-OBS-01` | Observatory Device Control | Accesso controllato a montatura, camere, fuocheggiatori, filtri e alimentazioni | ASCOM Platform, driver vendor, CPWI | EAGLE, USB, rete locale | Profili driver, versioni, configurazioni | ASCOM COM/Alpaca, USB, TCP locale |
| `DSG-CTR-OBS-02` | Observatory State Registry | Stato logico di osservatorio, sessione, Park, apertura/chiusura e readiness | File registry versionato o data catalog leggero | Automation, Logging | Stato sessione, checklist, incident evidence | File, Markdown, JSON/YAML sanitizzato |
| `DSG-CTR-OBS-03` | Environmental Context Adapter | Raccolta contesto meteo e AllSky per supporto decisionale | AllSky web, weather station export, file drop | AllSky, Weather Station, Monitoring | Snapshot meteo, immagini contesto, timestamp | HTTP locale, file, CSV/JSON da validare |

### `DSG-DOM-AUT` - Automation

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Coordinare sequenze operative, pre-check, recovery controllato, sincronizzazione dati e stop sicuro. |
| Confini | Non sostituisce controlli safety fisici; non abilita AI autonoma su funzioni critiche. |
| Dipendenze | Observatory, Imaging, Scheduler, Monitoring, Logging, Notification. |
| Interfacce | Sequenze N.I.N.A., PHD2, CPWI, ASCOM, script operativi approvati, checklist SOP. |
| Dati gestiti | Profili, sequenze, stati job, esiti controlli, anomalie, log automazione. |
| Servizi offerti | Avvio sessione, acquisizione automatica, recovery guidato, chiusura dati e handover evidenze. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-AUT-01` | Session Orchestrator | Coordina readiness, sequenza osservativa e stop controllato | N.I.N.A. Advanced Sequencer, script Windows approvati | Observatory, Imaging, Scheduler | Sequenze, profili, run state | File, COM/ASCOM, IPC locale da validare |
| `DSG-CTR-AUT-02` | Safety Gate Controller | Applica controlli pre-sessione e condizioni di stop | Checklist SOP, regole configurabili versionate | Monitoring, Weather, Observatory | Esiti checklist, soglie, evidenze | File, alert, log |
| `DSG-CTR-AUT-03` | Sync Agent | Trasferisce report, log, preview e dati verso PC Principale/storage | Robocopy/rsync-equivalente, tool sync approvato | Data Platform, Backup | Manifest trasferimento, hash, retry state | SMB/SFTP/VPN/cloud sync da validare |

### `DSG-DOM-IMG` - Imaging

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Gestire acquisizione FITS, calibrazione, elaborazione, controllo qualita immagini e prodotti finali. |
| Confini | Non governa scheduling globale o pubblicazione finale; produce dati e prodotti per Data Platform e Portal. |
| Dipendenze | Observatory, Automation, Data Platform, Analytics, external tools come PixInsight/Astrometry.net. |
| Interfacce | N.I.N.A., FITS, cartelle sessione, PixInsight, solver, repository dati. |
| Dati gestiti | Light, dark, flat, bias, master, immagini calibrate, log processing, metadata FITS. |
| Servizi offerti | Dataset immagini, prodotti calibrati, metriche qualita, asset pubblicabili. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-IMG-01` | Acquisition Workspace | Area di acquisizione temporanea su EAGLE | File system Windows, N.I.N.A. | Observatory, Automation | FITS raw, log sessione | File system locale |
| `DSG-CTR-IMG-02` | Processing Workspace | Calibrazione, integrazione ed export | PixInsight, ASTAP, tool FITS approvati | Data Platform | Master, calibrated, integrated, exports | File, FITS, XISF/TIFF/PNG da validare |
| `DSG-CTR-IMG-03` | Image Quality Evaluator | Calcola metriche tecniche e flag di qualita | PixInsight SubframeSelector, script report, analytics | Processing, Analytics | FWHM/HFR, eccentricita, SNR, rejection | CSV/JSON, report Markdown |

### `DSG-DOM-SCH` - Scheduler

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Pianificare finestre osservative, target, priorita, vincoli meteo, luna, disponibilita asset e readiness. |
| Confini | Non comanda direttamente hardware senza passare da Automation e safety gate. |
| Dipendenze | Observatory, Weather, Data Platform, Notification, User Portal. |
| Interfacce | Cataloghi target, calendari, finestre meteo, stato osservatorio, sequenze N.I.N.A. da validare. |
| Dati gestiti | Target list, priorita, vincoli, finestre, esiti pianificazione. |
| Servizi offerti | Piano sessione, readiness forecast, backlog target e raccomandazioni non vincolanti. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-SCH-01` | Target Planner | Mantiene target, vincoli e priorita | Foglio controllato, YAML/CSV, tool planetario da validare | Data Platform | Target backlog, vincoli | File, CSV/YAML |
| `DSG-CTR-SCH-02` | Session Plan Generator | Produce piano osservativo verificabile | N.I.N.A. planning export o script approvato | Automation, Weather | Piani sessione, versioni | File, JSON/CSV da validare |
| `DSG-CTR-SCH-03` | Readiness Calendar | Evidenzia finestre e blocchi operativi | Calendar, dashboard, static export | Monitoring, Notification | Finestre, stato readiness | ICS/Markdown/HTML da validare |

### `DSG-DOM-AI` - AI

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Supportare analisi, ricerca conoscenza, sintesi, classificazione e troubleshooting non safety. |
| Confini | Nessuna azione autonoma su cupola, montatura, alimentazioni o safety; nessun accesso a segreti. |
| Dipendenze | Documentation, Knowledge Graph, Data Platform, Governance, Identity & Access. |
| Interfacce | Knowledge base approvata, dataset sanitizzati, prompt registrati, audit output. |
| Dati gestiti | Prompt, risposte, riferimenti, confidence, revisioni umane, audit. |
| Servizi offerti | Assistente documentale, analisi report, spiegazione anomalie, supporto decisionale revisionato. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-AI-01` | AI Assistant Runtime | Esegue casi d'uso AI approvati | OpenAI API o modello approvato | IAM, Knowledge Graph | Audit prompt/output, versioni modello | HTTPS/API governata |
| `DSG-CTR-AI-02` | Retrieval Layer | Recupera fonti documentali e dati sanitizzati | RAG su indice documentale, vector store da decidere | Documentation, Knowledge Graph | Indici, embeddings, mapping fonti | HTTPS, file, query API da validare |
| `DSG-CTR-AI-03` | Human Review Queue | Traccia revisione umana degli output AI | GitHub Issues/PR, registro review | Governance | Esiti review, decisioni, eccezioni | GitHub, Markdown |

### `DSG-DOM-ANL` - Analytics

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Calcolare KPI, dashboard, trend, quality gate e report operativi. |
| Confini | Non e sistema di controllo real-time safety; pubblica insight e controlli. |
| Dipendenze | Data Platform, Logging, Imaging, Documentation, User Portal. |
| Interfacce | Dataset warehouse, CSV/JSON, dashboard statiche, report Markdown. |
| Dati gestiti | KPI sessione, qualita dati, trend, anomalie, stato validazione. |
| Servizi offerti | Dashboard, report, quality evidence e readiness indicator. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-ANL-01` | Analytics Warehouse | Consolida dataset e metriche | DuckDB/Parquet o engine gia ADR-003 | Data Platform | Tabelle, snapshot, lineage | SQL locale, file |
| `DSG-CTR-ANL-02` | KPI Engine | Calcola indicatori e quality gates | Python/pandas o tool approvato | Warehouse | KPI, esiti gate | CSV/JSON/HTML |
| `DSG-CTR-ANL-03` | Dashboard Publisher | Pubblica viste statiche | MkDocs, HTML statico, GitHub Pages | Portal, Documentation | Dashboard build output | Static files |

### `DSG-DOM-DP` - Data Platform

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Gestire storage, data catalog, schema, lineage, retention, integrita e dataset per analytics/AI. |
| Confini | Non sostituisce archivi raw; coordina livelli dati e controlli. |
| Dipendenze | Imaging, Logging, Backup, Analytics, Knowledge Graph. |
| Interfacce | File system, manifest, hash, warehouse, catalogo, repository Git per metadati. |
| Dati gestiti | Raw, processed, logs, metadata, manifest, catalogo, quality evidence. |
| Servizi offerti | Dataset versionati, controllo integrita, lineage, accesso controllato ai dati. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-DP-01` | Raw Data Repository | Conserva dati osservativi originali | Storage locale/NAS/cloud storage | Imaging, Backup | FITS raw, log raw | File, SMB/SFTP/cloud sync |
| `DSG-CTR-DP-02` | Curated Data Catalog | Registra dataset, metadata e stato qualita | Markdown registry, CSV/Parquet catalog | Analytics, Documentation | Dataset registry, manifest, hash | File, SQL/CSV |
| `DSG-CTR-DP-03` | Lineage and Retention Controller | Collega fonti, prodotti e policy retention | Manifest versionati, checksum | Backup, Governance | Lineage, retention class, restore evidence | Markdown/JSON/YAML |

### `DSG-DOM-KG` - Knowledge Graph

| Aspetto | Descrizione |
|---|---|
| Responsabilita | Modellare relazioni tra asset, osservazioni, documenti, ADR, rischi, controlli, release e dataset. |
| Confini | Non e implementato come piattaforma baseline; schema e storage sono TBD. |
| Dipendenze | Documentation, Data Platform, AI, Governance, Registries. |
| Interfacce | Registri enterprise, documenti MkDocs, metadata dataset, ADR, DSRA. |
| Dati gestiti | Entita, relazioni, URI documentali, provenance, stato validazione. |
| Servizi offerti | Ricerca semantica, impatto modifiche, tracciabilita e supporto AI. |

Container logici:

| ID | Container | Funzione | Tecnologie suggerite | Dipendenze | Dati persistenti | Protocolli |
|---|---|---|---|---|---|---|
| `DSG-CTR-KG-01` | Ontology Registry | Definisce classi e relazioni | RDF/OWL o property graph, TBD | Governance | Ontologia, versioni | Turtle/JSON-LD/Markdown |
| `DSG-CTR-KG-02` | Graph Store | Conserva relazioni interrogabili | Neo4j, RDF store o graph layer leggero | Data Platform | Nodi, relazioni, indici | Cypher/SPARQL/API TBD |
| `DSG-CTR-KG-03` | Traceability Mapper | Popola relazioni da documenti e registri | Parser documentale approvato, GitHub metadata | Documentation | Mapping roadmap-decisioni-rischi | File, GitHub, query graph |

### Domini trasversali

| Dominio | Container principali | Note architetturali |
|---|---|---|
| `DSG-DOM-DOC` Documentation | `DSG-CTR-DOC-01` MkDocs Source, `DSG-CTR-DOC-02` Registry Set, `DSG-CTR-DOC-03` Release Evidence Pack | Baseline AS-IS/Transition gia governata da `DSG-ADR-004`. |
| `DSG-DOM-UP` User Portal | `DSG-CTR-UP-01` Static Portal, `DSG-CTR-UP-02` Dashboard View, `DSG-CTR-UP-03` Publication Pipeline | Pubblicazione statica preferita per ridurre superficie d'attacco. |
| `DSG-DOM-API` API Gateway | `DSG-CTR-API-01` External Facade, `DSG-CTR-API-02` Internal Contract Registry, `DSG-CTR-API-03` Rate/Audit Policy | TO-BE; non implementare finche non approvato. |
| `DSG-DOM-IAM` Identity & Access | `DSG-CTR-IAM-01` VPN Access, `DSG-CTR-IAM-02` GitHub Permissions, `DSG-CTR-IAM-03` Secrets Custody | Segreti fuori repository; audit accessi richiesto. |
| `DSG-DOM-NOT` Notification | `DSG-CTR-NOT-01` Alert Router, `DSG-CTR-NOT-02` Notification Templates, `DSG-CTR-NOT-03` Escalation Log | Canali e destinatari da validare; no allarmi safety non testati. |
| `DSG-DOM-MON` Monitoring | `DSG-CTR-MON-01` Health Collector, `DSG-CTR-MON-02` Readiness Monitor, `DSG-CTR-MON-03` Availability Dashboard | Metriche locali e remote; tollerante a perdita VPN. |
| `DSG-DOM-LOG` Logging | `DSG-CTR-LOG-01` Local Log Collector, `DSG-CTR-LOG-02` Correlation Index, `DSG-CTR-LOG-03` Audit Archive | Correlazione per timestamp, sessione, componente e severity. |
| `DSG-DOM-BRC` Backup & Recovery | `DSG-CTR-BRC-01` Backup Executor, `DSG-CTR-BRC-02` Restore Test Evidence, `DSG-CTR-BRC-03` Continuity Runbook | RTO/RPO numerici da validare; restore test obbligatori. |

## Matrice dipendenze sintetica

| Dominio sorgente | Dipende da | Motivo |
|---|---|---|
| Observatory | IAM, Monitoring, Logging | Accesso sicuro, stato e diagnosi |
| Automation | Observatory, Scheduler, Notification, Logging | Esecuzione controllata e feedback |
| Imaging | Observatory, Data Platform, Backup | Acquisizione e conservazione |
| Scheduler | Observatory, Weather, Data Platform | Pianificazione verificabile |
| AI | Documentation, Knowledge Graph, IAM | Fonti approvate e controllo accessi |
| Analytics | Data Platform, Logging, Documentation | KPI e pubblicazione |
| Knowledge Graph | Documentation, Registries, Data Platform | Tracciabilita semantica |
| User Portal | Documentation, Analytics, IAM | Pubblicazione e accesso controllato |
| Monitoring | Observatory, Network, Logging | Health e readiness |
| Backup & Recovery | Data Platform, Documentation, IAM | Protezione dati e restore |

## Criteri di accettazione della decomposizione

- Ogni dominio ha responsabilita, confini, dipendenze, interfacce, dati e servizi.
- Ogni container ha funzione, tecnologia suggerita, dipendenze, dati persistenti e protocolli.
- I domini TO-BE sono marcati come `TBD` o `Da validare` quando mancano decisioni implementative.
- Nessun container assegna funzioni safety autonome ad AI, portal, dashboard o cloud.
- Le dipendenze rispettano la separazione PC Principale / EAGLE definita da `DSRA-001`.
