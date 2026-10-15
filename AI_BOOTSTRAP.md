# Digital StarGate AI Bootstrap

## BKL-051 — errore HTTP postmerge e correzione, 15 ottobre 2026

PR601 integrata dopo 18 controlli e ARB poi RQ; postmerge scientifico Windows
fallito per connessione interrotta su un percorso worker che deve restare 404.
Il gate precedente resta fallito. Correzione candidata riusa la chiusura
controllata delle risposte negate per tutti gli errori, senza cambiare accessi,
percorsi o idempotenza. [Evidenze, limiti e gate](docs/project/BKL-051-S1-REJECTED-HTTP-RESPONSES-2026-10-15.md).
Nessuna nuova attivazione cloud o ripetizione di analisi. BKL-051 OPEN /
NOT_VALIDATED, stima37%, zero controlli qualificati. Le note seguenti conservano
gli snapshot precedenti.

## BKL-051 — prove private della tripletta e controllo WCS, 15 ottobre 2026

PR599 rilasciata; ripresa autorizzata conclusa con tre tentativi RAW diagnostici
collegati al piano e ripristino del servizio. Calibrazione, provenienza e WCS
candidate delle tre esatte immagini verificate privatamente e lette nel portale;
non riassegnare i tentativi RAW ai derivati. Correzione candidata del verificatore
respinge confronti di coordinate mancanti o vuoti; gate del candidato separati
dalle prove native già concluse. [Stato, evidenze e limiti](docs/project/BKL-051-S1-WCS-COPY-EVIDENCE-2026-10-15.md).
Milestone OPEN / NOT_VALIDATED, stima37%, zero controlli qualificati. Nessuna nuova
prova cloud, query IRSA o segnalazione autorizzata da questa continuità.
Le sezioni seguenti conservano gli snapshot precedenti.

## BKL-051 — accesso Owner, 15 ottobre 2026

PR596 rilasciata; prova reale interrotta dopo un completamento diagnostico collegato al piano. Richiesta successiva non confermata, nessun reinvio; servizio, configurazione e IAM ripristinati. Candidato locale: controllo preventivo della scadenza prima di HTTP e nuovo intento, conservando gli intenti incerti. 49 test del portale locali PASS; CI/review/rilascio del successore da verificare. [Stato e limiti](docs/project/BKL-051-OWNER-SESSION-EXPIRY-2026-10-15.md). Milestone OPEN / NOT_VALIDATED, 37%, zero controlli qualificati. Le note seguenti conservano gli snapshot precedenti.

## BKL-051 — prova operativa e isolamento del registro, 15 ottobre 2026

PR594 integrata e portale pubblicato; le precedenti note di candidato restano storiche. La prova reale successiva si è fermata alla prima registrazione worker: stato cloud preesistente con identità diversa, HTTP400, zero nuovi job e avvii nativi. Traffico e permesso temporaneo ripristinati. Correzione locale con riferimento di registro esplicito, compatibilità storica e nessuna migrazione; non distribuita. [Contratto, prove e residui](docs/project/BKL-051-CONTROL-STATE-ISOLATION-2026-10-15.md). BKL-051 OPEN / NOT_VALIDATED, stima37%, zero controlli qualificati; niente nuova prova o deployment autorizzati da questo codice.

## BKL-051 — continuità del candidato, 15 ottobre 2026

Per il lavoro BKL-051 leggere il [nuovo handover](docs/project/HANDOVER_2026-10-15-BKL051-PLAN-CASE-WORKSPACE.md) e il [dossier del candidato](docs/project/BKL-051-PLAN-CASE-WORKSPACE-2026-10-15.md). Piano versionato, dispatch vincolato, contesti parziali, dossier e scheda passiva integrati localmente. Python445 OK (uno skip symlink), JavaScript274 e Pages992HTML PASS; ARB poi RQ locali APPROVED sul tree applicativo. Non attestano CI/review del commit finale, rilascio, servizio attivo o acceptance. Milestone OPEN / NOT_VALIDATED, stima37%, zero controlli qualificati; tripletta reale preparata non eseguita. Tutti i residui scientifici/operativi e IRSA restano aperti. Nessun nuovo cloud, costo, invio astronomico o fotografia pubblicata. Questa continuità riguarda BKL-051 e preserva gli altri package e gli snapshot sotto riportati.


## Portale pubblico — catene informative e brand, 14 ottobre 2026

PR587–589 integrate/pubblicate/verificate; baseline applicativa `9ea5f2ca377eca2e48af1c081fc64c4e7bb5b582`. Per lavori sul dettaglio sessione, Mission Control, manifest del reporting o brand, leggere anche [DSG-PORTAL-LINEAGE-REF-001](docs/developer/session-lineage-and-mission-control.md) e [ricevute di rilascio](docs/releases/2026-10-14-session-lineage-and-brand.md). Il passo Scientific assets include le versioni pubblicate con session ID esatto ma conserva RAW/provenance parziali; Transfer indica documenti/telemetria EAGLE, non RAW fotografici. Entrambe le pagine rileggono le fonti ogni 60s visibili e manualmente. Logo Owner comune; AP-013 storico/documentale, nessuna nuova authority/schedulazione.

Questa continuità è circoscritta al portale: non sostituisce la sequenza di bootstrap o gli stati scientifici/privati dei package seguenti.

## PixInsight — requisito persistente per decidere i rami alternativi

