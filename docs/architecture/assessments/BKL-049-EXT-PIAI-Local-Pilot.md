# BKL-049-EXT-PIAI — Pilota locale PixInsight con IA

## Continuità del 7 ottobre 2026

P6 resta aperta; ultima elaborazione SHO reale accettata privatamente, senza nuova certificazione end-to-end del portale. [Handover corrente](../../project/HANDOVER_2026-10-07-P6-BKL051.md). L'Owner ha approvato [BKL-051](../../project/BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md) come prossimo sviluppo dopo chiusura e accettazione operativa P6. Nessuna elaborazione o chiusura viene avviata dalla sola pianificazione.


> Stato corrente al 6 ottobre 2026: [baseline dei rilasci](../../project/CURRENT_TECHNICAL_BASELINE_2026-10-06.md). Le sezioni precedenti conservano gli snapshot e i limiti delle prove; le note di candidato o consegna pendente sono superate soltanto nei perimetri del riepilogo corrente.

| Campo | Valore |
|---|---|
| ID | BKL-049-EXT-PIAI |
| Versione | 1.10 |
| Stato | Owner-authorized pilot; architecture/release review required |
| Data | 2026-10-05 |
| Dipendenze | BKL-049 archive; importer 1.2; Owner PC/PixInsight; calibrated aligned masters |

## Scopo e baseline

Rendere ripetibile l’elaborazione assistita già effettuata su M27, sul PC dell’Owner con PixInsight installato. L’archivio BKL-049 rimane chiuso; questa estensione aggiunge un nuovo perimetro di elaborazione file, senza riaprire o alterare l’acceptance precedente. Le licenze già presenti evitano una nuova installazione nel primo test personale, ma non attestano diritti per servizio commerciale/multiutente. Versione dichiarata: PixInsight 1.9.5 build 1706; versioni e disponibilità effettive dei moduli devono essere registrate dal preflight.

## Architettura prevista

```mermaid
flowchart LR
    O[Owner e master privati] --> M[Manifest locale verificato]
    A[Assistente IA: piano motivato] --> V[Validatore della ricetta]
    M --> V
    V --> P[PixInsight: processi nativi su copie]
    P --> J[Journal e output privati]
    J --> Q[Verifica tecnica e valutazione Owner]
    Q --> E[Export History e importazione governata]
```

Il primo pilota usa l’assistente della sessione e una ricetta esplicita; non richiede chiamate API a pagamento. L’IA propone operazioni e parametri entro un insieme ammesso; PixInsight applica i pixel. Il journal futuro registra input/output e relazioni al momento dell’azione, così non dipende solo dalle correlazioni incomplete della History.

Un futuro worker sul PC riceverà job attraverso connessione autenticata in uscita. Il backend conserverà stato e coda; nessuna porta pubblica sul desktop. Credenziale dedicata, protocollo, provider/modello/costi e autorizzazioni cloud richiedono un pacchetto concreto successivo. La sola installazione PixInsight e l’abbonamento alla chat non rendono disponibile questa infrastruttura.

## Fasi e criteri di uscita

| Fase | Risultato richiesto | Stato iniziale |
|---|---|---|
| P1 — Preflight | Prova nativa M27 eseguita il 5 ottobre: PI 1.9.5 build 1706, quattro master invariati, 12 costruttori di processo disponibili; versioni moduli/licenze/modelli non attestati | Delivered #479; native PASS |
| P2 — Esecutore locale | Coordinatore locale, copie, snapshot esecutore, ricetta lineare fissa, journal e checkpoint; prova nativa completa, pre-cancel e replay | Delivered #480; native PASS |
| P3 — Prova M27 | Input bloccati, output non lineare, verifiche finite/dimensioni/colore, confronto visivo; nessuna accettazione scientifica automatica | Delivered #481; native technical/visual PASS; Owner acceptance open |
| P4 — Connessione e IA | Candidato autenticato/coda/adapter e recupero offline; SESSION_ASSISTED senza nuove API IA; proposta cloud distinta | Delivered #482/#483; Owner login and bounded administrative native transport PASS; operational acceptance/P5/P6 open |
| P5 — Portale e provenance | Comando Owner, stato, preview, revisione e collegamento esatto a sessioni e workflow | Technical M27 P5 PASS; Owner ACCEPT_PRIVATE/downloads confirmed; P5b folder/prompt candidate; P6 open |
| P6 — Acceptance | Casi errore/annullamento/offline, integrità originali, evidenza reale, review e rollback | Planned |

