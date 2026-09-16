# Decision Log

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEC-001 |
| Versione | 2.7 |
| Stato | Active |
| Data baseline | 15/09/2026 |

## 1. Scopo

Registrare decisioni operative, di governance e di implementazione che devono essere tracciate ma non modificano principi architetturali, authority, boundary o invarianti al punto da richiedere un ADR.

## 2. Quando usare il Decision Log

Usare questo registro per decisioni reversibili, circoscritte a processo, naming, organizzazione o implementazione, senza modifica dei contratti pubblici, dei boundary tra layer/bounded context o di safety/security authority e command model.

Creare invece un ADR quando la decisione modifica un principio architetturale, introduce o cambia un boundary, modifica contratti pubblici o compatibilità, introduce una tecnologia strutturale difficilmente reversibile, modifica authority/safety/security/data ownership o condiziona più release/capability.

## 3. Stati

- `Proposed`
- `Accepted`
- `Superseded`
- `Rejected`
- `Retired`

## 4. Registro

| ID | Data | Decisione | Motivazione | Ambito | Stato | Riferimenti |
|---|---|---|---|---|---|---|
| DLG-001 | 04/08/2026 | Il repository GitHub è la fonte autorevole; le conversazioni sono solo contesto ausiliario | Ridurre dipendenza dalla memoria e garantire tracciabilità | Governance | Accepted | `ENTERPRISE_ARCHITECTURE_CONTEXT.md` |
| DLG-002 | 04/08/2026 | Introdurre `docs/project/` come Project Governance Center | Centralizzare baseline, standard, backlog e registri senza duplicare AP/ADR | Documentation IA | Accepted | `docs/project/index.md` |
| DLG-003 | 04/08/2026 | Usare `ENTERPRISE_ARCHITECTURE_CONTEXT.md` come bootstrap di ogni nuova sessione | Prima regola di bootstrap, successivamente sostituita dal root bootstrap universale | Governance | Superseded | Superseded by DLG-010; DSG-CTX-001 resta mandatory context dopo `AI_BOOTSTRAP.md` |
| DLG-004 | 04/08/2026 | Mantenere separati Context, Knowledge Map, Backlog, Technical Debt e Decision Log | Evitare ownership sovrapposte e ambiguità | Governance | Accepted | GP-001 |
| DLG-005 | 04/08/2026 | Il Navigation Manager resta in `page-enhancements.js`; la gestione tema ha un componente dedicato | Applicare responsabilità singola ed eliminare coupling fragile | Portal JS | Accepted | RC1-HF01, TD-001 |
| DLG-006 | 04/08/2026 | Lo Scientific Data Engine è l'unico access layer condiviso per i componenti scientifici del portale | Evitare parsing e accessi paralleli ai dataset | Scientific Portal | Accepted | `scientific-data-engine.js` |
| DLG-007 | 04/08/2026 | I dataset JSON del portale sono proiezioni e non fonti primarie | Preservare data authority e ricostruibilità | Data Governance | Accepted | AP-002, AMP-002 |
| DLG-008 | 04/08/2026 | Il Governance Framework viene completato prima di RC1-HF01 | Stabilizzare contesto e processo prima della hotfix | Sequencing | Accepted | GP-001, RC1-HF01 |
| DLG-009 | 04/08/2026 | I documenti governance vengono creati incrementalmente con commit coerenti | Ridurre rischio e consentire review puntuale | Delivery | Accepted | `DEVELOPMENT_WORKFLOW.md` |
| DLG-010 | 04/08/2026 | `AI_BOOTSTRAP.md` è il punto di ingresso root per persone e assistenti AI | Rendere immediatamente visibile il percorso di lettura e subordinare i documenti di contesto a un entry point universale | Onboarding | Accepted | `AI_BOOTSTRAP.md`; supersedes DLG-003 as entry point |
| DLG-011 | 05/08/2026 | Il Chief Architect AI è autorizzato a utilizzare autonomamente il connettore GitHub fino al completamento del progetto, entro roadmap e boundary approvati | Eliminare approvazioni ripetitive e consentire esecuzione end-to-end delle milestone | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-012 | 05/08/2026 | Le milestone approvate vengono eseguite autonomamente fino alla chiusura tecnica e documentale | Ridurre handoff e mantenere responsabilità unitaria sulla delivery | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-013 | 05/08/2026 | Per file grandi o change set controllati si adottano le Git Database API (`blob -> tree -> commit -> ref`) | Evitare limiti e rischi delle sostituzioni complete tramite Contents API | Repository Operations | Accepted | commit `801c6246983af85fba571515f48fc038cccfcbcf` |

