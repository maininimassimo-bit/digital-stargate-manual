# DSG-ESB-001 - Enterprise Solution Blueprint

| Campo | Valore |
|---|---|
| Documento | Enterprise Solution Blueprint |
| Identificativo | `DSG-ESB-001` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Owner | Massimo Mainini |
| Data | 2026-07-26 |
| Fonte gerarchica | `DSG-MR-001` |
| Baseline correlate | `DSG-EAM-001`, `DSRA-000`, `DSRA-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## Scopo

Questo documento definisce il blueprint tecnico complessivo della piattaforma Digital StarGate. Traduce la baseline enterprise in una vista di soluzione che identifica macro-componenti, responsabilita, relazioni, confini operativi, dipendenze e vincoli di evoluzione.

Il blueprint non implementa software, backend, frontend, API o database. Le tecnologie citate sono raccomandazioni architetturali e devono essere formalizzate tramite governance, ADR o roadmap implementativa prima di diventare baseline esecutiva.

## Ambito

In ambito:

- architettura tecnica end-to-end della piattaforma Digital StarGate;
- domini applicativi e container logici;
- flussi dati principali;
- integrazioni esterne previste;
- requisiti non funzionali;
- modello di deployment locale/remoto;
- raccomandazioni tecnologiche;
- milestone implementative verificabili.

Fuori ambito:

- sviluppo applicativo;
- implementazione di API, servizi, database o UI;
- modifica della roadmap congelata `DSG-MR-001`;
- modifica di `DSG-EAM-001`, `DSRA-000`, `DSRA-001`, ADR approvati o Governance, salvo riferimenti futuri strettamente necessari;
- pubblicazione di credenziali, indirizzi sensibili, chiavi, token o configurazioni private.

## Posizionamento nella baseline enterprise

| Documento | Relazione con il blueprint |
|---|---|
| [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Fonte gerarchica e perimetro congelato |
| [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md) | Meta-modello di domini, capability, componenti ed evidenze |
| [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md) | Visione target AS-IS / Transition / TO-BE |
| [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) | Reference architecture operativa PC Principale / EAGLE |
| [Governance](../enterprise/governance.md) | Freeze policy, quality gate, change management e security governance |
| [DSRA Risk Assessment](../enterprise/DSRA-risk-assessment.md) | Rischi, controlli e mitigazioni enterprise |
| [ADR Index](../enterprise/adr/index.md) | Registro delle decisioni approvate e criteri per ADR futuri |

## Principi architetturali

| ID | Principio | Applicazione nel blueprint |
|---|---|---|
| `DSG-ESB-PRN-001` | Roadmap-first | Ogni componente deve mappare a `DSG-MR-001` |
| `DSG-ESB-PRN-002` | Operational separation | EAGLE governa le operazioni sul campo; PC Principale governa engineering, documentazione, analytics e release |
| `DSG-ESB-PRN-003` | Safety boundary | AI, automation remota e dashboard non comandano funzioni safety senza controlli approvati |
| `DSG-ESB-PRN-004` | Evidence and lineage | Dati, immagini, log e decisioni devono essere collegabili a sessioni, sorgenti e controlli |
| `DSG-ESB-PRN-005` | Local-first operations | L'osservatorio deve poter raggiungere uno stato sicuro anche in caso di perdita cloud o VPN |
| `DSG-ESB-PRN-006` | Progressive enablement | Le capability TO-BE vengono abilitate per milestone indipendenti e verificabili |
| `DSG-ESB-PRN-007` | Secure by default | Nessuna credenziale o configurazione sensibile nel repository; accessi remoti governati da VPN e IAM |

## Macro-componenti della piattaforma

| ID | Macro-componente | Responsabilita | Nodo primario | Stato architetturale |
|---|---|---|---|---|
| `DSG-MC-OBS` | Observatory Control | Strumentazione, cupola/tetto, montatura, camere, fuoco, alimentazioni e stato campo | EAGLE / componenti locali | AS-IS / Transition |
| `DSG-MC-AUT` | Automation Orchestration | Sequenze, pre-check, acquisizione, recovery operativo, sincronizzazioni | EAGLE | Transition |
| `DSG-MC-IMG` | Imaging Pipeline | FITS, calibrazione, elaborazione, prodotti finali e quality assessment immagini | EAGLE + PC Principale | Transition |
| `DSG-MC-SCH` | Scheduler | Pianificazione sessioni, finestre meteo, priorita target e readiness | PC Principale + EAGLE | TO-BE / Da validare |
| `DSG-MC-DAT` | Data Platform | Storage osservativo, warehouse, data catalog, lineage, retention | PC Principale / Storage | Transition |
| `DSG-MC-KG` | Knowledge Graph | Modello semantico di asset, osservazioni, documenti, decisioni e rischi | PC Principale / Cloud | TO-BE / TBD |
| `DSG-MC-AI` | AI Assistance | Analisi assistita, sintesi, classificazione, supporto troubleshooting non safety | PC Principale / Cloud | TO-BE / TBD |
| `DSG-MC-ANL` | Analytics and Dashboard | KPI, dashboard, report, quality gates e trend | PC Principale / GitHub Pages | AS-IS / Transition |
| `DSG-MC-DOC` | Documentation Platform | MkDocs, handbook, SOP, ADR, registri, release documentation | PC Principale / GitHub | AS-IS / Transition |
| `DSG-MC-PORTAL` | User Portal | Pubblicazione documentale, consultazione dashboard, stato e contenuti divulgativi | GitHub Pages / Cloud | AS-IS / Transition |
| `DSG-MC-INT` | Integration Layer | Contratti logici con N.I.N.A., ASCOM, CPWI, PHD2, AllSky, meteo e servizi esterni | EAGLE + PC Principale | Transition |
| `DSG-MC-SEC` | Identity and Access | VPN, account, permessi, segreti, autorizzazioni e audit accessi | RUT955 / GitHub / Cloud | Transition |
| `DSG-MC-OPS` | Monitoring, Logging and Alerting | Log applicativi, eventi rete, metriche operative, notifiche, incident evidence | EAGLE + PC Principale | Transition |
| `DSG-MC-BRC` | Backup, Recovery and Continuity | Copie, restore test, disaster recovery, readiness e continuita | Storage locale + remoto | Transition |

## Relazioni principali

```text
Operatori / Maintainer
        |
        v
