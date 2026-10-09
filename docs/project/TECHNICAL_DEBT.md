# Technical Debt Register

## BKL-051 — residui di validazione, 8 ottobre 2026

L’[ispezione proposta delle evidenze](BKL-051-S1-MEASUREMENT-EVIDENCE-2026-10-08.md) non introduce un runtime operativo. Parser di trasporto stretto, verifica indipendente delle dichiarazioni/byte, modello completo di incertezza, gestione delle sorgenti confuse, validazione dei falsi positivi e adapter privato rimangono acceptance gate S1–S5, non capacità completate o fallback impliciti. Nessuna soglia numerica accettata, nessuna nuova infrastruttura o deroga ai gate. P6 resta Accepted nei propri limiti.

## Riesame del 7 ottobre 2026

L'inserimento di [BKL-051](BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md) è pianificazione e non introduce codice o nuovo debito implementativo. Copertura dei provider, comparabilità fotometrica, falsi positivi, soglie scientifiche e scelte infrastrutturali restano decisioni e gate S1 del piano, da validare dopo P6; non sono debiti dichiarati risolti. Il registro esistente resta invariato.


> Stato corrente al 6 ottobre 2026: [gate residui e baseline](CURRENT_TECHNICAL_BASELINE_2026-10-06.md). Le sezioni precedenti conservano gli snapshot e i limiti delle prove; le note di candidato o consegna pendente sono superate soltanto nei perimetri del riepilogo corrente.

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.14 |
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


## Aggiornamento P5 — portale scientifico privato (2026-10-05)

Implementato il candidato P5: pagina Owner, selezione di master M27 registrati, sessioni/catalogo e versione di riferimento esatti; job con contesto immutabile e verifica sul PC prima delle copie; stato/cancel espliciti, preview privata, workflow delle 29 azioni, correlazioni runtime e revisione Owner vincolata alla ricevuta. Originale e journal completo restano sul PC. Le identità IMG/VER/WF del pilota sono private e distinte dall’archivio di pubblicazione; nessun caricamento o pubblicazione automatica. SESSION_ASSISTED senza nuove API IA; classificazioni WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e History a monte NOT_ESTABLISHED preservate. Release/deployment consegnati tramite #485; la prova scientifica reale HTTP/UI → PixInsight → consegna/revisione resta un gate P5 aperto, non sostituito dai test. P6 e acceptance scientifica Owner restano successivi. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md).

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json).


## P5b — cartella dei master e prompt (candidato del 5 ottobre 2026)

Incremento autorizzato dall’Owner dopo l’accettazione privata P5 e la conferma dei download. Il modulo aggiunge cartella locale assoluta e prompt, richiesta privata di pianificazione, verifica esplicita sul PC, proposta immutabile e conferma Owner dell’esatto piano prima della coda PixInsight. Nessun job alla sola ricezione del prompt; nessuna lettura automatica del disco o esecuzione di testo/script dal browser. SESSION_ASSISTED: questa sessione interpreta il prompt e propone ricetta, parametri ammessi di fondo, dettaglio, rumore, contrasto e stretch, motivazione e limiti; nessuna nuova API IA, risorsa, credenziale o espansione IAM. Il perimetro richiesto include altri oggetti importati, LRGB, OSC, SHO/HOO e mosaici da pannelli. Il candidato comprende inventario e selezione esplicita; le nuove ricette per campo singolo richiedono parametri di campo verificati. OSC CFA e assemblaggio mosaici restano bloccati fino a implementazione e collaudo nativo. [Stato e procedura](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md). Nessuna estensione è ancora pubblicata o dichiarata accettata.

Il piano conserva ruoli R/G/B/L, dimensioni, selezione esplicita dell’immagine nei contenitori, impronta del manifest e sequenza dei 29 processi. Cartella, prompt e piano sono dati privati Owner; master/hash individuali e diagnostica locale restano sul PC. Il worker confronta cartella, piano e manifest prima delle copie. Aggiornamenti di catalogo o riferimenti conflittuali fermano l’approvazione; retry identici non duplicano richieste/job. I vecchi risultati P5 rimangono accessibili e invariati. Il candidato richiede CI sull’head esatto, ARB/RQ sequenziali, merge, deployment API/Pages e prova Owner della nuova procedura; non è ancora dichiarato disponibile nel portale pubblico. P6 e acceptance operativa restano aperti.


## P6 — residui operativi e limiti riconciliati