| DLG-014 | 15/09/2026 | Promuovere BKL-031 F3-A1 come package documentale e definire normativamente gli intervalli UTC half-open prima di ogni materializzazione | Rimuovere l'ambiguità di ARB-191-MI02 senza anticipare schema, dati o runtime | BKL-031 F3-A1 | Accepted | F3-A1 handoff/contract/validation plan |
| DLG-015 | 15/09/2026 | Selezionare BKL-031 F3-A2 Setup Authority Contract come successore, iniziando da un Program Assessment/Handoff esclusivamente documentale | Completare in dependency order l'autorità setup dopo il contratto sito, senza anticipare materializzazione, provider o runtime | BKL-031 F3-A2 | Accepted | BKL-031-F3-A2-PROGRAM-001 |
| DLG-016 | 15/09/2026 | Attivare il mandato continuativo `DSG-AEM-001` e la deroga condizionata `W-DSG-AEM-RULESET-001` fino a completamento o revoca | Ridurre handoff autorizzativi mantenendo exact-head CI, review applicabile, rollback, privacy, safety, audit e post-merge | Delivery Governance | Accepted | `DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`; owner authorization 15/09/2026 |
| DLG-017 | 15/09/2026 | F3-A2 usa un reference envelope version-pinned verso una concrete approved baseline, distinta da AP-006 architecture authority e dall'observed state | Risolvere ARB-195-MI01 senza inventare baseline, owner o materializzazione e mantenere S09 fail-closed | BKL-031 F3-A2 | Accepted | `BKL-031-F3-A2-CONTRACT-001`; PR #197; ARB-197 |
| DLG-018 | 15/09/2026 | Accettare F3-A2 come contratto documentale e bloccare la materializzazione finché l'owner non risolve `ARB-197-MI01` | Il repository non determina concrete authority, approval source o prima baseline; mantenerne l'assenza fail-closed evita evidence inventata | BKL-031 F3-A2 | Accepted | `BKL-031-F3-A2-ACCEPTANCE-001`; ARB-197-MI01 |

| DLG-019 | 15/09/2026 | Notificare esplicitamente ogni stop condition prima della pausa, con stato, motivo, lavoro completato, decisione richiesta e criterio di ripresa | Rendere visibili i blocchi e preservare la continuità owner-assistente | Delivery Governance | Accepted | `DSG-AEM-001` v1.1; owner instruction 15/09/2026 |
| DLG-020 | 15/09/2026 | Materializzare il setup authority in un registro GitHub protetto fuori da `docs/`, con Repository Owner come Approval Authority e Architecture Office come custodian senza potere di auto-approvazione | Chiudere la parte authority/source di ARB-197-MI01 mantenendo separate baseline e assignment approval | BKL-031 F3-A2-D1 | Accepted | ADR-009; owner authorization 15/09/2026 |
| DLG-021 | 15/09/2026 | Registrare l’approvazione owner dell’exact payload `[protected digest recorded outside docs]` tramite receipt separata e promuovere solo l’envelope a `APPROVED` | Preservare immutabilità, audit e separazione dall’approvazione del site assignment | BKL-031 F3-A2-D2 | Accepted | PR #201; ADR-009; `DSG-SETUP-BASELINE-001-APPROVAL-001` |
| DLG-022 | 15/09/2026 | Accettare F3-A2-D2 dopo il merge/post-merge di PR #201 e selezionare F3-A1-M1 come prossimo owner decision gate | La baseline setup è integrata, ma sito e assignment restano authority separate; le coordinate protette e le semantiche aperte non possono essere inferite | BKL-031 F3-A1-M1 | Accepted | PR #201; `BKL-031-F3-A2-D2-ACCEPTANCE-001`; `BKL-031-F3-A1-M1-PROGRAM-001` |
| DLG-023 | 15/09/2026 | Registrare nel protected GitHub registry i fatti sito forniti dall'owner, con WGS84 decimal degrees, quota ortometrica MSL, timezone governata, validità unbounded e pubblicazione limitata alla generalizzazione comunale | Chiudere F3-A1-M1 senza inferire dati da telemetria, mappe o setup baseline e senza esporre coordinate, quota o indirizzo esatto | BKL-031 F3-A1-M2 | Accepted | owner-controlled source decision 15/09/2026; F3-A1 contract |
| DLG-024 | 15/09/2026 | Materializzare prima un record `DRAFT` ineligible e richiedere in seguito una distinta approvazione owner legata al digest canonico esatto | Separare autorizzazione alla registrazione, approvazione del payload e futura assegnazione; impedire che una generica autorizzazione di scrittura promuova il lifecycle | BKL-031 F3-A1-M2 | Accepted | protected decision evidence; ADR-009; DSG-AEM-001 |
| DLG-025 | 15/09/2026 | Accettare la decisione owner vincolata all'exact digest e alla validità unbounded e promuovere il Site Authority tramite receipt protetto ed envelope APPROVED separato, senza mutare il payload | Completare F3-A1 rispettando immutabilità, privacy, separazione dall'assegnazione e potere di approvazione esclusivamente umano | BKL-031 F3-A1-M3/M4 | Accepted | owner-controlled approval; F3-A1-M4 evidence; ADR-009 |
| DLG-026 | 15/09/2026 | Accettare F3-A1-M4 dopo PR #204 e selezionare F3-A2-D3 come owner decision gate separato per `CurrentSetupAssignment` | Site Authority e setup baseline sono approvati ma nessuna relazione current può essere inferita; mantenere S09 fail-closed preserva authority e approval separate | BKL-031 F3-A2-D3 | Accepted | PR #204; F3-A1-M4 acceptance; F3-A2-D3 assessment; ADR-009 |
| DLG-027 | 15/09/2026 | Registrare per il futuro `CurrentSetupAssignment` il registro GitHub protetto, Repository Owner come owner/Approval Authority, Architecture Office come custodian non approvatore e validità unbounded dalla baseline setup | Chiudere il gate decisionale senza inferire o approvare la relazione sito-baseline e mantenere DRAFT, approval e runtime come incrementi separati | BKL-031 F3-A2-D3/D4 | Accepted | owner decisions 15/09/2026; ADR-009; F3-A2-D3 decision; F3-A2-D4 handoff |

