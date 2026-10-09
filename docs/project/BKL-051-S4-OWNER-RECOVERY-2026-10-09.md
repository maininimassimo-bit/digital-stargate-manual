# BKL-051 S4 — Chiusura dichiarata della recovery

Stato: Released tramite PR #518, merge `0f5b2df4378cdec049468de92677f046c3d4979d`; 17 workflow exact-head e 17 post-merge SUCCESS, ARB/RQ APPROVED senza finding, sette endpoint pubblici verificati. Runtime disattivato.
Baseline: PR #517, merge `544fb860522918d0ffd00e8b172865abe647a8fa`, 17 gate exact-head e 17 post-merge SUCCESS, pubblicazione verificata.

## Decisione Owner

Il 9 ottobre l’Owner ha approvato la proposta concreta di chiusura dichiarata della recovery: «Approvo questa modalità». [Evento minimizzato](evidence/BKL-051-OWNER-RECOVERY-DECISION-2026-10-09.json). Questa approvazione autorizza la funzionalità; non attesta la quiescenza di un processo reale né attiva runtime, credenziali, IAM o nuovi invii.

## Contratto e conservazione

Dopo verifica sul PC del processo fermo e delle evidenze conservate, l’Owner invia una dichiarazione legata a jobId nella route e a decisionId, attemptId, rootId, bindingRef, SHA256 del dossier locale e quiescenceConfirmed true. Schema chiuso; il valore numerico 1 non equivale al booleano true. Solo Google Owner con origine autorizzata può usare POST `/v1/transient-analysis/jobs/TRN_…/close-recovery`; credenziali worker e route worker non concedono questa autorità.

Il server richiede RECOVERY_REQUIRED e identità esatta, registra request/recordedAt/authority OWNER_DECLARED nel medesimo stato CAS con backup immutabile. Decisione identica idempotente, diversa conflittuale; decisionId non può essere riusato su un altro job. Non legge il dossier né attesta il processo sul PC: hash e quiescenza sono dichiarazioni umane correlate. Il server non conserva percorso, coordinate, immagini, dossier completo o nuove credenziali.

Stato, attempt, lease, timestamps del tentativo, risultato e ultima ricevuta rimangono invariati. La closure è un’aggiunta immutabile, non riscrive il tentativo storico. Il job resta RECOVERY_REQUIRED, scientificamente NOT_VALIDATED e non diventa COMPLETED/CANCELLED. Solo il blocco di nuove prenotazioni è escluso dopo la dichiarazione valida. Il vecchio job non può essere riprenotato o rilanciato; i suoi report successivi sono rifiutati, anche un retry storico. Claim legacy può acquisire un diverso job QUEUED. Reserve con intent precedente continua a richiedere riconciliazione e non restituisce lease. Stato terminale incerto e ricevuta storica restano distinti.

Le viste Owner includono la closure. Le viste worker legacy e la receipt worker mantengono lo schema precedente. Nessun lease revocato viene ripristinato e nessuna ownership è ricostruita da PID.

## Percorso nel portale

La scheda RECOVERY_REQUIRED mostra tentativo e postazione opachi, campo SHA256 del dossier consultato e conferma esplicita del processo fermo/evidenze conservate. Il pulsante registra soltanto la dichiarazione: non termina PixInsight, non riprende il vecchio run e non crea automaticamente un nuovo job. La scheda distingue recovery chiusa su dichiarazione Owner e tentativo storico ancora incerto. Se la quiescenza non è verificabile, lasciare il blocco.

Il comando usa l’intent Owner persistito già governato: identità e dichiarazione immutabili, nessun segreto nello storage, refresh esplicito dopo risposta persa. Conferma solo dalla closure esatta; tentativo o dichiarazione diversi congelano la riconciliazione. Retry, quando ammesso, è soltanto esplicito della stessa dichiarazione, senza nuovo processo o job. Navigazione/disconnessione mantengono i confini precedenti.

## Verifica e residui

Tredici prove nuove Python coprono conservazione/idempotenza, tentativo vecchio rifiutato, nuovo job distinto, stato/identità/booleani invalidi, decisionId riusato, backup/CAS/concorrenza e ruoli HTTP. Sei prove Node nuove verificano dichiarazione esplicita, ACK perso senza seconda POST, identità cambiata, closure falsa su COMPLETED, dichiarazione conflittuale e ripristino senza invio automatico. Fixture deriva dalla coda Python reale sintetica, incluse le recovery chiuse. Nessuna prova nativa/cloud o nuova elaborazione scientifica: risultati e gate sul commit esatto nella PR.

RQ PR517 P3: il conteggio documentale della suite precedente è riconciliato a 127 prove, 126 PASS e uno skip Windows; il test aggiunto era già stato verificato separatamente. Nessun finding funzionale. Questo aggiornamento non promuove acceptance.

BKL-051 OPEN: caller operativo completo, IAM/credenziale/TLS/Google Owner e PC/cloud OAT reali, workflow scientifico, covarianze/calibrazione/passband, validation e soglie approvate, oggetti mobili, policy e reporting CBAT/TNS/VSX/MPC restano gate. Runtime e invii disattivati, P6 Accepted; F4/F5/BKL-050 e S10/Safety invariati.

Rollback: revert governato conservando closure, tentativi, intent, journal/outbox e History. Il vecchio codice ignora la closure per il blocco e torna conservativamente a bloccare nuove prenotazioni; non cancella dati. Arresto/rollback operativo non può essere dedotto dal revert. CI → ARB → RQ → merge sul commit atteso → post-merge e Pages.
