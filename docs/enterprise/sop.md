# DSG-SOP-001 - Standard Operating Procedures

| Campo | Valore |
|---|---|
| Documento | Standard Operating Procedures |
| Identificativo | `DSG-SOP-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Definire le SOP enterprise per documentazione, dati, release, incident, change management, assessment, configuration/security e Disaster Recovery.

Le SOP non duplicano le procedure tecniche dei capitoli operativi: le collegano a prerequisiti, responsabilita, controlli, evidenze e rollback.

## 2. Principi comuni

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-SOP-PRN-001` | Safety-first | Incertezza operativa -> stato conservativo |
| `DSG-SOP-PRN-002` | Evidence | Ogni procedura produce evidenza |
| `DSG-SOP-PRN-003` | Registry update | Cambiamenti significativi aggiornano i registri |
| `DSG-SOP-PRN-004` | Nessun contenuto sensibile | Nessuna configurazione sensibile nei documenti |

## 3. SOP documentazione - `DSG-SOP-DOC-001`

| Campo | Valore |
|---|---|
| Prerequisiti | Roadmap, documento fonte, `mkdocs.yml` |
| Responsabilita | Documentation Owner, Reviewer |
| Trigger | Nuovo documento o modifica strutturale |
| Input | Roadmap, registry, file Markdown |
| Output | Documento aggiornato, registri aggiornati, navigazione coerente |
| Controlli | `DSG-CTL-DOC-001`, `DSG-CTL-QA-001`, `QG-DOC` |

Procedura: verificare fonte esistente, creare nuovi file solo se necessari, inserire ID/stato/owner/data/scopo/ambito, collegare `DSG-MR-001`, aggiornare `mkdocs.yml`, controllare link, ID, duplicazioni e TBD.

Gestione errori: se un link non e verificabile nel runtime ma risulta gia in `mkdocs.yml`, annotare il limite; se manca anche dalla navigazione, correggere prima del commit.

Evidenze: diff file, controllo YAML, controllo link.

Rollback: ripristinare la voce MkDocs e il documento modificato nel commit correttivo.

Elementi TBD: automazione completa link checker.

## 4. SOP dati e analytics - `DSG-SOP-DATA-001`

| Campo | Valore |
|---|---|
| Prerequisiti | Fonte dati, periodo, schema o descrizione dataset |
| Responsabilita | Data Owner, Architecture Owner |
| Trigger | Nuova sessione, ricalcolo KPI, variazione schema |
| Input | Log, report, dataset |
| Output | Dataset validato, report aggiornato |
| Controlli | `DSG-CTL-DATA-001`, `QG-DATA` |

Procedura: identificare origine e periodo, separare dati grezzi/normalizzati/aggregati/pubblicati, validare completezza, marcare dati mancanti come `N/D`, `TBD` o `Da validare`, aggiornare report solo con fonte indicata, registrare anomalie.

Gestione errori: bloccare KPI senza fonte; documentare record esclusi.

Evidenze: report validazione, dashboard aggiornata, note anomalie.

Rollback: tornare al dataset/report precedente e registrare la motivazione.

Elementi TBD: schema finale data catalog.

## 5. SOP release - `DSG-SOP-REL-001`

| Campo | Valore |
|---|---|
| Prerequisiti | Deliverable completati, registry aggiornato |
| Responsabilita | Release Owner, Documentation Owner, Reviewer |
| Trigger | Preparazione release documentale o milestone |
| Input | Commit, validazioni, release notes |
| Output | Readiness checklist, rollback plan, PR summary |
| Controlli | `DSG-CTL-REL-001`, `QG-REL`, `QG-DOC`, `QG-SEC` |

Procedura: confermare scope release, verificare file pubblicabili, verificare link e contenuti sensibili, aggiornare release documentation e project history, definire rollback, preparare PR solo se richiesto.

Gestione errori: se build MkDocs non e disponibile, completare controlli statici e demandare build a PC Principale/GitHub Actions.

