# Conoscenza dello studio PixInsight e IA: struttura, consultazione e storico

## Stato corrente: H84 provvisoria e rendiconto v66

La conoscenza corrente è **H84, provvisoria**, con **239 schede**, lettore v36 e **46 controlli CLI riusciti**. Conservati 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner; autorità **v600 / 1.171** invariata. Sette famiglie e 25 assi restano aperti, **zero chiusure scientifiche**. Le sezioni successive conservano lo storico.

| Artefatto locale su H: | SHA256 |
| --- | --- |
| Conoscenza H84 | `f9b2ca6b320b231252c98d535ab0120e4866f3be4377311f9a9b2d5b95ab34a5` |
| Lettore v36 | `f144b813f96181d07d924f60200435755891b1bb7333052795700ab78d487137` |
| Qualificazione CLI H84 | `b8c51579f890cbc62927e538b51a639c0abec8a3b311592567bb0e67a7b55ba7` |
| Rendiconto v66 | `e15b5ac6b0d00dd89cb8ddae6d4aff8875780a72d18c61cd679f838f3e057925` |

### Errore osservato e lettura XISF con segno

Sul primo file monocromatico della prova, la chiamata predefinita `ImageWindow.open(path)`, con fixture Float64 e metadato bounds 0:1, ha portato **quattro valori negativi a zero**; gli altri 60 sono rimasti identici. Il controllo ha fermato la prova, conservando input, piani binari letti, History e ricevuta di errore.