La disponibilità futura nel portale dipende da P4–P6. Il successo della vecchia elaborazione M27 non dimostra il funzionamento del nuovo worker.

## Regole dell’esecutore

Manifest versionato, ID univoco, input selezionati con integrità, destinazione separata, ricetta e limiti espliciti. Un job alla volta. Rifiutare input mancanti, risultati precedenti, conflitti e processi non ammessi; niente esecuzione di script forniti dal portale. Non usare i master come target modificabili. Se un modulo richiesto manca, fermare il job senza sostituirlo tacitamente. Non miscelare lavoro manuale e job automatico sulla stessa istanza.

Per cancellare, controllare il segnale prima del prossimo processo e conservare il journal. Un processo nativo lungo può terminare prima dell’annullamento; non è promesso un arresto immediato. Crash o risultati parziali restano evidenza privata e non passano a `COMPLETED`. Nessun upload/publicazione deriva dal completamento locale.

## Privacy, rischi e prove

Percorsi, immagini, modelli plugin e parametri delle ricevute restano privati. Git conserva codice, default della ricetta revisionata, documenti e prove sintetiche/minimizzate; non pubblica le sorgenti native integrali dei run. La catena runtime registrata e l’export storico importato hanno classificazioni distinte. Sessioni associate per dichiarazione non diventano origine pixel provata.

Rischi: desktop non disponibile, occupazione RAM/disco, moduli mancanti, incompatibilità PJSR, gradienti/dati inadatti alla ricetta e qualità variabile. Le operazioni originali su M27 non sono una ricetta universale LRGB. L’Owner valuta il risultato prima di qualsiasi pubblicazione; il pilota conserva la versione pubblicata attuale.

Acceptance P1/P2: prove di rifiuto per identità/input incoerenti e destinazione conflittuale; un preflight nativo reale deve lasciare input e progetto invariati. Acceptance P3: job reale separato e output verificato. Test sintetici non sostituiscono PixInsight, licenze o giudizio scientifico.

## Riferimenti e revisione

[Handover](../../project/HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md), [baseline](../../project/CURRENT_TECHNICAL_BASELINE_2026-10-05.md), [closure archivio](../../project/BKL-049-CLOSURE-2026-10-02.md), [importer 1.2](BKL-049-Portal-Importer-1.2.md).

Versione 1.0: piano autorizzato il 5 ottobre, nessuna fase dichiarata accettata prima di esecuzione/review. Rollback: interrompere nuovi job, conservare ricevute e output parziali, ritirare il codice aggiuntivo; originali e gallery non richiedono modifica.

## P1 — prova nativa 2026-10-05

La [ricevuta minimizzata](../../project/evidence/BKL-049-PIAI-P1-2026-10-05.json) registra il primo controllo reale. Il primo tentativo ha rifiutato correttamente il contenitore XISF multi-image: master più maschera di ritaglio. La selezione esplicita dell’indice immagine e delle dimensioni attese ha consentito il secondo test. Quattro master monocromatici Float32 4634×2808, 12 costruttori richiesti disponibili, integrità dei file confermata dopo il run, zero master modificati, zero processi applicati e zero richieste provider. Parametri, percorsi e digest privati non sono pubblicati.

