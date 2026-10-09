# BKL-051 S4 — build verificata, OAT preparato

Stato: riconciliazione candidata ai gate di rilascio. BKL-051 OPEN. Le due build circoscritte sono state autorizzate separatamente dall’Owner; l’attivazione è una decisione diversa, ancora pendente in questa fotografia dello stato.

## Rilascio e immagine

PR #520 integrata su `bb68404e836c532986453c682846105e7fb5ce3a`: 15 workflow exact-head e 15 post-merge SUCCESS, ARB poi RQ APPROVED zero finding sullo stesso `e2c888aea80f38e5cb157c2bb7523d2c0e7e0c67`, sette endpoint effettivi verificati. Il dossier resta solo DRAFT. Nessun invio o authority scientifica.

Contesto della build: merge #519 `19e78cf0197cc74e62d43260825c6ea196a43a2f`, 138 file tracciati e 1.402.880 byte; allowlist verificata contro tutti i blob Git. Archivio tar SHA256 `1541bbf3a695e4da99d971450ec21fc9188affa7092117860177989f762eb7ff`. Il contesto iniziale con percorsi appiattiti è scartato e conservato, mai costruito. Il client ha respinto uncompressed .tar prima dell’invio; il contenitore gzip successivo è stato verificato byte-identico nel payload, senza modificare sorgenti.

Prima build `0f543a84-47d9-45f8-9f96-d545574ce99c`: FAILURE, 154 prove PASS e un errore di fixture. Il Dockerfile colloca app.py in /app/app.py; una prova cerca /app/infrastructure/pixinsight-pilot/app.py. Nessuna immagine registrata da quel tentativo. Esito, log, provenienza e dipendenze conservati, senza retry automatico.

Seconda build `1eacfa73-ac3c-48d9-914d-a6a326a7d7f6`, esplicitamente autorizzata: SUCCESS, tutte le 155 prove passano con network=none e senza credenziali nel contenitore. La ricetta monta in sola lettura la medesima app tracciata nel percorso richiesto dalla prova. Nessuna prova rimossa e nessun cambiamento di Dockerfile/app/requirements/strumenti. Oggetto sorgente esistente e generation pinned nella richiesta; SHA256 confrontato con provenienza remota. Tag distinto registrato solo dopo successo.

Digest immutabile verificato sia nella risposta Cloud Build sia in Artifact Registry:

`sha256:6fc584d445e00dad93490dcf249dfef111db0bdeceda7022543a61007236db24`

Immagine `europe-west1-docker.pkg.dev/digital-stargate-telemetry/pixinsight-pilot/worker-broker` del merge #519. L’incremento #520 è un esportatore locale senza endpoint cloud e non è incluso in questa immagine. La verifica registry non attesta un livello SLSA: API indica unknown. Base e versioni effettivamente risolte conservate in archivio privato; requirements e base tag esistenti restano floating e non diventano riproducibili soltanto grazie al digest finale.

## Runtime e proposta concreta

Lettura reale successiva: servizio ancora sulla revisione P6 `dsg-pixinsight-pilot-p6-f2afb30f`, traffico 100%, immagine precedente; nessun deploy, IAM o bearer nuovo durante le build. Stessi servizi/bucket/API già esistenti; ciascuna build timeout 900s, possibili consumi cloud dichiarati. Nessuna nuova fotografia o dossier caricato nel contesto.

Run tecnico locale nuovo già preparato con fixture sintetica 64×64, due posizioni di controllo, copia esclusiva e archivi genitori conservati. Registrazione locale/hashing e preflight del caller PASS; jobId null impedisce avvio fino alla scelta esatta. Nessun lancio, registrazione cloud o replay di un tentativo completato. Non è una misura fotografica Owner né una prova di scoperta.

Proposta privata concreta di OAT: digest esatto, identità worker distinta, bearer dedicato in memoria, grant objectUser soltanto sull’oggetto nuovo di stato, stessa infrastruttura con max1/CPU1/512Mi/concurrency1, massimo 60 minuti/cinque tentativi tecnici, ciascun avvio massimo 120s. Decisione specifica necessaria secondo mandato §5. Non pubblicare le identità/percorsi/calibrazioni/credenziali del piano privato nel portale. Google Owner e quiescenza reale non possono essere simulati.

Rollback proposto: disabilitare namespace/revocare digest, ripristinare traffico P6, rimuovere solo nuovo grant condizionale, conservare stato/backup/journal/outbox/History/checkpoint. Non inferire fermata di un processo e non chiudere PixInsight dell’Owner. C→F junction invariato.

## Residui

Build/test non sono OAT PC/cloud, né accettazione scientifica. S4 resta incompleta; S2/S3 full workflow, WCS/covarianze/matching, rumore/calibrazione/passband, blind validation/false positives/completeness, policy quantitativa, moving objects, adattatori provider/sandbox e accettazione finale rimangono aperti. Nessun invio attivato, P6/F4/F5/BKL-050 e S10/Safety invariati.
