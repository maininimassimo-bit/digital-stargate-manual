# BKL-046 — campagna spaziale, semantica statistica e controllo IA

Stato osservato il **13 novembre 2026**. BKL-046 resta **aperta**: sette famiglie scientifiche incomplete, zero chiusure scientifiche. Questo documento registra risultati circoscritti e limiti; non costituisce accettazione Owner, rilascio del portale o trasferimento completo degli archivi.

Per la struttura del file, le query e le regole di aggiornamento vedere il [riferimento tecnico della conoscenza](../developer/pixinsight-study-knowledge-format.md), aggiornato allo snapshot provvisorio H58. Il consuntivo sotto conserva il precedente snapshot H51 e le sue impronte.

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

L'aggiornamento tecnico H54 conserva 173 schede e documenta il recupero locale della capsula File IO, il contesto operativo dei vecchi gate backend e il perimetro delle condizioni di pubblicazione. Il [riferimento tecnico](../developer/pixinsight-study-knowledge-format.md#riconciliazione-corrente-e-pubblicazione-documentale-preparata) registra inoltre il censimento corrente, la correzione dei falsi assenti dovuti ai separatori dei percorsi, i 1.990 contenuti storici copiati da C a H e le 1.789 citazioni documentali dirette verificate.

H55 aggiunge la riconciliazione di una prova Timer esistente: quattro casi e nove callback, con default `precise=true` diverso dalla guida. Tre osservazioni retrospettive mostrano `count=0` dopo callback già registrate; restano distinte dai 23 controlli congelati originari. Il [riferimento tecnico](../developer/pixinsight-study-knowledge-format.md#timer-ricevuta-esistente-e-osservazioni-retrospettive) conserva condizioni e limiti di quella rilettura.

H57 aggiunge una prova successiva distinta e congelata, eseguita una sola volta in un'istanza nativa vuota: quattro casi, nove callback, 25 controlli con 20 corrispondenze e cinque discrepanze. Conferma il default `precise=true` diverso dalla guida e quattro letture di `count=0` fuori dal callback dopo consegne note. Le transizioni `false,true,false` vengono rilette correttamente; azzeramenti con base zero restano non identificabili. L'istanza è stata chiusa normalmente con codice zero. Questi esiti rimangono supplementi locali, senza modificare lo snapshot autorevole v600 o qualificare l'accuratezza temporale.

L'audit storico e la composizione delle fonti esatte sono conclusi: 498.056 identità e 854.043.191.084 byte unici coperti, mantenendo gli esiti negativi originali. Questa disponibilità locale non chiude lo staging immutabile, il perimetro corrente/finale o il recupero remoto.

È inoltre terminata la pubblicazione documentale v600, con un solo avvio e postverifica indipendente positiva: 239 oggetti aggiornati, altre 4.681 righe invariate, 11.217 artefatti e 19.604 posizioni fisiche preesistenti verificate. H56 separa tutte le 4.920 righe pubblicate dai record locali conservati; 1.623 di questi contengono solo supplementi non pubblicati. La conoscenza registrata resta v1.171 e non viene attestata una v1.172. Il [riferimento tecnico](../developer/pixinsight-study-knowledge-format.md#stato-pubblicato-e-valutazioni-locali) documenta i livelli di autorità e i limiti del lettore.

Restano: applicabilità e verifiche scientifiche nel dominio completo, confronto della conoscenza finale, gate Owner, completamento del perimetro corrente/virtuale finale, file di conoscenza finale e trasferimento integrale su GitHub con recupero indipendente dei byte. L'audit di reperibilità delle identità storiche è già concluso e non viene rimesso in coda. La percentuale complessiva e le ore residue della milestone non sono calibrate dai conteggi dei blocchi.

Questa pubblicazione è solo documentale: non avvia il portale, non riprende M27, non modifica master o script PixInsight installati e non interviene sui materiali BKL-051.

Il rendiconto v40 conserva 4.920 requisiti e 14.521 criteri letterali, con verifica indipendente sulle righe pubblicate v600. La nuova capsula locale della prova Timer ha superato estrazione e replay isolato dei 25 controlli e dei due confronti non identificabili. Il [riferimento tecnico](../developer/pixinsight-study-knowledge-format.md#rendiconto-v40-e-recupero-locale-della-prova-timer) riporta identità, condizioni e limiti. Questi aggiornamenti non chiudono criteri scientifici o di trasferimento remoto.

## Aggiornamento H58: misura PSF nativa e fallimenti conservati

La conoscenza provvisoria H58 conserva 4.920 requisiti e 183 schede, con record pubblicati v600 separati dai supplementi locali. Il nuovo ponte usa 216 ritagli sintetici già esistenti, con pixel Float64 verificati, e 1.728 richieste native di fit circolari.

Il tentativo originale fallisce per condivisione della ricevuta dopo 120 campi e 960 chiamate. Il recupero esegue solo i 96 campi e 768 chiamate rimanenti, con file di avanzamento distinti e lettura della ricevuta finale dopo un marcatore separato. Entrambe le istanze sono chiuse normalmente; l’uscita zero non trasforma il primo script in un successo. I due segmenti restano espliciti e il prefisso non viene ripetuto.

Sono conservati 1.310 profili finiti confrontabili e **418 fit nativi non validi**. Negli isolati, 472 slot sono confrontabili e 104 non validi, su 576 previsti; fra i confrontabili quattro posizioni e 173 flussi totali analitici superano la soglia del 5%. `b0` differisce dall’angolo del rettangolo richiesto in tutti i 1.310 fit validi: non certifica quindi la regione interna usata. Il [riferimento tecnico H58](../developer/pixinsight-study-knowledge-format.md#h58-ponte-nativo-psf-esiti-non-validi-e-recupero) conserva denominatori, impronte e limiti.

Queste misure appaiate su pixel riutilizzati non portano nativamente l’ottimizzatore Python, non sono nuove acquisizioni indipendenti e non chiudono famiglie scientifiche o gate Owner. Conoscenza registrata v1.171 e trasferimento integrale degli archivi restano distinti da questo aggiornamento curato.

## Aggiornamento del 24 novembre 2026 — Primary2048 su VM e verifica dello storico v571

**BKL-046 resta in corso.** Sette famiglie scientifiche, 25 assi e 19 criteri Owner restano aperti. I collaudi descritti di seguito non producono nuove chiusure scientifiche.

### Primary2048 e coordinamento R4

Il banco 00 conserva 64 casi storici. Restano 196 casi nel banco 00 e 260 nel banco 01. La riconciliazione del tentativo storico sui 196 casi è stata riletta confrontando il certificato con l'inventario del registro e verificando i 180 file della capsula precedente alla chiusura. Il tentativo si è fermato prima di eseguire un caso. La ricevuta del rilascio ordinario dei 64 casi appartiene a una prenotazione distinta. L'inventario del PC principale ne identifica percorso e impronta, ma la copia esatta resta da recuperare.

Sulla VM il fascicolo di revisione collega i due piani congelati ai worker candidati per PixInsight build 1719. I collaudi offline coprono custodia del padre originale in un registro R4 isolato, associazione alla finestra, controllo di avvio, osservazione delle risorse e riconciliazione dopo l'uscita. I test della finestra e del trasporto hanno usato testimoni Windows. Restano da qualificare il controllo della console PixInsight, l'integrazione operativa dell'analisi post-uscita e le revisioni indipendenti ARB e RQ del launcher completo.

Il preflight sulla VM ha rilevato 11,69 GiB di RAM disponibile, 13,12 GiB di commit disponibile e 318,77 GiB liberi sul volume di lavoro. Sono misure puntuali da ripetere prima di una prova. Nessuna nuova ammissione Primary2048 è stata richiesta.

| Evidenza archiviata su storage di progetto | SHA-256 |
| --- | --- |
| Fascicolo di revisione Primary2048 | `de0b7823806dbf0fc360710f6cecc97875c490957482b2e6f7237d0ee708e664` |
| Riconciliazione storica del tentativo interrotto | `0664548d0798e2fdf14e912fe20a32f3f7d125d5f69ab36165ecca760d45413c` |
| Verifica offline del passaggio all'analisi post-uscita | `3d730977c5db6629a532531d349594987105bfeb316f1ab1538ff404af1437ae` |

### Verifica retrospettiva della conoscenza v1.146

Il file storico prodotto dall'incremento v571 è stato riletto sullo storage fisico. Misura 1.153.824.341 byte e ha SHA-256 `7b11789d0616b54cb002c506f0bd2c4e4cfb123a0569f8c409a09da67b2e567e`. Sono stati verificati i registri prima e dopo l'incremento. La ricevuta originale v571 resta da recuperare. Il documento trovato con quel nome contiene la transazione successiva v572.

Questa verifica conserva la sequenza storica e non cambia la conoscenza registrata v1.171 descritta sopra. Il file integrale e la verifica del recupero dei byte da GitHub restano da consegnare.

## Rilettura della conoscenza registrata v1.171

Il file registrato con v600 è stato riletto integralmente su DSG-Shared. Sono stati verificati 3.030.957.683 byte, con SHA-256 `65511eaafd15af1ea7c7f07cdd90d7947d622b6d6f88b31f022e9ac2399c4c0d`.

- Tutti gli 802 file del catalogo v1.171 coincidono per lunghezza e SHA-256 con le copie conservate nel mirror. La verifica copre 1.525.423.639 byte. L’impronta del catalogo è `a2a5c042a1158a8254411bb0ef93b4d6a4c67f1c2d5cb7dfa0477f31b8797a3b`.
- I 229 nuovi record incorporati coincidono per nome, impronta del sorgente e contenuto JSON con i file del catalogo contrassegnati per l’inclusione. I 2.483 record ereditati includono 713 record riconducibili ai 708 sorgenti già verificati per v1.146.
- Il rapporto, l’indice e gli script di verifica sono conservati su H: e K:. Le copie dello ZIP hanno SHA-256 `7825c8ff54793b7d9ed111b8d6dfc5f6939ae015e19b857fb2a395fbd240f8e3`.

La rilettura attesta l’integrità e la corrispondenza dei dati nel perimetro descritto. Restano aperte la verifica di pubblicabilità dei materiali incorporati, la consegna integrale con riscaricamento da GitHub e la validazione scientifica delle sette famiglie.

La verifica successiva ha collegato tutti i **2.712 record** ai relativi sorgenti tramite **2.526 impronte distinte**. Oltre ai 713 record già coperti dalla verifica v1.146 e ai 229 nuovi record, sono stati riletti 1.766 sorgenti dei record ereditati nel mirror su H: e quattro originali ABE su J:. Sullo stesso archivio J: sono stati ritrovati e riletti anche i 292 originali v1.146 prima ricostruiti dal contenuto incorporato. Lo ZIP di copertura è verificato su H: e K: con SHA-256 `414677e1f46506cfc2938eb44a54bd0e1e34d135f782fd0745a597180b02146f`. Il confronto puntuale del contenuto JSON incorporato è attestato in questa verifica per i 229 nuovi record.

Il confronto integrale successivo ha riletto e verificato di nuovo le impronte dei sorgenti e ha confrontato tutti i **2.712 contenuti JSON incorporati** con i file sorgenti. I valori corrispondono in tutti i casi, con numeri decimali confrontati senza conversione in virgola mobile. Il rapporto integrale e il verificatore sono conservati nello ZIP con SHA-256 `0317fe6f1aed0d1957aec75a046a6c108df57e600eacc1b8e0d4bad3760f73ee`, riletto su H: e K:.

### Condizioni di consegna delle fonti

- L'archivio sorgente GaiaXPy corrisponde al commit pubblico `349e9a435d81de50b4c09bc4afb14548acc2c9ac`. La rilettura ha verificato tutti i 401 blob e le 60 directory. Il file LICENSE incluso coincide con quello della revisione pubblica. [Licenza GaiaXPy](https://github.com/gaia-dpci/GaiaXPy/blob/349e9a435d81de50b4c09bc4afb14548acc2c9ac/LICENSE)
- I due prodotti Gaia DR3 XP e i rispettivi VOTable coincidono con le quattro impronte storiche. ESA pubblica i dati Gaia sotto CC BY-NC 3.0 IGO e richiede il credito a ESA/Gaia/DPAC. I termini dell'archivio disciplinano gli usi commerciali. [Licenza Gaia](https://www.cosmos.esa.int/web/gaia-users/license) · [Attribuzioni Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Miscellaneous/sec_credit_and_citation_instructions/) · [Termini ESA](https://www.cosmos.esa.int/web/esdc/terms-and-conditions)
- La licenza del repository ufficiale PJSR prevede condizioni di redistribuzione e restrizioni per addestramento, corpora di addestramento e servizi di generazione automatica del codice. L'associazione dei frammenti effettivamente copiati va verificata per versione e file. [Licenza PJSR](https://gitlab.com/pixinsight/PJSR/-/raw/master/LICENSE)
- Quattro intestazioni di record v1.171 contengono locatori assoluti legati a un profilo Windows. Il rapporto registra gli ordinali senza riprodurre i locatori. Il riscontro sulle fonti è archiviato su H: e K: con SHA-256 `cb2df74643109d62bb1897b4ec55016f97f89ce0870eb1b703effce2157c626b`.

La consegna del file integrale al repository pubblico resta aperta. Queste verifiche documentano le fonti e i termini nei rispettivi perimetri.

La scansione del file intero individua profili Windows in 124 record incorporati e in altre sezioni. Un collaudo locale ha sostituito 280.706 componenti di percorso con un alias comune e ha ricostruito lo SHA-256 esatto del file registrato usando il registro di inversione conservato localmente. Il risultato attesta la reversibilità della trasformazione. Restano da verificare gli altri dati riservati e i diritti sui contenuti. L'indice di scansione è archiviato su H: e K: con SHA-256 `c3072f0b3f9e72d96f171aa5da31a49b7c34115d3f34823a5856e6fad9d9b343`.

### Rilettura del prefisso Primary2048

Sono stati riletti tutti i 12 record associati ai 64 casi storici del banco 00. Gli insiemi dei 64 casi completati e dei 196 mai avviati coincidono nei rendiconti originali. Due file omonimi della ricevuta comune sono stati respinti perché difformi dallo SHA-256 registrato. Per chiudere la verifica serve ancora la ricevuta originale della prenotazione `b9941dc6-8c9e-4c83-ad02-941bf4b28d39`. Il rapporto e i test di rifiuto sono archiviati su H: e K:, SHA-256 `fecd6dcbf1cc5385b654eb6197ada03f0198e257b4e2ec4848975dec2a723837`.

### Canali del processo originale e verifica post-uscita

Su DSG-Shared un testimone Python ha riprodotto il blocco del componente precedente saturando entrambi i canali standard. Con la candidata v2 il processo ha scritto 4 MiB per canale ed è uscito con il codice atteso. Sulla stessa identità sono state verificate lunghezze e impronte, senza conservare il contenuto dei canali.

La candidata di analisi post-uscita verifica le due impronte prima e dopo l'analisi e le lega alla stessa identità di processo e prenotazione. I 18 scenari sui due banchi includono due catene con processi testimone Windows e il rifiuto di canali incompleti, di un altro processo o alterati. Sono state ripetute anche le prove della finestra originale e del monitor di risorse. Le soglie del monitor sono rimaste quelle del protocollo. La prova con PixInsight richiede ancora l'integrazione nel launcher, ARB, RQ e l'ammissione R4.

Il pacchetto tecnico è riletto su H: e K: con SHA-256 `f515584cca6220f41e50fc4e05ea41dfb1e31b4c85cf977347d9a9c9a0893c51`. Il risultato riguarda l'affidabilità del launcher e lascia aperta la validazione scientifica delle sette famiglie.

### Replay numerico dei 64 casi storici

Il replay offline su DSG-Shared ha riprodotto byte per byte tutti i 64 rapporti di caso del banco 00. Nel riepilogo sono stati confrontati otto campi, inclusi piano, impronte native e riconciliazione. Sono stati verificati 2.912 endpoint, con 35.913.728 valori stimati, 786.432 senza supporto e zero divergenze del supporto. Restano esclusi dal replay i 196 casi del banco 00 mai avviati.

L'archivio integrale contiene 1.811 file di output verificati con SHA-256, più indice e rapporto. È conservato su H: e sullo storage K: tramite O:. SHA-256 dell'archivio `ea87865d283b50e42f02deebc1d0d0e751638390efd39d1cc115f0aa91f74fe6`. Il riscontro compatto è disponibile anche direttamente su K:, SHA-256 `a3060d03fa221b5f0849972652bafff073aaad9fdd6cc37a2b05517891b7efa6`.

La riproduzione riguarda i dati storici. Restano aperti la verifica della ricevuta comune originale, la prova nativa sulla build 1719 e la validazione scientifica.

### Verifica delle evidenze prima del rilascio R4

La candidata collega l'uscita del padre originale alla prenotazione e all'impronta attesa del piano congelato. Prima dell'unica richiesta di rilascio rilegge l'attestazione post-uscita, il rapporto numerico, il marcatore di completamento e le ricevute native. Dopo la conferma R4 verifica la ricevuta di rilascio e la sua impronta.

Il collaudo ha usato il coordinatore e l'adattatore con le impronte installate, con l'adattatore puntato a un registro isolato e dati scientifici simulati. Su 16 scenari, due rilasci sono stati confermati tramite rilettura, 12 prenotazioni sono rimaste trattenute per evidenze mancanti o difformi, uscita del padre non zero o piano errato, e in due casi la perdita simulata della conferma dopo la scrittura della ricevuta ha impedito di dichiarare il successo o ritentare. Le prove hanno verificato l'integrità dei record originali e l'identità dei processi testimone Windows.

Il pacchetto è riletto su H: e K: con SHA-256 `8d316234879f04b83faf0f0c43a6b26911429ad4e90e684867f9ef952b841e08`. Restano l'integrazione nel launcher completo, ARB, RQ e l'ammissione per la prova su PixInsight.

### Collegamento dell'analisi post-uscita al controllo R4

Il componente del padre confronta le impronte dei piani e dei worker con il descrittore congelato, verifica la corrispondenza dei percorsi VM e rilegge il piano prima dell'analisi. La verifica su DSG-Shared ha coperto tutti i 456 casi residui, 196 del banco 00 e 260 del banco 01. Prima di avviare l'analisi il padre verifica l'identità nativa e la prenotazione e registra un tentativo esclusivo. Il rapporto dell'analisi viene passato al controllo di rilascio soltanto tramite l'attestazione del padre originale.

Dieci scenari sui due banchi hanno verificato il collegamento con processi testimone Windows e output scientifici simulati. Ricevute modificate, impronte non corrispondenti e perdita della prenotazione hanno impedito di produrre l'attestazione finale. L'analisi incompleta ha conservato il tentativo senza consentire una ripetizione.

Il riscontro è conservato su H: e K:, SHA-256 `ed9fa55c4289df532ea6e1cff12ab1996958765f2675e47fe7313d7a4d6f9cbd`. Restano aperte l'integrazione dell'avvio, del comando e della chiusura nella stessa catena, le revisioni indipendenti e la prova nativa.

### Chiusura ordinaria della finestra originale

La candidata verifica la ricevuta del worker, il marcatore terminale e il riscontro della console legato alla prenotazione prima della richiesta di chiusura. Verifica anche che PID, ora di creazione, sessione e finestra corrispondano a quelli osservati all'invio del comando. Dopo la revisione della finestra, registra la richiesta una sola volta e ricontrolla le evidenze prima di inviare il messaggio Windows. L'analisi riceve le impronte delle ricevute solo dopo l'uscita con codice zero sullo stesso handle.

Su DSG-Shared sono passati 16 scenari. Per ciascun banco una finestra testimone reale è stata chiusa con un solo messaggio e l'uscita è stata osservata. Negli altri 14 scenari il messaggio non è stato inviato per identità difforme, evidenza mancante o cambiata, revisione respinta, richiesta già registrata o condizione di trattenimento. Console scientifica e revisione sono state simulate. La perdita di stabilità del testo dopo la registrazione ha mantenuto il tentativo e bloccato un secondo invio.

Il pacchetto è verificato su H: e K:, SHA-256 `46fb2be819981b2b0e319b2b5760bcac466db8d61e2ac4393189a535142d2c79`. Restano l'integrazione dell'avvio e dell'invio del comando, la revisione del launcher completo e la qualifica nativa del controllo della console e della finestra PixInsight.

### Sincronizzazione dell'avvio e invio del comando

Il controllo iniziale dello script poteva precedere la pubblicazione del PID da parte del padre. La candidata attende ora un marcatore pubblicato con rinomina atomica su Windows dopo la rilettura di `native-process.json`. Il marcatore associa banco, operazione e prenotazione alle impronte del binding e del processo. L'attesa candidata ha un limite di 10 secondi e interrompe l'avvio in caso di stop, prova incompleta o difforme. La revisione del dispatcher conserva i due piani, i due worker e i percorsi operativi.

Sedici scenari hanno verificato l'attesa sui due banchi con pubblicazione reale su Windows e runtime PJSR simulato. Altri otto scenari hanno verificato il collegamento al comando usando il renderer reale e il trasporto UI simulato. Il comando simulato è stato bloccato dopo modifiche del marcatore, cambi della finestra o perdita delle riserve di risorse. Restano la composizione finale del launcher e il collaudo nell'app sotto ammissione.

Descrittore dispatcher SHA-256 `d47fa874f474c67cfea9097cb1f42d7d882959303815d1eea1863f808f877b43`. Pacchetto riletto su H: e K: con SHA-256 `677057a7c7101da0818b17bcc2320d6f19d5514ffef0c649bd83e6e0ba1c25c1`.

### Sequenza del padre originale sulla VM

La candidata riunisce nello stesso padre R4 la preparazione dell'avvio, l'avvio del processo vincolato, il monitor delle risorse, l'invio del comando, l'attesa delle evidenze terminali e la chiusura con passaggio all'analisi. Il riscontro terminale della console deve arrivare prima della lettura delle impronte delle ricevute. L'uscita dal tempo assegnato interrompe la sequenza senza avanzare alla chiusura.

Diciotto scenari hanno collaudato la sequenza con processi Windows testimone e con autorità e fasi native simulate. Le due sequenze complete hanno passato al componente successivo il processo originale. Le altre si sono fermate per autorizzazione assente o revocata, byte di avvio mutati, rifiuto dell'avvio, perdita della prenotazione, finestra difforme o riscontro terminale errato o mancante.

Il pacchetto con le dipendenze è riletto su H: e K: con SHA-256 `f93ce3a2467ce81bbfea78c7186d48340497dc111189108f94856cfe6bfad114`. Il padre candidato richiede ancora il collegamento alle autorità operative per avvio e revisioni UI, la verifica del launcher integrato da parte di ARB e RQ e la qualifica nativa ammessa da R4.

### Soggetto Primary2048 e verifica delle autorizzazioni

Il soggetto candidato fissa le impronte di 40 componenti su DSG-Shared. Il verificatore Ed25519 lega ARB e RQ allo stesso soggetto e il verbale RQ al verbale ARB approvato. Il padre rilegge le impronte dei file prima di accettare l'autorizzazione all'avvio. Le decisioni di avvio e interazione con la finestra sono legate alla prenotazione, all'impronta della richiesta e al suo termine di validità.

Con chiavi effimere di collaudo sono state verificate le sei risposte richiamate dal padre, inclusa la rilettura del permesso di avvio e il rifiuto del riuso di un comando. Dieci casi avversi hanno coperto una chiave o un ruolo errato, verbali mancanti o disallineati, soggetto difforme, prenotazione diversa, risposta riutilizzata e scadenza. L'operatore esterno, l'ancora di fiducia operativa e le attestazioni effettive richiedono ancora qualificazione.

Soggetto SHA-256 `a09d886342b325d921f32c71b4392fc00b2e4549bd2502ed703fe51e8ecdfd0f`. Pacchetto riletto su H: e K: con SHA-256 `97492bc0fa0871b4a78b9da93a7175848db282922bbab4909851013353e3d63a`.

### Operatore R4 e padre originale

L'operatore candidato verifica i verbali prima di aprire la prenotazione e li rilegge prima di autorizzare la prosecuzione del padre. Mantiene il processo originale e accetta una sola attestazione finale con uscita a zero. Passa la richiesta di rilascio al controllo delle evidenze post-uscita, al massimo una volta.

Venti scenari sui due banchi hanno usato R4 e il suo adattatore su un registro isolato, con chiavi effimere ed evidenze scientifiche simulate. In quattro casi il rifiuto del preflight o l'assenza di ARB ha impedito di prenotare. In 12 casi la prenotazione è rimasta trattenuta dopo l'interruzione. Due rilasci sono stati confermati e due hanno scritto la ricevuta prima di una perdita simulata della risposta, senza ripetizione della richiesta.

Il soggetto candidato include ora 41 componenti con SHA-256 del descrittore `5fb282723a58e689051ab1942d6f90bde550b8bab48d555a045a0ff64c76733e`. Pacchetto verificato su H: e K:, SHA-256 `d595a71342cb78ef5bf30400b7a05b5dfb4d22b020ee91efeea4b30389566d21`. Il collegamento al preflight e alla configurazione operativa, l'ancora di fiducia autenticata, le revisioni sul nuovo soggetto e l'ammissione nativa restano aperti.

### Preflight del candidato operatore su DSG-Shared

Il collegamento candidato ha riletto il soggetto, il dispatcher, i due piani e i 456 casi rilocati. Ha verificato il coordinatore R4 installato e osservato memoria, storage, inventario processi e publisher. La rilettura dell'archivio storico ha riconosciuto l'arresto eccezionale del tentativo da 196 casi con zero nuovi casi. La ricevuta di rilascio ordinario dei 64 casi storici resta assente dalle radici controllate.

Il preflight reale ha bloccato entrambi i banchi prima della prenotazione. Mancano i verbali ARB/RQ del soggetto, la qualifica nativa del canale console e la ricevuta storica dei 64 casi. Le prove simulate hanno inoltre verificato il rifiuto di inventario incompleto, prenotazione attiva, PixInsight già presente, publisher incerto, riserve insufficienti, storia incompleta o piano difforme.

Il riscontro e il componente candidato sono archiviati su H: e K: con SHA-256 `ce766992457469b0d5ee842905e4349b0bb988ae40eecbae79087c7769b423b2`. Restano aperti il riscontro delle autorità operative e la prova nativa.

### Audit dei 64 casi storici Primary2048

Un verificatore separato dal codice di replay ha riletto l'archivio dei 64 casi del banco 00 (build 1706). Ha riconciliato 560 flussi per endpoint e 36.700.160 stati per campo con le impronte di lotto e i conteggi del rapporto. Si contano 35.913.728 stime, 786.432 stati con selettore non supportato e zero discrepanze di supporto. Fra le stime, 580 superano il 5% di errore relativo. Tutte rientrano nella tolleranza assoluta di 10⁻⁶. Per ciascuno dei 580 superamenti, il verificatore ha ricostruito gli errori dichiarati a partire dalle frazioni esatte conservate.

Il controllo aggiunge evidenza all'asse `NOISE_FLUX/3`, che resta aperto. Restano da dimostrare la validità sul disegno completo, il comportamento del rumore correlato dopo ricampionamento e l'incertezza sui casi indipendenti. Il risultato riguarda la rilettura di dati storici e registra zero avvii nativi e zero chiusure scientifiche. L'audit, il rapporto e l'addendum di tracciabilità sono archiviati su H: e K: con SHA-256 `8bceb1db05c167d3068b1848b873de834dc4eccde1b0859616bd443b1fd24f06`.

#### Diagnosi dei superamenti relativi

I 580 superamenti del 5% si concentrano nell'endpoint `PAIR_DIFFERENCE` (580 su 9.175.040 stime nel prefisso storico, distribuiti in 63 dei 64 casi). Nei testimoni il valore assoluto del riferimento originale arriva a 1,67 × 10⁻⁶ e l'errore assoluto massimo a 1,03 × 10⁻⁷. Il confronto usa le frazioni esatte archiviate.

Con lo stesso denominatore originale, la sola componente di aritmetica nativa supera il 5% in 420 testimoni, la sola componente di lettura in 8, entrambe in 98. Nei restanti 54 ciascuna componente rispetta la soglia e l'errore totale la supera. Usando come riferimento il valore previsto dopo la lettura, l'aritmetica supera il 5% in 517 dei 580 testimoni. Quest'ultimo confronto riguarda solo i testimoni già selezionati dal criterio originale.

Lo script, il rapporto e i 580 riscontri sono archiviati su H: e K: con SHA-256 `75c462396dc046164b0bd2e7caa2f2b511bd72408874c4273a0e759401415de0`. Per la successiva verifica sul disegno completo restano applicabili entrambe le soglie congelate. I conteggi descrivono il prefisso storico. L'asse `NOISE_FLUX/3` resta aperto.

### Perimetro di riconciliazione per le prove residue Primary2048

Il riscontro derivato dai piani congelati e dal modello elenca, per ciascun caso, tutti gli endpoint logici, l'intervallo dei campi e la disponibilità del selettore. Ha confrontato il prefisso storico con i rapporti dei 64 casi e ha verificato che il piano dei 196 casi coincida con la parte residua esatta del banco 00.

| Entrata | Build prevista o osservata | Casi | Posizioni campo-endpoint con selettore | Senza selettore |
| --- | ---: | ---: | ---: | ---: |
| Prefisso storico del banco 00 | 1706 | 64 | 35.913.728 | 786.432 |
| Casi residui del banco 00 | 1719 | 196 | 136.577.024 | 17.563.648 |
| Banco 01 | 1719 | 260 | 172.490.752 | 18.350.080 |

I conteggi dei casi residui sono attese di copertura. In sede di verifica si applicano le soglie congelate di 10⁻⁶ assoluto e del 5% relativo con riferimento zero indefinito. Le mancate stime per selettore assente, le discrepanze di supporto e le misure sospese per esito dell'audit grezzo richiedono conteggi distinti. Il prefisso 1706 resta identificabile nel confronto: una stima aggregata fra build richiede una verifica di equivalenza. Il modello dichiara che endpoint e configurazioni logiche condividono i campi di ingresso, quindi il numero di posizioni non è la numerosità di un campione indipendente.

Il pacchetto con generatore, mappa caso-endpoint e sei verifiche di rifiuto è archiviato su H: e K: con SHA-256 `8d80756e647565f4863a2bb9817a6ac46bfc10390959fc66ec5caae194a6e56a`. La riconciliazione futura richiederà i risultati nativi effettivi e le relative ricevute.

#### Verifica dei risultati salvati

Il verificatore offline usa la mappa congelata per rileggere il rapporto, i file dei singoli casi, gli stati per campo e i testimoni frazionari. Verifica le impronte, l'ordine dei casi e degli endpoint e la conservazione dei conteggi. Se mancano casi, l'esito completo viene rifiutato. Un esito esplicitamente parziale deve riportare tutti gli identificativi attesi che mancano. Un audit grezzo fallito ammette solo stati sospesi o privi di selettore, secondo il piano.

Il prefisso dei 64 casi e i 580 testimoni storici sono stati riconciliati con la stessa procedura. Dieci scenari isolati coprono anche superamenti contemporanei delle due soglie, discrepanze di supporto e un testimone alterato. Il pacchetto su H: e K: ha SHA-256 `e9a458bfb5f63d4a0c2768de39f9a2918355277358b74c7e57c4bae954a38b48`. La provenienza del processo nativo e le ricevute R4 richiedono la verifica del coordinatore. Le prove residue attendono l'ammissione.

### Inventario del canale console su DSG-Shared

In una finestra testimone WinForms identificata tramite processo originale, UI Automation ha visitato quattro elementi senza esporre pattern utilizzabili. Win32 ha individuato due controlli Edit, uno a sola lettura, e un pulsante. Due inventari sono coincisi, un PID diverso è stato respinto e il processo testimone si è chiuso con codice 0. L'inventario ha letto solo metadati dei controlli.

Il pacchetto archiviato su H: e K: ha SHA-256 `57a63161229a745882ab7614a0e37527ccf5adb2203b1c6260a8428dcd09fd75`. La qualifica del provider PixInsight resta aperta. La procedura proposta prevede un incarico dedicato sotto R4 per identificare la console della build 1719 e verificare un solo marcatore innocuo nell'istanza originale. Nessun avvio PixInsight o richiesta di ammissione in questo collaudo.

#### Contratto di qualifica dedicato

La candidata `BKL046_PRIMARY2048_CONSOLE_QUALIFICATION_DSG_SHARED_1719_001` separa la qualifica del provider dalle prove dei due banchi. Il contratto verifica che revisione, prenotazione R4, processo, finestra, unico marcatore e ricevuta di rilascio appartengano alla stessa operazione. Verifica anche l'ordine degli eventi e richiede zero invii di lavoro scientifico e zero letture di dati scientifici.

Un riscontro simulato coerente è stato accettato e dodici alterazioni sono state respinte, incluse operazione di banco, finestra diversa, doppio invio e rilascio anticipato. Il pacchetto su H: e K: ha SHA-256 `5eb5b11ab71cd0aa7248869f2dc7a3c392ad79afe6865ea1ab7dd43468826f73`. Il verificatore controlla la coerenza del fascicolo offline. Restano da collegare il launcher e le autorità reali e da ottenere l'ammissione per la prova dedicata. Nessun processo PixInsight è stato avviato.

#### Custodia R4 del parent di qualifica

Su DSG-Shared il coordinatore R4 è stato collaudato con processi reali e un registro isolato per l'operazione di qualifica. L'adattatore ha atteso la prenotazione prima di creare il parent. Il parent ha riletto i record di acquisizione e identità e il rilascio è stato confermato dopo l'uscita zero. In due scenari separati, un identificativo di operazione scientifica e un'impronta alterata hanno lasciato la prenotazione di prova trattenuta. Il registro canonico è risultato identico prima e dopo il collaudo.

Il pacchetto su H: e K: ha SHA-256 `28ca63486f5ced6e562a436c6d5a89d564e0acb43452e01b90b8addd7ee06840`. Il parent collaudato è un testimone. Il collegamento alla vera istanza PixInsight e le approvazioni della prova nativa restano aperti.

#### Autorizzazioni e sequenza di qualifica

Il componente candidato verifica firme distinte per ARB, RQ, operatore e interfaccia e richiede quattro autorizzazioni legate al singolo tentativo. L'avvio segue l'ammissione, l'invio segue l'identificazione del controllo e la chiusura segue la rilettura del marcatore. Le autorizzazioni consumate sono registrate in esclusiva. Un esito ambiguo interrompe la sequenza e respinge una seconda esecuzione nella stessa cartella di tentativo.

Undici scenari con chiavi temporanee hanno verificato la sequenza e i punti di arresto. Le risposte R4 e della console erano simulate in questo collaudo. Il pacchetto su H: e K: ha SHA-256 `f2151d2fcb7c0e9df5556b84f8acffbfa64c89887a6040ede8e42de923c5dd82`. Restano aperti il collegamento della sequenza al parent R4 e al provider nativo e la verifica delle autorità operative autentiche.

#### Integrazione della sequenza firmata con R4

In un registro isolato, la sequenza firmata ha ottenuto una prenotazione dal vero coordinatore R4, legato il parent originale e riletto la ricevuta di rilascio nel caso riuscito. Nei tre casi avversi (autorizzazione di avvio assente, risposta ambigua al marcatore, impronta del record originale alterata) il registro ha conservato la prenotazione senza scrivere una ricevuta di rilascio. Il tentativo duplicato è stato respinto in tutti e quattro i casi. Il confronto del registro canonico prima e dopo è risultato identico.

Il pacchetto su H: e K: ha SHA-256 `9c930b174fddffb28e9410239b48ae718b0895aa67fd2e912c9086105f00fb9c`. Il custode e il parent testimone erano processi reali. Il provider della console era simulato e le firme erano di collaudo. Restano aperti il collegamento al provider effettivo su build 1719, le revisioni autentiche e l'ammissione della prova dedicata.

#### Collaudo integrato con finestra testimone

Il parent testimone, creato dopo la prenotazione R4, ha avviato una finestra WinForms reale nella VM. Dopo le autorizzazioni firmate con chiavi di collaudo, il trasporto ha inviato una sola riga inerte al controllo Edit del processo originale. Nel caso riuscito ha riletto la riga, chiuso la stessa finestra, osservato uscita zero e ottenuto la ricevuta R4. Nel caso con conferma omessa, la sequenza si è arrestata dopo l'invio e ha conservato la prenotazione. Il nuovo tentativo è stato respinto in entrambi i casi. Il registro canonico è risultato identico prima e dopo.

Il pacchetto archiviato su H: e K: ha SHA-256 `04a1b874877a0b58c6c9ba2717745026c2e22ef615de8e86964bb23152537332`. La finestra testimone ha registrato il testo senza eseguirlo. Restano da identificare e verificare i controlli effettivi di PixInsight 1719 e da ottenere le approvazioni indipendenti e l'ammissione della prova dedicata.

#### Marcatore PJSR e risposta attesa

Il sorgente candidato contiene solo il controllo di build 1719, assenza di immagini e richiesta di interruzione, la stampa di un marcatore e il flush della console. Il marcatore deriva dall'operazione, dalla prenotazione, dal soggetto revisionato, dal PID e dall'ora di creazione del processo. Il verificatore richiede la stessa finestra, il transcript precedente integro e l'eco del comando e del percorso prima del marcatore unico. L'eco è modellata sul transcript nativo storico della build 1706 e attende verifica su 1719.

Quattro contesti JavaScript isolati e nove casi di rifiuto sono stati collaudati offline. Il pacchetto su H: e K: ha SHA-256 `009d405267acebeac516c6009e07630160284e0d7f7979aa3371305ed6098bda`. L'esecuzione PJSR effettiva e la selezione del controllo Qt restano da verificare con la distinta qualifica ammessa da R4.

#### Legame firmato tra operatore e parent

La sequenza Node e il provider Python candidato usano gli stessi campi firmati per invio e chiusura: operazione, tentativo, prenotazione, PID e ora di creazione, HWND, sessione, impronta del controllo, del transcript e dello script. Prima dell'azione il parent può rileggere la ricevuta consumata e verificare nuovamente la firma rispetto al soggetto e all'ancora fissati. La chiusura è legata anche all'impronta della risposta.

Il collaudo ha verificato in Python due autorizzazioni Node con chiavi di prova e respinto modifiche di finestra, sessione e script, un riuso e una diversa impronta del verificatore. La sequenza ha superato gli undici scenari Node e il provider candidato sette verifiche isolate. L'archivio su H: e K: ha SHA-256 `9bde5824c7e98fddaccecffe5c5ac773a6a7e117464705567881281ae34177f`. Le prove hanno lasciato aperte l'integrazione operativa del parent, le revisioni autentiche e l'ammissione R4.

#### Parent candidato per la prova nativa

Il punto d'ingresso candidato verifica le impronte R4 e l'identità del parent prima di attivare il provider. Il parent ricontrolla i record di acquisizione e identità durante le attese e prima delle azioni. Pubblica evidenze distinte per avvio, selezione e completamento. La chiusura richiede la risposta al marcatore e una decisione firmata che attesti finestra, applicazione inattiva, nessuna immagine o documento in sospeso e nessuna finestra di dialogo.

Il collaudo offline ha verificato la sequenza completa e tre arresti, per avvio rifiutato, marcatore incerto o uscita nonzero. Il controllo della custodia ha inoltre respinto un record originale alterato. L'archivio verificato su H: e K: ha SHA-256 `e4a62fb42be790923a9deb17ec1b3e8f3474c343fd631990ab3a32e0f882ba3b`. Per la prova effettiva rimangono il collegamento operativo dell'operatore, le revisioni e l'ammissione del coordinatore.

#### Soggetto candidato della prova console

L'operatore candidato collega la sequenza firmata all'adattatore R4 e al parent. Verifica il soggetto, i componenti installati e i record di custodia. Prima del rilascio richiede l'esito originale e l'inventario Windows, poi rilegge la ricevuta R4. Quattro scenari isolati verificano il percorso riuscito, la presenza di PixInsight prima della prenotazione, la modifica del record attivo e una ricevuta di rilascio con operazione diversa.

Il soggetto per la revisione contiene 24 componenti con SHA-256 `19cd2fc54ae32e0aeb822270b1836a45bfb0a4e808be25948284b552df006d0e`. Il pacchetto su H: e K: ha SHA-256 `f2583806c12adac1bd6f9bc6f0eef535bd5b939aaf6a62cb60be38d62a670c49`. Restano da acquisire le revisioni autentiche per questo soggetto e l'ancora di fiducia operativa. Non è stata richiesta l'ammissione canonica e PixInsight non è stato avviato.

### Covarianza esatta tra selettori adiacenti Primary2048

Il riscontro offline ricostruisce i coefficienti dei due pixel dagli endpoint `PAIR_MEAN` e `PAIR_DIFFERENCE` e verifica che il primo selettore coincida con `PIXEL`. Con le varianze di ingresso congelate, ha riconciliato tutte le 2.632 varianze marginali supportate, lasciato indisponibili 280 endpoint e calcolato 728 covarianze di coppia. La covarianza è positiva in 616 coppie e zero in 112. L'ipotesi di indipendenza può sovrastimare la varianza della differenza di un fattore 37,01 e ridurre la varianza stimata della media al 50,68% di quella calcolata nel modello.

I 580 testimoni di superamento relativo del prefisso storico interessano 133 endpoint. Nel modello congelato, 526 testimoni sono associati a coppie con covarianza positiva e 54 a coppie con covarianza zero. Il confronto seleziona soltanto i superamenti storici. Non stima frequenze di popolazione o causalità. L'archivio verificato su H: e K: ha SHA-256 `5825bcc266eddf67c8897ef91f32a0608c3ce9197e933f4fa1802aee8c38c8fd`. Resta aperta la verifica nativa e indipendente dell'asse `NOISE_FLUX/3`.

#### Confronto con le uscite PixInsight storiche

Nei 64 casi salvati della build 1706, media e differenza di ciascuna delle 140 coppie disponibili risultano stimate sugli stessi 65.536 campi. Dai momenti centrati si ricava la covarianza finita come varianza della media meno un quarto della varianza della differenza. Il confronto usa lo stesso campo per sorgente originale, lettura float32 prevista e uscita PixInsight.

Normalizzando per la media delle due varianze condizionali dei pixel, lo scostamento assoluto massimo tra la covarianza dell'uscita e quella della sorgente è 2,29 × 10⁻⁷. Tra la sorgente finita e il valore teorico del modello, il massimo alla stessa scala è 0,00739. Sono scostamenti descrittivi del prefisso storico. Il conteggio di 9.175.040 campi per coppia aggregati include osservazioni condivise tra endpoint e non è una numerosità indipendente. La baseline non estende il risultato alla build 1719 e non chiude l'asse `NOISE_FLUX/3`.

Riproduzione verificata dalla copia H: e copia K: con SHA-256 `a2c16ee68e4f6d64ad863bf145ab863272ee359f506598523fd129b0b2413b77`.

Una verifica diretta dei piani float32 storici ha confermato esattamente la ricostruzione dei momenti per tre coppie. La scelta si basa sul modello congelato: una coppia a covarianza teorica nulla, la coppia mediana superiore e quella con massimo valore positivo normalizzato nel prefisso disponibile. Per ciascuna sono stati riletti i piani di integrazione e di peso fissati per impronta, verificati 65.536 campi con pesi positivi e calcolati i prodotti incrociati dai pixel. Il calcolo è riproducibile dalla copia H:. L'archivio su H: e K: ha SHA-256 `5a7831e390ad229ba998e00171b705b823270f62313d177fb5492d0c5a075a81`. Il controllo verifica tre ricostruzioni storiche e lascia aperta la qualifica sulla build 1719.

L'estensione ha verificato tutte le 140 coppie del prefisso storico. Ha riletto 240 piani di integrazione e peso con le impronte originali, ricalcolato i prodotti incrociati per tutti i 65.536 campi di ciascuna coppia e confermato esattamente le 140 covarianze. I tre controlli iniziali coincidono anche con il secondo calcolo. L'archivio verificato su H: e K: ha SHA-256 `e7c35454f420d1f46be0e17cc806104db30953f9971c9fcd1c6caf3046f4df0e`. Il riscontro copre le coppie disponibili della build 1706. Restano la prova su 1719 e la verifica scientifica di popolazione.

### Prerequisiti per l'inferenza sulla covarianza

La verifica di provenienza conferma due intervalli disgiunti di 65.536 campi e nessuna impronta sorgente condivisa tra i banchi, anche nei blocchi 512 di origine. Per prodotto, le 56 referenze logiche puntano a 52 file distinti, con quattro riusi entro banco. La disgiunzione degli identificativi e dei byte non attesta l'indipendenza statistica.

Il certificato congelato per 2.632 endpoint richiede entrambi i banchi per il proprio limite simultaneo conservativo. Applicando il limite ideale ai due momenti noti di media e differenza e usando i valori teorici come osservazioni ipotetiche, il semintervallo della covarianza è `40/1599` della media delle due varianze dei pixel. In questa proiezione, 580 delle 728 coppie escluderebbero zero. Il calcolo serve a valutare la sensibilità del disegno prima della prova. Restano da dimostrare le ipotesi statistiche, la qualifica numerica della catena nativa e la confrontabilità delle build. Archivio verificato su H: e K: SHA-256 `764c174bed4a2934fc4eb7f3425bce51413a6e8e38cf6573860169f772f86a05`.

La rilettura dei 32 blocchi di ingresso riconcilia **33.554.432 parole primarie** e **262.224 parole di raffinamento** con le impronte del verbale di cattura, gli intervalli di byte e il relativo conteggio delle code. Tutti i blocchi decodificati coincidono con le impronte archiviate. La verifica collega ciascuna delle 896 registrazioni logiche 512 al relativo blocco decodificato e controlla tutti gli 896 collegamenti tra le sorgenti 512 e il reblocking 2048. Il pacchetto verificato su H: e K: ha SHA-256 `9f31db6348ebb13e9b2ebe75f3cdd88fd68cfcc01cec7455ef8dda9b97f892e9`. I file documentano la provenienza e la partizione degli input. L'ipotesi uniforme indipendente rimane quella dichiarata dal protocollo e nessuna nuova acquisizione o elaborazione nativa è stata effettuata.

Il limite di costruzione della sorgente si riconcilia per tutti i 2.632 endpoint supportati. Per i 548 endpoint storici osservati, il calcolo condizionale somma il limite di sorgente al termine RMS dell'errore misurato sullo stesso campo. Usa radici razionali con arrotondamento verso l'esterno e la disuguaglianza triangolare per delimitare il secondo momento ideale. I 548 intervalli diagnostici rimangono dentro la finestra congelata `[779/800,819/800]`. Il maggiore termine RMS normalizzato è 4,33 × 10⁻⁵.

Il prefisso conserva un solo banco per endpoint e non soddisfa il certificato simultaneo dell'intera famiglia. Il risultato condizionale richiede ancora la qualifica del modello delle parole, della conversione effettiva e della catena 1719. Non costituisce validazione di popolazione. Codice e riscontro riprodotti dalla copia H: e verificati su K:, SHA-256 `19d46e08da5be5122d8c14cdbf34c66cb6c9b571b16a5ef8f9f4755959e35e9d`.

#### Riconciliazione prevista dei due banchi

La mappa congelata e il prefisso storico verificato identificano 548 endpoint supportati per cui il piano unirebbe il primo banco in build 1706 e il secondo in 1719. Anche con i campi completi, il verificatore sospende l'aggregazione di queste misure in assenza di equivalenza tra build. I restanti 2.084 endpoint supportati hanno entrambi i banchi previsti in 1719 e richiedono comunque le qualifiche scientifiche. I 280 endpoint privi di selettore restano indisponibili.

Il collaudo offline copre sette scenari e distingue banco mancante, supporto incompleto, build o caso difforme e assenza di selettore. L'archivio su H: e K: ha SHA-256 `4b7dfdb8227dd07a57f5cc5a949cc9135ec567d699605bffbc01b08cfa433233`. La verifica non avvia prove native e non cambia le soglie.

Il piano candidato di confronto 1706/1719 lega i **64 casi storici** ai 548 endpoint a build mista, alle quattro esposizioni e alle impronte dei piani di integrazione e peso. I piani di pixel occuperebbero nominalmente 7.046.430.720 byte. Il confronto richiede la stessa geometria e le impronte identiche per ruolo e canale. Una differenza conserva entrambi gli esiti e lascia l'equivalenza non verificata. Il comparatore ha accettato i 64 riferimenti storici e rifiutato 64 impronte alterate. Nessun confronto reale tra build è stato eseguito.

Soggetto del piano candidato SHA-256 `a4e44f04d5c4b7492d384c9a5ef137b9a636e21ade3b9a600025fd3f0cae72bd`, archivio verificato su H: e K: `f5b6854f700a50009ed645cfe67eb59ef293eccfc9896d0dc403e474e2a9d0be`. Restano la qualifica degli input rilocati per questi 64 casi, le revisioni di un binding dedicato e un'ammissione distinta. Il piano dei 456 casi residui conserva il suo ambito.

Per i 64 casi appaiati sono stati verificati 62 sidecar XDRZ e 11 immagini sorgente. La sostituzione inversa dei percorsi ricostruisce i byte originali dei sidecar. Per 36 sidecar in comune, le impronte rilocate coincidono anche con quelle del pacchetto dei 456 casi. Le quattro esposizioni di ogni caso conservano i parametri e le impronte delle immagini di lavoro. I 62 file sono stati riletti dall'archivio H:. Manifest SHA-256 `310d5e5199ddd432829f7d2f4cfdff3087328abfedaeceb41520ee664be42410`, archivio verificato su H: e K: `dd2a49656276c4f37c6e89e054e1bcb9ce13fd1929b46635587b89efb14bf709`. Resta da verificare la lettura effettiva dei sidecar da PixInsight sotto il binding approvato e ammesso.

I 64 riferimenti storici del piano appaiato sono stati riconciliati con i file fisici originali. Tutti i 240 piani di integrazione e peso, per 7.046.430.720 byte, corrispondono alle impronte per ruolo e canale. Il controllo ha verificato anche stabilità e dimensione durante la rilettura. Rapporto e codice su H: e K:, SHA-256 `b5fd55db8edb160f28f92f57196c49f3157f876d7b7b202e0e187e768123116c`. Le misure rappresentano la sola base 1706: l'output 1719 appaiato e l'esito di equivalenza devono ancora essere prodotti.

Il comparatore candidato verifica i record R4 del parent originale e della prenotazione rilasciata, lega le ricevute ai 64 casi e all'esatto piano rilocato e ricalcola le impronte dei 240 piani prodotti. Distingue file assente, dimensione difforme, impronta difforme, reale differenza e coincidenza esatta. Dieci scenari isolati coprono anche la ricevuta di un'operazione estranea e la prenotazione ancora attiva. Il pacchetto su H: e K: ha SHA-256 `e549f197790dddf7c7ea6061b8977a9d65c8c150a44e55de5a8a55b85d75606f`. La prima esecuzione sul risultato 1719 attende il binding e le ricevute di una prova ammessa.

Il worker appaiato per la build 1719 è stato specializzato dal motore già verificato offline. Il protocollo fissa i 64 casi e mantiene le 26 letture tipizzate e le 547 impronte sorgente previste. Il collaudo di sintassi e nove scenari isolati verificano il rifiuto di modifica della build, operazione, ambito, parametri e sconfinamento nel caso seguente. Worker SHA-256 `5365f6bf92c3f7d9b9ce1fd9e17e88f020c82ecfd6e3af048ffd1229f5ac42c8`, protocollo `e43430ab99d9f6d64575b317c99f365b3c9505695b8a5a21a8ceea461f2c1630`, archivio H: e K: `27453c6e2f7998e05bf8be23b7611554b69bcba2474b173325d555bdd3145126`. Restano l'integrazione del nuovo soggetto con R4 e le verifiche indipendenti. Nessuna chiamata nativa.

### Candidata dispatch R4 per il confronto appaiato su DSG-Shared

La candidata collega il worker da 64 casi agli stadi di avvio e dispatch con il protocollo congelato. Il dispatch verifica le impronte del CURRENT e del manifest R4, l'identità del piano nei record di acquisizione, il processo padre originale e le evidenze di finestra e moduli. Il FILETIME del padre viene confrontato conservando tutte le cifre. Il segnale terminale richiede 64 casi osservati e 64 ricevute di chiusura, con zero immagini o risorse trattenute.

Il collaudo offline su DSG-Shared ha raggiunto una volta il callback simulato, respinto 13 casi negativi e verificato cinque condizioni terminali. Le due fasi native generate passano la verifica di sintassi JavaScript. Soggetto SHA-256 `4b24fabf1efcd676655271e3a4eb74469be7648fe62fa48607f28dfeed69892f`. Archivio riletto su H: e K:, SHA-256 `8c051528db62f9c79f5eede82c9f609a49ab6d0cf915ab132ed22e624905b4d8`.

La candidata copre avvio e dispatch interni a PixInsight. Restano il collegamento end-to-end al launcher padre, la qualifica nativa della console sulla build 1719 e la revisione indipendente. Nessuna richiesta di ammissione, chiamata nativa o chiusura scientifica.

### Collegamento del processo padre al confronto appaiato

Il padre dedicato risolve lo stesso soggetto congelato per entrambe le fasi, genera gli script con il Node verificato e confronta acquisizione e identità originale con la prenotazione ricevuta. Il collaudo su DSG-Shared ha osservato un processo testimone reale e la pubblicazione atomica della sua identità su NTFS. Il rendezvous ha respinto sette condizioni anomale. Il controllo del padre ha inoltre respinto l'operazione storica del suffisso, il cambio di un tick del FILETIME e l'acquisizione alterata nel registro di prova.

Manifest SHA-256 `86a01b8433b2de624e6498917e7d60dc9574f086ed128fd0cc9bf75d90673d2b`. Archivio riletto su H: e K:, SHA-256 `7c24e50aa678b8d85b03e905f6dba4440f024e268747b28983055801f8d525cd`. Restano da integrare e qualificare la consegna del comando attraverso la console 1719 e la finalizzazione appaiata dopo l'uscita. Nessuna richiesta di ammissione e nessuna chiusura scientifica.

### Verifica dei risultati del confronto dopo l’uscita del processo

La candidata di chiusura ordinaria richiede il completamento di tutti i 64 casi e delle 26 letture tipizzate. La verifica successiva lega le ricevute all’uscita del processo originale, alla prenotazione e al protocollo congelato. Rilegge i contenuti delle 26 letture e dei 240 piani binari prima di sigillare le evidenze. Il sigillo conserva le impronte usate per collegare il successivo rilascio R4 al confronto con la build 1706.

Il collaudo offline ha verificato i contatori terminali e riletto 240 piani sintetici. Ha respinto un caso con esecuzione fallita, un arresto parziale, una chiusura incompleta e un piano binario alterato. La chiusura tramite console e la produzione del sigillo nel processo padre restano da integrare nella catena completa. Manifest SHA-256 `2643e16ae29103495689901619d776a6d2879ec29b382b3cfe59a6f758b6e819`. Archivio riletto su H: e K:, SHA-256 `bf79f47c5fce0bf91f3ecde0298d1065521ada7fb4e7a3a06374093bd41349f1`. Nessuna ammissione richiesta e nessuna chiusura scientifica.

### Catena del padre e rilascio appaiato

Il runner del padre collega la finestra originale, la chiusura ordinaria e la verifica successiva alla stessa prenotazione. Il rilascio appaiato richiede il sigillo di verifica, l’uscita a zero del padre, l’identità originale completa e le impronte delle ricevute di caso, chiusura e lettura tipizzata. La rilettura verifica il rilascio e l’assenza della stessa prenotazione attiva.

Il collaudo su DSG-Shared ha esercitato dieci scenari del runner con un testimone Windows e sostituti per console e analisi, cinque scenari di chiusura e sigillo e sei scenari di rilascio con registro isolato e trasporto simulato. Il caso di risposta persa conserva la ricevuta del rilascio simulato e respinge un secondo tentativo. Archivio riletto su H: e K:, SHA-256 `9128c3f50f5dc3f2e47ae3ab18934be27caa6cb3b0251836f74a01ba7589b518`. Manifest SHA-256 `0cec71e833fa91ccbf3ff65eb9b83a1441ca9cdd0ef720d1ab5d60dcbae57f24`. Manca il collegamento al punto d’ingresso dell’operatore e la prova della console 1719. Nessuna richiesta di ammissione e nessuna chiusura scientifica.

### Operatore appaiato e consegna al comparatore

L’operatore appaiato accetta l’operazione e il protocollo congelati dei 64 casi. Attende la terminazione del padre originale e verifica il sigillo prima di chiedere il rilascio. Dopo il rilascio confermato, l’esportazione collega le ricevute R4 e i 64 record del worker all’input del comparatore.

Su DSG-Shared, dieci scenari hanno usato il codice R4 installato con un registro isolato, processi Windows reali e ricevute scientifiche simulate. Il caso positivo ha verificato il collegamento fino all’export per il comparatore. Una ricevuta di rilascio alterata viene respinta. Una risposta persa conserva la ricevuta nel registro isolato senza confermare l’export. Manifest SHA-256 `ad279c93fd092fd615a2bc9dce91db59fdc244015d82335013d9b718c3d516fe`. Archivio riletto su H: e K:, SHA-256 `356444d71c7608c2e2b89560c3e21c28079222abed81f9a5da8657c372f9672e`. Restano i collegamenti di produzione per la console e le autorizzazioni, la revisione indipendente e l’esecuzione nativa. Nessuna ammissione richiesta sul registro canonico.

### Autorizzazioni operative del padre appaiato

Il punto d’ingresso del padre passa al runner appaiato solo i callback per decisioni firmate. L’ambito lega operazione, protocollo e worker. La configurazione deve concordare con il soggetto revisionato anche su titolo esatto della finestra e scadenze. L’inventario registra 28 componenti del launcher e le impronte del coordinatore installato.

Il collaudo con chiavi effimere ha esercitato tutte le sei decisioni operative e dieci rifiuti nel verificatore, oltre al rifiuto di un’operazione estranea e di un inventario incompleto. I test hanno usato una console simulata. Archivio riletto su H: e K:, SHA-256 `c5b4ecfb2c976060e1f47048488c5e453eafda879498a1bf5513991a2a665055`. Manifest SHA-256 `56c131e816456ce3d2c45636aadaf846d99cd6a8166cc2194f11784a848cee2b`. L’inventario conserva aperta la qualifica del titolo reale 1719 e la disponibilità dei ruoli e delle revisioni operative. Nessuna ammissione richiesta.

### Verifica prima della richiesta di ammissione appaiata

La candidata controlla i riscontri di avvio, selezione, comando e chiusura della qualifica della console 1719. Collega titolo, sessione, finestra, PID e FILETIME del processo originale alle ricevute R4. Il controllo Node lega l’esito al soggetto revisionato e ai percorsi della prova prima di chiamare il confine di ammissione. Il collaudo ha respinto otto alterazioni nei riscontri sintetici e tre variazioni al confine Node.

La scansione in sola lettura su DSG-Shared ha osservato zero processi PixInsight, nessuna prenotazione attiva e nessun publisher in esecuzione nel perimetro osservato. La qualifica nativa e le revisioni indipendenti restano aperte. Archivio riletto su H: e K:, SHA-256 `ad43f5576601bf64124b18138211898c35752703e898cc6fdd9cbeea24953d59`. Manifest SHA-256 `8e3578bc7cd3090d3ed05c6ec102265d0d6aa0bb235381c76427267100a262a1`. Nessuna ammissione richiesta.

### Punto d’ingresso dell’operatore appaiato

Il punto d’ingresso combina il controllo aggiornato della VM, la verifica del soggetto revisionato, l’adattatore R4 e il padre Python sulla stessa sessione. In caso di errore chiude il canale del custode per EOF, conservando la prenotazione se il rilascio non è avvenuto. Il collaudo con l’adattatore installato diretto a un registro isolato ha verificato quattro scenari. Il preflight negato ha impedito la prenotazione. Il rifiuto del padre l’ha mantenuta trattenuta. Il caso positivo ha verificato le evidenze per il comparatore. La risposta persa ha conservato il rilascio registrato senza confermare l’export.

L’inventario per la revisione registra 36 componenti. Manifest SHA-256 `5bd7913c160678fc1746cc757a0ecec0709aa7f87172b4c054061b2bc2ec1bd4`. Archivio riletto su H: e K:, SHA-256 `45936133c7799aed51c5c3427936313a5cb967eac1001634b880d3d6988f3492`. La cartella delle qualifiche native della console 1719 non contiene ancora un tentativo e la PR #627 è in bozza senza revisioni. Nessuna ammissione richiesta al registro canonico e nessun avvio di PixInsight.

### Fascicolo per la revisione indipendente

Le copie su H: e K: del fascicolo contengono 60 file verificati, inclusi 36 componenti del launcher e il fascicolo dedicato alla prova console. Il verificatore incluso controlla l’archivio, le impronte dei membri e i legami tra manifest, dispatcher e protocollo. La prova ha respinto un singolo membro modificato anche con un nuovo hash ZIP valido. SHA-256 dell’archivio `5e06f422d8e9617ce18a3e1dc3674743a1cb06477b59f5340041f6cd789a556a`. SHA-256 dell’indice `9c18fe960d439fdb6cda92be57ede5b497c8552b0ed49444505d3207039e2180`.

La qualifica console e il confronto appaiato conservano operazioni, revisioni e ammissioni distinte. La prima deve verificare la console 1719 sul processo originale. Il secondo deve verificare la catena scientifica e i 240 piani. La PR è in bozza e risulta priva di revisori assegnati e di revisioni registrate. Nessuna ammissione richiesta.

### Diagnostica degli scostamenti per piano binario

La diagnostica misura differenze a livello di bit e di valore, errore massimo, medio e quadratico, e superamento delle soglie 1/1.000.000 e 1/20. Conta i confronti con riferimento zero e quelli con valori non finiti. Legge a blocchi e verifica entrambe le impronte prima di restituire misure. La decodifica Float32 little-endian va sostenuta dal riscontro nativo della rispettiva build.

Sono passati sette scenari sintetici, inclusi un cambio a cavallo del limite di blocco e il rifiuto di un’impronta errata. La rilettura di due piani storici della build 1706 ha confrontato 8.388.608 pixel con i propri byte, con zero differenze. Archivio riletto su H: e K:, SHA-256 `713ad391c1c003acc824a4774bff3513bd2fba400607d37b7e4c4e6925199b75`. Il collegamento del misuratore ai 240 piani dopo il rilascio R4 resta da qualificare. Nessuna prova 1719 e nessuna chiusura scientifica.

### Misure finite dopo il rilascio R4

La candidata collega l’esito del controllo dei byte alla misura dei piani. Per costruire la coda richiede le ricevute R4 della prova appaiata e due riscontri nativi di layout con impronte verificate. Il riscontro 1719 deve riferirsi alla prenotazione della prova. Le misure rileggono le impronte dei piani e riportano separatamente i riepiloghi per integrazione e peso, conservando la copertura incompleta.

Il collaudo con 240 piani sintetici ha misurato 239 piani, recuperato la differenza nota e contato un file mancante. Ha respinto una coda alterata, una voce duplicata e un riscontro di layout riferito a un’altra prenotazione. Archivio verificato su H: e K:, SHA-256 `b0f6f78cc3e763d263335cb5a1bd4a74a1546adb44cd2770e01299095ee8b02f`. I riscontri nativi del formato e i risultati appaiati della build 1719 restano da acquisire. Nessuna chiusura scientifica.

### Layout storico Float32 della build 1706

La rilettura indipendente ha decodificato i sorgenti XISF Float64 e ha riprodotto byte per byte i 26 piani di lettura salvati nativamente. Il controllo copre 109.051.904 campioni e ha discriminato l’ordine dei byte in ogni piano. La verifica separata dei 64 casi ha riletto tutti i 240 piani di integrazione e peso, per 7.046.430.720 byte. La decodifica little-endian ha riprodotto gli estremi nativi sui pixel con peso positivo in ogni caso. La lettura byte-swapped ha fallito il controllo in tutti i casi.

Ricevuta di layout per il comparatore SHA-256 `85d5174ba24ba8c5822f8c28c94f5821cb4cf3a4f8fee133dc4fe87bc4961a5a`. Riscontro completo SHA-256 `af4c4b46b871d8d78040622026b15c235a397ac71467b72b051ef5c4a1b959f6`. Archivio riletto su H: e K:, SHA-256 `520d34a9b3a3d762dcc246d8dc80b7bc67143c44460ee11ba933cbbb8a6e051f`. La qualifica riguarda l’ordine dei byte dei risultati archiviati della build 1706. Per la build 1719 il riscontro resta da acquisire sulla prova ammessa. Nessuna chiusura scientifica.

### Verifica differita del formato della build 1719

Il verificatore candidato consuma le evidenze della prova rilasciata da R4 e ricostruisce i 64 casi, le 26 letture tipizzate e i 240 piani. Prima di produrre la ricevuta di formato confronta le letture con la conversione XISF indipendente e verifica gli estremi nativi decodificando entrambi gli ordini dei byte. Rilegge la stessa evidenza di rilascio prima della pubblicazione.

Il collaudo sul protocollo congelato ha ricostruito le dimensioni dei 240 piani e ha respinto una ricevuta alterata. Il lettore adattato ha riprodotto i riscontri di due casi storici, otto piani complessivi. La copia v2 della generazione della coda corregge un fine riga letterale che rendeva il JSON scritto dalla CLI illeggibile a Node. Archivio verificato su H: e K:, SHA-256 `840b735b70c686cd1d831dad8f02e3fba4d5b83b01a86c5a9602e46ad37f5383`. Nessun esito nativo 1719 disponibile per questo confronto e nessuna chiusura scientifica.

### Matrice residua e percorso di chiusura BKL‑046

La riconciliazione confronta riga per riga l’indice GitHub riletto con il registro locale. Corrispondono 4.920 identificativi e 14.521 criteri letterali. Le disposizioni restano 4.887 con completamento da dimostrare, 26 con evidenza parziale, sei con revisione dei metadati e attestazione di matrice pendente, una con esclusione API interna motivata e attestazione pendente. La mappa conserva il criterio e la prossima prova per tutti i 25 assi e i 19 criteri di consegna.

| Famiglia | Assi aperti | Evidenza ancora necessaria |
| --- | ---: | --- |
| CFA, dither, drizzle | 4 | Identità fisica Bayer, registrazione, supporto e scale native confrontabili |
| Fondo diffuso | 3 | Contrasto, fondo assoluto e contaminazione su domini indipendenti |
| Filtri e colore | 4 | Risposta misurata, PSF e indipendenza dei riferimenti |
| Rumore e flusso | 3 | Calibrazione fisica e verifica della covarianza su realizzazioni indipendenti |
| PSF e campionamento | 4 | Riferimenti e incertezza per campionamento, variazioni e confusione |
| Saturazione e sovrapposizione | 4 | Risposta del sensore, clipping per canale e prove di ricomposizione |
| Versioni e backend | 3 | Confronti a input identico, variazioni isolate e protocollo stocastico |

Il layout 1706 e il collaudo del launcher sono collegati con le rispettive impronte. Il confronto 1719, la conoscenza finale e il trasferimento integrale GitHub restano aperti. SHA-256 del rapporto `e6bcc0ef775a2c019fdaf8c06139eb3345245e368aa2b6caba6ddf1f8f3b8676`. Archivio riletto su H: e K:, SHA-256 `ca4edd6875ca488a09e2691ab9e5f4994f78d0e9b5866a164bddc036ece87e86`. Zero chiusure scientifiche.

### Copertura della fase subpixel nel campo NGC 6341

Il confronto congelato dell’asse `PSF_PIXEL/2` contiene 415 stelle al centro del pixel, 314 nella fascia intermedia e sette al bordo. Le sette stelle di bordo occupano sette tessere distinte. Il chip 1 ne contiene quattro su 185 tessere e il chip 2 tre su 178.

Con il ricampionamento separato per chip già fissato, la probabilità che una replica perda la classe di bordo è circa **0,0851%**. Su 1.000 repliche la probabilità di perderla almeno una volta è **57,3%**. Il calcolo usa, per ogni chip, la probabilità di estrarre sempre tessere prive di bordo e moltiplica le probabilità dei due chip. La replica incompleta osservata resta nel registro e l’intervallo bordo–centro resta assente.

Per qualificare il confronto successivo servono posizioni indipendenti dal fit fotometrico e una copertura al bordo distribuita tra tessere, chip e campi indipendenti. L’occupazione delle tessere verifica se il confronto è calcolabile. La precisione del 90º percentile richiede una verifica distinta. Le copie archiviate su H: e K: hanno riprodotto lo stesso rapporto, SHA‑256 `49c93db0bd2dfc4970928945ad50ccf0455d4bcb1bed0efd21d4618f2ed0a269`. L’asse scientifico resta aperto.

### Copertura Gaia DR3 e provenienza WCS delle pose NGC 6341

La selezione Gaia DR3 entro 0,1° dal centro contiene 21.629 righe. Il filtro per soluzione astrometrica, duplicati e RUWE conserva 11.988 sorgenti. Le posizioni sono state propagate da J2016.0 all’epoca delle tre pose ACS/WFC GO‑9453 del 27 agosto 2002 e proiettate nella geometria FITS. La verifica usa il moto proprio e la covarianza formale di posizione e moto proprio. La parallasse apparente e l’incertezza della registrazione restano fuori da questo controllo. [Schema Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) · [Archivio HST MAST](https://archive.stsci.edu/hst/archive_services.html)

Nella posa da 90 s, con deviazione standard formale sull’asse maggiore fino a 5 mas, la fase nominale al bordo comprende 132 proiezioni in 115 tessere sul chip 1 e 195 in 165 tessere sul chip 2. Sono proiezioni del catalogo. Le corrispondenze univoche con le stelle misurate e l’idoneità fotometrica per la coorte restano da verificare. Il rapporto riprodotto dai tre FITS originali sulle copie locali e su H: ha SHA‑256 `498064cfb99600c65f2bbeff7eb2c32c6f16120bee720240c414c470967c0379`.

Tutti e sei gli header SCI indicano `FIT_REL_GAIAeDR3` nella WCS primaria. La proiezione primaria con Gaia DR3 serve a selezionare il campo e misurarne la copertura. Per un confronto astrometrico indipendente occorre partire da una soluzione strumentale con provenienza verificata e riservare tessere intere alla validazione. Il riscontro degli header ha SHA‑256 `37f3a14120ced79058070425b24620e74a95a96c236eec8f0659a3b524af6002`. L’asse `PSF_PIXEL/2` resta aperto.

### Soluzione WCS strumentale e separazione delle tessere NGC 6341

L’alternativa FITS `A` ricostruisce la stessa mappatura del blocco WCS incorporato `IDC_4bb1536oj`, che contiene la correzione di distorsione e ha il campo catalogo vuoto. Il controllo usa 81 posizioni interne per chip su tutte e tre le pose GO‑9453. In totale, 486 posizioni coincidono entro 3,1 × 10⁻⁹ pixel. Nella stessa griglia, il passaggio dalla WCS primaria all’alternativa sposta le coordinate di 47,8–50,8 pixel circa. Questo scarto misura la differenza tra le due trasformazioni. L’accuratezza sulle stelle resta da misurare. [Convenzioni WCS STScI](https://hst-docs.stsci.edu/drizzpac/chapter-4-astrometric-information-in-the-header/4-5-absolute-astrometry)

La rilettura delle 736 posizioni archiviate mostra che tutte ricadono nelle tessere dispari da 256 pixel nelle pose da 5 e 90 s. Una partizione da 512 pixel colloca 360 di queste stesse stelle nelle tessere pari. Per mantenere separato il campione storico, la prossima registrazione deve riservare le tessere dispari da 256 pixel e determinare le corrispondenze di addestramento separatamente. Il ricampionamento descrittivo del confronto storico conserva le tessere da 128 pixel.

Il rapporto WCS riprodotto dai FITS su H: e sul volume della VM ospitato su K: ha SHA‑256 `bd2500f06adc346d83518f90e001003404dbe3e28529f76d053f449b71fdc538`. Il rapporto di partizione ha SHA‑256 `2b388795582bbcc56b429f4d686b0efe2c604084b15cfbc62909863276809721`. La registrazione e la valutazione metrologica sui centroidi restano aperte.

### Registrazione pilota Gaia sulla WCS strumentale di NGC 6341

La traslazione iniziale e il fit affine sono stati stimati separatamente per posa e chip, usando soltanto picchi estratti dalle tessere pari da 256 pixel e sorgenti Gaia con incertezza formale propagata fino a 5 mas. La valutazione usa le 736 stelle storiche delle tessere dispari. Sono ammesse soltanto corrispondenze reciproche e univoche entro 1 pixel. Le sorgenti prive di corrispondenza restano nel denominatore.

| Posa | Chip fisico | Stelle con corrispondenza | P90 radiale delle corrispondenze | Entro 0,10 pixel |
| --- | ---: | ---: | ---: | ---: |
| 5 s | 1 | 44 / 341 | 0,536 px | 3 |
| 5 s | 2 | 71 / 395 | 0,470 px | 11 |
| 90 s | 1 | 44 / 341 | 0,536 px | 4 |
| 90 s | 2 | 71 / 395 | 0,477 px | 11 |

Il confronto pilota non qualifica il riferimento per distinguere le fasi subpixel secondo il limite di 0,10 pixel. I due totali per posa non attestano la continuità di identità Gaia tra le due pose. Il P90 è condizionato alle sole associazioni accettate. La prova non misura la fotometria né isola i contributi di propagazione, affollamento, centroidi e registrazione. Rapporto identico dai dati su H: e sul volume della VM ospitato su K:, SHA‑256 `b4402ddb36b9c9ecd8bb04f8491bba961c63032809abff7581f8c108dd1ed64c`. L’asse resta aperto.

### Continuità delle associazioni Gaia tra le pose da 5 e 90 secondi

La rilettura del pilota ha prodotto lo stesso rapporto senza modificare l’allineamento o la selezione. Le 44 associazioni del chip 1 e le 71 del chip 2 appartengono alle stesse stelle e alle stesse sorgenti Gaia nelle due pose. Nel campione comune, il P90 della media vettoriale degli scarti vale 0,533 pixel sul chip 1 e 0,479 sul chip 2. Il P90 della differenza tra gli scarti vale rispettivamente 0,226 e 0,038 pixel. Il risultato mostra che una parte rilevante dello scarto si ripete fra le due pose. La sua origine resta da isolare.

Tra le 115 associazioni comuni, i centroidi archiviati contengono una sola stella di bordo nella posa da 5 s e nessuna nella posa da 90 s. La classe nominale da Gaia e quella del centro misurato concordano per 33 e 31 stelle rispettivamente. Questa coorte non sostiene il confronto fotometrico bordo–centro. Il rapporto è riproducibile dai dati su H: e sul volume della VM ospitato su K:, SHA‑256 `967776bea29bc659008d39b1821e668a1057043131023ec8b2bc908f7db31c78`. L’asse scientifico resta aperto.

### Provenienza e sovrapposizione di osservazioni indipendenti per NGC 6341

La tabella osservativa HACKS include le immagini ACS/WFC F606W GO‑9453 dell’agosto 2002 utilizzate nello studio. Il catalogo combinato dei moti propri HACKS riusa quella serie e va escluso dalla verifica indipendente delle pose GO‑9453. JWSTSTARS ERS‑1334 usa immagini di un altro telescopio, mentre il catalogo pubblicato allinea RA e Dec a Gaia DR3. La provenienza dei pixel e quella del riferimento celeste richiedono due verifiche distinte. [Tabella HACKS](https://archive.stsci.edu/hlsps/hacks/hlsp_hacks_hst_multi_all_multi_v1.0_observation-table.pdf) · [Descrizione catalogo JWSTSTARS](https://archive.stsci.edu/hlsps/jwststars/hlsp_jwststars_readme.txt)

Da MAST sono state acquisite e verificate due pose originali ACS/WFC F606W GO‑10775 dell’11 aprile 2006. I FITS identificano `j9l958p2q` da 7 s e `j9l958p4q` da 140 s. Con le WCS strumentali, **502 delle 736 posizioni storiche** cadono in entrambe le nuove immagini ad almeno 32 pixel dai margini. Le WCS primarie ne contano 504. Sono proiezioni geometriche. Rimangono da verificare le identità, i centroidi e l’effetto dei moti propri tra il 2002 e il 2006. Le misure di registrazione e la validazione della fase restano aperte. [Programma ACS GO‑10775](https://archive.stsci.edu/prepds/acsggct/)

Il rapporto e le due acquisizioni esatte sono conservati su H: e sul volume della VM ospitato su K:. La rilettura da H: ha riprodotto il rapporto con SHA‑256 `c65075becf0a5f3760ab8873c667754f528091a4e6d04071533a8358944cc9da`.

### Centroidi nelle pose ACS indipendenti del 2006

La registrazione parte dalle WCS strumentali del 2002 e del 2006. Il fit affine per posa e chip usa soltanto rilevazioni dalle tessere pari del 2002. Il controllo sulle 736 posizioni storiche esclude qualsiasi rilevazione del 2006 impiegata come ancora. Le corrispondenze reciproche e univoche sono accettate entro 1,5 pixel.

Ciascuna posa del 2006 restituisce 197 candidati su 519 posizioni ammissibili dopo il fit e il margine. Le due pose condividono 192 identificativi del campione storico. Il P90 radiale delle associazioni accettate varia tra 0,269 e 0,313 pixel nei quattro raggruppamenti per chip e posa. La verifica dell’identità fisica delle stelle tra le due epoche e la correzione dei moti propri restano da fare. Le distanze misurano il residuo dell’intera catena di confronto, che comprende registrazione, centroidi e variazioni intercorse dal 2002.

I dati su H: e sul volume della VM ospitato su K: hanno prodotto lo stesso rapporto, SHA‑256 `05bb4c2377a54151badf959d01f45de0b16861747031b62a550fb7d8832c322d`. L’asse `PSF_PIXEL/2` resta aperto.

### Ripetibilità dei centroidi del 2006 sul piano ACS del 2002

Il pilota è stato riprodotto senza modificare rilevazioni, fit o associazioni. Per le 192 candidate comuni, i centroidi da 7 s e 140 s sono stati invertiti attraverso le trasformazioni delle rispettive pose e riportati sullo stesso piano ACS del 2002. Il P90 delle distanze tra i due centroidi del 2006 è **0,059 pixel** e 186 coppie sono entro 0,10 pixel. Il P90 della distanza fra la loro media e il centro archiviato del 2002 è **0,288 pixel** e 43 coppie sono entro 0,10 pixel.

La ripetibilità tra pose vicine nel 2006 è misurabile in questa sottocoorte. Lo scarto tra epoche include ancora effetti di registrazione, centraggio e moto proprio. Il campione contiene solo due centri storici al bordo del pixel e resta insufficiente per il confronto fotometrico bordo–centro.

Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `fd0f4ca1cacd3a31299eb94d21145c9300bc7fc06eaa5c927b7ff8e5c32b6fe7`. L’asse scientifico resta aperto.

### Effetto dei moti propri Gaia sullo scarto fra 2002 e 2006

L’incrocio delle associazioni Gaia coerenti nelle due pose del 2002 con le candidate comuni delle pose del 2006 conserva 26 stelle, 12 sul chip 1 e 14 sul chip 2. I due pilot sono stati riletti senza modificare registrazione o associazioni. Il controllo proietta il moto proprio catalogato su 3,622 anni e rimuove le componenti affini sia dal vettore previsto sia da quello misurato. La rimozione serve al confronto differenziale e lascia intatto il fit delle immagini.

| Chip | P90 dello scarto misurato | P90 dopo la sottrazione Gaia | Variazione della somma degli scarti quadratici |
| --- | ---: | ---: | ---: |
| 1 | 0,213 px | 0,207 px | +20,8% |
| 2 | 0,190 px | 0,180 px | −7,9% |

Lo scarto dopo la sottrazione rimane sopra 0,10 pixel su entrambi i chip. I moti propri catalogati danno un risultato diverso sui due chip, nel sottoinsieme selezionato dalle associazioni concordanti. La verifica non separa gli errori di centraggio e registrazione dall’incertezza dei moti propri. Rapporto riprodotto da H: e dal volume della VM ospitato su K: con SHA‑256 `cc9c96cbace48557a3b8addc9c192393577f98b9390d7ea88aab66ebef0cc1b8`. L’asse resta aperto.

### Sensibilità della copertura di fase al modello di centraggio

Sulle 736 sorgenti storiche sono stati ricalcolati i centroidi nei FITS del 2002 con il modello ePSF ACS/WFC F606W pre‑SM4. Il fit parte dai centri archiviati, usa lo stesso nucleo di raggio 3 pixel per ogni sorgente e conserva i rifiuti per qualità dei pixel o spostamento fuori tolleranza. Le classi di fase mantengono le soglie di 0,25 e 0,375 pixel.

| Posa | Centroidi confrontabili | Bordo con i vecchi centroidi | Bordo con ePSF |
| --- | ---: | ---: | ---: |
| 5 s | 685 | 7 | 278 |
| 90 s | 647 | 3 | 259 |

Sono disponibili 643 sorgenti in entrambe le pose. Il P90 dello spostamento tra i due stimatori varia tra 0,188 e 0,192 pixel nei quattro gruppi chip–posa. La scarsa occupazione storica del bordo dipende dalla definizione del centro utilizzata per il confronto. Entrambi gli stimatori usano i pixel delle stesse immagini. L’accuratezza assoluta e la nuova fotometria per classe di fase restano da verificare. Il rapporto riprodotto da H: ha SHA‑256 `f38337d25d96f1100b2a539567f55931651f3bf0d29a41544ab7593778008da6`. L’asse resta aperto.

### Ripetibilità del flusso per fase con i centroidi ePSF

Le 643 stelle comuni alle pose da 5 e 90 s sono state rimisurate con lo stesso modello ePSF e gli stessi pixel per entrambe le scelte di centro. Per ciascuna scelta si stimano ampiezza e fondo costante. Il rapporto fra le ampiezze è normalizzato solo per il tempo di esposizione.

Con le classi definite sulla posa da 5 s, la differenza bordo meno centro del P90 del log‑rapporto assoluto è +0,0047 sul chip 1 e −0,0039 sul chip 2. Gli intervalli descrittivi al 95% del ricampionamento per tessere comprendono zero su entrambi i chip, rispettivamente da −0,0139 a +0,0160 e da −0,0173 a +0,0090. Anche gli intervalli del cambiamento dovuto alla scelta del centro comprendono zero. Il confronto conserva le riclassificazioni tra pose e le misure della sottocoorte con classe stabile.

Fase e flusso derivano dagli stessi pixel e i campioni appartengono allo stesso campo. Per una validazione indipendente servono un riferimento di fase separato e la replica su un secondo campo. Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `17cb145f156f601430d433c4fba55ee7fab946ed44b6c0be9f4b9699bab3317a`.

### Pose distinte per il riferimento di fase e la fotometria nel 2006

Il protocollo fissa i ruoli prima della lettura delle nuove immagini. Le pose F606W `j9l958p6q` e `j9l958p8q`, entrambe da 140 s, sono riservate alla stima di fase. La posa `j9l958paq`, anch’essa da 140 s, è riservata a un controllo di ripetibilità separato. Le pose `j9l958p2q` da 7 s e `j9l958p4q` da 140 s restano destinate alla fotometria. Le cinque acquisizioni ACS/WFC GO‑10775 dell’11 aprile 2006 hanno impronte distinte e coprono circa 94,3 minuti tra i primi e gli ultimi istanti centrali.

Con la WCS strumentale, a più di 32 pixel dai margini, 468 posizioni della coorte storica cadono in entrambe le pose di fase e in entrambe le pose di fotometria. Di queste, 435 ricadono anche nella posa riservata alla ripetibilità. La copertura è geometrica. Restano da misurare i centroidi indipendenti e l’errore con cui si può predire la fase nelle pose di fotometria.

Il protocollo ha SHA‑256 `67cdd5b15372c5d2710979a87b7a204fda455acc8e0a8b55182ef65ecb852f10`. I FITS aggiuntivi sono archiviati su H: e sul volume della VM ospitato su K:. La prova riprodotta da H: ha SHA‑256 `327cbaa23fe8920bc186384ff82acc9bb80b86ba4e365e3d546ea3d795b5775f`.

### Ripetibilità predittiva sulle sole pose di riferimento nel 2006

La media dei centroidi delle due pose di fase è stata riportata nel piano della terza posa di riferimento. Il fit geometrico di ciascuna posa usa rilevazioni nelle tessere pari del 2002. La verifica riguarda una coorte separata, dalle tessere dispari. I due FITS destinati alla fotometria sono rimasti fuori dalle letture e dal fit.

Le tre pose condividono 36 candidate. Sul chip 1 il P90 dello scarto radiale è 0,147 pixel e la classe coincide per 14 candidate su 21. Sul chip 2 il P90 è 0,082 pixel e la classe coincide per 15 su 15. Le misure non qualificano l’intero riferimento. Il chip 1 supera il limite di 0,10 pixel e la coorte comune è molto più piccola della copertura geometrica. Rimane da stabilire una previsione di fase trasferibile alle pose destinate al flusso.

Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `b3d9888b7bb685891e014df8ff947b969037337dadb96fa296ba8d2ce5f86ffb`. L’asse scientifico resta aperto.

### Campione rilevato direttamente nelle pose di riferimento del 2006

Il confronto è stato ripetuto partendo da nuove rilevazioni nella prima posa di riferimento del 2006. Le rilevazioni nelle tessere pari da 256 pixel servono alla registrazione e quelle nelle tessere dispari alla verifica. I pixel del 2002 e quelli delle due pose fotometriche non sono stati letti.

Dalle 4.096 rilevazioni iniziali nelle tessere dispari si ottengono 548 candidate con corrispondenza univoca nelle altre due pose. Sulla posa di controllo, il P90 radiale è 0,133 pixel sul chip 1 e 0,131 sul chip 2. La classe di fase coincide per 181 su 277 candidate e 195 su 271, rispettivamente. Anche il controllo descrittivo limitato alle previsioni lontane più di 0,10 pixel dalle soglie conserva dieci cambi di classe su 106 candidate.

Il campione più ampio rende misurabile la ripetibilità senza dipendere dalle associazioni tra epoche. Il limite radiale di 0,10 pixel rimane superato su entrambi i chip. La qualifica e il trasferimento di fase alle pose fotometriche restano aperti. Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `a5e2d33f9068019614af6d006f6736b433f34d454ef5dbc14a352da60ad2a82d`.

### Controllo ePSF sulle stesse associazioni del 2006

Il confronto mantiene le associazioni e i coefficienti di registrazione del pilota a momenti. Dei 548 candidati, 372 hanno dati accettabili per entrambi gli stimatori nelle tre pose di riferimento. I rifiuti dei fit sono conteggiati separatamente. I pixel delle pose fotometriche restano fuori dal controllo.

| Chip | Candidati comuni | P90 a momenti | P90 ePSF | Classi concordanti con ePSF |
| --- | ---: | ---: | ---: | ---: |
| 1 | 182 | 0,127 px | 0,045 px | 176 |
| 2 | 190 | 0,128 px | 0,038 px | 172 |

L’ePSF porta il P90 sotto 0,10 pixel su entrambi i chip della posa di controllo, nella sottocoorte accettata e con la registrazione congelata. La precisione e la copertura nelle due pose fotometriche restano da verificare. Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `0b519a9d051fc30a5a64672afcc5f63fce048fdf26af17f00bd2550a15568eb8`. L’asse scientifico resta aperto.

### Trasferimento della fase alle pose fotometriche del 2006

Un protocollo distinto, fissato prima della prova, usa le tessere pari per calibrare la geometria di ciascuna posa fotometrica e le tessere dispari per valutarla. Le previsioni individuali della fase derivano dalle due pose di riferimento. I centroidi bersaglio delle tessere dispari servono a verificare le previsioni e a controllare l’univocità delle corrispondenze. La prova non misura il flusso.

| Posa bersaglio | Chip | Associazioni valutate / candidate | P90 ePSF |
| --- | ---: | ---: | ---: |
| 7 s | 1 | 186 / 274 | 0,09788 px |
| 7 s | 2 | 176 / 248 | 0,10317 px |
| 140 s | 1 | 194 / 289 | 0,04140 px |
| 140 s | 2 | 183 / 264 | 0,04198 px |

La posa da 140 s rispetta il limite di 0,10 pixel nei due chip sulla sottocoorte accettata. Il chip 2 della posa da 7 s supera il limite. La qualifica congiunta per il confronto di flusso resta aperta. Il protocollo ha SHA‑256 `60301c08b6fbaa1c4efb978f6199c19f6d7405688fff61617e3c0ef9f1aa9f9d`. Il rapporto riprodotto da H: e dal volume della VM ospitato su K: ha SHA‑256 `45e0534b23d387ecb20a2973a30d4311d0d00ff411cc276785df30c655bd8ece`.

### Incertezza spaziale del P90 nel trasferimento di fase

Il rapporto di trasferimento è stato riprodotto senza cambiare le associazioni o le stime puntuali. Per ciascuna posa e chip sono state ricampionate 5.000 volte tessere sorgente da 128 pixel. Il controllo ha ricalcolato anche il P90 escludendo a turno una sola tessera.

| Posa | Chip | P90 | Intervallo descrittivo 95% |
| --- | ---: | ---: | ---: |
| 7 s | 1 | 0,0979 px | 0,0744–0,1076 px |
| 7 s | 2 | 0,1032 px | 0,0823–0,1219 px |
| 140 s | 1 | 0,0414 px | 0,0382–0,0469 px |
| 140 s | 2 | 0,0420 px | 0,0347–0,0475 px |

Nella posa da 7 s entrambi gli intervalli attraversano 0,10 pixel. Sul chip 2 il P90 rimane sopra la soglia escludendo a turno ciascuna delle 118 tessere. Per la posa da 140 s gli intervalli rimangono sotto la soglia su entrambi i chip. La diagnosi riguarda il campione accettato di un solo campo. Non modifica il criterio stabilito né qualifica la coppia fotometrica. Rapporto riprodotto da H: e dal volume della VM ospitato su K: con SHA‑256 `13457e6c91efd8ad8f49064bc9b43943a3147dd58eb0c4989bf5cb2e436656d7`.

### Scarti di fase in funzione del segnale nella posa breve

Il confronto usa gli stessi abbinamenti e gli stessi scarti del trasferimento di fase. Per ciascun chip sono stati ordinati in quartili secondo un’approssimazione del rapporto segnale/rumore. Il numeratore usa gli elettroni nel nucleo dopo la sottrazione del fondo locale. Il denominatore combina in quadratura i valori `ERR` del nucleo. La stima non propaga l’incertezza del fondo né le correlazioni fra pixel.

Nella posa da 7 s, il quartile con segnale più debole contiene 15 dei 17 scarti oltre 0,10 pixel sul chip 1 e 18 dei 21 sul chip 2. I P90 passano rispettivamente da 0,130 e 0,162 pixel nel quartile più debole a 0,045 e 0,046 nel più forte. Il confronto per quartili è diagnostico. Una corrispondenza per chip nella posa breve è rimasta senza stima valida del segnale.

La concentrazione degli scarti accompagna il calo di segnale nel campione misurato. Il risultato non giustifica l’esclusione retroattiva del quartile debole. La soglia e la disposizione della coppia restano registrate. Rapporto riprodotto da H: e dal volume della VM ospitato su K: con SHA‑256 `2eb03017dd8a41ae7f850ee242078d3d48c25519edd9b289bf18220a18f8855d`.

### Secondo campo indipendente NGC 5986 e replica del controllo di fase

Sono state acquisite cinque pose ACS/WFC F606W da 350 s del programma GO‑10775, tutte del 16 aprile 2006. I ruoli sono fissati in ordine temporale dai soli header primari. Le prime due pose forniscono le stime di fase, la terza serve alla verifica e le ultime due sono riservate alla fotometria. La posa da 20 s è fuori dal protocollo a profondità uniforme. In una griglia strumentale di controllo, 105 punti su 153 per chip cadono in tutte e cinque le immagini ad almeno 32 pixel dai margini. [Programma ACS GO‑10775](https://archive.stsci.edu/prepds/acsggct/)

Il confronto mantiene la separazione spaziale e il modello ePSF usati in NGC 6341. Nel campione accettato per entrambi gli stimatori, il P90 sulla posa di controllo passa da 0,116 a 0,051 pixel sul chip 1 (171 candidate) e da 0,117 a 0,032 sul chip 2 (151 candidate). Le classi di fase concordano per 153 e 136 rispettivamente con ePSF. La ripetibilità sotto 0,10 pixel è stata osservata anche nel secondo campo, entro il perimetro di questa prova. Restano da verificare trasferimento e fotometria nelle due pose riservate. Il protocollo ha mantenuto invariata la disposizione della coppia corta–lunga di NGC 6341.

I rapporti riprodotti da H: hanno SHA‑256 `58f949e6ae3fe1f65f185629b6e37f7c2497bf6a30ab5d6e1b07bdc49f140acf` per gli input e `bd68f4a37b556396994ff3f31c24d54c931786011814f7f7c262eac32ef7be63` per la ripetibilità. L’asse scientifico resta aperto.

### Ripetibilità del flusso con fase da pose distinte in NGC 5986

Il trasferimento dalle due pose di riferimento alle due pose fotometriche da 350 s dà P90 radiali da 0,044 a 0,063 pixel sui quattro gruppi posa–chip. Tutti sono sotto 0,10 pixel. Il fit geometrico usa le tessere pari e i centroidi individuali delle tessere dispari per la fotometria sono previsti dalle sole pose di riferimento. Prima della misura del flusso sono state congelate 117 associazioni comuni. La selezione richiede corrispondenze univoche anche nelle pose bersaglio.

Il fit ePSF a centro fisso, con fondo costante e normalizzazione per il tempo di esposizione, conserva 115 stelle dopo due rifiuti per qualità dei pixel. Il confronto bordo–centro del P90 del log‑rapporto assoluto vale +0,01275 sul chip 1 e −0,00183 sul chip 2. Gli intervalli descrittivi per tessere comprendono zero, da −0,00046 a +0,05020 e da −0,02948 a +0,02868. Nella sottocoorte a classe stabile alcune repliche perdono una classe. I relativi intervalli sono omessi.

Questo risultato misura la ripetibilità in conteggi per unità di tempo, nelle due pose profonde di NGC 5986. La coppia da 7 e 140 s di NGC 6341 mantiene la propria disposizione. La calibrazione assoluta e l’estensione ad altri regimi restano aperte. Il trasferimento e la fotometria sono stati riprodotti da H:. I rapporti hanno SHA‑256 `728079b5532eade5930ae9b944828a4bc2b406e6f6999557adcd84d2591a3317` e `8dc4d9df537a9a5f543d91b85ac0298bb289ee73aaa614796582b783c44c6296`.

### Effetto della mappa dell’area dei pixel nel campo NGC 5986

La fotometria a centro fisso è stata riprodotta e confrontata con le ampiezze corrette per l’area dei pixel. La correzione usa le mappe medie STScI per WFC1 e WFC2, interpolate nelle coordinate già congelate. Le 115 stelle e i rifiuti sono gli stessi nelle due misure. [Mappe dell’area dei pixel ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/pixel-area-maps)

Il 90º percentile della variazione assoluta del log‑rapporto fra pose è 0,00521 sul chip 1 e 0,00410 sul chip 2. La differenza bordo–centro passa da +0,01275 a +0,00842 e da −0,00183 a −0,00139, rispettivamente. Dopo l’applicazione della mappa, entrambi gli intervalli descrittivi comprendono ancora zero. La correzione misura la sensibilità alle mappe medie nel dither disponibile. La calibrazione assoluta resta aperta.

Il rapporto è stato riprodotto da H: con SHA‑256 `f25f34703e37419072ccdd07668facf6a87d7bcbcccbe02433181953ef64d511`.
