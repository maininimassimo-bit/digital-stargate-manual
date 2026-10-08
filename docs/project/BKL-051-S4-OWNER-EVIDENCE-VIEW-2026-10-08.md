# BKL-051 S4 — Consultazione privata delle evidenze

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate read-only portal view; deployment, authenticated cloud OAT and science acceptance pending |
| Baseline verificata | PR #512 merge `1e0a476b93329a9479db2b2c282005d14ac5f768`: 16 exact-commit checks, ARB/RQ, 15 post-merge e sette HTTP/projection PASS |

## Esperienza disponibile nel candidato

La nuova pagina [Analisi scientifiche private](../scientific-transient-analysis/index.md) prepara la consultazione Owner
del namespace già approvato nella [coda privata](BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md). Il servizio dedicato resta
disabilitato; il testo della pagina lo dichiara prima dell'accesso. La disponibilità della pagina dopo Pages non equivale
ad attivazione del servizio o completamento S4.

L'Owner può avviare Google sign-in con lo stesso client pubblico del pilota, leggere manualmente lo stato e terminare
l'accesso. Il token esiste solo in memoria; niente local/session storage o URL con credenziali. Nessuna lettura privata
prima dell'azione Owner; una lettura GET dopo il sign-in, poi soltanto il pulsante Aggiorna stato. Nessun polling,
heartbeat, claim, POST, avvio nativo, query a cataloghi o invio esterno. La lettura server può persistere una lease
scaduta come recovery secondo il contratto preesistente: la vista non rinnova né risolve il tentativo.

La vista mostra stato del servizio e suo updatedAt, riferimenti opachi del gruppo/input/riferimento/algoritmo/contratto,
conteggi riportati e digest del rapporto locale quando COMPLETED, valutazioni Owner già registrate e loro data.
COMPLETED è soltanto completamento tecnico comunicato dal PC. Cancel pendente non prova arresto; recovery mantiene
lo stato incerto e rimanda alla verifica sul PC. Nessun indicatore di presenza/connessione PC viene dedotto dal timestamp.
NOT_VALIDATED, WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e NONE restano distinti.

Il download conserva un `BKL051_OWNER_STATUS_SNAPSHOT_V1` con la vista minimizzata già validata, fonte
AUTHENTICATED_SERVICE_VIEW e localBytesVerified=false. Non scarica il rapporto completo, non verifica il suo hash
sul disco e non contiene immagine, coordinate, misure individuali, maschere, History, path o lease. Nessuna nuova
route o modifica al contratto server. Il digest identifica soltanto il rapporto dichiarato; non dimostra il suo contenuto.

## Confini del consumer

GET su origine HTTPS Cloud Run fissa, redirect vietati, credentials omit, cache no-store e timeout operativo 30 s.
Risposta JSON/UTF-8 limitata a 1 MiB anche durante la lettura streaming; nessun fallback a HTML o endpoint alternativo.
Schema chiuso della vista dedicata, correlazioni TRN/request/binding/report/review, capacità 32 job/review, sequenze
e vocabolari verificati prima di mostrare o esportare. Campi non ammessi, inclusa leaseToken, provocano rifiuto dell'intera
risposta. Questo controllo riguarda struttura e correlazione del JSON ricevuto dal servizio fidato: non attesta il PC,
metadati scientifici o indipendenza e non è un parser raw con rilevamento delle chiavi JSON duplicate.

404 significa servizio non attivato/route non disponibile, mai zero candidati. 401/403 cancellano token e schede;
errore, risposta invalida o nuova lettura cancellano la vecchia vista, senza mostrarla come corrente. Errori remoti
non vengono riflessi nella UI. Disconnect e Instant Navigation abortiscono la richiesta, cancellano schede/token,
revocano i blob del download e invalidano callback/risposte tardive mediante identità di sessione. Inizializzazione
idempotente; nessuna attività sulle altre pagine. Rendering textContent, controlli nativi, status live, focus e design token.

## Verifiche e limiti

22 test browser componente con DOM/fetch/sign-in simulati: completamento incompleto, cancel/recovery, review bound,
download minimizzato, 404/403/503, limiti, media/UTF-8, payload ostili, disconnessione e navigazione concorrenti.
Una fixture riproducibile prodotta dal vero TransientQueue/MemoryStore espone otto viste Owner dei lifecycle, con
attemptId normalizzato e nessuna leaseToken; il check Python verifica il drift e il browser consuma ciascuna vista.
Sono prove sintetiche di contratto, non login Google reale, servizio cloud o dati astronomici.

Controllo visivo locale della pagina senza login: tema chiaro/scuro, desktop e viewport tablet 768×1024,
focus/tastiera, refresh diretto, passaggio PixInsight e ritorno via navigazione, console senza errori/warning osservati.
Le schede private e il download sono verificati nei test componente, non nella UI autenticata reale: quest'ultima resta
OAT dopo attivazione autorizzata. Non è stato estratto un token o riutilizzata una credenziale Owner.

La CI esegue il check della fixture e la nuova suite su Windows/Linux insieme alle suite transients. La regressione
P5 esistente è verificata localmente. Build MkDocs strict, generator/projection e gate exact-head → ARB → RQ → merge
protetto → post-merge/Pages rimangono obbligatori e si registrano nella PR; non sono anticipati da questa nota.

## Residui e rollback

Questa consegna copre soltanto consultazione/download della ricevuta. Selezione e creazione richieste, annullamento
Owner e nuova decisione Owner nella UI, rapporto locale completo/esportazione, driver e recovery operativa, collaudi
autenticati e scientifici, policy quantitative e reporting CBAT/TNS/VSX/MPC restano da realizzare o validare.
S4 non completa, BKL-051 OPEN e S5 non accettata. Nessun nuovo master elaborato o collaudo P6 ripetuto.

Rollback: revert pagina/script/stile/nav/test/documenti e rigenerare projection. Non cancellare job, registri, rapporti,
originali, History/checkpoint o archivi privati. Nessuna modifica di cloud, credenziali/IAM, gallery, root C→F, apparati,
F4/F5/BKL-050 o Safety. [Ricevuta minimizzata](evidence/BKL-051-S4-OWNER-EVIDENCE-VIEW-2026-10-08.json).
