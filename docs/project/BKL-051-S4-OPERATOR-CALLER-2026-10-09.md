# BKL-051 S4 — Caller locale per un solo job selezionato

Stato: Released tramite PR #519, merge `19e78cf0197cc74e62d43260825c6ea196a43a2f`; 15 workflow exact-head e 15 post-merge SUCCESS, ARB/RQ APPROVED senza finding e sette endpoint Pages verificati. Runtime disattivato. I gate descritti nel seguito sono stati completati nel perimetro di codice e pubblicazione, senza OAT reale.
Baseline rilasciata: PR #518, merge `0f5b2df4378cdec049468de92677f046c3d4979d`, 17 gate exact-head e 17 post-merge SUCCESS, sette endpoint pubblici verificati. Recovery Owner disponibile come funzione, runtime disattivato.

## Contratto

`python -m tools.scientific_transients.operator_run` espone tre azioni distinte: `preflight`, `register-binding` e `run-selected`. Richiede `--plan` locale e `--plan-sha256` verificato indipendentemente. Solo `run-selected` accetta e richiede `--authorize-native-launch`; non implica autorizzazione operativa se il gate Owner non è stato approvato. Un job esatto già scelto dall’Owner, nessuna selezione automatica, daemon o acquisizione del prossimo job.

Piano chiuso `DSG_TRANSIENT_OPERATOR_PLAN_V1`: serviceOrigin HTTPS fidato e fisso del servizio esistente, workerId/rootId/jobId/reservationRef/operationRef opachi, binding chiuso e manifestSha256, paths artifacts/registry/run/intents/journals/outboxes e timeoutSeconds intero 1..900. jobId null consente soltanto preflight/registrazione. Tutte le cartelle devono essere assolute, già esistenti e prive di link secondo LocalRegistry; le root sono disgiunte, il run deve essere discendente di artifacts. Nessun codice remoto, parametro scientifico remoto, credenziale, URL arbitrario o schema esteso. Runtime PixInsight e librerie sono verificati dai componenti nativi rilasciati.

Preflight verifica byte e digest del piano, registro, input/parametri/algoritmo e run preparato non avviato. Non legge credenziali e non effettua rete/native. Registrazione è un comando esplicito del solo binding verificato: risposta esatta richiesta, nessuna prenotazione o elaborazione. Una risposta persa resta non confermata; nessun retry automatico.

Le azioni con rete leggono soltanto `DSG_TRANSIENT_OPERATOR_TOKEN` in memoria dopo il preflight. Nessun token nei parametri, file, output o journal, nessun fallback a Google/PIAI o ricerca di credenziali. Trasporto rilasciato: TLS verificato, origine fissa, no proxy/redirect, richieste/risposte bounded e nessun retry implicito. La credenziale dedicata e l’attivazione non vengono create da questo comando.

## Esecuzione e conservazione

Run esplicito crea ReservationIntent esclusivo e usa una sola POST reserve per il job selezionato. Una risposta perduta/conflittuale congela il percorso; nessun claim legacy, recupero di lease, secondo intento o replay. Il caller prepara LocalDriver, verifica nuovamente piano e run prima di start, conserva operator-start-intent legato al digest del piano e avvia una sola volta. Poll bounded ogni due secondi attraverso il driver/supervisore, entro il timeout scelto; nessun loop della coda.

Cancel remoto e timeout conservano le semantiche già revisionate: punto sicuro nativo, conservazione prima dell’eventuale chiusura dell’handle posseduto. Un timeout o un’interruzione non attestano l’arresto del processo. Errore/KeyboardInterrupt conserva operator-unconfirmed senza dettagli sensibili e senza ricostruzione dell’ownership da PID. Output del comando minimizzato; errore o recovery exit 2. Un esito COMPLETED rimane tecnico, WORKER_REPORTED_NOT_ATTESTED e scientificamente NOT_VALIDATED/NORMALIZED_SAMPLE_SUM.

Prima di un eventuale nuovo tentativo occorrono riconciliazione esplicita delle evidenze, verifica reale della quiescenza sul PC ed eventuale dichiarazione Owner della recovery. Il run precedente non si riutilizza. Conservare tutti i record, checkpoint, History e archivi genitori, inclusi i fallimenti parziali. Il comando non esporta automaticamente un report come scientificamente validato: resta disponibile l’esportatore con digest independently pinned.

## Verifica e gate residui

Quindici prove nuove con MemoryStore e processo mock coprono completamento, preflight offline, consenso esplicito, job assente, schema/origine/root/timeout, piano alterato prima/dopo reserve, risposta persa, doppia invocazione, timeout, interruzione, cancel prima/durante launch, registrazione difforme e failure del record finale dopo il risultato remoto conservato. Non sono OAT cloud/PC o nuove misure scientifiche. CI include queste prove; ricevute exact-head nella PR.

BKL-051 OPEN: caller è un collegamento operativo del kernel tecnico preparato, non una pipeline scientifica completa. Restano IAM/credenziale/Google Owner/TLS/CAS e PC/cloud OAT reali, WCS/covarianze indipendenti, matching/coverage/calibrazione/passband, validazione su eventi/controlli/iniezioni, soglie e policy Owner, oggetti mobili e reporting CBAT/TNS/VSX/MPC. Invii disattivati. P6/F4/F5/BKL-050/S10/Safety invariati.

Rollback governato del codice conservando piano/intent/journal/outbox/run; non arresta un processo già avviato e non rimuove evidenze. CI → ARB → RQ → merge expected-head → post-merge e Pages prima di qualsiasi proposta runtime.
