# BKL-046 — campagna spaziale, semantica statistica e controllo IA

Stato osservato il **13 novembre 2026**. BKL-046 resta **aperta**: sette famiglie scientifiche incomplete, zero chiusure scientifiche. Questo documento registra risultati circoscritti e limiti; non costituisce accettazione Owner, rilascio del portale o trasferimento completo degli archivi.

Per la struttura del file, le query e le regole di aggiornamento vedere il [riferimento tecnico della conoscenza](../developer/pixinsight-study-knowledge-format.md), aggiornato allo snapshot provvisorio H53. Il consuntivo sotto conserva il precedente snapshot H51 e le sue impronte.

## Campagna spaziale congelata

Sono completati 4.794 blocchi nativi. La ricomputazione finale copre tutti i 24 strati, 1.104 regole congelate e 192 confronti appaiati. La verifica delle ricevute di provenienza copre tutti i 4.794 blocchi: 3.735 dell'epoca precedente e 1.059 della successiva; il confronto di appartenenza agli archivi riusa esplicitamente 3.760 verifiche precedenti ed esegue 1.034 confronti nuovi.

I risultati restano condizionati al modello sintetico di acquisizione e agli operatori studiati. Il controllo della provenienza dei byte non dimostra entropia fisica o indipendenza statistica. Le coppie appaiate non sono ulteriori prove indipendenti e non stimano una probabilità congiunta di successo scientifico.

| Confronti di copertura | Coppie | Covarianza completa entro il criterio | Approssimazione diagonale entro il criterio |
| --- | ---: | ---: | ---: |
| Controllo | 96 | 96 | 65 |
| Bilineare a un quarto di pixel | 96 | 96 | 0 |

Questi conteggi descrivono le regole e le simulazioni congelate. Non qualificano automaticamente StarAlignment, DrizzleIntegration, una camera reale o una generica elaborazione ricampionata. Sono conservati anche esiti diagnostici e inconclusivi.

Un errore di accesso al volume durante la sessione 43 è conservato. Il recupero usa il medesimo input del blocco interrotto, senza ridisegno casuale, e i 51 blocchi rimanenti seguono gli indici originali. La ricevuta composita distingue il prefisso completato, il tentativo fallito, il recupero e la coda; non inventa una ricevuta terminale del tentativo fallito.

## Errore emerso sul clipping delle statistiche

La prova iniziale su otto casi Float64 dichiarava 40 confronti con oracoli esatti. **38 coincidono; due falliscono**: con campioni sui limiti di clipping, MAD e medianAbsoluteDeviation restituiscono zero contro un'attesa inclusiva di un quarto. Il test originale resta fallito e immutato.

La guida installata descrive l'esclusione dei campioni inferiori o superiori ai limiti; questa formulazione aveva motivato l'oracolo inclusivo. Gli estratti pertinenti del sorgente PCL installato usano invece limiti stretti nella selezione degli ordini statistici.

È stata quindi congelata una prova nuova, con casi asimmetrici, controlli senza clipping e un controllo senza campioni sui limiti. Tutti i 40 risultati coincidono con il modello a intervallo strettamente interno; 13 distinguono l'alternativa inclusiva. I 16 XISF salvati di ciascuna prova sono stati decodificati indipendentemente: campioni, selezioni e History costruita risultano conservati.

La conclusione riguarda i metodi, i tipi e i casi effettivamente provati in PixInsight 1.9.5 build 1706. Per una selezione inclusiva occorre un calcolo esplicito verificato; non presumere che il range clipping conservi gli estremi. Non è una caratterizzazione fisica del rumore né la qualificazione completa dell'oggetto Image.

Un nuovo gate nominato incorpora la semantica verificata e conserva i due fallimenti iniziali. I launcher e i protocolli precedenti restano storici; nessuna loro ricevuta mancante è trasformata retroattivamente in un successo.

## Proiezioni: distinguere codice storico e attuale

Una prova scalare nativa confronta estratti originali delle implementazioni storica e attuale, con la loro rotazione sferica e un oracolo indipendente basato su vettori tridimensionali. Tre punti interni passano per ciascuna versione. Per un punto esterno al dominio ortografico, il codice storico restituisce un risultato finito, mentre quello attuale lo respinge.

Il controesempio non va attribuito indistintamente ai workflow moderni. La prova non esegue un solver completo, non verifica un FITS reale e non misura accuratezza astrometrica sulla griglia fotografica. Il comportamento al bordo esatto è conservato come diagnostica separata.

Una correzione di provenienza distingue inoltre gli hash del testo prima della scrittura dagli hash dei file salvati: la conversione dei terminatori Windows aveva prodotto identità diverse. I rapporti originali sono conservati e accompagnati dalla riconciliazione dei byte effettivi.