Libreria `tools/pixinsight/local_pilot/preflight.jsh`; 13 test sintetici di rifiuto/selezione passati localmente. I test CI usano stub e non sostituiscono il test nativo. Le versioni dei moduli non sono esposte da ProcessInstance e restano sconosciute; disponibilità dei costruttori non prova licenza o caricamento dei modelli RC. Il risultato P1 non produce una nuova foto né modifica la gallery. Versione 1.1: prova nativa P1; consegnata con PR #479, merge `76d6186489c78aceb32f34a6b96afbe8f88457a7`, 17 controlli exact-head e 16 workflow post-merge SUCCESS, review sequenziali senza finding finali.

## P2 — esecutore e prove native 2026-10-05

Implementati `worker.py` e `executor.jsh`, con [procedura operativa nel repository](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/pixinsight/local_pilot). La ricetta `LRGB_LINEAR_PREP_V1` applica quattro ABE alle copie R/G/B/L e compone RGB: cinque processi, cinque checkpoint XISF Float32 lineari. La luminanza è preparata ma non ancora integrata. Non è una foto finale né una ricetta universale. Calibrazione colore, astrometria RGB, riduzione rumore, dettaglio, stretch e confronto visivo restano P3.

La [ricevuta minimizzata P2](../../project/evidence/BKL-049-PIAI-P2-2026-10-05.json) distingue la prova reale dai test sintetici. Run nativo completato: cinque processi/checkpoint, file originali e viste di input invariati, snapshot dello script e header verificati. Pre-cancel nativo: zero processi/output. Replay nativo rifiutato: tutti i 37 file del job concluso invariati. Seconda preparazione nello stesso worker root rifiutata. Test locali: 13 preflight, 15 esecutore, 20 coordinatore; l’errore nativo simulato non è presentato come OAT fisica.

Una prenotazione locale e un handle File esclusivo Windows, verificato a runtime prima dei pixel, serializzano un root configurato. Non è un lock globale di più worker. Il lancio resta supervisionato da Script → Execute Script File. Crash o preparazione incompleta conservano la prenotazione; nessuna ripresa o scadenza automatica. Per recuperare, confermare l’arresto di PixInsight, conservare/quarantinare il root e usare un root nuovo. Non forzare lo sblocco di un job vivo.

Le sorgenti native di ogni processo restano esatte nel journal privato. `workflow.js` esporta solo le cinque istanze riuscite, con identificatori rinominati e valori letterali preservati; il lettore 1.2 le legge come dati. Le correlazioni runtime restano separate; questa prova non rende completa la History a monte e non modifica il contratto pubblico importato. Nessuna API provider, connessione remota, modifica gallery o accettazione scientifica. Versione 1.2: P2 implementato e provato nativamente; delivery, CI e review da registrare sulla PR del relativo head.

Una seconda prova nativa completa conferma anche la correlazione dell’immagine creata da ChannelCombination: il target registrato al completamento coincide con l’output salvato. Entrambi i run e le ricevute restano privati e immutati.

Riesame P2: un Major ARB ha rilevato che il comando cancel tentava di leggere il file tenuto con handle esclusivo. Corretto con identità immutabile del job separata e marker completo pubblicato atomicamente, vincolato al token e verificato dal runtime. Prova Windows con handle reale e prova nativa PixInsight: lettura del lease negata, comando cancel riuscito durante il primo processo; arresto prima del checkpoint successivo, un processo registrato, zero output e originali invariati. Il processo in corso può terminare prima dell’annullamento. Il riesame finale richiede CI e ARB/RQ sul nuovo head.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

## P3 — ricetta non lineare e verifica

`M27_LRGB_NONLINEAR_V1` aggiunge alla preparazione lineare la correzione radiale, calibrazione stellare empirica, BXT/NXT lineari, SXT, stretch separato RGB/L, maschera di luminanza, contrasto locale, combinazione LRGB, colore selettivo e ricomposizione delle stelle. Non usa SPCC e non certifica colori fotometrici. La ROI relativa è specifica del campo M27: un altro soggetto richiede una nuova ricetta revisionata. I costruttori sono verificati prima dei pixel; l’esecuzione effettiva dei plugin attesta disponibilità per quel run, non licenze, versione o hash del modello.

