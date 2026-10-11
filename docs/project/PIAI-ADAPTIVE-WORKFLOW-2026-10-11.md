# PixInsight — workflow adattivo fondato sulle immagini

| Campo | Valore |
|---|---|
| Identificativo | BKL-049-EXT-PIAI-ADAPTIVE |
| Versione | 1.5 |
| Stato | Owner-authorized / In Progress; statistiche master abilitate sul backend, ciclo adattivo non operativo |
| Data | 2026-10-11 |

Owner autorizza analisi delle immagini, verifica dei risultati intermedi e scelta del workflow IA dal tipo indicato nel portale. Richiesta successiva: rimozione della quota di una chiamata API al giorno.

## Stato implementato e residui

Quota giornaliera disabilitata nella revisione Cloud Run `dsg-pixinsight-pilot-quota0-20261011`, 100% traffico e quota0 verificati. PR [#558](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/558), head `d5b314e0354465952278545fe1fcdd7e375eccad`, merge `fdd41047a3679c07dc68763416da106743d03a2b`; 11/11 check, ARB poi RQ separate APPROVED zero finding, 167 test Python e MkDocs strict PASS. Build `540516ac-cf0f-46ec-b26c-f615c480eea0` SUCCESS, 17 test dedicati nel container, digest `sha256:11c3df286c7eaa5b4143752038524ab4676375535d0145b1c86fd911d18853bc`. Sorgenti tools/infrastructure del build byte-identici al merge; secret esistente preservato, nessuna chiave letta. Health disponibile non certifica una nuova chiamata provider.

Primo modulo locale candidato `tools/pixinsight/local_pilot/image_analysis.py`: diagnostica read-only di export nativi XISF singoli Float32 non compressi planari. Hash atteso obbligatorio, controllato prima/dopo. Tutti i pixel verificati senza imporre [0,1] ai dati lineari; momenti/clipping esatti e quantili/MAD su griglia dichiarata. Nove prove sintetiche PASS; tre checkpoint M27 già conservati analizzati privatamente senza modifiche, avvio nativo o API: RGB lineare, RGB processato lineare e LRGB finale, 4634×2808. Non è un OAT del ciclo adattivo.

Differenze numeriche prima/dopo esportabili, ma `scientificComparison=NOT_ESTABLISHED`: stessa geometria non prova registrazione o dominio. Nessuna soglia/score di miglioramento; PSF e rumore di fondo indisponibili, MAD del campo non è SNR. Layout compressi/Float64 richiedono il futuro adapter nativo, senza fallback silenzioso; multi-image supportato nel nuovo candidato solo con indice esplicito.

PR [#560](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/560) collega il modulo al worker di pianificazione e al payload numerico OpenAI, con consenso separato nel portale. Runtime cloud/worker aggiornati e flag abilitato dopo verifica coordinata. Ricetta V1 invariata. Restano requisiti aperti: adapter master/export, maschere/background/PSF validati, catalogo/grafo V2, piano da immagini, segmentazione, decisioni checkpoint multiple e accounting persistente, recovery/OAT e History/progetto. Non sono debito accettato o scope escluso. P6 e BKL-051 invariati; nessuna accettazione o pubblicazione immagini.

### Ricevuta di attivazione statistiche

Head revisionato `83ae02bb3763e78ad853b80abae7ebae18c74473`, ARB poi RQ indipendenti APPROVED zero finding, 15 check PR SUCCESS e main allineato prima del merge protetto. Merge `16119b01ffd66294e8d395b407c0fa08648885a9`; 14 workflow applicabili post-merge SUCCESS, incluse Pages e prove Windows/Linux. 184 test Python, 84 Node e MkDocs strict PASS. [Ricevuta completa](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/560#issuecomment-6107578919).

Build `6f6da9c7-84a3-4351-87a9-378040b674f0` SUCCESS con 23 test planner a provider simulato. Digest `sha256:132e9a16d8075ec32427850c5dc0c7a3527819a34c0028f8c463aad1570b3b30`; sorgenti pubblici verificati sul Git archive revisionato. Le conversioni CRLF/LF del Git archive Windows non sono identità byte con i blob Git grezzi. Worker aggiornato allo stesso pacchetto, ciclo singolo PASS e polling 30 s ripreso con token DPAPI esistente; nessun avvio nativo. Backup del wrapper conservato; errore iniziale di sostituzione corretto dopo verifica dei file esatti.

Revisione `dsg-pixinsight-pilot-pixels-20261011` creata a traffico 0, Ready/digest/model `gpt-6-luna`/quota0/flag `LOCAL_WORKER_VERIFIED` verificati, poi traffico 100%. Secret esistente preservato senza lettura della chiave. Health disponibile, conteggio provider non esposto. Pagina pubblicata ricaricata; accesso Google non completato nel browser di verifica: opzione autenticata e nuova richiesta reale con consenso statistico non collaudate. Nessuna chiamata API aggiuntiva nel rilascio. La revisione quota0 precedente resta disponibile per rollback.

### Fondazione V2 integrata, non attivata

PR [#562](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/562), head `f0ae5a22e944fa22305d3035fea21c4093daf4ad`, merge `59d3e670195fb65330748c61581f2948a3526f76`: ARB poi RQ indipendenti APPROVED, zero finding; 15 check PR SUCCESS, main allineato e merge protetto sull'head atteso. 290 test Python PixInsight PASS con due skip già previsti; MkDocs strict PASS. [Ricevuta dei gate](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/562#issuecomment-6107749078). Il merge non attiva il ciclo V2.

Tutti i 14 workflow applicabili sul merge effettivo SUCCESS, incluse prove Windows/Linux e deploy Pages. Pagina pubblica verificata con il metodo scientifico e il controllo di dominio corretto. Runtime cloud/worker V1 invariati.

`adaptive_catalog.py` valida grafi DIRECT/STARLESS per LRGB/OSC/SHO/HOO e un insieme finito di processi/parametri. Nessuna espressione PixelMath, comando, percorso o codice prodotto dal modello è ammesso. Prerequisiti di dominio, registrazione, fondo, riferimenti stellari, runtime e maschera restano fatti del worker con provenienza distinta; una statistica del campo non può promuoverli. Ordine e dipendenze sono controllati. I valori ammessi ereditano i limiti della V1: sono limiti tecnici, non ottimi scientifici dimostrati.

`adaptive_ledger.py` conserva richieste/risultati immutabili e un cursore compatto con ordinali assegnati dal server. Policy Owner, sorgenti, catalogo e runtime sono invarianti; solo l'evidence cambia al checkpoint successivo. Un risultato del modello resta `AWAITING_EXECUTION` fino alla distinta ricevuta nativa legata a checkpoint e History. Crash dopo il risultato recupera il risultato senza invio; risposta persa conserva prenotazione e usage incompleto, senza nuovo ordinale. Annullamento/ritiro impediscono nuove prenotazioni. Capacità finita 16 decisioni/sessione e 16 sessioni: vincolo del candidato, nessuna quota giornaliera o budget monetario.

Quindici prove offline PASS su concorrenza, crash, doppia ripresa, sostituzione di binding, dati non finiti, dipendenze e incertezze, incluso il rifiuto del denoise con dominio non attestato. Questi moduli non sono collegati a endpoint, provider, worker o esecutore attivi. Il broker V1 non ammette `OPENAI_API_ADAPTIVE`: non costituiscono attivazione V2, validazione di adapter scientifici, OAT o chiusura dei residui.

### Misure native integrate, non collegate al ciclo: rumore e profili stellari

PR [#563](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/563), head `07809d1f8a8996de7d308050d750a44dd67bfcf5`, merge `f4a864da0f69207a8e2d88fc77377bff861c1f9d`: ARB poi RQ indipendenti APPROVED, zero finding; nove check PR SUCCESS, main allineato e merge protetto. 296 test Python PASS, con due skip già previsti, 88 Node PASS e MkDocs strict PASS. Tutti gli otto workflow applicabili sul merge SUCCESS, Pages incluse; pagina pubblica verificata. [Ricevuta dei gate](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/563#issuecomment-6107867825). Nessuna attivazione di un nuovo endpoint o dispatch.

`measurements.jsh` usa API locali documentate nell'installazione PixInsight: `Image.noiseMRS`, StarDetector V2 e DynamicPSF. Lavora sulla vista della copia selezionata, senza processi di trasformazione dei pixel, salvataggio del master o rete. Regioni dichiarate in coordinate intere, massimo otto; selezioni ripristinate anche in caso di errore. StarDetector opera sul campo completo, selezionando deterministicamente la sorgente isolata più luminosa per cella di una griglia 16×16, massimo 256 candidati. I fit gaussiani sono registrati separatamente per canale, compresi background, ampiezza, centro, assi, angolo e residuo. Fit mancanti restano mancanti; non sono sostituiti con una PSF ipotetica.

Ogni ROI conserva tre stime MRS, con 4, 3 e 2 strati, e il numero di campioni del supporto. La deviazione standard è espressa nelle unità normalizzate dell'immagine, senza divisione per Sn. È una stima della componente gaussiana secondo il modello wavelet: un supporto piccolo o variabile fra strati richiede interpretazione, non un voto automatico. Una ROI coincidente con tutto il campo non diventa automaticamente cielo vuoto; questi valori non sono SNR, rumore di fondo validato o prova di conservazione del segnale. Non viene applicato un fallback silenzioso né mediato il risultato dei diversi strati.

`native_measurements.py` controlla forma, conteggi, finitezza, geometria, ruoli dei fit e binding verso hash/indice della sorgente e impronte del componente e di StarDetector. Per una Gaussiana ellittica calcola soltanto descrittori matematici: `FWHM_major = 2√(2 ln 2) max(sx, sy)`, analogo per l'asse minore, ed eccentricità `√(1 − (min(sx, sy)/max(sx, sy))²)`. Un profilo non gaussiano può essere descritto male da quel modello; residui, saturazione, blending e selezione delle stelle vanno esaminati prima di usare le misure per un confronto. Il campione delle stelle più luminose non è una stima imparziale di tutte le stelle o del seeing.

Il validatore non autentica da solo un file JSON e non certifica ciò che è avvenuto sul PC. L'adapter chiamante deve verificare fisicamente file, impronte, runtime e ricevuta locale prima di conservarlo. Tutte le attestazioni di linearità, registrazione, validità del fondo e accettazione restano `NOT_ESTABLISHED`; il componente non le promuove usando i fit. Sei test Python sintetici e quattro test JavaScript con API simulate verificano questo contratto, distintamente dal collaudo nativo.

Prova privata read-only sul master L M27, indice 0, 4634×2808 mono, PixInsight 1.9.5 build 1706: 3.165 sorgenti rilevate, 255 selezionate, 253 fit gaussiani riusciti. Hash originale/copia e History invariati. Launcher, log e rapporto conservati privatamente; nessuna richiesta OpenAI, trasformazione dei master, accettazione o pubblicazione di immagini. L'istanza del lavoro precedente è rimasta aperta; soltanto l'istanza isolata della prova è stata chiusa dopo la ricevuta. Questa prova riguarda la misura, non il ciclo adattivo: collegamento al worker, attestate precondizioni scientifiche, endpoint V2, esecuzione segmentata e verifica dei checkpoint restano requisiti aperti.

Riferimenti primari consultati: documentazione PJSR locale `Image/Image.html`, `PSF/PSF.html` e `StarDetector/StarDetector.html`, header `StarDetector.jsh` V2.01 rilasciato il 15/09/2026 e script nativo `FWHMEccentricity.js`. Le dipendenze e i moduli/modelli effettivamente caricati devono essere attestati nel futuro manifest runtime completo: il solo hash dell'header StarDetector non certifica tutte le sue dipendenze o un modello ML.

### Provenienza integrata, non collegata al ciclo: History e relazione di autocrop

PR [#564](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/564), head `ef8acee525776ab2b790bb9ab870b794ece7850a`, merge `aefb8a2a189400f1f65f2144b788ba1b82d7dd35`: ARB poi RQ indipendenti APPROVED zero finding, nove check PR SUCCESS, main allineato e merge protetto. 217 test del coordinatore locale PASS, MkDocs strict PASS. La review iniziale ha individuato il bypass del blocco entità con UTF-16: corretto prima del merge, con regressioni in entrambi i reader. [Ricevuta di revisione](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/564#issuecomment-6108333773). Il merge non attiva endpoint o dispatch V2; la verifica post-merge è distinta.

`source_provenance.py` legge la proprietà nativa `PixInsight:ProcessingHistory` della sola immagine XISF esplicitamente selezionata. Conserva hash della proprietà e nomi dei processi registrati, senza eseguire né importare le istanze. Una History di DrizzleIntegration non contiene necessariamente calibrazione e allineamento dei suoi input: la copertura è `RECORDED_VIEW_OPERATIONS_ONLY`, upstream, dominio, registrazione e accettazione restano non stabiliti.

La relazione di autocrop è verificata su tutti i byte dei pixel selezionati, canale per canale, rispetto a un genitore indicato esplicitamente e verificato con SHA256. La regione proviene dal record `WBPPCROP`, controllato contro le geometrie reali; nessuna interpolazione, normalizzazione o approssimazione tollerata. La History del figlio deve coincidere con quella del genitore. Questa prova stabilisce una relazione fra file, senza attribuire un dominio lineare ai dati che precedono il crop.

Il confronto con un contenitore XPSM verifica gli input e ogni campo che modifica i pixel del processo DrizzleIntegration. Differenze nelle sole opzioni di interfaccia sono esposte; campi nuovi, incompleti o corrispondenze ambigue sono rifiutati. Il contenitore salvato documenta impostazioni, non una ricevuta di esecuzione. I log WBPP e i file di calibrazione/registrazione referenziati richiedono ulteriori riconciliazioni prima di promuovere una precondizione scientifica.

Letture read-only, hash prima/dopo, XML senza DTD/entità, massimo 16 immagini e indice obbligatorio; header limitato a 4 MiB, allineato all'inventario sorgenti, contenitore a 16 MiB. La prova dei pixel supporta esclusivamente Float32 non compresso planare little-endian, con attachment delimitato e geometria/canali verificati. Nessuna enumerazione di directory, rete, ricerca automatica di genitori o fallback silenzioso. Il limite separato di 1 MiB della diagnostica V1 attiva rimane invariato.

Dodici test sintetici PASS, incluse DTD/entità in UTF-16 con e senza BOM rifiutate prima del parsing. Riconciliazione privata reale dei quattro master M27 R/G/B/L: pixel di ciascun crop byte-identici al rispettivo genitore 5504×4320, regione `(456,656)–(5090,3464)`, risultato 4634×2808. Input e 25 campi del contenitore DrizzleIntegration corrispondono univocamente, con la sola differenza `showImages` dichiarata. I file sono rimasti invariati. Il primo tentativo si era fermato sul parent L con header 1.123.713 byte: rifiuto conservato, reader di provenienza reso compatibile con il limite documentato di 4 MiB e tutte e quattro le prove ripetute; nessuna modifica alla V1 o avvio nativo/API. Rapporti e impronte conservati privatamente.

### Provider multimodale candidato, non attivato

`image_previews.py` produce proiezioni di visualizzazione dai campioni reali, senza modificare gli originali. Campo completo limitato al lato maggiore di 512 pixel; ritagli di massimo 256 pixel per lato conservano la scala dei pixel. Si applica la funzione midtones `MTF(m,x)=(m−1)x/((2m−1)x−m)`, con estremi di display 0 e 1 e parametro ricavato dalla mediana del genitore e dal target dichiarato. Clipping e quantizzazione PNG a otto bit riguardano soltanto la proiezione. Il ridimensionamento del campo usa BOX dopo la curva. La mediana del campo non viene interpretata come cielo vuoto. Curve, geometria, crop, metodo e impronta sono registrati; prima/dopo devono usare la stessa curva del genitore, senza normalizzazione indipendente che mascheri una perdita di segnale.

`adaptive_provider.py` prepara una richiesta Responses con massimo quattro PNG, ciascuno di massimo 1 MiB, testo numerico limitato e output strutturato. Gli asset sono verificati con SHA256, geometria/canali e crop contro il ruolo sorgente, e decodificati/ricodificati per eliminare metadati; nessun URL remoto o immagine sintetica. Servono tre consensi distinti e veri: dati generali, statistiche e anteprime. L'adapter chiamante deve ricavarli dall'approvazione Owner registrata, non da un'attestazione arbitraria del worker. La policy e gli endpoint attuali non sono ancora estesi a questo trasferimento: nessun invio visivo abilitato dal solo modulo.

Le misure native vengono validate contro binding locali indipendenti e proiettate in descrittori per canale, conteggi, supporto MRS e mediana dei fit gaussiani. Hash sorgenti, History, percorsi e binding privati non sono inviati al provider. Le mediane descrivono il campione selezionato, senza score di qualità, SNR o certificazione di risoluzione. Il modello può proporre solo un grafo del catalogo o fermarsi per revisione; il validatore ricontrolla parametri, ordine, dominio e prerequisiti, senza promuovere fatti sconosciuti dalla valutazione visiva.

La prenotazione durevole deve precedere la richiesta e legare l'evidence esatta; un secondo invio nello stesso processo è bloccato anche dopo timeout. Questa protezione in memoria integra la ledger, senza sostituirla. Risposte incomplete, rifiuti, codice/processi esterni al catalogo e usage incoerente sono rifiutati senza retry. L'adapter restituisce una proposta, non una ricevuta nativa o accettazione. Collegamento a policy, portale, ledger, checkpoint e dispatch rimane da completare.

Dieci test sintetici PASS sulle anteprime e sul provider simulato, incluse conservazione dei campioni, confronto con curva condivisa, consenso/binding e risposta persa. Renderer locale usa NumPy; decodifica provider richiede soltanto Pillow. Prova privata sul master L M27: campo e crop centrali ottenuti dai pixel veri, originale SHA256 invariato, mediana del genitore 0,00782873854, target display 0,2. Nessun trasferimento al provider, processo nativo o accettazione scientifica. La ricostruzione dei 328 input WBPP prosegue separatamente e non è ancora una nuova attestazione.

### Modelli e input visivi: capacità documentate, attivazione separata

La [scheda ufficiale GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) conferma input di immagini e Responses. Il modello richiesto resta `gpt-6-luna`; la capacità documentata non certifica un collaudo multimodale del servizio. La V1 invia ancora soltanto numeri. Anteprime limitate, trasformazioni di visualizzazione dichiarate e consenso distinto devono precedere il collegamento visivo V2; niente immagini prodotte da generatori o pixel da fotografie di riferimento.

La [documentazione della suite RC Astro](https://www.rc-astro.com/unified-pixinsight-rc-astro-suite/) specifica che `ml_version=0` sceglie il modello più recente disponibile; un altro valore numerico seleziona quella versione. Le precedenti ricevute M27 riportano zero, non una versione ML chiamata “0”. Per il nuovo runtime occorrono selezioni esplicite e impronte: sul PC sono stati verificati i file ONNX BlurXTerminator 4, NoiseXTerminator 3.1 e StarXTerminator 11 e la DLL della suite. Probe isolati dei soli costruttori confermano che i valori 4/3.1/11 sono mantenuti; nessun processo sui pixel o caricamento di modelli attestato. File, selezione e modello effettivamente caricato sono evidenze distinte. Nessun aggiornamento o download di modelli eseguito, istanza PixInsight precedente preservata.

Uso locale: `python -m tools.pixinsight.local_pilot.image_analysis --input <export-privato.xisf> --sha256 <sha256-verificato> --output <nuovo-rapporto-privato.json>`. Rapporto con hash da conservare privatamente, output create-only. Nessuna rete, enumerazione cartelle, token o avvio PixInsight.

### Collegamento delle misure al pianificatore

Contratto opzionale `openaiPlanning.pixelStatisticsConfirmed=true`, distinto dal consenso al testo/metadati. Richieste precedenti conservano il payload originario. Backend espone `pixelStatisticsEnabled` soltanto con `DSG_PIAI_PIXEL_STATISTICS=LOCAL_WORKER_VERIFIED` e provider configurato; nuove richieste statistiche rifiutate finché disabilitato. Attivazione richiede worker aggiornato e ciclo locale verificato, prima di abilitare l'opzione.

`planning_agent.evidence_for` analizza ogni master già selezionato e verificato; non enumera nuove directory. Per questa versione Float32 non compresso, indice esplicito verificato dal worker anche in file multi-image. L'indice è parte dell'evidence: senza indice esplicito la CLI conserva il rifiuto dei file multi-image. Mappe ausiliarie di rigetto/peso non sono master. Formato non supportato/hash cambiato produce `LOCAL_REVIEW_REQUIRED` prima della richiesta a pagamento, senza fallback a soli metadati dopo il consenso alle misure. CFA/mosaici restano subordinati alla preparazione verificata.

Il backend valida ruoli, geometria, canali, finitezza e campionamento; campi/testi aggiunti, conteggi impossibili e dichiarazioni non attestate sono rifiutati prima della prenotazione. SHA256 delle sorgenti e delle misure entrano nel binding durevole conservato privatamente. Payload provider conserva solo ruolo, geometria e statistiche; omette hash e percorsi. Il risultato esatto resta associato all'evidence: replay restituisce la ricevuta, dati cambiati non autorizzano un secondo invio. Valore numerico è evidence riferita dal worker autenticato, non attestazione indipendente del provider.

Verifica locale reale dell'11 ottobre: quattro master M27 originali, ciascuno con immagine Float32 principale e immagine ausiliaria UInt8. Analizzato esclusivamente l'indice 0 già selezionato, 4634×2808 mono; tutti i pixel selezionati finiti e hash prima/dopo invariati. Rapporti/hash conservati privatamente; nessuna nuova chiamata API, scrittura sui master o esecuzione nativa. Il primo tentativo single-image era stato rifiutato prima delle misure; non è stato aggirato selezionando un'immagine tacitamente. Non certifica calibrazione, linearità, PSF o qualità.

Questa integrazione motiva i parametri della ricetta V1, senza scegliere ancora un grafo o verificare checkpoint nel ciclo operativo. Nessuna immagine condivisa o chiamata reale aggiuntiva nel collaudo offline; `gpt-6-luna` conservato. Le [API per input visivi](https://developers.openai.com/api/docs/guides/images-vision) distinguono testo e immagini: qui vengono inviati soltanto numeri. Compatibilità visiva documentata nella scheda del modello; collegamento multimodale V2 non collaudato.

Rollback: disabilitare `DSG_PIAI_PIXEL_STATISTICS`, impedendo nuovi intake con statistiche, e mantenere sorgente aggiornato per terminare quelli già conservati. Non avviare un worker legacy per intake con il nuovo consenso: produrrebbe evidence incompleta e sarebbe rifiutato. Prima di rollback completo verificare assenza di intake statistici pendenti; conservare richieste, risultati e prenotazioni. La quota giornaliera resta 0; il limite tecnico V1 di 16 tentativi non è ancora sostituito dalla ledger adattiva.

## Contratto di prodotto

Owner sceglie LRGB, SHO, HOO, OSC RGB oppure OSC CFA e indica l'obiettivo di resa. Il tipo descrive ruoli e composizione dei canali; non impone una sequenza universale. L'IA sceglie un grafo di processi revisionati compatibile con dati, obiettivo e moduli verificati. CFA e mosaici conservano la preparazione esistente prima della scelta del workflow di elaborazione.

Il workflow migliore è il candidato meglio supportato dai dati fra quelli confrontati e compatibili con i vincoli. Nessuna promessa di ottimo globale o equivalenza a una calibrazione scientifica. Vincoli di integrità precedono preferenze estetiche. Una riduzione del rumore con perdita di segnale non è automaticamente un miglioramento.

## Evidence locale

Master e checkpoint identificati tramite SHA256, indice, ruolo, geometria e dipendenze. Il PC misura i pixel senza modificare gli originali. Linearità e calibrazione richiedono provenienza: formato Float32, nome e header da soli non le dimostrano. Evidence con stato per misura: disponibile, indisponibile o non comparabile; nessuno zero sostitutivo.

Diagnostica: finitezza e intervallo reale (senza imporre [0,1] ai master lineari); quantili e clipping per canale; fondo su regioni verificate; rumore robusto con metodo, campione e limiti; PSF/eccentricità su stelle non sature adatte al fit; geometria/allineamento; confronto di ROI rappresentative e maschere. MAD della distribuzione dell'intero campo non viene etichettata SNR o rumore del fondo. Dopo denoise/deconvoluzione il rumore può essere correlato e la PSF modificata dal modello.

Anteprime e ROI condivise con il provider solo secondo un consenso esplicito coerente con il nuovo payload. Ogni anteprima conserva geometria, trasformazione/stretches e sorgente esatta; confronto prima/dopo con identica trasformazione. Pixel scientifici e diagnostica quantitativa restano distinti dalle immagini di presentazione RGB8.

## Decisioni e catalogo

### Metodo tecnico e scientifico di scelta

Il tipo LRGB/OSC/SHO/HOO stabilisce quali canali comporre e quali relazioni conservare. La scelta della sequenza considera invece lo stato dei dati, i trattamenti precedenti, le misure disponibili e l'obiettivo dichiarato. «Migliore» significa una soluzione motivata fra le alternative supportate e confrontabili, con incertezze esplicite; non un massimo universale ottenuto da un voto dell'IA. Il metodo seguente è il target V2, non una capacità già attivata dalla sola integrazione delle statistiche.

Un modello osservativo semplificato è `I = S ⊗ PSF + B + N`: segnale astronomico convoluto con la risposta del sistema, fondo e rumore. Dai soli valori di `I` non si separano univocamente questi termini. Per questo varianza e MAD sull'intero campo comprendono stelle, nebulosità e gradienti oltre al rumore. Un denoise può ridurre la varianza eliminando anche filamenti; uno sharpening può aumentare le alte frequenze amplificando rumore o ringing. Nessuna di queste variazioni prova da sola dettaglio recuperato.

| Valutazione | Evidence necessaria | Effetto sulla decisione |
|---|---|---|
| Integrità e identità | SHA256, indice XISF esplicito, canali, geometria, finitezza, ricevuta runtime | Dati incoerenti fermano il ramo; nessuna decisione IA li supera |
| Dominio e calibrazione | Provenienza dell'integrazione e dei processi; trattamento precedente verificabile | Consente solo processi appropriati allo stato attestato; Float32 e istogramma non attestano linearità |
| Gradiente/fondo | Campioni di cielo validati, maschera e distribuzione spaziale | Evita di sottrarre nebulosità debole come fondo; una ROI numerica da sola non prova cielo vuoto |
| PSF e stelle | Stelle adatte al fit, residui, distribuzione centro/bordi, pixel scale verificata quando disponibile | Motiva deconvoluzione e raggi spaziali; FWHM in pixel non è automaticamente risoluzione angolare |
| Rumore e segnale debole | Stesso checkpoint, ROI e maschere validati, metodo/scala e trattamenti precedenti | Confronta riduzione del rumore con perdita di segnale e artefatti; non usa MAD del campo come SNR |
| Stretch e clipping | Distribuzioni per canale, pixel ai limiti, stelle/nuclei e ROI al 100% | Controlla neri chiusi, alte luci e colore; output senza saturazione non dimostra acquisizione non satura |
| Contrasto e separazione stelle | Maschere, rami/ricombinazione, checkpoint comune e prove su ritagli | Confronta DIRECT/STARLESS e trattamento locale conservando stelle, aloni e struttura diffusa |
| Colore | Filtri, mapping, procedura di calibrazione e provenienza | Distingue calibrazione cromatica dalla palette SHO/HOO di presentazione |

Per BlurXTerminator, il manuale del produttore richiede dati lineari appropriati, sconsiglia il denoise precedente e l'accumulo di deconvoluzioni, e descrive l'uso delle stelle come riferimenti PSF locali. Campi con poche stelle richiedono particolare attenzione alla stima automatica. Queste condizioni motivano il gate del catalogo; non attestano la versione del modello caricata nell'istanza locale. [Manuale tecnico RC Astro](https://www.rc-astro.com/blurxterminator-technical-manual/).

Una prova candidata parte dal medesimo genitore, applica una variazione identificabile su ritagli rappresentativi e mantiene stessi crop, orientazione, maschere e trasformazione di confronto. Le misure hanno metodo, unità, campione e stato di comparabilità. Un confronto non valido resta `NOT_ESTABLISHED`; non viene trasformato in uno zero né in un esito positivo. Solo dopo una scelta motivata si applica il segmento al campo completo e si ricontrollano regioni centrali e bordi.

La verifica del checkpoint ha due livelli: controlli deterministici di identità/integrità e valutazione motivata del tradeoff. L'IA espone processo scelto, alternativa scartata, evidence pertinente e incertezze. Una continuazione è permessa solo sul checkpoint esatto verificato; un risultato incerto conserva il ramo e richiede revisione. Non vengono inventate soglie universali o una somma pesata di FWHM, rumore e contrasto. Accettazione scientifica e pubblicazione rimangono eventi Owner distinti.

La risposta strutturata serve a limitare la forma dei dati, non a provare correttezza scientifica. Rifiuti, risposte incomplete e valori fuori contratto arrestano quella decisione; una risposta persa non provoca un retry ambiguo. [Structured Outputs OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs).

Responses strutturata seleziona esclusivamente processi/varianti e parametri ammessi. Non genera codice eseguibile. Il catalogo definisce ruoli, stato lineare/non lineare, moduli, dipendenze, checkpoint, maschere e condizioni di confronto.

Decisioni motivate: correzione del fondo solo con evidenza compatibile e regioni affidabili; deconvoluzione da lineare prima di denoise/separazione; denoise confrontato sullo stesso genitore; separazione stelle facoltativa, con residui verificati; stretch esplicito come cambio di dominio; palette SHO/HOO separata dalla calibrazione fotometrica. Per ogni azione ammessi anche salto del processo, conservazione del genitore o richiesta di review.

## Ciclo persistente

ANALYSIS_READY → PLAN_READY → OWNER_APPROVED → SEGMENT_RUNNING → CHECKPOINT_READY → CHECKPOINT_VERIFIED → DECISION_READY → segmento successivo oppure REVIEW_REQUIRED/COMPLETED.

Manifest V2 separato e leggibilità V1 conservata. Ogni segmento usa il genitore esatto, preserva originale, tentativo e History; output create-only con hash. La decisione lega job, numero decisione, piano/policy, checkpoint, evidence e modello. Prenotazione CAS prima di ogni chiamata; risultato immutabile e cache per quella decisione. Timeout o crash dopo invio non causano un nuovo invio ambiguo. Ripresa nativa vietata quando lease o completamento sono ambigui: RECOVERY_REQUIRED.

Il catalogo finito e il numero massimo di revisioni per segmento impediscono cicli infiniti; niente quota giornaliera artificiale. Usage cumulativo visibile. Un tetto di costo monetario richiede tariffe applicabili e accounting validato; non si confonde un limite di token con euro.

## Verifica scientifica e conservazione

Controlli tecnici prima di valutare il miglioramento. Confronti misurabili su stesso dominio, griglia, maschera/campione; confronto non valido indicato come tale. Nessuna soglia universale o somma pesata inventata. Il modello espone motivi, tradeoff e incertezze; controlli deterministici rifiutano violazioni. Risultati incerti possono fermarsi sul checkpoint precedente senza accettazione scientifica automatica.

Salvare XISF, maschere, History/progetto e dipendenze prima dell'uscita dell'istanza. Conservare prove scartate e versioni reali dei modelli dove attestabili. Niente strutture generate con inpainting o immagini esterne. Consegna privata, accettazione Owner e pubblicazione rimangono eventi distinti.

## Sequenza di consegna e acceptance

1. Analisi read-only locale e contratto evidence, test sintetici su casi limite e prove su master reali preservati.
2. Catalogo validato e scelta iniziale IA, compatibilità V1, piano visualizzato nel portale con motivazione/limiti e consumo.
3. Esecuzione segmentata e raccolta checkpoint, prove cancellazione/crash/risposta persa/doppia ripresa e History.
4. Decisioni iterative da evidence e confronti, policy di adattamento approvata nel piano, costi e deduplicazione.
5. OAT LRGB, SHO/HOO e OSC; CFA/mosaici solo attraverso preparazione già prevista; acceptance dei risultati distinta dal completamento tecnico.

Non dichiarare il perimetro concluso dopo il solo schema, l'analisi statistica o una nuova chiamata del modello. Rollback arresta la pianificazione adattiva, conserva tutti i segmenti e ripristina la modalità V1 senza replay dei job adattivi.
