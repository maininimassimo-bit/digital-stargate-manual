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
