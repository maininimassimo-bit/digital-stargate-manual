# Current Technical Baseline — 2026-10-05

| Campo | Valore |
|---|---|
| ID | DSG-BASELINE-20261005 |
| Versione | 1.3 |
| Stato | P1/P2 delivered; P3 native technical trial passed; Owner acceptance required |
| Data | 2026-10-05 |

La [baseline del 25 settembre](CURRENT_TECHNICAL_BASELINE_2026-09-25.md) conserva le foundation storiche. Il presente aggiornamento prevale per continuità, BKL-049 e M27; non promuove capability estranee.

## Stato attuale

- BKL-043 resta corrente e aperta; [F4 al 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md) attende lifecycle e accettazione finale. F5 resta subordinata.
- BKL-049 archivio available-history ed exact gallery linkage: chiusa/accettata nel [perimetro dichiarato](BKL-049-CLOSURE-2026-10-02.md).
- BKL-034 procedura foto/sessioni: caricamento manuale Owner-only e archiviazione separata, runbook in `infrastructure/scientific-photo-ingestion/README.md`; PR #474–#476.
- Importer PixInsight 1.2: PR #477 merged; esportatore multi-view 2.0.1. Esportazione/importazione non equivalgono a completezza universale o replay.
- M27 ultima versione: elaborazione locale nativa assistita, export 24 viste/80 processi/147 istanze; nuova pubblicazione verificata il 5 ottobre con 16 associazioni Owner-declared. [Handover ed evidenza](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).
- BKL-049-EXT-PIAI: P1 consegnata con PR #479; P2 consegnata con PR #480: cinque processi e checkpoint lineari. P3 ricetta non lineare provata: 29 azioni, 15 checkpoint e pixel finali verificati; confronto visivo effettuato, Owner acceptance richiesta. P4–P6 restano pianificati. Nessun worker remoto o modello IA di produzione già implementato.
- BKL-046 resta advisory/read-only, `aiModelImplemented=false`, efficacia scientifica non valutabile e produzione non pronta. Il pilota PixInsight è distinto.

## Contratti e autorità

AP-013 resta authority degli asset; AP-014 resta boundary di catalogo. Le 16 sessioni dichiarate non attestano contributo ai pixel. Il workflow pubblico contiene nomi di processi, non parametri privati; `executionEvidence=NOT_ESTABLISHED` e `captureCompleteness=PARTIAL` sono corretti per il contratto importato.

Il pilota autorizza esclusivamente elaborazione di file su copie locali sul PC dell’Owner. Autorità sui dispositivi e Safety Authority non cambiano; S10 production runtime rimane `UNAVAILABLE`. Nessuna nuova installazione, licenza, API a pagamento o accesso cloud viene inferita.

## Prossimo gate

Consegnare P3 già provata nativamente/visivamente con CI e review sullo stesso head. Successivamente definire il pacchetto concreto P4; provider, costi, diritti e protocollo rimangono da decidere. Il [piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md) separa preflight, esecutore, elaborazione e integrazione futura. Registro: v1.0, riconciliazione 2026-10-05; review e consegna tracciate sulle PR.

Aggiornamento v1.1: preflight nativo e 13 test sintetici; [evidenza P1](evidence/BKL-049-PIAI-P1-2026-10-05.json). La disponibilità dei processi non attesta versioni/licenze/modelli.

Aggiornamento v1.2: [evidenza P2](evidence/BKL-049-PIAI-P2-2026-10-05.json), run completato, pre-cancel e replay nativi; integrità e identità esecutore verificate. 15 test esecutore e 20 coordinatore sintetici. Header verificati, qualità pixel/scientifica non certificata; nessun provider o mutazione del portale.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.