Owner approva servizio, due bucket privati, identità e credenziale di prova dedicate. Ambiente cloud isolato attivo sul digest già rilasciato; concorrenza Owner e recupero nativo cloud reali ancora da eseguire. CFA/SHO reali e download CFA riconciliati con limiti espliciti. P6 resta aperta; accettazione operativa finale pendente. Nessuna mutazione del pilota operativo, gallery, dispositivi o Safety. BKL-051 Planned dopo chiusura P6. Piano corrente: [PIAI-P6-ISOLATED-OAT-2026-10-07.md](PIAI-P6-ISOLATED-OAT-2026-10-07.md)

## P6 — collaudo completo, accettazione operativa pendente

Concorrenza Owner HTTPS reale, interruzione nativa isolata e nuovo worker, offline oltre 120 s, restart/rollback/forward del servizio di prova: PASS nei limiti documentati. Ambiente sospeso, archivi e prenotazioni conservati; stato della coda operativa byte-identico al baseline. HOO nativo sui master reali Drizzle2 ora PASS tecnico: 26 processi, 14 checkpoint, 26 coppie History, originali invariati; non accettazione estetica. P6 resta aperta per accettazione operativa; CFA è fixture tecnica da singola esposizione con decisione scientifica pendente. BKL-051 Planned dopo chiusura P6; F4/F5 e BKL-050 invariati. [Dossier finale e limiti](PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md). Questa nota supera soltanto i residui tecnici provati, conserva snapshot e gate di consegna.

## P6 — accettazione operativa Owner

L’Owner conferma «Accetto operativamente P6 con i limiti del dossier». Nessuna esclusione HOO: collaudo nativo completato. Accettazione distinta da valutazione estetica e pubblicazione; CFA resta prova tecnica su singola esposizione, History a monte non attestata e recupero soltanto conservativo. [Chiusura](BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md), [handover](HANDOVER_2026-10-07-P6-CLOSURE.md). Gate di consegna exact-head e post-merge nella PR #499; nessun PASS anticipato.


## BKL-051 S1 — preparazione autonoma del 7 ottobre

P6 delivery verificata sulla PR #499 e sul merge `0bd6e20df0b449cd163543ed30bd69d9264862b0`: 16/16 workflow post-merge SUCCESS incluse Pages e proiezioni pubbliche conformi. [Handover corrente](HANDOVER_2026-10-07-BKL051-S1.md), [fattibilità e contratto proposto](BKL-051-S1-FEASIBILITY-AND-CONTRACT-2026-10-07.md). Accessi pubblici limitati verificati, tentativi negativi conservati, nove test di intake offline. S1 non accettata: decisioni su architettura/trasporto, query minime su campi Owner e dataset pilota ancora pendenti. Nessuna soglia, analisi Owner, runtime o foto pubblicata. Le sezioni precedenti restano snapshot storici.

## BKL-051 — 8 ottobre 2026: incertezza proposta

[Contratto offline](BKL-051-S1-UNCERTAINTY-CONTRACT-2026-10-08.md) con dati ignoti espliciti, covarianze e controllo del doppio rumore di lettura. Nessuna accettazione di modello completo, soglia, classificazione o runtime; residui scientifici e di trasporto invariati. La prova numerica non chiude BKL-051.

## BKL-051 — propagazione d’epoca proposta, 8 ottobre 2026

[Modello e verifiche](BKL-051-S1-EPOCH-MODEL-2026-10-08.md): sette test aggiuntivi e sei controlli numerici ESA, senza accettazione del matching o covarianze. Prosecuzione autonoma e revisioni ARB/RQ autorizzate; trasporto concreto e policy scientifica restano decisioni separate.

## BKL-051 — trasporto concreto approvato, 8 ottobre 2026

[Decisione Owner](evidence/BKL-051-OWNER-TRANSPORT-2026-10-08.json) e [coda candidata](BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md). Implementazione separata e collaudi locali; attivazione, IAM/credenziale dedicata e percorso S4 completo ancora da verificare. Nessuna soglia/acceptance scientifica, nuova risorsa o fotografia pubblicata. Le precedenti decisioni pending sono snapshot superati soltanto per la scelta di trasporto.

## BKL-051 — segnalazioni approvate nello scope, 8 ottobre 2026

