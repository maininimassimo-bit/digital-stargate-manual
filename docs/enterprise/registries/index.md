# DSG-REG-001 - Enterprise Registry and Traceability

| Campo | Valore |
|---|---|
| Documento | Enterprise Registry and Traceability |
| Identificativo | `DSG-REG-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## 1. Scopo

Questo documento centralizza i registri enterprise richiesti da `DSG-MR-001` e li collega al [Program Portfolio](../program-portfolio.md), al meta-modello [DSG-EAM-001](../../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), alla reference architecture [DSRA-001](../../enterprise-architecture/DSRA-001-reference-architecture.md) e alla governance [DSG-GOV-001](../governance.md).

Il registro non sostituisce i capitoli tecnici esistenti: conserva una vista enterprise di tracciabilità e rimanda ai documenti operativi come fonte AS-IS.

## 2. Ambito

I registri inclusi sono:

- Platform Registry;
- Program Registry;
- Component Registry;
- Technology Registry;
- Asset Registry;
- Configuration Registry;
- Knowledge Registry;
- Requirement, Risk, Control, Decision, Deliverable e Change Registry già previsti dalla baseline.

## 3. Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-REG-PRN-001` | Unicità della fonte | Ogni elemento enterprise ha un ID stabile |
| `DSG-REG-PRN-002` | Freeze compliance | Nessuna piattaforma o programma fuori `DSG-MR-001` |
| `DSG-REG-PRN-003` | Stato esplicito | AS-IS, Transition, TO-BE, TBD o Da validare |
| `DSG-REG-PRN-004` | Nessun segreto | Configurazioni sensibili non vengono pubblicate |
| `DSG-REG-PRN-005` | Linkability | Ogni elemento deve collegarsi a documento, controllo o evidenza quando disponibile |

## 4. Ruoli e responsabilità

| Ruolo | Responsabilità | Stato |
|---|---|---|
| Registry Owner | Manutenzione struttura registri e ID | Documentation Owner |
| Architecture Owner | Coerenza componenti, piattaforme e capability | Da validare |
| Governance Owner | Applicazione Roadmap Freeze Policy | Da validare |
| Security Owner | Controllo segreti e configurazioni sensibili | Da validare |
| Program Owner | Validazione elementi del proprio programma | Da validare per programma |

Gli owner non nominativamente confermati restano ruoli funzionali.

## 5. Processo

1. Identificare elemento e fonte.
2. Verificare se rientra in `DSG-MR-001`.
3. Assegnare ID, stato, programma e documento correlato.
4. Collegare rischi, controlli, input, output o KPI quando pertinenti.
5. Marcare come `TBD` o `Da validare` ogni informazione non confermata.
6. Aggiornare MkDocs solo per documenti pubblicabili, non per ogni elemento di registro.
7. Riesaminare il registro a ogni milestone enterprise o modifica strutturale.

## 6. Stati standard

| Stato | Uso |
|---|---|
| Proposto | Elemento identificato ma non ancora approvato |
| Approvato | Elemento valido e applicabile |
| In trattamento | Azione o controllo in corso |
| Verificato | Evidenza disponibile e accettata |
| Sospeso | Elemento valido ma temporaneamente non applicato |
| Superato | Elemento sostituito da decisione o requisito successivo |
| AS-IS | Elemento documentato nello stato corrente |
| Transition | Elemento in consolidamento |
| TO-BE | Elemento target non ancora pienamente implementato |
| TBD | Dettaglio non definito |
| Da validare | Dettaglio plausibile ma non confermato da evidenza |

## 7. Platform Registry

