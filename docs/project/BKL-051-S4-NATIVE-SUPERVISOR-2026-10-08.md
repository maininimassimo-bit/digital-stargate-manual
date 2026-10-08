# BKL-051 S4 — Supervisore del processo nativo

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate same-session lifecycle; cloud/portal/science OAT incomplete |
| Baseline verificata | PR #511 merge `c537de154989241003071adb6c3895ac7bba12a3`: 16 CI, ARB/RQ, 15 workflow post-merge e sette HTTP/projection PASS |

## Avvio locale controllato

`native_supervisor.py` collega registry, journal, outbox e [produttore PJSR](BKL-051-S4-NATIVE-APERTURE-2026-10-08.md) per un solo tentativo della sessione corrente. Non acquisisce job, token o credenziali: il chiamante fidato fornisce gli oggetti preparati e il lease solo in memoria. Root outbox disgiunta da artifact/registry, binding/manifest pinned, input/parametri/library registrati, launcher/hash/runtime verificati prima dell'avvio. Nuova directory supervisor esclusiva; journal PREPARED, outbox fresca e stessa istanza journal richiesti. Un riavvio, directory parziale o tentativo precedente non ammette rilancio.

Prima dell'avvio conserva e conferma RUNNING e OPERATION_STARTED con letture worker dedicate, poi ricontrolla stato/cancel e byte locali. Registra launch-intent prima di creare il processo. Il backend usa soltanto l'eseguibile PixInsight installato, argomenti fissi, senza shell, nuova istanza/automation/no startup script o update, finestra nascosta su Windows. Nessun executable payload dal portale. Hash/versioni non sono firma o attestazione isolata; filesystem e installazione restano quiescenti e fidati, ACL Owner da collaudare. Include standard transitive non archiviate integralmente.

Il supervisore è una library con `start()` e `tick()` chiamati esplicitamente: niente daemon, analisi periodica, scheduler osservativo o heartbeat aggiuntivo. Il timeout 300 s, configurabile 1–900 s dal chiamante locale, è un limite operativo, non scientifico. Le ricevute RUNNING già previste dalla coda possono rinnovare il lease; le letture e i terminali cancel/recovery non lo rinnovano. Un processo uscito senza receipt rimane incerto fino al timeout; non è recuperato automaticamente.

## Annullamento e stati incerti

Cancel remoto prima dell'ultimo controllo evita l'avvio. Durante l'esecuzione una lettura autenticata con cancel, stato remoto terminale o errore di osservazione richiede un marker locale al punto sicuro. Non prova che PixInsight sia già fermo. Esiste una finestra tra ultimo controllo e avvio: cancel non è una transazione atomica distribuita; il polling successivo applica la richiesta. Manca ancora il driver operativo con frequenza di polling/OAT autenticata e recovery server.

La outbox ora consente, con cancelRequested, soltanto nuovi terminali CANCELLED o RECOVERY_REQUIRED con sequenza attesa; RUNNING/COMPLETED continuano a congelarsi. Identità, lease e ultimo ACK restano verificati; terminale remoto, conflitto o restart non sono bypassati. Una receipt pendente resta intatta senza secondo envelope/retry automatico. Dopo tutti gli ACK un nuovo terminale recovery può essere inviato una sola volta, senza rinnovo; esito remoto confermato e stato locale sono distinti.

Timeout, terminale mancante/invalido, marker in conflitto e checkpoint fallito non concedono terminazione del processo. Si conservano marker, ricevute e recovery, senza acquisire un altro job. L'handle del processo creato nella stessa sessione è l'unica proprietà utilizzabile per chiuderlo; un PID salvato non autorizza azioni dopo restart. Un errore di lancio/persistenza è ambiguo, non prova che nessun figlio sia nato. Nessun arresto di istanze Owner.

Una receipt nativa valida viene conservata prima della chiusura dell'istanza. Per COMPLETED si raccolgono checkpoint, parametri e quattro History, poi il journal produce il rapporto tecnico e gli ACK. Se l'Owner annulla dopo completamento nativo, checkpoint/History restano ma non si ammette un successo nella coda. Se cancel o consegna incerta arrivano dopo il rapporto locale COMPLETED, questo non viene riscritto: stato remoto/recovery e rapporto locale restano separati. La chiusura può usare terminate sull'handle corrente dopo attesa breve e conservazione; il codice di uscita del processo chiuso non sostituisce la receipt del kernel.

## Evidenze

18 nuovi test supervisore con processo mock e receipt sintetiche; due nuovi test outbox per terminali cancel/recovery. Suite locale Python: 88, 87 PASS e un symlink skip per privilegio Windows. I 65 test Node già verificati nella PR #511 sono invariati; CI Windows/Linux sul nuovo commit e review indipendenti restano gate, non anticipati. Fixture e mock non sono attestazioni di processo o cloud.

Prova componente reale in PixInsight: due aperture del controllo numerico genitore riutilizzato, cinque eventi journal, quattro ACK MemoryStore, checkpoint e quattro History; flusso massimo di errore `3.885780586188048e-16`, parent invariato. Questa prova usa la prima revisione del supervisore, congelata privatamente prima dell'ulteriore gestione del marker in conflitto; quella correzione ha test mock dedicato. Una seconda prova nativa con sorgenti finali pinned prima/dopo esegue l'annullamento prima di aprire l'immagine: zero chiamate kernel, quattro eventi, tre ACK, parent invariato e chiusura soltanto dell'handle creato. Checkpoint/History immagine non generati nel cancel pre-open; input/copiatore/provenienza conservati. Nessuna nuova epoca astronomica indipendente. Runtime e rami privati conservati separatamente, non un archivio autonomo completo.

Entrambe sono integrazioni locali MemoryStore, non servizi cloud o flusso UI. Failure/cancel/crash/timeout/lease perduto concorrenti nel runtime reale e filesystem/ACL/reparse restano OAT; finora le casistiche negative sono mock, tranne il cancel pre-open nativo. Non ripete elaborazioni P6 approvate, solves, detection o i precedenti collaudi.

## Gate residui e rollback

Workflow scientifico completo, report confrontabile, unità/calibrazione/variance/covariance/passband, precisione e dataset indipendenti/policy Owner. Driver operativo/recovery esplicita del server, UI/accessi/PC/cloud OAT, reporting CBAT/TNS/VSX/MPC e acceptance finale. Nessuna significatività, candidato o scoperta attestata. Coda/invii restano disabilitati; BKL-051 OPEN, S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6, F4/F5/BKL-050, gallery, root C→F, device/S10/Safety invariati.

Rollback via revert supervisor/preflight/cancel terminal/test/docs e rigenerazione projection, conservando ogni directory e receipt senza replay. Gate exact-head CI → ARB → RQ → expected-head merge → post-merge/Pages. [Ricevuta minimizzata](evidence/BKL-051-S4-NATIVE-SUPERVISOR-2026-10-08.json).
