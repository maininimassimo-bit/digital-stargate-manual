# DSG-ESB-004 - NFR, Deployment, Technology Decisions and Roadmap

| Campo | Valore |
|---|---|
| Documento | NFR, Deployment, Technology Decisions and Roadmap |
| Identificativo | `DSG-ESB-004` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Data | 2026-07-26 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Definire i requisiti non funzionali, il modello di deployment, le raccomandazioni tecnologiche e la roadmap implementativa incrementale della piattaforma Digital StarGate.

Le scelte tecnologiche sono raccomandazioni architetturali. Non costituiscono implementazione approvata e devono essere convertite in ADR, change request, SOP o milestone esecutive secondo [Governance](../enterprise/governance.md).

## Requisiti non funzionali

### Scalabilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-SCA-001` | Scalare storage e catalogo dati per crescita annuale osservazioni | Aggiunta capacita senza ristrutturare naming, manifest e catalogo | Valori di capacita `TBD` |
| `DSG-NFR-SCA-002` | Separare raw, processed, analytics e publishable assets | Ogni classe dati ha percorso e retention chiari | Collegato a capitolo gestione dati |
| `DSG-NFR-SCA-003` | Consentire evoluzione AI/KG senza impatto sulle operazioni EAGLE | AI e KG consumano dati governati, non comandano safety | Coerente con `DSRA-001` |

### Disponibilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-AVL-001` | Operazioni locali resilienti a perdita cloud | EAGLE resta operativo per sequenza controllata e stato sicuro | Cloud non prerequisito safety |
| `DSG-NFR-AVL-002` | Accesso remoto tramite VPN e failover rete | Stato WAN/VPN monitorato e testato | RUT955/Starlink/SIM da validare |
| `DSG-NFR-AVL-003` | Portale documentale pubblicabile indipendentemente dall'EAGLE | MkDocs/GitHub Pages non dipendono dalla disponibilita campo | AS-IS / Transition |

### Performance

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-PER-001` | Acquisizione non bloccata da upload o analytics | Trasferimenti differiti o limitati durante sessione | Priorita a N.I.N.A. e storage locale |
| `DSG-NFR-PER-002` | Dashboard generate da dataset curati | Build dashboard ripetibile e tracciata | Tempi target `TBD` |
| `DSG-NFR-PER-003` | Processing immagini separato da controllo campo | PixInsight/processing su PC Principale o workstation, non in conflitto con sessione EAGLE | Da validare per risorse locali |

### Affidabilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-REL-001` | Ogni sessione produce evidenze minime | Log, report, conteggio frame, stato archiviazione | Collegato a SOP e data flow |
| `DSG-NFR-REL-002` | Recovery documentato per failure critiche | Procedure per guida persa, connessione persa, storage pieno, rete indisponibile | Capitoli tecnici esistenti |
| `DSG-NFR-REL-003` | Single control path per dispositivi critici | Nessun controllo concorrente non governato su montatura/camere/cupola | Vincolo ASCOM/CPWI |

### Osservabilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-OBS-001` | Log correlabili per sessione | ID sessione o timestamp coerente in report, log e dataset | Schema `TBD` |
| `DSG-NFR-OBS-002` | Metriche health minime | Spazio disco, stato rete, disponibilita EAGLE, esito sync, backup | Soglie `Da validare` |
| `DSG-NFR-OBS-003` | Incident evidence preservata | Timeline e log raccolti prima di cleanup | Collegato a problem management |

### Manutenibilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-MNT-001` | Documentazione e configurazioni pubblicabili versionate | MkDocs, registri e template sanitizzati in GitHub | Segreti esclusi |
| `DSG-NFR-MNT-002` | Aggiornamenti driver/tool con rollback | Versioni registrate, backup profili, test post-update | ASCOM, CPWI, PHD2, N.I.N.A. |
| `DSG-NFR-MNT-003` | Componenti TO-BE introdotti per milestone | Ogni fase ha criteri di verifica e rollback | Roadmap implementativa |

### Portabilita

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-PRT-001` | Documentazione portabile come sito statico | Build MkDocs riproducibile | GitHub Pages o hosting statico |
| `DSG-NFR-PRT-002` | Dataset leggibili con formati aperti quando possibile | FITS, CSV, Parquet, Markdown, JSON/YAML sanitizzato | Scelte definitive da ADR |
| `DSG-NFR-PRT-003` | Evitare lock-in dove non porta valore operativo | Alternative documentate per cloud, graph, analytics | Technology decision matrix |

### Backup, Recovery e Business Continuity

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-BRC-001` | Almeno due copie per dati osservativi rilevanti | Copia primaria e secondaria verificate | Supporti e cloud `TBD` |
| `DSG-NFR-BRC-002` | Restore test periodico | Evidenza restore con data, dataset, esito | Frequenza `Da validare` |
| `DSG-NFR-BRC-003` | Continuita operativa minima in caso perdita remoto | Procedure per messa in sicurezza e recupero accesso | Collegato a rete/VPN |
| `DSG-NFR-BRC-004` | RTO/RPO definiti per classe dati | Valori approvati per raw, processed, docs, configs | `TBD` |

