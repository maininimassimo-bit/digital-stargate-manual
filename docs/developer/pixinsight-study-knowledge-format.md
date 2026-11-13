# Conoscenza dello studio PixInsight e IA: struttura, consultazione e storico

## Stato e perimetro

Questo riferimento descrive la conoscenza consolidata **provvisoria H58** dello studio BKL-046. Il suo formato rende consultabili risultati, condizioni, errori ed evidenze; non costituisce un'autorizzazione a eseguire processi PixInsight né una baseline scientifica finale.

Snapshot del 13 novembre 2026:

| Componente | Identità |
| --- | --- |
| File di conoscenza | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v58.json` |
| SHA-256 del file | `b4e57205ef437d669a8973b63d02e60f917d92214732d8eb10e159579dd9e6ca` |
| Lettore | `consult_provisional_dsg_knowledge_h_v5_v10.py` |
| SHA-256 del lettore | `0e1ff134e9619f2fa22e1d376e81ab7009bb3e71eb9df9463830fc59392900ba` |
| Formato | `schemaVersion: 1` |
| Stato | `PROVISIONAL_CONSOLIDATED_QUERYABLE_NO_SCIENTIFIC_PROMOTION` |
| Requisiti | 4.920 |
| Schede di evidenza | 183 |
| Famiglie / assi / criteri Owner | 7 / 25 / 19 |
| Chiusure scientifiche | 0 |

Il registro autorevole preesistente, attestato alla versione v1.171, resta distinto da H57. Una versione provvisoria non aggiorna quel registro e non riavvia il publisher. Tutti i vincoli su portale, master, installazione, migrazione Codex e M27 restano applicabili.

Questa proposta pubblica la documentazione del formato. I file JSON, i lettori e gli archivi grezzi identificati dagli hash non sono caricati da questa pagina: il loro trasferimento completo e recupero remoto restano da attestare.

## Stato pubblicato e valutazioni locali

H57 conserva lo snapshot esatto della matrice **pubblicata v600 nel registro locale dello studio**, separato dai record locali ereditati da H55. Il confronto completo trova 3.297 righe coincidenti e 1.623 righe con soli campi aggiuntivi o ampliamenti di liste locali: nove processi, un file di script e 1.613 membri PJSR. Nessun campo pubblicato è rimosso o sostituito nei record locali.

L'incremento v600 pubblica le attestazioni documentali dei 239 oggetti e lascia invariate le altre 4.681 righe. Non pubblica automaticamente i supplementi locali delle 1.623 righe. H56 conserva entrambi i livelli e aggiunge uno snapshot di autorità per ciascuno dei 4.920 requisiti.

Il lettore distingue l'autorità **al momento dello snapshot identificato** da una consultazione del registro corrente: non legge il registro durante le query. `canonicalMatrixRecord` indica ora il record pubblicato; `localRecordedMatrixRecord`, `localSemanticRecord` e `localVersusPublishedRelation` espongono i dati locali e il loro rapporto con lo snapshot. I vecchi nomi di hash contenuti nei record semantici conservati restano riferimenti locali, con una precisazione esplicita nella risposta.

`--role` può attestare la pubblicazione documentale degli oggetti nello snapshot v600, conservando come storico il testo dell'attestazione originariamente preparata in staging. Non attesta comportamento nativo, chiusura scientifica o autorizzazione all'esecuzione. Il lettore rifiuta un file privo del livello di autorità richiesto e rileva la modifica di una riga pubblicata rispetto alla sua impronta.

H57 non aggiorna la conoscenza registrata v1.171 e non attesta una versione v1.172. Rimane un consolidamento provvisorio. Rispetto a H56 aggiunge la nuova evidenza Timer a undici requisiti e un contesto successivo a tre schede storiche: i testi di preparazione restano conservati e non sono interpretati come nuove richieste da eseguire.

## Struttura del file

| Campo | Funzione |
| --- | --- |
| `provenance` | Predecessore, programmi produttori e impronte dei supplementi. |
| `requirements` | Record per identificatore esatto di ogni requisito. |
| `evidenceCards` | Risultati circoscritti con fonti, condizioni e limiti. |
| `scientificFamilies`, `axes` | Dominio scientifico e criteri di chiusura; gli stati restano espliciti. |
| `axisEvidenceIndex` | Collegamenti tra assi e schede; un collegamento non è un'ammissione scientifica. |
| `ownerCriteria` | Diciannove requisiti di consegna finale e trasferimento completo. |
| `usePolicy` | Input necessari, soglie confermate, sequenza di uso e limiti di autorizzazione. |
| `scopeNotes` | Precisazioni della versione e differenze rispetto ai predecessori. |
| `studyComplete`, `scientificClosures`, `deliveryState` | Gate di completamento, distinti dai conteggi delle evidenze. |

I requisiti comprendono 125 processi, 368 file di script, 239 oggetti PJSR e 4.188 membri PJSR. Non si riduce il dominio ai soli processi già provati.

Ogni record conserva:

- `residual`: identificatore, criteri letterali, impronta del record locale conservato, disposizione e azione residua;
- `matrixRecord`: record locale H55 conservato, che può includere supplementi non pubblicati;
- `authoritativePublishedMatrixRecord`: riga esatta dello snapshot pubblicato v600, con la propria impronta separata;
- `localVersusPublishedRelation`: coincidenza o campi/liste locali aggiuntivi, senza confondere i livelli;
- `semanticRecord`: lettura semantica locale e storia conservata, distinta dalla prova di pubblicazione;
- `additionalScopedEvidenceIds`: supplementi consultabili per quel requisito;
- l'eventuale `documentaryAttestation`, con la portata documentale dichiarata.

I supplementi non riscrivono automaticamente gli stati canonici. H52 ha collegato 17 requisiti esatti alle nuove evidenze; H53 ha aggiunto collegamenti per l'oggetto File e quattro suoi membri; H54 collega agli stessi cinque requisiti anche il recupero locale della capsula File IO. H54 aggiunge inoltre il contesto operativo successivo ai vecchi gate del backend e il riesame delle fonti primarie di pubblicazione, conservando le conclusioni storiche nel loro ambito. Gli altri campi dei requisiti sono stati confrontati nella loro rappresentazione canonica: matrici locali, criteri, disposizioni e storia non vengono promossi tramite l'aggiunta di una scheda. H56 conserva questi campi e aggiunge i record pubblicati separati. Le cinque nuove schede riguardano audit storico, pubblicazione documentale, provenienza delle note, confronto dei livelli Timer e componenti offline della prova successiva; aggiunge collegamenti a 249 requisiti.

H55 aggiunge una scheda riferita alla prova Timer già esistente e la collega all'oggetto e ai suoi dieci membri canonici. La scheda temporale precedente conserva tutti i dati e riceve un contesto operativo esplicito, così che il vecchio testo «prove native da eseguire» non provochi una ripetizione automatica.

## Consultazione riproducibile

I comandi seguenti si eseguono sul pacchetto recuperato contenente file e lettore verificati. Non sono endpoint del portale.

```text
python consult_provisional_dsg_knowledge_h_v5_v10.py --audit
python consult_provisional_dsg_knowledge_h_v5_v10.py --workflow process:ACDNR
python consult_provisional_dsg_knowledge_h_v5_v10.py --role pjsr_object:File
python consult_provisional_dsg_knowledge_h_v5_v10.py --workflow pjsr_object:File
```

Il lettore predefinito verifica l'impronta esatta di H57 prima della consultazione. Per un altro file occorre fornire esplicitamente `--file` e `--sha256`; l'impronta di una versione diversa non è accettata.

Sono disponibili anche `--requirement`, `--axis`, `--family` e `--evidence`, con identificatori esatti. Per esempio, `--evidence FILE_ASCII_ESCAPED_JSON_AND_BINARY_NATIVE_COMPOSITIONS` restituisce la scheda della composizione nativa circoscritta.

`--audit` verifica identità interne, collegamenti, impronte delle righe, criteri e conteggi. Non rilegge automaticamente tutti gli archivi esterni, non esegue PixInsight e non valida scientificamente un'immagine.

`--role` separa la qualificazione documentale dichiarata dell'oggetto dalla sua pubblicazione autorevole e dall'ammissione nativa. Il lettore corrente restituisce anche le evidenze circoscritte più recenti, comprese le anomalie. `--workflow` espone il contratto, i residui e le schede collegate al requisito. Nessuna delle due query autorizza un'esecuzione.

## Come interpretare le evidenze

Occorre mantenere distinti almeno questi livelli:

1. inventario o dichiarazione di una funzione;
2. revisione della definizione e delle dipendenze effettivamente lette;
3. controllo isolato con sostituti espliciti;
4. osservazione nativa con input, runtime, parametri e output identificati;
5. verifica indipendente degli effetti entro un dominio e un modello dichiarati;
6. validazione scientifica applicabile al caso e accettazione dei relativi gate.

Non sono livelli intercambiabili. Un processo terminato con successo può produrre un risultato diverso dal riferimento; un archivio integro può contenere una prova fallita; una dichiarazione documentale completa non prova il comportamento di tutti i consumatori.

Le soglie Owner confermate sono il 5% per le misure relative con riferimento definito e il 5% della FWHM iniziale per la posizione sulla stessa griglia. Queste soglie non definiscono un tasso d'errore accettabile delle decisioni IA e non sostituiscono l'incertezza delle misure.

## Esempio: errori di codifica e composizione verificata

Nel campione nativo su PixInsight 1.9.5 build 1706, i quattro casi di lettura e scrittura binaria conservano i byte. I risultati testuali richiedono invece una lettura separata:

| Prova originale | Risultato circoscritto |
| --- | --- |
| Testi vuoti, ASCII e BMP selezionati | Scrittura conforme ai byte UTF-8 attesi nei cinque casi dichiarati. |
| Due testi con caratteri fuori dal piano Unicode di base | Byte e testo di ritorno diversi dal riferimento. |
| Testo con zero interno | Troncamento nella lettura e nella scrittura testuale provate. |
| Sorgente Latin-1 non valido come UTF-8 | Caratteri sostituiti; non confermata l'interpretazione Latin-1 descritta nella guida. |
| Sorgente UTF-8 con BOM iniziale | BOM rimosso nel caso osservato. |

Un modello dei tratti pertinenti del sorgente PCL installato riproduce tutti gli otto output testuali osservati. La conversione della coppia surrogata calcola il codice esteso, ma usa i bit del primo elemento per l'ultimo byte UTF-8; le funzioni esaminate impiegano inoltre lunghezze di stringhe terminate da zero. Questa concordanza non chiude la provenienza di compilazione o l'intero collegamento PJSR e non viene presentata come verifica di tutti i percorsi di codifica.

Una **prova successiva distinta** ha verificato:

- otto composizioni `File.writeTextFile` con JSON escapato in ASCII, seguite da `File.readTextFile` e `JSON.parse`;
- i codici UTF-16 effettivi degli otto input JavaScript prima della scrittura, confrontati con il produttore indipendente;
- quattro copie binarie di byte UTF-8 indipendenti, inclusi caratteri estesi e zero interno;
- due esempi di nomi di file Unicode, uno BMP e uno esteso.

Tutti questi confronti successivi coincidono con i riferimenti dichiarati. La composizione non corregge il metodo testuale originale: i suoi fallimenti restano conservati. La copia binaria preserva byte già codificati indipendentemente; non dimostra la correttezza di un qualsiasi encoder aggiunto a monte.

Nella console della seconda istanza sono stati osservati anche due messaggi di eccezione Win32 con riferimenti Qt/V8, prima del marcatore dello script. L'istanza ha prodotto le ricevute, i file sono stati ricontrollati e la chiusura normale è terminata con codice zero. Non si attesta un avvio privo di anomalie né si attribuisce una causa certa al disco o ai metodi File.

Le schede `FILE_DEFAULT_TEXT_BINARY_NATIVE_DISCREPANCIES`, `FILE_SELECTED_PCL_UTF_CONVERSION_SOURCE_MODEL`, `FILE_ASCII_ESCAPED_JSON_AND_BINARY_NATIVE_COMPOSITIONS` e `FILE_COMPOSITION_RUN_OBSERVED_RUNTIME_STARTUP_ANOMALIES` devono essere lette insieme.

La capsula locale File IO conserva 121 file, inclusi tentativi falliti, composizioni successive e verifiche. Estrazione isolata e replay dei byte/ricevute sono passati. Il suo ZIP ha SHA-256 `17e8bd7a13e8344e1b551bb4d4fe2dfce10f14bc7973c02d94fe835016edd209`. Questo recupero locale non attesta un recupero da GitHub.

## Timer: ricevuta esistente e osservazioni retrospettive

La rilettura di una prova già acquisita su build 1706 identifica quattro casi composti e nove callback registrate. I 23 controlli originari restano immutati: 22 conformi e uno discrepante. Le tre etichette di caso conformi riguardano quei controlli specifici e non validano tutti i contratti dei membri Timer.

La proprietà `precise` è inizialmente `true`, mentre la guida conservata dichiara `false` come default. La successiva assegnazione di `true` a un valore già vero non verifica una transizione da falso a vero; nessuna accuratezza temporale è stata calibrata.

Un'analisi **retrospettiva distinta** considera il contratto documentato di `count`, numero di eventi generati dall'ultimo `start()`. Nei tre punti seguenti la ricevuta registra già callback e il codice acquisito non contiene un nuovo avvio, cambio di intervallo o sostituzione del gestore prima della lettura:

| Punto di lettura | Callback già registrate almeno | `count` letto |
| --- | ---: | ---: |
| Dopo la prima scadenza singola | 1 | 0 |
| Prima dello stop periodico | 2 | 0 |
| Prima del cambio di intervallo attivo | 2 | 0 |

Questi tre punti appartengono alla stessa esecuzione composta; non sono tre prove indipendenti e non vengono aggiunti retroattivamente agli endpoint congelati. Il classificatore originario non controllava l'incremento di `count` in questi punti e resta conservato.

Per il dominio osservato, mantenere un registro esplicito dei callback invece di usare `Timer.count` come prova di consegna degli eventi. Stato del timer, callback e completamento di un processo esterno restano contratti distinti. Non è stabilita la causa nell'implementazione o nel binding, né l'applicabilità ad altre build, piattaforme o condizioni di carico.

Il rapporto retrospettivo ha SHA-256 `74c35f36220ab75310497ca832a06b971fa9b8cf3d1b2ff91e9e8efacc76b8a5`; la verifica indipendente di H55 e del lettore ha SHA-256 `a783322da099d7214718511c0bddd3a01bc04b17f86838cf7f52b9d839720575`. I dieci file sorgente della rilettura sono conservati localmente con le impronte originali. Nessuna nuova chiamata nativa o API è stata eseguita per questo aggiornamento.

La lettura completa dei file client PCL Timer conferma che il contatore C++ viene incrementato prima del gestore e azzerato da operazioni specifiche. Quel codice descrive un'interfaccia client, non prova l'identità del binding PJSR: default di intervallo e stato dopo mutazione differiscono tra i livelli documentati e osservati. Non si attribuisce automaticamente al wrapper la semantica del client.

### Prova successiva congelata ed eseguita

Dopo la pubblicazione v600 e i controlli di esclusività è stata avviata **una sola nuova istanza nativa**, vuota, su build 1706. La prova distinta comprende quattro casi composti e nove callback registrate. Dei **25 controlli congelati, 20 coincidono con l'atteso e cinque sono discrepanti**. Non vengono trasformati in un successo generale perché il processo è terminato con codice zero.

| Osservazione nativa | Risultato e portata |
| --- | --- |
| Due costruttori nel caso di precisione | `precise=true` iniziale, diverso dal default `false` documentato. |
| Scritture e riletture `false,true,false` | Coincidono nei tre punti; il controllo non modificato conserva lo stato. Questo non calibra il clock. |
| Periodico, dopo tre callback e prima di stop o altre mutazioni | `count=0`, contro il limite inferiore di tre eventi già consegnati. |
| Singolo, dopo il primo e dopo il secondo avvio | Una callback per ciascun avvio nella finestra osservata; entrambe le letture successive di `count` sono zero. |
| Prima del cambio di intervallo, dopo due callback | `count=0`, contro il limite inferiore di due eventi consegnati. |
| Contatore prima e dopo cambio di intervallo o gestore | La base è già zero: l'azzeramento resta **non identificabile**, non viene classificato come dimostrato. |

Le quattro letture discrepanti del contatore avvengono fuori dal callback, dopo il ritorno del ciclo di elaborazione degli eventi e prima delle mutazioni pertinenti. Il risultato precedente retrospettivo e questa nuova prova congelata restano separati: condividono il dominio e non costituiscono prove indipendenti di accuratezza fisica.

Avvio, scadenze singole, stop, rilettura dell'intervallo e sostituzione del gestore hanno esiti finiti conservati. L'assenza di ulteriori callback nella finestra quieta non prova un'assenza universale dopo qualsiasi stop. Le letture zero immediatamente dopo un nuovo avvio non dimostrano l'azzeramento di un contatore precedentemente positivo.

Per il dominio osservato, usare un registro esplicito dei callback e identità/ricevute dei processi per monitorare il lavoro, senza affidarsi a `Timer.count`. Stato del timer, proprietà di precisione e completamento scientifico restano contratti distinti. Parentela con `Control`, argomenti non provati, altri carichi, altre build e calibrazione temporale rimangono fuori da questi risultati.

L'istanza è stata chiusa normalmente tramite i controlli supportati della finestra, dopo la ricevuta con zero immagini; uscita effettiva zero e impronta del registro invariata sono verificate. La console conservata segnala che `msleep()` è deprecato e indica `System.msleep()`. Il sorgente congelato resta immutato: l'avviso non è una spiegazione causale dei controesempi.

| Evidenza della nuova prova | SHA-256 |
| --- | --- |
| Protocollo congelato | `229ee32fd2c432422aca527a789766d2e7c4b56765735cd5cacd8dffa31f0013` |
| Entry nativa | `b1e3005f138afb007454a74c79163c5cb5645bbf349576d70142804bcbe7af69` |
| Ricevuta nativa | `6c13e55af5a19b70de1c84b3c27649e67a0f8d21de8f2db3fca9483d9d347962` |
| Verifica indipendente degli esiti e della provenienza | `3417a71eadcb6be0fde12e3df04c6caa2b9be60e1b57c989ca9696ac5773f711` |
| Verifica indipendente H57 e lettore | `41b0c7291c4d26272d8a1f29ddf80c295c7df5018c0038318de42ce1cc930465` |

I modelli e i nove controlli offline restano qualificazioni del codice di prova. La nuova ricevuta è evidenza nativa circoscritta, senza taratura del tempo, causalità del binding o promozione delle famiglie scientifiche.

## Produzione, verifica e aggiornamento

Una nuova evidenza deve mantenere la catena:

```text
requisito → protocollo congelato → input/versioni → tentativo identificato
          → ricevuta e output → verifica indipendente → decisione e limiti
