# P6 — dossier per accettazione operativa

Stato: **prove cloud isolate e collaudo nativo HOO completati; P6 aperta per accettazione operativa Owner**. BKL-049 archivio resta chiusa nel suo perimetro. BKL-051 resta Planned dopo chiusura P6; BKL-043 F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. Nessuna fotografia pubblicata e nessuna elaborazione scientifica già conclusa ripetuta.

## Prove concluse

La riconciliazione scientifica e i suoi limiti sono nel [piano isolato](PIAI-P6-ISOLATED-OAT-2026-10-07.md): M27 LRGB con accettazione privata, M31 OSC/mosaico con ACCEPT_PRIVATE riconfermata, CFA reale singola esposizione RGGB con Debayer e consegna, ricetta SHO nativa e ultima SHO Drizzle2 SPCC accettata privatamente. Riverificati tutti i 43 checkpoint della nuova SHO, tre master e riferimento Owner. Nel browser Owner sono stati realmente scaricati e confrontati workflow CFA, correlazioni minimizzate e ricevuta.

Il collaudo residuo è stato eseguito sull’ambiente dedicato, dopo approvazione Owner delle risorse. Pagina PR #498, head `431c35db6c3a0d30798bf255bf59e256161e6251`, merge `bd84aff31fd86a0a05e0794ad20cb2829cc04bb9`: 19 check pre-merge positivi, ARB/RQ AI-assisted process-separated senza finding, 18 workflow post-merge positivi inclusa Pages, script pubblico conforme al merge. Backend immutabile `sha256:33547c26692f639cc4bf580ba4899dd97e253fde1ed8e4546c3c9d3ae7cc7d3d`, origine `f2afb30f9fafb906895e7c937ba8b23f51357452`.

| Prova reale | Esito e limite |
|---|---|
| Owner Google e HTTPS, due create e due cancel contemporanei | Un solo job, CANCELLED/NONE. Concorrenza client; servizio serializzato, nessun interleaving CAS interno attestato |
| Processo nativo isolato su copie sintetiche | Interrotto dopo evento process-started e prima della ricevuta terminale; RECOVERY_REQUIRED trasmesso al servizio reale |
| Nuovo processo OS worker, stesso root | Stessa claim, prenotazioni e binding conservati, 14 file invariati, originali/copie identici, nessun replay; Owner conferma secondo job QUEUED |
| Offline oltre 120 secondi | Owner legge OFFLINE, primo RECOVERY_REQUIRED e secondo QUEUED, nessuna riassegnazione |
| Riavvio servizio sul medesimo digest | Seconda revisione isolata pronta, stato primario byte-identico, backup corrispondente |
| Rollback/forward traffico solo servizio isolato | Stato identico sulla prima e sulla seconda revisione; nessun ripristino di stato precedente |
| Sospensione ambiente | allUsers invoker rimosso, controllo IAM attivo, ingress internal-only; chiamata esterna HTTP 404. Risorse, credenziale protetta, root e ricevute conservati |
| Produzione | Stato coda finale byte-identico al baseline iniziale; nessuna mutazione di servizio operativo, IAM, credenziale, root o fotografie |

La sola rimozione IAM non aveva ancora respinto la chiamata osservata: esito intermedio conservato, non PASS. L’isolamento di ingresso è stato verificato prima di dichiarare sospensione. Nessuna cancellazione di risorse. La prova dimostra un arresto controllato del nuovo PID, non power-loss o crash del desktop. Il blocco conservativo è deliberato: non offre sblocco o recupero automatico della coda.

## Collaudo HOO e accettazione finale richiesta

Il nuovo collaudo HOO sui master reali Drizzle2 Hα/OIII è **PASS tecnico**: 26 processi, 14 checkpoint, 26 coppie di esportazioni History iniziale/corrente, copie e originali invariati. Geometria 6230×4154, RGB Float32, tutti i pixel finiti e nell’intervallo [0,1]. Saturazione finale: 9 campioni nel rosso, zero nel verde/blu; campioni a zero R/G/B: 6541/1/9. Clipping misurato, non dichiarato assente. Hα→R, OIII→G/B, luminanza derivata da Hα; palette assegnata senza SPCC, nessuna certificazione fotometrica. Ricetta nativa del pilota invariata, snapshot locale esteso soltanto per esportare la History di checkpoint e viste terminali. Lo ZIP History/workflow dipende dagli XISF e master privati conservati, non è replay autonomo. La validazione tecnica non costituisce accettazione estetica o pubblicazione.

CFA dimostra una singola esposizione reale calibrata, non master integrato; discrepanza con sessioni dichiarate conservata e valutazione scientifica della fixture ancora pendente nel portale. History a monte NOT_ESTABLISHED; un temporaneo grigio del tentativo SHO fallito non fu esportato separatamente, con journal/input e ramo successivo conservati. Nessuna soglia scientifica, ricetta universale o completezza retroattiva della History è certificata. Accettazione richiesta per il pilota SESSION_ASSISTED nei casi effettivamente provati LRGB, OSC RGB/CFA, mosaico, SHO e HOO, con questi limiti e con CFA qualificata come prova tecnica.

Il 7 ottobre l’Owner ha richiesto esplicitamente HOO prima della chiusura: nessuna esclusione del profilo è applicata. Il nuovo ramo è su copie e root separato, senza alterare SHO approvata. P6 e l’estensione restano aperte fino all’accettazione operativa e al rilascio governato. L’approvazione delle risorse isolate e l’autorizzazione a elaborare HOO non costituiscono questa accettazione. Nessun pulsante di accettazione scientifica è stato premuto dall’assistente.

Ricevute grezze e screenshot restano privati; [evidenza pubblica minimizzata](evidence/BKL-049-PIAI-P6-ISOLATED-RESULTS-2026-10-07.json). La presente riconciliazione conserva propri gate CI, ARB, RQ, expected-head merge e post-merge/Pages. Rollback: revert della sola riconciliazione; ambiente isolato già sospeso, preservare evidenze e prenotazioni. Non ripristinare né riscrivere code o decisioni immutabili.