La [sorgente ufficiale del modulo XISF](https://gitlab.com/pixinsight/PCL/-/raw/master/src/modules/file-formats/XISF/XISFInstance.cpp) documenta il read hint `no-normalize` e la sua applicazione all'opzione di lettura. La sorgente è stata congelata localmente con SHA256; non si assume equivalenza completa tra sorgente pubblica e binario installato.

Il confronto nativo sul medesimo file, cambiando il solo hint in `ImageWindow.open(path, "", "no-normalize")`, conserva esattamente tutti i 64 valori, inclusi i quattro negativi. La successiva prova comprende soltanto i 25 file mai aperti: **1.600 valori e 140 negativi identici agli input**. L'identità del percorso del modulo XISF caricato e l'hash del relativo file su disco sono attestati prima di quest'ultima prova; non è un confronto delle pagine rilocate in memoria.

Il gruppo completo comprende **27 file distinti, 1.856 valori e 144 negativi conservati**: 26 file mono letti con no-normalize e un sentinella RGB positivo verificato con la lettura predefinita. Il file RGB concluso non è stato riaperto. Le letture native complessive sono 28 perché il caso monocromatico alterato è stato confrontato sotto due condizioni diverse.

Resta conservato anche il primo arresto del controllo di identità: PixInsight restituisce wrapper distinti della medesima vista. Prima di chiuderla sono stati verificati percorso, identificatore nativo, pixel e History; i controlli successivi usano tali identità stabili. Tutte le istanze possedute sono uscite normalmente. Nessun master o script installato modificato.

Questa prova circoscritta dimostra il trasporto dei pixel delle fixture; non dimostra il percorso interno di lettura di Drizzle, ogni formato, file grandi futuri o validazione fisica. Prima di estendere il riscontro alle campagne storiche occorre verificarne gli effettivi intervalli dei pixel e gli hint conservati.

### Esecuzione attuale del decoder e prossimi controlli Drizzle

Su H: sono stati ricontrollati **2.462 file numerici**, senza differenze dall'inventario storico, prima degli import. Con le parole deterministiche già archiviate, il decoder riproduce gli stessi quantili su **132.452 target**; sei fallback iniettati coincidono con l'oracolo scalare e quattro stream invalidi sono rifiutati. Le operazioni Float64 separate producono **529.808 valori** entro i margini esatti dichiarati. Nessuna nuova parola casuale e nessuna prova di legge CNG ideale o di indipendenza fisica.

Sono congelati **quattro controlli Drizzle non ancora eseguiti**: due coppie mono/RGGB con identici ingressi firmati, geometria e pesi, distinguendo hint predefinito e no-normalize. Le previsioni includono lettura firmata, clipping dell'ingresso e clipping dell'uscita. Verifica indipendente della geometria: **1.472 righe supportate, 576 senza stima**. Il configuratore supera 44 contratti simulati; il dispatcher 27, inclusi salvataggio prima della chiusura, stop al confine salvato, ricevute fallite e viste trattenute. Questi controlli simulati non sono chiamate native né validazione scientifica.

Il gate comune R4 ha ora approvazioni ARB e RQ verificate sul manifest SHA256 `3507d07d0e6ceac970644447971b64c479970a80c48777dfd9da5263b1b2c37e`; include BKL-046, BKL-049 e BKL-051 sulla stessa prenotazione. L'integrazione nei nostri nuovi piani resta da qualificare e revisionare prima del rilascio. L'osservazione di coordinamento incorporata in H84 precede queste approvazioni e resta storica; una ricevuta separata su H: attesta lo stato successivo. Gli avvii passati e i piani congelati restano intatti; il lavoro offline continua.

### Conservazione e limiti di consegna

- Capsula delle letture native: **981 file, 664.555 byte**, SHA256 `7f191acd19648308608f80e07e539d1d8c038c1d56b06e063eeb46db20391450`. Estrazione/hash verificati e audit di tutti i pixel riprodotto identico, rebasing esplicito dei percorsi storici verso i file estratti.
- Capsula H84: **134 file, 11.424.080 byte**, SHA256 `e7f87c92e02370c892a58a9f520001b3950713b36a4a291c377075774ad4aa9b`. Estrazione/hash verificati e audit del lettore identico.
- Archivi e lavoro di questa chat restano sotto `H:/Codex/Produzione/2026-10-13/Digital-StarGate-PixInsight`. Il registro autorevole su C: resta nel proprio percorso; i materiali degli altri progetti non sono spostati.
- Genitore H83, dipendenze storiche, sorgente terza e ambiente installato/licenziato restano separati. Le capsule attestano recuperi locali circoscritti, non un nuovo replay nativo o il recupero remoto integrale GitHub.
- Restano aperti i quattro controlli Drizzle, la campagna del rumore con il suo intero margine numerico e statistico, le altre famiglie scientifiche, il criterio IA, il file finale e il trasferimento integrale con ricostruzione dei byte remoti. Nessun merge, deploy o attivazione del portale.

## Stato storico: H83 provvisoria e rendiconto v65

La conoscenza corrente è **H83, provvisoria**, con **237 schede**, lettore v35 e **44 controlli CLI riusciti**. Conservati tutti i 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner. Autorità invariata: **v600 / 1.171**. Le sezioni successive documentano stati storici: sette famiglie e 25 assi restano aperti, zero chiusure scientifiche.

| Artefatto locale su H: | SHA256 |
| --- | --- |
| `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v83.json` | `fde27abdd69abe9840e85eafca9eec5634b9c2ab2a54debe167ce4fce7fbc11f` |
| `consult_provisional_dsg_knowledge_h_v5_v35.py` | `589445cb743fa93d9f87f803afbe1cb95fd12aa5bcb33e4a87aef0b72e6f97ad` |
| Qualificazione CLI H83 | `c3c57ee1efca19220d05407e32422c3a487333d9debc5ac4ccee54ba7461261e` |
| Rendiconto v65 | `ed416af0dd29083fcdcb74021adfa7f93498c9f82dd827122972762252dc3858` |

### Dominio del rumore e riuso delle esecuzioni

Il manifest completo conserva i 376 osservabili originari e tutte le quattro classi PIXEL, PAIR_MEAN, PAIR_DIFFERENCE e RECTANGLE_MEAN. Comprende 280 configurazioni logiche, **2.632 endpoint supportati** e **280 selettori senza stima**, senza sostituzioni adattive. Verifica indipendente: 2.256 nuovi coefficienti ricostruiti dai selettori e 71.680 varianze sorgente controllate.

Le fixture deterministiche con valori anche negativi producono 260 pacchetti distinti; la rilettura XML/XISF verifica 71.680 valori logici. I 20 possibili riusi sono una partizione delle fixture, **non identità già qualificata degli ingressi futuri e dei parametri nativi**. Prima di condividere un'esecuzione occorrono identità effettiva dei file e controllo dei valori letti dal processo installato.

### Copertura condizionale e margine numerico

Per l'intera famiglia K=2.632, N=131.072 repliche per endpoint è sufficiente secondo il certificato gaussiano ideale a media nota; il limite simultaneo conservativo è circa 7,064×10^-6. Una verifica indipendente con diverso parametro MGF e arrotondamenti diretti conferma la sufficienza. N=65.536 non soddisfa questo particolare certificato completo; non si dimostra che N=131.072 sia minimo né si garantisce potenza o accettazione al 5%.

La proposta corrisponde a due banchi di 65.536 tile e, soltanto se tutte le qualifiche sono soddisfatte, 520 chiamate native. Le 344.981.504 osservazioni scalari logiche condividono **33.554.432 variabili gaussiane unitarie**: non sono test indipendenti né acquisizioni fisiche.

Il collegamento tra parole discrete e gaussiane continue è dimostrato **condizionatamente a parole ideali uniformi e indipendenti**, con 345 fixture algebriche esatte. L'esclusione simultanea delle code estreme aggiunge un limite 2^-54. Questo non prova che Windows CNG abbia quella legge: resta un'ipotesi esplicita del modello.

Per i 2.632 endpoint il margine condizionale complessivo della sorgente è inferiore a 2,13×10^-12 della deviazione standard di riferimento. Comprende trasporto del quantile e costruzione Float64 specificata con moltiplicazione e somma separate. Verifica esatta indipendente per tutti gli endpoint. **Non comprende errore nativo PixInsight, qualificazione effettiva del generatore, lettura nativa degli ingressi con segno o legge della varianza della popolazione in uscita**. Nessun nuovo campione casuale o processo nativo è stato avviato per questi certificati. Il criterio IA 1%/95% è distinto.

### Recupero locale e attività ancora aperte

- Capsula delle evidenze sorgente: 528 file, 2.475.349 byte, SHA256 `17c3145a6d4b8ac877ce4e116eab73fa70552324a82403181002e46424d7f0d7`. Estrazione e hash verificati; il controllo dei margini ricostruisce la ricevuta identica.
- Capsula H83: 117 file, 13.736.493 byte, SHA256 `7fbd885591f8786bcb14c752fcc8aa570d1992695e0bd674199faed828e7a3b8`. Estrazione e hash verificati; audit del lettore recuperato identico.
- Gli archivi restano sotto `H:/Codex/Produzione/2026-10-13/Digital-StarGate-PixInsight/work`; genitore H82, dipendenze storiche e ambiente installato/licenziato rimangono separati. Recupero locale circoscritto, non replay nativo completo né recupero remoto GitHub.
- Prima di nuovi campioni: qualificare decoder/guard e ambiente effettivi, operazioni Float64 e lettura nativa con segno, identità delle configurazioni condivise e ambito dell'inferenza/errore nativo.
- File di conoscenza finale, validazione scientifica dell'intero dominio, criterio decisionale IA e trasferimento integrale con recupero remoto degli archivi restano aperti. Nessun merge, deploy o attivazione del portale.

## Stato storico: H76 provvisoria e rendiconto v58

La conoscenza corrente è **H76, provvisoria**, con **221 schede**, 4.920 requisiti, 14.521 criteri letterali e 19 criteri dell'Owner. Conserva integralmente le 219 schede H75. L'autorità registrata resta **v600 / 1.171**; sette famiglie e 25 assi incompleti, **zero chiusure scientifiche**.

| Componente corrente | Identità |
| --- | --- |
| Conoscenza H76 | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v76.json` |
| SHA256 conoscenza | `92bb40df598e9ac37e61ed11e78a595161e5c258b60a12def1fea18ce8ed591a` |
| Lettore v28 | `consult_provisional_dsg_knowledge_h_v5_v28.py` |
| SHA256 lettore | `489067d9f869202382287e17db509794416b120ee91d4d17a4e5bcd4d060adf7` |
| Qualificazione CLI | 28 controlli riusciti; ricevuta `3aff43044330434a0e2c0a93e0b94bf44d99529a2f78d3d3c98565d95d241442` |
| Rendiconto v58 | SHA256 `ffeb78489af42461a7f0c12ac982781084b90318fd0f6c0b11fbbbed031f5f25` |
| Drizzle chiuso alla sessione 022 | 18.118 casi unici verificati / 20.720; 2.602 pendenti |
| Gruppi e archivi | 69 gruppi completi / 17.871 casi in 21 capsule; altri 247 casi conclusi in gruppi parziali |

L'**87,4% riguarda soltanto la campagna finita Drizzle**, non l'intera milestone. La sessione 023 e le eventuali successive restano escluse da questo snapshot. Le sezioni precedenti conservate sono storiche. Conoscenza finale e trasferimento integrale con recupero remoto dei byte restano aperti: questa pagina documenta gli artefatti ma non li carica. La consultazione non autorizza nuove esecuzioni.

## Snapshot storico iniziale: H66

Questo riferimento descrive la conoscenza consolidata **provvisoria H66** dello studio BKL-046. Il suo formato rende consultabili risultati, condizioni, errori ed evidenze; non costituisce un'autorizzazione a eseguire processi PixInsight né una baseline scientifica finale.

Snapshot del 14 novembre 2026 (le sezioni successive conservano anche gli stati storici):

| Componente | Identità |
| --- | --- |
| File di conoscenza | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v66.json` |
| SHA-256 del file | `6986087d5f6096bdb2f3a250a54a8035d5f00ed274da02bce40a13a0860e2319` |
| Lettore | `consult_provisional_dsg_knowledge_h_v5_v18.py` |
| SHA-256 del lettore | `e921152787ed5e2c2e6741ae6b03a4d7de952980df852e3fb3f5308d625e8fa6` |
| Formato | `schemaVersion: 1` |
| Stato | `PROVISIONAL_CONSOLIDATED_QUERYABLE_NO_SCIENTIFIC_PROMOTION` |
| Requisiti | 4.920 |
| Schede di evidenza | 201 |
| Famiglie / assi / criteri Owner | 7 / 25 / 19 |
| Chiusure scientifiche | 0 |

Il registro autorevole preesistente, attestato alla versione v1.171, resta distinto da H64. Una versione provvisoria non aggiorna quel registro e non riavvia il publisher. Tutti i vincoli su portale, master, installazione, migrazione Codex e M27 restano applicabili.

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
python consult_provisional_dsg_knowledge_h_v5_v16.py --audit
python consult_provisional_dsg_knowledge_h_v5_v16.py --workflow process:ACDNR
python consult_provisional_dsg_knowledge_h_v5_v16.py --role pjsr_object:File
python consult_provisional_dsg_knowledge_h_v5_v16.py --workflow pjsr_object:File
```

Il lettore predefinito verifica l'impronta esatta di H64 prima della consultazione. Per un altro file occorre fornire esplicitamente `--file` e `--sha256`; l'impronta di una versione diversa non è accettata.

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


## H62: otto gruppi verificati, sospensione e ripresa esatta

H62 conserva tutti i 4.920 requisiti e le 191 schede H61; aggiunge una scheda circoscritta, per 192 totali. Il lettore v14 ha superato audit, query della scheda, requisito DrizzleIntegration e asse CFA/3; un'impronta errata viene respinta. Lo snapshot autorevole resta v600 e la conoscenza registrata v1.171: nessuna v1.172 o conoscenza finale attestata.

Su richiesta Owner, la prima istanza è stata fermata e chiusa normalmente, senza viste residue. Sono conservati 2.235 casi conclusi e 133 tentativi interrotti; 18.352 casi non erano ancora avviati. I tentativi interrotti non sono classificati come fallimenti scientifici. Il comando di interruzione nativo era intercettato dal ciclo: un blocco intenzionale del successivo percorso di checkpoint ha attivato il gestore d'errore soltanto dopo la ricevuta del caso e la chiusura delle viste. La directory di blocco resta documentata; la ricevuta originale conserva lo stato di errore, senza trasformarlo in successo.

Otto gruppi uniformi completi, 2.072 casi, sono stati ridotti e verificati: 655.360 coefficienti, 21.888 endpoint di covarianza condizionale e 66 confronti di apertura supportati. Una verifica iniziale supera la tolleranza assoluta numerica 1e-14: differenza 1,4210854715202004e-14 su una varianza di circa 60,25. Il fallimento resta conservato. Un successivo calcolo razionale ricostruisce esattamente i residui di conversione, somme e prodotti; un protocollo distinto deriva limiti conservativi e controlla 18.948 somme e 1.035.648 prodotti delle valutazioni finite. Il controllo revisionato conserva gli altri criteri e usa i limiti numerici qualificati solo per le aperture. Non cambia il limite scientifico Owner del 5% e non prova universalmente il comportamento delle somme su ogni piattaforma.

L'archivio locale degli otto gruppi contiene 4.200 file sorgente e il manifest; ogni membro è stato ricontrollato per dimensione e SHA256, insieme alla stabilità delle fonti. SHA256 ZIP: `e0278da0266cfc2f376e6e5ad302ec6bd6913c009f8fd49db2a6ee3b88d2d6cb`. Restano dipendenze esterne conservate su H: non è un ambiente di replay scientifico autonomo né un recupero remoto.

La ripresa congela esattamente 18.485 casi, escludendo tutti i 2.235 conclusi. Sono stati riletti 73.940 sidecar e 269 input originali. La nuova versione del worker supera 16 prove simulate, incluse esclusione dei casi conclusi, duplicati, omissioni, pin alterati e arresto dopo il primo caso fallito; l'host supera 12 prove simulate su ricevute immutabili e assenza di retry automatici. La nuova istanza separata è stata osservata viva con checkpoint di 64 casi, 64 osservati e zero fallimenti operativi. Questo è uno snapshot storico di avanzamento, non il totale corrente o l'esito finale.

| Identità locale | SHA256 |
| --- | --- |
| Conoscenza H62 | `abc86a6c7dae381c61c36c698eed0753296e2ac5bd7ce821e672abc1c7e2f53b` |
| Lettore v14 | `a8aeff415833bc335964d2798479dcced1a166833ffd57d24653ba11bd1fca28` |
| Piano esatto di ripresa | `364913e61959f941d7352e17c691b077e8b3b8067778e0d1bcd2da809eddba96` |
| Sigillo di ripresa | `bb14b27183e83a27811cbcdbd57e86012524d0474a5949f3badb3336379ee03b` |
| Qualificazione dei limiti numerici | `fe55f4793fac42a03f3bf6f5d792c289559bb4cb7a4a01aa2aba40977300e57d` |

Tutti i sette controlli CI del precedente commit `825e78032bb2188ce24ec31470c1b5b7e126ff4a` sono conclusi con successo; non attestano quelli di questo nuovo aggiornamento. Questa pubblicazione riguarda documentazione tecnica: nessun merge, deploy, caricamento degli archivi grezzi o attivazione del portale. Sette famiglie e 25 assi restano incompleti, zero chiusure scientifiche; file finale, criteri Owner e trasferimento completo su GitHub con recupero indipendente restano aperti.


## H63: riesame dei fondi diffusi e classificazioni relative esatte

H63 conserva tutti i 4.920 requisiti e le 192 schede precedenti; aggiunge tre schede, per 195 totali. SHA256 conoscenza `9cfbbdf266028b55282f5847ccc39c14d457cae775dc4ae6ed201b7029e57ccc`; lettore v15 `d864c5e896388f50b0dcfee39a025e8552f17f5a56c0cdf3eeaaf3c3c5302027`. Audit, query ABE e asse diffuse/2 riusciti; impronta errata respinta. Il rendiconto v45 conserva 14.521 criteri letterali e tutti i 19 criteri Owner, aggiungendo soltanto collegamenti a tre requisiti. SHA256 rendiconto `c18894ae4e38d42a207ee0251987e4d303e5cfc5ffab1ccf524e0e15d394ff5a`. È precisata anche la provenienza del produttore: v44 aveva ereditato il pin precedente; v45 identifica il proprio programma salvato senza riscrivere i documenti storici.

Sono stati ricontrollati 22 intervalli condizionali di flusso già conservati e nove fonti storiche sui byte presenti su H, lasciando intatti i percorsi G storici. Per un flusso positivo compatibile con [L,U], esiste una sola stima entro il 5% per ogni verità compatibile se e solo se 19U ≤ 21L. Dieci intervalli soddisfano il criterio, dodici no. Il controesempio di due mondi con la stessa immagine richiede un errore relativo minimax di circa 8,038%: nessun successo del processo identifica automaticamente la decomposizione additiva/moltiplicativa. Le garanzie più strette richiedono le ipotesi dichiarate di calibrazione, linearità, cielo e apertura nota; non attestano una camera reale.

Il riesame dei 3.304 campi ABE held-out usa solo i flussi scalari originali, senza nuove chiamate native o estrazioni casuali. La classificazione relativa al 5% è **retrospettiva**, distinta dai 96 indicatori di ordinamento congelati originariamente. Sono mantenuti due gradi, due regioni e due estimandi sugli stessi campi: le varianti non sono acquisizioni indipendenti.

| Confronti sui flussi conservati | Entro 5% | Oltre 5% | Indefiniti: verità zero | Totale |
| --- | ---: | ---: | ---: | ---: |
| Varianti native ABE | 486 | 19.338 | 6.608 | 26.432 |
| Controllo non corretto con fondo vero noto all'analisi | 1.492 | 3.464 | 1.652 | 6.608 |

Le 10.818 stime native negative sono un sottoinsieme sovrapposto alle classificazioni, non un denominatore aggiuntivo. La prima versione del nuovo conteggio si era fermata prima dell'output perché assumeva flusso positivo in ogni regione; i profili compatti hanno invece regioni a flusso esattamente zero. La versione separata conserva tali casi come indefiniti. Una verifica indipendente con prodotti interi controlla tutte le 33.040 classificazioni e tutti i conteggi. Il controllo non corretto dispone del fondo vero del generatore: non è un estimatore operativo disponibile su una foto reale. Nessuna politica di scelta dei gradi viene validata selezionando i risultati favorevoli dopo averli osservati.

Il riesame non misura nuovamente morfologia, appartenenza dei pixel ai campioni, perdita di segnale nel modello o incertezza al bordo. Questi restano requisiti da confrontare con le altre evidenze del dominio, mantenendo separati controlli di solo fondo, segnale senza gradiente e correzione omessa.

La terza scheda H63 riassume i primi 13 gruppi uniformi pesati: 10.992 varianze diagonali e 16.284 covarianze fra vicini con riferimento non nullo rientrano nel 5%; 12.612 riferimenti nulli restano indefiniti. Sono conservate 63 aperture confrontabili e 30 senza stima per supporto incompleto. La varianza completa di apertura è da 1,1435 a 4,4814 volte la stima diagonale nel modello dichiarato. Il controllo indipendente riclassifica 39.951 endpoint scalari; non dimostra covarianza empirica o indipendenza fisica. Fuori da questa scheda storica sono già verificati altri cinque gruppi, per 18 su 80; campagna nativa ancora in corso nella stessa istanza, senza riavvii automatici.

| Evidenza locale | SHA256 |
| --- | --- |
| Limiti condizionali di flusso diffuso | `513844a524faa454ffa77a62190cd8607c48b1ca0efbf983c0c77b342b8695bd` |
| Conteggio ABE retrospettivo completo | `ab718e1ecb4e88643a73f16ec016807a34dcf3a2a75ba8c476774b8aa6ed41d5` |
| Riepilogo dei 13 gruppi pesati | `1a886f87bc49a0662df0d63a1ad448c192e7f8a46f408fcddebc8905b21b0aef` |

Il conflitto della PR con main è stato risolto integrando il main esatto `25d03e492f514058a4e7d7a9bc947462735f1d6a`: due blocchi di un test meteo sintetico, conservando helper di normalizzazione e casi di incertezza. Tutti i sette CI del successivo commit `a69371d76acc8e9b8812d53f4b763f599f8e8ad5` sono riusciti. Non attestano i CI del presente aggiornamento H63. La PR resta in bozza; nessun merge verso main o deploy. Sette famiglie/25assi incompleti, zero chiusure scientifiche, conoscenza finale e trasferimento integrale con recupero remoto ancora aperti.


## H64: evidenze osservate già disponibili e profilo uniforme completo

H64 conserva 4.920 requisiti e tutte le 195 schede H63; aggiunge tre schede, per 198 totali. File SHA256 `7bd122781df154cccf0a50332619417b3e9462f351ea55db4f64abe747739301`; lettore v16 `4d4ecf4f3f898cb4a539b2a39ebaf3e2d1d7ced8d6107407b88a0463e6dcb1aa`. Audit, query della scheda filtri, dei 20 gruppi uniformi e dell'asse FILTER_COLOR/3 riusciti; impronta errata respinta. Rendiconto v46 `19468f7c37669e2cd087bed8c651741c698524804fcb9225da8dd8d95920ea3d`: 14.521 criteri letterali e 19 criteri Owner preservati, solo due righe con collegamenti aggiunti. Autorità registrata sempre v600/v1.171, senza nuova v1.172 o conoscenza finale.

La revisione storica dei soli studi nominali non stabiliva assenza di prove cromatiche nell'intero corpus. Sono state riconciliate quattro schede successive, ricontrollando otto fonti e dodici transizioni appaiate: coppie osservate NGSL/Gaia, sostituzione NGSL/LOWLIB sullo stesso cohort, supporto comune CALSPEC e 256 campi cromatici sintetici con 36 riferimenti separati. Le vecchie richieste di cercare queste prove vanno lette nel loro contesto storico, senza ripeterle per riempire un'etichetta generica.

Le coppie NGSL/Gaia restano selezionate da metadati, con supporto nominale parziale, epoche e risoluzioni diverse. Nella variante con RVS riportata, R/G conserva 147 confronti entro5% e uno oltre su148; senza velocità ne conserva154entro e2oltre su156. Le dimensioni diverse non consentono di attribuire causalmente la differenza alla correzione di velocità. La sostituzione LOWLIB/NGSL riusa osservazioni HST e72intestazioni di visita corrispondenti;720confronti per convenzione non sono720nuove acquisizioni indipendenti. CALSPEC esclude intervalli accanto a DATAQUAL=0 senza imputarli. Non sono attestate indipendenza dalla calibrazione Gaia/SPCC, distribuzioni misurate della risposta filtri/QE o calibrazione assoluta.

Le prove cromatiche conservano casi in cui la correzione di apertura stimata migliora il confronto e casi in cui la deriva della PSF peggiora il risultato rispetto al grezzo. L'esatta frazione del simulatore rimane un controllo analitico. Restano separati i riferimenti reali, i campioni indipendenti e l'incertezza di PSF, fondo e registrazione. SHA256 della riconciliazione `1ba5a793d7eba5dbe171d428a3ee07deff017dfec233ca4412d3475c6a7339c7`.

Sono completati i controlli indipendenti su **tutti i20gruppi del profilo uniforme**:5.180casi,2.129.920coefficienti,71.136endpoint di covarianza condizionale e192confronti di apertura supportati. Coprono MONO e quattro pattern Bayer, scale1/2 e due larghezze Square nelle geometrie congelate. Aperture senza supporto completo restano senza stima. Questo completa quel profilo finito, non l'intero studio, il rumore empirico o una qualificazione universale. Riepilogo SHA256 `403286778135dfc28a104d4ca1d2fdf9281edb371da4373b88975a7ddcc0379d`.

Il primo gruppo non uniforme, nella medesima geometria00, conserva529coefficienti differenti rispetto all'uniforme e supera il confronto indipendente. Il rapporto fra varianze complete dell'apertura, non uniforme/uniforme, vale circa2,6795nel modello di varianza crescente,0,5268in quello decrescente e1,4202con varianza unitaria. Sono effetti condizionali sui medesimi input di base, non misure del rumore reale né evidenza di un miglioramento generale. Rapporto SHA256 `f882de7be069c87c2801a7802d8cf110c5c583a8108110c7fdd453d0b8a0538b`.

È attivo un controllore separato per l'analisi dei soli gruppi completi. Sei prove di flusso verificano esclusione di gruppi incompleti e già verificati, blocco su risultati esistenti non verificati e arresto al primo errore di analisi senza retry. Il primo collaudo da stdin mancava del percorso dei moduli: il controllo precedente all'avvio ha respinto la qualificazione assente prima della prenotazione; il collaudo salvato corretto è passato. Il controllore non avvia né termina PixInsight e non riscrive le ricevute native; ogni lotto congela indice delle fonti e programmi. Nell'osservazione successiva risultano27gruppi verificati, non lo stato permanente della campagna ancora in corso.

La capsula locale H63,35file e9.502.844byte, ha superato estrazione, rehash completo e audit del lettore recuperato identico all'originale: SHA256 `f275c4cb2c5727fcaea41e9683a05080a8f7592f5cadd50f14bb4073d8ab8eee`. È autosufficiente per le query offline della conoscenza e contiene alcuni input scalari dei riesami; non contiene ogni evidenza esterna delle195schede o tutto l'ambiente nativo. Non attesta recupero remoto. La successiva capsula dei lotti001–006 conserva nove gruppi,2.331casi e4.756file con tutti i membri verificati: SHA256 `605c0972f4da7420b85a10259a8ce346d8738afd8f350d1efc9a9297154031eb`; anche questa mantiene dipendenze esterne dichiarate.

Tutti i sette CI del precedente commit H63 `44c908a9fc50c41db8b2c1c92fc87d32633f5d74` sono riusciti; verificare quelli del nuovo aggiornamento separatamente. PR in bozza, nessun merge verso main, deploy o attivazione del portale. Sette famiglie e25assi restano incompleti, zero chiusure scientifiche; conoscenza finale e trasferimento completo su GitHub con recupero indipendente ancora aperti.


## H65: saturazione, rischio decisionale e ripresa dopo esaurimento della memoria

Aggiornamento del 14 novembre 2026. H65 conserva tutte le 198 schede H64 e aggiunge due schede, per 200 totali. Il lettore v17 usa H65 come riferimento verificato e aggiunge `--policy` per leggere criteri e limiti senza autorizzare esecuzioni. Sette prove CLI verificano audit, riepilogo, policy, entrambe le nuove schede, asse VERSION_BACKEND/3 e rifiuto dell'impronta errata. Prova SHA256 `457b29391c80e7db4bc3e3929c13a84fbded18b98f8f86b098be0933b2ec774d`. Rendiconto v47 SHA256 `9788f33cecb5dc51adb6a6bb5003aac0f907dd8bda8341dde2e7194d2f67a1dc`: conserva 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner; solo due righe ricevono collegamenti aggiuntivi.

L'Owner ha confermato un massimo dell'1% di decisioni scientificamente errate, da verificare con limite superiore di confidenza del 95%. Il criterio è **definito, non ancora validato**: popolazione, campionamento, dipendenza, molteplicità e adjudicazione devono essere congelati prima del collaudo confermativo. Le 32 risposte descrittive precedenti restano escluse. La scelta non autorizza nuove chiamate a pagamento. Restano invariati il 5% sulle misure relative e il 5% della FWHM iniziale per la posizione sulla stessa griglia; le violazioni operative comportano sempre rifiuto.

Il riesame saturazione ricolloca le prove già presenti: 80 target held-out, otto campi di calibrazione separati e 64 scene sovrapposte. Il fit congiunto a due componenti rientra nei criteri in 13 scene su64; quello singolo in nessuna. Il prior di puntamento grossolano e le varianti post hoc della PSF non diventano rilevamento completamente cieco o nuove osservazioni indipendenti. Nelle 384 aperture appaiate di ricomposizione mascherata, tutte le undici nuove violazioni di flusso oltre5% compaiono anche nel ramo con solo bordo e smoothing fissato. La conformità della posizione non dimostra conservazione del flusso. Riconciliazione SHA256 `c1564cd53067d298504f26743c65b41d8d32d293800577020e5e5923e59bab30`.

La scheda dei primi30gruppi pesati (20 uniformi e10 crescenti) conserva 96.339 classificazioni scalari verificate con aritmetica intera indipendente: 26.256 varianze diagonali e38.619 covarianze con riferimento non nullo entro5%; 31.317 riferimenti nulli restano indefiniti. Aperture:147 confrontabili entro5%,75 senza supporto completo. La varianza completa rispetto alla diagonale varia da circa1,1435 a4,9540 sotto i modelli dichiarati: non è rumore empirico. Riepilogo SHA256 `b76551b22e5942bfd7c786c8abe1708e83e9122e6922426784b2292b8a32cdb0`.

### Incidente di memoria e nuovo segmento limitato

La seconda sessione lunga è stata fermata dopo un effettivo avviso nativo «Out of memory»:6.412 tentativi,6.411 casi OBSERVED e un'interruzione NativeReturnedFalse, tutti preservati. Un'analisi indipendente del lotto019 aveva inoltre registrato MemoryError prima della lettura del piano mentre erano attivi più lavori; non viene attribuita una causa esclusiva. Dopo l'uscita normale di PixInsight con codice0, l'analisi invariata del lotto019 è stata eseguita una sola volta e ha superato il verificatore originale. Il fallimento iniziale resta conservato. Sono verificati33gruppi completi, non tutti gli80.

Il successivo programma limita ogni sessione a128casi e osserva contatori Windows in sola lettura: richiede arresto al successivo confine salvato fra casi se la memoria privata raggiunge2GiB, la riserva di commit scende sotto4GiB, la memoria fisica disponibile sotto2GiB o i contatori diventano indisponibili. Ventisette fixture del programma e18fixture del worker verificano il controllo operativo, senza garanzia di prevenire ogni errore di allocazione. Nessun kill, retry automatico o modifica all'installazione.

Il primo segmento limitato ha concluso128casi, con ricevute, History, hash dei campioni binari e chiusura delle viste verificati; uscita normale codice0. Massimo privato campionato985.718.784byte su74campioni, nessuna richiesta di arresto; il massimo campionato non è il picco assoluto del sistema operativo. L'audit esclude duplicazioni con le precedenti8.646conclusioni: **8.774 casi unici conservati e11.946rimanenti su20.720**. Questo conteggio misura l'integrità dei risultati conservati, non l'accettazione scientifica. Audit e piano esatto rimanente: `weighted-bounded128-case-audit-h-v1/report-and-exact-pending-cases.json`, SHA256 `eaf0c92e58342b2e633f0f4765959aadbef2ee39f4df5d9cb3cf05f503a14541`.

Le sezioni H64 e precedenti descrivono gli stati osservati allora; la loro indicazione di sessione in corso è superata dal presente aggiornamento. Tutti i sette CI del precedente head H64 `065b7ba575bb70126d86e9cd6d96739837fed2ea` sono riusciti; i CI di questo nuovo aggiornamento richiedono una verifica separata. PR ancora in bozza; nessun merge verso main o attivazione del portale. Sette famiglie e25assi incompleti, zero chiusure scientifiche. Conoscenza finale e trasferimento integrale su GitHub con recupero dei byte restano aperti.


## H66: recupero controllato e primi36gruppi pesati verificati

H66 conserva tutte le200schede H65, aggiungendo una scheda operativa e scientifica circoscritta, per201totali. File SHA256 `6986087d5f6096bdb2f3a250a54a8035d5f00ed274da02bce40a13a0860e2319`; lettore v18 SHA256 `e921152787ed5e2c2e6741ae6b03a4d7de952980df852e3fb3f5308d625e8fa6`. Otto prove CLI verificano audit, riepilogo, policy, schede di saturazione/pesi/ripresa, asse del rischio IA e rifiuto dell'impronta errata. Prova SHA256 `702664d68ff87d861d0bd634c02e28dee7d0716a5dc88507aaaa80cdd91b4060`. Il rendiconto v48 `c0970cc535f9056255ed2ea4b2545aacae2f9c15cba4ab779597e3e9845dcaa6` conserva4.920requisiti,14.521criteri letterali e19criteri Owner; una sola riga riceve un collegamento aggiuntivo. Registro v600/v1.171 invariato; H66 è una conoscenza locale provvisoria, non una nuova versione registrata o finale.

Lo snapshot della scheda termina all'uscita normale dell'epoca003: **9.414casi unici con integrità verificata,11.306rimanenti su20.720**. Dei casi conservati,9.324appartengono a36gruppi completi verificati indipendentemente;90sono in un gruppo incompleto. La frazione45,4% riguarda il completamento dei casi nativi della campagna finita, non la milestone o l'accettazione scientifica. L'attestazione lega i gruppi ai loro rapporti e verificatori esatti, senza pretendere un nuovo replay di tutti i verificatori precedenti: SHA256 `4b4e528dc4dd53e791a2e8281653d2d2802d9bad9ba86c5af36b02fde9504b4d`.

Dopo due segmenti da128casi, l'epoca003 ha completato512casi senza errori dichiarati, con hash binari dei campioni, History e cleanup ricontrollati e uscita normale codice0. Il massimo privato campionato è1.212.624.896byte su550campioni, senza richiesta di arresto. Audit e partizione esatta rimanente: `weighted-bounded-epoch-003-case-audit-h-v1/report-and-exact-pending-cases.json`, SHA256 `60b2131e2b29aced286839bc1004ff1dd2cd95ae4398d2a4a7e6143faaed4342`. I due nuovi gruppi14/15 del profilo crescente completano tutte le fasi di riduzione, certificazione numerica e verifica indipendente del lotto021. La verifica resta condizionata agli operatori, input e modelli di covarianza congelati.

La nuova preparazione genera programmi immutabili da template verificati, controlla l'esatto prefisso dei casi rimanenti e riesegue18fixture del worker e27fixture del programma di avvio per la configurazione effettiva. Il massimo è512casi per segmento; resta il limite privato2GiB e la richiesta di arresto al successivo confine salvato se mancano le riserve di memoria o i contatori. Le prove effettuate non garantiscono sicurezza di memoria in ogni carico e non identificano una causa esclusiva dell'incidente precedente. Nessun kill, riavvio automatico o ripetizione dei casi conclusi.

La successiva epoca004 è separata e non è conteggiata nello snapshot H66. Ogni suo risultato richiede ricevuta finale, controllo delle viste, uscita effettiva e audit prima dell'inclusione. Le vecchie ricevute di errore e gli avvisi Out of memory/MemoryError restano conservati.

La capsula locale H65 ha inoltre superato estrazione e rehash di318file e riproduzione identica dell'audit del lettore recuperato:9.627.483byte, SHA256 `6965403533ac9f2b8b8595f0eaeaac66dfd6d12aeeabc1f23002a1eb774f7627`. Include conoscenza, lettore, riesami selezionati e ricevute del primo segmento128; non tutti gli input esterni delle200schede, i sidecar/pixel originali, le epoche storiche o l'intero ambiente scientifico. Non attesta recupero remoto degli archivi.

Tutti i sette CI del precedente head H65 `5f57c81afefaa6a73b8a2100643ec79359e772dc` sono riusciti. I CI del presente aggiornamento vanno verificati separatamente. PR in bozza; nessun merge verso main, deploy o attivazione del portale. Sette famiglie/25assi incompleti, zero chiusure scientifiche; file finale di conoscenza e trasferimento integrale con recupero remoto restano aperti.


## H67: quaranta gruppi, confronto dei pesi e diagnosi dell'avvio

H67 conserva integralmente le 201 schede precedenti e aggiunge due schede circoscritte, per **203 totali**. Conoscenza provvisoria SHA256 `80bb92f2bdcbdf9485906a3c2da8a7b4625557120209caf5f6507cba419fda6d`; lettore v19 `1601861730dd1796e68c3005c010441037db47748fd0bf66eeeb827fbb10856f`. Dieci prove CLI verificano audit, policy, query storiche e nuove schede, oltre al rifiuto dell'impronta errata: prova `f45779c2de90298c85aae99e5ffb750c40125d56f6399010825f74b4d167d978`. Rendiconto v49 `01ce4747bd0895983486ee71c9c00ac4ee10a61a88e9d83cd2e7adf19626282b`: tutti i 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner conservati; due collegamenti aggiunti nella sola riga DrizzleIntegration. Registro v600 / conoscenza registrata v1.171 invariati. H67 non è una nuova versione registrata né la conoscenza finale.

Lo snapshot termina all'epoca **006 chiusa e sottoposta ad audit**: **10.438 casi unici conclusi con integrità verificata, 10.282 rimanenti su 20.720 (50,4% della sola campagna nativa finita)**. Quaranta gruppi completi su 80 sono verificati indipendentemente: 10.360 casi, più 78 casi in un gruppo incompleto. Tutti i 20 gruppi uniformi e i 20 crescenti sono conservati. Audit della partizione `ffcbb37fc3b8714c262d956b80ff7ce3ed756cd14328089aee2888d6cb926bc8`; attestazione dei 40 gruppi `9ea37efcd63836ff0ed0e2c7bcdcde56c7380249dd5e57b816e60601e70d598b`. L'attestazione rilegge rapporti e ricevute indipendenti e ne verifica l'appartenenza alla partizione; non pretende di rieseguire ogni verificatore storico. Epoche successive attive o preparate sono escluse dal conteggio.

Il confronto post hoc include tutte le 20 geometrie uniformi/crescenti, 2.129.920 coefficienti e 156 coppie di aperture complete: **96 supportate e 60 senza stima**, rispettivamente 32 e 20 per ciascuno dei tre modelli di rumore dichiarati. I pesi crescenti aumentano la varianza condizionata salvata in tutte le 32 aperture supportate del modello crescente-indipendente e del modello unitario; la riducono nelle 32 del modello decrescente-indipendente. Nessuna discordanza dell'ordinamento rispetto al riferimento salvato. Rapporto `6f93b7a5b0c1019b407c812ac9486c12ae4beed9b045de27461a0948738bb2bd`; verifica con decodifica indipendente dei binary64 mediante interi `a6f644d7cedc27c99882a125b3c172ce60da4fc3e09bf839e0263958dcf023eb`. Si confrontano varianze condizionate salvate in binary64, non verità analitiche razionali esatte né rumore fisico misurato. Le coppie non sono nuovi campi indipendenti. Il risultato non giustifica un miglioramento universale tramite pesi arbitrari e non chiude covarianza empirica, pesi adattivi, rejection o calibrazione hardware.

Restano conservate le anomalie d'avvio. Tre prove senza immagini hanno mostrato rispettivamente due, zero e zero marcatori C0000005 nella console acquisita. Le ultime due hanno atteso la ricevuta prima dell'osservazione; soltanto una aggiungeva al processo figlio un'opzione diagnostica grafica. I messaggi grafici su stderr persistono in tutte e tre: nessuna causa esclusiva o soluzione dimostrata, nessuna opzione grafica adottata come correzione. Riesame `7108a4263d869d54d401c697d5396a2990a5b543637dd208208ff18fe1ee67af`.

L'epoca 006 ha verificato un blocco prima dell'elaborazione: durante l'attesa sincrona del controllo non era disponibile il testo accessibile completo. L'avvio è stato respinto esplicitamente, con **zero tentativi, zero integrazioni, zero immagini residue e uscita normale 0**. Il testo è diventato leggibile dopo il ritorno dello script; questa osservazione non prova una causa universale dell'interfaccia. Evidenza `e799d66ad0618373e8f56bd7474fbb4b30b4fd1e680d5b5fd258a288ec953679`. La partizione pendente resta invariata. Il successivo schema separa uno script d'avvio che ritorna all'applicazione dalla revisione di due trascrizioni complete e dall'esecuzione separata sullo stesso processo, vincolata a identità e piano. Le verifiche simulate del nuovo schema coprono 13 casi della prima fase, 32 del controllo, 23 del worker e 37 del sistema di lancio; non attestano affidabilità generale dell'avvio o validazione scientifica.

Sei capsule locali coprono ora i 40 gruppi completi e 10.360 identità di caso disgiunte, lasciando i 78 casi parziali separati. L'ultima capsula del lotto 023 conserva 1.157 file / 518 casi, 6.218.642 byte: SHA256 `67531797e2dce1fde3060cd47ef867f70bc12a5110fa47d96fb90e6429ff0218`. Tutti i suoi membri sono stati riletti e verificati; l'attestazione aggregata `abd2639f4d10b428be7f8f74289c8bf2f8624493da2be5293925fdd74206e76a` ricontrolla identità degli archivi e copertura disgiunta, senza una nuova estrazione integrale delle capsule precedenti. Dipendenze esterne e limiti di replay rimangono espliciti. Archiviazione locale e documentazione dei digest non equivalgono a trasferimento remoto dei byte.

I sette CI dell'head H66 `7eb5d5871833a856aae4b4edc181a11d98913b99` sono riusciti; i controlli del nuovo aggiornamento richiedono verifica separata. PR in bozza, nessun merge verso main, deploy o attivazione del portale. Sette famiglie e 25 assi incompleti, **zero chiusure scientifiche**. Conoscenza finale e trasferimento completo su GitHub con recupero remoto restano aperti.


## H68: partizione chiusa a 42 gruppi e controlli PSF ellittici

H68 conserva tutte le 203 schede precedenti e aggiunge due schede, per **205 totali**. Conoscenza provvisoria SHA256 `5e29bda26be8d56730705b2d6810f36204110c53da94aa834830aeab44857adf`; lettore v20 `db961d4cdc99a4fe35277587981024abd30bddeaad833a8324aeab986cd0e69a`. Dodici prove CLI verificano audit, policy, query storiche e nuove schede, inclusa la distinzione fra casi conclusi e avvio respinto: prova `23ded84e6136aa94637d6deae4ddf64808769a13f48dc552db692a3ed3a0336b`. Rendiconto v50 `88bb0af25697a81033be853dfb15ab8c85a11b0148c76228493e7c3d8f537099`: 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner conservati; un collegamento aggiunto alla riga DrizzleIntegration e due indici di asse aggiornati. Registro v600 / conoscenza registrata v1.171 invariati; H68 resta locale provvisoria e non è la conoscenza finale.

Lo snapshot chiuso termina all'epoca **008**, respinta senza elaborazioni dopo l'epoca 007 completata: **10.950 casi unici con integrità verificata, 9.770 rimanenti su 20.720 (52,8% della sola campagna nativa finita)**. Sono verificati indipendentemente **42 gruppi su 80**, per 10.878 casi completi più 72 casi in un gruppo incompleto. Audit della partizione `15766b5f50ac5f88d4767f30e7cd134ea3a7328437ace6c0cd565a382c25a076`; attestazione dei 42 gruppi `28e07c2d3321c02ceff026bcfeb80d76c7e3497cb6797cc8de54cb36b01dfed5`. I due nuovi gruppi decrescenti 00/01 completano il lotto 024, incluse riduzione, certificazione numerica e ricevute indipendenti. Le epoche successive attive o preparate non sono conteggiate.

Nell'epoca 007, due trascrizioni complete della console inattiva sono state conservate prima dell'unico invio del worker sullo stesso processo, con piano e identità verificati. Tutti i 512 casi sono stati ricontrollati tramite campioni binari, History e cleanup; zero fallimenti dichiarati, zero immagini residue, uscita normale 0. Il massimo privato campionato è 1.211.367.424 byte su 1.525 osservazioni, senza richiesta di arresto; non è un massimo assoluto del sistema operativo. L'epoca 008 ha invece mostrato due C0000005 nella prima revisione inattiva: nessuna liberatoria scientifica, ricevuta nativa di rifiuto con zero tentativi/integrazioni e chiusura normale. Evidenza `37b376f06da0e8fc3246fe0c27f2538d2bf6e10de56531a00f317787113201e6`.

Il riesame lega sei osservazioni d'avvio conservate: marcatori di eccezione **2, 0, 0, 0, 0, 2**. Le condizioni differiscono e non costituiscono una campagna indipendente di affidabilità; non si stima una probabilità di guasto. Gli stessi quattro messaggi grafici normalizzati compaiono in tutte e sei. Attendere la ricevuta non è quindi una prevenzione dimostrata; causa esclusiva, effetto dell'accessibilità, efficacia dell'opzione grafica e guasto della RAM fisica restano non dimostrati. Identità e versioni delle dipendenze installate sono state ricontrollate in sola lettura, senza inventare hash storici mancanti. Riesame `a58cceb630212b2c9a221dd73563f23882f079b114a02b2971d2b09f5e830f7a`. Un nuovo host aggiunge soltanto la registrazione dei cinque valori grafici ereditati e verifica che non cambino prima del lancio: nessuna opzione aggiunta, 41 prove simulate del sistema di avvio. Ogni nuovo tentativo richiede piano immutabile, identità corrente, due trascrizioni complete, rifiuto degli errori noti e sorveglianza della memoria; questo non attesta affidabilità generale o ammissione scientifica.

Per PSF_PIXEL/2 è stato ricontrollato l'intero insieme già esistente di **24 scene strutturali senza rumore / 96 fit nativi di sviluppo**. Un decodificatore indipendente dei binary64 e confronti mediante interi confermano tutte le **768 decisioni entro il 5%** dei flussi di modello salvati nelle aperture fisse di raggio 8/12, mantenendo entrambe le ipotesi angolari e le valutazioni puntuale/integrata. Nessun caso selezionato per il risultato migliore, nessun nuovo fit o campo indipendente. Rapporto `071ba7e87f252c97780f907621056ea37fa1e946d732d88abe8f608aa95da67c`; 24 fixture indipendenti su decodifica, soglie e operandi invalidi, prova `8a819dc8b3b095cc0bd37ce0976da39bf52d679a9c69b3b45fd62add8fe69cc1`.

La nuova scheda PSF riconcilia tutte le sei misure originali, conservando i limiti: aritmetica esatta sui valori salvati non certifica quadratura o verità fisica; due aperture non sono curve complete di energia racchiusa; campi isolati inizializzati da catalogo non misurano rilevamento cieco o sorgenti confuse; quattro varianti per scena non sono quattro campioni indipendenti. Le FWHM generative maggiore/minore non sostituiscono il riferimento iniziale misurato richiesto per la posizione. Il modello analitico di ricostruzione dichiarato conserva il proprio ruolo senza inventare un requisito di nuova convoluzione nativa; dominio completo e incertezza restano aperti.

Sette capsule locali coprono i 42 gruppi completi / 10.878 identità di caso disgiunte; i 72 casi parziali restano separati. L'ultima capsula del lotto 024 conserva 1.157 file / 518 casi, 5.840.708 byte: SHA256 `b67c759b34d9ed0c60d91a20ba751966533965a3760aee102b1d2a114972f529`. Copertura aggregata `1908509e79a8b86e8a72ebfa674c575096949bda1f8ddc249fd4f2bab755523c`: identità degli archivi e appartenenza disgiunta ricontrollate, non una nuova estrazione di tutte le capsule precedenti. La capsula selezionata PSF è di 105.638 byte / 10 file, SHA256 `a4bb299bb40a8fa11af971cfc3361daddf51d44526c787cb759fbb9614d41327`, con dipendenze native esterne esplicite.

È inoltre completato il recupero locale della capsula H67: 236 file estratti e ricontrollati, audit del lettore identico all'originale; archivio 12.344.999 byte, SHA256 `a1556a869c770f44fe8391ede4574eff3cb37b76bb009170f338b3d0ac4cf6f4`. Resta un recupero locale selezionato, non di tutte le dipendenze delle schede né dei byte su GitHub.

Tutti i sette CI dell'head H67 `e706b3e5e4a119c0c87a15f10529f137efeee4ac` sono riusciti; i controlli del presente aggiornamento richiedono verifica separata. PR in bozza, nessun merge verso main, deploy o attivazione del portale. **Sette famiglie e 25 assi incompleti, zero chiusure scientifiche**. File finale di conoscenza e trasferimento completo su GitHub con recupero remoto restano aperti.


## H69: rumore preesistente, equivalenza al 5% e identità delle configurazioni

H69 conserva tutte le 205 schede precedenti e aggiunge due schede, per **207 totali**. Conoscenza provvisoria SHA256 `e67f56d9628052fb15764ac4b3838e2eabd52ee81dd452926f8d255e110c0104`; lettore v21 `caf4054448ed8ed72bd2a84edee5b3f1eb5fa94710efcf6fee7c853e8f074adb`. Quattordici prove CLI verificano audit, policy, query storiche e nuove schede, incluso il rifiuto dell'impronta errata: prova `ca2128973226fe261e7be9be8c7c12f4a14b57aa298720ee9f3b2f7d035ba865`. Rendiconto v51 `aabace236c5aeac969820d0e2a5ff3b8b4803e6372c5c3f56e264aa8f045f4d7`: tutti i 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner conservati; due collegamenti aggiunti nella sola riga DrizzleIntegration. Registro v600 / conoscenza registrata v1.171 invariati; H69 non è una nuova versione registrata né la conoscenza finale.

La scheda nativa H69 termina all'epoca **009 chiusa e sottoposta ad audit**: **11.462 casi unici conclusi con integrità verificata, 9.258 rimanenti su 20.720 (55,3% della sola campagna nativa finita)**. Quarantaquattro gruppi su 80 sono verificati indipendentemente: 11.396 casi completi più 66 casi parziali. Audit `99ebbfc28aefa7858cde2fe6f54708d91044e5cef471a78ad44c4132c3090c8a`; attestazione dei gruppi `db812f20f8c15120e4483d0b9b458bad4398c11da79e9a69cebc28e28f9c50b9`. L'epoca 009 conserva 512 casi senza errori dichiarati, zero immagini residue, uscita normale 0, due trascrizioni inattive prima dell'unico invio del worker. Massimo privato campionato 1.212.403.712 byte su 1.433 osservazioni, senza richiesta di arresto; i cinque valori grafici ereditati risultavano assenti, nessuna opzione aggiunta. Restano conservati gli avvii respinti e il mancato accertamento di causa o affidabilità generale.

È stata riconciliata una campagna sul rumore già conclusa: **5.120 elaborazioni native, 128 blocchi gaussiani condivisi, 512 campi-base di esposizione dichiarati e 376 osservabili scalari**, con 40 rettangoli senza stima conservati. Tutti i 376 confronti restano compatibili con il modello congelato. Le 2.560 viste di modalità e le diverse configurazioni non sono nuovi campi indipendenti: non si ripetono le prove come se fossero assenti e non si contano le 5.120 chiamate come altrettanti campioni grezzi indipendenti.

Il riesame post hoc distingue compatibilità ed equivalenza al 5%. Dalle somme quadratiche a media nota salvate, 94 stime puntuali di varianza e 206 stime puntuali di RMS rientrano nel 5%; gli intervalli ricostruiti con i quantili chi-quadrato congelati non rientrano interamente nel 5% per nessuno dei 376 osservabili. Il rapporto di larghezza fissato dai quantili è circa 2,620537 per la varianza e 1,618807 per l'RMS, già troppo ampio prima dell'espansione per arrotondamento. Questa mancata ammissione di equivalenza non trasforma in fallimento il precedente confronto di compatibilità. Rapporto `87a019b6ff9987142041145120ca8a6996f36899db59ab6ce68e9b889317fd78`; verifica indipendente con razionali esatti dei valori salvati, dei punti e dell'impedimento di larghezza `3776a4586296b0a707f74ece7f15df8c8db3292aa097a67797fb5d64de92a96f`.

Gli intervalli restano condizionati al modello ideale gaussiano/PRNG e ai quantili approssimati conservati: nessuna nuova certificazione della loro CDF, del limite uniforme di arrotondamento, della risposta fisica delle camere o della copertura. Questo esito non riguarda l'altro requisito Owner sul rischio di decisioni IA dell'1% con confidenza 95%.

Un primo tentativo di associare per nome tutti i vecchi pesi diseguali ai nuovi pesi decrescenti è stato fermato da un'asserzione prima di emettere un certificato di risultato. Il confronto corretto controlla **tutte le 160 coppie** fra 40 configurazioni legacy e quattro nuove politiche, con geometria, fasi, convenzione delle colonne sorgenti, pesi per esposizione/canale e coefficienti razionali. Risultano **24 corrispondenze di configurazione**: 20 uniformi e quattro monocromatiche decrescenti. Le altre 16 configurazioni CFA legacy hanno pesi dipendenti dal canale, diversi dalle quattro nuove politiche. Per esempio, il canale G legacy diseguale usa la sequenza 1/2,1/4,1/8,1, che non è una riscalatura comune della sequenza decrescente 1,1/2,1/4,1/8.

Sono verificate 2.293.760 identità di coefficienti, inclusi gli zeri impliciti, nelle 24 corrispondenze; le altre decisioni conservano controesempi esatti. Nessuna coincidenza numerica senza corrispondenza dei metadati è stata usata per trasferire evidenza nativa. Rapporto `86d17791c129d5e9127e4f87c3fd2cb798ede4350ba387601113ce58fc6a2186`; verifica indipendente tramite prodotti incrociati di interi, senza importare il produttore o Fraction, `a1ae087f465bc646f6b0353cd8e60cd3f36bf6bce68b86f033afdc22d004cee8`. Tutte le 24 configurazioni abbinate hanno ora un gruppo di base completo e verificato: attestazione sullo snapshot a 44 gruppi `2fdbf93d11e0f5657e0fed72a778331592cb0d97b0ebc7f020d5caa0167da24e`. Il precedente conteggio 22/42 resta storico. L'identità riguarda gli operatori razionali dichiarati, non linearità universale o correttezza fisica; l'assenza di un abbinamento in questa campagna non dimostra assenza di ogni altra evidenza nel corpus.

Il tentativo errato, il confronto corretto e le dipendenze selezionate sono conservati in una capsula di 99 file / 3.532.160 byte, SHA256 `d00882d598940cf44c643a52b484bb914ae2ac64f261ade9b47a69355ce01c31`, riletta integralmente per gli hash. Non è un replay nativo autonomo né un recupero remoto.

Separatamente dallo snapshot congelato H69, la successiva epoca **010** ha già completato altri 512 casi con uscita normale e audit: **11.974 casi unici, 8.746 rimanenti (57,8% della sola campagna)**; 46 gruppi verificati su 80. Audit `6b1605adc79c354fea23632233797458dd1adf63ea478dc1dcb2674d0df4c050`; attestazione dei gruppi `553bb8a106a360b9e11bdd752bd57007b100039b9ff1823af35ce954f1d37ff2`. Nove capsule locali coprono 11.914 identità disgiunte dei gruppi completi, più 60 casi parziali separati: copertura `46fe7848fb08e8d84a3c0267bd7cbc2a7c75514be9be7b8a85f94e689f568bbc`. Questa attestazione controlla archivi, manifest e appartenenza alla partizione corrente; non riestrae tutti i membri storici né amplia l'ammissione scientifica. I casi dell'epoca successiva attiva non sono conteggiati.

Tutti i sette CI dell'head H68 `3262281c55bfabc70d05c77466d4976b685bdf74` sono riusciti; quelli del presente aggiornamento richiedono verifica separata. PR in bozza, nessun merge, deploy o attivazione del portale. **Sette famiglie e 25 assi incompleti, zero chiusure scientifiche**; conoscenza finale e trasferimento completo su GitHub con recupero remoto restano aperti.

## Aggiornamento H70: due lotti chiusi e 48 gruppi verificati — 14 novembre 2026

La conoscenza **H70** consolida gli snapshot chiusi delle epoche **010 e 011**: **12.486 casi nativi unici verificati su 20.720**, **8.234 pendenti**, **48 gruppi su 80** verificati indipendentemente. Il **60,3%** descrive soltanto l'esecuzione della campagna finita Drizzle; non misura il completamento scientifico della milestone. I 1.024 casi dei due lotti hanno ricevute, History, controllo dei pixel, cleanup e uscita normale attestati. I casi della successiva epoca 012 attiva sono esclusi da questo snapshot.

- Conoscenza provvisoria H70: `035acc51d2c2386abde0b32259e54c39fabcc0eaaf73dc4644fd8e023229f7e1`, **208 schede**; tutte le 207 schede H69, le righe dei 4.920 requisiti e i criteri dell'Owner sono conservati.
- Lettore v22: `048b3fabb51156637f25973dcd1c8266a504a257833ca365a8e898e4cd06ede9`; **15 controlli CLI** riusciti, inclusi audit, interrogazioni storiche, nuova scheda e rifiuto di un'impronta errata. Ricevuta `96044b3b7146802c2d9ebb04ff1a384dd3eb960d0f60a79141579ebd953c4ed3`.
- Rendiconto v52: `2d48620c55ab8111a65f108f9e8db15feaaf885667e155834decb11ba206ebe7`; conserva **14.521 criteri letterali e 19 criteri dell'Owner**. L'unica riga con collegamento aggiunto è `process:DrizzleIntegration`; nessuna promozione dei gate.
- Audit chiuso 011: `0ac2b4f4e2628b1a4b02eed3223b302fb6e38ff82746687dff3ee5bb7fbc4f00`; attestazione corrente dei gruppi `d1c8566e2ba48786ceb16aa688195314b296d5dbacabde29b6ce303dda9f7d20`.
- Dieci capsule locali coprono **12.432 identità disgiunte** dei gruppi completi; **54 casi parziali** rimangono separati. Copertura `a8998948bf514503ad4d408d67217f84a641e59b6b0d948251be66f9a259d04f`. L'ultima capsula dei due gruppi 027 ha impronta `044238ede3b00fe9e0e67855720fc5ef740f8268a804bcbf0699fc3f1cb4cdae`.

La pubblicazione autorevole rimane **v600 / conoscenza registrata 1.171**; H70 è un consolidamento locale provvisorio, senza nuova versione registrata. Restano espliciti i limiti delle 128 realizzazioni di rumore e dei 24 abbinamenti esatti di configurazione descritti in H69. Le due osservazioni dell'avvio e il controllo della memoria consentono il collaudo circoscritto; non dimostrano affidabilità generale, causa risolta degli errori d'avvio o validazione fisica.

Tutti i sette CI dell'head H69 `77cc52ed70b310e85205a4ec327ccaa1ad55a955` sono stati verificati come riusciti (ricevuta `21df2516771483b2a9cdcf29350d39d298770559b0800d2b4d9d746881466a74`). I CI di questo aggiornamento richiedono un controllo distinto. **Sette famiglie e 25 assi incompleti, zero chiusure scientifiche**. Conoscenza finale, trasferimento completo su GitHub e recupero remoto dei byte rimangono aperti; questa pagina documenta le evidenze e non costituisce il loro trasferimento. Nessun merge, deploy o attivazione del portale.

## Analisi retrospettiva ABE: forma, fondo e bordi sui 24 campi già selezionati

Sono stati riletti e ricontrollati **122 membri dell'archivio nativo** per i 24 campi storici selezionati dal precedente replay (primo, centrale e ultimo indice in ciascuna delle otto celle). Le 48 varianti native dei gradi 1/4 sono confrontate su intero campo, centro64 e bordo16: **432 combinazioni regione–stimatore**, senza nuovi campi indipendenti o chiamate native. Rapporto `8994c0b6c4db09786c8dcd8818caeb68bf7af186c06fffb891a519298711691d`; verifica indipendente con lettore binario separato e aritmetica Fraction, contrapposta agli interi su scala comune del produttore, `2d0e2252bc4b56114cef5d6f5c947e4cc210ae7eb2b3153ab2afcd2290593e08`.

La definizione descrittiva aggiunta misura errore di flusso e norma L2 rispetto alla sorgente ideale conservata; la soglia L2 del 5% è verificata esattamente con `400*somma(errori²)<=somma(segnale²)`. È una nuova analisi retrospettiva, non una soglia morfologica confermativa congelata prima della campagna. Tutti i 48 risultati `X-M` e tutti i 48 risultati normalizzati `Y-mediana(M)` superano il 5% di errore di flusso sull'intero campo. Nessuna misura L2 definita rientra nel 5%, **neppure per il confronto che sottrae il vero fondo**: la discrepanza include rumore e non può essere attribuita interamente alla correzione del fondo. Le regioni con riferimento esattamente nullo mantengono la misura relativa indefinita.

La decomposizione esatta separa energia del rumore, scarto del modello rispetto al fondo noto e loro prodotto incrociato. La proiezione del modello sulla sorgente è una contaminazione allineata alla verità, comprensiva del rumore adattato e dello scarto di fondo; non dimostra rimozione causale del solo segnale. I pixel a verità nulla non sono i campioni effettivamente accettati dall'algoritmo ABE. Il produttore aveva esportato la media ma omesso il residuo quadratico medio assoluto su questo sottoinsieme, promesso nel protocollo: l'addendum indipendente conserva la prima versione e fornisce **216 valori** mancanti.

La riconciliazione `e26dcbccb831a3eff34e79e46db0252765c55d5a94118941ffc868ef1d601b02` collega i risultati alle cinque misure e ai tre controlli originali. Non introduce prove native con solo fondo o con solo segnale senza gradiente. Il confronto `X-B` usa il fondo vero e non viene rinominato mancata correzione di `X`. Restano aperti appartenenza dei campioni, controlli causali, dominio moltiplicativo e incertezza indipendente sui bordi.

Capsula selezionata locale: **137 file / 19.071.999 byte**, SHA256 `99846530a7dd4e86ca229b0fb9e44402767d653cd372195b3fc77008eb88b38a`, tutti estratti e ricontrollati. Include i pixel selezionati; il manifest storico del genitore cita anche membri assenti. Non è il replay completo dei 3.304 campi, un ambiente nativo autonomo o un recupero remoto. I risultati sono successivi al file H70 e attendono il prossimo consolidamento della conoscenza.

Separatamente, l'epoca Drizzle **012** è chiusa normalmente e sottoposta ad audit: **12.998 casi unici / 7.722 pendenti**, **62,7% della sola campagna**; audit `96052d70edffc06cffe710b79126248641ab59e3bb8a599c9f355aa59056826c`. La verifica indipendente dei gruppi successivi è separata e non viene anticipata. H70 conserva il proprio snapshot chiuso 011. I sette CI dell'head precedente `3725b223083c32efd82ab6d7e293bdbe3f550ec1` sono riusciti (ricevuta `1abbb7fe33dad3afd194d2132ed47899c8d64da9cb64e7473050aaeacb471e6c`); i controlli di questa nuova revisione richiedono verifica distinta. Nessuna chiusura scientifica o trasferimento integrale degli archivi è dichiarato.

## Consolidamento H71: ABE integrata nella conoscenza, 50 gruppi congelati

La conoscenza provvisoria **H71** integra ora i risultati ABE sopra descritti e lo snapshot Drizzle chiuso **012**. Contiene **210 schede**, conserva integralmente le 208 schede H70 e tutti i 4.920 requisiti, senza cambiare pubblicazione autorevole, decisioni dell'Owner o ammissione scientifica.

- File H71: `6d0019158bea62bba546af3e50995327748664e815d5ce7a91ee823f52a90085`.
- Lettore v23: `84c6844ab249f00e532aa427aacf704996de02b3922eb35476044741d7110296`; **17 controlli CLI** riusciti, con tutte le interrogazioni storiche, le due nuove schede, audit e rifiuto di un'impronta errata. Ricevuta `0cb450dfe3f40726f81da8d726233de4ac8838196be82b9836cb000a5ebcc9d1`.
- Rendiconto v53: `4cb39e31b5598ce27f5fa4649573a99004ca0abe9ed7ed1c6a87eef44140ac35`; **14.521 criteri letterali e 19 criteri dell'Owner** preservati. Aggiunge collegamenti soltanto ad `AutomaticBackgroundExtractor` e `DrizzleIntegration`; nessuna chiusura di gate.
- Snapshot H71: **12.998 casi unici verificati, 7.722 pendenti, 50 gruppi indipendentemente verificati**. Undici capsule locali coprono 12.950 casi disgiunti dei gruppi completi e 48 casi parziali separati; copertura `ff62b7fae64acf0a95ee2b8840730957c1e722b6d5e1d6ed1c27c40fc3f1796c`.

La nuova scheda ABE conserva le cinque misure, i tre controlli e i rispettivi limiti: 24 campi storici, 48 varianti, 432 confronti e 216 valori aggiunti dal verificatore indipendente. Nessuna nuova acquisizione indipendente, chiamata nativa ABE o soglia confermativa è stata introdotta dal consolidamento.

Separatamente dallo snapshot H71, l'epoca **013** è già chiusa normalmente e sottoposta ad audit: **13.510 casi unici, 7.210 rimanenti**, **65,2% della sola campagna Drizzle**; audit `9a7f143889847ea113aab8be3e0cb5c5e6448880f4c9fbd774cd8715a09ed7b3`. Sono ora verificati indipendentemente **52 gruppi**: attestazione `724bf2d23c2008a9d40a81373160a1386f8ee28db7e0cf7696cc6d1154ddc110`. L'epoca 014 successiva non è conteggiata. I numeri successivi non riscrivono lo snapshot congelato H71.

Tutti i sette CI dell'head precedente `cd796b383c669ec5deddfd868485c100d35bf004` sono riusciti; ricevuta `8a4079d7d9b5a9a22fec6f4f94e62281b661fe1b34979be4b24890e8c956d5ed`. I controlli di questa revisione restano da verificare separatamente. **v600 / conoscenza registrata 1.171**, sette famiglie e 25 assi incompleti, zero chiusure scientifiche. H71 è provvisoria: file finale e trasferimento integrale su GitHub con recupero remoto rimangono aperti.

## H72: controllo di fondo esistente e 54 gruppi Drizzle congelati

La conoscenza provvisoria **H72** contiene **212 schede** e conserva tutte le 210 schede H71, i 4.920 requisiti e le 19 decisioni dell'Owner. File SHA256 `0653cdeb4a734979f8d5f9a198fcea30516aab4953307f8fbc68f8410e494b93`. Il lettore v24 `bce3f8a4271ff94b0310a9d24f504e05faea861bb17637dfa3f752dbe7155108` supera **19 controlli CLI**, incluse tutte le precedenti interrogazioni di regressione, nuove schede, audit e impronta errata; ricevuta `1d52192098c0c0c8451b273c5bb0b2d8dabf11632f17931024d77e9d1bd519bd`. Il rendiconto v54 `991c4a29922e9ae1b46f8ad83bab7030cf0a943e7e8544a632b6769d7b96dcf2` conserva tutti i **14.521 criteri letterali**.

Lo snapshot termina alle epoche chiuse **013/014**: **14.022 casi unici verificati, 6.698 pendenti, 54 gruppi su 80** verificati indipendentemente. Il **67,7%** riguarda soltanto la campagna finita Drizzle. Audit 014 `ad08d71db78cf2b0e0702b94694988dddced7832652cb203a1aaaea75a1c997b`; attestazione `59e8dfe7cc5b0363b574b133a0154c2f46d9f5221792957cc429db0d6bbd915c`. Tredici capsule locali coprono 13.986 casi disgiunti dei gruppi completi, più 36 casi parziali separati: copertura `5398b6ad72bbca00beddd2f7b9acd40eb552beb77010e1270f417290a91da82e`. I casi della successiva epoca 015 attiva sono esclusi.

La nuova scheda ABE riconcilia **un solo campo deterministico di fondo positivo**, già eseguito in otto varianti di correzione/normalizzazione/formato. Otto modelli rientrano nel 5% L2 rispetto a quel fondo; il segnale astronomico è zero, quindi il relativo errore di flusso della sorgente resta indefinito e non viene promosso a successo fotometrico. Rapporto numerico, verificato con due lettori e due aritmetiche, `ccc29b944cd5c0c36f0801582a965e4ff8c960da9e929f1a6c90c8a18bcfdcf2`.

Una sola configurazione — sottrazione, normalizzazione, modello/output f64, grado 1 — coincide con tutte le 22 assegnazioni diverse dal nome dell'uscita dei **24 sorgenti di parametri heldout riletti**. Le sette altre varianti restano non corrispondenti; il grado 4 non è incluso. Rapporto `0ac4795754109acff6e5ab3fa9be79e43e8b4ae8b84e2e85ef146f981b200fb2`, verificato separatamente tramite confronto dell'intero testo dopo la rimozione della sola riga dell'identificatore di uscita. L'identità delle impostazioni non dimostra identità del codice caricato, equivalenza della risposta o validità del dominio rumoroso. Tutti i 16 ritorni negativi storici su campi zero/negativi restano conservati.

La capsula del controllo e dell'abbinamento contiene 45 file / 390.376 byte, SHA256 `66db5b8399641d6e724803e0171ac751279eed30f5276532b417f1c0b1e2ed97`, tutti estratti e ricontrollati. Comprende il precedente archivio selezionato del controllo; resta distinto da replay nativo completo e recupero remoto.

Successivamente al congelamento H72 sono stati preparati **nove input di controllo senza rumore** sulle due forme diffuse conservate e tre fondi (zero, costante e gradiente 2D). I 147.456 valori e il piano sono verificati indipendentemente; nessuna esecuzione nativa nuova è avvenuta. Il piano prevede 17 tentativi nuovi anziché 18 perché il caso zero/grado 1, già fallito con identiche impostazioni, viene riusato come riferimento indisponibile senza ripeterlo né sintetizzarne un modello. Protocollo `1bcdf2098c6572ec39240359c57736fbca20dbd13f98deae505c0c0611d070d5`; manifest `0f576ef3efa5b856625013dbd0a6fb7a1aa663cdbbf195d9098de5eb95617dd6`. Worker, host, gestione dei fallimenti e dispatch devono ancora essere qualificati. Questi input non completano controlli nativi, incertezza, ammissione scientifica o i requisiti della milestone.

Sull'head H71 precedente `aad508526e2516754c3184afde2da08750fd6a5d`, il primo controllo browser è fallito per timeout nell'ultima asserzione del planner sintetico. Test invariato e diff limitato alla documentazione; log e fallimento sono conservati. **Un solo nuovo tentativo del job è riuscito**, e tutti i sette CI dell'head sono poi risultati riusciti: ricevuta `c67b8cc60d0c68e6b450ffba9e7f778c2771255e0928fb07665dd5e2ecc6b8a1`. La causa non è stabilita e non è dichiarata una correzione del codice o un tasso di affidabilità. I controlli del presente aggiornamento richiedono una verifica distinta.

Pubblicazione autorevole **v600 / conoscenza registrata 1.171**; **sette famiglie e 25 assi incompleti, zero chiusure scientifiche**. H72 resta provvisoria; conoscenza finale e trasferimento integrale su GitHub con recupero remoto rimangono aperti. Nessun merge, deploy o attivazione del portale.

## Aggiornamento verificato: epoca Drizzle 016 e controlli ABE originali eseguiti

Lo snapshot H72 precedente rimane immutato. Dopo la sua creazione, l'epoca Drizzle 016 è terminata e l'istanza è stata chiusa normalmente, con ricevute native e del supervisore e uscita 0. L'audit conta **15.046 casi unici conclusi e 5.674 pendenti su 20.720 (72,6% della sola campagna)**. Non è la percentuale della milestone. Audit: `a3faa8a8fa730206ea67b375f85a970c7a4fca8f092e83270c5cdca416988c1c`.

Sono verificati indipendentemente **58 gruppi completi / 15.022 casi**, più 24 casi conclusi in gruppi parziali. Quindici capsule locali hanno identità e appartenenze disgiunte riconciliate con questa partizione: `Weighted-Drizzle-copertura-archivi58gruppi15022casi-H-v1.json`, SHA256 `4e54bcc8f7a6a4f3344ba4f5d081b3708662f277fe4eded0280e5346838c4947`. Questi controlli non provano calibrazione del rumore reale o recupero remoto.

### Controlli ABE: esecuzione e integrità

I nove input deterministici senza rumore, congelati prima della generazione, hanno prodotto **17 nuovi tentativi nativi**. Il precedente zero/grado 1 con ritorno negativo è escluso e conservato: nessuna ripetizione e nessun modello inventato. I 17 tentativi sono terminati con **14 ritorni positivi e 3 negativi**, senza eccezioni native, con 17 ricevute di caso e di chiusura, zero immagini residue e uscita ordinaria 0. I negativi sono `CTRL_F00_D4`, `CTRL_F01_D1` e `CTRL_F01_D4` (fondo zero/grado 4 e fondo costante/gradi 1 e 4).

Prima dell'esecuzione: worker qualificato con 41 prove simulate, supervisore con 59 e controllo di rilascio con 14; ricostruzione indipendente dei launcher e controllo della versione installata. La fase iniziale è tornata al ciclo eventi senza processi scientifici; due console complete osservate a tempi distinti, identità PID/creazione e percorso del modulo BackgroundModelization caricato con impronta del corrispondente file su disco sono stati verificati prima dell'unico comando nativo. Questo non equivale a verifica delle pagine binarie in memoria o prova generale di affidabilità dell'avvio.

Un primo verificatore statico ha rilevato un confronto dipendente dall'ordine delle chiavi JSON; la versione successiva confronta sorgenti esatte e configurazione JSON strutturale. Errore originario e decisione sono conservati; launcher e casi non sono stati modificati o ripetuti.

L'audit successivo alla vera uscita del supervisore ha riletto **62 immagini XISF e 1.015.808 valori**, verificando payload rispetto ai campioni nativi, input prima/dopo immutati, parametri effettivi rispetto ai blueprint, History iniziale/corrente, ricevute e partizione di non ripetizione. SHA256 audit `15026718749ae6573a7c6a94438221b5da80e28af453eaffcf14011ec1ab0347`. Il decoder è circoscritto ai formati effettivamente riscontrati; non è una certificazione generale XISF.

### Cinque misure e tre ruoli di controllo: risultati circoscritti

L'analisi usa aritmetica razionale esatta sui binary64 conservati, senza errore di somma, nelle regioni whole128, central64 e outer16. Separa X meno modello e uscita nativa Y meno mediana del modello; confronta anche X grezzo con S (correzione omessa) e l'oracolo X meno fondo noto. La correzione omessa resta distinta dall'oracolo. Il limite esatto dell'arrotondamento iniziale S+B è registrato separatamente e non chiamato incertezza stocastica.

| Esito sui rami nativi | Conteggio |
| --- | ---: |
| Varianti per regione complessive | 84 |
| Confronti relativi di flusso con riferimento non nullo | 60 |
| Flusso entro il 5% | 16 |
| Flusso oltre il 5% | 44 |
| Diagnostiche relative L2 con riferimento non nullo | 60 |
| L2 entro il 5% | 18 |
| L2 oltre il 5% | 42 |
| Confronti controllati di modello disponibili | 4 |
| Confronti controllati di modello indisponibili | 8 |

I 24 confronti nativi per ciascuna misura con riferimento nullo restano indefiniti, senza trasformarli in successi. Il quadrato L2 verifica esattamente 400 volte energia residua <= energia del segnale; è una diagnostica di forma nelle regioni dichiarate, non una validazione completa della morfologia. Il flusso verifica 20 volte errore assoluto <= valore assoluto del riferimento. Le diagnostiche del modello sui pixel a segnale esattamente zero non identificano i campioni accettati da ABE.

Le differenze M(B+S)-M(B), proiettate su S, esistono solo dove entrambi i modelli nativi sono realmente disponibili: quattro coppie, tre regioni ciascuna. Le altre otto coppie restano indisponibili a causa del modello di fondo assente, compreso il precedente zero/grado 1. Nessuna sostituzione con zero, inferenza sui campioni accettati o calibrazione stocastica.

Un secondo programma, senza importare il produttore dell'analisi, ricostruisce gli stessi valori tramite interi su una scala comune potenza di due e verifica **186 risultati per misura/regione, 42 diagnostiche del fondo e 12 proiezioni regionali**, incluse indisponibilità e violazioni. Report SHA256 `a456ca233c40581e99ff82ec946f8c036cd770f4b4d2be6e6845598b49f0b5cc`; verifica indipendente `83cf28d08bedea3292c8f895055da8514e228bb189fcb59e0d766fa18f2e4e73`. Nessuna nuova chiamata nativa dall'analisi o dai verificatori.

### Conservazione e requisiti ancora aperti

La capsula `ABE-controlli-originali17-nativi-misure-esatte-verificate-H-v1.zip` contiene **351 file / 10.785.090 byte**. Tutti i membri sono stati estratti e ricalcolati, con confronto alle sorgenti stabili. SHA256 archivio `9c2fba2d18bfd20e1561a7f4895ccf8b8037ad391801e5976c3fd2424a411abf`; manifest `7377217d768cbab7b4554345f0a8887ce200660b6c8390f2af90d2ee580b581f`.

Il recupero è locale. Restano esterni installazione/licenza PixInsight, ambiente Windows/PJSR, registro autorevole, dipendenze dei controlli del supervisore e piena provenienza dell'archivio heldout storico. La capsula include verità numerica, input, parametri, output, ricevute e fallimento precedente; non è dichiarata replay nativo autonomo o recupero da GitHub.

Questi nove campi deterministici impiegano profili già studiati: non sono nuove osservazioni fisiche, campioni rumorosi indipendenti o una coorte morfologica mai vista. Le violazioni del 5% e i ritorni negativi impediscono una promozione generalizzata. **Sette famiglie e 25 assi rimangono incompleti, zero chiusure scientifiche**. Conoscenza finale e passaggio integrale su GitHub con verifica dei byte recuperati restano aperti; pubblicazione autorevole invariata **v600 / conoscenza registrata 1.171**. I CI di questo nuovo aggiornamento devono essere osservati separatamente dai sette successi dell'head H72 precedente. Nessun merge, deploy o attivazione del portale.

## Conoscenza provvisoria H73, rendiconto v55 e recupero verificato

H73 aggiunge due schede alle 212 di H72, preservandole tutte: **214 schede**, gli stessi **4.920 requisiti, 14.521 criteri letterali e 19 criteri dell'Owner**. Una scheda riconcilia i 17 tentativi ABE, i 3 ritorni negativi e le 186 diagnostiche verificate; l'altra fotografa Drizzle chiuso alla sessione 016, con 15.046 casi unici, 5.674 pendenti e 58 gruppi completi. Le sessioni successive attive o preparate non sono conteggiate.

| Artefatto | SHA256 |
| --- | --- |
| Conoscenza H73 | `c29d620f8472e379469e41792fd9c222d7e6b15ff0133ba7b29854235363cd13` |
| Lettore v25 | `ae78ae41f3db6f7a71836c6a4bd74f7ebd0bb201b8b79575481f7cc379851845` |
| Verifica CLI H73 corretta, versione 2 | `9b4a49d1cbb4442a2ff5da254091ba7b80af8f76f515e0861229734e54d05e70` |
| Rendiconto v55 | `6571e16646a31989f269885453dff0438143f288f39e66adfd4ea190bdd23058` |
| Capsula H73 recuperata localmente | `fd40e119247149ab39d143a1d32125d28c93167482ad193f187ceff3b5d8b8f4` |

Il lettore v25 supera 21 controlli CLI, inclusi audit, criteri dell'Owner, interrogazioni storiche e nuove schede e rifiuto di un'impronta errata. La prima ricevuta del qualificatore riportava erroneamente l'impronta H72 nel campo conclusivo, pur avendo interrogato il lettore H73. La riconciliazione del rendiconto ha rifiutato questa discrepanza prima di scrivere. La ricevuta originaria è conservata; il qualificatore corretto ha rieseguito gli stessi 21 controlli in una cartella distinta e registrato l'impronta H73 corretta. Nessun caso nativo ripetuto. Rendiconto v55 prodotto soltanto dopo questa correzione, senza promuovere criteri o stati scientifici.

La capsula H73 contiene **2.531 file / 27.007.075 byte**, compresi conoscenza, lettore, rendiconto, ricevute originali e corrette, evidenze delle sessioni chiuse 015/016, 58 matrici con verifiche e capsula ABE nativa. Ogni membro è stato estratto e ricalcolato, confrontando le sorgenti stabili. L'audit del lettore recuperato coincide esattamente con quello originale: SHA256 stdout `ea888e18c9caabeb94b13ed58ffc7fe8b91425827f0ab7112e2ac6a0bbbefc35`. Manifest `c137ecfd5b8b2f19cd105589c4db6f67aad0175ff58c26a67023b2be4cdb4b8d`. Restano dipendenze esterne della capsula H72 e delle schede storiche, input grezzi e installazione/licenza nativa. Non è recupero da GitHub o replay nativo completo.

### Implicazioni operative ABE circoscritte

La riconciliazione `abe-original-controls-workflow-implications-h-v1/report.json` (SHA256 `bb03d8a0837a690a194e68d9684d5054f1b5ea4af2052836279156f4e6e2e56e`) collega quattro precauzioni ai valori esatti già verificati, senza nuove prove native o selezione retroattiva di parametri:

- Nel profilo Cauchy senza fondo o gradiente, sia grado 1 sia grado 4 superano il 5% su flusso e L2 del campo completo. L'assenza di gradiente non protegge automaticamente il segnale diffuso dalla sottrazione.
- Nelle creste compatte con fondo lineare, il grado 1 passa la diagnostica L2 ma non il flusso; il grado 4 passa il flusso ma non L2. Un grado maggiore o un solo indicatore non selezionano una correzione valida.
- Per creste compatte su fondo zero, il grado 4 passa il flusso su Y nativa meno mediana del modello, ma non su X meno modello. Conservare entrambi gli estimandi; questa differenza non identifica da sola clipping o normalizzazione come causa esclusiva.
- La risposta controllata M(B+S)-M(B) resta disponibile solo per quattro coppie e non è una frazione del flusso totale sottratto, un'inferenza sui campioni accettati o un'incertezza empirica.

Nessuna delle 34 combinazioni caso/estimando dispone di tutte e tre le regioni con flusso e L2 definiti ed entrambi entro il 5%: **questo include regioni con riferimento nullo o modello mancante, che restano indefiniti e non sono automaticamente fallimenti numerici**. L'intersezione descrittiva non sostituisce criteri originari, una validazione morfologica completa o una ricetta universale. Queste sono precauzioni derivate dall'evidenza, non un nuovo algoritmo validato di mascheratura o scelta del grado.

Tutti i sette CI dell'head documentale precedente `d8ed6efa4b6f7ca117125e94bf6442b2b117bda6` sono riusciti; ricevuta `69db0f12c6961c57ddf53c311fcafc288177b4ec9ec906d5caa69cdac62a253b`. I controlli del presente aggiornamento richiedono osservazione separata. **H73 resta provvisoria; sette famiglie e 25 assi incompleti, zero chiusure scientifiche.** Pubblicazione autorevole invariata v600 / conoscenza registrata 1.171. Archivio locale, documentazione remota e CI non provano accettazione scientifica o trasferimento integrale dei byte su GitHub. Nessun merge, deploy o attivazione del portale.

## Evidenze aggiunte in H74: pesi, covarianza e recupero

H74 aggiunge tre schede: sessioni chiuse 017/018 senza duplicazioni; confronto dei tre profili di peso e diagnostica dell'omissione della covarianza sui 60 gruppi precedenti; precauzioni ABE legate ai 17 controlli già eseguiti. Le righe dei requisiti restano identiche salvo collegamenti aggiuntivi a due processi. Nessun criterio o gate scientifico è promosso. I 24 controlli del lettore includono query storiche, nuove schede, audit, criteri dell'Owner e rifiuto di un'impronta errata, con controllo esplicito dell'impronta H74 nella ricevuta.

### Confronto dei tre profili sulle stesse 20 geometrie

Sono ora conservati tutti i confronti a coppie tra uniforme, crescente e decrescente. Ciascun nuovo confronto verifica 2.129.920 coefficienti memorizzati e 156 coppie di aperture tramite un programma indipendente che decodifica binary64 in interi. Le tre coppie riusano le stesse 60 matrici e basi deterministiche: non sono tre campioni indipendenti.

La riconciliazione controlla l'identità esatta delle medesime varianze nelle tre coppie: **96 confronti a tre supportati, 60 senza stima**. Sui valori memorizzati sia di riferimento sia dell'operatore misurato, l'ordine crescente della varianza è:

| Modello dichiarato | Ordine / frequenza sui 32 confronti supportati |
| --- | --- |
| ascending-independent | decrescente < uniforme < crescente: 32 |
| descending-independent | crescente < uniforme < decrescente: 32 |
| unit | uniforme < crescente < decrescente: 4; decrescente < uniforme < crescente: 14; uniforme < decrescente < crescente: 14 |

Non è un ordinamento empirico con incertezza separata né una scelta di pesi ottimali; il risultato cambia con il modello. Report SHA256 `fcb56e814c9ccadc9eee3617264e683d3f88ac8974d611b29089792e72824871`. Capsula di 206 file / 4.614.836 byte, ogni membro decompresso e ricalcolato: `ae3bd1926ef02999c2998f72afc5b1a2480731d4d66861c36d7206998ebf0020`.

### Omissione della covarianza nelle aperture

Un confronto esaustivo posthoc sui 60 gruppi conserva 468 record: **288 combinazioni apertura/modello supportate e 180 senza stima**. Per ciascuna combinazione supportata sono confrontati separatamente riferimento e operatore misurato; questi rami non sono ulteriori osservazioni indipendenti.

Ignorando la covarianza, l'errore supera il 5% in **286/288 confronti sulla varianza** e **280/288 sull'RMS**, con gli stessi conteggi nei due rami. Il calcolo razionale è verificato indipendentemente con prodotti tra interi, 576 rapporti controllati: varianza, 20*abs(diagonale-completa) <= completa; RMS, 361*completa <= 400*diagonale <= 441*completa. Questi sono confronti esatti sui binary64 memorizzati, non varianze analitiche razionali esatte, intervalli di confidenza o prove sul rumore reale.

Report `a6df5dad6628f16b715092814320f19379774971417e753e96a871c5b0569886`; verifica indipendente `30850e2c6df9ff98052d22c9f8fc7bc224af8ece6b7777420adf6e355bdccbca`. Capsula di 135 file / 8.667.066 byte, inclusa senza modifiche la capsula delle matrici: `bb1a33d8ba4c163dbd3ff29f24b41e23f0947174ba1239cb991a8468f9a0cac9`. Modelli dichiarati, maschere fisse e supporto limitano le conclusioni; nessuna accettazione empirica, fisica, adattiva o con normalizzazione locale è inferita.

### H74 recuperata localmente

La capsula H74 include **2.440 file / 29.750.082 byte**, con lettore v26, rendiconto v56, ricevute chiuse 017/018, rapporti di 62 matrici e nuove capsule. Tutti i membri sono estratti e ricalcolati; audit del lettore recuperato identico all'originale.

- Archivio: `2fb614b800e09b2f07708c52c80facb907dfb9c4c27caecbc72b52b8926013c7`.
- Manifest: `65bc66fc815fb0b80b9d5980b1c6e36b3fb408a35d1f6b0674f2ac574dbf2e80`.
- Audit recuperato: `93bb1a60ebd668fcab316329fbfd13dc81db4fa6584ae9ba55de504dc0496eb4`.

La sessione 019 attiva non è inclusa. Restano esterni capsula H73 e dipendenze storiche delle schede, input grezzi e ambiente installato/licenziato. Non è replay nativo autonomo, recupero da GitHub o consegna finale.

I sette CI dell'head H73 precedente `44b2c1b06cf87806f64ca0ab5c00d72cd87c30d4` sono riusciti; ricevuta `e1ef1d4ccf69b5b43ac92269c74a717388a6818c95a0d6f2b2dd04bc6004dd87`. Il nuovo head richiede controlli distinti. Conoscenza finale, condizioni di pubblicazione dei materiali di terzi e caricamento/scaricamento integrale verificato restano aperti. Nessun merge, deploy o attivazione del portale.

## Snapshot storico H74: introduzione conservata

La conoscenza corrente di questo documento è **H74, provvisoria**, con **217 schede**, 4.920 requisiti, 14.521 criteri letterali e 19 criteri dell'Owner. Conserva tutte le 214 schede H73 e i criteri precedenti. La conoscenza registrata autorevole resta separata, **v600 / 1.171**. Sette famiglie e 25 assi sono incompleti, **zero chiusure scientifiche**.

| Componente corrente | Identità |
| --- | --- |
| Conoscenza H74 | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v74.json` |
| SHA256 conoscenza | `6d27eefa5a4612afabca95ca8985790ba37282bccbb786925754695e35d001d7` |
| Lettore v26 | `consult_provisional_dsg_knowledge_h_v5_v26.py` |
| SHA256 lettore | `b6b59e863a9632f74a6868a181c4c06eac2ce314463dff0132a4790d9f1ad412` |
| Qualificazione CLI | 24 controlli riusciti; ricevuta `423d94d5251577f6e2ecf5c1522fa620601f6eace9ab15ba0161cda3a6f97775` |
| Rendiconto v56 | SHA256 `9cac86591b85f748be5d12fd98c1360f4e447407e6b0d085a224ae16fcf9a164` |
| Drizzle chiuso alla sessione 018 | 16.070 casi unici verificati / 20.720; 4.650 pendenti; 62 gruppi completi |
| Archivi dei gruppi | 17 capsule; 16.058 casi nei gruppi completi e 12 nei parziali |

Il **77,6% riguarda soltanto la campagna finita Drizzle**, non la milestone. Sessioni attive successive sono escluse. File di conoscenza finale e trasferimento integrale con recupero remoto dei byte restano aperti; questa pagina documenta gli artefatti e non li carica. Gli snapshot e gli esempi di lettori precedenti conservati nelle sezioni successive sono storici: non sostituiscono le identità correnti della tabella. Nessuna autorizzazione all'esecuzione deriva dalla consultazione della conoscenza.


## H75: quantili certificati e robustezza dei risultati conservati

Le sessioni native 019 e 020 sono chiuse normalmente con uscita 0, zero immagini residue e successivo audit. I 1.024 casi aggiunti non ripetono le identità precedenti. La sessione 021 attiva è esclusa dalla conoscenza H75 e dai conteggi chiusi. Riconciliazione dei 19 archivi contro le identità dei 66 gruppi: SHA256 `4f7c2c96f860211101084f006f5b74598a154a66d135b05a3ff3e7d4c9bf453d`.

### Audit numerico del protocollo statistico a 128 gruppi

I 5.120 casi nativi storici erano già stati confrontati con il rispettivo operatore e le 376 osservabili avevano già superato la compatibilità del modello: non sono ripetuti. Questa compatibilità resta distinta dall'equivalenza entro il 5%.

Il protocollo conservato usa chi-quadro con **128 gradi di libertà** e probabilità per coda **1/15040**. Due metodi distinti con aritmetica razionale certificano un intervallo attorno a ciascuno dei due quantili memorizzati, raggio esatto **2^-30** (circa 9,31323e-10):

1. Serie positiva dell'esponenziale attraverso il termine 256 e limite geometrico della coda.
2. Serie alternata dopo riduzione dell'argomento, con limiti razionali elevati alla potenza intera 128.

Si usa la relazione tra chi-quadro e gamma incompleta e la formula finita per parametro intero, documentate da [NIST](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm) e [DLMF 8.4](https://dlmf.nist.gov/8.4). Report `da8662602a3eee149c829abcf5b85fd9df5cd5c39ae80695a04153e4f24a7c9d`; verifica con metodo alternativo `cdc6cd98de21dd768a905d9f97ca8b107db2fbb3123fbd2449234e2fd0b8ecee`.

Il punto binary64 inferiore conservato è leggermente sopra il quantile esatto; quello superiore è leggermente sotto. I punti e il protocollo originali restano immutati. Non si dichiarano numeri approssimati come quantili esatti.

Anche usando il rapporto minimo consentito dai due intervalli certificati, il rapporto fra estremi dell'intervallo di varianza è maggiore di **2,6205371884**. È superiore al rapporto **21/19** della banda di equivalenza ±5%, e al suo quadrato per l'RMS. Per uno statistico positivo nessun intervallo ottenuto con questa inversione a 128 gruppi può quindi stare interamente nella banda ±5%; le espansioni di arrotondamento conservate non lo restringono. È una dimostrazione condizionata al modello e a questa costruzione di intervallo, non una prova sul rumore fisico o su ogni possibile metodo statistico.

Separatamente, tutte le **376 decisioni positive memorizzate** restano positive anche nell'intervallo di accettazione più stretto consentito dai quantili certificati. Verifiche: disuguaglianze razionali con isolamento del termine a radice e confronto mediante limiti di radice quadrata su griglia 2^-80 ricavati da radici intere. Report `71409baf200d8dbf983e40601d433d20fe79c5fe6388ab1553aa1de791d04f70`. Questo controllo riguarda lo statistico e il margine binary64 conservati e l'incertezza del quantile; **non certifica nuovamente gli arrotondamenti a monte**, l'indipendenza PRNG, il modello gaussiano o la copertura fisica. Nessuna soglia riscritta, nuovo dato confermativo o nuova esecuzione nativa.

La capsula dei quantili contiene 9 file / 133.526 byte, tutti decompressi e ricalcolati: SHA256 `96f81fb3a4badbafb4b4ecf2fab1bab985abc3aeca231ebc1ca0ec1331e9c092`. Il successivo audit delle 376 decisioni è conservato nella capsula H75.

### Recupero H75 e requisiti residui

La capsula H75 contiene **2.471 file / 17.276.996 byte**, con lettore v27, rendiconto v57, ricevute chiuse 019/020, rapporti delle 66 matrici, prove sui quantili e audit delle 376 decisioni. Ogni membro è estratto e ricalcolato; l'audit del lettore recuperato coincide con l'originale.

| Identità | SHA256 |
| --- | --- |
| Archivio H75 | `e7d5a2b3a47d4a320cb516126713ddae6afa64e639105df1f5088f0e9c9e12aa` |
| Manifest | `52c6b31c4d0bcafb86df55bce6b9bb650bd1ed14db51618eea71d2daf329df4b` |
| Audit del lettore recuperato | `a1c69887564d7869f755517ceeccc08569cc6304e279582e6b38c31f02e36375` |

Restano esterni la capsula H74 e le dipendenze delle schede precedenti, gli input grezzi e l'ambiente installato/licenziato. Non è replay nativo autonomo o recupero da GitHub. Tutti i sette CI dell'head H74 precedente `d427a2554c0607add35f6c875530428030020547` sono riusciti; ricevuta `4d9f97dd657f754399afa11ea342f9b4621f253f309894cef7cc2495f4f848af`. Il nuovo aggiornamento richiede verifiche CI distinte.

**H75 resta provvisoria; sette famiglie e 25 assi incompleti, zero chiusure scientifiche.** Condizioni di pubblicazione dei materiali di terzi, conoscenza finale e trasferimento integrale con verifica dei byte recuperati restano aperti. Nessun merge, deploy o attivazione del portale.

## Snapshot storico H75: introduzione conservata

La conoscenza corrente è **H75, provvisoria**, con **219 schede**, 4.920 requisiti, 14.521 criteri letterali e 19 criteri dell'Owner. Tutte le 217 schede H74 sono conservate. L'autorità registrata resta **v600 / 1.171**; sette famiglie e 25 assi incompleti, **zero chiusure scientifiche**.

| Componente corrente | Identità |
| --- | --- |
| Conoscenza H75 | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v75.json` |
| SHA256 conoscenza | `f64a9aa40ded82ff2e33d9cb1ed4c700c3169455ae1ae035a67f14b1831fb45d` |
| Lettore v27 | `consult_provisional_dsg_knowledge_h_v5_v27.py` |
| SHA256 lettore | `21244d074b6ed7f2b3ccc39a68a17b75bd366a99039151390b2f42b776f83e92` |
| Qualificazione CLI | 26 controlli riusciti; ricevuta `5a8586e08e7c74b991bd888b448b1560fbc9e62e5e300aa000333b82055f1518` |
| Rendiconto v57 | SHA256 `930b20c7c80082ecf7f959e05d16a113aaa8a9158b2ce99f67cfacaaed9a842b` |
| Drizzle chiuso alla sessione 020 | 17.094 casi unici verificati / 20.720; 3.626 pendenti |
| Gruppi completi e archivi | 66 gruppi / 17.094 casi; 19 capsule, nessun caso concluso in gruppi parziali |

L'**82,5% riguarda soltanto la campagna finita Drizzle**, non l'intera milestone. Le sessioni attive successive sono escluse. Le sezioni e gli esempi di lettori precedenti sono snapshot storici. Conoscenza finale e trasferimento integrale con recupero remoto dei byte restano aperti: questa pagina documenta gli artefatti ma non li carica. La consultazione non autorizza nuove esecuzioni.


## H76: sessioni 021/022 e separazione dei problemi del fondo

Le due sessioni native sono chiuse normalmente con uscita 0, senza immagini residue e con audit successivo alla ricevuta terminale dell'host. Aggiungono 1.024 identità di caso senza ripetere quelle precedenti. Il punto di ripresa esatto è il rapporto `weighted-bounded-epoch-022-case-audit-h-v1/report-and-exact-pending-cases.json`, SHA256 `450799a9dd3071cd350835f4fc87ff4c54f7281fe16e80f2ff32ce0cf30f94ed`. Il successo nativo non è ammissione scientifica.

La revisione dell'asse DIFFUSE_BACKGROUND/2 corregge un'azione successiva troppo generica, prima concentrata sulle prove ABE. L'asse originario distingue **fondo additivo e variazione moltiplicativa della sensibilità**. La conoscenza aveva già risultati su ambiguità e limiti condizionati nel modello Y=g*S+B, identificabilità con dithering/ancore, bilanci di incertezza su 231 pixel sintetici e ripetibilità dei flat LDN1320 a un solo livello. Questi risultati vanno riutilizzati con i rispettivi domini e limiti, prima di proporre altre prove.

La ripetibilità a un solo livello non dimostra accuratezza del flat, guadagno o linearità del sensore. Il trasferimento ai dati fisici richiede i vincoli misurati di dose ottica e fondo indipendente dichiarati dal protocollo pertinente; non diventano prerequisiti universali per affermazioni matematiche finite. Le prove additive ABE su 3.304 campi e i 17 tentativi senza rumore rimangono evidenze distinte dalla calibrazione moltiplicativa. Revisione conservata: `b0df1654f72135ef42f6e4f2c31d4404930182921c2bb013ed82688aea53d18b`.

La riconciliazione semantica conserva il criterio originale dei processi: validare gli effetti per i domini previsti **oppure documentare un'esclusione esplicita e motivata**. Un risultato negativo può essere una conclusione scientifica utile; non equivale automaticamente a studio non svolto. Questo non autorizza a ridurre il dominio originario o a chiudere automaticamente gli assi: restano da soddisfare controlli, misure, incertezze e limiti previsti. Revisione `615cef78f6f157d4e1b93f4e2393adb7719bb092a124609436e5e81ec49fbfe9`.

Il rendiconto v58 aggiunge soltanto collegamenti circoscritti alle righe DrizzleIntegration e DynamicBackgroundExtraction e aggiorna le azioni operative. Tutti i criteri sono conservati. Il primo produttore v58 si è fermato prima di scrivere il rendiconto per un nome di archivio generato erroneamente; il produttore v2 corregge il riferimento e supera i controlli. Tentativo e correzione restano conservati; nessuna prova nativa ripetuta.


Tutti i sette CI dell'head H75 precedente `eb87ea0257cb11fff8cdce6ddc39bc4063649d29` sono riusciti; ricevuta `9cbea93fb91e05f44d7fbec201889ef9cc3a8301e84c03261204bc1d6e0e6b56`. Questo aggiornamento richiede verifiche distinte. Il recupero locale della capsula H76 è completato: **2.483 file / 17.455.215 byte**, ogni membro estratto e ricalcolato, con audit del lettore recuperato identico all'originale. Archivio SHA256 `a5423680c27e855c1aa56c976a4d43f30e2511276c1360c20061fb60a6e8a6e2`; manifest `5d52c3f34d528fc8ca75bee7467891846bb3e5ac86fd4432a25a1514c03496e3`; audit recuperato `4cfc3a09053daf9e84fd6867ac7f1f0adf03343e880991a6ef51d5bf65c57872`. Include conoscenza, lettore, rendiconto, ricevute 021/022, rapporti delle 69 matrici e revisioni circoscritte. Restano esterni la capsula H75, le dipendenze delle schede precedenti, gli input grezzi e l'ambiente installato/licenziato; non è replay nativo autonomo o recupero remoto. Non è avvenuto un trasferimento integrale degli archivi su GitHub.


## BKL-046: H77 — campagna finita Drizzle completa e pedestal circoscritto (2026-11-14)

Questo aggiornamento supera lo snapshot operativo H76 per le attività qui elencate; conserva le sezioni precedenti come storico. L’autorità pubblicata separata resta v600 / conoscenza 1.171. H77 è provvisoria, non la conoscenza finale: sette famiglie e 25 assi restano incompleti, zero chiusure scientifiche.

- Conoscenza H77: 224 schede; SHA-256 `8b65bca444ee8ba6375d9a965972bb328a9540f058cfe97c7f894569ad0b26b2`.
- Lettore v29: SHA-256 `faafaf4ff1e6cf0cc84861200b100b026aca8aac813b6996a2500153c3c44c39`. Superati 31 controlli CLI, inclusi audit, criteri Owner, interrogazioni delle nuove evidenze e rifiuto dell’impronta errata.
- Rendiconto v59: SHA-256 `40e15482d4f14fd1a4c3bfe0c20efe3078116b73ec6abc48a1a89ed53c51cd98`. Conservati 4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner. Collegamenti aggiunti soltanto a DrizzleIntegration, ImageCalibration e DynamicBackgroundExtraction.

### Drizzle: 20.720 casi e 80 gruppi, nessun caso pendente nel banco congelato

Le esecuzioni effettive terminano con l’epoca 029: 20.720 casi unici su 20.720, 80 gruppi su 80 verificati indipendentemente. Le 27 capsule locali coprono tutti i casi senza sovrapposizioni; nessun caso resta in gruppi parziali. L’ultima istanza PixInsight è uscita normalmente con codice zero, ricevuta conservata e nessuna immagine aperta.

La percentuale del banco finito è 100%; non è la percentuale dell’intera milestone. Le verifiche di matrici, covarianze condizionate e aperture congelate non dimostrano automaticamente accuratezza fotometrica, rumore fisico o validità universale del workflow. Nessuna ripetizione del banco già concluso è richiesta.

La preparazione 028 è stata interrotta prima della qualificazione Node e di qualsiasi avvio nativo: il percorso storico dell’ambiente non esisteva più. Il preparatore v6 cambia soltanto tale percorso; 029 usa gli stessi 42 identificativi ancora pendenti. Conservato anche il fallimento dell’analisi 044, che enumerava impropriamente 028; la revisione successiva esclude esplicitamente questa preparazione senza esecuzione, verificando gli stessi casi e la catena degli audit. L’analisi 045 completa l’ultimo gruppo. Nessun errore è convertito in successo retroattivo.

### ImageCalibration: pedestal, residui con segno e metadati

Sono state completate 24 celle congelate: sei campi deterministici monocromatici Float64 da 128×128 pixel, quattro modalità di pedestal. I 12 oracoli numerici letterali rientrano nella tolleranza numerica prefissata, distinta dal limite scientifico Owner del 5%.

Cinque casi a pedestal letterale zero mantengono il flusso totale entro il 5% ma perdono oltre tale limite nel sottoinsieme dei residui inizialmente negativi. Un residuo di calibrazione negativo non rappresenta fotoni incidenti negativi. Cinque uscite Auto non hanno un header PEDESTAL numerico: assenza e zero restano distinti. Due discrepanze rispetto alla sola frazione negativa non identificano un difetto della documentazione, che cita anche pixel insignificanti la cui definizione interna non è stata dimostrata.

Il primo tentativo è stato rifiutato prima di qualsiasi chiamata di elaborazione: il parametro autoPedestalLimit nominale 0,0001 è restituito in rappresentazione Float32. Una sonda separata di soli setter/getter, senza elaborare immagini, ha attestato tale rappresentazione; il factory corretto usa il confronto Float32 esatto solo per questo parametro. Non è stata introdotta una tolleranza generica.

Una ricostruzione descrittiva successiva, condizionata al valore DN registrato e alla sua normalizzazione Float32, coincide con tutti i pixel di 19 celle ammissibili. Non sostituisce l’oracolo congelato, non identifica l’intero algoritmo e non autorizza una raccomandazione universale di 128 DN.

La capsula pedestal è stata realmente estratta in un albero nuovo: 434 file recuperati e verificati; il verificatore intero portabile, invariato, ha ricalcolato 24 casi e 147 confronti di sottoinsiemi, producendo una ricevuta identica byte per byte. Archivio: 663.397 byte, SHA-256 `2d24cbf312cf4081992543af2f790f0eae9e190cc710fae4b360bcbfc14794a3`. È recupero locale e ricalcolo sui campioni conservati, non replay nativo completo né caratterizzazione fisica delle camere.

### Requisiti residui e conservazione

La mappa dei controlli già esistenti distingue fondo additivo e sensibilità moltiplicativa, dati grezzi X, riferimento X−B, uscita nativa normalizzata Y e sottrazione con segno X−M. Le iniezioni additive e i flat a una sola dose non attestano accuratezza moltiplicativa o linearità del sensore. Le prove ImageCalibration precedenti, la disposizione dei 70 parametri e i relativi falsi ritorni/eccezioni restano conservati.

Tutti i nuovi materiali BKL-046 restano su H:. I criteri originali e il dominio non vengono ridotti; le esclusioni motivate vanno riconciliate con il requisito originale, senza chiudere automaticamente gli assi. File di conoscenza finale e trasferimento integrale GitHub con recupero effettivo dei byte restano aperti. Questo commit documenta gli esiti; non costituisce upload di tutti gli archivi, merge, deploy o attivazione del portale.


### Recupero locale della capsula H77 attestato

La verifica locale è terminata: 5.997 file estratti in un albero nuovo, ogni dimensione e SHA-256 confrontati con il manifest e con le sorgenti; l’audit del lettore recuperato coincide byte per byte con quello originale. Archivio H77: 23.183.318 byte, SHA-256 `7a4910c4dd51c4b362117f0750c6c328fc07c9dedebc44823d3461e6da9c0f53`; manifest SHA-256 `f4e1a8410cd32ebe64cbf168829fc5bc219bc0aeb7a2bcaa89dd84d9af8be2c5`; audit recuperato SHA-256 `23c42f33d2fa537a65feb8b79743448d35f04b43f6bfe732fcc00cefa79f41c0`.

La capsula conserva conoscenza, lettore, rendiconto, ricevute delle epoche 023–027 e 029, 80 rapporti di matrici con verifiche indipendenti e il recupero pedestal circoscritto. Capsula genitore H76, dipendenze delle schede storiche, input grezzi e ambiente installato/licenziato restano separati. Il risultato attesta recupero locale e consultazione; non un replay nativo completo o recupero remoto degli archivi GitHub.


## BKL-046: H78 — riepilogo completo e controlli combinati (2026-11-14)

H78 è una conoscenza provvisoria di 226 schede. Conserva tutte le 224 schede H77, i 4.920 requisiti, i 14.521 criteri letterali e i 19 criteri Owner. Il lettore v30 ha superato 33 controlli CLI, compreso il rifiuto dell’impronta errata. Il rendiconto v60 aggiunge collegamenti alla sola voce DrizzleIntegration, senza modificare criteri o dichiarare chiusure scientifiche.

| Artefatto | SHA-256 |
| --- | --- |
| Conoscenza H78 | `d8a143dddd3c6f158f652099542878a2fbb94d96edf133cebb41331ddc4944c8` |
| Lettore v30 | `f6a99da4e3197f5b5e6ecd246eec5b44e9a9f28c835a9e32dc7b4267d5720893` |
| Rendiconto v60 | `957795a3b5a55e7edcae013995e69bc5cdaca74c8b68406f19c74a02f1ca6ec7` |

### Riepilogo degli 80 gruppi

Il secondo calcolo intero conferma 284.928 confronti sugli endpoint conservati. Le 384 varianze d’apertura supportate sono entro il 5%; 240 aperture restano senza stima. Restano indefiniti 23.808 riferimenti diagonali nulli e 73.680 riferimenti nulli fra vicini: non sono contati come successi relativi.

La capsula del riepilogo è stata estratta in un albero nuovo: 165 file, verificatore intero invariato, ricevuta rigenerata identica byte per byte. Archivio SHA-256 `3356192278b633d40ac3e07449341c4d8245527ae94584f77d0ec2425e8d3ce4`. Sono confronti di operatori finiti e covarianze condizionate, non una dimostrazione della legge di rumore delle acquisizioni reali.

### Sedici controlli combinati di pesatura, rigetto e XNML

Due campi deterministici monocromatici da 64×64 pixel sono riusati nei sedici incroci dei tre interruttori. Si usano griglia identità, kernel Square, coefficienti affini XNML costanti forniti e maschere fissate prima del confronto. La prova non stima coefficienti o maschere dai dati.

Il primo tentativo è stato rifiutato durante l’apertura del primo XISF Float64: mancava l’attributo obbligatorio bounds. Il verificatore offline limitato non controllava tale requisito. Il tentativo, i file e il controllo incompleto restano conservati; l’audit attesta zero chiamate di elaborazione, nessun caso rivendicato e tutti i sedici casi ancora pendenti. Il generatore e il verificatore corretti aggiungono bounds 0:1. Un confronto separato attesta 262.144 byte di pixel invariati; nei sidecar cambiano soltanto i percorsi verso la nuova versione.

Il secondo tentativo, vincolato all’audit del primo, completa sedici chiamate una sola volta. Le ricevute conservano identità degli otto input, parametri prima/dopo, intenti precedenti alle chiamate, campioni, History e chiusure delle sole viste possedute. PixInsight esce normalmente con codice zero e nessuna immagine aperta.

L’analisi razionale e il verificatore intero indipendente concordano su 65.536 pixel: 65.528 pixel supportati rispettano l’ipotesi congelata entro la tolleranza numerica 1e-6 e il confronto relativo descrittivo del 5%; otto pixel interamente rigettati restano senza stima. Non ci sono discrepanze nel supporto previsto. I 24 contrasti appaiati sui controlli grezzi rendono osservabile l’effetto dei sei bit pubblici di rigetto.

L’accordo con l’operatore non equivale all’accuratezza rispetto al segnale noto. Con normalizzazione fornita ma rigetto disabilitato, restano oltre il 5% quattro pixel contaminati senza pesatura e tre con pesatura. I controlli con rigetto e normalizzazione mantengono entro il 5% tutti i 4.095 pixel supportati di ciascuna configurazione contaminata; il pixel interamente rigettato non diventa una misura di flusso zero. Questi confronti non identificano pesi universalmente migliori.

La capsula della prova combinata è stata realmente recuperata: 246 file, verificatore intero invariato e ricevuta identica sui 65.536 pixel. Archivio: 394.125 byte, SHA-256 `1883e1bc88f58ccfcc29c3675ad84615d338318a4ff4a877cc034ee74a6c6c7c`. Il recupero include il rifiuto iniziale; non lo converte retroattivamente in successo.

### Recupero H78 e perimetro residuo

La capsula H78 contiene 100 file / 15.182.895 byte, tutti estratti e verificati in un albero nuovo; l’audit del lettore recuperato coincide con l’originale. Archivio SHA-256 `cc525a24285e5da1da565a42bdc9fb4faf576a489ab47ef8c9291477b4d7dbc3`; manifest SHA-256 `7a9fa69eeea7c7144e113bb5ced8521d1ff61cc819c68c0a4d5cef6cc0ef1a04`.

Le prove native XNML precedenti, i 162 file storici, le verifiche ai bordi e le distinzioni fra livello medio e contrasto restano evidenze esistenti. Non vengono dichiarate mancanti né ripetute per cambiare etichetta. Restano da riconciliare gli effetti combinati nel dominio originale: CFA/Variable15, geometrie non identità, coefficienti spazialmente variabili e incertezza dei modelli effettivamente stimati. Nessuna FWHM stellare è definita nei due campi correnti, quindi non si dichiara accettazione di posizione.

Autorità separata ancora v600 / conoscenza 1.171; sette famiglie e 25 assi incompleti, zero chiusure scientifiche. I criteri originali non impongono che ogni controllo intenzionalmente errato rispetti il 5%; richiedono esiti, limiti ed eventuali esclusioni motivati nel dominio previsto. Dipendenze delle schede storiche, capsula genitore H77, input grezzi e installazione restano separati. Il recupero locale circoscritto non è replay nativo completo né trasferimento integrale GitHub con recupero dei byte. Tutti i nuovi materiali restano su H:; nessun merge, deploy o attivazione del portale.


## BKL-046: H79 — XNML spaziale, aperture e ipotesi al bordo (2026-11-14)

La conoscenza provvisoria H79 contiene 228 schede e conserva tutte le 226 schede H78, i 4.920 requisiti, i 14.521 criteri letterali e i 19 criteri Owner. Il lettore v31 supera 35 controlli CLI. Il rendiconto v61 aggiunge soltanto evidenze alla voce DrizzleIntegration; sette famiglie e 25 assi restano incompleti, zero chiusure scientifiche.

| Artefatto | SHA-256 |
| --- | --- |
| Conoscenza H79 | `bda25f8dd59c7fdfee96c17f7777f2b25209b3914c2c19fa46fc9e95e48cc47b` |
| Lettore v31 | `fbe218273f30ae15854cad361fc6a286c9a301fcc856b69c93cb16c080811fba` |
| Rendiconto v61 | `385bdc56e4705fc5a6aa40e8bd2fdf906e73af13d4b60e547de56ef8fd308d63` |

### Nuovo controllo combinato con coefficienti spazialmente variabili

Sedici nuove configurazioni incrociano pesatura, rigetto e normalizzazione su due campi mono 64×64 con piani Scale e ZeroOffset variabili da 4×4 nodi. Il riferimento usa l’interpolazione B-spline pubblica, comprese le regole ai bordi; fonte pubblica e identità del binario installato restano affermazioni distinte. Il modello e l’alternativa diagnostica sono congelati prima dell’esecuzione.

Sono condizioni diverse dal precedente controllo a coefficienti costanti: non vengono ripetuti i vecchi casi né conteggiate le varianti come acquisizioni indipendenti. Coefficienti e maschere sono forniti, non stimati sui dati. Restano separati CFA/Variable15, geometrie non identità, stima dei modelli reali e rumore fisico.

Gli input registrano i valori ideali e quelli realmente salvati, con limiti di mezzo ULP verificati indipendentemente per entrambe le operazioni: inversione della trasformazione e aggiunta del contaminante. Due incrementi nominali di 1/16 differiscono dalla quantità effettivamente salvata dopo l’addizione Float64. Il riferimento usa i campioni conservati; questa differenza non è presentata come rumore del sensore.

PixInsight completa sedici chiamate e chiude normalmente senza immagini residue. Sono conservati 131.072 valori di uscita con ricostruzione dei relativi hash. L’analisi razionale e il verificatore intero indipendente concordano sui 65.536 pixel: 65.528 supportati rispettano il modello congelato entro 1e-6; otto pixel interamente rigettati restano senza stima. Interno, ultima cella orizzontale dei coefficienti e altri bordi sono rendicontati separatamente, senza selezionare soltanto le regioni favorevoli.

### Aperture: accordo con l’operatore e accuratezza del segnale

Le 32 aperture fissate prima del test mantengono geometria e denominatori originali. Le 24 supportate concordano con l’operatore entro il confronto relativo del 5%; dodici concordano anche con il segnale noto, mentre dodici controlli intenzionalmente privi di normalizzazione superano tale soglia. Otto aperture di campo completo contengono il pixel interamente rigettato e restano senza stima. L’apertura centrale è fissata a priori e non sostituisce retroattivamente quella completa.

Questi esiti verificano una composizione finita di coefficienti forniti, pesi e maschere. Non attestano l’accuratezza dei coefficienti stimati da immagini reali, una legge di rumore o la risposta fisica delle camere. Nei campi non esiste una FWHM stellare di riferimento: nessuna accettazione di posizione è dedotta da queste prove.

### Il 5% non identifica l’interpolazione

L’alternativa CLAMP_ALL era prevista dal protocollo come diagnostica. Nella cella orizzontale finale, su otto configurazioni con normalizzazione attiva, sono confrontati 8.192 endpoint conservati. Il modello primario rispetta la tolleranza numerica in tutti; CLAMP_ALL la supera in 6.656. Tuttavia entrambi restano entro il 5% relativo su questi endpoint.

Un secondo verificatore ricostruisce CLAMP_ALL con polinomi e tabelle intere dei bordi e conferma tutti i conteggi. L’alternativa non sostituisce l’ipotesi primaria; il confronto mostra perché identità numerica dell’implementazione e soglia scientifica relativa vanno dichiarate separatamente. Gli endpoint condividono due campi deterministici e non sono 8.192 osservazioni indipendenti.

### Recuperi locali e stato del passaggio GitHub

La capsula della prova spaziale è stata realmente estratta: 184 file, ricalcolo intero invariato dei 65.536 pixel e delle 32 aperture, ricevuta identica. Archivio: 3.105.990 byte, SHA-256 `6d29d0574cd09630befabebb44675d0a9535899812725ed519909429cbb5259d`.

Anche la diagnostica del bordo è recuperata e ricalcolata: 33 file, 8.192 endpoint, ricevuta identica; archivio SHA-256 `7c14dbfc32d48eeb98798a5bfbf565895907eabd3e5c667be25f62b8ade7207a`.

La capsula H79 contiene 102 file / 14.663.005 byte, tutti estratti e verificati; l’audit del lettore recuperato coincide con quello originale. Archivio SHA-256 `3546220bafb052f118ab4a5e5f5c68232a1a9771bdfa7d964e501bd2f49d1b1b`; manifest SHA-256 `c22e9c8961adaa0cadbd09fbac8593d58d2f0c4984ffdeafedae5ed32b3d6c48`.

Autorità separata ancora v600 / conoscenza 1.171. H79 non è il file finale. Capsula genitore H78, dipendenze storiche delle schede, input grezzi e ambiente installato/licenziato rimangono separati. Questi recuperi locali non attestano un replay nativo completo né il trasferimento integrale GitHub con recupero remoto dei byte. Tutti i nuovi materiali BKL-046 restano su H:. Nessun merge, deploy o attivazione del portale.


## H80 — campionamento gaussiano condizionale, isolamento e arrotondamento (14 novembre 2026)

H80 conserva tutte le 228 schede H79 e aggiunge tre schede, per **231 schede**. Rimangono integri **4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner**. Tutte le sette famiglie e i 25 assi scientifici rimangono aperti, senza chiusure scientifiche.

### Disegno statistico: certificato ideale, nessun nuovo esperimento

Per 384 endpoint supportati ad apertura fissa, con media nota e contrasti gaussiani ideali indipendenti fra ripetizioni, è stato derivato il limite di Chernoff e applicata l'unione di Bonferroni. Con N=65.536 e delta=1/40, il limite superiore conservativo sulla probabilità di mancata copertura simultanea è 0,027739236849192408, inferiore a 0,05. Un verificatore indipendente con parametri di Chernoff diversi produce anch'esso un limite inferiore a 0,05. Non occorre indipendenza fra endpoint; resta necessaria quella fra ripetizioni per ogni endpoint.

Questo N è sufficiente per il certificato scelto: non è un minimo dimostrato, una garanzia di potenza o la promessa che i dati supereranno la soglia. Per contenere l'intero intervallo ideale di varianza nel ±5% Owner, il rapporto osservato T/V0 deve cadere in [779/800,819/800]. Nessun rumore nuovo è stato generato. Il criterio Owner sul rischio di decisione IA (1% con confidenza 95%) resta distinto.

Certificato SHA-256: `d93cd6f0f4505b9015429dcf5957a4c9c395a4d954165efafb0dd17ebba3f261`. Il riferimento primario per la distribuzione chi-quadro è il [NIST Engineering Statistics Handbook](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm); limiti e aritmetica del disegno sono derivati e verificati localmente.

### Isolamento geometrico e margine numerico

Il modello Square esatto sulle aperture centrali ricostruisce 6.784 righe supportate, mantiene 1.536 righe prive di supporto e non trova contributi da tile esterni. La verifica indipendente usa una griglia intera a 120 unità e controlla 480 margini geometrici, includendo i parametri arrotondati binary64/binary32. Traslazioni di otto pixel preservano la parità CFA. L'indipendenza dei contrasti di riferimento segue solo condizionatamente a variabili d'ingresso indipendenti; non è una prova dell'indipendenza di un generatore pseudocasuale o dell'operatore nativo su immagini più grandi.

Per 128 aperture supportate sono stati calcolati esattamente i moltiplicatori degli errori assoluti d'ingresso e d'uscita; 80 configurazioni di apertura non supportate restano escluse. Se la discrepanza RMS fra contrasto reale e ideale è limitata da epsilon, la disuguaglianza triangolare propaga tale margine nell'intervallo statistico. Il verificatore intero indipendente ricostruisce coefficienti e sei esempi di propagazione. **Il limite effettivo dell'errore nativo e il collegamento fra generatore e distribuzione ideale non sono ancora dimostrati.**

Rapporto isolamento SHA-256: `55df58cc4656ff42566980921e1682664767b61e2c9cef04307da7fd5a91f1bd`.
Rapporto margine numerico SHA-256: `c498d4f7ea2d54083cd9ca6e751dce105b94450faa3ee127ae18571638788153`.

Il candidato a tile richiederebbe 240 chiamate native per tre modelli, quattro profili e venti geometrie; questo numero è distinto dai 65.536 contrasti per endpoint. Non è stato rilasciato all'esecuzione. Prima occorrono qualificazione del generatore e dei suoi limiti, margini numerici verificati e una prova nativa limitata di traslazione/supporto, formato, memoria e scrittura. Restano separati acquisizioni fisiche, rumore non gaussiano, normalizzazione stimata e validazione delle decisioni IA. I casi già completati non vanno duplicati.

### Conoscenza, lettore e conservazione

- H80 SHA-256: `f934cce8bbffa0a358f9f324cedd9f51575cb451fda100fc93a719e45b3db9ef`.
- Lettore v32 SHA-256: `53b15901edde1a9db6ce4293effcf72f16302141620aa1d5bf2f464fcaa33c45`; tutti i 38 controlli CLI superati, inclusi i 35 precedenti e il rifiuto di impronta errata.
- Rendiconto v62 SHA-256: `9175edf59e14ee1920736e86309504949226415917df6b1780d7a655021c4081`; una sola riga di requisito riceve collegamenti aggiuntivi, senza modificare criteri o ammissione scientifica.
- Capsula locale H80: 105 file, 9.591.483 byte; SHA-256 `07463b058137921bc58afa18ac2a5a89eaa1d10103729f1fbdc58f5f0121c8f8`, manifest `94d647f990b1bc6391cf08f1a483ccfc85837f10b0014b5cd5586b531e8190c4`. File estratti e riverificati; audit del lettore recuperato identico.
- Capsula del margine numerico: nove file, 579.036 byte; SHA-256 `35934f1f0b4d274848eddb287a6d1db19ee5cf036717b7ecbd57d9158265a115`. Verificatore indipendente eseguito dai file recuperati, prova identica all'originale.

Autorità separata verificata: v600 / conoscenza 1.171, nessun publisher attivo al controllo. H80 è provvisoria. Genitore H79, dipendenze storiche, input grezzi e ambiente installato/licenziato restano esterni alla capsula incrementale. Recupero locale e controlli GitHub non provano il trasferimento completo con recupero remoto dei byte. Nessuna nuova chiamata nativa, nessun nuovo campione di rumore, nessun merge o deploy in questo incremento. Materiali BKL-046 conservati su H:.


## H81 — prova nativa di traslazione a tile e controllo Float32 (14 novembre 2026)

H81 conserva tutte le 231 schede H80 e aggiunge due schede, per **233 schede**. Il lettore v33 supera **40 controlli CLI**, inclusi i 38 precedenti. Il rendiconto v63 conserva **4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner**; aggiunge collegamenti su una sola riga di requisito, senza promozioni scientifiche. Sette famiglie e 25 assi rimangono aperti.

### Dalla previsione al controllo nativo a 64 pixel

È stata conclusa la prova deterministica prima indicata come prerequisito: quattro ingressi monocromatici a 64×64 pixel, organizzati in 64 tile di lato otto, venti geometrie Square e quattro profili di peso, per **80 integrazioni native uniche**. Le geometrie includono mono e quattro pattern CFA, scale 1/2 e drop 11/20 o 17/20. Un ingresso RGB sentinella distinto controlla l'associazione del vero ingresso CFA; non costituisce una quinta esposizione scientifica.

I valori attesi sono congelati prima dell'esecuzione. Il verificatore indipendente ricostruisce la geometria su griglia intera a 120 unità, senza leggere la matrice dei coefficienti salvata. La prova usa valori positivi deterministici esattamente rappresentabili in Float64: non genera rumore e non produce ripetizioni statisticamente indipendenti.

Esiti nativi, controllati anche con un secondo verificatore a interi sui valori binari salvati:

| Misura nel perimetro congelato | Esito |
| --- | --- |
| Valori supportati confrontati | 434.176, tutti entro 10⁻⁶ assoluto e il 5% del modello |
| Valori previsti senza supporto | 98.304, conservati senza stima |
| Aperture supportate | 8.192, tutte entro il 5% del modello e il limite numerico propagato |
| Aperture senza stima | 5.120 |
| Discrepanze di supporto | 0 |
| Valori nativi di uscita ricostruiti e verificati mediante SHA-256 | 4.259.840 |

Lo scostamento assoluto massimo dal riferimento nominale è esattamente 627527/14857902489600, circa 4,22352347809×10⁻⁸. Le 532.480 decisioni sui pixel selezionati e le 13.312 decisioni sulle aperture sono state ricalcolate indipendentemente. Il conteggio include esplicitamente i casi senza stima; questi non diventano successi o verità scientifiche pari a zero.

L'istanza isolata è stata chiusa normalmente dopo il salvataggio, senza viste residue e senza ripetere casi già conclusi. Massimo impegno privato osservato nei 169 campionamenti del controllo: 970.457.088 byte. È un massimo campionato su questa sessione, non un picco OS certificato né una previsione per immagini di lato 2.048.

Rapporto esatto SHA-256: `7c05abae563605a4b60593115c9a0d42dab3ece8363d2ea6cbd99b4bcf3e2e92`.
Verifica intera indipendente: `5e4bc0aacfb18785918039bf0e7bc6dfe6bb33295329459f431b99f3d310a188`.
Audit di integrità e partizione senza ripetizioni: `2f7228bae17a3cb0496a14a2a1d576d8b016f5bbdac86c723bcdaae4f5ae8425`.

### Errore emerso e correzione circoscritta

Il primo tentativo ha letto correttamente i cinque file d'ingresso ma si è fermato al controllo del parametro, con **zero integrazioni native**. Il getter di dropShrink restituisce 0,550000011920929 e 0,8500000238418579: valori osservati uguali alla conversione Float32 dei nominali 0,55 e 0,85.

Il nuovo controllo accetta esclusivamente questa rappresentazione verificata per dropShrink e conserva separatamente valore richiesto e valore nativo. Nessuna tolleranza generica viene aggiunta agli altri parametri. Geometria razionale, risultati attesi e soglie restano invariati. Il primo tentativo, la lettura del getter e la chiusura normale rimangono conservati, con audit SHA-256 `8c277657c765e373f69186f8b98fc08b0752926f6031cb28c6f9672d37d4612e`.

Prima del secondo tentativo sono superati, in simulazione, 147 controlli di configurazione, 22 dell'esecutore, 56 del processo ospite e 14 del rilascio. Questi controlli attestano i rispettivi vincoli operativi; i risultati numerici derivano invece dalle 80 esecuzioni reali e dai verificatori separati.

### Riuso dei componenti gaussiani già conservati

Sono stati riletti e verificati tramite impronte il controllo dei quantili, il decoder dei valori binari e le ricevute storiche della sorgente Windows CNG. Non vengono descritti come mancanti né rigenerati. Le prove storiche comprendono 65.536 fixture deterministiche del controllo dei quantili e 132.452 confronti esatti del decoder.

Per le 128 configurazioni di apertura supportate risultano al massimo 81 variabili d'ingresso. Condizionatamente al limite di approssimazione del quantile 2⁻⁴² per variabile standardizzata, Cauchy–Schwarz limita il solo contributo normalizzato di quel termine a **9/4398046511104**. Questo non esaurisce discretizzazione dei valori binari casuali, code, conversioni, scaling, somma e aritmetica nativa. Provenienza e replay CNG non provano indipendenza, uniformità ideale o trasferimento quantitativo della probabilità di errore.

Rapporto di riuso SHA-256: `45575beb5e4138059a7164ac5279591e8f7d3bbe99f15a9902287a3a792ff322`. Nessun nuovo valore casuale generato da questa riconciliazione.

### Conoscenza e archivi locali recuperati

- H81 SHA-256: `82577399813cc352552ff9b97d4aabada39ef52f4768872159af736a27a20ade`.
- Lettore v33 SHA-256: `f878ec2c2fe9b5e18578759dc661dfacb7c90632fee7227f2e017a89537df17e`; verifica dei 40 controlli `e060c7e265d5fbab8f6aa420a7c2b213ac90bdc6860e855b1f6fe24e4f6ab86e`.
- Rendiconto v63 SHA-256: `6713bb6495356aad2b30c6bf3d468f0f2d8bdf3b0401afc0338678b373e62de3`.
- Capsula delle prove native: 795 file, 19.368.696 byte; SHA-256 `24a5750e496fb2acbc53499c578f50b89969c82055fdcbbb83eace97fed1ac82`, manifest `c7189c15a465270b594a78dcbaf3e6bf2510251b3a66a45e512197afbd7ee907`. Estrazione effettiva, impronte verificate e ricalcolo intero identico dai file recuperati.
- Capsula incrementale H81: 118 file, 28.571.138 byte; SHA-256 `ca32a605573f915285a0baecf22fa37731b0bd58701c6bae5fb40bfdf72e5bf8`, manifest `dd1aa62127123a1fc34063516f34ee5f19eee470c351a04b245703655dfa5ed8`. Estrazione effettiva e audit del lettore recuperato identico.

La prova di traslazione deterministica a 64 pixel è conclusa e non va ripetuta. Rimangono da qualificare comportamento e risorse su immagini di lato 2.048, limiti numerici sull'intervallo di ampiezze pertinente e collegamento statistico completo del generatore alla campagna sul rumore. Restano distinti rumore fisico delle camere, normalizzazione stimata e rischio delle decisioni IA. Questa prova non convalida tali ambiti.

H81 resta provvisoria; l'autorità separata rimane v600 / conoscenza 1.171. Genitore H80, dipendenze storiche e ambiente installato/licenziato rimangono esterni alla capsula incrementale. Il recupero locale non attesta il trasferimento integrale degli archivi su GitHub con recupero remoto. Tutti i nuovi materiali BKL-046 rimangono su H:. Nessun merge, deploy o attivazione del portale.


## H82 — due casi nativi a 2.048 pixel e dominio statistico originario (14 novembre 2026)

H82 conserva tutte le 233 schede H81 e aggiunge due schede, per **235 schede**. Il lettore v34 supera **42 controlli CLI**, inclusi tutti i 40 precedenti. Il rendiconto v64 conserva **4.920 requisiti, 14.521 criteri letterali e 19 criteri Owner**; una sola riga riceve collegamenti aggiuntivi. Le sette famiglie e i 25 assi scientifici restano aperti, senza chiusure scientifiche.

### Risorse e trasporto nativo su immagini più grandi

Sono conclusi due casi deterministici con quattro ingressi mono di lato 2.048 e un distinto file RGB sentinella per controllare la selezione CFA:

- mono, geometria 03, scala 2, drop nominale 17/20, pesi descending-common;
- RGGB, geometria 06, scala 2, drop nominale 11/20, pesi channel-skew.

Il sentinella non è una quinta esposizione scientifica. I 29.360.128 valori dei cinque file d'ingresso sono verificati indipendentemente mediante lettura binaria a righe. Le aspettative geometriche sono congelate prima dell'esecuzione e ricostruite indipendentemente su griglia intera a 120 unità.

Ogni caso produce immagini di lato 4.096. I valori nativi sono conservati in otto piani Float32, un canale alla volta, con rilettura e verifica SHA-256 prima di salvare la ricevuta e chiudere le viste. Sono conservati separatamente History, metadati, parametri nominali e valori restituiti nativamente. Questo evita di costruire grandi liste JSON contenenti tutti i campioni.

L'audit ricostruisce **536.870.912 byte / 134.217.728 valori di uscita**, senza valori non finiti. Questi sono valori decodificati, non altrettanti test o acquisizioni indipendenti.

Nei 123 campionamenti del controllo del processo, il massimo impegno privato osservato è **1.614.733.312 byte**. Non è stato richiesto alcun arresto per memoria. È un massimo campionato dell'istanza, non un picco OS certificato o una garanzia per tutte le configurazioni della campagna futura. L'istanza è uscita normalmente, senza immagini residue e senza ripetere casi conclusi.

### Confronto limitato alle regioni congelate

Per ciascun caso sono prefissati 16 tile diagnostici, comprendenti bordi, angoli e regioni interne. Il confronto esatto e il verificatore indipendente che decodifica i bit Float32 concordano:

| Quantità nel perimetro dichiarato | Esito |
| --- | --- |
| Valori supportati selezionati | 3.072, tutti entro 10⁻⁶ assoluto e il 5% del modello |
| Valori senza supporto | 1.024, conservati senza stima |
| Aperture supportate | 16, tutte entro il 5% del modello e il limite numerico propagato |
| Aperture prive di stima | 48 |
| Discrepanze di supporto | 0 |

Massimo errore assoluto nel caso mono: 100709/2476317081600, circa 4,06688629450×10⁻⁸. Nel caso RGGB: 9039/973078528000, circa 9,28907558836×10⁻⁹. I casi privi di stima non vengono convertiti in successi, zeri scientifici o aperture adattivamente ridotte.

Le verifiche geometriche coprono **4.096 decisioni sui valori selezionati e 64 decisioni sulle aperture**, includendo i casi senza stima. Non costituiscono un confronto numerico di tutti i 65.536 tile, né di tutte le configurazioni del candidato statistico.

Audit dei piani nativi SHA-256: `c2efc082084e3f06a6e72a1ca57f4c6a01a07400214dfac17e101dd1ff7e8ae5`.
Rapporto del confronto selezionato: `f6f6fe31c213eff62d1ddb26c19a89d732959cbb168b386ad118b87fe02e4ae1`.
Verifica intera indipendente: `de80da8019233bb28b8ad7396d2f80cec71f3a77802f3794e5d2f3e5805c4a09`.

### Definizione mancante e diagnosi conservata

Il primo tentativo è terminato con ReferenceError per UndoFlag_NoSwapFile, prima di creare immagini o eseguire i due casi grandi. Mancava nel lanciatore il caricamento di `pjsr/UndoFlag.jsh`. Il file installato è stato letto e verificato tramite impronta, senza modificarlo.

Una diagnosi separata nella stessa istanza, con l'include esplicito, verifica il formato little-endian e il salvataggio/rilettura di quattro immagini piccole: mono/RGB a 32/64 bit, otto piani e 96 valori esatti, oltre ai due test di layout binario. Tutte le viste vengono chiuse dopo la conservazione. La sessione corretta ripete il controllo preliminare nel proprio processo prima dei due casi grandi. Sono verifiche tecniche di trasporto, distinte dalle integrazioni scientifiche.

L'errore iniziale, la diagnosi e la nuova sessione rimangono separati. Un ulteriore errore nel test simulato di arresto parziale — tre casi su un piano da due — è conservato e corretto a un caso concluso. Il controllo del processo supera 61 fixture e il rilascio 14; non vengono allentate le soglie numeriche o sostituiti gli ingressi.

Audit del tentativo iniziale e della diagnosi SHA-256: `a227394c94a548090a2f6c134b19f8607cd6a7fdf61941235b6865997e5596d6`.

### Le quattro classi originarie del rumore restano nel piano

La rilettura del protocollo statistico originario conserva:

| Osservabile | Endpoint originari disponibili |
| --- | ---: |
| PIXEL | 104 |
| PAIR_MEAN | 104 |
| PAIR_DIFFERENCE | 104 |
| RECTANGLE_MEAN | 64 |

Restano inoltre le 40 aperture originarie non disponibili. Le **5.120 integrazioni native storiche e i 376 esiti di compatibilità** sono preservati; non devono essere rigenerati o descritti come mancanti.

Il certificato ideale sui 384 endpoint ad apertura fissa conserva la propria validità condizionale, ma **non copre da solo le tre classi pixel/coppie del dominio originario**. L'analogia fra aperture nuove e RECTANGLE_MEAN non dimostra l'identità dei selettori, delle varianze d'ingresso o delle configurazioni. Restano esplicite anche le 16 configurazioni CFA storiche a pesi disuguali che non hanno un abbinamento di metadati con i quattro nuovi profili.

Prima di nuovi valori casuali occorre congelare un manifest completo degli endpoint, riconciliare selettori, colonne sorgenti, modelli di varianza e pesi, ricalcolare numerosità e copertura simultanea per quella famiglia e completare il margine del generatore e dell'aritmetica nativa. Non si riusa 384 come conteggio globale. Nessuna nuova campagna sul rumore viene rilasciata da questi due casi di risorse.

Rapporto di riconciliazione del dominio SHA-256: `1d63d588b0ab07fbaaf4ef81535f17f19ae17a88b7bb7c21c7ff1c54c47c2548`.

### Conoscenza e recupero effettivo degli archivi locali

- H82 SHA-256: `518d8c2075ee54999b5b197b5be498e424918424b896c2b92ca4024c0170e57f`.
- Lettore v34 SHA-256: `00931a900c3870310bf0a78bdb2302aede9050176310d33775cb291abb3e7bec`; verifica dei 42 controlli `5a05a83bb75c58530d636ca8f90591396dd29e1ef3972f8d1c8845cb6255c41b`.
- Rendiconto v64 SHA-256: `546e96e260c3b940b090656f292d8f5c254979cd63d9e94c959fecd091d8b03c`.
- Capsula delle prove native: 190 file, 226.113.010 byte; SHA-256 `41082896799b8b21d7b963923e8ab719d46f0c669ba21f2ee0d9fdbd4197c8dc`, manifest `2b3299d27d59f485b8b944bf5f968f14270594656b8cd21ee65dae6db6d8987c`. Estrazione effettiva e impronte verificate; ricalcolo intero selezionato identico dai file recuperati.
- Capsula incrementale H82: 124 file, 233.981.932 byte; SHA-256 `490147f62b4641c550876a648c4d802d0e33ed0427dc704252df058e9cf9c533`, manifest `161ae61d8d9929a60794afda0be5136397681f1de17d8c0822dab4a9555fec63`. File recuperati e audit del lettore identico.

H82 resta provvisoria; autorità separata v600 / conoscenza 1.171. La capsula genitore H81, le dipendenze storiche e l'ambiente installato/licenziato rimangono esterni alla capsula incrementale. Il recupero locale non attesta un replay nativo completo né il trasferimento integrale degli archivi su GitHub con recupero remoto dei byte.

Questa fase conclude due casi deterministici di risorse e i loro confronti selezionati. Non convalida il rumore fisico delle camere, errori numerici per ampiezze generali, normalizzazione stimata, tutte le configurazioni statistiche o il rischio delle decisioni IA. Tutti i nuovi materiali BKL-046 restano su H:. Nessun merge, deploy o attivazione del portale.
