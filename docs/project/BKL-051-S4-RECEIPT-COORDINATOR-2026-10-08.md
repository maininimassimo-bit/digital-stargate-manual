# BKL-051 S4 — Ricevute persistenti e riconciliazione

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-RECEIPT-COORDINATOR |
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate library/loopback transport, native producer and cloud OAT incomplete |
| Baseline verificata | PR #509 merge `b634c0d5f3be9cfd00334d7c13f2a16cf2f7fb9a`: 19 CI, ARB/RQ, 17 workflow post-merge e sette HTTP/projection PASS |

## Ricevuta prima dell'invio

`receipt_coordinator.py` aggiunge una library dedicata al [journal](BKL-051-S4-ATTEMPT-JOURNAL-2026-10-08.md). Root locale esistente e disgiunta dal journal, directory esclusiva per attempt, identità chiusa con cinque binding e manifest pinned. Prima di qualunque invio crea esclusivamente una ricevuta numerata con identity, hash head del journal e envelope senza lease. Scrittura flush/fsync, rilettura di schema/ordine/catena/head e ACK; fino a 128 messaggi come limite operativo. Una ricevuta pendente blocca la successiva; un terminale riconosciuto chiude la sequenza. Collisioni, directory parziali e copie precedenti si conservano, non si riscrivono.

La root outbox è scelta dal coordinatore locale fidato; non dal portale. Deve essere quiescente, sotto ACL Owner e distinta anche dagli originali/registry nel futuro runbook operativo. La library verifica separazione dal journal e link/reparse negli antenati, non attesta ACL, isolamento, transazione atomica o piena durabilità dopo perdita di alimentazione. Filesystem ostile e riscritture coordinate non sono esclusi. Niente firma o ancora esterna; parziali prima del receipt e recovery server sono gate futuri. Unico coordinatore fidato, niente daemon o auto-replay.

## Lettura dedicata e trasporto

La coda aggiunge `worker_receipt(jobId)`, esposta soltanto su GET `/v1/transient-analysis/worker/jobs/TRN_<id>` con credenziale worker scientifica distinta dalla PIAI. Risposta chiusa: job/attempt/root/binding, stato/cancel/sequence/result e ultima ricevuta senza lease; nessun review Owner, path, pixel, History o coordinate. La lettura applica la scadenza già prevista dalla coda: può registrare RECOVERY_REQUIRED, non rinnovare il lease. Un job non riservato non produce una receipt. Namespace e default-disabled del servizio invariati; non è un endpoint Owner pubblico e non aggiunge authority.

`TransientTransport` eredita dal trasporto PIAI la policy origin HTTPS Cloud Run, TLS, niente proxy o redirect; allowlist separata soltanto claim/register/worker-job/report. Richieste 16 KiB, risposte 64 KiB, timeout 30 s, nessun retry automatico. HTTP loopback ammesso soltanto con opzione esplicita di test. Un errore HTTP/rete ritorna delivery non confermata senza salvare body/token/log. Bearer e lease sono passati in memoria dal chiamante autorizzato; nessuna lettura/estrazione o nuova credenziale, provisioning, servizio cloud o deployment in questo incremento.

## ACK perso, riavvio e conflitti

L'invio rilegge artifact/journal attuali, legge la ricevuta dal server autenticato e confronta identità/attempt/root/binding, sequence, envelope completo e stato. Se è già accettata non esegue un secondo POST. Se non è accettata, nella stessa sessione consegna esattamente l'envelope persistito con il lease corrente in memoria, poi una nuova GET conferma tutti i byte della receipt. Il risultato del solo POST non costituisce ACK. La library `reconcile(remote)` usa dichiarazioni del chiamante; il percorso `deliver(transport, lease)` ottiene la lettura attraverso il trasporto. Una fixture MemoryStore non è attestazione cloud.

Una risposta persa dopo commit si riconcilia senza secondo POST. Perdita prima di commit consente ritentativo identico nella stessa sessione, senza rilancio nativo. Un restart permette solo la riconciliazione di una receipt già accettata; se non accettata o divergente registra RECONCILIATION_REQUIRED e non reinvia. Non riapre il journal attivo, non continua o avvia PixInsight e non trasforma il restart in heartbeat/estensione del lease. Cancel, scadenza, terminale divergente e sequence inattesa conservano insieme receipt locale e osservazione remota in un record di recovery esclusivo. ACK storico prova la ricevuta accettata al momento della lettura, non che un job sia tuttora attivo.

La library non risolve una recovery né ammette nuove ricevute su outbox congelata. Manca ancora il coordinatore operativo per punto nativo sicuro, cancel concorrente, crash a metà copia/invio/ACK, lease perso, recovery esplicita del server e passaggio al job successivo. Un COMPLETED locale rifiutato non viene riscritto: terminale computazionale e stato remoto restano separati. Nessuna promessa exactly-once o transazione distribuita. Completa il protocollo di receipt candidato, non il worker scientifico.

## Verifiche e gate residui

17 nuovi test: receipt/ACK privi di segreti, risposta persa prima/dopo commit, riavvio accepted/unaccepted, cancel/scadenza, identità/secret extra, conflitto remoto, ordine/terminale, journal avanzato/head alterato, parametri/checkpoint mutati, directory parziale e ACK alterato. Test HTTP reali loopback verificano GET worker dedicata, delivery e credenziale PIAI negata; fixture journal/runtime/History sintetiche e dichiarate. Totale suite transient locale 60 (59 PASS, un symlink fixture skipped per privilegio Windows); 36 regressioni PIAI PASS. CI Windows/Linux e review sul commit esatto restano gate della PR, non anticipati. 55 test Node scientifici invariati.

Nessun processo nativo o query scientifica nuova; originali/archivi/P6 invariati. Rapporto tecnico NOT_VALIDATED, non misure scientifiche, detection o scoperta. Produttore nativo, rapporto scientifico completo, UI e OAT cloud/PC, full variance/covariance/passband/rates, criteri operativi Owner e reporting CBAT/TNS/VSX/MPC restano necessari. Coda e invii disabilitati. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata; BKL-051 OPEN. F4 lifecycle, F5 dopo F4, BKL-050 conclusiva, S10/device/Safety invariati.

Rollback: revert library/worker GET/docs e rigenerare projection; conservare ogni snapshot, receipt, ACK e recovery privato, senza replay o cancellazione. Gate exact-head CI → ARB → RQ → expected-head merge → 17 workflow applicabili e Pages. [Ricevuta minimizzata](evidence/BKL-051-S4-RECEIPT-COORDINATOR-2026-10-08.json).