Un run completo richiede 29 azioni native e 15 checkpoint XISF. I metadati della combinazione RGB sono mantenuti; il finale è marcato LRGB/non lineare senza attribuire esposizione aggregata non ricostruita. Le relazioni private registrano copie, output stelle, maschere e inversione. Le 29 istanze derivate sono dati per l’importer, non replay o History integrale a monte.

La raccolta controlla integrità, geometria, canali e ordine/processi della ricetta. Sul finale legge tutti i pixel Float32, rifiutando non finiti, intervallo non normalizzato, canali costanti, blocchi troncati e formati non supportati. Per questo pilota è richiesto XISF planar little-endian senza compressione. Conta clipping ed estremi per canale senza dichiararli assenti. Se la raccolta fallisce, la prenotazione resta conservata anche con ricevuta di esecuzione `COMPLETED`.

Confronto visivo e valutazione Owner restano distinti dall’esito tecnico. Originali e M27 pubblicata restano invariati; P4–P6 non sono attivati. La prova tecnica/visiva è registrata di seguito; consegna e review di questo head sono tracciate sulla PR.

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](../../project/evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

Verifica candidato P4: 33 test Node e 62 Python Windows, inclusi 32 casi trasporto. [Ricevuta minimizzata](../../project/evidence/BKL-049-PIAI-P4-2026-10-05.json). CI/review dello stesso head e post-merge da registrare sulla PR; nessuna attivazione cloud anticipata.

Riesame P4: un Major ARB ha riprodotto una seconda preparazione su root nuovo privo di binding. Corretto con identità locale persistente fissata dalla prima claim e transizione PREPARING confermata prima delle copie; claim avanzata senza binding rifiutata. Cinque regressioni coprono nuovo root, stati avanzati, perdita della risposta iniziale e preparazione interrotta. CI e riesame finale dello stesso head richiesti sulla PR.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](../../project/evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](../../project/PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

Autenticazione Google Owner reale PASS sulla pagina diagnostica: creazione sintetica, ripetizione idempotente, annullamento e lettura CANCELLED/NONE. Google valido non-Owner negato e stale-create CAS reale negato senza mutazione. Riavvio del servizio sullo stesso digest e perdita deliberata dell’ack PREPARING dopo commit remoto: stessa richiesta recuperata, una preparazione; ciclo ripetuto con otto file identici.

Trasporto nativo sul PC verificato con due fixture amministrative isolate: pre-cancel con zero processi/output; M27 non lineare COMPLETED con 29 azioni, 15 checkpoint e 29 istanze workflow, originali invariati, finale Float32 RGB 4634×2808 e tutti i pixel finiti in [0,1]. Clipping misurato, non certificato assente. Raccolta dopo arresto PixInsight, prenotazioni chiuse e report remoto verificato. Questa prova usa Broker/BackedUpStore tramite CLI Owner amministrativa: non attesta ancora la creazione di un job scientifico dal comando HTTP/UI Owner. La prova HTTP Owner separata è sintetica; executionEvidence resta WORKER_REPORTED_NOT_ATTESTED, publication=NONE.

P4 ha ora una prova tecnica nativa circoscritta; CAS GCS concorrente reale PASS tramite CLI Owner amministrativa: due scritture degli stessi bytes di coda terminale, una accettata e una rifiutata per generazione obsoleta, backup verificato e stato logico invariato. Concorrenza sulle route Owner HTTP soltanto sintetica; acceptance operativa più ampia resta aperta. P5 comando scientifico/sessioni/preview/provenance, P6 e acceptance scientifica Owner sono successivi. SESSION_ASSISTED, zero nuove chiamate API IA; M27 pubblicata e autorità dispositivi/Safety invariate. Evidenza privata conservata; ricevuta pubblica minimizzata e runbook collegati sopra. CI/review/merge e Pages di questa riconciliazione sono da verificare sulla PR di consegna.

Osservazione reale dopo oltre 120 secondi senza contatto: OFFLINE diagnostico, stesso job/root ancora RUNNING, nessuna scadenza o riassegnazione osservata. Non è una prova di crash recovery del desktop.

Derivati locali TIFF RGB16/JPEG sRGB verificati; soluzione astrometrica conservata e checkpoint invariato dopo export. History disponibile: 13 viste, 47 passi, 82 istanze, 429679 byte; importer 1.2 PARSED_SUBSET. La History conservata non prova completezza a monte: executionEvidence=NOT_ESTABLISHED e workflowCompleteness=UNAVAILABLE del file importato restano invariati. Journal e correlazioni runtime delle 29 azioni conservati separatamente. Campo intero/dettaglio coerenti con la ricetta P3; nessuna superiorità scientifica o sostituzione pubblica dichiarata.


## Aggiornamento P5 — portale scientifico privato (2026-10-05)

Implementato il candidato P5: pagina Owner, selezione di master M27 registrati, sessioni/catalogo e versione di riferimento esatti; job con contesto immutabile e verifica sul PC prima delle copie; stato/cancel espliciti, preview privata, workflow delle 29 azioni, correlazioni runtime e revisione Owner vincolata alla ricevuta. Originale e journal completo restano sul PC. Le identità IMG/VER/WF del pilota sono private e distinte dall’archivio di pubblicazione; nessun caricamento o pubblicazione automatica. SESSION_ASSISTED senza nuove API IA; classificazioni WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e History a monte NOT_ESTABLISHED preservate. Release/deployment consegnati tramite #485; la prova scientifica reale HTTP/UI → PixInsight → consegna/revisione resta un gate P5 aperto, non sostituito dai test. P6 e acceptance scientifica Owner restano successivi. [Procedura P5](../../project/PIAI-P5-PORTAL-2026-10-05.md).

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](../../project/PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](../../project/evidence/BKL-049-PIAI-P5-2026-10-05.json).


