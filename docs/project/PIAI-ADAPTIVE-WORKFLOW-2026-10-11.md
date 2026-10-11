# PixInsight — workflow adattivo fondato sulle immagini

| Campo | Valore |
|---|---|
| Identificativo | BKL-049-EXT-PIAI-ADAPTIVE |
| Versione | 1.1 |
| Stato | Owner-authorized / In Progress; analisi locale candidata, ciclo adattivo non operativo |
| Data | 2026-10-11 |

Owner autorizza analisi delle immagini, verifica dei risultati intermedi e scelta del workflow IA dal tipo indicato nel portale. Richiesta successiva: rimozione della quota di una chiamata API al giorno.

## Stato implementato e residui

Quota giornaliera disabilitata nella revisione Cloud Run `dsg-pixinsight-pilot-quota0-20261011`, 100% traffico e quota0 verificati. PR [#558](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/558), head `d5b314e0354465952278545fe1fcdd7e375eccad`, merge `fdd41047a3679c07dc68763416da106743d03a2b`; 11/11 check, ARB poi RQ separate APPROVED zero finding, 167 test Python e MkDocs strict PASS. Build `540516ac-cf0f-46ec-b26c-f615c480eea0` SUCCESS, 17 test dedicati nel container, digest `sha256:11c3df286c7eaa5b4143752038524ab4676375535d0145b1c86fd911d18853bc`. Sorgenti tools/infrastructure del build byte-identici al merge; secret esistente preservato, nessuna chiave letta. Health disponibile non certifica una nuova chiamata provider.

Primo modulo locale candidato `tools/pixinsight/local_pilot/image_analysis.py`: diagnostica read-only di export nativi XISF singoli Float32 non compressi planari. Hash atteso obbligatorio, controllato prima/dopo. Tutti i pixel verificati senza imporre [0,1] ai dati lineari; momenti/clipping esatti e quantili/MAD su griglia dichiarata. Nove prove sintetiche PASS; tre checkpoint M27 già conservati analizzati privatamente senza modifiche, avvio nativo o API: RGB lineare, RGB processato lineare e LRGB finale, 4634×2808. Non è un OAT del ciclo adattivo.

Differenze numeriche prima/dopo esportabili, ma `scientificComparison=NOT_ESTABLISHED`: stessa geometria non prova registrazione o dominio. Nessuna soglia/score di miglioramento; PSF e rumore di fondo indisponibili, MAD del campo non è SNR. Layout compressi/multi-image/Float64 richiedono il futuro adapter nativo, senza fallback silenzioso.

Il candidato successivo collega il modulo al worker di pianificazione e al payload numerico OpenAI, con consenso separato nel portale. Runtime cloud/worker non ancora aggiornati: opzione disabilitata fino alla verifica coordinata. Ricetta V1 invariata. Restano requisiti aperti: adapter master/export, maschere/background/PSF validati, catalogo/grafo V2, piano da immagini, segmentazione, decisioni checkpoint multiple e accounting persistente, recovery/OAT e History/progetto. Non sono debito accettato o scope escluso. P6 e BKL-051 invariati; nessuna accettazione o pubblicazione immagini.

Uso locale: `python -m tools.pixinsight.local_pilot.image_analysis --input <export-privato.xisf> --sha256 <sha256-verificato> --output <nuovo-rapporto-privato.json>`. Rapporto con hash da conservare privatamente, output create-only. Nessuna rete, enumerazione cartelle, token o avvio PixInsight.

### Collegamento delle misure al pianificatore

Contratto opzionale `openaiPlanning.pixelStatisticsConfirmed=true`, distinto dal consenso al testo/metadati. Richieste precedenti conservano il payload originario. Backend espone `pixelStatisticsEnabled` soltanto con `DSG_PIAI_PIXEL_STATISTICS=LOCAL_WORKER_VERIFIED` e provider configurato; nuove richieste statistiche rifiutate finché disabilitato. Attivazione richiede worker aggiornato e ciclo locale verificato, prima di abilitare l'opzione.

`planning_agent.evidence_for` analizza ogni master già selezionato e verificato; non enumera nuove directory. Per questa versione indice 0, singola immagine Float32 non compressa: formato non supportato/hash cambiato produce `LOCAL_REVIEW_REQUIRED` prima della richiesta a pagamento, senza fallback a soli metadati dopo il consenso alle misure. CFA/mosaici restano subordinati alla preparazione verificata.

Il backend valida ruoli, geometria, canali, finitezza e campionamento; campi/testi aggiunti, conteggi impossibili e dichiarazioni non attestate sono rifiutati prima della prenotazione. SHA256 delle sorgenti e delle misure entrano nel binding durevole conservato privatamente. Payload provider conserva solo ruolo, geometria e statistiche; omette hash e percorsi. Il risultato esatto resta associato all'evidence: replay restituisce la ricevuta, dati cambiati non autorizzano un secondo invio. Valore numerico è evidence riferita dal worker autenticato, non attestazione indipendente del provider.

Questa integrazione motiva i parametri della ricetta V1, senza scegliere ancora un grafo o verificare checkpoint nel ciclo operativo. Nessuna immagine condivisa o chiamata reale aggiuntiva nel collaudo offline; `gpt-6-luna` conservato. Le [API per input visivi](https://developers.openai.com/api/docs/guides/images-vision) distinguono testo e immagini: qui vengono inviati soltanto numeri. Compatibilità visiva del modello scelto non attestata e non necessaria per questo payload testuale.

Rollback: disabilitare `DSG_PIAI_PIXEL_STATISTICS`, impedendo nuovi intake con statistiche, e mantenere sorgente aggiornato per terminare quelli già conservati. Non avviare un worker legacy per intake con il nuovo consenso: produrrebbe evidence incompleta e sarebbe rifiutato. Prima di rollback completo verificare assenza di intake statistici pendenti; conservare richieste, risultati e prenotazioni. La quota giornaliera resta 0; il limite tecnico V1 di 16 tentativi non è ancora sostituito dalla ledger adattiva.

## Contratto di prodotto

Owner sceglie LRGB, SHO, HOO, OSC RGB oppure OSC CFA e indica l'obiettivo di resa. Il tipo descrive ruoli e composizione dei canali; non impone una sequenza universale. L'IA sceglie un grafo di processi revisionati compatibile con dati, obiettivo e moduli verificati. CFA e mosaici conservano la preparazione esistente prima della scelta del workflow di elaborazione.

Il workflow migliore è il candidato meglio supportato dai dati fra quelli confrontati e compatibili con i vincoli. Nessuna promessa di ottimo globale o equivalenza a una calibrazione scientifica. Vincoli di integrità precedono preferenze estetiche. Una riduzione del rumore con perdita di segnale non è automaticamente un miglioramento.

## Evidence locale

Master e checkpoint identificati tramite SHA256, indice, ruolo, geometria e dipendenze. Il PC misura i pixel senza modificare gli originali. Linearità e calibrazione richiedono provenienza: formato Float32, nome e header da soli non le dimostrano. Evidence con stato per misura: disponibile, indisponibile o non comparabile; nessuno zero sostitutivo.

Diagnostica: finitezza e intervallo reale (senza imporre [0,1] ai master lineari); quantili e clipping per canale; fondo su regioni verificate; rumore robusto con metodo, campione e limiti; PSF/eccentricità su stelle non sature adatte al fit; geometria/allineamento; confronto di ROI rappresentative e maschere. MAD della distribuzione dell'intero campo non viene etichettata SNR o rumore del fondo. Dopo denoise/deconvoluzione il rumore può essere correlato e la PSF modificata dal modello.

Anteprime e ROI condivise con il provider solo secondo un consenso esplicito coerente con il nuovo payload. Ogni anteprima conserva geometria, trasformazione/stretches e sorgente esatta; confronto prima/dopo con identica trasformazione. Pixel scientifici e diagnostica quantitativa restano distinti dalle immagini di presentazione RGB8.

## Decisioni e catalogo

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
