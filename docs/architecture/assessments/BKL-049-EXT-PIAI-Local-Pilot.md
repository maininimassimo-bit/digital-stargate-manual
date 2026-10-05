# BKL-049-EXT-PIAI — Pilota locale PixInsight con IA

| Campo | Valore |
|---|---|
| ID | BKL-049-EXT-PIAI |
| Versione | 1.5 |
| Stato | Owner-authorized pilot; architecture/release review required |
| Data | 2026-10-05 |
| Dipendenze | BKL-049 archive; importer 1.2; Owner PC/PixInsight; calibrated aligned masters |

## Scopo e baseline

Rendere ripetibile l’elaborazione assistita già effettuata su M27, sul PC dell’Owner con PixInsight installato. L’archivio BKL-049 rimane chiuso; questa estensione aggiunge un nuovo perimetro di elaborazione file, senza riaprire o alterare l’acceptance precedente. Le licenze già presenti evitano una nuova installazione nel primo test personale, ma non attestano diritti per servizio commerciale/multiutente. Versione dichiarata: PixInsight 1.9.5 build 1706; versioni e disponibilità effettive dei moduli devono essere registrate dal preflight.

## Architettura prevista

```mermaid
flowchart LR
    O[Owner e master privati] --> M[Manifest locale verificato]
    A[Assistente IA: piano motivato] --> V[Validatore della ricetta]
    M --> V
    V --> P[PixInsight: processi nativi su copie]
    P --> J[Journal e output privati]
    J --> Q[Verifica tecnica e valutazione Owner]
    Q --> E[Export History e importazione governata]
```

Il primo pilota usa l’assistente della sessione e una ricetta esplicita; non richiede chiamate API a pagamento. L’IA propone operazioni e parametri entro un insieme ammesso; PixInsight applica i pixel. Il journal futuro registra input/output e relazioni al momento dell’azione, così non dipende solo dalle correlazioni incomplete della History.

Un futuro worker sul PC riceverà job attraverso connessione autenticata in uscita. Il backend conserverà stato e coda; nessuna porta pubblica sul desktop. Credenziale dedicata, protocollo, provider/modello/costi e autorizzazioni cloud richiedono un pacchetto concreto successivo. La sola installazione PixInsight e l’abbonamento alla chat non rendono disponibile questa infrastruttura.

## Fasi e criteri di uscita

| Fase | Risultato richiesto | Stato iniziale |
|---|---|---|
| P1 — Preflight | Prova nativa M27 eseguita il 5 ottobre: PI 1.9.5 build 1706, quattro master invariati, 12 costruttori di processo disponibili; versioni moduli/licenze/modelli non attestati | Delivered #479; native PASS |
| P2 — Esecutore locale | Coordinatore locale, copie, snapshot esecutore, ricetta lineare fissa, journal e checkpoint; prova nativa completa, pre-cancel e replay | Delivered #480; native PASS |
| P3 — Prova M27 | Input bloccati, output non lineare, verifiche finite/dimensioni/colore, confronto visivo; nessuna accettazione scientifica automatica | Delivered #481; native technical/visual PASS; Owner acceptance open |
| P4 — Connessione e IA | Candidato autenticato/coda/adapter e recupero offline; SESSION_ASSISTED senza nuove API IA; proposta cloud distinta | Delivered #482; Owner-approved cloud active; partial live OAT; Owner login/native transport pending |
| P5 — Portale e provenance | Comando Owner, stato, preview, revisione e collegamento esatto a sessioni e workflow | Planned |
| P6 — Acceptance | Casi errore/annullamento/offline, integrità originali, evidenza reale, review e rollback | Planned |

La disponibilità futura nel portale dipende da P4–P6. Il successo della vecchia elaborazione M27 non dimostra il funzionamento del nuovo worker.

## Regole dell’esecutore

Manifest versionato, ID univoco, input selezionati con integrità, destinazione separata, ricetta e limiti espliciti. Un job alla volta. Rifiutare input mancanti, risultati precedenti, conflitti e processi non ammessi; niente esecuzione di script forniti dal portale. Non usare i master come target modificabili. Se un modulo richiesto manca, fermare il job senza sostituirlo tacitamente. Non miscelare lavoro manuale e job automatico sulla stessa istanza.

Per cancellare, controllare il segnale prima del prossimo processo e conservare il journal. Un processo nativo lungo può terminare prima dell’annullamento; non è promesso un arresto immediato. Crash o risultati parziali restano evidenza privata e non passano a `COMPLETED`. Nessun upload/publicazione deriva dal completamento locale.