Coordinatore LRGB dal portale attivo: backend research-lineage-v1-20261011, worker e3eddeb4; PR579–584 integrate con revisioni separate e gate applicabili verificati. PR584 corregge la proiezione del fit SPCC antenato e rende la ripresa Owner vincolata a stato/policy/evidenza, senza replay o azzeramento. Accesso Owner e ripresa reale verificati. M27 2ffd1ae8: 12 API note / sei prove native, 137.239 token totali. SPCC CP001 selezionato, controllo conservato dopo BXT CP002/CP003, denoise0,3 CP004 e stretch0,06 CP005 selezionati. CP006 COMBINE verificato ma non promosso; STOP per campioni RGB ai limiti e beneficio non dimostrato. Catalogo COMBINE fisso: mL=mc=0,5, clipHighlights=true, una sola prova; nessun parametro alternativo o ritorno a fasi precedenti. Non riprendere ripetutamente per forzare il finale: occorre una nuova capacità verificata, conoscenza motivata e perimetro approvato coerente con le nuove impronte. Restano nominalmente10prove/20API, ma non autorizzano processi fuori catalogo. Originali invariati, CP005 conservato; finale e accettazione Owner aperti. Conoscenza SHA5b2bc101... invariata; QHY695A / ZWO RGB / Optolong L-Pro soloL, curve nominali / IdealQE dichiarate. [Consuntivo e limite operativo](docs/project/PIAI-RESEARCH-COORDINATOR-2026-10-11.md#fusione-lrgb-prova-non-promossa-e-limite-operativo). Tentativi b013 indeterminato e 1f respinto conservati senza retry. Non attestare workflow completo o globalmente migliore.

Owner precisa che occorre capire e fornire al coordinatore la conoscenza appropriata per decidere i rami alternativi, e richiede di memorizzare questo requisito. La conoscenza deve collegare stato/ricetta dell'immagine, precondizioni native, misure e limiti, alternative plausibili (inclusa omissione), parametri e costo delle prove, criteri di confronto sul medesimo genitore e condizioni di arresto. Una lista di processi o una riduzione isolata del rumore/FWHM non basta. Conoscenza versionata distinta da capacità realmente validate e dati osservati; motivazione e prove della scelta conservate e consultabili nel portale. Questo requisito guida il coordinatore rilasciato tecnicamente e il suo OAT: non attestare autonomia completa dalla sola memorizzazione o dai test sintetici.

## PixInsight — conoscenza scientifica API e sviluppo dal portale

Owner autorizza sviluppo SPCC/confronto autonomo e precisa uso finale interamente dal portale, senza chat. PR577 integrata `a6408267da05d3be8f1adf4e5205de4f95f80103`: ARB poi RQ zero finding, nove check PR e otto workflow post-merge SUCCESS. Backend scientific-v1100% sull'immagine `198beb5c994d4c41c257d96e033f2b8376e4a6d6d625f79dfcbc4391a8660fc5`, configurazione preservata, health200 e dati privati403 anonimi. La proiezione portabile della skill `pixinsight-scientific` passa nelle istruzioni API dei nuovi job e nei checkpoint, con SHA256/pacchetto archiviato; job storici conservano metodo precedente. Nuove misure read-only M27 su cinque regioni concluse, originali/copie/History invariati, istanza dedicata chiusa. Nessuna nuova chiamata API reale o SPCC: guide non abilitano processi mancanti. [Stato e requisito portale v1.1](docs/project/PIAI-SCIENTIFIC-KNOWLEDGE-2026-10-11.md); OAT provider della guida e nuovo controller SPCC/prove ancora da completare. Le sezioni seguenti conservano lo stato precedente.

## PixInsight — nuova richiesta di ripartenza fotometrica

Owner chiede nuova elaborazione M27 dai master lineari con misure, SPCC e selezione autonoma di prove tramite API. Camera QHY695A, RGB ZWO e Optolong L-Pro come luminanza confermati 11/10/2026 e registrati nei capitoli10/22. Originali SHA invariati e proprietà astrometriche presenti; validità sulla griglia non ancora verificata. Curve nominali ZWO/Optolong presenti nel database SPCC installato, QE specifica non individuata nel database esaminato. [Verifica preliminare e nuovo perimetro richiesto](docs/project/PIAI-M27-PHOTOMETRIC-RESTART-2026-10-11.md). Non è una nuova misura pixel/SPCC, un avvio nativo o una chiamata API. Il servizio V2 resta attivo e il finale precedente distinto: COLOR empirico, adattamento solo del prossimo passo, non selezione autonoma di rami. Implementazione, astrometria/SPCC M27 e OAT del nuovo ciclo restano necessari; non dichiararli completati dalla registrazione dell'inventario.

## PixInsight — consegna adattiva M27 e worker dal portale

PR574 integrata `f8134b0827ba1d2c4b5dd9d788889cd203ee5378`, head `9d077656079102ee6fcef072f9bfc32c630bf4ac`: ARB poi RQ zero finding, nove check PR e otto post-merge SUCCESS; 13 test worker/MkDocs strict PASS, Pages v2.4 HTTP200. Worker aggiornato con impostazioni e byte nativi preservati; backend PR573 invariato. Piano M27 COLOR/STRETCH0,06/COMBINE eseguito su copie alla risoluzione originale, tre segmenti PHYSICALLY_VERIFIED; ultimo controllo API COMPLETE_FOR_REVIEW. Consegna FINAL_FILES_REVERIFIED, READY_FOR_OWNER_REVIEW/job COMPLETED, XISF e archivio privati verificati; portale reale mostra anteprima e azioni di revisione. Quattro chiamate della richiesta completata: 20991 input/4225 output; il tentativo storico indeterminato resta tale, senza retry. Owner autorizza background30s con avvio solo per piani esatti confermati nel portale; processo nascosto e più cicli verificati, nessun nuovo avvio o accettazione automatica. [Stato e metodo v2.5](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). Accettazione scientifica Owner pendente; catalogo iniziale verificato solo M27 LRGB, nuove cartelle richiedono analisi supervisionata e OAT delle altre ricette/confronti alternativi restano da completare. I paragrafi seguenti sono snapshot storici.

## PixInsight — OAT astronomico supervisionato e guard candidato

PR573 integrata272c09fe, nove check PR/otto post-merge SUCCESS, backend adaptive-diag100%, riferimento2.3HTTP200. Owner ha autorizzato una nuova richiesta distinta dopo il tentativo indeterminato e poi il piano esatto COLOR/STRETCH0,06/COMBINE su master M27 originali. Tre segmenti nativi PHYSICALLY_VERIFIED, originali conservati; primi due controlli API CONTINUE senza cambio parametri. Timeout1800s aggiunto alla configurazione privata dopo il primo avvio, riconciliato senza rilancio. Candidato impedisce l'avvio supervisionato senza timeout valido e mantiene curva identità per l'anteprima finale non lineare. [Stato v2.4](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). Restano ultimo controllo API, consegna/archivio privati e valutazione Owner; nessuna accettazione scientifica. I paragrafi seguenti sono snapshot storici.

## PixInsight — catalogo LRGB attivo, diagnostica candidata

PR572 integrata (merge `0678a9c2814e96e213438a6fea81e7ebdf19871c`), ARB poi RQ zero finding, nove check PR e otto post-merge SUCCESS, 291 Python/MkDocs strict PASS. Backend adaptive-lrgb a traffico100%, worker head796d8f52 con impostazioni e byte nativi preservati. Quarta richiesta distinta RESERVED senza piano validato; consumo indeterminato, nessun retry o esecuzione nativa. Candidato registra soltanto categorie fisse della fase/ragione/stato dell'errore, senza payload privati e senza recupero retroattivo. [Stato v2.3](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). Restano diagnosi, proposta valida e OAT astronomico supervisionato. I paragrafi seguenti sono snapshot storici.

## PixInsight — completamento LRGB candidato dopo le analisi reali

PR571 integrata (`6cc459d844d1d84be00ebeb88ac2270664da8f64`), nove check PR e otto workflow post-merge SUCCESS; backend adaptive-rules attivo e avviso trasferimento verificato. Due richieste reali STOP conservate; confronto read-only su quattro regioni periferiche/campo completo verificato. Terza analisi reale propone COLOR/DENOISE/STRETCH, ma senza fusione LRGB: nessuna approvazione o esecuzione. Nuovo candidato impone COMBINE dopo STRETCH in LRGB e aggiorna il fingerprint/proiezione del catalogo; occorre una nuova proposta distinta. Coordinatore attualmente a cicli singoli dopo rifiuto automatico del riavvio in background. [Stato v2.2](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). Restano OAT astronomico, esatto grafo e avvio supervisionato. Gli snapshot seguenti descrivono stati precedenti.

## PixInsight — backend adattivo attivo e prima analisi reale

PR570 integrata (`af51880b2d73f26c22e09f5648cbddf8896e1ac1`), head `04061a091f2434f20c88c1024aef5da94db0e1ed`, ARB poi RQ APPROVED zero finding e nove check PR SUCCESS. Backend `adaptive-on-20261011` al 100%, flag adattivo attivo, gpt-6-luna/quota0 e secret esistenti conservati. Worker privato con catalogo M27 e polling30s attivo, avvio nativo disabilitato per default. Accesso Owner reale e opzione adattiva verificati. Consenso esplicito a prompt/statistiche/anteprime M27 e intermedi verso OpenAI. Prima analisi reale: STOP_FOR_REVIEW, 4890/1396 token, nessun segmento nativo. Candidato successivo chiarisce al provider i prerequisiti empirici del catalogo e aggiorna l'avviso di trasferimento della pagina; non forza la prosecuzione e conserva l'arresto. OAT astronomico e nuovo grafo esatto restano da completare. [Stato e metodo v2.1](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). I paragrafi seguenti sono snapshot storici.

## PixInsight — preparazione e segmenti candidati

PR569 integrata (`5708c262b538e7b148d2be0ce478712facc3a1dd`), ARB poi RQ indipendenti APPROVED zero finding, 15 check PR SUCCESS; post-merge in corso. Tutti gli 11 segmenti del controller hanno superato il collaudo nativo su soli dati sintetici, con BIN2, History e ricevute fisiche; nessuna qualità scientifica M27 viene dedotta. Nuova revisione cloud pronta a traffico 0 e flag adattivo assente; worker privato installato, ciclo singolo senza avvio nativo verificato. Nuovo candidato `initialAnalysisCatalog` consente nuove richieste portale sui medesimi master verificati senza registrazione per requestId; ogni richiesta conserva prompt/consensi propri e riverifica fonti/runtime. Master nuovi richiedono ancora analisi supervisionata. Owner conferma i quattro master M27 WBPP pre-stretch; nessun nuovo workflow fisico M27 o invio immagini al provider eseguito. Attivazione coordinata, OAT autenticato, copertura delle altre preparazioni e policy esatta restano necessari. [Contratto v2.0](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md).

## PixInsight — ammissione adattiva candidata (snapshot precedente)

PR566 integrata, otto workflow post-merge SUCCESS e Pages verificate. Nuovo candidato per consensi distinti, proposta iniziale e policy Owner sul grafo esatto; isolamento dai claim/rapporti V1, prenotazione/accounting senza retry ambiguo e verifica finale distinta. Portale/route presenti nel candidato, flag adattivo disabilitato nel runtime attivo. Raccolta read-only dei quattro master M27 verificata nativamente, originali/copie/History invariati. Dispatch segmentato, invocazione checkpoint, preparazione CFA/mosaici e consegna/OAT adattivi restano aperti. Nessuna nuova chiamata reale, denoise o stretch; quota0 e gpt-6-luna attivi invariati. [Contratto e stato](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md).

## PixInsight — confronto dei checkpoint e provenienza M27

La verifica privata dei 328 input WBPP e delle quattro relazioni di autocrop è completa. Owner conferma che i quattro master esatti sono WBPP prima dell'elaborazione: attestazione dello stato pre-stretch, distinta da linearità fisica e accuratezza astrometrica. Contratti candidati per confronto RGB/L con curva condivisa e modifiche ai soli parametri del prossimo processo; maschera pianificata distinta da maschera verificata. Provider e controlli offline non attivano endpoint o esecuzione V2; journal finale, portale, dispatch segmentato e OAT restano aperti. Quota0 e gpt-6-luna attivi invariati. [Metodo e stato corrente](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md).

## PixInsight — integrazione statistica candidata

Incremento autorizzato del ciclo adattivo: consenso separato per statistiche dei pixel, analisi locale dei master selezionati, evidence validata/binding immutabile e payload OpenAI senza hash o percorsi. PR #560 integrata, 14 workflow post-merge PASS, backend/worker aggiornati e flag abilitato; quota0 e gpt-6-luna conservati. Accesso browser non completato: nuova opzione autenticata e richiesta statistica reale non collaudate; nessuna chiamata API aggiuntiva o avvio nativo nel rilascio. Il planner conserva la ricetta V1: catalogo, analisi PSF/background, segmentazione e decisioni checkpoint multiple restano aperti. Quota0 attiva e P6/BKL-051 invariati. [Contratto e rollback](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md#collegamento-delle-misure-al-pianificatore).


## PixInsight — analisi adattiva in sviluppo, quota giornaliera rimossa

Owner approva l’11 ottobre analisi immagini/checkpoint e scelta workflow IA dal tipo LRGB/SHO/HOO/OSC indicato nel portale. PR558 rilasciata; quota0 attiva, revisione `dsg-pixinsight-pilot-quota0-20261011` al 100%, nessuna quota giornaliera. Il piano V1 conserva singolo invio/capacità16. Primo modulo diagnostico locale candidato: nove test e tre checkpoint M27 privati verificati read-only; non ancora collegato a planner/portale/esecutore. Catalogo, analisi scientifica/native export, segmentazione, decisioni multiple, accounting/recovery e OAT restano requisiti aperti. [Direzione, stato e acceptance](docs/project/PIAI-ADAPTIVE-WORKFLOW-2026-10-11.md). Non promuove acceptance P6/BKL-051 o pubblicazione immagini.


## Estensione PixInsight autorizzata — 11 ottobre 2026

Owner autorizza analisi dei master, verifica dei checkpoint e scelta del workflow IA compatibile con il tipo LRGB/SHO/HOO/OSC selezionato nel portale. Sviluppo adattivo aperto, non attivato né validato scientificamente. Richiesta successiva: rimuovere la quota di una chiamata API al giorno. Candidato compatibile con `DSG_PIAI_OPENAI_DAILY_LIMIT=0`: nessuna quota giornaliera, idempotenza e capacità tecnica V1 conservate; default 1 per installazioni non aggiornate. Attivazione del nuovo valore subordinata al deploy del codice compatibile e verifica della revisione effettiva. [Contratto e limiti](docs/project/PIAI-OPENAI-PLANNING-2026-10-10.md). P6, BKL-051 e pubblicazione scientifica invariati.


## Incremento PixInsight OpenAI attivo, consegna privata verificata

Integrazione OpenAI autorizzata e rilasciata (PR #553/#555/#556). Collaudo reale M27 completato fino alla consegna privata: piano gpt-6-luna, conferma Owner esplicita, copie verificate, una esecuzione supervisionata PixInsight 1.9.5 build 1706, 29 operazioni e 15 checkpoint, originali invariati e pixel finiti/normalizzati. Una chiamata API (455 input / 769 output); nessuna chiamata aggiuntiva dal nativo. Presenza di clipping misurata privatamente, History a monte NOT_ESTABLISHED e modello ML caricato non attestato indipendentemente. Risultato privato visualizzato; nessuna accettazione scientifica o pubblicazione. Costo monetario non verificato; P6 Accepted e BKL-051 invariati. [Contratto, esito e runbook](docs/project/PIAI-OPENAI-PLANNING-2026-10-10.md). Il lavoro BKL-051 corrente rimane quello documentato sotto.

## Aggiornamento corrente — leggibilità dossier preliminare

Dossier preliminare privato con note e percorsi lunghi a capo, viewport e struttura main; due regressioni permanenti. Candidato byte-identico verificato manualmente su schermate Owner, con viewport/zoom non attestati e senza audit completo di accessibilità. Gate del rilascio esatto nella PR e ricevute. BKL-051 OPEN / NOT_VALIDATED, residui S1–S5 interi; nessun nuovo nativo/cloud/invio/spesa. Rapporti storici immutabili; P6/F4/F5/BKL-050/Safety/C→F invariati. [Dossier](docs/project/BKL-051-S4-DRAFT-READABILITY-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-DRAFT-READABILITY.md).

## Snapshot precedente — prima della leggibilità del dossier

## Aggiornamento corrente — accessibilità rapporto locale

Correzione candidata del renderer del rapporto locale: regioni scorrevoli nominate e raggiungibili da tastiera, caption/focus e identificativi lunghi a capo. Quattro test aggiuntivi; gate exact-head, ARB poi RQ e post-merge nelle ricevute del presente incremento. Il candidato privato precedente aveva 12 test PASS e verifica browser circoscritta, non acceptance S5. JSON, sigillo, unità, coda e authority invariati; rapporti storici conservati. BKL-051 OPEN / NOT_VALIDATED, tutti i residui S1–S5 e reporting interi; cloud isolato concluso/spento, nessun nuovo nativo/cloud/invio/fotografia. P6/F4/F5/BKL-050/Safety/C→F invariati. [Dossier](docs/project/BKL-051-S4-LOCAL-REPORT-ACCESSIBILITY-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-LOCAL-REPORT-ACCESSIBILITY.md).

## Snapshot precedente — prima della correzione del rapporto

## Aggiornamento corrente — archivio privato del rapporto conservato

Candidato locale passivo dopo PR549 merge `37955d323b36bd107c69acd4abebef9ac272395b`: ZIP privato del rapporto, journal e soli artefatti referenziati dell'attempt sigillato, copie streaming e verifica CRC/SHA256, fallimenti conservati. Cinque test sintetici Windows e 19 regressioni collegate PASS; CI/revisioni/rilascio sul proprio head obbligatori. Non archivio completo delle dipendenze o accettazione scientifica. Cloud isolato concluso e spento, nessun nuovo login/build/nativo/invio. BKL-051 OPEN / NOT_VALIDATED; tutti i residui S1–S5, P6/F4/F5/BKL-050/Safety/C→F invariati. [Dossier](docs/project/BKL-051-S4-RETAINED-REPORT-BUNDLE-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-RETAINED-REPORT-BUNDLE.md).

## Snapshot precedente — prima dell’archivio del rapporto

## Aggiornamento corrente — collaudo cloud isolato S4

Collaudo cloud isolato S4 della coppia concorrente completato tecnicamente, servizio arrestato e assenza osservata. Una build e un deploy del candidato PR546 fissato al merge c3942103366b0bccb20eb7a534877d96f2e2b4cf; manifest/config/layer dell’immagine verificati per digest, dipendenze reali 2.61.0/3.17.0 e 168 file tools/sorgente corrispondenti al pacchetto pubblico approvato. Accesso Google e coppia eseguiti personalmente dall’Owner. Due esecutori nello stesso container, non due repliche: due binding, due job QUEUED, quattro commit e sei backup, comprese due candidate respinte. Contatore runtime: due upload412, 100/200 invii provider e 24/80 richieste HTTP; non audit indipendente del provider. Letture GCS dirette dopo lo stop confermano quattro generazioni, testa finale e SHA256 di tutti i sei backup. Nuova fase CLI26/40; nessuna riattivazione o seconda scrittura dopo l’errore di lettura conservato. Processo di arresto separato sullo stesso PC, non protezione indipendente dal suo guasto. Preventivo complessivo prudenziale5EUR e limite Owner10EUR; fattura e pulizia futura non osservate. Policy7giorni sui soli nuovi dati sintetici, versioning/soft-delete e conservazione potenzialmente più lunga; archivio privato102elementi CRC e ogni SHA256 PASS, profilo e payload/token runtime esclusi. Il risultato completa soltanto la coppia isolata: S4 complessiva incompleta, S5 non accettata e BKL-051 OPEN / NOT_VALIDATED. S1/S2 aperte e S3 parziale; P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4/BKL-050 finale, Safety/S10/Scheduler/C→F invariati. Nessuna elaborazione PixInsight, fotografia pubblicata o invio astronomico. Nessun nuovo avvio autorizzato dall’esito. [Dossier corrente](docs/project/BKL-051-S4-ISOLATED-CLOUD-OAT-EVIDENCE-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-ISOLATED-CLOUD-OAT.md).

## Snapshot precedente — prima del collaudo cloud isolato

## Aggiornamento corrente — covarianze formali Gaia

Preparazione separata delle covarianze formali Gaia: cinque errori e dieci correlazioni, unità/TCB/cosδ verificati nella documentazione DR3; 32 vicini diagnostici distinti, 27 matrici5D complete e 5 incomplete mantenute indisponibili senza zeri inventati. Modello lineare condizionale a piano tangente fissato: 124 proiezioni su 144 coppie posizione/vicino e 51 blocchi fra epoche per lo stesso riferimento, senza presumere indipendenza. Otto test PASS e confronto NumPy indipendente sulle matrici/proiezioni/blocchi reali; sorgente pubblico byte-identico al prototipo verificato. Non è propagazione6D/observer, covarianza delle immagini, match o astrometria accettata; qualità Gaia, sistematiche, centroidi/covarianze native, frame/timing e policy restano gate. Nessuna nuova query, dipendenza, misura nativa o integrazione automatica nelle decisioni. PR547 catalogo rilasciata sul merge8fba0c9833dff2d3f13d5e39db8a2bd15aa3317c, CI14/14 e ARB poi RQ zero finding, gate validi, 14 workflow postmerge e 10 risorse PASS; archivio55elementi verificato. Catalogo80.328, subset585 e TOP100 preservati; 28 vicini cambiati su72posizioni conservate a stesso modello6D condizionale, 144 confronti sferici indipendenti PASS. PR546 candidata S4 completata e piano privato della prossima sola lettura fissato al suo mergec3942103366b0bccb20eb7a534877d96f2e2b4cf, non aggiornato implicitamente alla main. Budget futuro totale10EUR e Owner nel solo piano privato; nuovo login isolato/sola lettura, poi distinta build/retention e dopo digest attivazione/OAT/verifica GCS/arresto restano decisioni future. BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. IRSA metadata invariati nella ricerca conservata, nessuna nuova risposta tecnica attestata, corpo consultato o invio. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4/BKL-050 finale, S10/Safety/Scheduler e C→F invariati. Nessuna nuova credenziale/sessione cloud, fotografia, soglia, invio astronomico o elaborazione nativa. [Dossier corrente](docs/project/BKL-051-S2-GAIA-FORMAL-COVARIANCE-PREPARATION-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-GAIA-COVARIANCE.md).

## Snapshot precedente — prima delle covarianze formali

## Aggiornamento corrente — catalogo Gaia e rilascio candidato S4

Catalogo pubblico Gaia DR3 del campo Atami già conservato: quattro query TAP HTTP200, 80.328 righe del cono senza TOP o filtri e 585 nella selezione RV/parallasse positiva/PM; conteggi e ID verificati. Moti propri disponibili per 57.215 righe e mancanti per 23.113, senza zeri inventati. TOP100, subset585 e 72 posizioni native preservati; cambia il vicino più prossimo in 28 posizioni passando da 100 a 585 con identico modello6D condizionale. Formula sferica indipendente verifica 144 identità/distanze; FITS originali invariati. Completezza della restituzione query soltanto: epoca, frame, osservatore, covarianze e associazioni restano NOT_VALIDATED; il catalogo completo statico non prova astrometria alla stessa epoca. IRSA metadata invariati nella nuova ricerca limitata, nessuna nuova risposta tecnica attestata, corpo consultato o invio. PR546 candidata S4 completata sul merge c3942103366b0bccb20eb7a534877d96f2e2b4cf: CI23/17, ARB poi RQ zero finding, gate validi, 17 workflow postmerge e 10 risorse PASS; pacchetto229elementi verificato. Budget futuro totale 10 EUR e Owner nel solo piano privato; prossimo passo distinto login fresco isolato di sola lettura, poi build/retention e dopo digest effettivo attivazione/OAT/verifica GCS/arresto. BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4/BKL-050 finale; S10/Safety/Scheduler e C→F invariati. Nessuna nuova credenziale/sessione cloud, fotografia, soglia, invio astronomico o misura nativa. [Dossier corrente](docs/project/BKL-051-S2-GAIA-CATALOG-COMPLETENESS-2026-10-10.md). [Handover corrente](docs/project/HANDOVER_2026-10-10-BKL051-GAIA-CATALOG.md).

## Snapshot precedente — prima del catalogo Gaia completo

## Aggiornamento corrente — candidato lab S4

Preparazione autorizzata del candidato lab S4: gateway concorrente con due esecutori HTTP indipendenti, runtime/Docker separato, quattro client GCS con contatore dei retry e Google Owner con trasporto iniettato. Pagina Owner con descrittore fissato, token solo in memoria e coppia senza replay; controller worker, staging pubblico da Git, wrapper CLI bounded con profilo fresco/ledger/preflight/context fissato e piani build/deploy/arresto. Sedici test gateway/runtime, sei staging/piano/stop, cinque browser protocol e quattro SDK e dieci CLI offline PASS; 53 regressioni Python e browser desktop/mobile sintetico verificati, nessun Google/cloud reale. SDK 3.17.0/2.61.0 fissati, fetch metadata bucket asincroni disabilitati; fallimenti del prototipo conservati e corretti. Tetto futuro totale Owner 10 EUR, identità Google nel solo piano privato; prezzi EUR, configurazione privata e armamento watchdog, conservazione pagata finita e fresh build/digest/login/OAT/verifica GCS/arresto restano gate prima del live. PR544 completata sul merge 75a164f66b7f95d78cf9209b70ba02aac7cebbd7, 15 workflow post-merge e sette risorse PASS. Qualificazione repository del nuovo candidato nelle ricevute exact-head e post-merge, nessuna attivazione autorizzata dalla preparazione o dall’assenza Owner. PR540 storicamente non conforme, PR542 correttiva completata senza sanatoria. BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. IRSA21929/21930: sola presa in carico nella nuova ricerca metadata limitata, nessuna risposta tecnica attestata o reinvio. Restano calibrazione/rumore/covarianze, astrometria/timing, pipeline e rapporto completi, prove cieche/falsi positivi, moving objects/tracklet, integrazione autenticata dei canali/formati provider/trasporto/esiti e policy quantitativa Owner. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4, BKL-050 finale. Nessuna nuova credenziale/sessione cloud, fotografia, soglia scientifica, invio astronomico o prova nativa; Safety e C→F invariati. [Dossier corrente](docs/project/BKL-051-S4-LAB-CLOUD-CANDIDATE-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-LAB-CANDIDATE.md).

## Snapshot precedente — prima del candidato lab

## Aggiornamento corrente — preparazione concorrenza isolata

Owner approva la preparazione dell’ambiente isolato a due esecutori, distinta da una nuova attivazione cloud. Controller offline con due HTTPServer indipendenti, handler/coda di produzione invariati e storage MemoryStore sintetico comune; rendezvous dopo lettura della stessa generazione, due conflitti CAS sintetici, quattro commit e sei copie di backup verificate. Sei test dedicati PASS; credenziali e Google Owner sintetici, nessun HTTP412 provider attestato. L’immagine/gateway cloud, autenticazione Google, trasporto GCS e controller live restano da implementare e revisionare prima di chiedere attivazione. PR542 correttiva completata sul merge 765dee4e8e3f73e0817f0853ca260ba34ac84a35, 15 workflow post-merge e sette risorse verificate; PR540 resta storicamente non conforme, nessuna sanatoria. BKL-051 OPEN / NOT_VALIDATED: S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata; IRSA21929/21930 risposte tecniche non attestate nell’ultima verifica conservata. Restano calibrazione/rumore/covarianze, astrometria/timing, pipeline/rapporto completi, recuperi ciechi/falsi positivi, moving objects/tracklet, integrazione autenticata di revisioni/formati provider/trasporto/esiti e policy quantitativa Owner. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. Nessuna nuova sessione cloud, credenziale, fotografia, soglia scientifica, invio astronomico o prova nativa; Safety e collegamento C→F invariati. [Dossier corrente](docs/project/BKL-051-S4-ISOLATED-CONCURRENCY-PREPARATION-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-ISOLATED-CONCURRENCY.md). [Baseline corrente](docs/project/CURRENT_TECHNICAL_BASELINE_2026-10-07.md).

## Snapshot precedente — prima della preparazione isolata

## Aggiornamento corrente — riconciliazione gate registro

PR540 è MERGED sul commit `93be5531da5243c79c3f3f03f9762095700a6f45`, ma il gate pre-merge behind-main è fallito dopo avanzamento PR541 e il comando di merge è stato eseguito erroneamente. Questa non conformità storica non è sanata retroattivamente. Il rilascio del registro resta INCOMPLETE in attesa del presente incremento correttivo, CI esatta, nuove ARB poi RQ sull’albero corrente e gate pre/post-merge validi. Il delta concorrente di sei file Allsky/SEO/nav/template è stato letto integralmente: nessuna sovrapposizione con i sorgenti del registro, preservati senza modifica. BKL-051 OPEN / NOT_VALIDATED; nessuna accettazione scientifica o authority. Tutti i residui scientifici, servizio/Owner/reporting/S4/S5 e i limiti precedenti restano interi; nessuna nuova sessione cloud, credenziale, soglia, fotografia o prova nativa. P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Dossier corrente](docs/project/BKL-051-S1-LEDGER-RELEASE-RECONCILIATION-2026-10-09.md).

## Snapshot precedente — prima della riconciliazione

## Aggiornamento corrente — cronologia delle revisioni, 9 ottobre 2026

BKL-051 OPEN / NOT_VALIDATED; P6 Accepted nei limiti. PR539 TNS/VSX rilasciata sul merge `3c4ab0a0aee8cc86f41c6223261fff040719a522`, ARB poi RQ sul commit esatto, 15 workflow post-merge e sette risorse pubblicate verificati. Nuovo registro locale delle revisioni private CBAT/MPC/TNS/VSX: snapshot verificata, digest indipendenti di ancora/testa, eventi create-only e revoca conservativa. Venti test sintetici del prototipo PASS; gate del nuovo incremento pending. Identità e UTC degli attori soltanto dichiarati; nessuna autenticazione Owner, accettazione scientifica, authority o invio. Tutta la pipeline scientifica/rapporto/servizio, rumore/calibrazione e covarianze, astrometria/timing, recuperi ciechi/falsi positivi, moving objects/tracklet, integrazione autenticata/policy/formati provider/trasporto/esiti/accessibilità/S5 restano aperti. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. IRSA21929/21930 sole prese in carico nell’ultima ricerca conservata, nessuna risposta tecnica o reinvio. Refunc ZTF diagnostico; prove native concluse non ripetute, evento noto non cieco, Gaia TOP100 incompleto e tempi condizionali. Nessuna nuova sessione cloud, credenziale, soglia o fotografia. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Dossier](docs/project/BKL-051-S1-PREVIEW-REVIEW-LEDGER-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-PREVIEW-REVIEW-LEDGER.md).

