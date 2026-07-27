# DSG-ESB-001 - Enterprise Solution Blueprint

| Campo | Valore |
|---|---|
| Documento | Enterprise Solution Blueprint |
| Identificativo | `DSG-ESB-001` |
| Stato | Proposed architecture baseline |
| Versione | 0.2 |
| Owner | Massimo Mainini |
| Data | 2026-07-27 |
| Fonte gerarchica | `DSG-MR-001` |
| Baseline correlate | `DSG-EAM-001`, `DSRA-000`, `DSRA-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## Scopo

Questo blueprint descrive la piattaforma reale Digital StarGate: un osservatorio astronomico remoto governato da EAGLE, N.I.N.A., CPWI, PHD2, ASCOM, ASTAP, montatura Celestron CGX-L, ottiche C8 XLT e Sky-Watcher Quattro 200P, camere astronomiche, AllSky, monitoraggio meteo, rete RUT955/Starlink/VPN, repository documentale MkDocs, data platform, analytics e archiviazione osservativa.

Il documento non crea software, backend, frontend, API o database. Quando una informazione non e tracciabile alla documentazione esistente, viene registrata in [Open Architectural Decisions](open-decisions.md).

## Ambito

In ambito:

- architettura funzionale dell'osservatorio automatizzato;
- domini osservativi, strumentali, dati, processing, portali e conoscenza;
- lifecycle dei dati astronomici;
- component registry e integration catalog;
- requisiti non funzionali e deployment model;
- decisioni architetturali aperte.

Fuori ambito:

- modifica della roadmap `DSG-MR-001`;
- modifica di `DSG-EAM-001`, `DSRA-000`, `DSRA-001`, ADR approvati o Governance;
- introduzione di prodotti non presenti nel repository;
- pubblicazione di segreti, indirizzi sensibili, token o configurazioni private.

## Posizionamento nella baseline enterprise

| Documento | Relazione con il blueprint |
|---|---|
| [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Fonte gerarchica e perimetro congelato |
| [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md) | Meta-modello di domini, capability, componenti ed evidenze |
| [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md) | Visione target AS-IS / Transition / TO-BE |
| [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) | Separazione PC Principale / EAGLE |
| [Governance](../enterprise/governance.md) | Freeze policy, quality gate, change management e security governance |
| [ADR Index](../enterprise/adr/index.md) | Decisioni approvate e candidate ADR future |

## Principi architetturali applicati

| ID | Principio | Applicazione Digital StarGate |
|---|---|---|
| `DSG-ESB-PRN-001` | Observatory-first | La piattaforma e modellata intorno alla sessione osservativa e alla sicurezza dell'osservatorio, non intorno a componenti enterprise generici. |
| `DSG-ESB-PRN-002` | EAGLE operational boundary | EAGLE resta il nodo operativo per N.I.N.A., CPWI, PHD2, ASCOM, ASTAP, dispositivi e acquisizione. |
| `DSG-ESB-PRN-003` | PC Principale engineering boundary | PC Principale governa documentazione, GitHub, MkDocs, processing, analytics, release e architettura. |
| `DSG-ESB-PRN-004` | Single device control path | La montatura CGX-L e controllata direttamente da CPWI; N.I.N.A. e PHD2 passano da ASCOM. |
| `DSG-ESB-PRN-005` | Safety before automation | Meteo UNKNOWN o incoerente non autorizza apertura; AI e portali non comandano safety. |
| `DSG-ESB-PRN-006` | FITS lineage | Raw images, calibrazioni, session manifest, catalogo e archive devono restare collegati. |
| `DSG-ESB-PRN-007` | Evidence-based architecture | Ogni statement architetturale deve rimandare a capitoli, ADR, governance o open decisions. |

## Macro-capability Digital StarGate

| ID | Capability | Responsabilita | Nodo primario | Stato |
|---|---|---|---|---|
| `DSG-CAP-OBS` | Observatory Readiness and Safety | Stato osservatorio, meteo, copertura, rete, EAGLE, Park/Unpark e condizioni SAFE | EAGLE / campo | AS-IS / Transition |
| `DSG-CAP-EQP` | Equipment Control and Configuration | CGX-L, C8, Quattro, camere, filtri, fuocheggiatori, flat panel, profili e mapping hardware | EAGLE / documentazione tecnica | AS-IS / Transition |
| `DSG-CAP-SES` | Observation Session Management | Avvio, sequenza, log, eventi, report sessione e chiusura dati | EAGLE | Transition |
| `DSG-CAP-SCH` | Observation Scheduling | Target, finestre, priorita, readiness, profilo ottico e piano sessione | PC Principale / EAGLE | TO-BE / Decisione aperta |
| `DSG-CAP-CAL` | Calibration Management | Dark, flat, bias, dark-flat, master calibration e validita librerie | EAGLE + PC Principale | Transition |
| `DSG-CAP-ACQ` | Image Acquisition | FITS raw, header, naming, guida, solve, autofocus, dithering e meridian flip | EAGLE | AS-IS / Transition |
| `DSG-CAP-PROC` | Image Processing | Calibrazione, registrazione, integrazione, processing, metriche e export | PC Principale | Transition |
| `DSG-CAP-DATA` | Astronomical Data Platform | Session manifest, catalogo osservazioni, warehouse, metadata, lineage e quality gates | PC Principale / Storage | Transition |
| `DSG-CAP-ARCH` | Observation Archive and Recovery | Raw, processed, configurazioni, log, copie, restore evidence e retention | Storage locale/remoto | Transition |
| `DSG-CAP-KG` | Knowledge Graph | Relazioni tra target, sessioni, asset, documenti, ADR, rischi e dataset | PC Principale | TO-BE / Decisione aperta |
| `DSG-CAP-AI` | AI Assistant | Supporto documentale e analisi non safety su fonti approvate | PC Principale / provider approvato | TO-BE / Decisione aperta |
| `DSG-CAP-DOC` | Documentation Platform | MkDocs, manuale, SOP, ADR, registri, release evidence | PC Principale / GitHub | AS-IS / Transition |
| `DSG-CAP-ANL` | Analytics | KPI, dashboard, quality gate, validation history e trend | PC Principale / GitHub Pages | AS-IS / Transition |
| `DSG-CAP-SCI` | Science Portal | Pubblicazione osservazioni, immagini finali, metadati e contenuti scientifici validati | MkDocs / GitHub Pages | TO-BE / Transition |
| `DSG-CAP-ENG` | Engineering Portal | Architettura, registri, dashboard tecniche, release e publication guidelines | MkDocs / GitHub Pages | Transition |
| `DSG-CAP-MNT` | Maintenance Portal | Manutenzione, incident, recovery, backup, asset e obsolescenza | MkDocs / GitHub Pages | Transition |
| `DSG-CAP-REMOTE` | Remote Access and Network Continuity | VPN, RUT955, Starlink, LTE failover, desktop remoto e log rete | RUT955 / EAGLE | AS-IS / Transition |

## Concetti generici sostituiti

| Concetto precedente | Trattamento nel blueprint raffinato |
|---|---|
| API Gateway | Non e una capability operativa attuale. Rimane decisione aperta `DSG-OAD-025` solo se emergera un caso d'uso reale. |
| Identity & Access | Sostituito da `DSG-CAP-REMOTE`: VPN RUT955, account GitHub, segreti fuori repository e access governance. |
| Notification | Sostituito da evidenze di sessione, incident/recovery e decisione aperta sui canali di escalation. |
| Monitoring | Sostituito da Observatory Readiness, meteo SAFE/UNSAFE, log sessione, dashboard analytics e health evidence. |
| Logging | Sostituito da log reali N.I.N.A., PHD2, CPWI, ASCOM, Windows, RUT955, AllSky e correlazione sessione. |
| Backup | Sostituito da Observation Archive and Recovery, coerente con dati FITS, configurazioni, repository e restore evidence. |

## Relazione logica principale

```text
Operatore / Maintainer
  -> Science Portal / Engineering Portal / Maintenance Portal
  -> Scheduling
  -> Observation Session Management
  -> N.I.N.A.
  -> ASCOM / CPWI / PHD2 / ASTAP
  -> CGX-L / camere / fuocheggiatori / filtri / AllSky / meteo
  -> Image Acquisition
  -> Astronomical Data Platform
  -> Image Processing
  -> Observation Catalog / Archive
  -> Knowledge Graph / AI Assistant
  -> Documentation Platform / Analytics
