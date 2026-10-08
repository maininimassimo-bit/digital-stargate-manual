# BKL-051 S4 â€” Prenotazione esplicita con intent conservato

Stato: Candidate; CI sul commit esatto, ARB, RQ e release pending.
Baseline: PR #516, merge `2ad11bf0551d89909d179df1b451464fff44f2c0`, release verificata.

## Contratto

Il chiamante locale fidato seleziona un job giÃ  QUEUED e un run nativo giÃ  preparato, con binding e manifest pinned. `ReservationIntent.prepare` verifica registro, input, parametri e algoritmo prima della rete; scrive intent e marker esclusivi. Le root di intent, registro e artefatti sono disgiunte. Nessuna credenziale viene caricata o salvata.

La POST worker `/v1/transient-analysis/worker/reserve` accetta soltanto workerId, rootId, jobId, bindingRef e reservationRef opachi. Richiede worker dedicato autenticato, root e binding corrispondenti, job QUEUED e nessun tentativo RESERVED/RUNNING/RECOVERY_REQUIRED. La mutazione CAS crea un tentativo e lease nuovi insieme all'intent server. Intent giÃ  presente restituisce RECONCILIATION_REQUIRED senza job o lease; identitÃ  diversa con lo stesso riferimento Ã¨ conflitto. Nessun rinnovo o adozione implicita. La scadenza materializza recovery secondo il contratto esistente.

L'intent server non compare nelle viste pubbliche o legacy. Il vecchio claim resta compatibile e puÃ² restituire una prenotazione esistente: il nuovo percorso sicuro non vi ricade. Questa aggiunta non riduce l'autoritÃ  della credenziale worker esistente e non costituisce attestazione contro un caller che usa direttamente l'API legacy.

Il client effettua una sola POST dopo aver conservato dispatch-intent. Valida schema chiuso, identitÃ , stato iniziale, tempi UTC e durata lease. Salva solo identitÃ  e digest; il lease resta in memoria. Risposta persa, alterata o salvataggio fallito congela il client in RECONCILIATION_REQUIRED e cancella il lease locale. Niente retry, reopen, adozione, nuovo tentativo o replay. File completi e parziali restano conservati; gli errori non vengono serializzati per evitare la persistenza di segreti.

`prepare_driver` verifica di nuovo byte e prenotazione, impone root disgiunte e runtime/catalog originariamente pinned, poi prepara il driver giÃ  rilasciato. Non avvia PixInsight: start resta esplicito. Un errore dopo la preparazione conserva journal/outbox e impedisce il riuso dell'intent. Il marker Ã¨ esclusivo per il run, non un lock globale contro copie o caller estranei. Nessuna ownership deriva da PID persistito.

## Verifica e limiti

Prove sintetiche con MemoryStore, HTTP loopback e processo mock: selezione, completamento mock, concorrenza, intent duplicato, risposta persa, identitÃ /schema alterati, scadenza, input cambiato, root sovrapposte e errori di persistenza dopo commit/preparazione. Nessuna prova nativa/cloud nÃ© nuova elaborazione astronomica. Verifica locale: 127 prove Python (126 PASS, un symlink skip Windows), 62 regressioni trasporto/worker PIAI PASS, 104 prove Node PASS; build MkDocs strict, fixture e generator/consistency PASS. Diciotto prove specifiche dell’intent PASS. I gate CI/review exact-head e di release restano pendenti e sono registrati nella PR; nessun PASS anticipato.

Non vengono attivati runtime, polling automatico, credenziali, IAM, risorse o invii. Recovery server, orchestration completa, workflow scientifico, calibrazione/uncertainty, validation, policy, OAT PC/cloud e reporting CBAT/TNS/VSX/MPC restano aperti. BKL-051 OPEN; P6 Accepted, F4 lifecycle pending, F5 dopo F4 e BKL-050 finale.

Rollback: revert dell'aggiunta e rigenerazione delle projection, conservando intent, marker, journal, outbox e History. Non cancellare evidenze nÃ© riusare run. Gate: CI â†’ ARB â†’ RQ â†’ merge sul commit atteso â†’ post-merge e Pages.