## Snapshot precedente — prima del registro delle revisioni

## Aggiornamento corrente — schede TNS/VSX, 9 ottobre 2026

BKL-051 OPEN / NOT_VALIDATED; P6 Accepted nei limiti. PR #536 conclusa sul merge `3f9c93d5e142a0f01c5676a7477dc7ad46519712`, ARB poi RQ AI-assistite, 15 workflow post-merge e sette risorse pubblicate verificati. Nuove schede private TNS/VSX API/CLI, 19 test sintetici iniziali PASS, precisione/unknown e provenienza conservate, nessun payload provider/invio/authority. TNS aperture dirette HTTP403 e soli estratti ufficiali indicizzati: schema/identificatori correnti non attestati; VSX guida consultata, nessun modulo automatizzato. Gate nuovo package pending. Refunc ZTF diagnostico, input storico/rumore interno/covarianze e calibrazione completa non attestati; IRSASD-21929/21930 sole prese in carico nell’ultima ricerca conservata, nessuna risposta tecnica o reinvio. Prove native concluse non ripetute, evento noto non cieco, Gaia TOP100 incompleto e tempi condizionali. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata; tutti i requisiti di pipeline/rapporto/servizio, validazione cieca, calibrazione/astrometria/timing/covarianze, moving objects/tracklet, reporting/ledger/revoca/esiti, policy Owner/accessibilità/S5 restano aperti. Cloud/build/OAT/probe precedenti conclusi; nessuna nuova sessione/credenziale/soglia/fotografia. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Dossier](docs/project/BKL-051-S1-TNS-VSX-REVIEW-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-TNS-VSX-REVIEW.md).

