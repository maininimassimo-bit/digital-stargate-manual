# DSG-ESB-007 - Component Registry

| Campo | Valore |
|---|---|
| Documento | Component Registry |
| Identificativo | `DSG-ESB-007` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Data | 2026-07-27 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Registrare i componenti software e logici della piattaforma Digital StarGate che risultano dalla documentazione esistente o dalla blueprint architecture. Il registro non autorizza nuove implementazioni: identifica responsabilita e lifecycle status.

## Stati lifecycle

| Stato | Significato |
|---|---|
| `AS-IS` | Componente gia documentato come parte dell'osservatorio o del repository |
| `Transition` | Componente logico necessario a governare o completare flussi gia previsti |
| `TO-BE` | Capacita futura prevista dalla roadmap ma non implementata |
| `TBD` | Decisione architetturale aperta |

## Registro componenti

| Identifier | Purpose | Owner | Technology | Interfaces | Input | Output | Dependencies | Lifecycle status | Related documents |
|---|---|---|---|---|---|---|---|---|---|
| `DSG-CMP-EAGLE` | Nodo operativo di controllo osservatorio | Operations Owner | PrimaLuceLab EAGLE / Windows | RDP/VPN, USB, LAN | Profili, sequenze, driver, comandi operativi | FITS, log, stato dispositivi | RUT955, N.I.N.A., CPWI, PHD2, ASCOM | AS-IS | `docs/chapters/06-eagle.md` |
| `DSG-CMP-NINA` | Sequencer acquisizione e orchestrazione sessione | Operations Owner | N.I.N.A. | ASCOM, PHD2, ASTAP, file system | Target, profilo, sequenza, stato device | FITS, log, eventi sequenza | EAGLE, ASCOM, CPWI, PHD2, camere | AS-IS | `docs/chapters/11-nina.md`, `docs/chapters/17-acquisizione-automatica.md` |
| `DSG-CMP-ASCOM` | Middleware dispositivi astronomici | Engineering Owner | ASCOM Platform | COM/driver, Alpaca TBD | Comandi device, profili driver | Stato device, controllo mount/camera/focuser/filter wheel | EAGLE, driver vendor, CPWI | AS-IS | `docs/chapters/14-ascom.md` |
| `DSG-CMP-CPWI` | Controllo diretto montatura CGX-L | Operations Owner | Celestron CPWI | ASCOM Telescope, USB mount | Park/Unpark, slew, tracking | Stato montatura, disponibilita driver | CGX-L, EAGLE, ASCOM | AS-IS | `docs/chapters/13-cpwi.md`, `docs/chapters/07-cgx-l.md` |
| `DSG-CMP-PHD2` | Autoguida e dithering | Operations Owner | PHD2 Guiding | ASCOM mount, camera guida, N.I.N.A. | Stella guida, profilo, comandi dither | Correzioni guida, log, RMS | EAGLE, ASCOM, CPWI, camera guida | AS-IS | `docs/chapters/12-phd2.md` |
| `DSG-CMP-ASTAP` | Plate solving locale | Operations Owner | ASTAP | N.I.N.A. solver integration | Frame solve, coordinate iniziali | Coordinate risolte, errore puntamento | N.I.N.A., database stellare | AS-IS | `docs/chapters/11-nina.md`, `docs/chapters/17-acquisizione-automatica.md` |
| `DSG-CMP-PI` | Elaborazione immagini astronomiche | Imaging Owner | PixInsight | File FITS/XISF/export | Raw, calibrazioni, registered frames | Master, integrated, processed images, metriche | Data Platform, Calibration | Transition | `docs/chapters/28-gestione-dati-archiviazione.md` |
| `DSG-CMP-ALLSKY` | Monitoraggio visuale cielo e contesto | Operations Owner | AllSky su Raspberry/equivalente con ASI290MC | HTTP locale/file, LAN/Wi-Fi | Cielo, timestamp, immagini | Immagini correnti, timelapse, evidenza meteo-visiva | Rete osservatorio, storage | AS-IS / Da validare | `docs/chapters/27-sistema-allsky.md` |
| `DSG-CMP-WEATHER` | Stato meteo e sicurezza ambientale | Operations Owner | Weather Station TBD | Sensori/export TBD | Pioggia, vento, umidita, dew point, cloud | SAFE/WARNING/UNSAFE/UNKNOWN, log meteo | Observatory, Automation | Da validare | `docs/chapters/26-monitoraggio-meteo-sicurezza-ambientale.md` |
| `DSG-CMP-RUT955` | Gateway rete, VPN, firewall, failover | Infrastructure Owner | Teltonika RUT955 | VPN, WAN/LAN, LTE, firewall | Stato WAN, VPN, traffico remoto | Accesso EAGLE, log rete, failover | Starlink, SIM1/SIM2, EAGLE | AS-IS / Transition | `docs/chapters/05-infrastruttura-rete.md` |
| `DSG-CMP-STARLINK` | Connettivita primaria | Infrastructure Owner | Starlink router | WAN/LAN verso RUT955 | Connettivita Internet | Link primario | RUT955 | AS-IS / Da validare | `docs/chapters/05-infrastruttura-rete.md` |
| `DSG-CMP-MKDOCS` | Generazione sito documentale | Documentation Owner | MkDocs Material | Markdown, mkdocs.yml | Documenti, nav, asset | Sito statico | GitHub, repository docs | AS-IS | `mkdocs.yml`, `docs/enterprise/release-documentation.md` |
| `DSG-CMP-GITHUB` | Repository, controllo versione e pubblicazione | Documentation Owner | GitHub | Git, PR, Pages, Issues | Markdown, dashboard, release evidence | Branch, commit, sito, issue | MkDocs, PC Principale | AS-IS / Transition | `docs/enterprise/governance.md`, `docs/developer/portal-publication-guidelines.md` |
| `DSG-CMP-WAREHOUSE` | Dataset analytics e query locali | Data Owner | Warehouse engine documentato da ADR-003 | File/SQL locale | Catalogo, KPI, report sessione | Dataset curati, dashboard input | Data Platform, Analytics | Transition | `docs/architecture/ADR-003-Warehouse-Engine.md`, `docs/architecture/warehouse/index.md` |
| `DSG-CMP-ANALYTICS-DASH` | Dashboard e KPI Digital StarGate | Analytics Owner | Dashboard statica / MkDocs assets | Dataset warehouse, HTML/static files | KPI, validation data | Dashboard, trend, quality gate output | Warehouse, Documentation Platform | Transition | `docs/analytics/index.md`, `docs/analytics/dashboard-integrated.md`, `docs/architecture/ADR-002-Analytics-Quality-Gates.md` |
| `DSG-CMP-SESSION-MANIFEST` | Manifest sessione osservativa | Data Owner | Schema TBD, Markdown/JSON/YAML da decidere | File/catalogo | Session plan, FITS, log, meteo, equipment | Lineage sessione, stato archive | N.I.N.A., Data Platform, Archive | TBD | `docs/enterprise-solution-blueprint/data-architecture.md`, `docs/enterprise-solution-blueprint/open-decisions.md` |
| `DSG-CMP-TARGET-REGISTRY` | Registro target osservativi | Science/Operations Owner | Registry TBD | Markdown/CSV/YAML TBD | Target, coordinate, priorita, filtri | Observation Request, Session Plan | Scheduling, Equipment | TBD | `docs/enterprise-solution-blueprint/data-architecture.md` |
| `DSG-CMP-EQUIPMENT-REGISTRY` | Registro configurazioni strumenti | Engineering Owner | Registry documentale | Markdown/registri | Asset, seriali, driver, profili, mapping USB | Configurazioni standard e compatibilita | Equipment, Calibration, Scheduler | Transition | `docs/chapters/10-camere-treno-ottico.md`, `docs/chapters/22-inventario-asset-management.md` |
| `DSG-CMP-OBS-CATALOG` | Catalogo osservazioni e prodotti | Data Owner | Catalogo dati / warehouse TBD | File/warehouse | Session manifest, metadata, processed images | Observation Catalog, KPI, portal data | Data Platform, Warehouse, Archive | Transition / TBD | `docs/chapters/28-gestione-dati-archiviazione.md`, `docs/architecture/warehouse/datasets-and-schema.md` |
| `DSG-CMP-KG` | Relazioni semantiche documenti-dati-asset | Knowledge Owner | Knowledge Graph storage TBD | Query graph TBD, document links | Catalogo, registri, ADR, DSRA, docs | Relazioni, context retrieval, impact map | Data Platform, Documentation Platform | TO-BE / TBD | `docs/enterprise/knowledge-index.md`, `docs/enterprise-architecture/DSRA-000-vision-target-architecture.md` |
| `DSG-CMP-AI` | Assistente AI governato | Governance Owner | OpenAI TBD / provider approvato | HTTPS API, retrieval controllato | Fonti approvate, prompt sanitizzati | Sintesi, analisi, checklist, audit | KG, Documentation, Governance | TO-BE / TBD | `docs/enterprise/governance.md`, `docs/enterprise-solution-blueprint/open-decisions.md` |
| `DSG-CMP-SCIENCE-PORTAL` | Vista pubblica/scientifica delle osservazioni | Science Owner | MkDocs/GitHub Pages | Static pages, catalog links | Processed images, metadata, catalog | Pagine science, pubblicazioni candidate | Documentation, Data Platform | TO-BE / Transition | `docs/enterprise-solution-blueprint/logical-architecture.md` |
| `DSG-CMP-ENGINEERING-PORTAL` | Vista architetturale e tecnica | Engineering Owner | MkDocs/GitHub Pages | Static pages, dashboard | ADR, registri, blueprint, KPI | Manuale tecnico, dashboard engineering | Documentation, Analytics | Transition | `docs/developer/portal-publication-guidelines.md` |
| `DSG-CMP-MAINT-PORTAL` | Vista manutenzione, incident e recovery | Maintenance Owner | MkDocs/GitHub Pages | Static pages, issue/evidence links | Log, backup, incident, asset status | Checklist, runbook, restore evidence | Documentation, Backup, Equipment | Transition | `docs/chapters/18-emergenze-recovery.md`, `docs/chapters/21-backup-disaster-recovery.md` |
| `DSG-CMP-BACKUP` | Backup e restore osservatorio | Infrastructure Owner | Strategia 3-2-1, tool storage TBD | File copy, checksum, restore report | Configurazioni, repository, FITS, log, calibrazioni | Backup set, restore evidence | Storage, GitHub, EAGLE | Transition | `docs/chapters/21-backup-disaster-recovery.md` |
| `DSG-CMP-CLOUD-STORAGE` | Copia off-site / storage remoto | Infrastructure/Data Owner | Cloud Storage TBD | Sync/storage API TBD | Dataset, manifest, backup | Copia remota, restore source | Backup, Data Platform | TBD | `docs/chapters/21-backup-disaster-recovery.md`, `docs/enterprise-solution-blueprint/open-decisions.md` |

## Componenti esclusi o non confermati

| Elemento | Motivo | Stato |
|---|---|---|
| API Gateway generico | Non esiste una API implementata o approvata nella baseline corrente | Registrato come decisione aperta, non come componente operativo |
| Notification platform generica | Canali, destinatari e regole non sono definiti nel repository | Decisione aperta |
| IAM enterprise generico | La baseline documenta VPN, GitHub permissions e segreti fuori repository, non una piattaforma IAM dedicata | Sostituito da Remote Access e Access Governance |
| Monitoring stack generico | Non risultano Prometheus/Grafana o stack equivalenti approvati | Sostituito da session evidence, health checks e dashboard analytics |
| Logging stack generico | Log reali sono N.I.N.A., PHD2, CPWI, ASCOM, Windows, RUT955, AllSky | Sostituito da Session Evidence e Log Correlation |

## Regole di manutenzione del registro

- Aggiornare il registro solo quando un componente e documentato, approvato o richiesto da una decisione aperta.
- Non dichiarare `AS-IS` un componente TO-BE.
- Collegare ogni componente ad almeno un documento sorgente o a una decisione aperta.
- Creare ADR solo quando cambia una scelta strutturale o tecnologica reale.