[Piano](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md) e [evento Owner](evidence/BKL-051-OWNER-REPORTING-SCOPE-2026-10-08.json). Dossier, oggetti mobili, invio assistito e capacità autonoma condizionata sono requisiti da realizzare nella milestone. Adapters, formati, identità/credenziali, riconciliazione di esito e collaudi restano aperti; nessun invio attivo o policy quantitativa accettata. Rollback dei futuri invii conserva ledger/ricevute e non ritira automaticamente quanto già consegnato.

## BKL-051 — origini pixel e misure raccordate, 8 ottobre 2026

[Contratto proposto](BKL-051-S2-PIXEL-CONVENTION-2026-10-08.md): unità/origini esplicite, nessuna API attestata dal solo input dichiarato. Tre fixture native e due known-answer di apertura, vecchi export/misure conservati; ensemble comune raccordato per identità. Doppio/mancato offset risolto nel ramo corretto; budget dipendenti dalle aperture e covarianze complete ancora aperti. 55 test offline locali; CI/review/post-merge nella PR, non acceptance scientifica. Coda/invii rimangono disabilitati.

## BKL-051 — registro locale e budget parziali, 8 ottobre 2026

[Library e limiti](BKL-051-S4-LOCAL-EVIDENCE-REGISTRY-2026-10-08.md): verifica dei byte puntuale, manifest/receipt esclusivi privati; non execution snapshot, native journal o attestazione scientifica. Budget corretti raccordati senza promuovere sky-only a varianza completa. Restano adapter/report/UI/OAT e scientific noise/covariance validation; CI/review/post-merge nella PR, non acceptance.

## BKL-051 — snapshot/journal tentativi e teardown, 8 ottobre 2026

[Incremento candidato](BKL-051-S4-ATTEMPT-JOURNAL-2026-10-08.md): copie verificate, eventi esclusivi, parametri/runtime/checkpoint/History correlati e rapporto tecnico; receipt caller-reported, non native attestate. Bridge MemoryStore non trasporto operativo. Restano producer/coordinatore/outbox/report scientifico/UI/OAT e validation; native/rates/policy non dedotti. Handler condiviso gestisce diniego TCP con scarto raw bounded dopo 403; auth invariata, nessun deployment.

## BKL-051 — coordinatore ricevute, 8 ottobre 2026

[Library/loopback candidati](BKL-051-S4-RECEIPT-COORDINATOR-2026-10-08.md): outbox senza credenziali, GET worker dedicata e ACK dell'envelope completo; perdita risposta e restart conservati senza rilancio. Restano producer/cancel/crash/recovery operativa, scientific report/UI/cloud OAT e scientific validation/reporting. Nessuna attivazione o soglia/acceptance.

## BKL-051 — produttore nativo, 8 ottobre 2026

[Adapter e collector candidati](BKL-051-S4-NATIVE-APERTURE-2026-10-08.md): kernel installato, unità normalizzate e History/receipt conservate. Prove numeriche native e MemoryStore locale, non full workflow scientifico/cloud OAT. Restano supervisore operativo, recovery, report/calibrazione/variance/policy/UI e reporting. Nessuna attivazione o acceptance finale.

## BKL-051 — supervisore nativo, 8 ottobre 2026

[Lifecycle candidato](BKL-051-S4-NATIVE-SUPERVISOR-2026-10-08.md): avvio dopo ACK, handle corrente, cancel al punto sicuro; timeout/receipt mancanti non autorizzano terminate/replay. Prove componente native e MemoryStore, non cloud OAT o validazione scientifica. Restano driver/recovery/UI/OAT e workflow/report/variance/policy/reporting completi.

## BKL-051 — consultazione Owner, 8 ottobre 2026

[Vista candidata](BKL-051-S4-OWNER-EVIDENCE-VIEW-2026-10-08.md): solo GET manuale e ricevuta minimizzata, senza verifica del rapporto locale o attestazione scientifica. UI logged-out locale e contratti sintetici, non cloud OAT. Restano percorso selezione/decisione/report completi, driver/recovery, accessi/PC/cloud e validation/reporting.

## BKL-051 — comandi Owner, 8 ottobre 2026

[Incremento candidato](BKL-051-S4-OWNER-ACTIONS-2026-10-08.md): contratti di coda esistenti, selezione esplicita e intent immutabile conservato prima del POST, riconciliazione dopo lost-ack e dichiarazione Owner sul report esatto. Nessun runtime/claim/query/invio. Storage per sessione/tab, non backup durevole; recovery e cloud OAT pendenti.