Evidenze: log validazione, commit hash, release checklist.

Rollback: rimuovere o correggere voci MkDocs e documenti impattati.

Elementi TBD: automazione release readiness.

## 6. SOP incident - `DSG-SOP-INC-001`

| Campo | Valore |
|---|---|
| Prerequisiti | Accesso sicuro, stato meteo/safety disponibile se possibile |
| Responsabilita | Operations Owner, Infrastructure Owner |
| Trigger | Stato non sicuro, perdita accesso, errore cupola, blocco EAGLE |
| Input | Stato osservatorio, log, sintomi |
| Output | Stato conservativo, log incidente, azione correttiva |
| Controlli | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001`, `QG-OPS` |

Procedura: assumere la condizione piu conservativa, verificare meteo/copertura/montatura/alimentazione, completare la chiusura solo se sicura, evitare comandi distruttivi se lo stato e incerto, registrare timestamp/sintomo/azione/risultato, aprire post-mortem se necessario, aggiornare DSRA/SOP/registry.

Gestione errori: se l'accesso remoto non e affidabile, privilegiare recovery documentata e intervento sicuro.

Evidenze: log incidente, checklist, post-mortem.

Rollback: tornare a stato operativo precedente solo dopo verifica safety.

Elementi TBD: soglie escalation e tempi target.

## 7. SOP change management - `DSG-SOP-CHG-001`

| Campo | Valore |
|---|---|
| Prerequisiti | Descrizione modifica e impatto stimato |
| Responsabilita | Governance Owner, Architecture Owner, Documentation Owner |
| Trigger | Modifica hardware, software, dati, architettura o governance |
| Input | Change request, ADR, rischio, documento |
| Output | Change log, ADR se necessario, registry aggiornato |
| Controlli | `DSG-CTL-ADR-001`, `DSG-CTL-DOC-001`, `QG-ARCH` |

Procedura: descrivere cambiamento e impatto, classificare area e stato AS-IS/Transition/TO-BE, verificare Roadmap Freeze Policy, redigere ADR solo per decisione reale, aggiornare registri e documenti, validare con controlli appropriati.

Gestione errori: se il cambio introduce ambito non approvato, marcarlo `Proposed` o `TBD` e non pubblicarlo come baseline.

Evidenze: ADR, registry diff, commit.

Rollback: revert documentale o commit correttivo tracciato.

Elementi TBD: template change request.

## 8. SOP assessment - `DSG-SOP-ASMT-001`

Prerequisiti: fonti interne disponibili. Responsabilita: Governance Owner, Reviewer. Procedura: separare evidenze da analisi, non trasformare ipotesi in fatti, indicare data o `Da validare`, collegare fonti interne, registrare gap e raccomandazioni. Rollback: ripristinare conclusione precedente se la nuova evidenza non regge. Elementi TBD: scoring automatico.

## 9. SOP configuration/security - `DSG-SOP-CFG-SEC-001`

Prerequisiti: diff o configurazione da revisionare. Responsabilita: Security Owner, Documentation Owner. Procedura: classificare configurazione come pubblicabile, sensibile o `Da validare`, rimuovere valori privati, aggiornare Configuration Registry, bloccare release in caso di finding sensibile. Rollback: rimozione immediata e commit correttivo. Elementi TBD: tooling dedicato.

## 10. SOP Disaster Recovery - `DSG-SOP-DR-001`

Prerequisiti: piano rollback o backup disponibile. Responsabilita: Infrastructure Owner, Release Owner. Procedura: identificare oggetto da ripristinare, verificare ultimo stato valido noto, applicare rollback documentale o recovery, registrare risultato e limiti, aggiornare DSRA e registry se il rischio cambia. Rollback: definito per singola release. Elementi TBD: RTO/RPO target e frequenza test.

## 11. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Enterprise Program Portfolio](program-portfolio.md)
- [Enterprise Registry](registries/index.md)
- [Governance](governance.md)
- [Release documentation](release-documentation.md)
- [Assessment](assessment.md)