### Security

| ID | Requisito | Criterio | Note |
|---|---|---|---|
| `DSG-NFR-SEC-001` | Accesso remoto solo tramite canali approvati | VPN, account nominativi, revoca credenziali | RUT955 / GitHub / Cloud |
| `DSG-NFR-SEC-002` | Segreti fuori repository | Nessuna password, chiave VPN, token, certificato privato o export sensibile | Controllo `QG-SEC` |
| `DSG-NFR-SEC-003` | AI senza dati sensibili non necessari | Prompt sanitizzati, retention nota, human review | Provider `TBD` |
| `DSG-NFR-SEC-004` | Logging e audit accessi | Eventi amministrativi e pubblicazioni tracciati | Scope da validare |

## Deployment model

### Vista generale

```text
[Operator / Maintainer]
        |
        v
[PC Principale] -- Git / MkDocs / Analytics / Processing / Release
        |
        +-- GitHub -- Repository / Pages / Issues / Release Evidence
        |
        +-- Cloud -- AI provider / storage / external catalogs (TBD)
        |
        v
[VPN / Remote Access]
        |
        v
[RUT955 / Starlink / LTE failover]
        |
        v
[EAGLE] -- N.I.N.A. / CPWI / PHD2 / ASCOM / ASTAP / Local Storage
        |
        +-- Observatory devices
        +-- AllSky / Weather / local sensors
        |
        v
[Storage / Backup] -- Primary archive / secondary copy / restore evidence
```

### PC Principale

| Responsabilita | Componenti logici | Dati | Note |
|---|---|---|---|
| Engineering e governance | Git, MkDocs, registri, ADR, release docs | Documentazione, registry, release evidence | Nodo di authoring e controllo documentale |
| Analytics e reporting | Warehouse, KPI engine, dashboard publisher | Dataset curati, KPI, report | Non real-time safety |
| Processing e curation | PixInsight/workspace, catalogo dati | Processed data, manifest, immagini finali | Separato da acquisizione campo |
| AI/KG TO-BE | Retrieval, graph, audit AI | Fonti approvate e dati sanitizzati | Solo dopo governance/ADR |

### EAGLE

| Responsabilita | Componenti logici | Dati | Note |
|---|---|---|---|
| Operazioni campo | N.I.N.A., CPWI, PHD2, ASCOM, ASTAP, driver | Profili, sequenze, log, FITS raw | Nodo operativo critico |
| Acquisizione | Acquisition Workspace, session orchestrator | FITS raw, log, report sessione | Priorita a stabilita e storage locale |
| Telemetria e readiness | Monitor locale, checklist, eventi | Stato dispositivi, health, errori | Contratti da validare |
| Sync controllato | Sync agent | Manifest, hash, retry state | Trasferimento non deve bloccare acquisizione |

### Cloud

| Responsabilita | Componenti logici | Stato | Vincoli |
|---|---|---|---|
| Storage remoto | Backup secondario, archive, sharing | TBD | Cifratura, retention e costi da decidere |
| AI provider | AI Assistant Runtime | TO-BE / TBD | Prompt sanitizzati, audit, human review |
| Servizi scientifici | Astrometry.net, TNS, AAVSO | TBD | Uso soggetto a SOP e decisioni future |

### GitHub

| Responsabilita | Componenti logici | Dati | Note |
|---|---|---|---|
| Source of record documentale | Repository, branch, PR, commit | Markdown, config MkDocs, evidence | Baseline gia operativa |
| Pubblicazione | GitHub Pages o pipeline statica | Sito, dashboard statiche, release notes | Build e link check richiesti |
| Governance workflow | Issues, review, changelog | Decisioni, commenti, approvazioni | Nessuna credenziale nel repo |

### Storage e Backup

| Livello | Contenuto | Requisito | Stato |
|---|---|---|---|
| Local EAGLE | FITS raw, log correnti, profili operativi | Disponibile durante sessione | AS-IS / Transition |
| Primary archive | Raw selezionati, processed, report, manifest | Verifica integrita | Da validare |
| Secondary backup | Copia off-site/cloud/offline | Isolamento da guasto locale | TBD |
| Restore evidence | Esito restore, hash, data test | Evidenza governata | Transition |

### Remote Access e VPN

| Componente | Responsabilita | Vincoli |
|---|---|---|
| RUT955 | Gateway, VPN, failover, firewall, log rete | Configurazioni sensibili non pubblicate |
| Starlink | WAN primaria | Health check e comportamento NAT da validare |
| LTE SIM1/SIM2 | Failover | Priorita, timeout e costi da validare |
| Desktop remoto | Accesso operativo EAGLE | Solo tramite canale approvato e account protetti |