## Snapshot precedente — prima delle schede TNS/VSX

## Aggiornamento corrente — anteprima CBAT e refunc ZTF, 9 ottobre 2026

BKL-051 OPEN / NOT_VALIDATED; P6 Accepted nei limiti. PR #534 conclusa sul merge `719b455b9bb2b45d55ed7998c127a55b3bba951a`, ARB poi RQ AI-assistite e 15 workflow post-merge/sette risorse Pages verificati. Nuova anteprima CBAT locale ASCII per possibile nova galattica dichiarata: 15 test sintetici, precisione/unknown e byte-boundary conservati, controlli di catalogo non attestati; nessun invio o provider acceptance. Nuovo refunc ZTF completo acquisito e griglia confrontata con il riferimento pubblico, copertura locale diagnosticamente finita; input esatto, rumore interno/covarianze e calibrazione completa non attestati. IRSASD-21929 e IRSASD-21930 sole prese in carico, nessuna risposta tecnica attestata o reinvio. Prove native concluse non ripetute, evento noto non cieco, Gaia TOP100 incompleto e timing condizionale. Gate del nuovo package pendenti. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata; restano pipeline/rapporto scientifico/servizio completi, PSF con errore verificato, calibrazione/astrometria/tempi/covarianze, recuperi/falsi positivi ciechi, moving objects/tracklet, reporting/authority/receipts, policy Owner/accessibilità/S5. Cloud/build/OAT precedenti conclusi; nessuna nuova sessione, credenziale, soglia o fotografia. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Dossier](docs/project/BKL-051-S1-CBAT-NOVA-PREVIEW-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-CBAT-NOVA.md).

