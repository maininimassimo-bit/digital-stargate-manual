# DSG-PRG-001 - Enterprise Program Portfolio

| Campo | Valore |
|---|---|
| Documento | Enterprise Program Portfolio |
| Identificativo | `DSG-PRG-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## 1. Scopo

Questo documento rende operativo il Program Portfolio previsto da `DSG-MR-001`, senza introdurre programmi, piattaforme o domini ulteriori rispetto alla roadmap congelata.

Il portfolio collega programmi, capability, documenti tecnici, rischi, registri, KPI ed evidenze. Dove la documentazione esistente non conferma dettagli tecnici o ownership specifiche, l'informazione resta `TBD` o `Da validare`.

## 2. Ambito

L'ambito copre i programmi richiesti dalla milestone:

- Observatory;
- Infrastructure;
- Operations;
- Data Platform;
- Warehouse;
- Reporting;
- Renderer;
- Analytics Dashboard;
- Dashboard Live;
- Image and Scientific Repository;
- Live Operations;
- Portal;
- AI Platform;
- Documentation Platform;
- Knowledge Platform;
- Engineering Governance;
- Community;
- Security;
- Disaster Recovery;
- Asset and Configuration Management.

`Warehouse`, `Reporting`, `Renderer`, `Analytics Dashboard`, `Dashboard Live`, `Portal`, `AI Platform`, `Documentation Platform` e `Knowledge Platform` sono trattati come programmi o sotto-capability del portfolio congelato, coerenti con `Data`, `Analytics and Reporting`, `Live Operations`, `AI`, `Documentation` e `Knowledge` definiti in `DSG-MR-001`.

## 3. Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-PRG-PRN-001` | Roadmap-first | Ogni programma deriva da `DSG-MR-001` |
| `DSG-PRG-PRN-002` | No duplication | I capitoli tecnici restano fonte AS-IS per dettagli operativi |
| `DSG-PRG-PRN-003` | Stato esplicito | Ogni programma distingue AS-IS, Transition e TO-BE |
| `DSG-PRG-PRN-004` | Evidence-based | KPI ed evidenze devono avere fonte o marcatura `Da validare` |
| `DSG-PRG-PRN-005` | Governance by design | Ogni programma è collegato a controlli, rischi e registri |

## 4. Ruoli e responsabilità

| Ruolo | Responsabilità | Stato |
|---|---|---|
| Program Owner | Priorità, scope e accettazione del programma | Da validare per programma |
| Architecture Owner | Coerenza con `DSG-EAM-001`, `DSRA-000` e `DSRA-001` | Transition |
| Governance Owner | Applicazione di `DSG-GOV-001` e Roadmap Freeze Policy | Transition |
| Documentation Owner | Tracciabilità, link, MkDocs e release documentale | Transition |
| Operations Owner | Procedure operative e safety | Da validare dove non confermato |
| Data Owner | Dataset, lineage, KPI e qualità dati | Da validare dove non confermato |

Gli owner nominali non confermati non vengono inventati. Le responsabilità operative specifiche restano `Da validare`.

## 5. Modello di portfolio

| Campo | Uso |
|---|---|
| ID programma | Identificativo stabile `DSG-PRG-*` |
| Stato | AS-IS, Transition, TO-BE, TBD o Da validare |
| Scopo | Risultato atteso del programma |
| Input | Documenti, dati, log o decisioni consumati |
| Output | Artefatti prodotti |
| Controlli | Quality gate o controlli collegati |
| Rischi | Rischi DSRA o roadmap collegati |
| KPI/Evidenze | Misure o prove verificabili |

## 6. Vista sintetica dei programmi