### Componenti locali e remoti

| Locale | Remoto |
|---|---|
| EAGLE, dispositivi osservatorio, AllSky, sensori, storage temporaneo, RUT955 | PC Principale quando fuori osservatorio, GitHub, cloud storage, AI provider, cataloghi scientifici |

Il modello considera remoti tutti i servizi non necessari alla messa in sicurezza locale dell'osservatorio.

## Technology decisions consigliate

| Macro-componente | Tecnologia consigliata | Motivazione | Alternative | Stato decisione |
|---|---|---|---|---|
| Observatory Control | ASCOM Platform + driver vendor + CPWI | Coerente con manuale esistente e catena di controllo CGX-L | ASCOM Alpaca per integrazioni future | Raccomandazione, AS-IS per ASCOM/CPWI |
| Automation | N.I.N.A. Advanced Sequencer + SOP versionate | Riduce complessita e mantiene controllo nel tool operativo gia documentato | Script PowerShell controllati, orchestratore futuro | Raccomandazione |
| Imaging Processing | PixInsight + ASTAP + manifest file | Standard astrophotography e integrazione con pipeline esistente | Siril, AstroPixelProcessor, astrometry.net | Raccomandazione |
| Scheduler | Target list versionata + generatori piano sessione | Introduzione graduale e verificabile senza backend | N.I.N.A. Scheduler plugin, planner esterni | TO-BE / TBD |
| Data Platform | File system governato + DuckDB/Parquet per analytics | Portabile, locale, adatto a dataset analitici e build statiche | SQLite, PostgreSQL, cloud warehouse | Raccomandazione coerente con ADR-003, da confermare |
| Knowledge Graph | JSON-LD/RDF o Neo4j secondo complessita | Supporta relazioni e query impatto | Markdown registry esteso, SQLite graph tables | TBD, richiede ADR |
| Documentation | MkDocs Material + GitHub | Gia baseline, statico, revisionabile | Docusaurus, Sphinx | AS-IS / Approved baseline |
| User Portal | GitHub Pages / static hosting | Superficie d'attacco ridotta e integrazione con docs | Cloud app dinamica | Raccomandazione |
| API Gateway | Nessun gateway finche non esistono API approvate | Evita overengineering e superfici non necessarie | Cloudflare/API Gateway/Nginx | TBD, non implementare ora |
| Identity & Access | VPN RUT955 + GitHub permissions + secret vault esterno | Coerente con rete esistente e governance segreti | Tailscale, WireGuard, cloud IAM | Da valutare con ADR se cambia accesso |
| Notification | GitHub Issues/email/servizio messaging approvato | Tracciabilita e semplicità iniziale | Slack, Telegram, webhook, SMS | TBD |
| Monitoring | Export log locale + dashboard health statica | Basso impatto su EAGLE e utile per readiness | Prometheus/Grafana, Uptime Kuma | Raccomandazione graduale |
| Logging | File log centralizzati + correlation index | Rispetta strumenti Windows/app esistenti | ELK/OpenSearch, Loki | TBD per scala futura |
| Backup & Recovery | 3-2-1 adattato + manifest hash + restore test | Riduce rischio perdita dati e deriva documentale | Cloud-only, NAS-only, offline-only | Raccomandazione |
| AI | OpenAI API o provider approvato con retrieval controllato | Forte capacita per sintesi e analisi documentale | Modello locale, altro provider cloud | TBD, governance richiesta |

## Roadmap implementativa

