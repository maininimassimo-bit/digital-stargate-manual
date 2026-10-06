# P5 — richiesta scientifica e revisione privata PixInsight

| Campo | Valore |
|---|---|
| Versione | 1.5 |
| Stato | Technical M27 Owner HTTP/UI/native/private-delivery OAT PASS; Owner private result accepted |
| Data | 2026-10-05 |
| Perimetro | BKL-049-EXT-PIAI P5; M27, Owner PC, SESSION_ASSISTED |

## Procedura

La pagina [Elabora con PixInsight e IA](../pixinsight-pilot/index.md) è raggiungibile dalla navigazione Osservatorio e dalla galleria. L’Owner accede con Google, seleziona un gruppo di master M27 registrato dal PC, le sessioni già importate, titolo/data e, facoltativamente, l’esatta immagine/versione/workflow pubblicata di riferimento.

Il server verifica catalogo e relativa impronta, sessioni dello stesso target e identità della versione corrente. Conserva lo snapshot privato e crea il job con l’impronta del contesto nella stessa transizione CAS della coda. Il retry dello stesso identificativo conserva la selezione originaria anche se il catalogo cambia; un contenuto differente viene rifiutato. Il browser conserva solo la richiesta ambigua, mai la credenziale Google. Non aggiunge una scadenza.

Il worker riceve il contesto tramite autenticazione dedicata in uscita e confronta l’impronta del manifest locale: ricetta, parametri di background, hash dei quattro master, ruoli, indici immagine e geometria; nella registrazione e nel contesto non vengono trasmessi percorsi o parametri integrali; il workflow runtime consegnato successivamente conserva i parametri dei processi. La verifica precede la preparazione delle copie. La ricetta resta quella M27 revisionata, non un’elaborazione arbitraria proposta da un file caricato. L’assistente attivo avvia lo script nativo preparato sotto supervisione.

La pagina mostra stato, conteggi e contatto PC su aggiornamento esplicito. OFFLINE conserva job/prenotazione; nessuna riassegnazione o elaborazione continua. L’annullamento viene applicato tra processi; quello in corso può terminare. La raccolta richiede conferma che l’esecuzione nativa sia arrestata.

## Consegna e revisione

Un’azione esplicita sul PC riconvalida originali/copie, runtime/journal/checkpoint e tutti i pixel finali, genera una preview JPEG dal checkpoint verificato e invia al servizio privato preview, workflow delle 29 azioni e correlazioni runtime. Il server richiede job COMPLETED verificato e binding worker/lease; valida JPEG, rimuove metadati, legge JavaScript come dati, verifica l’ordine dei processi della ricetta e il job/ordinale/variabili delle correlazioni. Non esegue il workflow.

La ricevuta immutabile collega job, manifest, snapshot catalogo/sessioni, versione di riferimento, hash originale sul PC e hash di preview/workflow/correlazioni. Gli identificatori IMG/VER/WF del risultato sono **identità private del pilota**, non record automaticamente ammessi all’archivio di pubblicazione. Il caricamento separato genera i propri identificatori e conserva i gate esistenti. Nessuna falsa equivalenza fra le due versioni è dichiarata.

Originale XISF e journal completo restano sul PC. Preview, workflow e correlazioni sono conservati soltanto nei due bucket privati esistenti, con backup prima delle scritture; nessun URL pubblico o download anonimo. Il server riporta `WORKER_REPORTED_NOT_ATTESTED`, non un’attestazione indipendente del desktop. Le sessioni rimangono `OWNER_DECLARED`; il workflow ha scope `RUNTIME_RECIPE_ONLY`, mentre la History a monte rimane `NOT_ESTABLISHED`.

L’Owner apre l’anteprima, consulta i 29 processi e scarica workflow, correlazioni e ricevuta. Accetta il risultato privatamente oppure registra il rifiuto, con decisione vincolata all’esatto hash della revisione. Una decisione o consegna diversa sulla stessa identità viene rifiutata: per una revisione nuova serve un nuovo job. La valutazione non pubblica, non ritira M27 e non avvia automaticamente un altro lavoro. L’accettazione scientifica reale resta una decisione Owner; non è simulata dai test.

