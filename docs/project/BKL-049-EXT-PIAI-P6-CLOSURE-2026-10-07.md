# BKL-049-EXT-PIAI — chiusura operativa P6

| Campo | Valore |
|---|---|
| Package | BKL-049-EXT-PIAI |
| Stato | Accepted |
| Versione | 1.0 |
| Data | 2026-10-07 |
| Owner | Massimo Mainini |
| Accettazione | Accetto operativamente P6 con i limiti del dossier |
| Release evidence | [PR #499](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/499): exact-head CI, ARB/RQ sequenziali, expected-head merge e post-merge/Pages richiesti prima di dichiarare la consegna verificata |

L’Owner ha accettato esplicitamente il pilota SESSION_ASSISTED nei casi effettivamente verificati LRGB, OSC RGB/CFA, mosaico, SHO e HOO, con i limiti del [dossier operativo](PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md). La precedente approvazione delle risorse isolate e le accettazioni private delle fotografie restano eventi separati. Nessun pulsante di revisione scientifica è stato azionato dall’assistente e nessuna fotografia è pubblicata.

## Evidenze che chiudono i residui

- Profili reali: M27 LRGB e M31 OSC/mosaico con decisioni private conservate; CFA reale RGGB calibrato con Debayer, consegna e download verificati; SHO e HOO nativi sui master reali, nuova SHO Drizzle2 accettata privatamente. HOO è stato completato su richiesta Owner prima di acceptance, senza esclusione del profilo: 26 processi, 14 checkpoint, 26 coppie di esportazioni History e originali invariati.
- Owner HTTPS reale: due create contemporanee, un solo job; due cancel contemporanei, CANCELLED/NONE. Non prova CAS interno interleaved in un servizio serializzato.
- Recupero conservativo: nuovo processo PixInsight isolato su copie sintetiche interrotto dopo process-started e prima della ricevuta; nuovo processo worker stesso root/claim, RECOVERY_REQUIRED, binding e 14 file invariati, secondo job QUEUED confermato Owner. Nessun replay o riassegnazione.
- Offline oltre 120 s e restart/rollback/forward del solo servizio isolato: stato primario byte-identico, backup corrispondente. Ambiente esterno sospeso, risorse/evidenze/prenotazioni conservate; produzione byte-identica al baseline.
- Portale: accesso Owner, anteprima/workflow e tre download CFA realmente salvati; workflow identico all’export nativo, correlazioni identiche all’export minimizzato governato e impronte conformi alla ricevuta. Esiti storici negativi non riscritti.

## Limiti accettati

CFA è prova tecnica su una singola esposizione calibrata, non un master integrato né una fotografia finale accettata esteticamente; decisione scientifica nel portale ancora pendente e discrepanza temporale delle sessioni dichiarate conservata. I casi provati non certificano ricette universali o tutti i campi. SHO/HOO sono palette assegnate; il nuovo HOO non usa SPCC e non è certificazione fotometrica. Nel finale HOO sono presenti 9 campioni saturi nel rosso e 6541/1/9 campioni a zero R/G/B: clipping misurato, non assente.

History a monte NOT_ESTABLISHED; un temporaneo grigio del precedente tentativo SHO fallito non fu esportato separatamente, con journal/input e ramo successivo conservati. History runtime, maschere, checkpoint, tentativi e genitori restano privati. L’archivio HOO dipende dagli XISF e master conservati separatamente, non è un replay autonomo. WORKER_REPORTED_NOT_ATTESTED e OWNER_DECLARED non diventano attestazione remota o provenance indipendente.

Non sono dimostrati power-loss, crash desktop o recupero automatico. Il blocco conservativo preserva prenotazioni ambigue e non offre reset/sblocco della coda. La prima sola rimozione IAM non aveva ancora impedito l’accesso osservato; sospensione attestata solo dopo controllo IAM e ingresso interno, HTTP esterno 404. Nessuna risorsa cancellata.

## Sequenza e rollback

BKL-049 archivio resta chiusa nel proprio perimetro; questa acceptance chiude l’estensione PIAI/P6 entro i limiti sopra. Il prossimo package approvato è BKL-051, con sola preparazione S1 e sviluppo dopo consegna P6 verificata. Nessun modulo o nuovo runtime è dichiarato implementato. BKL-043 F4 attende lifecycle reale, F5 dopo piena accettazione F4; BKL-050 resta conclusiva, S10 UNAVAILABLE e Safety/device authority invariati. Junction C→F non modificata.

Rollback della consegna: revert governato dei documenti e rigenerazione delle projection, conservando l’evento Owner accettato e tutte le evidenze. Non cancellare file, non riscrivere decisioni immutabili o code, non riattivare il servizio di prova automaticamente. [Evidenza minimizzata](evidence/BKL-049-PIAI-P6-ISOLATED-RESULTS-2026-10-07.json).
