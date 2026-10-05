# Current Technical Baseline — 2026-10-05

| Campo | Valore |
|---|---|
| ID | DSG-BASELINE-20261005 |
| Versione | 1.1 |
| Stato | Current reconciliation; native pilot P1 tested |
| Data | 2026-10-05 |

La [baseline del 25 settembre](CURRENT_TECHNICAL_BASELINE_2026-09-25.md) conserva le foundation storiche. Il presente aggiornamento prevale per continuità, BKL-049 e M27; non promuove capability estranee.

## Stato attuale

- BKL-043 resta corrente e aperta; [F4 al 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md) attende lifecycle e accettazione finale. F5 resta subordinata.
- BKL-049 archivio available-history ed exact gallery linkage: chiusa/accettata nel [perimetro dichiarato](BKL-049-CLOSURE-2026-10-02.md).
- BKL-034 procedura foto/sessioni: caricamento manuale Owner-only e archiviazione separata, runbook in `infrastructure/scientific-photo-ingestion/README.md`; PR #474–#476.
- Importer PixInsight 1.2: PR #477 merged; esportatore multi-view 2.0.1. Esportazione/importazione non equivalgono a completezza universale o replay.
- M27 ultima versione: elaborazione locale nativa assistita, export 24 viste/80 processi/147 istanze; nuova pubblicazione verificata il 5 ottobre con 16 associazioni Owner-declared. [Handover ed evidenza](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).
- BKL-049-EXT-PIAI: estensione autorizzata; preflight P1 nativo verificato, esecutore P2 ed elaborazione P3 ancora pianificati. Nessun worker remoto o modello IA di produzione già implementato.
- BKL-046 resta advisory/read-only, `aiModelImplemented=false`, efficacia scientifica non valutabile e produzione non pronta. Il pilota PixInsight è distinto.

## Contratti e autorità

AP-013 resta authority degli asset; AP-014 resta boundary di catalogo. Le 16 sessioni dichiarate non attestano contributo ai pixel. Il workflow pubblico contiene nomi di processi, non parametri privati; `executionEvidence=NOT_ESTABLISHED` e `captureCompleteness=PARTIAL` sono corretti per il contratto importato.

Il pilota autorizza esclusivamente elaborazione di file su copie locali sul PC dell’Owner. Autorità sui dispositivi e Safety Authority non cambiano; S10 production runtime rimane `UNAVAILABLE`. Nessuna nuova installazione, licenza, API a pagamento o accesso cloud viene inferita.

## Prossimo gate

Consegnare la riconciliazione con CI/review e poi verificare l’ambiente reale PixInsight, implementare manifest ed esecutore locale controllato e registrare un primo test. Il [piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md) separa preflight, prova di elaborazione e integrazione futura. Registro: v1.0, riconciliazione 2026-10-05; review e consegna tracciate sulla PR.

Aggiornamento v1.1: preflight nativo e 13 test sintetici; [evidenza P1](evidence/BKL-049-PIAI-P1-2026-10-05.json). La disponibilità dei processi non attesta versioni/licenze/modelli.
