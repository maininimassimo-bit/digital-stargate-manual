# Handover — M27 e pilota PixInsight con IA

| Campo | Valore |
|---|---|
| ID | DSG-HO-BKL049-20261005 |
| Versione | 2.6 |
| Data | 2026-10-06 |
| Stato | Riconciliazione operativa; estensione pilota autorizzata, non accettata come produzione |
| Pacchetto | BKL-049 archivio chiuso; BKL-049-EXT-PIAI pilota distinto |

## Continuità e autorità

Questo documento e la [baseline corrente](CURRENT_TECHNICAL_BASELINE_2026-10-05.md) sostituiscono gli snapshot del 25 settembre come punto di ingresso. Gli snapshot e la [closure BKL-049](BKL-049-CLOSURE-2026-10-02.md) restano storici. BKL-043 rimane aperta: F4 attende lifecycle e accettazione finale, secondo lo [stato del 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md). Il lavoro PixInsight non ne modifica autorizzazioni o gate.

L’Owner ha richiesto documentazione completa e avvio del pilota sul proprio PC già utilizzato per M27. Questa autorizzazione riguarda file scientifici locali e copie di lavoro; non introduce comandi all’osservatorio, Safety Authority, servizi a pagamento o pubblicazione automatica.

## Lavoro effettuato

| Risultato | Evidenza e limite |
|---|---|
| Archivio e collegamento immagine/versione/workflow | BKL-049 chiusa nel perimetro available-history; PR #471 e closure. La successiva rimozione della scadenza mantiene la pubblicazione fino a ritiro esplicito. |
| Caricamento foto e workflow | Procedura Owner-only autenticata, archivio privato e preview pubblica; PR #474–#476, runbook infrastrutturale. Gli esempi M31/M42/NGC7000 sono stati rimossi. |
| Esportazione History e lettore | Esportatore multi-view 2.0.1 e importer 1.2, PR #477. Importazione dati senza eseguire JavaScript caricato. Correlazioni e lacune esplicite. |
| M27 LRGB con assistenza IA | Elaborazione nativa PixInsight su quattro master calibrati/allineati, 4634×2808, senza modificare i master. ABE, composizione RGB, calibrazione colore stellare, BXT/NXT/SXT, stretch, luminanza, contrasto locale, saturazione e reintegrazione stelle. Non è stata applicata SPCC. |
| Dettaglio interno M27 | Due LHE mascherate sulla nebulosa senza stelle; parametri conservati privatamente; ricomposizione con le stelle conservate. Versione precedente conservata. |
| File finali | XISF Float32 non lineare, TIFF RGB16 sRGB, JPEG piena risoluzione e derivato web. Verifiche native e integrità conservate privatamente. Non si dichiara assenza di clipping o qualità scientifica certificata. |
| History dell’ultima versione | 24 viste selezionate, 80 processi, 147 istanze, export di 452929 byte. Viste invariate dopo esportazione. Completezza delle history disponibili, non ricostruzione universale del progetto o replay garantito. |
| Sostituzione pubblicazione | Il 5 ottobre vecchia versione ritirata e nuova versione pubblicata sulla stessa immagine M27, con il relativo workflow. UI archivio e successiva GET pubblica verificate; evidenze private conservate. |
| Sessioni associate | Tutte le 16 sessioni M27 presenti nel catalogo consultato sono associate per dichiarazione Owner; questa associazione non dimostra il contributo di ogni sessione ai master finali. |

## Identità dell’ultima pubblicazione

- Immagine: `IMG-c82f01a62d69990ecb22693d6caf76d2`.
- Versione ritirata: `VER-66396f1a229a92f53d6d64aa9e225976`.
- Versione pubblicata: `VER-5e5dd49a62f90e349e2931f3d143b941`.
- Workflow: `WF-5e5dd49a62f90e349e2931f3d143b941`.
- Data elaborazione: 2026-10-02; pubblicazione: 2026-10-05.

La [evidenza minimizzata](evidence/BKL-049-M27-PUBLIC-2026-10-05.json) deriva da una nuova GET anonima effettuata il 5 ottobre: una sola riga per M27, versione corretta, 80 passi, 16 sessioni, zero parametri pubblici. La GET non dimostra da sola il ritiro privato della vecchia versione o gli hash dei file privati. La [gallery](../scientific-image-gallery/index.md) conserva `PARTIAL`, `NOT_ESTABLISHED` e `OWNER_DECLARED`: l’importer non certifica l’esecuzione anche quando l’elaborazione assistita è documentata separatamente.

## Ripresa del pilota