## Privacy, rischi e prove

Percorsi, immagini, modelli plugin e parametri delle ricevute restano privati. Git conserva codice, default della ricetta revisionata, documenti e prove sintetiche/minimizzate; non pubblica le sorgenti native integrali dei run. La catena runtime registrata e l’export storico importato hanno classificazioni distinte. Sessioni associate per dichiarazione non diventano origine pixel provata.

Rischi: desktop non disponibile, occupazione RAM/disco, moduli mancanti, incompatibilità PJSR, gradienti/dati inadatti alla ricetta e qualità variabile. Le operazioni originali su M27 non sono una ricetta universale LRGB. L’Owner valuta il risultato prima di qualsiasi pubblicazione; il pilota conserva la versione pubblicata attuale.

Acceptance P1/P2: prove di rifiuto per identità/input incoerenti e destinazione conflittuale; un preflight nativo reale deve lasciare input e progetto invariati. Acceptance P3: job reale separato e output verificato. Test sintetici non sostituiscono PixInsight, licenze o giudizio scientifico.

## Riferimenti e revisione

[Handover](../../project/HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md), [baseline](../../project/CURRENT_TECHNICAL_BASELINE_2026-10-05.md), [closure archivio](../../project/BKL-049-CLOSURE-2026-10-02.md), [importer 1.2](BKL-049-Portal-Importer-1.2.md).

Versione 1.0: piano autorizzato il 5 ottobre, nessuna fase dichiarata accettata prima di esecuzione/review. Rollback: interrompere nuovi job, conservare ricevute e output parziali, ritirare il codice aggiuntivo; originali e gallery non richiedono modifica.

## P1 — prova nativa 2026-10-05

La [ricevuta minimizzata](../../project/evidence/BKL-049-PIAI-P1-2026-10-05.json) registra il primo controllo reale. Il primo tentativo ha rifiutato correttamente il contenitore XISF multi-image: master più maschera di ritaglio. La selezione esplicita dell’indice immagine e delle dimensioni attese ha consentito il secondo test. Quattro master monocromatici Float32 4634×2808, 12 costruttori richiesti disponibili, integrità dei file confermata dopo il run, zero master modificati, zero processi applicati e zero richieste provider. Parametri, percorsi e digest privati non sono pubblicati.

Libreria `tools/pixinsight/local_pilot/preflight.jsh`; 13 test sintetici di rifiuto/selezione passati localmente. I test CI usano stub e non sostituiscono il test nativo. Le versioni dei moduli non sono esposte da ProcessInstance e restano sconosciute; disponibilità dei costruttori non prova licenza o caricamento dei modelli RC. Il risultato P1 non produce una nuova foto né modifica la gallery. Versione 1.1: prova nativa P1; consegnata con PR #479, merge `76d6186489c78aceb32f34a6b96afbe8f88457a7`, 17 controlli exact-head e 16 workflow post-merge SUCCESS, review sequenziali senza finding finali.

## P2 — esecutore e prove native 2026-10-05

Implementati `worker.py` e `executor.jsh`, con [procedura operativa nel repository](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/pixinsight/local_pilot). La ricetta `LRGB_LINEAR_PREP_V1` applica quattro ABE alle copie R/G/B/L e compone RGB: cinque processi, cinque checkpoint XISF Float32 lineari. La luminanza è preparata ma non ancora integrata. Non è una foto finale né una ricetta universale. Calibrazione colore, astrometria RGB, riduzione rumore, dettaglio, stretch e confronto visivo restano P3.

La [ricevuta minimizzata P2](../../project/evidence/BKL-049-PIAI-P2-2026-10-05.json) distingue la prova reale dai test sintetici. Run nativo completato: cinque processi/checkpoint, file originali e viste di input invariati, snapshot dello script e header verificati. Pre-cancel nativo: zero processi/output. Replay nativo rifiutato: tutti i 37 file del job concluso invariati. Seconda preparazione nello stesso worker root rifiutata. Test locali: 13 preflight, 15 esecutore, 20 coordinatore; l’errore nativo simulato non è presentato come OAT fisica.

Una prenotazione locale e un handle File esclusivo Windows, verificato a runtime prima dei pixel, serializzano un root configurato. Non è un lock globale di più worker. Il lancio resta supervisionato da Script → Execute Script File. Crash o preparazione incompleta conservano la prenotazione; nessuna ripresa o scadenza automatica. Per recuperare, confermare l’arresto di PixInsight, conservare/quarantinare il root e usare un root nuovo. Non forzare lo sblocco di un job vivo.

