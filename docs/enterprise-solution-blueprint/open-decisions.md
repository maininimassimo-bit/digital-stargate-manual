# DSG-ESB-009 - Open Architectural Decisions

| Campo | Valore |
|---|---|
| Documento | Open Architectural Decisions |
| Identificativo | `DSG-ESB-009` |
| Stato | Active decision backlog |
| Versione | 0.1 |
| Data | 2026-07-27 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Raccogliere le decisioni architetturali non ancora finalizzabili sulla base della documentazione disponibile. Questo documento non propone risposte non supportate da evidenze: registra cosa manca, perche impatta l'architettura e quale input serve.

## Regole

- Una decisione aperta non e un'approvazione implicita.
- Le risposte future devono rispettare `DSG-MR-001`, `DSG-EAM-001`, `DSRA-000`, `DSRA-001` e Governance.
- Se una decisione cambia confini, tecnologia, sicurezza, dati o deployment, deve produrre ADR o aggiornamento governato.
- Le informazioni operative sensibili restano fuori repository.

## Decision backlog

| ID | Decision | Reason | Impact | Owner | Required input |
|---|---|---|---|---|---|
| `DSG-OAD-001` | Schema formale di Observation Request | La documentazione descrive target e sequenze, ma non un record standard della richiesta | Scheduling, catalogo, portale scientifico, tracciabilita | Operations Owner / Science Owner | Campi minimi, stato richiesta, formato, esempi storici |
| `DSG-OAD-002` | Target Registry definitivo | Esistono profili e target operativi, ma non un registro target consolidato | Pianificazione, Knowledge Graph, Science Portal | Science Owner | Lista target, coordinate, priorita, filtri, finestre, naming |
| `DSG-OAD-003` | Equipment Registry completo | Asset e configurazioni sono documentati in capitoli separati con molti `DA VALIDARE` | Scheduling, calibrazione, troubleshooting, backup configurazioni | Engineering Owner | Seriali, versioni driver/firmware, mapping USB, alimentazioni, profili |
| `DSG-OAD-004` | Session Manifest standard | La chiusura dati richiede report, log e verifica, ma manca schema manifest | Lineage dati, archive, analytics, KG | Data Owner | Campi sessione, ID, link file, checksum, stato, formato Markdown/JSON/YAML |
| `DSG-OAD-005` | Storage fisico del catalogo osservativo | Il repository descrive warehouse e gestione dati, ma non il modello finale del catalogo scientifico | Data Platform, Analytics, Science Portal | Data Owner | Scelta tra Markdown registry, CSV/Parquet, warehouse, combinazione controllata |
| `DSG-OAD-006` | Relazione tra warehouse analytics e Observation Catalog | ADR-003 copre il warehouse; il catalogo osservativo richiede scopo e ownership specifici | KPI, dashboard, publication, KG | Data Owner / Analytics Owner | Schema dati, data refresh, fonti, quality gate |
| `DSG-OAD-007` | Policy retention dettagliata per raw, intermedi e finali | Il capitolo backup indica classi e retention parziale; i dati osservativi hanno `DA VALIDARE` | Storage cost, recovery, reprocessing | Infrastructure Owner / Data Owner | Volume medio sessione, valore scientifico, capacita storage, costi |
| `DSG-OAD-008` | RTO/RPO per dati osservativi | Manuale/repository/config hanno valori; dati osservativi restano da validare | Disaster Recovery e continuita | Infrastructure Owner | Obiettivi per raw, processed, catalog, cloud/off-site |
| `DSG-OAD-009` | Provider e architettura Cloud Storage | Cloud Storage e off-site sono previsti ma non decisi | Backup, archiviazione, costi, security | Infrastructure Owner / Data Owner | Provider candidate, cifratura, retention, restore, budget |
| `DSG-OAD-010` | Protocollo e soglie Weather Station | Il monitoraggio meteo e critico, ma modello, protocollo e soglie operative non sono finalizzati | Safety, automazione, scheduling | Operations Owner | Modello sensori, soglie vento/pioggia/umidita, freshness, test UNSAFE |
| `DSG-OAD-011` | Contratti telemetria EAGLE -> PC Principale | EAGLE produce stato/log, ma contratti e frequenze non sono formalizzati | Observability, dashboard, incident evidence | Engineering Owner | Metriche minime, frequenza, formato, percorso trasferimento |
| `DSG-OAD-012` | Regole Scheduler e target priority | Scheduler e TO-BE; manca regola approvata per priorita e vincoli | Automazione osservativa e backlog target | Operations Owner / Science Owner | Criteri scientifici/fotografici, meteo, luna, configurazione ottica |
| `DSG-OAD-013` | Uso N.I.N.A. Scheduler/plugin o piano esterno | Non risulta scelta implementativa per scheduler | Deployment, component registry, SOP | Architecture Owner | Funzioni richieste, compatibilita N.I.N.A., vincoli safety |
| `DSG-OAD-014` | ASCOM Alpaca enablement | ASCOM e documentato; Alpaca e citato come possibile integrazione ma non approvato | Network exposure, single control path, security | Architecture Owner / Security Owner | Necessita reale, rete, auth, threat model, test laboratorio |
| `DSG-OAD-015` | Knowledge Graph model | KG e previsto come TO-BE, ma schema e storage sono TBD | AI, tracciabilita, impact analysis | Knowledge Owner / Architecture Owner | Entita, relazioni, query target, storage candidate, governance |
| `DSG-OAD-016` | AI Assistant use cases | AI e prevista ma non operativa; use case e guardrail devono essere definiti | Sicurezza, privacy, operazioni, audit | Governance Owner | Use case ammessi, dati consentiti, retention, human review, provider |
| `DSG-OAD-017` | OpenAI data handling | OpenAI e integrazione prevista; mancano modello, retention e sanitizzazione definitiva | Security, AI governance, compliance | Governance Owner / Security Owner | Policy provider, prompt policy, secret handling, audit trail |
| `DSG-OAD-018` | Astrometry.net usage policy | ASTAP e locale; Astrometry.net esterno richiede criteri d'uso | Privacy immagini, dipendenza esterna, banda | Science Owner / Security Owner | Quando usarlo, quali dati inviare, credenziali, fallback |
| `DSG-OAD-019` | TNS submission process | TNS previsto solo come integrazione esterna; mancano SOP e responsabilita | Publication scientifica, qualita, reputazione | Science Owner | Criteri evento, review, formato, account, approvazione |
| `DSG-OAD-020` | AAVSO submission process | AAVSO richiede dati fotometrici validati e formato appropriato | Science Portal, calibration, metadata | Science Owner | Standard fotometria, validazione, account, SOP |
| `DSG-OAD-021` | Notification channels and escalation | Notifiche sono citate nei capitoli ma canali/destinatari non sono definiti | Incident response, operations | Operations Owner | Canali, severita, destinatari, finestre, test |
| `DSG-OAD-022` | Session log correlation format | Log esistono in piu strumenti ma manca formato di correlazione | Troubleshooting, analytics, incident evidence | Operations Owner / Data Owner | ID sessione, timestamp standard, severity, parser o template |
| `DSG-OAD-023` | Science Portal publication model | Portale scientifico e vista logica, ma template e contenuti non sono formalizzati | Pubblicazione immagini, cataloghi, community | Documentation Owner / Science Owner | Template pagina osservazione, metadata minimi, review |
| `DSG-OAD-024` | Maintenance Portal operating model | Manutenzione ha capitoli dedicati, ma vista portale e workflow non sono definiti | Handover, recovery, asset lifecycle | Maintenance Owner | Registro manutenzione, incident template, backup evidence, ownership |
| `DSG-OAD-025` | API Gateway exclusion or future scope | Il blueprint precedente citava API Gateway; non esistono API approvate | Evitare architettura generica non necessaria | Architecture Owner | Conferma che non serve, oppure use case reale e ADR |