Seguire il [piano BKL-049-EXT-PIAI](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md). Prima verificare ambiente e disponibilità dei master senza modificarli, poi eseguire una ricetta controllata su copie. Un job per volta; journal privato per ogni azione, output e dipendenza. Le history importate restano dati, mai programmi da eseguire.

La coda P4 è implementata e il cloud/credenziale sono stati approvati e attivati; OAT Owner/nativo ancora aperto. Provider IA con API e comando scientifico P5 non sono attivati. L’abbonamento alla chat non è una credenziale API per un servizio. L’installazione già presente non costituisce attestazione di licenza per usi multiutente o commerciali.

## Handover operativo e rollback

Conservare privatamente originali, XISF/TIFF/JPEG, export, correlazioni, journal di elaborazione e verifiche. Il repository pubblico contiene documentazione, codice e prove minimizzate: niente percorsi privati, parametri integrali, token o binari scientifici.

Per un errore del pilota fermare il job tra i processi, conservare la ricevuta e ripartire da copie nuove. Non sovrascrivere master, prodotti approvati o revisioni pubblicate. Il pilota non richiede sostituzione della M27 pubblicata. Un eventuale ritiro pubblico segue la procedura autenticata e conserva l’archivio privato; non garantisce il richiamo di copie o cache di terzi.

## Gate e registro revisione

Riconciliazione locale e verifica GET effettuate. CI, ARB, Release Quality, merge e verifica Pages della presente revisione devono risultare dalla PR di consegna; non sono anticipati come completati. Versione 1.0: prima riconciliazione cumulativa al 5 ottobre e consegna al pilota locale.

## Aggiornamento successivo — pilota P1 avviato

Riconciliazione documentale consegnata tramite PR #478, merge `351067822c5b5ac0632c57408fd530ad85614914`, 17 controlli exact-head e 18 workflow post-merge SUCCESS; ARB e RQ AI-assistite sequenziali, zero finding finali. Successivamente effettuato il preflight nativo sul PC Owner: PI 1.9.5 build 1706, quattro master integri e invariati, selezione esplicita nei contenitori multi-image e 12 costruttori di processo disponibili. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P1-2026-10-05.json). Nessuna elaborazione pixel o richiesta provider nel test. Versioni moduli, modelli e licenze non attestati dal preflight. P2 esecutore su copie e P3 elaborazione restano successivi; il pilota è avviato, non completo né di produzione. Versione 1.1: esito P1, nuova consegna CI/review da tracciare sulla PR di implementazione.

## Aggiornamento storico — P2 locale verificato

P1 consegnata tramite PR #479, merge `76d6186489c78aceb32f34a6b96afbe8f88457a7`, 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ sequenziali senza finding finali. P2 ora dispone di coordinatore, prenotazione di un job, snapshot esecutore, handle esclusivo Windows, copie verificate e journal privato delle operazioni native. Il lancio rimane supervisionato in PixInsight; nessuna connessione remota è inclusa.

Prova nativa M27: cinque processi riusciti e cinque checkpoint Float32 4634×2808 lineari, con originali invariati. Quattro estrazioni del fondo sulle copie e composizione RGB; luminanza preparata ma non integrata. Pre-cancel nativo con zero processi; replay rifiutato e 37 file del job concluso invariati. [Ricevuta P2](evidence/BKL-049-PIAI-P2-2026-10-05.json). Il workflow derivato contiene solo le cinque operazioni riuscite, leggibili come dati dall’importer 1.2; non rappresenta tutta la History precedente dei master.

Il prossimo gate è P3: elaborazione non lineare, controlli pixel, colore/astrometria e confronto visivo. Questa prova non sostituisce la M27 pubblicata e non ne certifica qualità scientifica. Annullamento durante un processo reale verificato dopo la correzione ARB del canale di richiesta; guasti nativi coperti da test sintetici; crash/offline e connessione remota restano gate futuri. Per un crash conservare la prenotazione e l’evidenza, confermare PixInsight fermo e quarantinare il root prima di usarne uno nuovo. Procedura dettagliata in `tools/pixinsight/local_pilot/README.md`. Versione 1.2: esito P2; CI/review/merge e post-merge da registrare sulla PR della consegna.

Riesame P2: un Major ARB ha rilevato che il comando cancel tentava di leggere il file tenuto con handle esclusivo. Corretto con identità immutabile del job separata e marker completo pubblicato atomicamente, vincolato al token e verificato dal runtime. Prova Windows con handle reale e prova nativa PixInsight: lettura del lease negata, comando cancel riuscito durante il primo processo; arresto prima del checkpoint successivo, un processo registrato, zero output e originali invariati. Il processo in corso può terminare prima dell’annullamento. Il riesame finale richiede CI e ARB/RQ sul nuovo head.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

