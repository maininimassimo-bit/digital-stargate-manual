# Technical Debt Register

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.10 |
| Stato | Active |
| Data review | 23/09/2026 |

## 1. Scopo

Registrare esclusivamente debito tecnico noto, accettato e tracciato. Problemi operativi, difetti aperti e attività pianificate appartengono rispettivamente a incident management, bug tracking e backlog.

## 2. Regole

Ogni voce deve includere: identificativo, descrizione, causa, impatto, rischio, area, priorità, owner, strategia di rimozione, dipendenze, stato e data di revisione.

Stati ammessi: `Proposed`, `Accepted`, `Mitigated`, `Scheduled`, `Resolved`, `Rejected`. Priorità: `P0` critica, `P1` alta, `P2` media, `P3` bassa.

## 3. Registro

| ID | Area | Debito | Impatto/Rischio | Priorità | Stato | Strategia / evidence |
|---|---|---|---|---|---|---|
| TD-001 | Portal Theme | Gestione tema accoppiata al DOM interno di Material in `page-enhancements.js` | Pulsante fragile e responsabilità errata | P0 | Resolved | WP-03 Enterprise Theme Framework `Completed / Accepted`; Theme Service centralizzato in `dsg-theme-manager.js` |
| TD-002 | Portal JS | Presenza di logica inline in alcune pagine | Duplicazione, coupling e incompatibilità con Instant Navigation | P1 | Resolved | JavaScript eseguibile inline eliminato; gate `verify-no-inline-portal-js.mjs`; BKL-010 closure 30/08/2026 |
| TD-003 | Repository Entry Point | README root descriveva soprattutto il manuale storico | Onboarding incompleto | P1 | Resolved | README root riallineato alla piattaforma; BKL-008 closure 29/08/2026 |
| TD-004 | CI/CD | Coesistenza di workflow documentali attivi, disabilitati e storici | Ownership ambigua | P1 | Resolved | `deploy-pages.yml` unico owner Pages; `docs.yml` validation-only; BKL-007 closure |
| TD-005 | Projections | Roadmap e dashboard JSON possono divergere dalle fonti autorevoli | Stato visualizzato obsoleto | P1 | Resolved | Consistency gate AMP-002/roadmap/backlog attivo nel Developer Foundation; BKL-009 Done |
| TD-006 | Documentation IA | Project Governance Center non integrato nella nav MkDocs | Documenti canonici difficili da scoprire | P1 | Resolved | `mkdocs.yml` include Project Governance; BKL-002 Done |
| TD-007 | Release History | Guide e release storiche in root non sempre contestualizzate | Possibile confusione con baseline corrente | P2 | Accepted | Creare indice storico e dichiarare stato/supersession — BKL-016 |
| TD-008 | Knowledge Traceability | Collegamenti AP/ADR/componenti/evidence non machine-readable | Analisi manuale e rischio di gap | P2 | Resolved | BKL-015 F1-F3 accepted; merge F3 `c1a9f96b34a23407c5804e7fd6facfbad226f8fc` |
| TD-009 | EAGLE Reporting Automation | Launcher EAGLE inizialmente non governato dalla source of truth | Configuration drift | P1 | Mitigated | Runtime inspection, SHA/task definition e AP-014 OAT completati; mantenere change control |
| TD-010 | EAGLE Session Launcher | Un'eccezione dopo la creazione del session branch può lasciare il runtime clone fuori da `main` | Preflight successivo fail-closed e recovery manuale | P1 | Accepted | Introdurre restore-to-main governato in `finally` o equivalente, senza reset distruttivi; regression test obbligatorio |
| TD-011 | Reporting CI | Copertura quality gate 1.0.7/1.0.8 non ancora riconciliata formalmente con tutti i check storici pre-remediation | Possibile perdita silenziosa di controlli | P2 | Accepted | Confrontare gate storico/corrente e ripristinare check applicabili con workflow evidence |
| TD-012 | BKL-040 Timeline Contract | F2 accepted contract non riproduce tutti i minimum-envelope field dichiarati in F1 e usa il proprio tie-break deterministico basato su `replay_event_id` anziché il F1 `source_event_id` | Futuri consumer possono assumere una envelope uniforme inesistente o introdurre incompatibilità retroattiva | P2 | Accepted | Non retrofit silenzioso della F2 accepted baseline. Qualunque normalizzazione deve essere un incremento/versione compatibile, con migration contract, fail-closed tests e ARB review. Closure BKL-040 documenta esplicitamente il boundary. |

## 4. Criteri di rimozione

Una voce può essere chiusa solo quando la modifica è implementata, i test applicabili sono eseguiti, non sono introdotti debiti equivalenti, documentazione/backlog/decision log sono aggiornati o verificati non applicabili ed esiste evidence verificabile.

## 5. Review 08/09/2026

La review riconcilia il registro con BKL-040 e le foundation precedenti:

- TD-001–TD-006 e TD-008 restano `Resolved`;
- TD-007, TD-010 e TD-011 restano `Accepted`;
- TD-009 resta `Mitigated`;
- viene registrato **TD-012** per rendere esplicita la compatibilità bounded tra BKL-040 F1 e l'accepted F2 contract, evitando di nascondere o retrofittare il debito durante la closure;
- TD-012 non mette in discussione l'acceptance F2/F3/F4: governa una futura eventuale normalizzazione compatibile;
- la copertura eseguibile BKL-040 resta bounded: NINA/PHD2/CloudWatcher e session projection dove definita; nessuna dichiarazione implicita di materializzazione Power/Network/Safety;
- nessuna nuova authority, command path, remediation authority o Safety Authority coupling viene introdotta dalla closure.

## Review 23/09/2026 — RC2 closure