## BKL-051 — rapporto locale, 8 ottobre 2026

[Incremento candidato](BKL-051-S4-LOCAL-REPORT-2026-10-08.md): esportazione passiva privata del journal sigillato, digest tecnico distinto dal derivato, misure del kernel e limiti conservati. Non modifica coda/authority o acceptance. Driver/recovery, workflow scientifico completo, OAT e reporting restano aperti; nessun nuovo collaudo nativo o attivazione. Gate nella PR.


## BKL-051 — driver locale candidato, 8 ottobre 2026

PR #515 integrata e post-merge verificata; [driver locale e riconciliazione](BKL-051-S4-LOCAL-DRIVER-2026-10-08.md) candidati per una prenotazione fornita dal chiamante fidato. Nessun claim, replay, credenziale su disco o reset della recovery server; ACK storico distinto dallo stato corrente. Tredici test mock/MemoryStore, non OAT nativa/cloud. Claim sicuro e recovery server restano aperti insieme al workflow scientifico, policy, reporting e acceptance. Runtime/invii disattivati; BKL-051 OPEN. Gate exact-head nella PR; rollback conservativo tramite revert, nessun cleanup delle evidenze.


## BKL-051 — prenotazione esplicita candidata, 9 ottobre 2026

PR #516 rilasciata e verificata. [Intent di prenotazione](BKL-051-S4-RESERVATION-INTENT-2026-10-09.md) candidato: selezione esplicita, singola POST, nessun lease su duplicazione o replay dopo incertezza. Recovery server e requisiti scientifici/OAT restano aperti; nessuna attivazione runtime o invio. Gate exact-head pending. BKL-051 OPEN.


## BKL-051 — recovery Owner candidata, 9 ottobre 2026

PR #517 rilasciata e verificata. [Recovery dichiarata](BKL-051-S4-OWNER-RECOVERY-2026-10-09.md) approvata come modalità dall’Owner: conserva RECOVERY_REQUIRED e consente solo nuovi job distinti, nessun replay o process kill. Gate release pending. RQ517 P3 conteggio test corretto in questo incremento. Caller/OAT, scientific workflow, validation/policy e reporting restano aperti; runtime e invii disattivati. BKL-051 OPEN.

## BKL-051 — caller locale candidato, 9 ottobre 2026

PR #518 recovery Owner rilasciata e verificata. [Caller locale](BKL-051-S4-OPERATOR-CALLER-2026-10-09.md) per un job selezionato, preflight offline e intento conservato; 15 prove sintetiche, release pending. Nessuna attivazione/credenziale/IAM o misura scientifica nuova. PC/cloud OAT, workflow scientifico, validation/policy, oggetti mobili e reporting restano aperti; BKL-051 OPEN.

## BKL-051 — dossier preliminare candidato, 9 ottobre 2026

PR #519 caller rilasciata, 15 workflow post-merge e sette endpoint verificati. [Dossier privato candidato](BKL-051-S4-REPORTING-DRAFT-2026-10-09.md): solo DRAFT e 12 prove sintetiche; nessun invio, validazione o authority derivata. Build proposta privata pending; PC/cloud OAT, scientific validation, moving objects e reporting produttivo restano aperti.

## BKL-051 — build verificata, OAT preparato, 9 ottobre 2026

PR #520 dossier DRAFT rilasciata e verificata. [Build/OAT](BKL-051-S4-BUILD-READINESS-2026-10-09.md): due tentativi autorizzati separatamente, primo fallito conservato, secondo SUCCESS 155/155 prove offline/digest immutabile. Runtime P6 invariato, attivazione proposta privata pending. [Dataset pubblico Atami](BKL-051-S3-MOVING-DATASET-PREPARATION-2026-10-09.md) preparato senza misure o validazione. OAT reale, pipeline scientifica, policy/moving/reporting produttivo ancora aperti; nessuna chiusura BKL-051.

## BKL-051 — diagnostica nativa non validata, 9 ottobre 2026

[Atami](BKL-051-S3-NATIVE-DIAGNOSTICS-2026-10-09.md): V3 INVALID per offset signed FITS provato su tutti i pixel; segnale e originali invariati. V4 path error conservato, esecuzione/fermata non confermate; genitore 49 file salvati/verificati, V5 solo preparato. Nessun nuovo lancio prima della verifica reale. Attivazione/OAT distinta ancora da autorizzare; scientific acceptance e chiusura BKL-051 assenti.
