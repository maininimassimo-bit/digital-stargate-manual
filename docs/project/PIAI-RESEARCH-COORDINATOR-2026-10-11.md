# PixInsight — coordinatore di prove e scelta dei rami

| Campo | Valore |
|---|---|
| Versione | `DSG_PIAI_RESEARCH_V1`, rilascio tecnico 11/10/2026 |
| Stato | Backend research-lineage-v1 attivo e portale pubblicato; M27 2ffd1ae8: 12 API note / 6 prove native, STOP dopo confronto della fusione CP006; controllo CP005 conservato, nessun finale consegnato o accettato |
| Perimetro | LRGB, campo singolo, campionamento originale, inventario QHY695A/ZWO RGB/Optolong L-Pro L |
| Conoscenza | `DSG_PIAI_RESEARCH_KNOWLEDGE_V1`, distinta dal pacchetto scientifico storico V1 |

## Come il coordinatore decide

La ricetta indica la struttura degli ingressi e l'intento dell'Owner. Il coordinatore riceve un protocollo scientifico versionato, le misure native dei master e dei checkpoint, i limiti strumentali e le immagini di confronto. La guida contiene le ipotesi pertinenti a ogni famiglia di prove, precondizioni, controindicazioni, difetti da cercare, criteri di confronto e condizioni di arresto. Questo requisito è registrato anche nel bootstrap: conoscere i nomi dei processi non basta a scegliere un ramo.

Il primo catalogo di prove ammette la sequenza calibrazione SPCC, dettaglio, rumore, stretch, fusione LRGB, presentazione e verifica finale. Le fasi di dettaglio, rumore e presentazione possono conservare il controllo senza trattamento. Il modello decide se una prova è utile, quali parametri ammessi provare e quale risultato verificato preferire. La sequenza conserva la deconvoluzione prima del denoise e dello stretch e distingue il checkpoint cromatico lineare dal risultato di presentazione.

| Fase | Alternative ammesse | Evidenze e rischi da valutare |
|---|---|---|
| Calibrazione | SPCC con profilo strumentale fissato | WCS della griglia RGB, curve, QE, riferimento bianco, catalogo spettrale, regressioni e copertura; niente neutralizzazione del fondo implicita |
| Dettaglio | Controllo, BlurXTerminator correction only, sharpening moderato | Morfologia stellare, ali e nuclei, filamenti, aloni, ringing, tessitura artificiale; FWHM descrittiva |
| Rumore | Controllo, NoiseXTerminator entro i limiti confermati | MRS a scale e supporti dichiarati, struttura debole, grana e perdita di tessitura; MRS non equivale a SNR |
| Stretch | Alternative MaskedStretch nel catalogo | Headroom, estremi dei campioni, nuclei, fondo, rapporti cromatici e dominio non lineare |
| Fusione | LRGBCombination verificata | Differenze di PSF e risposta spettrale di L-Pro, diluizione del colore, allineamento e aloni |
| Presentazione | Controllo, saturazione moderata con CurvesTransformation | Clipping dei canali, rumore cromatico, stelle sovrasature; scelta estetica dichiarata |

Ogni alternativa nasce dal medesimo genitore esatto; non si accumulano ripetutamente deconvoluzioni o denoise per cercare un numero migliore. Il controllo e tutti i fratelli della fase accompagnano la decisione. Le anteprime usano la stessa curva di display e comprendono campo intero RGB/L e un ritaglio centrale di 256 pixel per traccia, senza ricampionamento del ritaglio. Il ritaglio centrale è una copertura limitata: non certifica l'assenza di difetti in tutte le stelle o ai bordi. Nella fase di stretch il display identità comune rende esplicito il cambio di dominio.

La PSF viene nuovamente rilevata per checkpoint: le popolazioni non sono appaiate, perciò il confronto dei loro riassunti non misura una variazione sulle stesse stelle. Il coordinatore deve dichiarare questa limitazione e non scegliere soltanto dal minimo rumore/FWHM/eccentricità. Le verifiche su tutti i campioni distinguono valori negativi, maggiori di uno ed esattamente zero/uno: questi conteggi non dimostrano, da soli, che un processo abbia causato clipping.