| ID | Piattaforma | Programmi collegati | Stato | Input | Output | Controlli | Rischi | Evidenze |
|---|---|---|---|---|---|---|---|---|
| `DSG-PLT-001` | Digital StarGate Portal | Documentation Platform, Portal, Reporting | AS-IS / Transition | Markdown, `mkdocs.yml`, analytics | Portale MkDocs, pagine pubblicate | `QG-DOC`, `QG-REL` | `DSG-RSK-DOC-001` | Build o verifica statica |
| `DSG-PLT-002` | Remote Observatory | Observatory, Operations, Infrastructure | AS-IS | Capitoli tecnici, log, checklist | Sessioni, telemetria, evidenze operative | `QG-OPS`, `DSG-CTL-SAF-001` | `DSG-RSK-OPS-001`, `DSG-RSK-OPS-002` | Checklist e log |
| `DSG-PLT-003` | Data and Analytics Platform | Data Platform, Warehouse, Reporting, Analytics Dashboard | Transition | Report sessione, dataset | Warehouse, KPI, dashboard | `QG-DATA` | `DSG-RSK-DATA-001` | Report validazione |
| `DSG-PLT-004` | Live Operations Platform | Live Operations, Dashboard Live, Security | TO-BE | Feed live, stato safety, meteo | Stato live validato | `QG-OPS`, `QG-SEC`, `QG-DATA` | `DSG-PRG-RSK-003` | Da validare |
| `DSG-PLT-005` | AI-assisted Knowledge Platform | AI Platform, Knowledge Platform | TO-BE / TBD | Knowledge base, registri | Assistenza AI auditabile | `QG-AI`, `QG-SEC` | `DSG-RISK-004` | TBD |

## 8. Program Registry

