# Current Technical Baseline — 2026-10-05

| Campo | Valore |
|---|---|
| ID | DSG-BASELINE-20261005 |
| Versione | 1.6 |
| Stato | P1/P2/P3 and P4 candidate delivered; P4 approved cloud active; bounded native OAT; operational acceptance open |
| Data | 2026-10-05 |

La [baseline del 25 settembre](CURRENT_TECHNICAL_BASELINE_2026-09-25.md) conserva le foundation storiche. Il presente aggiornamento prevale per continuità, BKL-049 e M27; non promuove capability estranee.

## Stato attuale

- BKL-043 resta corrente e aperta; [F4 al 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md) attende lifecycle e accettazione finale. F5 resta subordinata.
- BKL-049 archivio available-history ed exact gallery linkage: chiusa/accettata nel [perimetro dichiarato](BKL-049-CLOSURE-2026-10-02.md).
- BKL-034 procedura foto/sessioni: caricamento manuale Owner-only e archiviazione separata, runbook in `infrastructure/scientific-photo-ingestion/README.md`; PR #474–#476.
- Importer PixInsight 1.2: PR #477 merged; esportatore multi-view 2.0.1. Esportazione/importazione non equivalgono a completezza universale o replay.
- M27 ultima versione: elaborazione locale nativa assistita, export 24 viste/80 processi/147 istanze; nuova pubblicazione verificata il 5 ottobre con 16 associazioni Owner-declared. [Handover ed evidenza](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).
- BKL-049-EXT-PIAI: P1 consegnata con PR #479; P2 consegnata con PR #480: cinque processi e checkpoint lineari. P3 ricetta non lineare provata: 29 azioni, 15 checkpoint e pixel finali verificati; confronto visivo effettuato, Owner acceptance richiesta. P4 cloud/worker implementati e attivati nel pilota con OAT parziale; P5/P6 pianificati, nessun modello IA di produzione.
- BKL-046 resta advisory/read-only, `aiModelImplemented=false`, efficacia scientifica non valutabile e produzione non pronta. Il pilota PixInsight è distinto.

## Contratti e autorità

AP-013 resta authority degli asset; AP-014 resta boundary di catalogo. Le 16 sessioni dichiarate non attestano contributo ai pixel. Il workflow pubblico contiene nomi di processi, non parametri privati; `executionEvidence=NOT_ESTABLISHED` e `captureCompleteness=PARTIAL` sono corretti per il contratto importato.

Il pilota autorizza esclusivamente elaborazione di file su copie locali sul PC dell’Owner. Autorità sui dispositivi e Safety Authority non cambiano; S10 production runtime rimane `UNAVAILABLE`. Nessuna nuova installazione, licenza, API a pagamento o accesso cloud viene inferita.

## Prossimo gate

P3 consegnata #481 e candidato P4 consegnato #482. Cloud/credenziale approvati e attivati; prova tecnica nativa circoscritta verificata; completare acceptance operativa prima della chiusura P4 e P5/P6. La modalità IA è SESSION_ASSISTED senza nuove API a pagamento; diritti commerciali/multiutente non attestati. Il [piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md) separa preflight, esecutore, elaborazione e integrazione futura. Registro: v1.0, riconciliazione 2026-10-05; review e consegna tracciate sulle PR.

Aggiornamento v1.1: preflight nativo e 13 test sintetici; [evidenza P1](evidence/BKL-049-PIAI-P1-2026-10-05.json). La disponibilità dei processi non attesta versioni/licenze/modelli.

Aggiornamento v1.2: [evidenza P2](evidence/BKL-049-PIAI-P2-2026-10-05.json), run completato, pre-cancel e replay nativi; integrità e identità esecutore verificate. 15 test esecutore e 20 coordinatore sintetici. Header verificati, qualità pixel/scientifica non certificata; nessun provider o mutazione del portale.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

Autenticazione Google Owner reale PASS sulla pagina diagnostica: creazione sintetica, ripetizione idempotente, annullamento e lettura CANCELLED/NONE. Google valido non-Owner negato e stale-create CAS reale negato senza mutazione. Riavvio del servizio sullo stesso digest e perdita deliberata dell’ack PREPARING dopo commit remoto: stessa richiesta recuperata, una preparazione; ciclo ripetuto con otto file identici.

Trasporto nativo sul PC verificato con due fixture amministrative isolate: pre-cancel con zero processi/output; M27 non lineare COMPLETED con 29 azioni, 15 checkpoint e 29 istanze workflow, originali invariati, finale Float32 RGB 4634×2808 e tutti i pixel finiti in [0,1]. Clipping misurato, non certificato assente. Raccolta dopo arresto PixInsight, prenotazioni chiuse e report remoto verificato. Questa prova usa Broker/BackedUpStore tramite CLI Owner amministrativa: non attesta ancora la creazione di un job scientifico dal comando HTTP/UI Owner. La prova HTTP Owner separata è sintetica; executionEvidence resta WORKER_REPORTED_NOT_ATTESTED, publication=NONE.

P4 ha ora una prova tecnica nativa circoscritta; CAS GCS concorrente reale PASS tramite CLI Owner amministrativa: due scritture degli stessi bytes di coda terminale, una accettata e una rifiutata per generazione obsoleta, backup verificato e stato logico invariato. Concorrenza sulle route Owner HTTP soltanto sintetica; acceptance operativa più ampia resta aperta. P5 comando scientifico/sessioni/preview/provenance, P6 e acceptance scientifica Owner sono successivi. SESSION_ASSISTED, zero nuove chiamate API IA; M27 pubblicata e autorità dispositivi/Safety invariate. Evidenza privata conservata; ricevuta pubblica minimizzata e runbook collegati sopra. CI/review/merge e Pages di questa riconciliazione sono da verificare sulla PR di consegna.

Osservazione reale dopo oltre 120 secondi senza contatto: OFFLINE diagnostico, stesso job/root ancora RUNNING, nessuna scadenza o riassegnazione osservata. Non è una prova di crash recovery del desktop.

Derivati locali TIFF RGB16/JPEG sRGB verificati; soluzione astrometrica conservata e checkpoint invariato dopo export. History disponibile: 13 viste, 47 passi, 82 istanze, 429679 byte; importer 1.2 PARSED_SUBSET. La History conservata non prova completezza a monte: executionEvidence=NOT_ESTABLISHED e workflowCompleteness=UNAVAILABLE del file importato restano invariati. Journal e correlazioni runtime delle 29 azioni conservati separatamente. Campo intero/dettaglio coerenti con la ricetta P3; nessuna superiorità scientifica o sostituzione pubblica dichiarata.
