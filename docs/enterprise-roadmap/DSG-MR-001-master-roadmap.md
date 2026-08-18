# DSG-MR-001 - Digital StarGate Master Roadmap

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Master Roadmap |
| Identificativo | DSG-MR-001 |
| Stato | Approved |
| Versione | 1.0 |
| Owner | TBD |
| Data | 2026-07-26 |
| Ambito | Baseline enterprise Digital StarGate |

## Riferimenti gerarchici

- Fonte gerarchica principale: questo documento.
- Policy di congelamento: [DSG-GOV-001 - Roadmap Freeze Policy](../enterprise/governance.md#dsg-gov-001---roadmap-freeze-policy).
- Architettura derivata: [DSG-EAM-001 - Enterprise Architecture Meta Model](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), [DSRA-000 - Vision Target Architecture](../enterprise-architecture/DSRA-000-vision-target-architecture.md), [DSRA-001 - Reference Architecture](../enterprise-architecture/DSRA-001-reference-architecture.md).
- Portfolio, registri e governance: [Enterprise Program Portfolio](../enterprise/program-portfolio.md), [Registri e tracciabilità](../enterprise/registries/index.md), [Governance](../enterprise/governance.md).
- Documentazione tecnica e operativa esistente: sezioni MkDocs `Architettura`, `Observatory`, `Generalità`, `Infrastruttura`, `Automazione`, `Governance e continuità`, `Operations avanzate`, `Analytics`, `Developer`, `Release Notes`.

## Uso del documento

DSG-MR-001 definisce la roadmap master del programma Digital StarGate. È il documento di riferimento per priorità, ambiti, dipendenze e governance della documentazione enterprise.

La roadmap non sostituisce i manuali tecnici esistenti: li organizza in un modello enterprise, evidenziando stato attuale, transizione e target atteso. Le informazioni tecniche non presenti nella documentazione esistente sono marcate come `TBD` o `Da validare`.

---

# PART I - Enterprise Foundation

## 1 Executive Summary

Digital StarGate è un programma enterprise per consolidare, governare ed evolvere l'osservatorio remoto, la piattaforma documentale, i dati operativi, le dashboard, l'analytics, l'AI e la conoscenza strutturata.

La roadmap 2026-2030 stabilisce un modello unico per:

- mantenere tracciabilità tra documenti, decisioni, rischi, controlli e release;
- distinguere ciò che è già operativo da ciò che è in transizione o target;
- evitare duplicazioni documentali;
- governare evoluzioni architetturali senza introdurre componenti non approvati;
- collegare le attività su PC Principale e EAGLE in un modello operativo coerente.

## 2 Vision

Costruire una piattaforma Digital StarGate governata, documentata e verificabile, capace di supportare osservazione remota, automazione, gestione dati, analytics, AI, knowledge graph e comunicazione verso stakeholder tecnici e community.

## 3 Mission

Fornire un sistema documentale e operativo che permetta di:

- comprendere lo stato dell'osservatorio e della piattaforma;
- pianificare evoluzioni senza perdere controllo configurativo;
- supportare operazioni affidabili e ripetibili;
- valorizzare dati, immagini, metriche e conoscenza prodotta;
- abilitare release documentali e software verificabili.

## 4 Core Values

- **Sicurezza operativa**: la protezione dell'osservatorio e delle persone prevale su automazione e continuità di servizio.
- **Tracciabilità**: decisioni, modifiche, asset, configurazioni e rischi devono essere collegabili.
- **Evidenza**: ogni affermazione tecnica rilevante deve derivare da documenti, registri o validazioni.
- **Evoluzione controllata**: nuove capacità passano da governance, assessment e quality gate.
- **Semplicità sostenibile**: la documentazione deve essere utile, navigabile e mantenibile.

## 5 Guiding Principles

- La roadmap congelata guida priorità e perimetro.
- I documenti esistenti sono aggiornati prima di crearne di nuovi.
- AS-IS, Transition e TO-BE devono rimanere distinguibili.
- I dati tecnici non confermati sono marcati `TBD` o `Da validare`.
- I riferimenti usano link Markdown relativi.
- Le decisioni architetturali sono registrate tramite ADR solo quando esiste una decisione reale.

## 6 Strategic Objectives

| ID | Obiettivo | Stato |
|---|---|---|
| SO-01 | Consolidare la Master Roadmap enterprise | Approvato |
| SO-02 | Pubblicare baseline architetturale DSG-EAM/DSRA | Approvato |
| SO-03 | Governare portfolio, registri e processi enterprise | Approvato |
| SO-04 | Completare baseline documentale ADR, assessment, SOP, handbook e release | In corso |
| SO-05 | Preparare evoluzione 2026-2030 | Da validare |

## 7 Enterprise Scope

In ambito:

- Observatory;
- Infrastructure;
- Operations;
- Data;
- Image and Scientific Repository;
- Analytics and Reporting;
- Live Operations;
- AI;
- Documentation;
- Knowledge;
- Community;
- Security;
- Engineering Governance;
- Asset and Configuration Management.

Fuori ambito fino a nuova approvazione:

- nuovi programmi non presenti in questa roadmap;
- nuove piattaforme non registrate;
- configurazioni tecniche non documentate;
- decisioni architetturali non formalizzate.

## 8 Success Criteria

| Criterio | Evidenza attesa |
|---|---|
| Roadmap pubblicata | Documento DSG-MR-001 navigabile in MkDocs |
| Architettura enterprise pubblicata | DSG-EAM-001, DSRA-000, DSRA-001 |
| Portfolio e registri disponibili | Documenti enterprise collegati |
| Governance documentata | Processi e quality gate pubblicati |
| Baseline operativa completata | SOP, handbook, release, assessment e knowledge index |
| Build MkDocs verificabile | `mkdocs build --strict` su PC Principale o GitHub Actions |

## 9 Governance Principles

- Ogni cambiamento rilevante deve essere tracciato.
- Le modifiche alla roadmap congelata richiedono processo di change management.
- I registri enterprise sono fonti di controllo, non appendici decorative.
- La documentazione pubblicata deve essere verificabile tramite build e link check.

## 10 Roadmap Governance

La roadmap è soggetta a DSG-GOV-001. Qualsiasi variazione di programma, dominio, piattaforma o decisione architetturale deve essere:

1. proposta;
2. valutata rispetto a impatti e rischi;
3. registrata nei documenti appropriati;
4. approvata prima della pubblicazione come baseline.

---

# PART II - Enterprise Architecture

## 11 AS-IS

Lo stato AS-IS include documentazione tecnica e operativa già presente nel manuale MkDocs:

- capitoli infrastrutturali e astronomici;
- procedure operative esistenti;
- documentazione analytics e warehouse;
- ADR tecnici esistenti in `architecture/`;
- assessment tecnici esistenti;
- release note UI esistente;
- contenuti relativi a PC Principale ed EAGLE.

Le informazioni AS-IS non confermate sono considerate `Da validare`.

## 12 Transition

La fase Transition consolida la documentazione in una baseline enterprise:

- roadmap master;
- meta-modello architetturale;
- reference architecture;
- portfolio programmi;
- registri enterprise;
- governance;
- ADR index;
- assessment consolidati;
- SOP;
- handbook;
- release documentation;
- knowledge index e traceability matrix.

## 13 TO-BE

Lo stato TO-BE prevede una piattaforma integrata, governata e misurabile, con:

- osservatorio remoto documentato end-to-end;
- flussi dati e repository scientifico tracciabili;
- dashboard analytics e live operations governate;
- AI e Knowledge Graph soggetti a governance;
- release e change management ripetibili;
- documentazione MkDocs come fonte pubblicabile e revisionabile.

## 14 Enterprise Platform Model

| Dominio | AS-IS | Transition | TO-BE |
|---|---|---|---|
| Observatory | Manuali e procedure esistenti | Allineamento con SOP enterprise | Operatività remota governata |
| Automation | Procedure e strumenti esistenti | Formalizzazione controlli | Automazione verificabile |
| Network | Documentazione infrastrutturale esistente | Registro configurazioni | Configurazione tracciata |
| Data | Warehouse e analytics documentati | Registry e KPI framework | Data platform governata |
| Documentation | MkDocs esistente | Baseline DSG-MR-001 | Knowledge base enterprise |
| Analytics | Dashboard e quality gate esistenti | KPI framework | Reporting direzionale e operativo |
| AI | Ambito previsto | Governance e TBD | AI Platform governata |
| Knowledge Graph | Ambito previsto | Registro conoscenza | Knowledge Platform interrogabile |
| Web Portal | Portale/documentazione esistente | Release governance | Portale governato |

## 15 Capability Model

Le capability enterprise includono:

- osservazione e acquisizione;
- controllo strumenti;
- telemetria;
- automazione;
- sincronizzazione;
- documentazione;
- data management;
- analytics;
- reporting;
- AI governance;
- knowledge management;
- release management;
- security e disaster recovery;
- asset e configuration management.

## 16 Platform Interaction

Modello operativo approvato:

| Nodo | Responsabilità |
|---|---|
| PC Principale | sviluppo, Git, documentazione, MkDocs, dashboard, portale, analytics, release, attività di engineering e governance |
| EAGLE | gestione dell'osservatorio, acquisizione, controllo degli strumenti, telemetria, automazione, sincronizzazione, operazioni sul campo |

I dettagli di sincronizzazione e configurazione sono `Da validare` se non presenti nei manuali tecnici.

---

# PART III - Program Portfolio

## 17 Observatory

Programma per la gestione dell'osservatorio remoto e delle operazioni astronomiche. Collegato alla documentazione Observatory, ai capitoli infrastrutturali e alle SOP operative.

## 18 Infrastructure

Programma per infrastruttura fisica, elettrica, rete, computer EAGLE e componenti di supporto. Dettagli tecnici non confermati restano `Da validare`.

## 19 Operations

Programma per avvio, acquisizione, chiusura, manutenzione, troubleshooting, incident e post-mortem.

## 20 Data

Programma per gestione dati, warehouse, validazione storico, archiviazione e configurazioni analytics.

## 21 Image and Scientific Repository

Programma per organizzazione e conservazione di immagini e dati scientifici. Struttura definitiva `TBD` se non ancora descritta nei manuali.

## 22 Analytics and Reporting

Programma per dashboard, KPI, reporting operativo e qualità dati.

## 23 Live Operations

Programma per stato osservatorio, session report e dashboard live. Integrazione completa `Da validare`.

## 24 AI

Programma previsto per supporto AI, soggetto ad AI Governance. Use case e modelli `TBD`.

## 25 Documentation

Programma per manuale MkDocs, navigazione, indici, release documentali e qualità dei link.

## 26 Knowledge

Programma per knowledge index, registri, glossario, acronimi e riferimenti.

## 27 Community

Programma per contenuti e comunicazione verso stakeholder e community. Canali e responsabilità `Da validare`.

## 28 Security

Programma per sicurezza, accessi remoti, gestione segreti, controlli e incident response.

## 29 Engineering Governance

Programma per workflow repository, branch, commit, PR, review, quality gate, release e change management.

## 30 Asset and Configuration Management

Programma per asset registry, configuration registry, versioning e baseline configurative.

---

# PART IV - Enterprise Registry

## 31 Platform Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#platform-registry).

## 32 Program Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#program-registry).

## 33 Component Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#component-registry).

## 34 Technology Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#technology-registry).

## 35 Asset Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#asset-registry).

## 36 Configuration Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#configuration-registry).

## 37 Knowledge Registry

Fonte: [Registri e tracciabilità](../enterprise/registries/index.md#knowledge-registry).

---

# PART V - Planning

## 38 Release Strategy

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#38-release-strategy) e [Release documentation](../enterprise/release-documentation.md).

## 39 Milestone Strategy

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#39-milestone-strategy).

## 40 Sprint Strategy

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#40-sprint-strategy).

## 41 Enterprise Roadmap 2026-2030

| Periodo | Focus | Stato |
|---|---|---|
| 2026 | Baseline documentale e architetturale | In corso |
| 2027 | Stabilizzazione processi e registri | Da validare |
| 2028 | Automazione avanzata e analytics maturi | Da validare |
| 2029 | AI e Knowledge Platform governate | TBD |
| 2030 | Piattaforma enterprise consolidata | TBD |

## 42 Dependency Matrix

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#42-dependency-matrix).

## 43 Risk Matrix

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#43-risk-matrix).

## 44 KPI Framework

Fonte: [Enterprise Planning Framework](../enterprise/planning.md#44-kpi-framework).

---

# PART VI - Governance

## 45 Architecture Governance

Fonte: [Governance](../enterprise/governance.md#architecture-governance).

## 46 Change Management

Fonte: [Governance](../enterprise/governance.md#change-management).

## 47 Configuration Management

Fonte: [Governance](../enterprise/governance.md#configuration-management).

## 48 Data Governance

Fonte: [Governance](../enterprise/governance.md#data-governance).

## 49 AI Governance

Fonte: [Governance](../enterprise/governance.md#ai-governance).

## 50 Quality Gates

Fonte: [Governance](../enterprise/governance.md#quality-gates).

## 51 Documentation Governance

Fonte: [Governance](../enterprise/governance.md#documentation-governance).

## 52 Release Governance

Fonte: [Governance](../enterprise/governance.md#release-governance).

---

# PART VII - Long-Term Vision

## 53 Vision 2030

Entro il 2030 Digital StarGate mira a una piattaforma enterprise consolidata, con osservatorio remoto, documentazione, dati, analytics, release e governance coordinati da un modello unico.

## 54 Vision 2035

Entro il 2035 Digital StarGate mira a evolvere verso un ecosistema maturo di osservazione, conoscenza e automazione scientifica. Dettagli di investimento, capacità e responsabilità sono `TBD`.

## 55 Continuous Evolution

L'evoluzione continua avviene tramite roadmap review, ADR, assessment, SOP, release notes, project history e registri di tracciabilità.

## 56 Conclusion

DSG-MR-001 stabilisce la baseline enterprise del programma Digital StarGate e vincola le milestone successive a coerenza documentale, architetturale e operativa. Ogni estensione deve rispettare la Roadmap Freeze Policy e mantenere tracciabilità verso questa roadmap.