## 5. Delega operativa GitHub

La delega comprende, entro lo scope approvato: lettura e ricerca nel repository; creazione/aggiornamento/ritiro di file; commit e aggiornamenti fast-forward; controllo GitHub Actions, job, log e artifact; verifica GitHub Pages; correzione autonoma di errori coerenti con la milestone; review AI-assistite; merge condizionati; post-merge verification; aggiornamento dei registri di governance. `DSG-AEM-001` è la definizione operativa corrente.

Richiedono sempre approvazione esplicita: force push o aggiornamento non fast-forward; operazioni distruttive non previste; ampliamento dello scope o deviazione dalla roadmap; nuove integrazioni o dipendenze strutturali; cambi di boundary, authority, safety, security o contratti pubblici.

## 6. Relazioni con altri registri

- un compromesso accettato con costo futuro va in `TECHNICAL_DEBT.md`;
- un'attività da eseguire va in `BACKLOG.md`;
- un difetto va nel sistema di issue/bug tracking;
- una decisione strutturale va in un ADR;
- una variazione di roadmap va prima nella source governata applicabile e poi nelle proiezioni.

## 7. Review 08/09/2026

La closure BKL-040 e la promozione dependency-driven di BKL-038 non introducono una nuova decisione architetturale: applicano dipendenze e governance già approvate. La review elimina invece l'ambiguità storica tra DLG-003 e DLG-010: `AI_BOOTSTRAP.md` è l'unico root entry point; Enterprise Architecture Context e Repository Knowledge Map restano documenti obbligatori nella sequenza di bootstrap.

| DLG-028 | 15/09/2026 | Materializzare F3-A2-D4 come DRAFT protetto, immutabile e resolver-ineligible con schema decisionale chiuso, schema assignment, canonicalizzazione, validator e test | Implementare unicamente quanto determinato da ADR-009 e dalle decisioni owner, preservando l'approvazione exact-digest come successivo atto umano separato | BKL-031 F3-A2-D4 | Accepted | PR #207; merge `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b`; 7/7 post-merge workflows |
| DLG-029 | 15/09/2026 | Fermare la progressione del lifecycle al gate di approvazione umana dell'exact digest protetto | CI, review AI-assistite e merge non equivalgono all'approvazione umana obbligatoria; receipt e promozione restano separati | BKL-031 F3-A2 | Resolved | owner exact-digest approval 15/09/2026; ADR-009; PR #207 post-merge evidence |
| DLG-030 | 15/09/2026 | Registrare l'approvazione owner dell'exact assignment digest nel registro protetto e promuovere un envelope separato a `APPROVED` senza modificare payload o digest | Rendere auditabile l'atto umano, preservare immutabilità e mantenere runtime/Safety separati | BKL-031 F3-A2-D5 | Accepted | owner-controlled approval; PR #209; merge `bc4307c2042a45985622044e11631421de5b2c3d`; F3-A2-D5 evidence |