| ID | Programma | Stato prevalente | Fonte roadmap | Note |
|---|---|---|---|---|
| `DSG-PRG-OBS` | Observatory | AS-IS / Transition | Sezione 17 | Osservatorio fisico e strumenti |
| `DSG-PRG-INF` | Infrastructure | AS-IS / Transition | Sezione 18 | Rete, EAGLE, storage, continuità |
| `DSG-PRG-OPS` | Operations | AS-IS / Transition | Sezione 19 | Avvio, acquisizione, chiusura, incident |
| `DSG-PRG-DATA` | Data Platform | Transition | Sezione 20 | Dati operativi e scientifici |
| `DSG-PRG-WHS` | Warehouse | Transition | Sezioni 20, 22 | Sotto-capability Data/Analytics |
| `DSG-PRG-RPT` | Reporting | Transition | Sezione 22 | Report e KPI |
| `DSG-PRG-RND` | Renderer | Transition / Da validare | Sezione 22 | Rendering dashboard/report, dettagli `Da validare` |
| `DSG-PRG-ANL-DASH` | Analytics Dashboard | Transition | Sezione 22 | Dashboard analytics |
| `DSG-PRG-LIVE-DASH` | Dashboard Live | TO-BE | Sezione 23 | Stato live, feed `Da validare` |
| `DSG-PRG-IMG` | Image and Scientific Repository | TO-BE / Da validare | Sezione 21 | Repository immagini e metadata |
| `DSG-PRG-LIVE` | Live Operations | TO-BE | Sezione 23 | Operatività live governata |
| `DSG-PRG-PORTAL` | Portal | AS-IS / Transition | Sezioni 25, 31 | MkDocs e Web Portal |
| `DSG-PRG-AI` | AI Platform | TO-BE / TBD | Sezione 24 | AI assistiva governata |
| `DSG-PRG-DOC` | Documentation Platform | AS-IS / Transition | Sezione 25 | Docs-as-Code e release |
| `DSG-PRG-KNW` | Knowledge Platform | Transition / TO-BE | Sezione 26 | Knowledge base e Knowledge Graph |
| `DSG-PRG-ENG-GOV` | Engineering Governance | Transition | Sezione 29 | ADR, registri, quality gate |
| `DSG-PRG-COM` | Community | TO-BE / Da validare | Sezione 27 | Contributi e stakeholder |
| `DSG-PRG-SEC` | Security | AS-IS / Transition | Sezione 28 | Accessi, segreti, pubblicazione |
| `DSG-PRG-DR` | Disaster Recovery | AS-IS / Transition | Sezioni 18, 28 | Backup, recovery, continuità |
| `DSG-PRG-ACM` | Asset and Configuration Management | Transition / Da validare | Sezione 30 | Asset e configurazioni |

## 7. Programmi

### 7.1 Observatory - `DSG-PRG-OBS`

| Campo | Valore |
|---|---|
| Scopo | Governare osservatorio fisico, strumentazione e sicurezza osservativa |
| Ambito | Cupola, montatura, ottiche, camere, treno ottico, ambiente |
| AS-IS | Manuale tecnico presente |
| Transition | Collegamento a checklist, DSRA e asset registry |
| TO-BE | Stato osservatorio integrabile con Live Operations dopo validazione |

Input: capitoli tecnici su cupola, sistema astronomico, automazione e sicurezza.

Output: checklist osservatorio, evidenze di sessione, rischi e asset collegati.

Controlli: `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001`.

Rischi: `DSG-RSK-OPS-001`, `DSG-RSK-OPS-002`.

KPI/evidenze: sessioni completate, checklist, log osservativi. Frequenze e soglie: `Da validare`.

Riferimenti: [struttura cupola](../chapters/03-struttura-cupola.md), [montatura CGX-L](../chapters/07-cgx-l.md), [chiusura osservatorio](../chapters/25-chiusura-osservatorio.md), [DSRA](DSRA-risk-assessment.md).

### 7.2 Infrastructure - `DSG-PRG-INF`

| Campo | Valore |
|---|---|
| Scopo | Governare rete, alimentazione, EAGLE, storage e continuità tecnica |
| Ambito | Infrastruttura remota, connettività, accesso, continuità, backup |
| AS-IS | Capitoli infrastrutturali presenti |
| Transition | Consolidamento test e registri |
| TO-BE | Continuità misurabile con evidenze periodiche |

Input: documenti rete, EAGLE, backup, sicurezza e configurazioni.

Output: evidenze di test rete, backup, configurazioni sanitizzate, registro infrastruttura.