## Comandi locali

Con la configurazione privata P4 e la credenziale DPAPI già autorizzata, caricata solo nell’ambiente del processo:

```text
python -m tools.pixinsight.local_pilot.scientific_delivery register --config <private-config.json>
python -m tools.pixinsight.local_pilot.transport --config <private-config.json>
# Avvio supervisionato del run.js preparato tramite PixInsight.
python -m tools.pixinsight.local_pilot.transport --config <private-config.json> --native-stopped
python -m tools.pixinsight.local_pilot.scientific_delivery deliver --config <private-config.json> --job <PIAI_job>
```

Registrazione limitata a otto gruppi immutabili, coda a 16 job e un root/worker nativo attivo. Preview ≤4 MiB, workflow ≤2 MiB, correlazioni ≤256 KiB, richiesta di consegna ≤9 MiB. Nessuna porta in ingresso, credenziale nuova, API IA, polling continuo o nuova risorsa cloud. Costi della stessa infrastruttura già approvata possono aumentare per i nuovi oggetti privati e le operazioni; nessun hard cap è dichiarato.

## Prove e gate

Test locali PASS: 43 Node e 80 Python Windows, MkDocs strict e consistenza roadmap. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json). Test sintetici di selezione, idempotenza, parent/versione, integrità contesto, consegna/decisione immutabile, ordine dei processi, binding e privacy; HTTP loopback reale con identità sintetiche, distinto da Google/cloud/PixInsight. Test browser sintetici per risposta persa, richiesta congelata, account negato e OFFLINE senza mutazioni automatiche. CI, review ARB/RQ separate e sequenziali, deployment per digest e Pages sul merge SHA precedono il completamento operativo.

La prova reale richiesta è: comando scientifico Owner HTTP/UI → preparazione PC → nuova esecuzione nativa → raccolta verificata → consegna privata → anteprima/workflow/sessioni esatte. Finché questa prova non è registrata, P5 non è dichiarata completata. P6 mantiene errore/annullamento/crash recovery e acceptance complessiva; le prove P4 restano circoscritte ai perimetri già registrati.

## Rollback

Interrompere nuove richieste e cicli prima del rollback; non forzare lo sblocco di un job vivo. Conservare root, binding, prenotazioni, copie, journal, ricevute e bucket/backup. Ripristinare il digest P4 già verificato e ritirare il collegamento P5 tramite revert revisionato solo quando non ci sono job P5 attivi; un job scientifico non deve essere adottato da un worker privo del controllo del contesto. Non cancellare evidence né modificare M27 pubblicata. [Piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md), [P4](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md), [handover](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).

Correzioni ARB: le registrazioni condividono il solo oggetto CAS già autorizzato `control/piai-state.json`; nessun ampliamento IAM. Un rifiuto HTTP 400 consente una nuova selezione solo dopo verifica autenticata `JOB_NOT_FOUND`; esiti ambigui conservano la richiesta. Le dipendenze dei master nelle correlazioni cloud sono riferimenti di ruolo associati al digest composto del manifest; il grafo originale con hash individuali rimane sul PC. Regressioni per seconda registrazione, minimizzazione e recupero del catalogo obsolete aggiunte.

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.

## Compatibilità del target rilevata nel collaudo Owner

Il primo accesso Owner alla pagina scientifica è stato verificato, senza creazione di job: catalogo e galleria usano `M 27`, mentre il gruppo locale registrato usa `M27`. Il confronto letterale della prima versione nascondeva sessioni e parent. La correzione ammette esclusivamente questi due alias per il pilota M27, conserva target e identità originali nel contesto scientifico e non amplia i target o le ricette consentiti. Tre regressioni coprono parent/catalogo con nome spaziato, 16 sessioni e rifiuto di nomi ambigui. Verifica aggiuntiva dei profili pubblici reali in un broker locale sintetico: 16 sessioni e un parent corrente, target originale conservato; non è prova Owner HTTP/nativa. La correzione deve superare CI/ARB/RQ e distribuzione prima del collaudo scientifico; P5 rimane aperta.


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json).