La scelta deve spiegare il beneficio cercato, le evidenze osservate, i danni rilevati e le incertezze. Se il controllo è preferibile, va conservato. Se mancano evidenze indispensabili o una capacità eseguibile, va richiesto un arresto con ricevute conservate. «Migliore» significa preferito fra le alternative realmente provate nel perimetro confermato; non ottimo globale né nuova risoluzione fisica dimostrata.

## Evidenze SPCC reali di sviluppo

Prova su copie dei quattro master WBPP M27, griglia 4634 × 2808, PixInsight 1.9.5 build1706. Originali SHA invariati; RGB costruito nativamente con soluzione astrometrica ereditata e SPCC completato. Il nuovo adapter ha conservato checkpoint, History, sorgenti native dei processi e misure; verifica Python dei campioni finiti completata. Questa prova non è un nuovo job nel portale, una chiamata API reale, una scelta autonoma o accettazione scientifica.

Un secondo tentativo distinto ha eseguito BlurXTerminator correction only su copie del checkpoint SPCC RGB/L, con le dipendenze e il selettore modello fissati. Ricevuta terminale, originali, input del genitore, checkpoint, History e tutti i campioni verificati. Dimostra l'esecuzione del ramo tramite il nuovo adapter; non dimostra un miglioramento né che questo ramo debba essere scelto per il finale M27. I tentativi preliminari falliti restano conservati come evidenza di sviluppo.

| Prodotto osservato | Valore |
|---|---|
| Stelle comuni RGB esportate | 70, presenti nelle 16 celle 4×4 |
| Retta R/G | pendenza 0,644231; intercetta −0,165701; sigma nativa stampata 0,052101 |
| Retta B/G | pendenza 0,737704; intercetta 0,015599; sigma nativa stampata 0,096741 |
| Fattori RGB nativi stampati | 0,9458 / 0,7519 / 1,0000 |
| Curve | ZWO R/G/B nominali; Ideal QE curve sostitutiva; Average Spiral Galaxy |
| Luminanza | Optolong L-Pro; escluso dal profilo RGB |
| Fondo SPCC | Neutralizzazione disabilitata; la ROI operativa non prova cielo vuoto |

Il CSV `SPCC-data.csv` della versione installata contiene coordinate e rapporti catalogo/immagine delle stelle comuni, senza flag di rigetto della regressione robusta. L'adapter conserva i prodotti originali localmente e proietta verso OpenAI soltanto aggregati. MAD/RMS dei residui delle righe esportate sono descrittivi e distinti dalla sigma nativa; non si inventano il numero degli inlier o la loro incertezza.

Il rapporto del riferimento bianco viene ricostruito indirettamente dai fattori normalizzati nativi: se la retta è `y = a*x + b`, `x_white = (W_G/W_R − b)/a` per R/G e analogamente per B/G. Intervalli conservativi comprendono l'arrotondamento di stampa dei fattori e dei coefficienti. Per questa prova risultano interni agli intervalli catalogo esportati. È una verifica di inclusione da prodotti nativi arrotondati, non una nuova integrazione dello spettro, una validazione della QE reale o una stima dell'errore fotometrico. Se l'inclusione non è stabilita, il catalogo impedisce la selezione di SPCC.

## Contratti, portale e conservazione

Il servizio usa Responses con una singola funzione strutturata `choose_pixinsight_action`: `TEST`, `SELECT`, `FINISH`, `STOP`. Argomenti, fase, genitore, limiti, checkpoint e binding dello stato sono validati prima dell'esecuzione. Il modello non fornisce codice, espressioni native o percorsi. [Function calling OpenAI](https://developers.openai.com/api/docs/guides/function-calling).

Il portale raccoglie i consensi per metadati, statistiche e anteprime. Dopo l'analisi locale mostra il perimetro esatto da confermare: sorgenti/runtime/protocollo fissati, inventario e approssimazioni, griglia originale, ROI misurata e catalogo. L'Owner conferma l'esecuzione delle prove su copie. Il worker già esistente coordina poi le decisioni e le operazioni native senza richieste alla chat. L'accettazione finale resta un evento privato distinto dalla conferma iniziale; nessuna pubblicazione automatica.

Limiti tecnici iniziali: 32 prenotazioni API, 16 prove native, tre alternative per fase; SPCC e fusione ammettono una sola prova ciascuno. Questi limiti delimitano la sessione approvata; non ripristinano la quota giornaliera di una chiamata, già rimossa. Non sono un prezzo massimo garantito. Il modello rimane `gpt-6-luna` e la chiave rimane sul backend.