## Aggiornamento corrente — P3 non lineare

Implementata la ricetta M27 separata: 29 processi nativi e 15 checkpoint, incluso il finale Float32 RGB non lineare. Il journal registra anche maschere e output stelle; l’export delle istanze è dati, non replay o completezza della History a monte. La raccolta legge tutti i pixel finali e conta clipping/canali. La valutazione cromatica è empirica, non SPCC; l’acceptance scientifica rimane Owner review required.

Prova nativa definitiva e confronto visivo completati; evidenza minimizzata riportata di seguito. Consegna CI/review riferita allo stesso head sulla PR. P4 protocollo/provider/diritti e P5–P6 portale/acceptance sono successivi. Nessuna nuova pubblicazione, chiamata provider o authority sui dispositivi. Conservare privatamente XISF, derivati, workflow, correlazioni, manifest e ricevute. [Procedura](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/pixinsight/local_pilot).

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

Verifica candidato P4: 33 test Node e 62 Python Windows, inclusi 32 casi trasporto. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P4-2026-10-05.json). CI/review dello stesso head e post-merge da registrare sulla PR; nessuna attivazione cloud anticipata.

Riesame P4: un Major ARB ha riprodotto una seconda preparazione su root nuovo privo di binding. Corretto con identità locale persistente fissata dalla prima claim e transizione PREPARING confermata prima delle copie; claim avanzata senza binding rifiutata. Cinque regressioni coprono nuovo root, stati avanzati, perdita della risposta iniziale e preparazione interrotta. CI e riesame finale dello stesso head richiesti sulla PR.

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

## Correzione compatibilità target durante il collaudo P5

Accesso Owner sulla nuova pagina verificato. Nessun job scientifico creato: confronto letterale `M27`/`M 27` rendeva invisibili le sessioni e il parent reali. Correzione con soli due alias espliciti, contesto originale conservato, tre regressioni e verifica locale dei profili pubblici reali (16 sessioni/un parent). Correzione candidata da rilasciare; il percorso Owner HTTP → nativo → consegna privata resta aperto. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md).


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json).


## P5b — cartella dei master e prompt (candidato del 5 ottobre 2026)

Incremento autorizzato dall’Owner dopo l’accettazione privata P5 e la conferma dei download. Il modulo aggiunge cartella locale assoluta e prompt, richiesta privata di pianificazione, verifica esplicita sul PC, proposta immutabile e conferma Owner dell’esatto piano prima della coda PixInsight. Nessun job alla sola ricezione del prompt; nessuna lettura automatica del disco o esecuzione di testo/script dal browser. SESSION_ASSISTED: questa sessione interpreta il prompt e propone ricetta, parametri ammessi di fondo, dettaglio, rumore, contrasto e stretch, motivazione e limiti; nessuna nuova API IA, risorsa, credenziale o espansione IAM. Il perimetro richiesto include altri oggetti importati, LRGB, OSC, SHO/HOO e mosaici da pannelli. Il candidato comprende inventario e selezione esplicita; le nuove ricette per campo singolo richiedono parametri di campo verificati. OSC CFA e assemblaggio mosaici restano bloccati fino a implementazione e collaudo nativo. [Stato e procedura](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md). Nessuna estensione è ancora pubblicata o dichiarata accettata.

Il piano conserva ruoli R/G/B/L, dimensioni, selezione esplicita dell’immagine nei contenitori, impronta del manifest e sequenza dei 29 processi. Cartella, prompt e piano sono dati privati Owner; master/hash individuali e diagnostica locale restano sul PC. Il worker confronta cartella, piano e manifest prima delle copie. Aggiornamenti di catalogo o riferimenti conflittuali fermano l’approvazione; retry identici non duplicano richieste/job. I vecchi risultati P5 rimangono accessibili e invariati. Il candidato richiede CI sull’head esatto, ARB/RQ sequenziali, merge, deployment API/Pages e prova Owner della nuova procedura; non è ancora dichiarato disponibile nel portale pubblico. P6 e acceptance operativa restano aperti.

## Aggiornamento P5b — 6 ottobre 2026