## Controllo nativo RGBL e quattro decisioni OpenAI

È stato preparato e verificato indipendentemente un genitore RGBL ideale, senza rumore campionato, da un campo atteso già esistente. RGB e L condividono la struttura; i guadagni sono potenze di due. Non rappresenta una caratterizzazione di camera, una calibrazione fotometrica o una nuova acquisizione indipendente.

Sul genitore effettivamente salvato sono state effettuate quattro richieste reali OpenAI, in ordine ABBA, con le guide archiviate base e base più indicazioni sui rami. Sono mantenuti input comune, contratto e impostazioni; cambiano le istruzioni della guida. Una sola esecuzione isolata, massimo quattro invii, prenotazione prima di ogni invio, nessun retry automatico.

Tutte e quattro le risposte selezionano il controllo CP000 senza applicare denoise. Il replay indipendente verifica il contratto archiviato e l'endpoint predefinito di conservazione del genitore. Le decisioni operative coincidono nelle due ripetizioni di ciascun ramo e fra i rami.

| Consumo rilevato | Token |
| --- | ---: |
| Input | 27.210 |
| Output | 1.234 |
| Totale | 28.444 |
| Input servito da cache | 13.335 |

Le 14 evidenze remote di esecuzione sono state recuperate per generazione e verificate sui byte. Il costo monetario effettivamente fatturato non è verificato. L'alias del modello non attesta pesi fissi.

È un solo blocco descrittivo su un controllo ideale. Non dimostra beneficio causale della guida, tasso d'errore accettabile, confronto della conoscenza finale o efficacia del denoise. La revisione semantica del linguaggio prevista in cieco resta aperta: le etichette dei rami erano già visibili durante il controllo operativo e non si dichiara una revisione cieca retroattiva.

## Conoscenza e archiviazione

La conoscenza consolidata **provvisoria H51** contiene 4.920 righe di requisito conservate byte per byte e 162 schede di evidenza. Integra risultati, correzioni e limiti; non promuove gli stati scientifici o i 19 criteri Owner. Il registro autorevole preesistente resta distinto e invariato; il publisher non è stato riavviato.

| Artefatto | SHA-256 |
| --- | --- |
| Ricomputazione spaziale finale | `98526929d964a84a2efbed392920c536309431c6fecba3a82639cc6514781809` |
| Verifica provenienza dei 4.794 blocchi | `9eb1e5d1e2f74dd844279204a7cd58e8d55b7eaa6e3159e23b1c905c6838f295` |
| Riconciliazione del test statistico originale fallito | `2043c70da6a2bd5ad35712ebd3d1cbbbafd7039d40d56488c6310b143ba2286e` |
| Nuovi casi statistici e due modelli congelati | `cff5c74c74f14efe26264609456214c089c30996e8c3604b32c77ff7dcf6ae49` |
| Proiezioni scalari native e oracolo vettoriale | `742d74c571d35efeee9982b3fbf3f7228f9f5c357756ae7de0f95b6c178674b3` |
| Genitore RGBL verificato | `f60e9a91124aca2fcfee3326c43c6cf9134f60e1c8e375f38567439fa7037fbd` |
| Quattro decisioni reali e replay del contratto | `b807beb0c21fdd4e10479dbeb86311f9795e0279a5ba9afc48d03717c2e6f3cf` |
| Conoscenza provvisoria H51 | `be3a8dd834b90362eccd72cc413c79c76e0784abffcf2a13d4ec8a3540034687` |

Gli hash identificano evidenze conservate localmente; questa tabella non afferma che i relativi byte siano già pubblicati o recuperabili da GitHub.

La verifica del contenuto storico è ancora in corso su 498.056 oggetti unici, 854.043.191.084 byte. Un percorso aggiornato dell'adapter SpatialLag differisce dalla versione storica attesa; i byte precedenti sono stati ritrovati e verificati nella copia di conservazione. L'audit dei percorsi storici mantiene comunque la propria osservazione originale, con una riconciliazione supplementare separata.

Restano: applicabilità e verifiche scientifiche nel dominio completo, confronto della conoscenza finale, gate Owner, completamento dell'audit storico e del perimetro corrente/virtuale, file di conoscenza finale e trasferimento integrale su GitHub con recupero indipendente dei byte. La percentuale complessiva e le ore residue della milestone non sono calibrate dai conteggi dei blocchi.

Questa pubblicazione è solo documentale: non avvia il portale, non riprende M27, non modifica master o script PixInsight installati e non interviene sui materiali BKL-051.