Prenotazioni, risposte, conoscenza, approvazioni e prodotti sono conservati con impronte e ricevute immutabili. Una risposta API persa non viene reinviata; una risposta già salvata può essere riconciliata senza seconda chiamata. Un avvio nativo incerto non viene ripetuto. Il worker condivide lock e lease con il ciclo precedente, usa una nuova istanza isolata e conserva tentativi falliti. Il finale include XISF, anteprima e archivio di checkpoint/rami/History; per ripetere servono gli originali e il runtime con licenza esterni, quindi l'archivio non è una riproduzione autonoma.

## Attivazione, compatibilità e collaudo

Il gate `DSG_PIAI_RESEARCH=LOCAL_WORKER_VERIFIED` è attivo dopo la verifica in sola lettura del worker, insieme al gate adattivo esistente. Il profilo locale protetto `research.profilePath`/`profileFileSha256` contiene le curve installate e le basi Gaia; `research.backgroundROI` deve coincidere con una regione misurata e con il binding dell'analisi. Niente chiave OpenAI o token nel file del profilo.

Il vecchio contratto V2, i job conclusi e il pacchetto scientifico V1 rimangono distinti. SHO/HOO/OSC, mosaici, BIN2, maschere, starless, MLDenoise e correzioni di gradiente non appartengono a questo primo catalogo autonomo. La guida può citarli ma non li abilita. Non dichiarare l'intera conoscenza operativa di PixInsight disponibile da un catalogo finito.

## Evidenze del rilascio tecnico

PR [579](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/579), head revisionato `5ef1460ac8273fca4f4827993b749d261b870fae`, merge `e2b13c7abd2f861284d973a7ea6914b6820145d2`: ARB poi RQ AI-assistite, separate, APPROVED senza finding residui; 15/15 controlli exact-head e 16/16 post-merge SUCCESS, inclusa pubblicazione Pages. Applicata la deroga continuativa `W-DSG-AEM-RULESET-001` con tutti i gate sostitutivi verificati. I CRLF del controller sono preservati con `-text` per le impronte dei byte.

Build `29241fb7-1955-4e33-82cf-59248301e35d` SUCCESS; immagine `sha256:cab5d08bb29c8c997796391383585d0d5691df4f3ba3bb1b88f6f15169881083`; revisione `dsg-pixinsight-pilot-research-v1-20261011`, traffico 100%. Prima della promozione: health HTTP200, dati privati/options HTTP403 anonimi; ambiente precedente, identità, risorse, concorrenza e timeout invariati, salvo il nuovo gate. Nessuna nuova credenziale o modifica IAM.

Worker aggiornato con moduli revisionati e byte nativi V2 preservati. Preflight in sola lettura: R/G/B/L, griglia 4634 × 2808, profilo e factory approvata verificati; zero chiamate provider e avvii nativi. Primo polling interrotto durante il cambio di backend; successiva diagnostica autenticata di elenco e contesto precedente, ciclo singolo e riavvio completati. La causa dell'interruzione non è accertata; non è una prova generale di recovery automatico. Ricevute e tentativo conservati.

Nuova richiesta M27 creata dall'interfaccia Owner con le stesse 16 sessioni già dichiarate per i master. Analisi iniziale completata; portale in `AWAITING_OWNER_PERIMETER`, zero prove/API. Verificata la catena portale → worker → analisi → conferma richiesta; OAT conferma → API → prove → consegna e accettazione scientifica ancora pendenti. I test sintetici e le prove native di sviluppo non li sostituiscono.

Rollback: ripristinare il traffico su `dsg-pixinsight-pilot-scientific-v1-20261011` e il wrapper/worker precedente, preservando impostazioni, tentativi e ricevute. Spegnere il gate blocca nuove approvazioni, decisioni e avvii; risposte o avvii indeterminati non vengono ripetuti automaticamente.


## Primo OAT dal portale e diagnostica candidata

L’Owner ha confermato il perimetro M27 `b013b0bb` il 11/10/2026: fino a 16 prove native e 32 richieste API, tre alternative per fase, copie alla risoluzione originale e approssimazioni SPCC dichiarate. La prima chiamata è stata riservata e tentata; il servizio ha restituito un errore dopo circa 7,8 secondi e lo stato autenticato è `API_INDETERMINATE_NO_RETRY`, contatore API 1, nessuna decisione validata e nessuna prova nativa. Il tempo di risposta non identifica la causa. Non sono disponibili risposta/uso del provider nella ricevuta storica: non attestare consumo zero né successo del passaggio della conoscenza. Nessun reinvio automatico e nessuna accettazione.