| DLG-031 | 15/09/2026 | Accettare F3-A2-D5 dopo exact-head review, expected-head merge e 7/7 post-merge workflow; mantenere la disponibilità limitata al repository e sottoporre il successore al Program Architect | La repository authority è completa, ma il runtime adapter non esiste e non può essere inferito dalla disponibilità repository | BKL-031 post-D5 | Accepted | PR #209; merge `bc4307c2042a45985622044e11631421de5b2c3d`; `ARB-204-MI02`; D5 acceptance reconciliation |

| DLG-032 | 15/09/2026 | Selezionare F3-A3 Method ADR and validation spike come successore dependency-ready, iniziando da un handoff esclusivamente documentale | F3-A1/A2 hanno completato le autorità repository e F3-B dipende da una decisione metodologica accettata; il handoff prepara i gate senza scegliere provider o introdurre runtime | BKL-031 F3-A3 | Accepted | `BKL-031-F3-A3-PROGRAM-001`; PR #210; F3-OD04–F3-OD10 |

| DLG-033 | 15/09/2026 | Avviare F3-A3 come decision-preparation package composto da Solution Architecture, ADR-010 proposto e validation-spike plan non eseguito | Rendere F3-OD04–F3-OD10 decision-ready senza trasformare una raccomandazione in selezione di provider o autorizzazione allo spike | BKL-031 F3-A3 | Accepted | `BKL-031-F3-A3-SOLUTION-001`; `ADR-010`; `BKL-031-F3-A3-VAL-001`; PR #211 |

| DLG-034 | 15/09/2026 | Registrare la baseline prudente F3-A3 e preparare un host Google Cloud Run Job isolato tramite Terraform e GitHub OIDC/WIF, mantenendo F3-OD05 aperto | Rendere eseguibile il prossimo incremento senza chiavi statiche, costi di VM idle o accoppiamento con EAGLE/N.I.N.A.; impedire apply e spike fino al kernel esatto | BKL-031 F3-A3 | Partially Accepted | `ADR-010`; `BKL-031-F3-A3-OD-2026-09-15`; `BKL-031-F3-A3-INFRA-001` |

| DLG-035 | 16/09/2026 | Approvare F3-OD05 con l'identità immutabile `de442s.bsp`, copertura, catene SPICE, provenienza NAIF, MD5, SHA-256 e URI privata content-addressed | Chiudere la scelta proprietario del kernel senza trasformarla in autorizzazione a upload, Terraform o validazione scientifica | BKL-031 F3-A3 | Accepted at decision level | `BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16`; `ADR-010`; ARB-213-MI01/MI02 restano aperti |


| DLG-036 | 16/09/2026 | Materializzare i valori approvati F3-OD04–F3-OD10 nel profilo immutabile `BKL-031-F3-A3-METHOD-PROFILE-001` con SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca` e preflight fail-closed | Eliminare la duplicazione dei limiti runtime e fornire evidence statica ARB-213-MI01 senza costruire o eseguire container | BKL-031 F3-A3 | Accepted at repository-contract level | `ADR-010`; `ARB-213-MI01`; container/IERS/cloud/scientific evidence remain open |

| DLG-037 | 16/09/2026 | Applicare l'exact saved bootstrap plan `9bf2804a…`, migrare immediatamente lo state in GCS e fermarsi sul mismatch seriale previsto dal runbook | Materializzare il bootstrap autorizzato mantenendo 0 update/0 destroy e applicare fail-closed alla prima divergenza; correggere la regola MI02 al persist remoto `serial +1` solo con lineage e managed content invariati | BKL-031 F3-A3 | Applied / post-promotion verified | `main@af8b18f2…`; `ARB-213-MI02-I01`; PR #219; merge `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60` |

| DLG-038 | 16/09/2026 | Dichiarare ARB-213-MI02 soddisfatta dopo permanent-backend promotion, remote-state identity check, recovery-candidate read-only, locking check e zero-drift exit code `0` | Chiudere il lifecycle bootstrap con evidenza attribuibile senza estendere l'autorizzazione a platform apply, upload, container o campagna scientifica | BKL-031 F3-A3 | Accepted / post-promotion verified | PR #219; merge `6c6a9454f1f1f13f72b4ae5098c0f2475b537d60`; generation `1789570006160390`; plan transcript `5268bf29…` |