Controlli: `DSG-CTL-NET-001`, `DSG-CTL-INF-001`, `DSG-CTL-SEC-001`.

Rischi: `DSG-RSK-NET-001`, `DSG-RSK-INF-001`, `DSG-RSK-DR-001`.

KPI/evidenze: uptime accesso remoto, esito test failover, readiness backup. Valori target: `Da validare`.

Riferimenti: [rete](../chapters/05-infrastruttura-rete.md), [EAGLE](../chapters/06-eagle.md), [backup e Disaster Recovery](../chapters/21-backup-disaster-recovery.md), [sicurezza informatica](../chapters/24-sicurezza-informatica-accessi-remoti.md).

### 7.3 Operations - `DSG-PRG-OPS`

| Campo | Valore |
|---|---|
| Scopo | Governare ciclo operativo dell'osservatorio |
| Ambito | Avvio, acquisizione, chiusura, manutenzione, incident, post-mortem |
| AS-IS | Procedure operative presenti |
| Transition | Evidenze e registri collegati |
| TO-BE | Lifecycle operativo misurabile e riesaminato |

Input: SOP tecniche, log sessione, DSRA, FMEA.

Output: checklist, incident log, post-mortem, azioni correttive.

Controlli: `DSG-CTL-OPS-001`, `DSG-CTL-SAF-001`, `DSG-CTL-QA-001`.

Rischi: rischi operations e safety del DSRA.

KPI/evidenze: sessioni completate, incident recurrence, tempo di recovery. Soglie: `Da validare`.

Riferimenti: [avvio osservatorio](../chapters/16-sop-avvio.md), [acquisizione automatica](../chapters/17-acquisizione-automatica.md), [emergenze e recovery](../chapters/18-emergenze-recovery.md), [problem management](../chapters/31-problem-management-post-mortem.md), [SOP enterprise](sop.md).

### 7.4 Data Platform - `DSG-PRG-DATA`

| Campo | Valore |
|---|---|
| Scopo | Governare dati operativi, osservativi e scientifici |
| Ambito | Session report, dataset, lineage, qualità, archiviazione |
| AS-IS | Gestione dati documentata |
| Transition | Normalizzazione e quality gate |
| TO-BE | Contratti dati stabili e repository scientifico governato |

Input: log EAGLE/software, report sessione, dataset warehouse.

Output: dataset validati, catalogo dati, KPI, anomalie documentate.

Controlli: `DSG-CTL-DATA-001`, `QG-DATA`.

Rischi: `DSG-RSK-DATA-001`.

KPI/evidenze: qualità dati, record esclusi, completezza sessione. Schema finale: `TBD`.

Riferimenti: [gestione dati](../chapters/28-gestione-dati-archiviazione.md), [Warehouse](../architecture/warehouse/index.md), [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md).

### 7.5 Warehouse - `DSG-PRG-WHS`

| Campo | Valore |
|---|---|
| Scopo | Consolidare dati normalizzati per analytics e reporting |
| Ambito | Schema, dataset, quality gate, build e operatività |
| AS-IS | Documentazione Warehouse presente |
| Transition | Contratti dati e quality gate in consolidamento |
| TO-BE | Warehouse governato con versioning schema |

Input: session report e dati normalizzati.

Output: dataset warehouse, log validazione, evidenze build.

Controlli: `DSG-CTL-DATA-001`, `QG-DATA`.

Rischi: divergenza report/warehouse/dashboard.

KPI/evidenze: build riuscite, record validi, errori schema. Target: `Da validare`.

Riferimenti: [panoramica Warehouse](../architecture/warehouse/index.md), [dataset e schema](../architecture/warehouse/datasets-and-schema.md), [quality gate Warehouse](../architecture/warehouse/validation-and-quality-gates.md).

### 7.6 Reporting - `DSG-PRG-RPT`

| Campo | Valore |
|---|---|
| Scopo | Pubblicare report e KPI coerenti con dati validati |
| Ambito | Reportistica operativa, KPI, evidenze di qualità |
| AS-IS | Capitolo reportistica e sezione analytics presenti |
| Transition | Allineamento con warehouse e dashboard |
| TO-BE | Report periodici con lineage esplicito |