## Snapshot precedente — prima dell’anteprima CBAT

## Aggiornamento corrente — anteprima ADES e rumore ZTF, 9 ottobre 2026

BKL-051 OPEN / NOT_VALIDATED; P6 Accepted nei limiti. PR #530 conclusa e verificata sul merge `39d6e39977caaae2a68b56f493ec172417e6da4b`. Nuova anteprima ADES locale per oggetti numerati CCD/CMO/Gaia3: 13 test sintetici e XSD ufficiale fissato, due positivi/tre negativi; dichiarazioni non attestate, unknown preservati, nessun invio astronomico o attivazione. Riferimento ZTF completo verificato e checksum storico coincidente; input effettivo della sottrazione e budget completo del rumore ancora non attestati. Una nuova comunicazione IRSA rumore/provenienza autorizzata e inviata, distinta da IRSASD-21929; risposta tecnica non attestata. Gaia TOP100 incompleto e tempi ancora condizionali. Gate di consegna nuovo package pendenti. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano pipeline/misure native, calibrazione/astrometria/covarianze/tempi, recuperi/falsi positivi ciechi, moving objects/tracklet, reporting completo, servizio, policy Owner/accessibilità/S5. Build/OAT/probe cloud precedenti conclusi; nessuna nuova credenziale, soglia, fotografia o sessione. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Dossier](docs/project/BKL-051-S1-MPC-ADES-PREVIEW-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-MPC-ADES.md).