| Milestone | Titolo | Obiettivo | Deliverable verificabili | Dipendenze | Criterio di completamento |
|---|---|---|---|---|---|
| `DSG-IMP-M1` | Architecture Readiness | Rendere approvabile il blueprint e mappare TBD | Blueprint pubblicato, elenco TBD, eventuali ADR candidate | Baseline DSG-MR-001 | Review architetturale senza violazioni freeze |
| `DSG-IMP-M2` | Session Manifest and Data Catalog | Definire manifest sessione e catalogo dataset minimo | Schema manifest, template catalogo, esempi sanitizzati | M1, Data Governance | Una sessione storica catalogabile end-to-end |
| `DSG-IMP-M3` | Logging and Observability Baseline | Correlare log e metriche minime per sessione | Log inventory, severity model, health checklist | M2, Monitoring | Timeline sessione ricostruibile da evidenze |
| `DSG-IMP-M4` | Backup and Restore Evidence | Formalizzare backup classi dati e prove restore | Backup matrix, restore report template, RTO/RPO proposti | M2 | Restore test documentato per almeno un dataset campione |
| `DSG-IMP-M5` | Analytics Quality Expansion | Collegare catalogo e log ai KPI dashboard | Dataset curato, KPI definitions, dashboard evidence | M2, M3 | Dashboard con fonte, stato qualita e data refresh |
| `DSG-IMP-M6` | Scheduler Readiness | Definire target backlog e piano sessione verificabile | Target registry, session plan template, readiness rules | M2, M3 | Piano sessione generabile senza comando diretto hardware |
| `DSG-IMP-M7` | Knowledge Graph Prototype Governance | Approvare modello semantico e scope KG | Ontology draft, mapping documenti, ADR se necessario | M1-M5 | Query impatto dimostrabile su documenti/registri campione |
| `DSG-IMP-M8` | AI Assisted Operations Governance | Approvare use case AI non safety e audit | Use case register, prompt policy, review workflow | M7, AI Governance | Output AI collegato a fonti e revisione umana |
| `DSG-IMP-M9` | Notification and Incident Loop | Integrare alert non safety con incident evidence | Alert matrix, escalation log, incident template | M3, M4 | Alert test produce notifica e record tracciato |
| `DSG-IMP-M10` | Release and Business Continuity Gate | Consolidare readiness release e continuity | Release checklist, continuity runbook, follow-up register | M1-M9 | Release architetturale verificata con build e link check |

## Indipendenza e verificabilita delle milestone

- Ogni milestone produce documenti o evidenze verificabili senza richiedere sviluppo applicativo obbligatorio.
- Le milestone M2-M4 possono procedere anche senza AI, Knowledge Graph o API Gateway.
- M7 e M8 restano bloccate da governance dedicata e non devono anticipare implementazioni operative.
- Ogni milestone deve aggiornare registri e release evidence solo dopo review.

## Validazione contro baseline

| Fonte baseline | Verifica | Esito |
|---|---|---|
| `DSG-MR-001` | I domini derivano da Observatory, Operations, Data, Analytics, AI, Documentation, Knowledge, Security e DR | Coerente |
| `DSG-EAM-001` | I macro-componenti rispettano meta-modello Roadmap -> Domain -> Capability -> Component -> Evidence | Coerente |
| `DSRA-000` | AS-IS / Transition / TO-BE sono distinti, AI e KG restano TO-BE/TBD | Coerente |
| `DSRA-001` | PC Principale ed EAGLE mantengono responsabilita separate | Coerente |
| ADR approvati | Non sono stati modificati; ADR-002/ADR-003/DSG-ADR-004 sono richiamati come baseline | Coerente |
| Governance | Freeze policy rispettata; nuove capability sono raccomandazioni o TBD | Coerente |
| Architecture Principles | Roadmap-first, evidence-based, safety boundary, separation of concerns applicati | Coerente |
| Roadmap Freeze Policy | Nessun nuovo programma o piattaforma dichiarata implementata fuori roadmap | Coerente |

## Quality gate proposti

| ID | Gate | Check |
|---|---|---|
| `QG-ESB-ARCH` | Coerenza architetturale | Tutti i componenti mappano a roadmap e baseline |
| `QG-ESB-DATA` | Lineage dati | Ogni flusso indica fonte, output, controlli e owner logico |
| `QG-ESB-SEC` | Sicurezza | Nessun segreto, endpoint sensibile o credenziale pubblicata |
| `QG-ESB-OPS` | Operabilita | Nessun componente remoto e prerequisito per safety locale |
| `QG-ESB-REL` | Release readiness | Navigazione MkDocs aggiornata, link relativi coerenti, TBD espliciti |

## TBD consolidati

| ID | Elemento | Area | Priorita |
|---|---|---|---|
| `DSG-ESB-TBD-001` | Contratti telemetria e session manifest | Data / Monitoring | Alta |
| `DSG-ESB-TBD-002` | RTO/RPO numerici per classi dati | Backup & Recovery | Alta |
| `DSG-ESB-TBD-003` | Provider e policy cloud storage | Storage / Security | Media |
| `DSG-ESB-TBD-004` | Modello Knowledge Graph e storage | Knowledge | Media |
| `DSG-ESB-TBD-005` | Use case AI, modello, retention e audit | AI / Governance | Media |
| `DSG-ESB-TBD-006` | Canali notification ed escalation | Operations | Media |
| `DSG-ESB-TBD-007` | Scheduler rules e target registry definitivo | Scheduler | Media |
| `DSG-ESB-TBD-008` | Standard integrazione TNS/AAVSO | Scientific publication | Bassa |

## Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md)
- [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md)
- [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md)
- [Governance](../enterprise/governance.md)
- [ADR Index](../enterprise/adr/index.md)
- [Gestione dati e archiviazione](../chapters/28-gestione-dati-archiviazione.md)
- [Computer EAGLE](../chapters/06-eagle.md)
- [Infrastruttura di rete](../chapters/05-infrastruttura-rete.md)
