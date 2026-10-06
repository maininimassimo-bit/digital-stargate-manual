# P5b — master, prompt e profili scientifici

Stato: **codice, API e pagina P5b pubblicati; collaudo Owner della nuova procedura e acceptance dei profili aperti**. L'accettazione privata del precedente risultato M27 non equivale all'accettazione di questi profili.

## Perimetro autorizzato

L'Owner ha richiesto cartella dei master e prompt di elaborazione, altri oggetti delle sessioni scientifiche importate, LRGB, banda stretta, OSC e mosaici composti da pannelli da unire. L'assistente resta quello della sessione: nessuna nuova chiamata API IA a pagamento, credenziale, risorsa cloud o espansione IAM.

## Procedura

1. Selezionare l'oggetto dal catalogo delle sessioni importate, tipo dei master, campo singolo o pannelli, cartella principale ed eventuali altre cartelle del mosaico.
2. Scrivere l'obiettivo di elaborazione e associare le sessioni reali dello stesso oggetto. Inviare conserva una richiesta privata di pianificazione; non avvia PixInsight.
3. L'assistente esegue un inventario locale esplicito. I contenitori con più immagini e i file ambigui richiedono una selezione precisa di file e indice immagine. Per i mosaici l'assistente propone una selezione immutabile dei pannelli, con ruoli, file, indici e sessioni; l'Owner conferma l'esatto digest di questa selezione. La conferma autorizza la verifica dei master selezionati, non crea un job e non avvia PixInsight. Master normali, drizzle, riferimenti di normalizzazione e mappe di rigetto restano distinti.
4. Verificare linearità, canali, registrazione, astrometria e, per mosaici, sovrapposizioni e associazione dei singoli pannelli. L'intestazione XISF da sola non certifica l'idoneità scientifica.
5. Proporre un piano immutabile con sorgenti identificate, parametri ammessi, regioni del fondo, azioni, checkpoint, motivazione e limiti. L'Owner conferma l'esatto digest del piano prima dell'ingresso in coda.
6. Avviare l'esecuzione supervisionata su copie. Controllare risultato, workflow runtime e correlazioni prima dell'accettazione privata. La pubblicazione resta una decisione separata.

## Stato implementato nel candidato

| Profilo | Sorgenti | Candidato esecutore | Verifica nativa nuova |
| --- | --- | --- | --- |
| LRGB | R, G, B, L mono registrati | 29 azioni, 15 checkpoint | Da completare per altri campi |
| OSC RGB | RGB già demosaicizzato | 26 azioni, 12 checkpoint; luminanza derivata | Ricetta verificata localmente sul mosaico M31; prova Owner nel portale aperta |
| SHO | SII, Ha, OIII mono | 27 azioni, 15 checkpoint; luminanza derivata da Ha | Da completare |
| HOO | Ha, OIII mono | 26 azioni, 14 checkpoint; luminanza derivata da Ha | Da completare |
| OSC CFA | Mono CFA, pattern Bayer esplicito | Preparazione Debayer con conferma separata; successiva coda OSC | API nativa verificata sui quattro pattern con dati sintetici; dati reali e integrazione aperti |
| Mosaico | 2–16 pannelli selezionati | Selezione confermata separatamente; preparazione riproiezione e GradientMergeMosaic con conferma separata; successiva coda del profilo | Assemblaggio LPRO M31 verificato localmente; integrazione e accettazione aperte |

I profili generali richiedono parametri di campo espliciti; non riutilizzano automaticamente la regione di fondo di M27. SHO/HOO rappresentano palette assegnate e non certificano colori fotometrici. La luminanza OSC è derivata da RGB e non rappresenta una ripresa indipendente in filtro L. Il workflow runtime registra le operazioni della nuova esecuzione; la completezza della History precedente resta `NOT_ESTABLISHED`.

## Evidenza locale reale M31

La cartella fornita dall'Owner contiene quattro pannelli OSC RGB per ciascuno dei gruppi LPRO ed Extreme, varianti drizzle, riferimenti di normalizzazione e master di calibrazione. I master normali contengono l'immagine `integration` e mappe di rigetto; queste ultime sono escluse dalla selezione scientifica. L'immagine integration del primo pannello LPRO contiene proprietà astrometriche native: l'assenza di keyword FITS CTYPE non dimostra assenza di astrometria.

