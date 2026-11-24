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