La correzione candidata conserva per i futuri errori una ricevuta immutabile minimizzata: ragione da elenco chiuso, presenza/stato della risposta, eventuale ID, uso coerente dei token, causa ammessa di risposta incompleta e codice HTTP. Non conserva messaggi d’eccezione, corpi HTTP, prompt, chiavi o immagini. Hash e riepilogo accompagnano lo stato autenticato, mantenendo l’arresto senza retry. Non recupera il dettaglio del tentativo storico e non autorizza una nuova chiamata distinta. OAT scientifico e consegna restano aperti.


## Diagnostica rilasciata e vincoli della decisione API

PR581 integrata nel merge `3b22ad371c3865c2fbe08002a0c3b80da164c9a7`: ARB poi RQ APPROVED senza rilievi, 57 test research/transport e MkDocs strict PASS, 9/9 check sullo head. Build `5ce1f5a5-a720-4134-8666-21b55f2ecd51` SUCCESS, digest `b237e8ea872d71d60f64c438113943fbc5a60816f2b583a24213e1932cea56fd`. Backend `dsg-pixinsight-pilot-research-diag-v1-20261011` attivo 100% dopo verifica senza traffico: health200, dati privati403 anonimi, configurazione/identità/risorse/segreti conservati. Rollback tecnico alla precedente revisione research-v1; il worker esistente e i byte nativi restano preservati. Questa release non riavvia i tentativi fermati.

L’Owner ha autorizzato la richiesta distinta `1f377a51`, preparata dal portale con gli stessi master, prompt e perimetro. La prima risposta è completa e ha ricevuta minimizzata: `RESEARCH_EXACT_PARENT_REQUIRED`, 10.530 token input e 642 output, totale 11.172. Nessuna decisione validata né prova nativa. Il controllo respinto richiede insieme padre esatto e `checkpointId` nullo per TEST; la ricevuta non conserva gli argomenti, quindi non distingue quale dei due campi fosse errato. Il consumo di questa risposta è noto; quello della precedente b013b0bb resta non accertato. Non attribuire la seconda causa al tentativo storico.

La correzione candidata dello schema rende `parentId` un enum del solo checkpoint selezionato. `checkpointId` ammette soltanto null e le selezioni già verificate e legalmente selezionabili nella fase; alla prima calibrazione può essere soltanto null. Lo schema espone soltanto le azioni correntemente ammesse e toglie le prove quando i limiti della fase le vietano. Le istruzioni chiariscono che il server assegna l’ID del nuovo esperimento e che SELECT usa un ID già verificato, con step nullo. I controlli semantici finali restano obbligatori: lo schema non certifica correttezza scientifica, parametri, assenza di artefatti o accettazione Owner. Nessuna proposta respinta viene modificata e riutilizzata; un nuovo tentativo distinto resta da autorizzare.


## Prima prova SPCC reale e dimensione della ricevuta

PR582 integrata nel merge `a994380310cf330241bd67a68ba5b6a23748a39b`, ARB poi RQ APPROVED senza rilievi, 60 test research/transport e MkDocs strict PASS, 9/9 check head e 10/10 post-merge SUCCESS. Pages pubblicata con run38172485521. Build `eb155676-dd87-46fa-a318-e6dd9ca08f1a` SUCCESS, digest `c55afa83e4efea31eda78042ee42d29d129b53e9d75f4b2f4d2953cc8b5f9b4e`; backend `dsg-pixinsight-pilot-research-bind-v1-20261011` attivo 100% dopo verifica senza traffico, salute e protezione dei dati privati. Configurazione preservata e rollback research-diag-v1 disponibile.

Nuova richiesta distinta `2ffd1ae8` autorizzata dall’Owner con medesimo perimetro. Prima decisione TEST/SPCC validata dal contratto: padre CP000, `checkpointId` null, conoscenza SHA `5b2bc101e9b9a98d34dc24f9527e57985294df4faf510bc0f73d55c34b0daaf2`. Uso noto 10.613 input e 485 output, totale 11.098 token. CP001 è stata eseguita in nuova istanza dedicata su copie; ricevute native/History e tutti i pixel verificati localmente, originali invariati, fit SPCC `NATIVE_FIT_INSPECTABLE`, viste possedute chiuse. La selezione della calibrazione resta una decisione successiva e non è attestata dal solo completamento.