Il successivo controllo nativo in PixInsight 1.9.5 build 1706 ha letto tutte le otto immagini integration: RGB Float32, 4128×2808 pixel, astrometria presente su ciascuna. Il motore ufficiale MosaicByCoordinates 1.4.4 ha calcolato una superficie di 7510×5164 pixel per entrambi i gruppi. Centro, scala e rotazione dei due gruppi non sono identici: un'eventuale fusione richiede una griglia comune esplicita. Il controllo ha prodotto zero operazioni sui pixel e ha lasciato zero viste aperte, come all'inizio. I parametri nativi di GradientMergeMosaic, Debayer e StarAlignment sono stati letti separatamente; questo prova disponibilità dei costruttori, non il successo di un assemblaggio o Debayer.

L'Owner ha chiarito che le riprese M31 precedono il portale e le relative sessioni non sono importate. Questo consente il collaudo tecnico locale sulle copie, mantenendo l'origine storica e senza creare associazioni scientifiche nel portale. Un'eventuale futura associazione richiederà evidenze delle sessioni reali; non è necessaria per il collaudo locale corrente. Non si associano i pannelli M31 alle sessioni M27 né si inventano nuove sessioni. Percorsi locali e hash individuali restano negli artefatti privati.

Il primo assemblaggio LPRO ha completato le quattro riproiezioni e GradientMergeMosaic, ma è stato classificato `FAILED`: il risultato nativo Float64 era diverso dal formato Float32 richiesto dal candidato. La verifica esterna ha confermato l'integrità dei quattro originali e delle copie prima di chiudere la prenotazione fallita. Il kernel ora ammette il risultato reale Float64, registra il completamento di GradientMergeMosaic e applica una conversione esplicita `ImageWindow.setSampleFormat(32,true)`, anch'essa registrata. La seconda prova usa una nuova identità e gli stessi input copiati e riverificati, conservando gli artefatti della prova fallita. Un mosaico lineare non equivale a una foto finale non lineare né ad accettazione scientifica.

Aggiornamento 6 ottobre 2026: la seconda prova è `COMPLETED`. La raccolta esterna ha verificato gli hash degli otto originali, delle quattro copie e dei cinque output; risultato RGB Float32 7510×5164, con tutti i pixel finali finiti e compresi in [0,1]. Le quattro riproiezioni, l'istanza nativa GradientMergeMosaic e la conversione Float64→Float32 sono conservate nel journal; l'export JS contiene solo l'istanza nativa, mentre le operazioni PJSR restano nelle correlazioni. È un collaudo amministrativo locale, senza associazione al catalogo o pubblicazione; accettazione scientifica e risultato non lineare restano aperti. La prenotazione locale è stata chiusa dopo la verifica.

Un successivo collaudo API nativo ha eseguito Debayer VNG sui pattern RGGB, BGGR, GBRG e GRBG, usando quattro immagini CFA sintetiche 128×128. Ogni risultato è RGB Float32 della stessa geometria, con corrispondenza dei canali verificata sul pixel centrale. Le viste preesistenti sono state conservate e la prenotazione è stata chiusa dopo la verifica di identità e journal. Questo prova l'interfaccia del kernel nell'installazione locale; non costituisce accettazione di master CFA reali o del percorso completo nel portale.

## Verifiche e lavoro residuo

Il candidato locale include ora un contratto comune di preparazione per LRGB, OSC RGB/CFA, SHO/HOO e pannelli. La richiesta, i ruoli fisici, gli indici delle immagini, la griglia e gli hash sono conservati insieme a copie verificate e snapshot del runtime. L'esecutore controlla tutte le sorgenti prima di operare sui pixel, salva i checkpoint e registra Debayer, trasferimento astrometrico, riproiezione, GradientMergeMosaic e conversione del formato. Il raccoglitore verifica indipendentemente sorgenti, copie, output, sequenza nativa, dipendenze e tutti i pixel RGB o mono prima di chiudere la prenotazione. Questo era lo stato della prima implementazione locale; il candidato successivo descritto sotto integra ora la conferma separata e il collegamento alla coda, ancora senza rilascio o collaudo autenticato reale.

I master reali M31 hanno intestazioni XISF con History fino a circa 1,07 MB. Il lettore di inventario e selezione accetta ora intestazioni fino a 4 MiB, mantenendo il rifiuto di intestazioni superiori, entità XML, immagini ausiliarie e indici ambigui. Il limite precedente di 1 MiB rifiutava uno dei pannelli prima dell'avvio nativo.

