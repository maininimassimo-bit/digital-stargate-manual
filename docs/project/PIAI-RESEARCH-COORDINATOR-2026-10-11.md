# PixInsight — coordinatore di prove e scelta dei rami

| Campo | Valore |
|---|---|
| Versione | `DSG_PIAI_RESEARCH_V1`, rilascio tecnico 11/10/2026 |
| Stato | PR579 integrata, backend/worker/portale attivi; perimetro M27 confermato; prima API senza decisione validata, arresto senza prove native; OAT completo e accettazione finale pendenti |
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