## P5b — cartella dei master e prompt (candidato del 5 ottobre 2026)

Incremento autorizzato dall’Owner dopo l’accettazione privata P5 e la conferma dei download. Il modulo aggiunge cartella locale assoluta e prompt, richiesta privata di pianificazione, verifica esplicita sul PC, proposta immutabile e conferma Owner dell’esatto piano prima della coda PixInsight. Nessun job alla sola ricezione del prompt; nessuna lettura automatica del disco o esecuzione di testo/script dal browser. SESSION_ASSISTED: questa sessione interpreta il prompt e propone ricetta, parametri ammessi di fondo, dettaglio, rumore, contrasto e stretch, motivazione e limiti; nessuna nuova API IA, risorsa, credenziale o espansione IAM. Il perimetro richiesto include altri oggetti importati, LRGB, OSC, SHO/HOO e mosaici da pannelli. Il candidato comprende inventario e selezione esplicita; le nuove ricette per campo singolo richiedono parametri di campo verificati. OSC CFA e mosaici richiedono conferma separata della preparazione e un risultato lineare verificato prima della proposta finale; il candidato integra questo collegamento, ancora senza rilascio o accettazione autenticata reale. [Stato e procedura](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md). Nessuna estensione è ancora pubblicata o dichiarata accettata.

Il piano conserva i ruoli del profilo scelto, dimensioni, selezione esplicita dell’immagine nei contenitori, impronta del manifest e sequenza della ricetta corrispondente. Cartella, prompt e piano sono dati privati Owner; master/hash individuali e diagnostica locale restano sul PC. Il worker confronta cartella, piano e manifest prima delle copie. Aggiornamenti di catalogo o riferimenti conflittuali fermano l’approvazione; retry identici non duplicano richieste/job. I vecchi risultati P5 rimangono accessibili e invariati. Il candidato richiede CI sull’head esatto, ARB/RQ sequenziali, merge, deployment API/Pages e prova Owner della nuova procedura; non è ancora dichiarato disponibile nel portale pubblico. P6 e acceptance operativa restano aperti.


### Procedura P5b del candidato cartella/prompt

1. Owner accede, sceglie l’oggetto delle sessioni importate, LRGB/OSC/CFA/SHO/HOO, campo singolo o pannelli, cartella principale ed eventuali altre cartelle. Scrive il prompt, seleziona le sessioni reali dello stesso oggetto e l’eventuale versione pubblicata di riferimento. «Invia cartella e prompt» conserva una richiesta privata di pianificazione.
2. Owner scrive nella chat «richiesta inviata». L’assistente inventaria le cartelle dichiarate senza scansione ricorsiva. Seleziona esplicitamente file, ruoli e indice immagine; separa bias, dark, riferimenti di normalizzazione, mappe di rigetto e drizzle. Le intestazioni sono limitate a 4 MiB, senza XML DTD/entity. I profili richiedono master Float32 mono oppure RGB secondo i ruoli; CFA richiede un pattern Bayer esplicito. Metadati/digest non certificano l’idoneità scientifica. Per i mosaici l’Owner conferma la selezione esatta di pannelli, master e sessioni.
3. Per CFA e mosaici l’assistente propone separatamente la preparazione: sorgenti identificate, Bayer oppure griglia astrometrica comune e parametri di fusione, motivazione e limiti. La conferma Owner dell’esatto digest autorizza copie e avvio nativo supervisionato della preparazione; non crea il job finale. La raccolta verifica sorgenti, copie, runtime, journal, parametri delle istanze e tutti i pixel dei checkpoint prima di registrare un risultato lineare verificato.
4. L’assistente interpreta il prompt senza nuove API IA. Propone la ricetta del profilo con regione del fondo e parametri di campo, sette parametri limitati di dettaglio/rumore/contrasto/stretch, motivazione e limiti. LRGB prevede 29 operazioni/15 checkpoint; OSC 26/12; SHO 27/15; HOO 26/14. CFA preparato prosegue come OSC. Palette SHO/HOO e luminanza derivata non certificano colori fotometrici. Le richieste fuori dai parametri ammessi richiedono un piano compatibile, senza dichiarare modifiche non eseguite.
5. L’assistente registra il manifest e la proposta immutabile; per master preparati conserva il collegamento alla preparazione verificata. La pagina mostra sorgenti, parametri, motivazione e sequenza. «Conferma piano e richiedi elaborazione» crea il job soltanto per l’esatto digest. Catalogo modificato prima della conferma: fermare e ricreare la selezione, senza adottare nuovi dati tacitamente.
6. L’assistente avvia il ciclo worker esplicito e la procedura nativa supervisionata. Il worker riconfronta sorgenti, piano e manifest prima delle copie. Workflow e correlazioni comprendono preparazione e ricetta quando applicabile; la History precedente resta non certificata. Download e accettazione privata seguono la procedura P5. La pubblicazione resta separata.