Ulteriore avanzamento locale: contratto comune di preparazione, esecutore con richiesta immutabile e runtime conservato, raccolta indipendente con controllo di sorgenti/copiate, sequenza e correlazioni, hash, intestazioni e tutti i pixel mono/RGB. Le suite aggiornate hanno superato 112 test Python e 68 JavaScript. Le intestazioni dei master con History sono ammesse fino a 4 MiB, limite verificato con regressione. Il collaudo nativo del nuovo esecutore comune sui quattro pannelli M31 è distinto dalla precedente prova del kernel; fino alla sua raccolta verificata non è dichiarato completato. Validazione delle istanze native esportate e integrazione con approvazione/coda/consegna nel portale restano aperte. I numeri delle suite nel paragrafo seguente sono lo snapshot precedente.

Esito successivo: il collaudo nativo dell'esecutore comune è `COMPLETED` e raccolto con verifica indipendente dei quattro originali, quattro copie e tutti i pixel dei cinque output RGB Float32 7510×5164. La prenotazione è chiusa. Un audit separato ha analizzato l'istanza GradientMergeMosaic e confermato parametri e dipendenze esatte; lo stato `PENDING` della prima ricevuta del raccoglitore resta conservato, con audit distinto successivo. I test ora passati sono 114 Python e 68 JavaScript; la build documentale è passata. Nessuna modifica al servizio o al portale pubblicato; nuove ricette complete, integrazione della preparazione con la coda approvata, collaudo Owner, release e P6 restano da completare.

Il candidato include selezione immutabile dei pannelli e conferma Owner dell'esatto digest, separata dalla conferma del piano esecutivo. La selezione non crea job e non avvia PixInsight. Verifiche sintetiche: 102 Python e 58 JavaScript passate; build documentale completata. Il collaudo locale M31 LPRO ha prodotto un mosaico lineare RGB Float32 7510×5164; otto originali, quattro copie e cinque output verificati tramite SHA256, tutti i pixel finali finiti e nell'intervallo [0,1]. Il primo tentativo fallito per risultato nativo Float64 resta conservato; il secondo registra la conversione esplicita a Float32. Debayer VNG è verificato nativamente sui quattro pattern Bayer con immagini sintetiche. Entrambe le prenotazioni di collaudo sono chiuse. Le sessioni M31 precedono il portale: nessuna associazione fittizia al catalogo è stata creata. Collegamento della preparazione alla coda, nuovi profili completi, accettazione scientifica, pubblicazione del candidato e P6 restano aperti. Evidenza minima e limiti sono nel [dossier P5b](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md).

## Avanzamento candidato P5b: conferma della preparazione e consegna

Il candidato integra ora conferma Owner del piano di preparazione, raccolta indipendente versione 1.1 con analisi delle istanze native, associazione dei master preparati al piano finale e workflow combinato preparazione/ricetta. Le conferme sono separate e vincolate ai rispettivi digest; nessun avvio nativo automatico. 125 test Python e 71 JavaScript PASS. La prova nativa OSC sul mosaico M31 è ora COMPLETED e raccolta indipendentemente: 26 operazioni, 12 checkpoint, 26 istanze esportate; finale RGB Float32 7510×5164 non lineare, tutti i pixel finiti e normalizzati. Gli otto master originali e il mosaico lineare usato come input sono invariati; prenotazione chiusa dopo la verifica. È una prova tecnica locale, senza associazione al catalogo, accettazione scientifica o prova della catena unica preparazione/ricetta approvata dall’Owner nel portale. La History precedente resta NOT_ESTABLISHED. Le sessioni M31 anteriori al portale non sono inventate né associate a M27. Questo aggiornamento supera le precedenti note sul collegamento ancora da implementare; rilascio, controlli del commit esatto, review e percorso autenticato reale restano aperti. I precedenti artefatti nativi non sono riscritti con la nuova versione del raccoglitore. Nessun nuovo costo API IA, risorsa cloud o permesso IAM. P6 resta aperto.

La prima ARB del candidato ha rilevato un Major sulla scrittura del terminale senza ownership verificata del lease e un Minor sulla procedura precedente. Il candidato corretto non scrive artefatti da un tentativo respinto e rilascia il lease anche quando la scrittura del terminale fallisce; entrambe le condizioni hanno regressioni sintetiche. Procedura riconciliata. Nuovi CI, ARB e RQ sul commit esatto restano necessari prima del rilascio.


## Rilascio P5b verificato — 6 ottobre 2026