## Priorita consigliata

| Priorita | Decisioni |
|---|---|
| Alta | `DSG-OAD-003`, `DSG-OAD-004`, `DSG-OAD-007`, `DSG-OAD-008`, `DSG-OAD-010`, `DSG-OAD-011`, `DSG-OAD-022` |
| Media | `DSG-OAD-001`, `DSG-OAD-002`, `DSG-OAD-005`, `DSG-OAD-006`, `DSG-OAD-009`, `DSG-OAD-012`, `DSG-OAD-013`, `DSG-OAD-021` |
| Bassa fino a use case approvato | `DSG-OAD-014`, `DSG-OAD-015`, `DSG-OAD-016`, `DSG-OAD-017`, `DSG-OAD-018`, `DSG-OAD-019`, `DSG-OAD-020`, `DSG-OAD-023`, `DSG-OAD-024`, `DSG-OAD-025` |

## Candidate ADR future

| Candidate | Trigger |
|---|---|
| ADR Scheduler | Scelta tra N.I.N.A. scheduler/plugin, pianificazione documentale o altro modello operativo approvato |
| ADR Session Manifest | Adozione schema manifest come baseline dati |
| ADR Cloud Storage | Scelta provider e modello off-site/retention |
| ADR Knowledge Graph | Scelta modello e storage KG |
| ADR AI Assistant | Approvazione provider, use case, retention e guardrail |
| ADR ASCOM Alpaca | Abilitazione controllo device su rete |

## Riferimenti

- [Logical Architecture](logical-architecture.md)
- [Astronomical Data Architecture](data-architecture.md)
- [Component Registry](component-registry.md)
- [Integration Catalog](integration-catalog.md)
- [Governance](../enterprise/governance.md)
- [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md)
