# PixInsight — coordinatore di prove e scelta dei rami

| Campo | Valore |
|---|---|
| Versione | Candidato `DSG_PIAI_RESEARCH_V1`, 11/10/2026 |
| Stato | Implementato nel branch; SPCC e ramo correction only nativi verificati su copie M27; review, distribuzione e OAT dal portale pendenti |
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

Il candidato è disabilitato fino a verifica del worker: `DSG_PIAI_RESEARCH=LOCAL_WORKER_VERIFIED`, insieme al gate adattivo esistente. Il profilo locale protetto `research.profilePath`/`profileFileSha256` contiene le curve installate e le basi Gaia; `research.backgroundROI` deve coincidere con una regione misurata e con il binding dell'analisi. Niente chiave OpenAI o token nel file del profilo.

Il vecchio contratto V2, i job conclusi e il pacchetto scientifico V1 rimangono distinti. SHO/HOO/OSC, mosaici, BIN2, maschere, starless, MLDenoise e correzioni di gradiente non appartengono a questo primo catalogo autonomo. La guida può citarli ma non li abilita. Non dichiarare l'intera conoscenza operativa di PixInsight disponibile da un catalogo finito.

Prima dell'attivazione: ARB e RQ separate sull'exact HEAD; CI Linux/Windows e controlli del portale; distribuzione coordinata con rollback alla revisione scientifica V1 e al worker precedente; OAT autenticato dal portale con le API reali e verifica dei risultati al 100%. I test sintetici del ciclo fino alla revisione privata e la prova nativa SPCC non sostituiscono questo OAT.