La PR [#488](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/488) è integrata nel commit `ebbb7d3c1034130ef49df674fcc596c0403647f0`. Il codice revisionato è `bd628c51d0b5f76f22bf94a3ba8c8b673ed0c289`, albero `ed8a9ef7ac6fb640408621c5d1256ce5d4c1f945`: CI completa, ARB e RQ AI-assistite separate e sequenziali PASS, zero finding residui. La prima ARB fallita resta storica; il difetto di ownership della prenotazione e la procedura obsoleta sono corretti e verificati. Merge eseguito secondo DSG-AEM-001 e W-DSG-AEM-RULESET-001, senza deroga alla CI. Tutti i 17 workflow post-merge, inclusa la pubblicazione Pages, sono SUCCESS sul merge SHA.

Cloud Build `78bb9d31-1b02-46f9-ab63-b088ee8ccfea` SUCCESS sul codice revisionato, con 125 test Python. Il servizio esistente usa la revisione `dsg-pixinsight-pilot-p5b-bd628c51`, traffico 100%, immagine per digest `sha256:ddf1abe4369c5b682ddc92d377dbb6e77d3905a349b45a759905c56bafa337d8`. Prove HTTP reali PASS: health SESSION_ASSISTED e zero richieste provider, lettura worker autenticata, rifiuto degli accessi anonimi e delle approvazioni Owner da worker, rifiuto delle chiamate browser ai percorsi worker; stato invariato e nessun avvio nativo. Non sono state create risorse, credenziali o autorizzazioni IAM.

La [pagina pubblica](https://maininimassimo-bit.github.io/digital-stargate-manual/pixinsight-pilot/) è verificata nel browser: cartella locale, prompt, LRGB, OSC RGB/CFA, SHO/HOO e mosaico da pannelli sono presenti. L'accesso Google Owner e la nuova catena completa di conferme nel portale restano da collaudare; la verifica senza login non li sostituisce. Il pulsante Google incorporato richiede il clic dell'Owner perché il controllo browser non può indirizzarlo. Le prove native M31 restano tecniche locali su copie, senza sessioni inventate, accettazione scientifica o pubblicazione della foto. L'accettazione privata M27 precedente resta conservata. P6 e acceptance operativa dei nuovi profili restano aperti.

Rollback API: ripristinare il traffico sulla revisione precedente `dsg-pixinsight-pilot-p5-target-01` e riconciliare la pagina con il codice precedente, senza cancellare richieste, ricevute e risultati privati immutabili. Questo aggiornamento supera esclusivamente le precedenti note di candidato non pubblicato e gate di rilascio pendenti; conserva le limitazioni scientifiche e gli snapshot storici.


## Master storici senza sessioni importate — 6 ottobre 2026

La correzione Owner chiarisce che M27 è già elaborata e pubblicata; il nuovo collaudo riguarda M31, i cui pannelli precedono il portale. Il modulo distingue «Sessioni già importate» da «Riprese storiche senza sessioni nel portale». Il secondo percorso richiede nome dell'oggetto, provenienza dichiarata e conferma Owner. Non richiede sessioni, catalogo o immagine di riferimento: conserva `sessionIds=[]`, `catalogSha256=null`, `parent=null` e associazione al catalogo `NOT_ESTABLISHED`. La data richiesta è la data di elaborazione, non una data di ripresa inventata.

La dichiarazione `historicalSource` è immutabile e vincola registrazione degli input, selezione dei pannelli, piano esatto, coda, contesto locale e ricevuta privata. Il worker non può registrare un oggetto storico arbitrario senza la richiesta Owner corrispondente. I pannelli storici hanno associazioni di sessione vuote; profili, file, indici, astrometria, griglia, copie, raccolta verificata e conferme separate mantengono gli stessi controlli. La consegna conserva `HISTORICAL_OWNER_DECLARATION` e zero sessioni. Nessuna nuova sessione scientifica, ammissione al registro o pubblicazione è generata. M31 non usa la ricetta o le sessioni di M27.

«Ritira richiesta» conserva proposta e ricevute e impedisce nuove approvazioni e l'ingresso in coda, anche se il ritiro vince tra scrittura del contesto e commit della coda. È ammesso prima del job e dell'approvazione della preparazione nativa; non sostituisce annullamento e recupero di elaborazioni già autorizzate. La richiesta M27 creata erroneamente dall'assistente è un piano non eseguito: va ritirata tramite questo percorso, preservando il risultato M27 precedente.

Validazione sintetica locale: 135 Python e 74 JavaScript PASS, inclusi limiti della provenienza, idempotenza, assenza di sessioni inventate, vincolo di registrazione, consegna privata, ritiro e ruoli HTTP. Gate di rilascio CI → ARB → RQ e verifiche post-merge registrati nella PR di consegna. Le prove non sostituiscono il nuovo collaudo Owner M31 nel portale né accettazione scientifica, History a monte, pubblicazione o P6. Le precedenti note che limitano la procedura alle sessioni importate sono superate esclusivamente da questo ingresso storico esplicito.