Il successivo collaudo nativo dell'esecutore comune è completato e raccolto indipendentemente: quattro sorgenti originali e quattro copie invariate, cinque output RGB Float32 7510×5164, tutti i pixel di ciascun output finiti e normalizzati. Sono registrate quattro riproiezioni, GradientMergeMosaic e conversione esplicita del formato. La prenotazione è chiusa dopo la verifica. Un audit separato ha analizzato l'istanza nativa come dati e verificato file registrati e parametri di fusione; il raccoglitore di questa esecuzione conserva il proprio stato precedente `nativeInstanceValidation: PENDING`, mentre l'audit successivo è un artefatto distinto. Non è una prova della coda del portale né un risultato non lineare o una certificazione di qualità delle giunzioni.

Le suite sintetiche verificano separazione pianificazione/coda, identità immutabili, ruoli e indici immagine, profili di altri oggetti, parametri limitati, conteggi, correlazioni e rifiuto dei profili non ancora eseguibili. Questi risultati non costituiscono un collaudo nativo o un'accettazione scientifica.

Prima della consegna: completare i collaudi dei nuovi profili in PixInsight su copie, eseguire i controlli del commit esatto e le review previste dal mandato, pubblicare il candidato e verificare la procedura reale autenticata. P6 resta aperto.

## Collegamento candidato della preparazione alla consegna — 6 ottobre 2026

La selezione dei pannelli, la preparazione lineare e l'elaborazione finale hanno conferme distinte dell'Owner, ciascuna vincolata al digest esatto. La nuova conferma «preparazione dei master» mostra file, indici, ruoli, pattern Bayer e griglia del mosaico; non crea il job finale. L'assistente prepara copie soltanto dopo la conferma e l'avvio nativo resta supervisionato. Il raccoglitore aggiornato analizza le istanze native come dati e verifica parametri, journal, runtime, originali, copie e tutti i pixel dei checkpoint; conserva una verifica versione 1.1 e chiude la prenotazione soltanto dopo il successo.

Il piano finale richiede il risultato verificato della preparazione e la sua associazione immutabile alla richiesta. L'approvazione del piano finale crea il job del profilo corrispondente; CFA produce master RGB per il successivo profilo OSC. L'export comprende le istanze della preparazione prima di quelle della ricetta e le correlazioni delle riproiezioni e conversioni. I file locali delle istanze GradientMergeMosaic sono rappresentati da risorse logiche nell'export; le istanze esatte restano nel journal privato. Questo non certifica la History precedente dei master.

Verifica del candidato locale: **125 test Python e 71 test JavaScript PASS**. I test includono la separazione delle conferme e della coda, i cinque profili di mosaico, i digest, i rifiuti di artefatti modificati e l'autorità distinta dell'Owner e del worker. Sono prove sintetiche del contratto, non accettazione scientifica o prova completa autenticata nel portale. La prova nativa OSC sul mosaico M31 è ora COMPLETED e raccolta indipendentemente: 26 operazioni, 12 checkpoint, 26 istanze esportate; finale RGB Float32 7510×5164 non lineare, tutti i pixel finiti e normalizzati. Gli otto master originali e il mosaico lineare usato come input sono invariati; prenotazione chiusa dopo la verifica. È una prova tecnica locale, senza associazione al catalogo, accettazione scientifica o prova della catena unica preparazione/ricetta approvata dall’Owner nel portale. La History precedente resta NOT_ESTABLISHED. M31 resta una prova locale senza associazioni inventate al catalogo. Candidato non pubblicato; controllo del commit esatto, review, rilascio e verifica autenticata restano aperti.

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

Validazione sintetica locale: 136 Python e 74 JavaScript PASS, inclusi limiti della provenienza, idempotenza, assenza di sessioni inventate, vincolo di registrazione, consegna privata, ritiro e ruoli HTTP. Gate di rilascio CI → ARB → RQ e verifiche post-merge registrati nella PR di consegna. Le prove non sostituiscono il nuovo collaudo Owner M31 nel portale né accettazione scientifica, History a monte, pubblicazione o P6. Le precedenti note che limitano la procedura alle sessioni importate sono superate esclusivamente da questo ingresso storico esplicito.


Sospensione delle nuove richieste storiche: impostare DSG_PIAI_HISTORICAL_INTAKE=0 sul servizio corrente, mantenendo lettura delle ricevute, ritiro e guardie della coda. Non ripristinare il vecchio backend che ignora i ritiri o la provenienza storica dopo che questi record sono stati creati. Un recupero del codice deve conservare tali controlli e i record immutabili; eventuali job autorizzati seguono annullamento e recupero supervisionati.
