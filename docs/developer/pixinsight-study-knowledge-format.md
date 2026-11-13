# Conoscenza dello studio PixInsight e IA: struttura, consultazione e storico

## Stato e perimetro

Questo riferimento descrive la conoscenza consolidata **provvisoria H54** dello studio BKL-046. Il suo formato rende consultabili risultati, condizioni, errori ed evidenze; non costituisce un'autorizzazione a eseguire processi PixInsight né una baseline scientifica finale.

Snapshot del 13 novembre 2026:

| Componente | Identità |
| --- | --- |
| File di conoscenza | `Conoscenza-consolidata-provvisoria-DSG-PixInsight-IA-h-v54.json` |
| SHA-256 del file | `df06e52a008c910fcdff6d5061c75de3d97cd738f2ac6abc01b162350ac83792` |
| Lettore | `consult_provisional_dsg_knowledge_h_v5_v6.py` |
| SHA-256 del lettore | `29d9cccdfa3b1667013bd945cfe58a4713449f13df494b928f8078d1c1c6f69f` |
| Formato | `schemaVersion: 1` |
| Stato | `PROVISIONAL_CONSOLIDATED_QUERYABLE_NO_SCIENTIFIC_PROMOTION` |
| Requisiti | 4.920 |
| Schede di evidenza | 173 |
| Famiglie / assi / criteri Owner | 7 / 25 / 19 |
| Chiusure scientifiche | 0 |

Il registro autorevole preesistente, attestato alla versione v1.171, resta distinto da H54. Una versione provvisoria non aggiorna quel registro e non riavvia il publisher. Tutti i vincoli su portale, master, installazione, migrazione Codex e M27 restano applicabili.

Questa proposta pubblica la documentazione del formato. I file JSON, i lettori e gli archivi grezzi identificati dagli hash non sono caricati da questa pagina: il loro trasferimento completo e recupero remoto restano da attestare.

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

- `residual`: identificatore, criteri letterali, impronta della riga autorevole, disposizione e azione residua;
- `matrixRecord`: stato canonico e relativo contesto;
- `semanticRecord`: lettura semantica e storia delle matrici precedenti;
- `additionalScopedEvidenceIds`: supplementi consultabili per quel requisito;
- l'eventuale `documentaryAttestation`, con la portata documentale dichiarata.

I supplementi non riscrivono automaticamente gli stati canonici. H52 ha collegato 17 requisiti esatti alle nuove evidenze; H53 ha aggiunto collegamenti per l'oggetto File e quattro suoi membri; H54 collega agli stessi cinque requisiti anche il recupero locale della capsula File IO. H54 aggiunge inoltre il contesto operativo successivo ai vecchi gate del backend e il riesame delle fonti primarie di pubblicazione, conservando le conclusioni storiche nel loro ambito. Gli altri campi dei requisiti sono stati confrontati nella loro rappresentazione canonica: matrici, criteri, disposizioni e storia non vengono promossi tramite l'aggiunta di una scheda.

## Consultazione riproducibile

I comandi seguenti si eseguono sul pacchetto recuperato contenente file e lettore verificati. Non sono endpoint del portale.

```text
python consult_provisional_dsg_knowledge_h_v5_v6.py --audit
python consult_provisional_dsg_knowledge_h_v5_v6.py --workflow process:ACDNR
python consult_provisional_dsg_knowledge_h_v5_v6.py --role pjsr_object:File
python consult_provisional_dsg_knowledge_h_v5_v6.py --workflow pjsr_object:File
```

Il lettore predefinito verifica l'impronta esatta di H54 prima della consultazione. Per un altro file occorre fornire esplicitamente `--file` e `--sha256`; l'impronta di una versione diversa non è accettata.

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

Dei 1.982.768 record storici, 1.982.764 hanno un percorso corrente: 1.982.762 conservano anche la dimensione e due hanno dimensione diversa; quattro percorsi risultano ritirati. Stessa dimensione e stesso percorso non provano l'identità dei byte. I due casi mutati hanno copie esatte precedenti; i quattro ritirati sono ricostruibili dal contenitore e dal decoder identificati. La composizione conclusiva delle sei fonti supplementari attende il termine dell'audit completo su 498.056 identità di contenuto storico.