```

Per una prova nativa si conservano intento prima dell'avvio, identità del processo e sua creazione, input e sorgenti, errori, ricevuta terminale, salvataggi e History quando applicabili, chiusura dell'istanza posseduta e codice d'uscita effettivo. Un timeout di osservazione non autorizza un nuovo invio.

Ogni aggiornamento produce una versione nuova, conserva il predecessore e le sue impronte e verifica il risultato scritto. Le modifiche ai collegamenti sono dichiarate separatamente dalle modifiche alle righe canoniche. Quando cambia una conclusione, si conserva la prova precedente con la spiegazione della correzione.

Le query leggono il file identificato dall'impronta. La verifica indipendente di una fonte esterna resta un'operazione distinta; un riferimento contenuto nel JSON non dimostra che quella fonte sia stata recuperata in quel momento.

## Archivi, versioni dei percorsi e GitHub

Il trasferimento completo distingue tre perimetri:

- snapshot storici, con i percorsi e le impronte originali;
- contenuti correnti e finali, compresi i file creati dopo lo snapshot;
- originali ritirati recuperabili da archivi esatti tramite ricette e decoder identificati.

Un percorso mutabile può avere byte diversi in due versioni: il registro corrente non sostituisce la copia storica con un'altra impronta. I target di recupero devono quindi essere qualificati per versione o snapshot e ripristinati in una destinazione isolata, evitando di sovrascrivere il lavoro corrente.

L'indice della campagna completa rappresenta 23.956 originali virtuali per 4.794 blocchi, con 511.510.812.034 byte logici. Il confronto con lo snapshot di migrazione trova quattro identità storiche esatte e 23.952 percorsi/contenuti assenti da quello snapshot. Gli assenti restano nel perimetro di consegna.

Un originale virtuale richiede l'archivio effettivo, la sua impronta, il record selezionato e il decoder necessario a ricostruire i byte con dimensione e impronta attese. L'indice non vale da solo come recupero. I byte logici ricostruibili non devono essere sommati come nuovi upload ridondanti quando il contenitore preservato li trasporta già esattamente.

Per ogni artefatto restano necessari ruolo, versione, percorso storico, dimensione, SHA-256, dipendenze e identificatore remoto. Il completamento richiede i contenuti effettivi su GitHub e la loro rilettura, ricostruzione e verifica; un manifest che indica soltanto file locali non basta.

Le condizioni di pubblicazione dei materiali di terzi e dei dati privati devono essere risolte sul perimetro effettivo. Non si eliminano tali oggetti dallo storico per far risultare completo il trasferimento. La documentazione curata e gli hash pubblicati restano distinti dai byte degli archivi non ancora trasferiti.

## Riconciliazione corrente e pubblicazione documentale preparata

Il censimento dei tre alberi di studio su H registra **2.006.773 file regolari** e **1.810.646.631.304 byte logici**. È una scansione di metadati completata, non uno snapshot atomico: la directory del censimento stesso è esclusa e un percorso reparse non viene seguito. File creati successivamente, fixture di qualificazione e nuovi recuperi richiedono una ricognizione finale aggiuntiva.

Il primo confronto con lo storico usava stringhe con separatori Windows diversi e produceva false assenze. Quel risultato resta conservato come errore di confronto. La riconciliazione corretta normalizza solo i separatori, conserva i percorsi originali e non introduce confronti senza distinzione tra maiuscole e minuscole; nessuna collisione normalizzata è stata osservata.

Dei 1.982.768 record storici, 1.982.764 hanno un percorso corrente: 1.982.762 conservano anche la dimensione e due hanno dimensione diversa; quattro percorsi risultano ritirati. Stessa dimensione e stesso percorso non provano l'identità dei byte. I due casi mutati hanno copie esatte precedenti; i quattro ritirati sono ricostruibili dal contenitore e dal decoder identificati. L'audit completo ha verificato 498.051 identità attraverso gli alias registrati e ha lasciato cinque identità uniche irrisolte. Le sei osservazioni negative sui candidati restano conservate: i byte precedenti dell'adapter sono stati infine trovati anche in un altro alias registrato. Le due copie regolari supplementari e i quattro originali ricostruiti dal contenitore aggiungono quindi cinque identità nuove. La composizione copre tutte le **498.056 identità storiche e 854.043.191.084 byte unici**, senza ripristinare o sovrascrivere i percorsi originali.

Un controllo indipendente confronta l'intero insieme di identità e dimensioni con l'indice storico verificato e vincola le ricevute delle letture e delle ricostruzioni effettive. Riusa esplicitamente quelle osservazioni: non dichiara una seconda rilettura di tutti i payload. Disponibilità storica verificata, staging immutabile, copertura corrente/finale e recupero remoto sono eventi distinti.

Un controllo distinto del manifest autorevole v599 ha individuato 1.990 contenuti unici ancora rappresentati da fonti storiche su C. Sono stati copiati su H e ricontrollati sull'origine e sulla destinazione: **7.355.344.930 byte**, conservando nomi, provenienza e identità dei file. Le fonti C e il registro preesistente restano al loro posto. Si tratta di archiviazione dei dati dello studio, senza migrazione dell'installazione Codex.

La proposta documentale per i 239 oggetti PJSR ha tutte le **1.789 identità di citazione diretta** collegate a fonti correnti verificate, corrispondenti a 1.524 identità di contenuto. Questa verifica non è una nuova revisione semantica di ogni contenuto né una chiusura transitiva delle dipendenze.

Il pacchetto preparato comprende 1.462 artefatti e 239 modifiche di riga. Una verifica indipendente ha riletto tutti i 204.573.660 byte sorgente e riprodotto la trasformazione: le altre 4.681 righe restano invariate. I dati grezzi che rappresentano input falliti sono conservati come byte opachi, con le citazioni originali nel relativo indice.

Durante la qualificazione è emerso un difetto nel publisher H v2: aggiungeva una lista vuota `reviewEvidence` anche quando non erano previste evidenze comuni. Il caso isolato e la differenza non attesa sono conservati. Il publisher H v3 evita quell'aggiunta; ha superato 12 controlli isolati e quattro controlli dei vincoli di avvio. Una prova distinta con registro sintetico su H ha riprodotto tutte le 4.920 righe e le 239 modifiche reali.

Anche il verificatore successivo alla pubblicazione è stato qualificato su metadati reali completi e registro isolato: 11.217 elementi previsti, rilettura delle due copie dei 1.462 nuovi artefatti e rifiuto di una modifica estranea al registro. Questi esiti qualificano controlli di pubblicazione nel perimetro dichiarato; non sono prove native o scientifiche.

**L'incremento v600 è pubblicato e verificato indipendentemente.** Dopo l'effettiva uscita dei processi storici e il controllo delle fonti supplementari, la coda ha congelato il job e avviato il publisher una sola volta. Sono state verificate 19.604 posizioni fisiche preesistenti; il manifest contiene 11.217 artefatti. Le due copie dei 1.462 nuovi artefatti sono state rilette e confrontate. Publisher e controllo successivo sono terminati con codice zero.

Il registro preesistente resta nella propria posizione e la copia prima dell'aggiornamento è conservata su H. La conoscenza registrata resta v1.171; l'incremento riguarda la matrice documentale. Il registro è protetto da verifica dell'identità precedente, blocco e scrittura con sincronizzazione; questa modalità non viene descritta come una transazione resistente a ogni interruzione.

| Evidenza locale | SHA-256 |
| --- | --- |
| Verifica indipendente H54 e lettore | `b5268f04a0b7d59288b0b28f69db4a2c34ca04a3ad429de9a984b76d1cb85b9c` |
| Riconciliazione normalizzata dei percorsi | `080f02221e5046cbfba592faa63e1173efdf8f5396572ce53b01addf7979f1b0` |
| Archiviazione esatta dei 1.990 contenuti da C | `9ba12c80d15800c6478273ab83e6302c56b2b9d53d8c4844fe96e7bdafdcaa94` |
| Collegamento delle 1.789 citazioni dirette | `1df6779c88819d33947b2287c6cae5784f77b22cdd78c291fc02d3e02b60f2f7` |
| Controllo indipendente del pacchetto prima della pubblicazione | `494ccb85341ff894b64b981c8645a05c70583504862fd44b7ec37fa70abdddfc` |
| Qualificazione isolata del verificatore successivo | `b35a552d67ada9c86ff19268a10b3cdefb7202740490cc97ff36391e88aac96c` |

| Evidenza aggiunta in H56 | SHA-256 |
| --- | --- |
| Matrice pubblicata v600 | `8edad5a01e6df245af5631fb7b33f1274cf295abba92cd62c468220ad8437035` |
| Manifest pubblicato v600 | `0b72cb301dfcad9f55197d61b60137861c57a394b612b12ec73ef4bdc9a29cbb` |
| Postverifica indipendente della pubblicazione | `d7c9d0d6335bda667da0d15b219dc978b32b4ac7dd8dc0b81cff5fd7178ddf2f` |
| Copertura storica composta | `2d19bfd7116c87a5779d112e9add4dd50e25130668f64b84ed75a73c0f83ac90` |
| Verifica indipendente H56 e lettore con livelli separati | `e77285ceb2cfb57754d0b9383c971756746206ac5a1412f5dd99c3e3a0ac95f7` |

Le impronte identificano evidenze locali. Non affermano che gli archivi grezzi siano già caricati su GitHub.

## Gate ancora aperti

H58 conserva sette famiglie scientifiche incomplete e i gate finali Owner. Restano, secondo la loro portata: studio dei contratti residui, applicabilità fisica e incertezza nel dominio finale, confronto della proiezione di conoscenza finale, qualificazione delle decisioni IA e accettazione dei relativi criteri, inventario completo corrente/storico/virtuale, file finale e trasferimento integrale con recupero remoto.

I conteggi di file, schede, casi, blocchi o controlli CI non sono la percentuale della milestone. La pubblicazione di questa documentazione non attiva il portale, non modifica master o script installati e non riprende M27.

## Rendiconto v40 e recupero locale della prova Timer

Il rendiconto v40 riconcilia tutti i **4.920 requisiti e 14.521 criteri letterali** con H57 e con le righe effettivamente pubblicate in v600. Conserva separatamente gli hash dei record locali e pubblicati: le 1.623 integrazioni locali non vengono presentate come nuove pubblicazioni canoniche. I 239 ruoli documentali sono attestati solo nella loro portata documentale. Tutti i 19 criteri Owner restano non soddisfatti; sette famiglie e 25 assi restano incompleti, con zero chiusure scientifiche.

La verifica indipendente confronta le 4.920 impronte direttamente con la matrice v600, conserva i criteri e controlla i conteggi delle ricevute. SHA-256 del rendiconto: `8f49f96d32c1c86a592fa2123e643763add0ff47960ef2523af589dcebd91cdf`; della verifica: `00eb259efc0840b85ce7fe0738e7b774c7381d24e34b43bd320d0e9bd4ea13f7`.

La capsula `Prove-Timer-nativo-congelato-contatore-precisione-H-v1.zip` conserva 31 file sorgente e un manifest, inclusi preparazione storica, ricevuta nativa, discrepanze, console, chiusura normale e programmi di classificazione. I byte sono stati recuperati in una cartella isolata e il classificatore archiviato ha riprodotto esattamente i risultati: 20 controlli conformi, cinque discrepanti e due confronti di azzeramento non identificabili, separati dai 25 controlli.

| Evidenza locale | SHA-256 |
| --- | --- |
| Capsula Timer, 43.049 byte | `2749e6a9ac7d410d7f52b13b921d68bf1af57b648b0fb015e76b27189b297209` |
| Verifica di recupero e replay isolato | `518888e2fa7843574e1c2d0930b3a963ef3e8b341ec1aa69f7d6b208484140a7` |

Il replay legge soltanto i file recuperati e non avvia PixInsight, non consulta il registro corrente e non esegue chiamate API. È un recupero locale della prova, non una nuova esecuzione nativa, una calibrazione temporale o un recupero remoto da GitHub. Il contenuto completo della capsula non è caricato da questo aggiornamento documentale.

## H58: ponte nativo PSF, esiti non validi e recupero

H58 aggiunge tre schede e collegamenti a 27 requisiti, conservando tutti i record locali e pubblicati di H57. La verifica indipendente confronta tutte le 4.920 righe, le 180 schede precedenti e le query del lettore: le schede correnti sono 183. Registro, conoscenza registrata v1.171 e matrice pubblicata v600 restano distinti; nessuna v1.172 o conoscenza finale è attestata.

La prova usa gli stessi **216 ritagli sintetici già valutati dall’ottimizzatore Python**, ricostruiti con identità esatta dei pixel Float64. Gaussiane e Moffat con beta 2,4 e 5,2 sono provate con due larghezze. Ogni campo riceve otto richieste native: Gaussian e Moffat circolari, due rettangoli richiesti e due punti iniziali. Queste varianti sono appaiate sullo stesso campo; non sono nuove acquisizioni indipendenti. L’ottimizzatore Python della molteplicità non è stato portato nativamente.

Il primo tentativo conserva **120 campi e 960 chiamate**, poi fallisce con errore Win32 32 durante una riscrittura della ricevuta. Il monitor leggeva periodicamente lo stesso file mutabile: questo meccanismo va evitato, ma non è provato come causa esclusiva e non sono esclusi altri partecipanti alla condivisione. Non si attribuisce il guasto all’hardware.

Il recupero congelato esegue soltanto i **96 campi e 768 chiamate residui**. Usa nomi distinti scritti una sola volta per checkpoint e avanzamento; scrive la ricevuta finale una volta e solo dopo crea un marcatore separato. Il monitor legge la ricevuta dopo il marcatore. Le due istanze sono chiuse normalmente, con uscita effettiva zero. **Il primo script resta fallito**; il risultato completo è una composizione esplicita di due epoche, senza ripetere il prefisso.

| Esito circoscritto | Conteggio e denominatore |
| --- | --- |
| Profili nativi finiti confrontabili | 1.310 su 1.728 slot previsti |
| Fit nativi non validi | 418 su 1.728; stato 0, «Not fitted», causa del solver non stabilita |
| Slot di sorgenti isolate | 576 previsti: 472 confrontabili e 104 non validi |
| Posizione negli isolati confrontabili | 468 entro e quattro oltre il 5% della FWHM iniziale |
| Flusso totale analitico del modello negli isolati confrontabili | 299 entro e 173 oltre il 5% |
| Entrambe le soglie negli isolati confrontabili | 299 su 472, senza eliminare i 104 invalidi dai 576 previsti |

I conteggi condizionali non stimano un tasso generale di successo. Un `PSF.isValid` vero non qualifica fotometria o astrometria. Volume infinito del modello, `flux` nativo, `signal`, somme su pixel selezionati e energia in un disco continuo restano quantità distinte. Un singolo profilo adattato a una coppia di sorgenti è un controllo di stress, non un recupero fotometrico delle due componenti.

In tutti i 1.310 fit validi, `b0` differisce dall’angolo del rettangolo passato alla chiamata. La guida installata lo descrive come angolo della regione di campionamento. Non si usa quindi `b0` come attestazione della regione interna effettivamente impiegata: causa nel binding, correttezza della descrizione e regione interna restano da stabilire. Le formule scalari di FWHM e volume, dove definite, coincidono invece con i riferimenti nei casi confrontati.

| Evidenza locale | SHA-256 |
| --- | --- |
| Rapporto composito dei due segmenti | `c0370e353a2073fcc5e76daa525f6aa065f5351f7b934c30a19e6b62fb86a2c7` |
| Verifica indipendente dei due segmenti e delle soglie | `71a667c05ae45cfbc1c0d100a2bc50656ac4ac63bd74b835b17e4b7023a55701` |
| Verifica indipendente H58 e lettore | `94788b8c392f98c3336ddcc7bde59def7085c530f2301869ac36591bb775ba31` |

La costruzione iniziale H58 si è fermata prima di creare il file, per una chiave di percorso con separatori diversi da quelli della mappa Windows congelata. Sorgente ed errata restano conservati; la revisione corretta usa la chiave nativa e ha superato i confronti completi. Nessuna prova nativa è stata ripetuta per correggere questo errore documentale.

Le tre schede sono `PSF_NATIVE_CIRCULAR_SAME216_TWO_EPOCHS_SCOPED_MEASUREMENTS`, `PSF_NATIVE_RECEIPT_SHARING_FAILURE_AND_EXACT_SUFFIX96_RECOVERY` e `PSF_NATIVE_B0_DIFFERS_FROM_REQUESTED_REGION_CORNER`. Questa prova non esegue convoluzione, denoise o restauro e non chiude i residui di profilo, campionamento, incertezza, dominio fisico o decisione IA. Sette famiglie scientifiche restano incomplete, con zero chiusure. I byte grezzi sono conservati su H e non sono trasferiti da questo aggiornamento documentale.


## Riconciliazione dei criteri PSF — H59 (13 novembre 2026)

La conoscenza provvisoria H59 conserva i 4.920 requisiti, le 183 schede H58 e lo snapshot autorevole v600; aggiunge quattro schede di riconciliazione (187 totali). SHA256 del file: `0b943fd3eaf488f1cb812a61081a16bafffa8907e707983e1c480f9ea603de22`. Il confronto indipendente preserva integralmente le righe, salvo quattro collegamenti aggiunti ai soli requisiti PSF e fitSource. Verifica: `36b3301b208ead702aa3c733fc57d6a7cef9001225b014c77c4a70d81d2f1d25`. Lettore `consult_provisional_dsg_knowledge_h_v5_v11.py`, SHA256 `54a62bacd95c00d6f65d46576614834df91b7f69e105b1c2cc95d15233077e8f`: audit e consultazioni PSF/asse4 eseguiti. File e prove restano nell’archivio di lavoro su H:; questa documentazione non ne attesta il trasferimento integrale remoto.

La campagna spaziale/cromatica già completata copre sei categorie di misura su 28.874 campi RGB e 5.543.808 chiamate native. La ricostruzione gaussiana integrata usa un operatore analitico dichiarato: il criterio originale lo permette; non si introduce come prerequisito un’esecuzione di Image.convolve. Restano i limiti del modello circolare e del catalogo noto. Il modulo non restituisce una frazione cumulativa esplicita di energia racchiusa: questo limite del modulo non significa assenza nell’intero corpus.

La campagna di confusione contiene già frazioni discrete di energia racchiusa a raggi di una e due FWHM. Riconciliate 72.000 misure scalari su 5.000 campi, riprodotti tutti i riepiloghi di cella e i conteggi della verifica precedente. I 4.000 campi con coppie soddisfano il criterio dell’energia racchiusa nel modello a larghezza gaussiana nota; 3.513 soddisfano anche posizione e flusso totale congiuntamente. I restanti 1.000 campi sono isolati. Due aperture condividono gli stessi campi: non raddoppiano il campione indipendente. È una valutazione a posteriori con numero di componenti noto, non validazione generale o rilevamento cieco.

Sui 216 ritagli Gaussian/Moffat sono state riconciliate 432 decisioni di molteplicità conservate. Il ramo con profilo stimato presenta due sovrasegmentazioni su 72 stelle isolate; tutte le 144 coppie hanno numero corretto, ma 113 superano congiuntamente le soglie di flusso e posizione. Il ramo con profilo noto conserva una sovrasegmentazione isolata e 115 coppie con esito congiunto favorevole. Questi conteggi non certificano completezza su un intero campo. I 418 fit nativi non validi del ponte separato non equivalgono a 418 sorgenti astronomiche mancate.

Il limite del 5% sull’errore relativo non equivale a una soglia 0,05 sul valore assoluto del logaritmo del rapporto. Per quest’ultimo, valori fino a ln(1,05)=0,04879016416943204 sono sicuramente entro il limite; sopra -ln(0,95)=0,05129329438755058 sono fuori. Nell’intervallo intermedio serve il segno o il rapporto originale per una classificazione esatta. È una traduzione matematica, non una nuova misura empirica né un cambiamento della soglia Owner.

Report locali: `psf-original-axis-latest-evidence-reconciliation-h-v1/report.json` (SHA256 `2d8f2468c78ff249698f97d4a681bc9e1f08bf33ca39e7e9413dcd66bd626516`); `psf-spatial-frozen-endpoint-contract-audit-h-v1/report.json` (`ea8b73dd0532c6e15171927a3d47b572ca1cade6d87cab003d50cadf1acabcac`); `psf-existing-encircled-energy-reconciliation-h-v1/report.json` (`26c5e0a25bfe362f9771fc8ea282f515a22bbb211b7847dc048c083c44d71d1a`); `psf-multiplicity-failure-denominator-reconciliation-h-v1/report.json` (`0334cb3a688a7f824c8a9703150aabf0c0a247a9519b8e37883d8f4177033879`).

Nessuna nuova chiamata nativa o realizzazione di rumore, nessuna chiusura scientifica, nessuna versione registrata 1.172. Restano aperti i sette domini scientifici, i criteri Owner, la conoscenza finale e l’archivio completo su GitHub con recupero indipendente. Le azioni storiche che chiedevano di avviare campagne ora concluse non autorizzano ripetizioni.


## Campagna completa del flusso di modello — H60

H60 conserva i4.920 requisiti e tutte le187schede H59, aggiungendo due schede (189totali). SHA256 conoscenza `a2a407cda2fee212ed3e4e27ce8af060d8ce607c90407dd17c2761fb1b8585d4`; verifica strutturale e audit dell’autorità600 `f40a44d2537d7ec97745a11a66fcaaff7d48f88df7c813286459be2526f68cc9`. Lettore `consult_provisional_dsg_knowledge_h_v5_v12.py`, SHA256 `92813bc67807ea87c19a623f772b061ff81610342f657e66b28eb969d167f662`: audit, scheda completa del flusso e requisito volume consultati con esito positivo. Rendiconto v42: SHA256 `b502c5e56eb480cb93af0c44c5e8151e15cd9982bfd5cf7a42835a0328aa5c74`, preservati14.521criteri letterali; aggiunti solo collegamenti alle evidenze in tre righe PSF.

L’intera campagna conservata di28.874campi RGB e5.543.808slot nativi è stata ricontata dai parametri originali, verificandone le impronte contro le ricevute dei lotti. Il confronto usa aritmetica esatta sul parametro binary64 del volume gaussiano moltiplicato per65536 e sul flusso del componente simulato10000:5.064.768slot entro5%,479.040oltre, zero invalidi in questa specifica campagna. In14.239campi tutte le192configurazioni rispettano la soglia di flusso. Non sono192acquisizioni indipendenti per campo. Nessun nuovo fit o rumore generato; nessun dato originale modificato.

Verifica indipendente con aritmetica razionale su tutti5.543.808valori esportati, tutti384riepiloghi marginali e28.874riepiloghi di campo; concordano anche tutti15.621casi precedentemente ambigui nel valore assoluto del logaritmo. Questi ultimi si risolvono in14.145entro e1.476oltre il5%. La verifica indipendente eredita dal produttore la provenienza delle letture native: non è una seconda lettura completa dei file nativi.

Gli esiti dipendono dalla configurazione. Per Quattro760, regione r12:8marginali al primo punto iniziale e6al secondo sono oltre soglia in tutti14.437campi. Con r8 non ci sono marginali interamente oltre soglia. In C8_1260 nessuno dei quattro gruppi regione/punto ha marginali interamente oltre. Il confronto appaiato conserva anche esiti favorevoli solo a r12 e insuccessi di entrambe le regioni: non legittima una scelta universale r8 né una politica selezionata dopo aver visto i risultati. Causa del comportamento, regione interna effettiva e identità del binding compilato non sono stabilite.

Per i384indicatori fissi entro/fuori soglia è derivato separatamente un limite di precisione delle frequenze condizionale al modello IID originale: Hoeffding bilaterale e unione, n=14437,epsilon=0,02, limite superiore di probabilità di fallimento della famiglia0,007403441888403216. Non richiede indipendenza fra indicatori dello stesso campo; non dimostra indipendenza fisica dei flussi pseudocasuali. Non è ereditato dalla CDF dell’errore logaritmico, non è una soglia Owner sul rischio di errore e non ammette una politica scelta a posteriori.

Evidenze locali H: `psf-all-native-gaussian-flux-relative5-recount-h-v1/report.json` SHA256 `078040e87da4a86b8f6dc0825c55f90bd6858c67a05ab2c96f8d8900d641c43c`; verifica razionale `16095f7e3f96c2a8a53e368311852e35dbe0b4d52a1b50631b1896d81d4d4667`; tabella volumi/validità `0a12d1834b063b96d519ecab68c6e5f5ab8750050e3a5fa61d8f1f701b1fe8ac`; analisi configurazioni `9944a916c82883ec3958af1abf0f06f8532f886704b40376462a6df09598a363`.

Questa è fotometria del volume del modello gaussiano rispetto al generatore: non misura automaticamente flusso di apertura, energia racchiusa, incertezza del riferimento misurato, risposta della camera o validazione del workflow. Zero nuove chiusure scientifiche; sette famiglie/25assi e19criteri Owner restano aperti. File finale e trasferimento completo degli archivi con recupero remoto non attestati. I sette controlli riusciti del precedente commit40d6eeb restano evidenza di quel commit; verificare separatamente quelli del nuovo aggiornamento.


## Conoscenza H61 e confronto pesato in corso

H61 conserva i4.920requisiti, lo snapshot pubblicato600 e tutte le189schede H60; aggiunge due riconciliazioni CFA (191schede). SHA256 conoscenza `8b3c24a564c8c7947dc68e1ea3e38e86839a334123e8d34a05a44dde28bd9bda`; verifica `849beeacd0f9ac0e9af6470ed59c756e2c224c055d905ea9b16d0f5658d08e54`. Lettore `consult_provisional_dsg_knowledge_h_v5_v13.py`, SHA256 `c1e4b54ac5761aaa2012e0cb48208b1ecee5e452ec1a6a06da70e2618670ee68`: audit e consultazioni di asse3 e DrizzleIntegration riusciti. Rendiconto v43 SHA256 `9637d9a6cbe358631c2745c41377848a3fb7fa3693b02f3e75833ca7ed11979d`:14.521criteri letterali conservati, soltanto collegamenti aggiunti a Debayer e DrizzleIntegration.

La riconciliazione CFA conserva840contratti tecnici Debayer e280casi VNG il cui flag storico indicava che il riferimento indipendente non era allora disponibile. La successiva verifica dei riferimenti numerici resta una diversa epoca di evidenza: quel flag non significa assenza permanente del riferimento. Nei6.144campi VNG conservati (1.536perpattern),6.129sono entro5% su entrambi i rapporti con la verità sintetica,6oltre soltanto sul rosso e9soltanto sul blu. I16record interessati comprendono anche un caso fuori limite solo rispetto al riferimento diagnostico senza rumore: non si confondono le due basi di confronto. L’inversione iniziale degli assi della matrice nella nuova riconciliazione è stata intercettata prima dell’output e corretta in una versione separata; sorgenti e fallimento conservati.

Sono già disponibili5.180esecuzioni native per20matrici complete di risposta Square (MONO e quattro pattern Bayer, scale1/2 e due larghezze), con256colonne di base, baseline e due controlli deterministici per geometria. Tutti20file matrice sono stati ricontrollati. Le proiezioni Gram condizionali non costituiscono covarianza stocastica empiricamente validata né linearità universale. Queste prove non vengono ripetute come nuovo baseline.

Il nuovo disegno pesato congela quattro profili di pesi strettamente positivi, incluso uno differente per canale, sulle20geometrie:80gruppi e20.720casi pianificati. Cambia l’operatore `enableImageWeighting=true`; rigetto, spline e normalizzazioni locali/adattive restano esclusi da questo confronto e aperti nel dominio originale. Il riferimento razionale ha superato140.992controlli; un secondo calcolo dalle intersezioni geometriche ricostruisce tutte25.344righe supportate e verifica la rinumerazione delle esposizioni. Differenza massima dei coefficienti per la sola rappresentazione binaria delle fasi:6,68063635763649e-17.

Preparazione completata e verificata indipendentemente:20.720casi,82.880nuovi sidecar e269file di pixel di origine;20.989file originali ricontrollati prima della preparazione. Nessun originale modificato. Gestione nativa verificata con11prove simulate di flusso/guasto; controllo dell’avvio con12prove simulate su marcatori e assenza di riavvio. Queste sono qualificazioni operative, non test scientifici nativi. Ricevute distinte per caso e chiusura, campioni e History persistiti prima della chiusura, viste di errore salvate o conservate, finestre sconosciute non toccate. Un solo processo avviato; nessun riavvio automatico. SHA256 del sigillo: `1d0e32b398c1d3c909b53e379e6cdbedb61c674a1f30f560dfb65cde442a3bb1`.

La campagna è **in corso**. Nell’osservazione archiviata risultano704casi osservati, con ricevute e cleanup corrispondenti, zero errori operativi registrati. Questo conteggio descrive quell’osservazione, non lo stato attuale permanente né un esito scientifico finale. Sono ridotti e verificati indipendentemente soltanto i primi due gruppi uniformi MONO a scala1 (259casi ciascuno):32.768coefficienti di base,1.056endpoint di covarianza e12confronti di varianza d’apertura. Le risposte rispettano la tolleranza tecnica originale1e-6. Nel modello di input indipendente a varianza unitaria, la varianza completa dell’apertura è circa1,30 e1,44volte la stima diagonale. Sono proiezioni condizionali dell’operatore finito; non misure del rumore reale e non evidenza di successo dei profili non uniformi o degli altri78gruppi.

Il protocollo di implementazione della riduzione dichiara esplicitamente di essere stato scritto dopo l’avvio (448casi nell’osservazione), derivando dagli endpoint e dal riferimento congelati prima del dispatch. Prima di allora era stato ispezionato soltanto il primo controllo uniforme di64pixel. Non si attribuisce retroattivamente una data precedente a tutto il codice di analisi. Aperture con pixel senza supporto restano senza stima; nessuna matrice ricavata soltanto da casi favorevoli. In questo banco di base/checkerboard non viene inventata una FWHM stellare per dichiarare soddisfatto il requisito di posizione.

Riferimenti locali: riconciliazione pattern/colore `62975546ed555dc33db25b2d98c0ae408a0083266fd2bfb99f74a21dc2d698e2`; copertura/registrazione/pesi `b3659e4dc67d234edb7bf2516c8f8d985ec445c890cc3996cb6efbe3a8a693f4`; banco completo precedente `f4909475eebf36265da81a21d4c03de0f19ec5a8b0be1fe9a81fc52639ca99b0`; protocollo nuovo `6a04a506a0006957d00eaaf8fa4cead960e5e28152e8608f941d4f6e821af416`; verifica geometrica `e7255e928591e3fc2b6cdfd08c096305311877940d9dfd7b377a7c11d019a3ff`; verifica input `6b0557d3455d703477697548cb3b8e8982caf779fd92e665afbd5973b200e097`; riduzione `55e05f28f09bf673d7cab5b2392f958a822a10caea31f07c433badf0d4b85972`. Prove indipendenti dei due gruppi: `65b66d418f69e75492b1e4006170a68b57dcf69bf16b5cf22503c682f76c76e0` e `a1bb6e5c17344b014983e51c0e7685258f3be1ae70b8000fdf6c7ce1df603724`.

Zero chiusure scientifiche; sette famiglie/25assi e19criteri Owner restano aperti. Conoscenza finale e trasferimento integrale degli archivi con recupero remoto non attestati. Nessuna attivazione del portale, modifica a master/script PixInsight installati o ripresa M27.