Input: dataset validati, definizioni KPI, anomalie.

Output: report, tabelle KPI, note di aggiornamento.

Controlli: `DSG-CTL-DATA-001`, `DSG-CTL-QA-001`.

Rischi: KPI privi di fonte o non confrontabili.

KPI/evidenze: copertura KPI, data ultimo aggiornamento, fonti dichiarate.

Riferimenti: [reportistica e KPI](../chapters/29-reportistica-operativa-kpi.md), [Analytics](../analytics/index.md).

### 7.7 Renderer - `DSG-PRG-RND`

| Campo | Valore |
|---|---|
| Scopo | Governare la generazione o visualizzazione di output report/dashboard |
| Ambito | Rendering documentale, dashboard o viste pubblicate |
| AS-IS | Funzioni di pubblicazione presenti nel portale |
| Transition | Confini tecnici da documentazione esistente |
| TO-BE | Processo renderer tracciabile, se confermato |

Input: dataset, Markdown, configurazioni portale.

Output: pagine renderizzate, dashboard o report pubblicati.

Controlli: `DSG-CTL-DOC-001`, `DSG-CTL-QA-001`.

Rischi: output non allineato alla fonte dati.

KPI/evidenze: build MkDocs, verifica visualizzazione, aggiornamento dashboard. Dettagli tecnici renderer: `Da validare`.

Riferimenti: [gestione documentale e release](../chapters/34-gestione-documentale-release.md), [Dashboard](../analytics/dashboard-integrated.md).

### 7.8 Analytics Dashboard - `DSG-PRG-ANL-DASH`

| Campo | Valore |
|---|---|
| Scopo | Rendere consultabili KPI e andamento operativo |
| Ambito | Dashboard integrate, storico, configurazioni analytics |
| AS-IS | Sezione Analytics presente |
| Transition | Quality gate e refresh governati |
| TO-BE | Dashboard con lineage e stato qualità sempre visibili |

Input: warehouse, configurazioni analytics, validazione storico.

Output: dashboard, indicatori, anomalie documentate.

Controlli: `DSG-CTL-DATA-001`, `QG-DATA`, `QG-DOC`.

Rischi: disallineamento dati-dashboard.

KPI/evidenze: link health, qualità dati, ultimo aggiornamento.

Riferimenti: [Portale Analytics](../analytics/index.md), [Dashboard integrata](../analytics/dashboard-integrated.md), [Validazione storico](../analytics/history-validation.md).

### 7.9 Dashboard Live - `DSG-PRG-LIVE-DASH`

| Campo | Valore |
|---|---|
| Scopo | Pubblicare stato live solo dopo controlli safety e dati validati |
| Ambito | Stato osservatorio, meteo, avanzamento sessione, AllSky |
| AS-IS | Citata nella roadmap, non baseline completa |
| Transition | Contratti feed e policy pubblicazione da definire |
| TO-BE | Dashboard live affidabile e governata |

Input: telemetria, feed live, stato safety.

Output: vista live pubblicabile, log aggiornamento, alert governati.

Controlli: `QG-OPS`, `QG-SEC`, `QG-DATA`.

Rischi: pubblicazione stato non validato o dati sensibili.

KPI/evidenze: disponibilità feed, latenza, coerenza safety. Tutti `Da validare`.

Riferimenti: [Roadmap evolutiva](../chapters/33-roadmap-evolutiva.md), [sistema AllSky](../chapters/27-sistema-allsky.md), [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md).

### 7.10 Image and Scientific Repository - `DSG-PRG-IMG`

| Campo | Valore |
|---|---|
| Scopo | Governare immagini, target, metadati e output scientifici |
| Ambito | Archivio immagini, metadata, sessioni, qualità |
| AS-IS | Report sessione e gestione dati presenti |
| Transition | Modello metadata da definire |
| TO-BE | Repository scientifico tracciabile |

Input: immagini, log, report sessione, metadata disponibili.

Output: catalogo immagini, mapping sessione-target, evidenze qualità.

Controlli: `QG-DATA`, `DSG-CTL-DATA-001`.