La ricevuta di checkpoint, con misure di RGB/L prima e dopo, occupa 536.433 byte nella codifica canonica. Il limite client di 262.144 byte ha bloccato l’invio prima della richiesta HTTP: backend ancora `NATIVE_STARTED`, nessun nuovo tentativo nativo o API. La correzione candidata usa un limite condiviso finito di 2MiB per il solo `research-checkpoint`; conserva 256KiB per V2, autenticazione, validazione scientifica, hash, original guard e limiti del catalogo. I test HTTP verificano ricevute di dimensione reale, limite esatto, rifiuto oltre limite e conservazione di ruoli/limite V2. Dopo il rilascio il worker deve riverificare e consegnare la stessa ricevuta, senza rieseguire SPCC. Recupero effettivo, decisioni successive e consegna finale ancora da verificare.


## Consuntivo OAT M27

La richiesta distinta `2ffd1ae806a968db8d4240957fc3b900` è stata autorizzata dall'Owner con schema corretto, stessi master e dati OpenAI, `gpt-6-luna`, 16 prove native / 32 richieste e massimo tre alternative per fase. Le decisioni sono prodotte dall'API e applicate dal worker entro il perimetro confermato dal portale. I tentativi b013b0bb e 1f377a51 restano conservati senza reinvio; i loro esiti non descrivono lo stato corrente.

### Recupero della ricevuta SPCC e rilascio PR583

PR [583](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/583), head `e3eddeb44306e1bced2d580b7a9e96bd34322782`, merge `2ecbdfead8880decc05910cb443a4a994f23b901`: ARB poi RQ separate APPROVED, zero finding, 62 test research/transport e MkDocs strict PASS; 15/15 check head e 16/16 post-merge SUCCESS. Pages pubblicata con run38173608664. Build `964a21a6-c157-43ec-91d8-8320fb3f655e` SUCCESS; digest `14be9b31334e57075f5f827ebb5aa4a24f7a1679fb833670dce8260e8a38f713`; backend `dsg-pixinsight-pilot-research-cp-v1-20261011` attivo al 100% dopo health200/protetti403 anonimi e confronto della configurazione. Ambiente, identità, risorse, segreti e byte nativi preservati; rollback research-bind-v1 disponibile.

Il worker è stato aggiornato sotto lock di manutenzione fra cicli, preservando lease, impostazioni, profilo e tentativo CP001. Preflight sul prodotto reale: ricevuta canonica 536.433 byte entro 2MiB, originali invariati, verifica SHA `6771c7db001386232da378186f6af51d1fd6c69a060e54fa55857d6a07fd4f5d`. La stessa ricevuta è stata riverificata e consegnata; nessuna nuova esecuzione SPCC. Il backend ha ripreso da AWAITING_DECISION e l'API ha selezionato CP001.

### Scelte realmente osservate

CP001 conserva SPCC sul RGB lineare con 70 stelle comuni esportate, curve ZWO nominali, QE ideale sostitutiva e L-Pro escluso dai filtri RGB. Fit nativi ispezionabili e riferimento bianco entro gli intervalli esportati sono precondizioni soddisfatte per selezionare il checkpoint; non certificano la risposta strumentale reale, una calibrazione assoluta o l'accettazione scientifica.

In DETAIL sono stati confrontati CP001 senza ulteriore trattamento, CP002 BlurXTerminator correction only e CP003 deconvoluzione moderata (`sharpenL=0,2`, `sharpenRGB=0,1`). Entrambi i candidati hanno lo stesso genitore CP001: nessuna sovrapposizione delle deconvoluzioni. L'API ha conservato il controllo, dichiarando beneficio visivo non convincente sui dettagli deboli e rischio alle alte luci. Le FWHM inferiori dei candidati sono descrittive di popolazioni nuovamente rilevate, non prova di maggiore risoluzione.

| Checkpoint | Campioni esattamente 1, R / G / B | Campioni esattamente 1, L |
|---|---|---|
| CP001 controllo | 0 / 0 / 0 | 0 |
| CP002 correction only | 1.147 / 1.134 / 1.278 | 2.920 |
| CP003 deconvoluzione | 1.165 / 1.170 / 1.304 | 2.895 |