## Snapshot precedente — prima dell’anteprima ADES

## Aggiornamento corrente — adapter locale TPV, 9 ottobre 2026

P6 Accepted nei limiti; BKL-051 OPEN / NOT_VALIDATED. PR #529 rilasciata sul merge 2b66c184964ced44ec4b168b6740f024f255929d, 15 workflow post-merge e sette endpoint Pages verificati. Owner autorizza Astropy8.0.1/NumPy2.5.3 per il solo adapter locale TPV, PixInsight resta per misure native; nessun cloud/credenziale/soglia/invio. Adapter diagnostico, 10 test sintetici e trasformazione di 108 centri su sei FITS reali; non attesta frame/epoca/moto/covarianza o matching. Nuove PSF native: Atami72 e AT2018cow36, pixel e originali verificati, checkpoint/History/rami conservati; evento noto non cieco, fotometria non accettata. SN2023ixf primo prodotto404 conservato. IRSA ticket ricevuto, semantica UNC ancora irrisolta. Gate nuovo package pendenti. Restano pipeline scientifica completa, prove cieche/policy, rapporto/servizio completo, reporting e S5. Autorizzazioni cloud precedenti concluse. F4/F5, BKL-050, S10/Safety e C→F invariati. [Dossier](docs/project/BKL-051-S2-LOCAL-TPV-ADAPTER-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-LOCAL-TPV.md).

## Snapshot precedente — prima dell’adapter locale TPV

## Aggiornamento corrente — calibrazione fotometrica, 9 ottobre 2026

P6 Accepted nei limiti del dossier; BKL-051 OPEN / NOT_VALIDATED. PR #527 rilasciata e verificata: 15 workflow post-merge SUCCESS e sette endpoint Pages. Nuovo inspector fotometrico offline proposto: quattro variabili, sei covarianze, colore esplicito; semantica irrisolta blocca sigma e prodotti già calibrati/aperture non corrette non ricevono zero point. Fattorizzazione condivisa con contratto di coppia invariato. Audit dei tre cataloghi pubblici conservati: 76.932 righe compatibili con precisione decimale/float32, incertezza di calibrazione ancora irrisolta; richiesta IRSA autorizzata inviata, nessuna risposta attestata. Gate del nuovo package ancora da completare. Nessuna nuova query, credenziale, sessione cloud, fotografia o segnalazione astronomica. Cinque OAT, due build e due probe GCS conclusi. Restano pipeline e rapporto scientifico completi, timing/matching, multi-epoca, prove cieche/policy, intero servizio, reporting e S5. F4/F5, BKL-050, S10/Safety e C→F invariati. [Contratto e limiti](docs/project/BKL-051-S1-PHOTOMETRIC-CALIBRATION-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-PHOTOMETRIC-CALIBRATION.md).

## Snapshot precedente — prima del contratto fotometrico

## Aggiornamento corrente — coda/backup GCS, 9 ottobre 2026

P6 Accepted con i limiti del dossier; BKL-051 OPEN. PR #526 rilasciata e verificata: 15 workflow post-merge SUCCESS e sette endpoint Pages. Secondo probe coda/backup GCS singolo autorizzato PASS in 4,672 secondi: 43 richieste, due HTTP 412 reali, registrazioni e creazioni concorrenti conservate dopo retry, idempotenza senza riscrittura e sei backup verificati, compresi due candidati respinti non equivalenti a head. Primo tentativo fallito prima dello storage conservato. Codice invariato, namespace diagnostico nei due bucket esistenti: nessun control object operativo letto/scritto, servizio/IAM/traffico modificato o PixInsight avviato. Prova del nucleo coda/storage, non dell’intero servizio o login. Due autorizzazioni del probe consumate; cinque OAT e due build precedenti concluse. Restano intero servizio/regressioni, rapporto scientifico completo, calibrazione/covarianze/timing, pipeline multi-epoca, prove cieche/policy, reporting e S5. Nessuna scoperta, invio o fotografia pubblicata; F4/F5, BKL-050, S10/Safety e C→F invariati. [Evidenze](docs/project/BKL-051-S4-GCS-QUEUE-BACKUP-EVIDENCE-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-GCS-QUEUE-BACKUP.md).

## Snapshot precedente — prima del probe coda/backup GCS

## Aggiornamento corrente — ciclo nativo attivo, 9 ottobre 2026

P6 Accepted con i limiti del dossier; BKL-051 OPEN. PR #525 rilasciata e verificata: 15 workflow post-merge SUCCESS e sette endpoint Pages. Quinta OAT singola autorizzata conclusa in 792,91 secondi: due nuovi job e istanze native sintetiche. Owner annulla durante le misure: nativo/job CANCELLED dopo 292 righe. Fault locale dopo prima misura e prima del terminale: nativo CANCELLED dopo 13 righe, supervisore/job RECOVERY_REQUIRED; quiescenza e dichiarazione Owner sul dossier esatto verificate, nessun reset o replay. Entrambi i processi dedicati fermi; checkpoint e dump History conservati, 4.194.304 campioni bitwise invariati per ciascuna fixture. 66 richieste worker e 18 operazioni Owner entro limiti, 18 OPTIONS. Ripristino P6 100%, configurazione e permesso temporanei rimossi, verifica indipendente PASS. Le cinque autorizzazioni OAT sono consumate. Restano concorrenza/retry dell’intero servizio, rapporto scientifico completo, calibrazione/covarianze/timing, pipeline multi-epoca, prove cieche/policy, reporting e S5. Nessuna scoperta, invio o fotografia pubblicata; F4/F5, BKL-050, S10/Safety e C→F invariati. [Evidenze](docs/project/BKL-051-S4-ACTIVE-LIFECYCLE-EVIDENCE-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-ACTIVE-LIFECYCLE.md).

## Snapshot precedente — prima della quinta OAT

## Aggiornamento corrente — quarta OAT e recovery Owner, 9 ottobre 2026

P6 Accepted con i limiti del dossier; BKL-051 OPEN. PR #524 rilasciata e verificata: 15 workflow post-merge SUCCESS e sette endpoint Pages. Quarta OAT singola autorizzata conclusa in 930,74 secondi: tre nuovi job e tre istanze native sintetiche, tutti i processi dedicati fermi; checkpoint e History conservati. Recovery con perdita di osservazione locale dopo terminale nativo già presente, dichiarazione Owner legata al dossier esatto; vecchio tentativo ancora RECOVERY_REQUIRED. Risposta cloud COMPLETED scartata localmente prima dell’ACK, riconciliazione GET senza seconda POST o replay. Valutazione personale KEEP_FOR_REVIEW e ricevuta scaricata nel browser integrato, verificata contro rapporto e stato cloud. Annullamento durante il job NON superato: richiesta arrivata dopo COMPLETED, nessun rilancio. Probe GCS isolato: due scritture con stessa generazione, una riesce e una precondizione fallisce; non prova retry CAS dell’intero servizio. Ripristino P6 100%, configurazione e permesso temporanei rimossi, verifica indipendente PASS. Restano cancellazione integrata durante il nativo, recovery prima del terminale, concorrenza completa, pipeline e validazione scientifica, reporting e accettazione S5. Nessuna scoperta, invio o fotografia pubblicata; F4/F5, BKL-050, S10/Safety e C→F invariati. [Evidenze](docs/project/BKL-051-S4-FINAL-OAT-EVIDENCE-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-FINAL-OAT.md).

## Snapshot precedente — prima della quarta OAT

## Aggiornamento corrente — accessi Google e ciclo nativo, 9 ottobre 2026