Rischi: perdita metadata o confusione tra archivio grezzo e pubblicazione.

KPI/evidenze: immagini catalogate, metadata completi, esclusioni documentate. Schema: `TBD`.

Riferimenti: [gestione dati e archiviazione](../chapters/28-gestione-dati-archiviazione.md), [requisiti e tracciabilità](../chapters/40-requisiti-tracciabilita.md).

### 7.11 Live Operations - `DSG-PRG-LIVE`

| Campo | Valore |
|---|---|
| Scopo | Introdurre operatività live governata e sicura |
| Ambito | Stato osservatorio, sequenza, safety, telemetria |
| AS-IS | Non completa come baseline operativa |
| Transition | Definizione feed e controlli |
| TO-BE | Live Operations integrata con portale e dashboard |

Input: EAGLE, software astronomico, rete, sensori e log.

Output: stato live validato, evidenze e incidenti tracciati.

Controlli: `QG-OPS`, `QG-SEC`, `QG-DATA`.

Rischi: stato live non attendibile o uso improprio in decisioni safety.

KPI/evidenze: feed validi, errori feed, incidenti live. Dettagli: `Da validare`.

Riferimenti: [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md), [monitoraggio meteo](../chapters/26-monitoraggio-meteo-sicurezza-ambientale.md).

### 7.12 Portal - `DSG-PRG-PORTAL`

| Campo | Valore |
|---|---|
| Scopo | Pubblicare manuale, dashboard, release e conoscenza |
| Ambito | MkDocs, navigazione, GitHub Pages, contenuti pubblicabili |
| AS-IS | Portale MkDocs presente |
| Transition | Sezione enterprise e quality gate rafforzati |
| TO-BE | Portale come knowledge hub governato |

Input: Markdown, configurazioni, registri, release notes.

Output: sito navigabile, pagine enterprise, dashboard, release.

Controlli: `DSG-CTL-DOC-001`, `QG-DOC`, `QG-REL`.

Rischi: link rotti, navigazione incoerente, contenuti non verificati.

KPI/evidenze: build, link health, coverage documentale.

Riferimenti: [indice enterprise](index.md), [gestione documentale e release](../chapters/34-gestione-documentale-release.md), [Portal Publication Guidelines](../developer/portal-publication-guidelines.md).

### 7.13 AI Platform - `DSG-PRG-AI`

| Campo | Valore |
|---|---|
| Scopo | Abilitare assistenza AI governata e auditabile |
| Ambito | Ricerca, sintesi, diagnosi documentale, supporto non safety |
| AS-IS | Non baseline |
| Transition | AI governance e casi d'uso |
| TO-BE | AI assistiva con controlli e audit |

Input: knowledge base, documentazione approvata, registri.

Output: suggerimenti, sintesi, analisi; decisione sempre umana.

Controlli: `QG-AI`, `QG-SEC`, AI governance.

Rischi: uso oltre ambito, esposizione dati sensibili, suggerimenti non verificati.

KPI/evidenze: task assistiti con review, anomalie AI, audit output. Casi d'uso e tool: `TBD`.