La chiusura RC2 non introduce nuovo debito tecnico e congela la compatibilità RC1. Il lavoro successivo AP-015 è registrato come preparazione architetturale/semantica; eventuale selezione tecnologica, materializzazione runtime, provider o AI execution dovrà essere valutata come incremento separato con propri gate e review.


## Review 30/09/2026 — BKL-049 F0 acceptance

[Phase acceptance](BKL-049-F0-ACCEPTANCE-2026-09-30.md) transfers the demonstrated identity/digest/duplicate, source retention, privacy and PXP mapping gaps to explicit F1/F4/F5 acceptance obligations. They are not silently repaired or waived; no production component is introduced. ARB M01 stale ADR-008 status wording is corrected by this reconciliation. Existing debt dispositions remain unchanged.

## Review 2026-10-05 — continuità M27 e pilota locale

La riconciliazione corregge i punti d’ingresso obsoleti. History disponibile incompleta, replay non garantito e worker/coda/IA di produzione assenti sono limiti e lavoro pianificato espliciti nel [piano pilota](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md), non debiti dichiarati risolti. Le disposition TD esistenti restano invariate.

### 2026-10-05 — P2 local boundary

P2 adds a tested local coordinator and fixed linear executor; remote queue/model and full nonlinear pipeline remain planned. Crash recovery intentionally retains the reservation and requires confirmed stopped execution plus quarantine/new root; there is no expiry, automatic retry or forced unlock. This bounded pilot does not resolve production availability/recovery or scientific quality gaps. Existing TD dispositions remain unchanged.

### 2026-10-05 — P3 bounded nonlinear recipe

P3 supplies one M27-specific empirical recipe, not a universal image-planning model or production service. Compression/unsupported XISF layouts are rejected by pixel validation; model/version/license identity and commercial rights remain unverified. Pixel checks and visual comparison do not certify scientific effectiveness or no clipping. P4–P6 and all existing TD dispositions remain open/unchanged as applicable.

### 2026-10-05 — P4 transport candidate

Authenticated queue/client candidate does not resolve production cloud availability, identity provisioning, licensed commercial rights or native end-to-end recovery. SESSION_ASSISTED has zero new paid AI API calls and requires an active supervised conversation/operator. New cloud resources, dedicated credential, cloud restore/OAT and P5/P6 remain gated. Existing TD dispositions unchanged.

### 2026-10-05 — P4 approved deployment, partial live OAT

Resource/credential approval satisfied and bounded service deployed. Real PC HTTPS/role/root denial established. Owner Google authentication and bounded administrative native transport OAT are now proven; administrative GCS concurrent CAS is proven, while concurrent Owner HTTP operations remain synthetic. Broader operational acceptance, P5/P6 and scientific acceptance remain open; no production completion claimed. Infrastructure costs remain possible; no hard spending cap. Existing debt dispositions unchanged.

### 2026-10-05 — P4 bounded live/native OAT

Autenticazione Google Owner reale PASS sulla pagina diagnostica: creazione sintetica, ripetizione idempotente, annullamento e lettura CANCELLED/NONE. Google valido non-Owner negato e stale-create CAS reale negato senza mutazione. Riavvio del servizio sullo stesso digest e perdita deliberata dell’ack PREPARING dopo commit remoto: stessa richiesta recuperata, una preparazione; ciclo ripetuto con otto file identici.

Trasporto nativo sul PC verificato con due fixture amministrative isolate: pre-cancel con zero processi/output; M27 non lineare COMPLETED con 29 azioni, 15 checkpoint e 29 istanze workflow, originali invariati, finale Float32 RGB 4634×2808 e tutti i pixel finiti in [0,1]. Clipping misurato, non certificato assente. Raccolta dopo arresto PixInsight, prenotazioni chiuse e report remoto verificato. Questa prova usa Broker/BackedUpStore tramite CLI Owner amministrativa: non attesta ancora la creazione di un job scientifico dal comando HTTP/UI Owner. La prova HTTP Owner separata è sintetica; executionEvidence resta WORKER_REPORTED_NOT_ATTESTED, publication=NONE.

P4 ha ora una prova tecnica nativa circoscritta; CAS GCS concorrente reale PASS tramite CLI Owner amministrativa: due scritture degli stessi bytes di coda terminale, una accettata e una rifiutata per generazione obsoleta, backup verificato e stato logico invariato. Concorrenza sulle route Owner HTTP soltanto sintetica; acceptance operativa più ampia resta aperta. P5 comando scientifico/sessioni/preview/provenance, P6 e acceptance scientifica Owner sono successivi. SESSION_ASSISTED, zero nuove chiamate API IA; M27 pubblicata e autorità dispositivi/Safety invariate. Evidenza privata conservata; ricevuta pubblica minimizzata e runbook collegati sopra. CI/review/merge e Pages di questa riconciliazione sono da verificare sulla PR di consegna.

Osservazione reale dopo oltre 120 secondi senza contatto: OFFLINE diagnostico, stesso job/root ancora RUNNING, nessuna scadenza o riassegnazione osservata. Non è una prova di crash recovery del desktop.

Derivati locali TIFF RGB16/JPEG sRGB verificati; soluzione astrometrica conservata e checkpoint invariato dopo export. History disponibile: 13 viste, 47 passi, 82 istanze, 429679 byte; importer 1.2 PARSED_SUBSET. La History conservata non prova completezza a monte: executionEvidence=NOT_ESTABLISHED e workflowCompleteness=UNAVAILABLE del file importato restano invariati. Journal e correlazioni runtime delle 29 azioni conservati separatamente. Campo intero/dettaglio coerenti con la ricetta P3; nessuna superiorità scientifica o sostituzione pubblica dichiarata.