| ID | Programma | Stato | Documento fonte | Owner | Dipendenze | KPI/Evidenze |
|---|---|---|---|---|---|---|
| `DSG-PRG-OBS` | Observatory | AS-IS / Transition | [Portfolio](../program-portfolio.md#71-observatory---dsg-prg-obs) | Da validare | Safety, Operations, Asset Registry | Checklist, log sessione |
| `DSG-PRG-INF` | Infrastructure | AS-IS / Transition | [Portfolio](../program-portfolio.md#72-infrastructure---dsg-prg-inf) | Da validare | Network, DR, Security | Test rete e backup |
| `DSG-PRG-OPS` | Operations | AS-IS / Transition | [Portfolio](../program-portfolio.md#73-operations---dsg-prg-ops) | Da validare | Observatory, EAGLE, SOP | Sessioni e incident log |
| `DSG-PRG-DATA` | Data Platform | Transition | [Portfolio](../program-portfolio.md#74-data-platform---dsg-prg-data) | Da validare | Warehouse, Reporting | Qualità dati |
| `DSG-PRG-WHS` | Warehouse | Transition | [Portfolio](../program-portfolio.md#75-warehouse---dsg-prg-whs) | Da validare | Data Platform | Build e schema |
| `DSG-PRG-RPT` | Reporting | Transition | [Portfolio](../program-portfolio.md#76-reporting---dsg-prg-rpt) | Da validare | Warehouse, Analytics | KPI con fonte |
| `DSG-PRG-RND` | Renderer | Transition / Da validare | [Portfolio](../program-portfolio.md#77-renderer---dsg-prg-rnd) | Da validare | Portal, Analytics | Build/render output |
| `DSG-PRG-ANL-DASH` | Analytics Dashboard | Transition | [Portfolio](../program-portfolio.md#78-analytics-dashboard---dsg-prg-anl-dash) | Da validare | Warehouse, Reporting | Dashboard aggiornata |
| `DSG-PRG-LIVE-DASH` | Dashboard Live | TO-BE | [Portfolio](../program-portfolio.md#79-dashboard-live---dsg-prg-live-dash) | Da validare | Live Operations, Security | Feed validati, TBD |
| `DSG-PRG-IMG` | Image and Scientific Repository | TO-BE / Da validare | [Portfolio](../program-portfolio.md#710-image-and-scientific-repository---dsg-prg-img) | Da validare | Data Platform | Metadata scientifici, TBD |
| `DSG-PRG-LIVE` | Live Operations | TO-BE | [Portfolio](../program-portfolio.md#711-live-operations---dsg-prg-live) | Da validare | Operations, Network, Safety | Telemetria validata |
| `DSG-PRG-PORTAL` | Portal | AS-IS / Transition | [Portfolio](../program-portfolio.md#712-portal---dsg-prg-portal) | Documentation Owner | MkDocs, GitHub | Build, link health |
| `DSG-PRG-AI` | AI Platform | TO-BE / TBD | [Portfolio](../program-portfolio.md#713-ai-platform---dsg-prg-ai) | Da validare | Knowledge, Security | Audit output, TBD |
| `DSG-PRG-DOC` | Documentation Platform | AS-IS / Transition | [Portfolio](../program-portfolio.md#714-documentation-platform---dsg-prg-doc) | Documentation Owner | Portal, Governance | Documenti pubblicati |
| `DSG-PRG-KNW` | Knowledge Platform | Transition / TO-BE | [Portfolio](../program-portfolio.md#715-knowledge-platform---dsg-prg-knw) | Da validare | Documentation, AI | Knowledge registry |
| `DSG-PRG-ENG-GOV` | Engineering Governance | Transition | [Portfolio](../program-portfolio.md#716-engineering-governance---dsg-prg-eng-gov) | Governance Owner | ADR, Quality Gates | Review e ADR |
| `DSG-PRG-COM` | Community | TO-BE / Da validare | [Portfolio](../program-portfolio.md#717-community---dsg-prg-com) | Da validare | Documentation, Security | Contributi revisionati |
| `DSG-PRG-SEC` | Security | AS-IS / Transition | [Portfolio](../program-portfolio.md#718-security---dsg-prg-sec) | Da validare | Tutti | Security checks |
| `DSG-PRG-DR` | Disaster Recovery | AS-IS / Transition | [Portfolio](../program-portfolio.md#719-disaster-recovery---dsg-prg-dr) | Da validare | Infrastructure, Release | Test restore, TBD |
| `DSG-PRG-ACM` | Asset and Configuration Management | Transition / Da validare | [Portfolio](../program-portfolio.md#720-asset-and-configuration-management---dsg-prg-acm) | Da validare | Infrastructure, Security | Audit asset/config |

## 9. Component Registry

| ID | Componente | Piattaforma | Programma | Stato | Input | Output | Vincoli |
|---|---|---|---|---|---|---|---|
| `DSG-CMP-MKDOCS` | MkDocs Material portal | `DSG-PLT-001` | Documentation Platform | AS-IS | Markdown, `mkdocs.yml` | Sito pubblicabile | Build strict quando disponibile |
| `DSG-CMP-GITHUB` | GitHub repository and Pages | `DSG-PLT-001` | Portal | AS-IS | Branch, commit, PR | Versioning e pubblicazione | Nessun segreto |
| `DSG-CMP-EAGLE` | PrimaLuceLab EAGLE | `DSG-PLT-002` | Infrastructure / Operations | AS-IS | Comandi strumenti, log | Acquisizione e telemetria | Configurazioni sensibili escluse |
| `DSG-CMP-CUPOLA` | Cupola e copertura | `DSG-PLT-002` | Observatory | AS-IS | Stato fisico e safety | Protezione osservatorio | Safety-first |
| `DSG-CMP-CGX-L` | Celestron CGX-L | `DSG-PLT-002` | Observatory | AS-IS | Comandi CPWI/ASCOM | Puntamento, tracking, park | Park verificato |
| `DSG-CMP-NINA` | N.I.N.A. | `DSG-PLT-002` | Operations | AS-IS | Sequenze | Acquisizione | Dettagli configurazione Da validare |
| `DSG-CMP-PHD2` | PHD2 | `DSG-PLT-002` | Operations | AS-IS | Guida | Log guida | Parametri sensibili esclusi |
| `DSG-CMP-CPWI` | CPWI | `DSG-PLT-002` | Operations | AS-IS | Controllo montatura | Stato montatura | Safety boundary |
| `DSG-CMP-ASCOM` | ASCOM Platform | `DSG-PLT-002` | Automation | AS-IS | Driver e interfacce | Integrazione strumenti | Versioni Da validare |
| `DSG-CMP-WAREHOUSE` | Warehouse | `DSG-PLT-003` | Warehouse | Transition | Session report | Dataset normalizzati | Schema versionato, TBD |
| `DSG-CMP-ANALYTICS` | Analytics Dashboard | `DSG-PLT-003` | Analytics Dashboard | Transition | Dataset validati | KPI e grafici | Fonte e periodo obbligatori |
| `DSG-CMP-RENDERER` | Renderer | `DSG-PLT-001` / `DSG-PLT-003` | Renderer | Da validare | Markdown o dataset | Output visuale | Dettagli tecnici TBD |
| `DSG-CMP-LIVE` | Live Observatory status | `DSG-PLT-004` | Live Operations | TO-BE | Feed live | Stato pubblicabile | Contratti feed Da validare |
| `DSG-CMP-AI` | AI assistant | `DSG-PLT-005` | AI Platform | TBD | Knowledge base | Suggerimenti auditabili | Nessun comando safety |
| `DSG-CMP-KG` | Knowledge Graph | `DSG-PLT-005` | Knowledge Platform | TBD | Documenti e registri | Relazioni semantiche | Schema TBD |

## 10. Technology Registry

| ID | Tecnologia | Uso | Stato | Fonte | Vincoli |
|---|---|---|---|---|---|
| `DSG-TEC-MKDOCS` | MkDocs Material | Portale documentale | AS-IS | `mkdocs.yml` | Build strict quando disponibile |
| `DSG-TEC-MD` | Markdown | Sorgente documentale | AS-IS | Repository | Stile coerente |
| `DSG-TEC-GITHUB` | GitHub | Repository, PR, Pages, Actions | AS-IS | Repository | Nessun segreto |
| `DSG-TEC-PY` | Python | Pipeline e automazioni documentate | AS-IS / Transition | Warehouse/analytics | Versioni Da validare |
| `DSG-TEC-ASCOM` | ASCOM Platform | Integrazione strumenti | AS-IS | Capitolo ASCOM | Versioni Da validare |
| `DSG-TEC-NINA` | N.I.N.A. | Sequenze acquisizione | AS-IS | Capitolo N.I.N.A. | Parametri Da validare |
| `DSG-TEC-PHD2` | PHD2 | Guida | AS-IS | Capitolo PHD2 | Parametri Da validare |
| `DSG-TEC-CPWI` | CPWI | Controllo montatura | AS-IS | Capitolo CPWI | Safety boundary |
| `DSG-TEC-WHS` | Warehouse tooling | Consolidamento dati | Transition | Warehouse docs | Contratti dati TBD |
| `DSG-TEC-AI` | AI tooling | Assistenza conoscenza | TBD | Roadmap | Governance obbligatoria |

## 11. Asset Registry

| ID | Classe asset | Esempi documentati | Programma | Stato registro | Evidenza richiesta | Note |
|---|---|---|---|---|---|---|
| `DSG-AST-STRUCT` | Struttura | Cupola, copertura | Observatory | Da consolidare | Inventario e manutenzione | Dettagli fisici nei capitoli tecnici |
| `DSG-AST-POWER` | Energia | Alimentazione, eventuale UPS | Infrastructure / DR | Da validare | Test e autonomia | Non inventare autonomia |
| `DSG-AST-NET` | Rete | Starlink, router, SIM, VPN | Infrastructure / Security | Da consolidare | Test accesso e failover | Configurazioni sensibili escluse |
| `DSG-AST-COMPUTE` | Computer | EAGLE, PC Principale | Infrastructure | Da consolidare | Stato, ruolo, backup | Dettagli hardware Da validare |
| `DSG-AST-ASTRO` | Astronomia | Montatura, ottiche, camere | Observatory | Da consolidare | Schede asset e manutenzione | Collegare a capitoli 7-10 |
| `DSG-AST-DATA` | Dati | Dataset, report, immagini | Data Platform | Transition | Catalogo dati | Metadata scientifici TBD |
| `DSG-AST-DOC` | Documentazione | Pagine, registri, release | Documentation Platform | AS-IS / Transition | `mkdocs.yml`, PR | Link e owner |

## 12. Configuration Registry

| ID | Configurazione | Fonte | Programma | Stato | Pubblicabile | Controllo |
|---|---|---|---|---|---|---|
| `DSG-CFG-MKDOCS` | Navigazione e build MkDocs | `mkdocs.yml` | Documentation Platform | AS-IS | Si | `QG-DOC` |
| `DSG-CFG-PORTAL-ASSET` | CSS/JavaScript portale | `docs/styles`, `docs/javascripts` | Portal | AS-IS | Si | Review UI/documentale |
| `DSG-CFG-ASTRO-SW` | Parametri software astronomico | Capitoli 11-14, 37 | Operations | Da consolidare | Solo sanitizzato | `QG-SEC` |
| `DSG-CFG-NET` | Router/VPN/accesso remoto | Capitoli 5, 24, 36 | Infrastructure / Security | Da validare | Solo sanitizzato | `QG-SEC` |
| `DSG-CFG-WHS` | Schema Warehouse | Warehouse docs | Warehouse | Transition | Si, se non sensibile | `QG-DATA` |
| `DSG-CFG-ANL` | Configurazione Analytics | Sezione Analytics | Analytics Dashboard | Transition | Si, se non sensibile | `QG-DATA` |
| `DSG-CFG-LIVE` | Configurazione Live Operations | TBD | Live Operations | TO-BE | Da validare | `QG-OPS`, `QG-SEC` |
| `DSG-CFG-AI` | Configurazione AI | TBD | AI Platform | TO-BE / TBD | Da validare | `QG-AI`, `QG-SEC` |

## 13. Knowledge Registry

| ID | Conoscenza | Fonte | Programma | Stato | Output | Rischio |
|---|---|---|---|---|---|---|
| `DSG-KNW-MANUAL` | Manuale tecnico | Capitoli 1-44 | Documentation Platform | AS-IS | Procedure e contesto | Divergenza documentale |
| `DSG-KNW-ADR` | Decisioni architetturali | ADR esistenti | Engineering Governance | AS-IS / Transition | Decision log | Decisioni non registrate |
| `DSG-KNW-SOP` | Procedure operative | Capitoli e SOP enterprise | Operations | Transition | Checklist | Procedure non aggiornate |
| `DSG-KNW-RISK` | Rischi e FMEA | Capitolo 41 e DSRA | Governance | Transition | Risk register | Controlli non evidenziati |
| `DSG-KNW-DATA` | Warehouse e analytics | Warehouse/Analytics docs | Data Platform | Transition | Data knowledge | KPI non tracciati |
| `DSG-KNW-INCIDENT` | Incidenti e post-mortem | Capitolo 31 | Operations | Da consolidare | Lesson learned | Recurrence non gestita |
| `DSG-KNW-COMMUNITY` | Materiali community | Handbook/appendici | Community | Da validare | Guide contributor | Pubblicazione non controllata |
| `DSG-KNW-AI` | Knowledge AI-ready | TBD | AI Platform | TO-BE / TBD | Contesto AI governato | Output non verificati |

## 14. Registro requisiti

| ID | Requisito | Categoria | Priorita | Stato | Fonte | Verifica |
|---|---|---|---|---|---|---|
| `DSG-REQ-DOC-001` | Ogni documento enterprise deve richiamare `DSG-MR-001` | Documentale | Alta | Verificato | Roadmap | Revisione contenuti |
| `DSG-REQ-DOC-002` | Ogni pagina enterprise pubblicata deve essere raggiungibile da MkDocs | Documentale | Alta | Verificato | Roadmap | `mkdocs.yml` |
| `DSG-REQ-PRG-001` | Ogni programma deve essere collegato al portfolio congelato | Portfolio | Alta | Verificato | `DSG-PRG-001` | Program Registry |
| `DSG-REQ-REG-001` | Ogni piattaforma, programma, componente, tecnologia, asset, configurazione e conoscenza deve avere registro | Registry | Alta | Verificato | `DSG-MR-001` | Sezioni 7-13 |
| `DSG-REQ-ARC-001` | Ogni componente critico deve avere dominio, responsabilita e controllo associato | Architettura | Alta | Verificato | `DSG-EAM-001` | Component Registry |
| `DSG-REQ-SAF-001` | Le procedure operative devono privilegiare lo stato conservativo in condizioni incerte | Safety | Critica | Approvato | DSRA, FMEA | SOP incident |
| `DSG-REQ-OPS-001` | Avvio e chiusura osservatorio devono essere supportati da checklist | Operativo | Alta | Approvato | Manuale tecnico | Registro sessione |
| `DSG-REQ-OPS-002` | Gli incidenti devono produrre log, decisione e azione correttiva | Operativo | Alta | Approvato | DSRA | Post-mortem |
| `DSG-REQ-GOV-001` | Ogni modifica strutturale deve passare da review e change log | Governance | Alta | Approvato | `DSG-GOV-001` | PR e registro |
| `DSG-REQ-ADR-001` | Le decisioni architetturali rilevanti devono essere registrate in ADR | Governance | Alta | Verificato | `DSG-ADR-004` | Registro decisioni |
| `DSG-REQ-REL-001` | Ogni release documentale deve avere criteri di readiness e rollback | Release | Alta | Approvato | `DSG-REL-001` | Checklist release |
| `DSG-REQ-QA-001` | Link, navigazione e marcatori aperti devono essere controllati prima della PR | Qualita | Alta | Approvato | Handbook | Validazione documentale |

## 15. Registro decisioni

| ID | Decisione | Stato | Documento | Impatto |
|---|---|---|---|---|
| `DSG-ADR-001` | Session Layer | Approvata | `architecture/ADR-001-Session-Layer.md` | Struttura dati sessioni |
| `DSG-ADR-002` | Analytics Quality Gates | Approvata | `architecture/ADR-002-Analytics-Quality-Gates.md` | Controllo qualita analytics |
| `DSG-ADR-003` | Warehouse Engine | Approvata | `architecture/ADR-003-Warehouse-Engine.md` | Consolidamento dati |
| `DSG-ADR-004` | Enterprise documentation baseline | Approvata | `enterprise/adr/ADR-004-enterprise-documentation-baseline.md` | Governance `DSG-MR-001` |
| `DSG-REG-DEC-001` | I registri enterprise sono mantenuti in un documento unico per evitare duplicazioni | Approvata | `enterprise/registries/index.md` | Unicita fonte registry |

## 16. Registro rischi

| ID | Rischio | Classe | Stato | Controlli |
|---|---|---|---|---|
| `DSG-RSK-OPS-001` | Cupola o safety incoerente | Medio | Mitigato | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001` |
| `DSG-RSK-OPS-002` | Montatura non in park | Medio | Mitigato | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001` |
| `DSG-RSK-NET-001` | Perdita connettivita o VPN | Medio | Mitigato | `DSG-CTL-NET-001` |
| `DSG-RSK-INF-001` | Indisponibilita EAGLE o USB | Alto | In trattamento | `DSG-CTL-INF-001` |
| `DSG-RSK-DATA-001` | Divergenza report/warehouse/dashboard | Alto | In trattamento | `DSG-CTL-DATA-001` |
| `DSG-RSK-DOC-001` | Documenti non raggiungibili | Basso | Mitigato | `DSG-CTL-DOC-001` |
| `DSG-RSK-GOV-001` | Decisioni non registrate | Medio | Mitigato | `DSG-CTL-ADR-001` |
| `DSG-RSK-REL-001` | Release senza readiness completa | Medio | Mitigato | `DSG-CTL-REL-001` |
| `DSG-RSK-SEC-001` | Segreti o configurazioni sensibili pubblicati | Alto | Mitigato | `DSG-CTL-SEC-001`, `QG-SEC` |
| `DSG-RSK-DR-001` | Ripristino non testato o evidenze DR assenti | Medio | In trattamento | `DSG-CTL-DR-001` |
| `DSG-RSK-AI-001` | AI usata oltre ambito o senza audit | Alto | In trattamento | `QG-AI`, AI Governance |

## 17. Registro controlli

| ID | Controllo | Tipo | Frequenza | Evidenza |
|---|---|---|---|---|
| `DSG-CTL-DOC-001` | Navigazione MkDocs aggiornata | Preventivo | Ogni PR documentale | Diff `mkdocs.yml` |
| `DSG-CTL-QA-001` | Controllo link interni e marcatori aperti | Preventivo | Ogni PR documentale | Log validazione |
| `DSG-CTL-ADR-001` | ADR per decisioni strutturali | Preventivo | Quando necessario | ADR approvato |
| `DSG-CTL-SAF-001` | Verifica stato conservativo | Preventivo | Ogni sessione | Checklist |
| `DSG-CTL-OPS-001` | Checklist di avvio e chiusura obbligatorie | Preventivo | Ogni sessione | Registro sessione |
| `DSG-CTL-NET-001` | Test VPN e failover | Detective | Periodico, Da validare | Registro test |
| `DSG-CTL-INF-001` | Verifica EAGLE, USB e storage prima delle sessioni | Preventivo | Prima sessione, Da validare | Checklist avvio |
| `DSG-CTL-DATA-001` | Quality gate su dataset e KPI | Detective | Ogni aggiornamento dati | Report validazione analytics |
| `DSG-CTL-REL-001` | Release readiness | Preventivo | Ogni release | Checklist release |
| `DSG-CTL-SEC-001` | Verifica assenza segreti e configurazioni sensibili | Preventivo | Ogni PR | Log controllo |
| `DSG-CTL-CFG-001` | Audit configurazioni pubblicabili e sanitizzate | Preventivo | A ogni modifica configurazione | Registro configurazione |
| `DSG-CTL-DR-001` | Test restore e rollback documentato | Detective | Frequenza Da validare | Evidenza DR |

## 18. Registro deliverable

| ID | Deliverable | Stato | Percorso |
|---|---|---|---|
| `DSG-DEL-001` | Master Roadmap | Verificato | `docs/enterprise-roadmap/DSG-MR-001-master-roadmap.md` |
| `DSG-DEL-002` | Enterprise Architecture | Verificato | `docs/enterprise/enterprise-architecture.md` |
| `DSG-DEL-003` | DSRA | Verificato | `docs/enterprise/DSRA-risk-assessment.md` |
| `DSG-DEL-004` | ADR-004 | Verificato | `docs/enterprise/adr/ADR-004-enterprise-documentation-baseline.md` |
| `DSG-DEL-005` | Registri | Verificato | `docs/enterprise/registries/index.md` |
| `DSG-DEL-006` | Handbook | Verificato | `docs/enterprise/handbook.md` |
| `DSG-DEL-007` | SOP | Verificato | `docs/enterprise/sop.md` |
| `DSG-DEL-008` | Assessment | Verificato | `docs/enterprise/assessment.md` |
| `DSG-DEL-009` | Governance | Verificato | `docs/enterprise/governance.md` |
| `DSG-DEL-010` | Release documentation | Verificato | `docs/enterprise/release-documentation.md` |
| `DSG-DEL-011` | Appendici | Verificato | `docs/enterprise/appendices.md` |
| `DSG-DEL-012` | Enterprise Program Portfolio | Verificato | `docs/enterprise/program-portfolio.md` |
| `DSG-DEL-013` | Enterprise Architecture Meta Model | Verificato | `docs/enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md` |
| `DSG-DEL-014` | Vision Target Architecture | Verificato | `docs/enterprise-architecture/DSRA-000-vision-target-architecture.md` |
| `DSG-DEL-015` | Reference Architecture | Verificato | `docs/enterprise-architecture/DSRA-001-reference-architecture.md` |

## 19. Change log

| ID | Data | Cambiamento | Tipo | Stato |
|---|---|---|---|---|
| `DSG-CHG-001` | 26/07/2026 | Creazione baseline enterprise `DSG-MR-001` | Documentazione | Verificato |
| `DSG-CHG-002` | 26/07/2026 | Aggiunta sezione enterprise in MkDocs | Navigazione | Verificato |
| `DSG-CHG-003` | 26/07/2026 | Collegamento DSRA, ADR e governance | Tracciabilita | Verificato |
| `DSG-CHG-004` | 26/07/2026 | Pubblicazione Program Portfolio enterprise | Portfolio | Verificato |
| `DSG-CHG-005` | 26/07/2026 | Consolidamento Platform, Program, Component, Technology, Asset, Configuration e Knowledge Registry | Registry | Verificato |

## 20. KPI ed evidenze

| KPI | Formula o criterio | Stato |
|---|---|---|
| Copertura platform registry | Piattaforme registrate / piattaforme previste da roadmap | Transition |
| Copertura program registry | Programmi registrati / programmi portfolio | Verificato |
| Copertura component registry | Componenti critici registrati / componenti documentati | Transition |
| Asset registry maturity | Asset con stato e fonte / asset documentati | Da validare |
| Configuration registry maturity | Configurazioni classificate / configurazioni documentate | Da validare |
| Knowledge coverage | Fonti knowledge registrate / fonti enterprise | Transition |

## 21. Elementi TBD

| ID | Elemento | Stato | Documento correlato |
|---|---|---|---|
| `DSG-REG-TBD-001` | Owner nominali per programmi e registri | Da validare | [Portfolio](../program-portfolio.md) |
| `DSG-REG-TBD-002` | Inventario asset completo | Da validare | Capitolo asset management |
| `DSG-REG-TBD-003` | Configurazioni operative pubblicabili vs sensibili | Da validare | Capitoli configurazione e sicurezza |
| `DSG-REG-TBD-004` | Schema Knowledge Graph | TBD | `DSG-EAM-001` |
| `DSG-REG-TBD-005` | Contratti feed Live Operations | Da validare | `DSRA-000`, `DSRA-001` |
| `DSG-REG-TBD-006` | RTO/RPO Disaster Recovery | Da validare | Capitolo backup e DR |
| `DSG-REG-TBD-007` | Tooling AI e audit specifici | TBD | AI Governance |

## 22. Regole di manutenzione

- Un nuovo elemento deve avere ID, stato, fonte e programma quando applicabile.
- Un nuovo programma deve essere già previsto da `DSG-MR-001` o approvato da roadmap successiva.
- Un nuovo rischio medio o superiore deve avere almeno un controllo.
- Un controllo deve produrre un'evidenza osservabile.
- Una decisione strutturale deve avere un ADR.
- Un deliverable è verificato solo se è raggiungibile da MkDocs o escluso in modo esplicito.
- Un asset o una configurazione non confermata resta `Da validare`.
- Una configurazione sensibile non deve essere pubblicata nel repository.

## 23. Riferimenti

- [DSG-MR-001](../../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Enterprise Program Portfolio](../program-portfolio.md)
- [DSG-EAM-001](../../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md)
- [DSRA-000](../../enterprise-architecture/DSRA-000-vision-target-architecture.md)
- [DSRA-001](../../enterprise-architecture/DSRA-001-reference-architecture.md)
- [DSG-GOV-001](../governance.md)
- [DSRA Risk Assessment](../DSRA-risk-assessment.md)
- [Enterprise Assessment](../assessment.md)
- [Release documentation](../release-documentation.md)