Ogni canale comprende 13.012.272 campioni. Le verifiche non trovano campioni negativi, maggiori di uno o esattamente zero in questi tre checkpoint. La decisione API parla di clipping: il fatto verificato è l'aumento dei campioni al limite superiore e la riduzione del margine nelle alte luci. Il conteggio, senza ispezione locale dei nuclei e dell'operazione interna, non prova da solo il meccanismo della saturazione. Le prove scartate restano nell'archivio e non fanno parte della catena finale.

In NOISE, CP004 applica NoiseXTerminator 0,3 a L e RGB sul controllo CP001. L'API lo ha selezionato dopo confronto comune, descrivendo tessitura lievemente più uniforme senza perdita morfologica evidente nel crop disponibile; non ha ritenuto necessaria una prova più intensa. MRS sul campo completo, quattro livelli, passa da 1,5338e-4 / 1,4858e-4 / 3,7092e-4 a 4,3574e-5 / 4,2340e-5 / 9,3694e-5 per RGB e da 6,9373e-5 a 4,9185e-5 per L. Scala e supporto sono conservati nelle ricevute. Denoise cambia correlazioni e supporto: non dedurre un aumento di SNR da questi rapporti. Sulla ROI L la stima a quattro livelli restituisce sigma=0 e supporto=0 dopo denoise: stima non utilizzabile a quella scala, non assenza di rumore.

Le decisioni successive e la consegna devono essere riconciliate con le ricevute terminali; l'accettazione Owner resta distinta. Le sezioni di rilascio precedenti sono snapshot storici.


### Arresto in COMBINE e correzione della provenienza

L'API ha selezionato CP005, MaskedStretch con target di fondo 0,06, come risultato non lineare più leggibile rispetto al controllo lineare a display identità. Il target è tonale, non un campione di cielo vuoto e non una sottrazione del fondo. La ricevuta registra 130 campioni esattamente zero in R e L, massimi sotto uno: non ignorare il limite nelle successive valutazioni.

La decima decisione è STOP in COMBINE: il modello dichiara assenti i prodotti SPCC perché vede `photometry=null` su CP005. La calibrazione è invece conservata e verificata in CP001, già selezionato. Causa tecnica individuata nella proiezione API: comprende soltanto controllo e fratelli correnti e omette il fit dell'antenato. L'arresto è conservato, non convertito in approvazione scientifica. Consumo noto della richiesta fino allo STOP: 109.205 token input, 5.476 output, 114.681 totali; cinque prove native. Nessuna fusione, saturazione o consegna finale.

La correzione candidata aggiunge `calibrationLineage`: catena esatta del checkpoint selezionato fino a CP000, processi e dominio; checkpoint SPCC, impronta della sua ricevuta e prodotti aggregati originali. Controlla presenza, verifica, assenza di cicli, profilo strumentale e hash del fit prima di prenotare una nuova chiamata. Un fit di un ramo estraneo non diventa un antenato. Non duplica il fit nei checkpoint successivi e non deduce che denoise/stretch/fusione preservino rapporti fotometrici. La validità fotometrica a valle e l'accettazione restano NOT_ESTABLISHED.

Dal portale l'Owner può esaminare il fit dell'antenato e la catena, poi confermare la ripresa della stessa richiesta. GET/POST `research-resume` sono esclusivamente Owner: il worker non può riaprire il ciclo. La conferma vincola stato, policy e nuova evidenza con SHA; ricevuta immutabile e cronologia dell'arresto conservate. La ripresa non invoca OpenAI o PixInsight nell'endpoint: il worker torna alla scelta seguente, che può ancora essere STOP. Stessi parametri, sorgenti, runtime, conoscenza e massimali; non azzera prove, chiamate o selezioni, non riesegue SPCC. Nel caso corrente restano 11 prove e 22 richieste API. Gli stati indeterminati API, prenotazioni pendenti, avvii incerti, richieste annullate e finali consegnati non sono riapribili tramite questo controllo. Pubblicazione e accettazione finale non cambiano.

Il paragrafo precedente descrive lo snapshot prima del rilascio; l’esito successivo è riportato qui sotto. La consegna finale resta aperta.

### Fusione LRGB: prova non promossa e limite operativo