Riferimenti: [AI Governance](governance.md#10-ai-governance), [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md).

### 7.14 Documentation Platform - `DSG-PRG-DOC`

| Campo | Valore |
|---|---|
| Scopo | Governare documentazione Docs-as-Code |
| Ambito | Markdown, MkDocs, registri, SOP, release, appendici |
| AS-IS | Manuale e sezione enterprise presenti |
| Transition | Tracciabilità roadmap completa |
| TO-BE | Documentazione mantenibile e misurabile |

Input: modifiche tecniche, decisioni, requisiti, evidenze.

Output: documenti versionati, link, release notes, change log.

Controlli: `QG-DOC`, `DSG-CTL-QA-001`, `DSG-CTL-REL-001`.

Rischi: documentazione divergente dal sistema reale.

KPI/evidenze: coverage, link health, documenti con owner/stato.

Riferimenti: [handbook](handbook.md), [SOP](sop.md), [release documentation](release-documentation.md).

### 7.15 Knowledge Platform - `DSG-PRG-KNW`

| Campo | Valore |
|---|---|
| Scopo | Trasformare documenti, decisioni e incidenti in conoscenza riutilizzabile |
| Ambito | Glossario, ADR, SOP, registri, Knowledge Graph |
| AS-IS | Manuale, ADR, SOP e registri presenti |
| Transition | Normalizzazione conoscenza e cross-reference |
| TO-BE | Knowledge Graph e AI-ready knowledge base |

Input: documenti approvati, post-mortem, registri, glossary.

Output: knowledge registry, glossario, relazioni semantiche.

Controlli: `QG-DOC`, `QG-AI`.

Rischi: conoscenza duplicata, non aggiornata o usata fuori contesto.

KPI/evidenze: elementi knowledge registrati, link incrociati, coverage glossary. Knowledge Graph: `TBD`.

Riferimenti: [appendici](appendices.md), [registri](registries/index.md), [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md).

### 7.16 Engineering Governance - `DSG-PRG-ENG-GOV`

| Campo | Valore |
|---|---|
| Scopo | Governare scelte tecniche, qualità e release |
| Ambito | ADR, review, quality gate, assessment, change log |
| AS-IS | ADR e governance presenti |
| Transition | Quality gate enterprise consolidati |
| TO-BE | Governance misurata e riesaminata |

Input: change request, ADR, assessment, registri.

Output: decisioni, controlli, evidenze, release readiness.

Controlli: `QG-ARCH`, `QG-REL`, `DSG-CTL-ADR-001`.

Rischi: decisioni non registrate o modifiche non tracciate.

KPI/evidenze: ADR aggiornati, review chiuse, change log.

Riferimenti: [Governance](governance.md), [ADR-004](adr/ADR-004-enterprise-documentation-baseline.md), [Assessment](assessment.md).

### 7.17 Community - `DSG-PRG-COM`

| Campo | Valore |
|---|---|
| Scopo | Preparare collaborazione e fruizione controllata della conoscenza |
| Ambito | Stakeholder, contributor, reviewer, canali di contributo |
| AS-IS | Non definita come capability operativa completa |
| Transition | Handbook e regole contributo |
| TO-BE | Community governata e sostenibile |

Input: handbook, policy documentale, issue/PR.

Output: linee guida, template, materiali condivisibili.

Controlli: `QG-DOC`, Documentation Governance.

Rischi: contributi non controllati o informazioni sensibili pubblicate.

KPI/evidenze: contributi revisionati, feedback integrati. Canali e licenza: `Da validare`.

Riferimenti: [handbook](handbook.md), [appendici](appendices.md).

### 7.18 Security - `DSG-PRG-SEC`

| Campo | Valore |
|---|---|
| Scopo | Proteggere accessi, dati, configurazioni e pubblicazione |
| Ambito | Accessi remoti, segreti, dati sensibili, AI, Live Operations |
| AS-IS | Capitoli sicurezza presenti |
| Transition | Security gate enterprise |
| TO-BE | Security governance integrata nei release gate |

Input: configurazioni sanitizzate, PR, documenti operativi.

Output: controlli security, finding, correzioni, evidenze.

Controlli: `QG-SEC`, `DSG-CTL-SEC-001`.

Rischi: credenziali pubblicate, esposizione stato operativo sensibile.

KPI/evidenze: scansione segreti, finding risolti, review security.

Riferimenti: [sicurezza informatica](../chapters/24-sicurezza-informatica-accessi-remoti.md), [DSRA](DSRA-risk-assessment.md).

### 7.19 Disaster Recovery - `DSG-PRG-DR`

| Campo | Valore |
|---|---|
| Scopo | Governare continuità, backup, recovery e ritorno operativo |
| Ambito | Backup, rollback, incident recovery, procedure conservative |
| AS-IS | Capitoli recovery e backup presenti |
| Transition | Registro DR e test periodici |
| TO-BE | Recovery verificabile con evidenze |

Input: backup, log incidenti, release notes, configurazioni.

Output: recovery checklist, test DR, azioni correttive.

Controlli: `DSG-CTL-DR-001`, `QG-REL`, `QG-OPS`.

Rischi: perdita dati, indisponibilità accesso o ripristino non testato.

KPI/evidenze: esito test restore, RTO/RPO. Valori: `Da validare`.

Riferimenti: [backup e Disaster Recovery](../chapters/21-backup-disaster-recovery.md), [emergenze e recovery](../chapters/18-emergenze-recovery.md), [release documentation](release-documentation.md).

### 7.20 Asset and Configuration Management - `DSG-PRG-ACM`

| Campo | Valore |
|---|---|
| Scopo | Mantenere inventario, configurazioni e relazioni di controllo |
| Ambito | Asset fisici, digitali, configurazioni, versioni, obsolescenza |
| AS-IS | Capitoli asset/configurazioni presenti |
| Transition | Registry enterprise consolidato |
| TO-BE | Asset/config mapping completo e verificabile |

Input: inventari, configurazioni sanitizzate, ADR, change log.

Output: asset registry, configuration registry, evidenze audit.

Controlli: `DSG-CTL-CFG-001`, `QG-SEC`, `QG-ARCH`.

Rischi: configurazioni divergenti, asset non tracciati, segreti pubblicati.

KPI/evidenze: asset con owner/stato, configurazioni versionate, audit configurazione. Mapping completo: `Da validare`.

Riferimenti: [inventario e asset management](../chapters/22-inventario-asset-management.md), [configurazioni software](../chapters/37-configurazioni-software-parametri.md), [registri e checklist](../chapters/38-registri-checklist-modelli.md).

## 8. Dipendenze tra programmi

| Dipendenza | Programmi impattati | Stato |
|---|---|---|
| Safety state | Observatory, Operations, Live Operations, AI Platform | Critica |
| Connettività remota | Infrastructure, Operations, Dashboard Live | Da validare periodicamente |
| Session report | Data Platform, Warehouse, Reporting, Analytics Dashboard | Transition |
| `mkdocs.yml` e build | Portal, Documentation Platform, Release Governance | AS-IS / Transition |
| Registri enterprise | Tutti i programmi | Transition |
| Asset/configuration registry | Infrastructure, Security, Disaster Recovery, ACM | Da consolidare |

## 9. Rischi trasversali

| ID | Rischio | Programmi | Trattamento |
|---|---|---|---|
| `DSG-PRG-RSK-001` | Evoluzione fuori roadmap congelata | Tutti | Applicare `DSG-GOV-001` |
| `DSG-PRG-RSK-002` | Dati o KPI senza fonte | Data, Warehouse, Reporting, Analytics | `QG-DATA` |
| `DSG-PRG-RSK-003` | Automazione o AI su safety non approvata | Operations, Live, AI | Safety boundary e ADR |
| `DSG-PRG-RSK-004` | Duplicazione documentale | Documentation, Knowledge | Registro documenti e review |
| `DSG-PRG-RSK-005` | Configurazioni sensibili pubblicate | Security, Infrastructure, ACM | `QG-SEC` |

## 10. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md)
- [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md)
- [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md)
- [DSG-GOV-001](governance.md)
- [DSRA Risk Assessment](DSRA-risk-assessment.md)
- [Registri enterprise](registries/index.md)
- [Release documentation](release-documentation.md)

## 11. Elementi TBD

| ID | Elemento | Programma | Stato |
|---|---|---|---|
| `DSG-PRG-TBD-001` | Owner specifici per programma | Tutti | Da validare |
| `DSG-PRG-TBD-002` | Schema finale data catalog e scientific metadata | Data, Image Repository | TBD |
| `DSG-PRG-TBD-003` | Contratti feed live e dashboard live | Live Operations, Dashboard Live | Da validare |
| `DSG-PRG-TBD-004` | Casi d'uso, strumenti e controlli AI specifici | AI Platform | TBD |
| `DSG-PRG-TBD-005` | Canali, licenza e modello contributor community | Community | Da validare |
| `DSG-PRG-TBD-006` | RTO/RPO e frequenza test restore | Disaster Recovery | Da validare |
| `DSG-PRG-TBD-007` | Mapping completo asset-configurazioni-requisiti | ACM | Da validare |