P6 Accepted con i limiti del dossier; BKL-051 OPEN. PR #523 rilasciata e verificata dopo merge. Terza OAT Google conclusa: Owner HTTP 200, secondo account reale HTTP 403 e zero schede private; rollback e stato invariato verificati indipendentemente. Nuova prova locale PixInsight: cancellazione durante misure, checkpoint e History conservati, 4096 campioni invariati, handle proprio fermato. Due nuove prove con interruzione reale del socket loopback verificano riconciliazione senza seconda POST oppure recovery senza replay; storage sintetico, non OAT cloud. V6 diagnostico: 1033/439/1354 sorgenti, due posizioni su tre recuperate diagnosticamente; nessuna associazione o soglia accettata. Runtime corrente P6, transient disattivato. Restano ciclo completo portale/cloud, CAS concorrente reale, recovery/review/export Owner, pipeline scientifica, calibrazione/covarianze, prove cieche/policy, reporting e accettazione finale. Nessuna build, invio o fotografia pubblicata. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Evidenze](docs/project/BKL-051-ACCESS-LIFECYCLE-EVIDENCE-2026-10-09.md). [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-ACCESS-LIFECYCLE.md).

## Snapshot precedente
## Aggiornamento corrente — OAT e V5, 9 ottobre 2026

P6 Accepted con i limiti del dossier; BKL-051 OPEN. Dopo PR #522, due OAT cloud autorizzati e conclusi con rollback verificato: completamento tecnico sintetico Owner/nativo, annullamento prima dell’avvio, cinque GET negative e riconciliazione di ACK già ricevuto. Non provano risposta persa, CAS concorrente, cancel durante il nativo o account Google non-Owner. V4 osservato e chiuso; byte eseguiti ancora non attestati. V5 diagnostico completato: 639/206/1075 sorgenti, audit indipendente senza discrepanze di maschere/segnale e originali invariati; associazione Atami non accettata. Runtime corrente P6, transient disattivato; nessuna nuova build, invio o fotografia pubblicata. Pipeline scientifica, covarianze/calibrazione/timing, prove cieche/policy, lifecycle residuo, adattatori e accettazione finale restano aperti. Riconciliazione candidata ai gate, non chiusura milestone. [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-OAT-RECONCILIATION.md). F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e C→F invariati. [Riconciliazione OAT e diagnostica](docs/project/BKL-051-OAT-NATIVE-RECONCILIATION-2026-10-09.md).

## Snapshot precedente — prima degli OAT e di V5

P6 resta Accepted nei limiti del dossier. BKL-051 resta aperta. PR #521 riconcilia build e preparazione OAT sul merge `94f0b7aeb034499208d640de4c0e63f2a3a51ae8`: ARB poi RQ APPROVED zero finding, 16 check exact-head SUCCESS; post-merge e Pages attestati nella ricevuta privata di rilascio. Build autorizzata R2 SUCCESS con 155/155 prove offline e digest verificato; runtime P6 invariato, attivazione/OAT specifica ancora da autorizzare. Dossier locale #520 solo DRAFT, caller #519 e recovery #518 rilasciati. Dataset pubblico Atami: diagnostica nativa V3 completata ma INVALIDA per offset della maschera FITS; confronto di tutti i pixel prova +32768. Segnale importato invariato, nessuna misura o scoperta accettata. V4 ha un errore di destinazione conservato e nessuna esecuzione/fermata attestata entro il limite; genitore salvato e verificato su 49 file. Nessun nuovo lancio prima della verifica reale di processo/provenienza; V5 soltanto preparato, non autorizzato al lancio. Originali, History, checkpoint e tentativi conservati. Restano OAT PC/cloud, workflow scientifico, covarianze, calibrazione, blind validation, policy, moving objects e adattatori produttivi. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Nessun invio o pubblicazione fotografie; nessuna nuova elaborazione P6. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; S10/Safety e C→F junction invariati. [Handover corrente](docs/project/HANDOVER_2026-10-09-BKL051-NATIVE-DIAGNOSTICS.md).

## Snapshot storico — 7 ottobre 2026

P6 accettata operativamente dall’Owner il 7 ottobre 2026 con tutti i limiti del dossier, dopo collaudi reali e HOO completato. [Chiusura](docs/project/BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md); [handover corrente](docs/project/HANDOVER_2026-10-07-BKL051-S1.md). BKL-051 è il prossimo package approvato, preparazione S1 con fonti/probe pubblici e intake offline proposto; consegna P6 verificata nella PR #499. Decisioni architettura/query/dataset pendenti; nessun modulo operativo o runtime attivato. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; S10 e Safety invariati. Le sezioni precedenti sono snapshot storici, superati soltanto nei perimetri della chiusura accettata.


> Snapshot al 7 ottobre 2026: [handover P6/BKL-051](docs/project/HANDOVER_2026-10-07-BKL051-S1.md) e [baseline](docs/project/CURRENT_TECHNICAL_BASELINE_2026-10-07.md). Le sezioni precedenti conservano gli snapshot e i limiti delle prove; le note di candidato o consegna pendente sono superate soltanto nei perimetri del riepilogo corrente.

| Campo | Valore |
|---|---|
| Versione | 8.40 |
| Baseline | 09/10/2026 |
| Stato | Current root bootstrap — P6 accepted; BKL-051 Owner local/query direction approved, S1 open, S2 native solves with independent validation pending; BKL-043 lifecycle pending; S10 unavailable |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale
Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni e projection non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura
1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-10-09-BKL051-LOCAL-TPV.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-10-07.md`
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
5. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
6. `docs/project/BACKLOG.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/data/roadmap.json` — generated projection, non authority
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`
13. `docs/project/CODING_STANDARDS.md`
14. `docs/project/RELEASE_PLAYBOOK.md`
15. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
16. package, ADR, review, evidence e componenti direttamente coinvolti.

Gli handover e le baseline precedenti restano snapshot storici.

## 3. Stato corrente
- BKL-031: **Closed / Accepted / Post-Merge Verified** via PR #301 merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`.
- F3–F8: Accepted/Post-Merge Verified.
- F8 implementation: PR #279, reviewed head `3f05693482208df2b56b66dcb71162589880e72b`, merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`, 9/9 exact-head e 10/10 post-merge SUCCESS.
- F8 acceptance reconciliation: PR #280, reviewed head `bca410dcde804483052beded16c29a9f58f43872`, merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`, 17/17 exact-head e 19/19 post-merge SUCCESS; GitHub Pages build/integrity/deploy SUCCESS.
- F8 evidence: notte bounded 17–18/09/2026, forecast reale F7 site-specific, astronomia night-specific, suitability OTA/camera/filter esplicita, ranking/finestre advisory read-only.
- BKL-032 Session Readiness / Go-No-Go Decision Support è Closed / Accepted / Post-Merge Verified via PR #304; il suo evaluator resta read-only e il runtime source/transport è separatamente gated.
- BKL-036 è Closed come capability repository-only bounded; F3 Health Score resta `UNAVAILABLE`.
- AP-007 è **Accepted with conditions** come architecture baseline; non è un servizio operativo verificato.
- AP-008 è chiuso nel perimetro bounded read-only; non abilita command path, remediation o Safety Authority.
- BKL-042 è **Closed / Accepted** nel perimetro bounded read-only con limiti OAT espliciti.
- BKL-043 resta corrente: F4 attende lifecycle e accettazione finale secondo lo stato del 1 ottobre. BKL-049 archivio chiusa; M27 e importer aggiornati nel nuovo handover. Estensione BKL-049-EXT-PIAI autorizzata sul PC Owner, non produzione.
- S10 production runtime: `UNAVAILABLE`.

## 4. Boundary non negoziabili
- local physical interlocks = Safety Authority;
- BKL-032 = Session Readiness / Go-No-Go decision-support authority;
- BKL-031 = advisory/read-only, nessuna readiness/safety/action authority;
- nessun scheduler, automatic target selection o device command;
- coordinate sito protette mai in projection pubbliche;
- missing/stale/conflicted evidence fail-closed;
- provider/model/run lineage esplicita, nessun fallback/stitching silenzioso;
- il traffico MeteoHub F9 resta entro il modello ADR-012 governato: nessun limite giornaliero imposto dal workflow, budget EUR 0, fail-closed e GRIB effimeri.

## 5. Provider budget corrente
- F4-C generalized validation: `2/2_EXHAUSTED`;
- F7 protected-site one-shot: `1/1_EXHAUSTED`;
- F8: zero provider requests;
- F9 closure: refresh MeteoHub governato verificato; nessuna estensione di traffico oltre il limite ADR-012.