Un controllo distinto del manifest autorevole v599 ha individuato 1.990 contenuti unici ancora rappresentati da fonti storiche su C. Sono stati copiati su H e ricontrollati sull'origine e sulla destinazione: **7.355.344.930 byte**, conservando nomi, provenienza e identità dei file. Le fonti C e il registro preesistente restano al loro posto. Si tratta di archiviazione dei dati dello studio, senza migrazione dell'installazione Codex.

La proposta documentale per i 239 oggetti PJSR ha tutte le **1.789 identità di citazione diretta** collegate a fonti correnti verificate, corrispondenti a 1.524 identità di contenuto. Questa verifica non è una nuova revisione semantica di ogni contenuto né una chiusura transitiva delle dipendenze.

Il pacchetto preparato comprende 1.462 artefatti e 239 modifiche di riga. Una verifica indipendente ha riletto tutti i 204.573.660 byte sorgente e riprodotto la trasformazione: le altre 4.681 righe restano invariate. I dati grezzi che rappresentano input falliti sono conservati come byte opachi, con le citazioni originali nel relativo indice.

Durante la qualificazione è emerso un difetto nel publisher H v2: aggiungeva una lista vuota `reviewEvidence` anche quando non erano previste evidenze comuni. Il caso isolato e la differenza non attesa sono conservati. Il publisher H v3 evita quell'aggiunta; ha superato 12 controlli isolati e quattro controlli dei vincoli di avvio. Una prova distinta con registro sintetico su H ha riprodotto tutte le 4.920 righe e le 239 modifiche reali.

Anche il verificatore successivo alla pubblicazione è stato qualificato su metadati reali completi e registro isolato: 11.217 elementi previsti, rilettura delle due copie dei 1.462 nuovi artefatti e rifiuto di una modifica estranea al registro. Questi esiti qualificano controlli di pubblicazione nel perimetro dichiarato; non sono prove native o scientifiche.

**L'incremento di produzione non è ancora avviato.** La base autorevole resta publisher v599 e conoscenza v1.171. Il futuro avvio è subordinato all'esito storico completo, alle fonti supplementari esatte, alle impronte congelate e a una nuova verifica del registro. Il controllo di avvio rifiuta correttamente la mancanza della prova storica conclusiva. Il registro è protetto da verifica dell'identità precedente, blocco e scrittura con sincronizzazione; questa modalità non viene descritta come una transazione resistente a ogni interruzione.

| Evidenza locale | SHA-256 |
| --- | --- |
| Verifica indipendente H54 e lettore | `b5268f04a0b7d59288b0b28f69db4a2c34ca04a3ad429de9a984b76d1cb85b9c` |
| Riconciliazione normalizzata dei percorsi | `080f02221e5046cbfba592faa63e1173efdf8f5396572ce53b01addf7979f1b0` |
| Archiviazione esatta dei 1.990 contenuti da C | `9ba12c80d15800c6478273ab83e6302c56b2b9d53d8c4844fe96e7bdafdcaa94` |
| Collegamento delle 1.789 citazioni dirette | `1df6779c88819d33947b2287c6cae5784f77b22cdd78c291fc02d3e02b60f2f7` |
| Controllo indipendente del pacchetto prima della pubblicazione | `494ccb85341ff894b64b981c8645a05c70583504862fd44b7ec37fa70abdddfc` |
| Qualificazione isolata del verificatore successivo | `b35a552d67ada9c86ff19268a10b3cdefb7202740490cc97ff36391e88aac96c` |

Le impronte identificano evidenze locali. Non affermano che gli archivi grezzi siano già caricati su GitHub.

## Gate ancora aperti

H54 conserva sette famiglie scientifiche incomplete e i gate finali Owner. Restano, secondo la loro portata: studio dei contratti residui, applicabilità fisica e incertezza nel dominio finale, confronto della proiezione di conoscenza finale, qualificazione delle decisioni IA e accettazione dei relativi criteri, inventario completo corrente/storico/virtuale, file finale e trasferimento integrale con recupero remoto.

I conteggi di file, schede, casi, blocchi o controlli CI non sono la percentuale della milestone. La pubblicazione di questa documentazione non attiva il portale, non modifica master o script installati e non riprende M27.