## P5b — cartella dei master e prompt (candidato del 5 ottobre 2026)

Incremento autorizzato dall’Owner dopo l’accettazione privata P5 e la conferma dei download. Il modulo aggiunge cartella locale assoluta e prompt, richiesta privata di pianificazione, verifica esplicita sul PC, proposta immutabile e conferma Owner dell’esatto piano prima della coda PixInsight. Nessun job alla sola ricezione del prompt; nessuna lettura automatica del disco o esecuzione di testo/script dal browser. SESSION_ASSISTED: questa sessione interpreta il prompt e propone ricetta, parametri ammessi di fondo, dettaglio, rumore, contrasto e stretch, motivazione e limiti; nessuna nuova API IA, risorsa, credenziale o espansione IAM. Il perimetro richiesto include altri oggetti importati, LRGB, OSC, SHO/HOO e mosaici da pannelli. Il candidato comprende inventario e selezione esplicita; le nuove ricette per campo singolo richiedono parametri di campo verificati. OSC CFA e assemblaggio mosaici restano bloccati fino a implementazione e collaudo nativo. [Stato e procedura](../../project/PIAI-P5B-SOURCE-PROFILES-2026-10-05.md). Nessuna estensione è ancora pubblicata o dichiarata accettata.

Il piano conserva ruoli R/G/B/L, dimensioni, selezione esplicita dell’immagine nei contenitori, impronta del manifest e sequenza dei 29 processi. Cartella, prompt e piano sono dati privati Owner; master/hash individuali e diagnostica locale restano sul PC. Il worker confronta cartella, piano e manifest prima delle copie. Aggiornamenti di catalogo o riferimenti conflittuali fermano l’approvazione; retry identici non duplicano richieste/job. I vecchi risultati P5 rimangono accessibili e invariati. Il candidato richiede CI sull’head esatto, ARB/RQ sequenziali, merge, deployment API/Pages e prova Owner della nuova procedura; non è ancora dichiarato disponibile nel portale pubblico. P6 e acceptance operativa restano aperti.