Comandi dell’assistente: `list`, `inventory`, `inspect`, `propose-sources`, `propose-preparation`, `prepare-sources`, `collect-sources`, `propose`, usando la configurazione privata e la credenziale DPAPI esistente nel solo ambiente del processo. Nessun comando CLI avvia PixInsight. Output e backup privati non vengono sovrascritti; configurazione limitata a 64 KiB, con backup, lock esclusivo e aggiornamento atomico. Limiti: otto gruppi master, sedici richieste e sedici job; niente scadenza o riassegnazione. Lock/pending dopo crash e preparazioni fallite richiedono verifica del recupero; nessuna cancellazione automatica.

**Candidato NOT_DEPLOYED.** Sono necessari CI sull’head esatto, ARB/RQ sequenziali, rilascio API/Pages e prova Owner autenticata della nuova procedura. Le prove tecniche locali e sintetiche non equivalgono ad accettazione scientifica di tutti i profili. P6 resta aperto. Procedura dettagliata: [P5b](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md).


## Rilascio P5b verificato — 6 ottobre 2026

La PR [#488](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/488) è integrata nel commit `ebbb7d3c1034130ef49df674fcc596c0403647f0`. Il codice revisionato è `bd628c51d0b5f76f22bf94a3ba8c8b673ed0c289`, albero `ed8a9ef7ac6fb640408621c5d1256ce5d4c1f945`: CI completa, ARB e RQ AI-assistite separate e sequenziali PASS, zero finding residui. La prima ARB fallita resta storica; il difetto di ownership della prenotazione e la procedura obsoleta sono corretti e verificati. Merge eseguito secondo DSG-AEM-001 e W-DSG-AEM-RULESET-001, senza deroga alla CI. Tutti i 17 workflow post-merge, inclusa la pubblicazione Pages, sono SUCCESS sul merge SHA.

Cloud Build `78bb9d31-1b02-46f9-ab63-b088ee8ccfea` SUCCESS sul codice revisionato, con 125 test Python. Il servizio esistente usa la revisione `dsg-pixinsight-pilot-p5b-bd628c51`, traffico 100%, immagine per digest `sha256:ddf1abe4369c5b682ddc92d377dbb6e77d3905a349b45a759905c56bafa337d8`. Prove HTTP reali PASS: health SESSION_ASSISTED e zero richieste provider, lettura worker autenticata, rifiuto degli accessi anonimi e delle approvazioni Owner da worker, rifiuto delle chiamate browser ai percorsi worker; stato invariato e nessun avvio nativo. Non sono state create risorse, credenziali o autorizzazioni IAM.

La [pagina pubblica](https://maininimassimo-bit.github.io/digital-stargate-manual/pixinsight-pilot/) è verificata nel browser: cartella locale, prompt, LRGB, OSC RGB/CFA, SHO/HOO e mosaico da pannelli sono presenti. L'accesso Google Owner e la nuova catena completa di conferme nel portale restano da collaudare; la verifica senza login non li sostituisce. Il pulsante Google incorporato richiede il clic dell'Owner perché il controllo browser non può indirizzarlo. Le prove native M31 restano tecniche locali su copie, senza sessioni inventate, accettazione scientifica o pubblicazione della foto. L'accettazione privata M27 precedente resta conservata. P6 e acceptance operativa dei nuovi profili restano aperti.

Rollback API: ripristinare il traffico sulla revisione precedente `dsg-pixinsight-pilot-p5-target-01` e riconciliare la pagina con il codice precedente, senza cancellare richieste, ricevute e risultati privati immutabili. Questo aggiornamento supera esclusivamente le precedenti note di candidato non pubblicato e gate di rilascio pendenti; conserva le limitazioni scientifiche e gli snapshot storici.


## Master storici senza sessioni importate — 6 ottobre 2026

La correzione Owner chiarisce che M27 è già elaborata e pubblicata; il nuovo collaudo riguarda M31, i cui pannelli precedono il portale. Il modulo distingue «Sessioni già importate» da «Riprese storiche senza sessioni nel portale». Il secondo percorso richiede nome dell'oggetto, provenienza dichiarata e conferma Owner. Non richiede sessioni, catalogo o immagine di riferimento: conserva `sessionIds=[]`, `catalogSha256=null`, `parent=null` e associazione al catalogo `NOT_ESTABLISHED`. La data richiesta è la data di elaborazione, non una data di ripresa inventata.

La dichiarazione `historicalSource` è immutabile e vincola registrazione degli input, selezione dei pannelli, piano esatto, coda, contesto locale e ricevuta privata. Il worker non può registrare un oggetto storico arbitrario senza la richiesta Owner corrispondente. I pannelli storici hanno associazioni di sessione vuote; profili, file, indici, astrometria, griglia, copie, raccolta verificata e conferme separate mantengono gli stessi controlli. La consegna conserva `HISTORICAL_OWNER_DECLARATION` e zero sessioni. Nessuna nuova sessione scientifica, ammissione al registro o pubblicazione è generata. M31 non usa la ricetta o le sessioni di M27.

«Ritira richiesta» conserva proposta e ricevute e impedisce nuove approvazioni e l'ingresso in coda, anche se il ritiro vince tra scrittura del contesto e commit della coda. È ammesso prima del job e dell'approvazione della preparazione nativa; non sostituisce annullamento e recupero di elaborazioni già autorizzate. La richiesta M27 creata erroneamente dall'assistente è un piano non eseguito: va ritirata tramite questo percorso, preservando il risultato M27 precedente.

Validazione sintetica locale: 136 Python e 74 JavaScript PASS, inclusi limiti della provenienza, idempotenza, assenza di sessioni inventate, vincolo di registrazione, consegna privata, ritiro e ruoli HTTP. Gate di rilascio CI → ARB → RQ e verifiche post-merge registrati nella PR di consegna. Le prove non sostituiscono il nuovo collaudo Owner M31 nel portale né accettazione scientifica, History a monte, pubblicazione o P6. Le precedenti note che limitano la procedura alle sessioni importate sono superate esclusivamente da questo ingresso storico esplicito.


Sospensione delle nuove richieste storiche: impostare DSG_PIAI_HISTORICAL_INTAKE=0 sul servizio corrente, mantenendo lettura delle ricevute, ritiro e guardie della coda. Non ripristinare il vecchio backend che ignora i ritiri o la provenienza storica dopo che questi record sono stati creati. Un recupero del codice deve conservare tali controlli e i record immutabili; eventuali job autorizzati seguono annullamento e recupero supervisionati.