```

## Vista AS-IS / Transition / TO-BE

| Area | AS-IS | Transition | TO-BE |
|---|---|---|---|
| Operazioni campo | EAGLE, N.I.N.A., CPWI, PHD2, ASCOM, ASTAP e procedure | Session manifest, evidence e readiness consolidati | Session management tracciato end-to-end |
| Equipment | CGX-L, C8, Quattro, QHY/ToupTek, filtri, fuocheggiatori documentati | Equipment Registry e configurazioni standard | Scheduling basato su configurazione verificata |
| Dati osservativi | FITS, log, report e archiviazione | Catalogo osservazioni, lineage e quality gates | Data platform astronomica interrogabile |
| Processing | PixInsight e workflow documentati in termini architetturali | Metriche e processing evidence | Pipeline ripetibile e collegata a catalogo |
| Portali | MkDocs e analytics pubblicabili | Science/Engineering/Maintenance Portal come viste logiche | Esperienza integrata senza introdurre app dinamiche non approvate |
| Knowledge/AI | Previsti ma non implementati | Open decisions e governance | KG e AI Assistant auditabili e non safety |

## Documenti della sezione

- [Component Registry](component-registry.md): componenti software/logici reali e lifecycle status.
- [Astronomical Data Architecture](data-architecture.md): lifecycle completo dei dati astronomici.
- [Data Flow and Integrations](data-flow-integrations.md): flussi dati principali e integrazioni.
- [Integration Catalog](integration-catalog.md): protocolli, failure mode e recovery delle integrazioni.
- [Logical Architecture](logical-architecture.md): functional architecture e diagrammi logici.
- [NFR, Deployment and Roadmap](nfr-deployment-roadmap.md): requisiti non funzionali, deployment e milestone.
- [Open Architectural Decisions](open-decisions.md): backlog delle decisioni non finalizzate.
- [System Decomposition](system-decomposition.md): decomposizione precedente mantenuta come vista di container logici, da leggere insieme ai nuovi registri.

## Tracciabilita minima

| Capability | Documenti sorgente principali |
|---|---|
| Observatory Readiness and Safety | `docs/chapters/05-infrastruttura-rete.md`, `docs/chapters/16-sop-avvio.md`, `docs/chapters/26-monitoraggio-meteo-sicurezza-ambientale.md` |
| Equipment Control and Configuration | `docs/chapters/07-cgx-l.md`, `docs/chapters/08-c8-xlt.md`, `docs/chapters/09-quattro-200p.md`, `docs/chapters/10-camere-treno-ottico.md` |
| Observation Session Management | `docs/chapters/11-nina.md`, `docs/chapters/12-phd2.md`, `docs/chapters/13-cpwi.md`, `docs/chapters/14-ascom.md`, `docs/chapters/17-acquisizione-automatica.md` |
| Astronomical Data Platform | `docs/chapters/28-gestione-dati-archiviazione.md`, `docs/architecture/ADR-003-Warehouse-Engine.md`, `docs/architecture/warehouse/datasets-and-schema.md` |
| Documentation and Analytics | `mkdocs.yml`, `docs/analytics/index.md`, `docs/enterprise/release-documentation.md`, `docs/developer/portal-publication-guidelines.md` |
| Backup and Recovery | `docs/chapters/21-backup-disaster-recovery.md`, `docs/chapters/18-emergenze-recovery.md` |

## Open Architectural Decisions

Le informazioni non finalizzate sono consolidate in [Open Architectural Decisions](open-decisions.md). Questo blueprint non assegna risposte definitive a scheduler, manifest, target registry, equipment registry completo, cloud storage, Knowledge Graph, AI Assistant, TNS/AAVSO o ASCOM Alpaca.