PR [584](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/584), head `97b72aebbb4b791f371ddfbd8ba243767f2242aa`, merge `6a943ab9a9138021ef190a2487c31f10496b3e87`: ARB poi RQ separate APPROVED zero finding; 15/15 check PR e 16/16 post-merge SUCCESS, Pages38176433284 SUCCESS. Build330689a5-d30c-45fe-a431-30fc48e1ace5 SUCCESS, digest72d2d85e4bd1e76f8a5a1df15e6b818121d346b874b89320d40a084b65dfecf3. Backend research-lineage-v1-20261011 attivo100%, configurazione preservata e rollback research-cp-v1 disponibile. Ricevuta canonica di ripresa recuperabile dopo crash prima del CAS; replay già applicato non riapre un successivo STOP.

Owner autenticato nel portale reale. Dopo revisione della provenienza, ripresa della stessa richiesta con 10 API/5 prove invariati e STOP precedente conservato. Undicesima API TEST COMBINE dal genitore esatto CP005; CP006 completato e verificato. Dodicesima API STOP: non promuove CP006, mantiene CP005 e dichiara beneficio non dimostrato sui dettagli deboli, rischio cromatico ai limiti, campo intero/fit stellari appaiati non stabiliti. Il nuovo contesto ha correttamente conservato il fit SPCC ancestrale; questo arresto ha una motivazione diversa dal precedente errore di provenienza.

| Checkpoint | Esattamente 0, R / G / B | Esattamente 1, R / G / B |
|---|---|---|
| CP005 controllo | 131 / 0 / 0 | 0 / 0 / 0 |
| CP006 fusione non promossa | 8.574 / 975 / 0 | 685 / 0 / 1.348 |

Ogni canale ha 13.012.272 campioni; nessun negativo o valore maggiore di uno. L resta invariata: 130 zeri, nessun uno, massimo0,893953681. Il precedente riepilogo di130zeri in R era impreciso: la ricevuta RGB registra131. I campioni al bordo sono un rischio concreto da localizzare; non provano da soli la natura o rilevanza di ogni artefatto, né perdita generalizzata del segnale. La factory usa LRGBCombination con `mL=0.5`, `mc=0.5`, `clipHighlights=true`, `noiseReduction=false`, luminanza L-Pro nel solo canale L. L'abilitazione del clipping è verificata nel codice; la causalità pixel per pixel richiede confronto locale. L'immagine più luminosa non prova aumento di segnale acquisito, SNR o dettaglio fisico.

Il catalogo V1 ammette COMBINE con parametri vuoti e una sola prova. La selezione avanza per fasi; non consente al modello di modificare peso/trasformazione della luminanza o protezione delle alte luci, né tornare allo stretch. L'autonomia attuale raggiunge quindi un limite operativo reale: può rifiutare il risultato ma non esplorare un'alternativa di fusione. Restano10prove/20API nel budget, senza alternative COMBINE eseguibili. Non riaprire il ciclo allo stesso contenuto per forzare SELECT o FINISH.

Per proseguire serve progettare e verificare una famiglia di fusioni alternative: parametri nativi limitati, precondizioni di dominio e scala L/RGB, controllo dello stesso genitore, criteri di rischio alle alte luci e al nero, confronto su più regioni comprendenti nuclei stellari/nebulosità debole/bordi, ed eventuale revisione dello stretch con provenienza esplicita. Queste sono capacità richieste, non implementate o già validate. Ogni alternativa deve rispondere a un'ipotesi concreta; nessuna prescrizione di aumentare saturazione o luminosità senza evidenza. Un pacchetto di conoscenza deve descrivere quando conservarne il controllo o arrestare, oltre a come provarla. Nuove capacità/impronte richiedono un perimetro coerente, senza mutare silenziosamente la policy già approvata.

Consuntivo corrente: 12 API completate con uso noto, 131.118 token input / 6.121 output /137.239totali; sei prove native verificate, originali invariati. Nessuna saturazione o finale consegnato; CP005 è un controllo per revisione, CP006 una prova scartata, non finali LRGB approvati. Nessuna accettazione scientifica Owner. L'archivio terminale del worker non è generato finché il coordinatore non raggiunge FINISH: i tentativi e le ricevute locali restano conservati. I limiti nominali di curve ZWO/QE sostitutiva, fit SPCC e osservazione su anteprime/crop continuano ad applicarsi.