## 6. Disciplina di delivery
Exact-head CI → ARB → Release Quality sullo stesso SHA → expected-head merge → post-merge verification → acceptance reconciliation. Nessuna acceptance o runtime claim può precedere l'evidence reale.

## 7. Punto di ripresa storico del pilota — superato dal riepilogo del 7 ottobre
Riprendere dall’handover del 5 ottobre v2.0 e dal runbook PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md v1.1. P1–P3 e candidato P4 consegnati #479–#482; attivazione #483 post-merge verificata. P4 Owner HTTP sintetico, non-Owner negato, IAM/restore, restart/lost-ack, CAS GCS concorrente amministrativo e trasporto nativo amministrativo M27 verificati. P4 acceptance operativa resta aperta e concorrenza HTTP Owner soltanto sintetica; P5 è tecnicamente completata: prova scientifica Owner UI/nativa/consegna privata verificata; P6 e accettazione scientifica Owner sono successive. SESSION_ASSISTED senza nuove API IA; M27 pubblicata invariata, BKL-043 conserva i propri gate, nessuna authority dispositivi/Safety. Consegna CI/review e Pages della riconciliazione attuale da tracciare sulla PR.


## Aggiornamento P5 — portale scientifico privato (2026-10-05)

Implementato il candidato P5: pagina Owner, selezione di master M27 registrati, sessioni/catalogo e versione di riferimento esatti; job con contesto immutabile e verifica sul PC prima delle copie; stato/cancel espliciti, preview privata, workflow delle 29 azioni, correlazioni runtime e revisione Owner vincolata alla ricevuta. Originale e journal completo restano sul PC. Le identità IMG/VER/WF del pilota sono private e distinte dall’archivio di pubblicazione; nessun caricamento o pubblicazione automatica. SESSION_ASSISTED senza nuove API IA; classificazioni WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e History a monte NOT_ESTABLISHED preservate. Release/deployment consegnati tramite #485; la prova scientifica reale HTTP/UI → PixInsight → consegna/revisione resta un gate P5 aperto, non sostituito dai test. P6 e acceptance scientifica Owner restano successivi. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md).

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.

## Correzione compatibilità target durante il collaudo P5

Accesso Owner sulla nuova pagina verificato. Nessun job scientifico creato: confronto letterale `M27`/`M 27` rendeva invisibili le sessioni e il parent reali. Correzione con soli due alias espliciti, contesto originale conservato, tre regressioni e verifica locale dei profili pubblici reali (16 sessioni/un parent). Correzione candidata da rilasciare; il percorso Owner HTTP → nativo → consegna privata resta aperto. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md).


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](docs/project/PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](docs/project/evidence/BKL-049-PIAI-P5-2026-10-05.json).


## P5b — cartella dei master e prompt (candidato del 5 ottobre 2026)

Incremento autorizzato dall’Owner dopo l’accettazione privata P5 e la conferma dei download. Il modulo aggiunge cartella locale assoluta e prompt, richiesta privata di pianificazione, verifica esplicita sul PC, proposta immutabile e conferma Owner dell’esatto piano prima della coda PixInsight. Nessun job alla sola ricezione del prompt; nessuna lettura automatica del disco o esecuzione di testo/script dal browser. SESSION_ASSISTED: questa sessione interpreta il prompt e propone ricetta, parametri ammessi di fondo, dettaglio, rumore, contrasto e stretch, motivazione e limiti; nessuna nuova API IA, risorsa, credenziale o espansione IAM. Il perimetro richiesto include altri oggetti importati, LRGB, OSC, SHO/HOO e mosaici da pannelli. Il candidato comprende inventario e selezione esplicita; le nuove ricette per campo singolo richiedono parametri di campo verificati. OSC CFA e assemblaggio mosaici restano bloccati fino a implementazione e collaudo nativo. [Stato e procedura](docs/project/PIAI-P5B-SOURCE-PROFILES-2026-10-05.md). Nessuna estensione è ancora pubblicata o dichiarata accettata.

Il piano conserva ruoli R/G/B/L, dimensioni, selezione esplicita dell’immagine nei contenitori, impronta del manifest e sequenza dei 29 processi. Cartella, prompt e piano sono dati privati Owner; master/hash individuali e diagnostica locale restano sul PC. Il worker confronta cartella, piano e manifest prima delle copie. Aggiornamenti di catalogo o riferimenti conflittuali fermano l’approvazione; retry identici non duplicano richieste/job. I vecchi risultati P5 rimangono accessibili e invariati. Il candidato richiede CI sull’head esatto, ARB/RQ sequenziali, merge, deployment API/Pages e prova Owner della nuova procedura; non è ancora dichiarato disponibile nel portale pubblico. P6 e acceptance operativa restano aperti.


## P6 — collaudo isolato approvato il 7 ottobre 2026

Owner approva servizio, due bucket privati, identità e credenziale di prova dedicate. Ambiente cloud isolato attivo sul digest già rilasciato; concorrenza Owner e recupero nativo cloud reali ancora da eseguire. CFA/SHO reali e download CFA riconciliati con limiti espliciti. P6 resta aperta; accettazione operativa finale pendente. Nessuna mutazione del pilota operativo, gallery, dispositivi o Safety. BKL-051 Planned dopo chiusura P6. Piano corrente: [PIAI-P6-ISOLATED-OAT-2026-10-07.md](docs/project/PIAI-P6-ISOLATED-OAT-2026-10-07.md)

## P6 — collaudo completo, accettazione operativa pendente

Concorrenza Owner HTTPS reale, interruzione nativa isolata e nuovo worker, offline oltre 120 s, restart/rollback/forward del servizio di prova: PASS nei limiti documentati. Ambiente sospeso, archivi e prenotazioni conservati; stato della coda operativa byte-identico al baseline. HOO nativo sui master reali Drizzle2 ora PASS tecnico: 26 processi, 14 checkpoint, 26 coppie History, originali invariati; non accettazione estetica. P6 resta aperta per accettazione operativa; CFA è fixture tecnica da singola esposizione con decisione scientifica pendente. BKL-051 Planned dopo chiusura P6; F4/F5 e BKL-050 invariati. [Dossier finale e limiti](docs/project/PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md). Questa nota supera soltanto i residui tecnici provati, conserva snapshot e gate di consegna.

## P6 — accettazione operativa Owner

L’Owner conferma «Accetto operativamente P6 con i limiti del dossier». Nessuna esclusione HOO: collaudo nativo completato. Accettazione distinta da valutazione estetica e pubblicazione; CFA resta prova tecnica su singola esposizione, History a monte non attestata e recupero soltanto conservativo. [Chiusura](docs/project/BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md), [handover](docs/project/HANDOVER_2026-10-07-BKL051-S1.md). Gate di consegna exact-head e post-merge nella PR #499; nessun PASS anticipato.


### BKL-051 — capacità candidata offline (2026-10-15)

[Profilo esplicito del registro](docs/project/BKL-051-S1-CAMPAIGN-CAPACITY-2026-10-15.md): backend storico 32 binding/job, 1 MiB; profilo trusted CANDIDATE_59X3_V1 su registro isolato 512/8 MiB. Browser sola lettura 512/8 MiB. Nessuna adozione, migrazione, attivazione o replay impliciti. Milestone OPEN / NOT_VALIDATED, 37% indicativo, zero controlli qualificati. Rilascio subordinato a review indipendenti e gate sul commit esatto; cloud richiede nuovo perimetro approvato con conservazione di backup e versioni.


### BKL-051 — preparazione locale dei derivati, 2026-10-15

[Contratto e vista candidati](docs/project/BKL-051-S1-DERIVED-PREPARATION-VIEW-2026-10-15.md): ricevuta passiva per tre operatori senza job selezionati, con piano/provenienza/head corrispondenti, otto associazioni e quattro blocchi conservati. Produttore locale e lettore in memoria; nessun avvio o nuova autorità. Preparazioni e tentativi restano distinti. R01/R02/R09/R10/R14 parziali; milestone OPEN / NOT_VALIDATED, 37% indicativo, zero controlli qualificati. Nessuna nuova attivazione cloud o spesa; rilascio subordinato ai gate esatti e a verifiche postmerge.