User Portal / Documentation / Dashboard
        |
        v
PC Principale -- GitHub -- Cloud Storage / Remote Services
        |
        v
VPN / Remote Access / RUT955
        |
        v
EAGLE -- N.I.N.A. -- ASCOM -- CPWI -- CGX-L
  |          |         |        
  |          |         +-- PHD2 / guiding
  |          +-- camera / focuser / filter wheel / solver
  +-- local storage / logs / telemetry / sync
        |
        v
Data Platform -> Analytics -> Knowledge Graph -> AI Assistance
        |
        v
Backup / Archive / Publication
```

La relazione e logica. Non implica un bus applicativo implementato, un database operativo o API gia disponibili.

## Vista AS-IS / Transition / TO-BE

| Area | AS-IS | Transition | TO-BE |
|---|---|---|---|
| Operazioni campo | EAGLE, N.I.N.A., CPWI, PHD2, ASCOM e procedure documentate | Controlli readiness, logging e sync tracciati | Operazioni orchestrate con evidenze complete e safety gate |
| Dati osservativi | FITS, log, report e archiviazione documentata | Data catalog, lineage, quality gates e retention | Data platform scientifica governata e interrogabile |
| Analytics | Dashboard e warehouse documentati | KPI consolidati e controlli qualita | Dashboard operative e direzionali con trend affidabili |
| Knowledge | Manuale MkDocs e registri | Mapping semantico preliminare | Knowledge Graph interrogabile e versionato |
| AI | Ambito previsto ma non operativo | Use case e guardrail approvati | AI assistiva auditabile, non autonoma su safety |
| Portal | MkDocs e contenuti pubblicati | Navigazione enterprise estesa | Portale unico per manuale, dashboard e release evidence |
| Continuity | Backup e recovery documentati | Restore test e classificazione dati | Business continuity misurabile con RTO/RPO validati |

## Mappa di tracciabilita macro-componenti

| Macro-componente | Roadmap | Baseline | Evidenza esistente o attesa |
|---|---|---|---|
| `DSG-MC-OBS` | Observatory, Operations | `DSRA-001` | Capitoli osservatorio, EAGLE, strumenti |
| `DSG-MC-AUT` | Automation, Live Operations | `DSRA-000`, `DSRA-001` | SOP avvio, acquisizione, chiusura, recovery |
| `DSG-MC-IMG` | Image and Scientific Repository | `DSG-MR-001` | Capitolo gestione dati, pipeline processing |
| `DSG-MC-SCH` | Operations / Live Operations | `DSRA-000` | `TBD`, richiede validazione requisiti |
| `DSG-MC-DAT` | Data | `ADR-003`, Data Governance | Warehouse, dataset, schema, quality gate |
| `DSG-MC-KG` | Knowledge | `DSRA-000`, `DSRA-001` | `TBD`, modello semantico futuro |
| `DSG-MC-AI` | AI | Governance AI | `TBD`, use case approvati richiesti |
| `DSG-MC-ANL` | Analytics and Reporting | `ADR-002` | Dashboard, KPI, validation |
| `DSG-MC-DOC` | Documentation | `DSG-ADR-004` | MkDocs, registri, SOP, handbook |
| `DSG-MC-PORTAL` | Documentation / Community | Governance release | GitHub Pages / portale documentale |
| `DSG-MC-SEC` | Security | Governance Security | VPN, account, policy segreti |
| `DSG-MC-OPS` | Operations / Security | DSRA Risk Assessment | Log, monitoraggio, alert, incident evidence |
| `DSG-MC-BRC` | Disaster Recovery | Governance DR | Backup, restore, continuity evidence |

## Documenti della sezione

- [System Decomposition](system-decomposition.md): domini applicativi, confini, container logici e protocolli.
- [Data Flow and Integrations](data-flow-integrations.md): flussi dati principali e integrazioni esterne previste.
- [NFR, Deployment and Roadmap](nfr-deployment-roadmap.md): requisiti non funzionali, deployment model, technology decisions, milestone e validazione.

## Elementi TBD

| ID | Elemento | Motivazione | Governance richiesta |
|---|---|---|---|
| `DSG-ESB-TBD-001` | Contratti telemetria EAGLE -> PC Principale | Non risultano ancora baseline tecniche complete | Assessment + eventuale ADR |
| `DSG-ESB-TBD-002` | Modello dati Knowledge Graph | Capability TO-BE non implementata | AI/Knowledge governance |
| `DSG-ESB-TBD-003` | Scheduler operativo e regole di priorita | Requisiti e safety gate da validare | Architecture governance |
| `DSG-ESB-TBD-004` | RTO/RPO numerici per dataset e servizi | Valori non presenti nella baseline | DR governance |
| `DSG-ESB-TBD-005` | Provider cloud/storage definitivo | Decisione tecnologica non ancora approvata | ADR futuro |