Le sorgenti native di ogni processo restano esatte nel journal privato. `workflow.js` esporta solo le cinque istanze riuscite, con identificatori rinominati e valori letterali preservati; il lettore 1.2 le legge come dati. Le correlazioni runtime restano separate; questa prova non rende completa la History a monte e non modifica il contratto pubblico importato. Nessuna API provider, connessione remota, modifica gallery o accettazione scientifica. Versione 1.2: P2 implementato e provato nativamente; delivery, CI e review da registrare sulla PR del relativo head.

Una seconda prova nativa completa conferma anche la correlazione dell’immagine creata da ChannelCombination: il target registrato al completamento coincide con l’output salvato. Entrambi i run e le ricevute restano privati e immutati.

Riesame P2: un Major ARB ha rilevato che il comando cancel tentava di leggere il file tenuto con handle esclusivo. Corretto con identità immutabile del job separata e marker completo pubblicato atomicamente, vincolato al token e verificato dal runtime. Prova Windows con handle reale e prova nativa PixInsight: lettura del lease negata, comando cancel riuscito durante il primo processo; arresto prima del checkpoint successivo, un processo registrato, zero output e originali invariati. Il processo in corso può terminare prima dell’annullamento. Il riesame finale richiede CI e ARB/RQ sul nuovo head.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

## P3 — ricetta non lineare e verifica

`M27_LRGB_NONLINEAR_V1` aggiunge alla preparazione lineare la correzione radiale, calibrazione stellare empirica, BXT/NXT lineari, SXT, stretch separato RGB/L, maschera di luminanza, contrasto locale, combinazione LRGB, colore selettivo e ricomposizione delle stelle. Non usa SPCC e non certifica colori fotometrici. La ROI relativa è specifica del campo M27: un altro soggetto richiede una nuova ricetta revisionata. I costruttori sono verificati prima dei pixel; l’esecuzione effettiva dei plugin attesta disponibilità per quel run, non licenze, versione o hash del modello.

Un run completo richiede 29 azioni native e 15 checkpoint XISF. I metadati della combinazione RGB sono mantenuti; il finale è marcato LRGB/non lineare senza attribuire esposizione aggregata non ricostruita. Le relazioni private registrano copie, output stelle, maschere e inversione. Le 29 istanze derivate sono dati per l’importer, non replay o History integrale a monte.

La raccolta controlla integrità, geometria, canali e ordine/processi della ricetta. Sul finale legge tutti i pixel Float32, rifiutando non finiti, intervallo non normalizzato, canali costanti, blocchi troncati e formati non supportati. Per questo pilota è richiesto XISF planar little-endian senza compressione. Conta clipping ed estremi per canale senza dichiararli assenti. Se la raccolta fallisce, la prenotazione resta conservata anche con ricevuta di esecuzione `COMPLETED`.

Confronto visivo e valutazione Owner restano distinti dall’esito tecnico. Originali e M27 pubblicata restano invariati; P4–P6 non sono attivati. La prova tecnica/visiva è registrata di seguito; consegna e review di questo head sono tracciate sulla PR.

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](../../project/evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

Verifica candidato P4: 33 test Node e 62 Python Windows, inclusi 32 casi trasporto. [Ricevuta minimizzata](../../project/evidence/BKL-049-PIAI-P4-2026-10-05.json). CI/review dello stesso head e post-merge da registrare sulla PR; nessuna attivazione cloud anticipata.

Riesame P4: un Major ARB ha riprodotto una seconda preparazione su root nuovo privo di binding. Corretto con identità locale persistente fissata dalla prima claim e transizione PREPARING confermata prima delle copie; claim avanzata senza binding rifiutata. Cinque regressioni coprono nuovo root, stati avanzati, perdita della risposta iniziale e preparazione interrotta. CI e riesame finale dello stesso head richiesti sulla PR.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](../../project/evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](../../project/PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

Autenticazione Google Owner e prova nativa tramite trasporto non ancora eseguite. Pagina diagnostica P4 separata dalla navigazione principale: prova sintetica crea/legge/annulla, credenziale solo in memoria, destinazione approvata fissata per digest. Non abilita P5 né comandi scientifici dal portale. P4 OAT/P5/P6 e acceptance Owner restano aperti. M27 pubblicata e autorità dispositivi/Safety invariate.
