# Current Technical Baseline — 2026-10-05

| Campo | Valore |
|---|---|
| ID | DSG-BASELINE-20261005 |
| Versione | 1.10 |
| Stato | P1/P2/P3 and P4 candidate delivered; P4 approved cloud active; bounded native OAT; operational acceptance open |
| Data | 2026-10-05 |

La [baseline del 25 settembre](CURRENT_TECHNICAL_BASELINE_2026-09-25.md) conserva le foundation storiche. Il presente aggiornamento prevale per continuità, BKL-049 e M27; non promuove capability estranee.

## Stato attuale

- BKL-043 resta corrente e aperta; [F4 al 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md) attende lifecycle e accettazione finale. F5 resta subordinata.
- BKL-049 archivio available-history ed exact gallery linkage: chiusa/accettata nel [perimetro dichiarato](BKL-049-CLOSURE-2026-10-02.md).
- BKL-034 procedura foto/sessioni: caricamento manuale Owner-only e archiviazione separata, runbook in `infrastructure/scientific-photo-ingestion/README.md`; PR #474–#476.
- Importer PixInsight 1.2: PR #477 merged; esportatore multi-view 2.0.1. Esportazione/importazione non equivalgono a completezza universale o replay.
- M27 ultima versione: elaborazione locale nativa assistita, export 24 viste/80 processi/147 istanze; nuova pubblicazione verificata il 5 ottobre con 16 associazioni Owner-declared. [Handover ed evidenza](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).
- BKL-049-EXT-PIAI: P1 consegnata con PR #479; P2 consegnata con PR #480: cinque processi e checkpoint lineari. P3 ricetta non lineare provata: 29 azioni, 15 checkpoint e pixel finali verificati; confronto visivo effettuato, Owner acceptance richiesta. P4 cloud/worker implementati e attivati nel pilota con OAT parziale; P5/P6 pianificati, nessun modello IA di produzione.
- BKL-046 resta advisory/read-only, `aiModelImplemented=false`, efficacia scientifica non valutabile e produzione non pronta. Il pilota PixInsight è distinto.

## Contratti e autorità

AP-013 resta authority degli asset; AP-014 resta boundary di catalogo. Le 16 sessioni dichiarate non attestano contributo ai pixel. Il workflow pubblico contiene nomi di processi, non parametri privati; `executionEvidence=NOT_ESTABLISHED` e `captureCompleteness=PARTIAL` sono corretti per il contratto importato.

Il pilota autorizza esclusivamente elaborazione di file su copie locali sul PC dell’Owner. Autorità sui dispositivi e Safety Authority non cambiano; S10 production runtime rimane `UNAVAILABLE`. Nessuna nuova installazione, licenza, API a pagamento o accesso cloud viene inferita.

## Prossimo gate

P3 consegnata #481 e candidato P4 consegnato #482. Cloud/credenziale approvati e attivati; prova tecnica nativa circoscritta verificata; completare acceptance operativa prima della chiusura P4 e P5/P6. La modalità IA è SESSION_ASSISTED senza nuove API a pagamento; diritti commerciali/multiutente non attestati. Il [piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md) separa preflight, esecutore, elaborazione e integrazione futura. Registro: v1.0, riconciliazione 2026-10-05; review e consegna tracciate sulle PR.

Aggiornamento v1.1: preflight nativo e 13 test sintetici; [evidenza P1](evidence/BKL-049-PIAI-P1-2026-10-05.json). La disponibilità dei processi non attesta versioni/licenze/modelli.

Aggiornamento v1.2: [evidenza P2](evidence/BKL-049-PIAI-P2-2026-10-05.json), run completato, pre-cancel e replay nativi; integrità e identità esecutore verificate. 15 test esecutore e 20 coordinatore sintetici. Header verificati, qualità pixel/scientifica non certificata; nessun provider o mutazione del portale.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

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


## Rilascio P5b del 6 ottobre 2026

PR #488 integrata: codice, API esistente e Pages pubblicati e verificati; CI, ARB/RQ sequenziali PASS e 17 workflow post-merge SUCCESS. Cartella, prompt, LRGB, OSC RGB/CFA, SHO/HOO e mosaico da pannelli presenti nella pagina pubblica. La nuova catena Owner autenticata e acceptance scientifica restano aperte, come P6. M31 conserva il solo collaudo tecnico locale senza associazioni inventate. Identita di rilascio, rollback ed evidenza: [dossier P5b](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md#rilascio-p5b-verificato-6-ottobre-2026). Questo aggiornamento supera le precedenti note di candidato non pubblicato.


## Master storici senza sessioni importate — 6 ottobre 2026

La correzione Owner chiarisce che M27 è già elaborata e pubblicata; il nuovo collaudo riguarda M31, i cui pannelli precedono il portale. Il modulo distingue «Sessioni già importate» da «Riprese storiche senza sessioni nel portale». Il secondo percorso richiede nome dell'oggetto, provenienza dichiarata e conferma Owner. Non richiede sessioni, catalogo o immagine di riferimento: conserva `sessionIds=[]`, `catalogSha256=null`, `parent=null` e associazione al catalogo `NOT_ESTABLISHED`. La data richiesta è la data di elaborazione, non una data di ripresa inventata.

La dichiarazione `historicalSource` è immutabile e vincola registrazione degli input, selezione dei pannelli, piano esatto, coda, contesto locale e ricevuta privata. Il worker non può registrare un oggetto storico arbitrario senza la richiesta Owner corrispondente. I pannelli storici hanno associazioni di sessione vuote; profili, file, indici, astrometria, griglia, copie, raccolta verificata e conferme separate mantengono gli stessi controlli. La consegna conserva `HISTORICAL_OWNER_DECLARATION` e zero sessioni. Nessuna nuova sessione scientifica, ammissione al registro o pubblicazione è generata. M31 non usa la ricetta o le sessioni di M27.

«Ritira richiesta» conserva proposta e ricevute e impedisce nuove approvazioni e l'ingresso in coda, anche se il ritiro vince tra scrittura del contesto e commit della coda. È ammesso prima del job e dell'approvazione della preparazione nativa; non sostituisce annullamento e recupero di elaborazioni già autorizzate. La richiesta M27 creata erroneamente dall'assistente è un piano non eseguito: va ritirata tramite questo percorso, preservando il risultato M27 precedente.

Validazione sintetica locale: 136 Python e 74 JavaScript PASS, inclusi limiti della provenienza, idempotenza, assenza di sessioni inventate, vincolo di registrazione, consegna privata, ritiro e ruoli HTTP. Gate di rilascio CI → ARB → RQ e verifiche post-merge registrati nella PR di consegna. Le prove non sostituiscono il nuovo collaudo Owner M31 nel portale né accettazione scientifica, History a monte, pubblicazione o P6. Le precedenti note che limitano la procedura alle sessioni importate sono superate esclusivamente da questo ingresso storico esplicito.


Sospensione delle nuove richieste storiche: impostare DSG_PIAI_HISTORICAL_INTAKE=0 sul servizio corrente, mantenendo lettura delle ricevute, ritiro e guardie della coda. Non ripristinare il vecchio backend che ignora i ritiri o la provenienza storica dopo che questi record sono stati creati. Un recupero del codice deve conservare tali controlli e i record immutabili; eventuali job autorizzati seguono annullamento e recupero supervisionati.
