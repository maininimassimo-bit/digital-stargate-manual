# BKL-051 S4 — Snapshot e journal per tentativo

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-ATTEMPT-JOURNAL |
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Local library and MemoryStore bridge candidate; native producer/HTTP/OAT incomplete |
| Baseline | PR #508 merge `a0950bcad358f9e5de52e4071bb3bed6e5e2525a`, 15 workflow post-merge e sette HTTP/projection PASS |

## Dal registro al tentativo

Il [registro locale](BKL-051-S4-LOCAL-EVIDENCE-REGISTRY-2026-10-08.md) verificava byte quiescenti al momento della lettura, senza snapshot per il lavoro successivo. `attempt_journal.py` copia tutti gli artifact registrati in una nuova directory per attempt, verificando i digest del manifest pinned e dei file copiati. Root artifact/registro/journal esistenti e disgiunte, niente traversal/link/reparse. Copie e manifest/eventi sono creati esclusivamente, con flush/fsync; errori/parziali conservati, directory esistente blocca una nuova preparazione. Non è garanzia completa di transazione o durabilità in caso di perdita di alimentazione.

Identità chiusa: job TRN, attempt, root, cinque bindingRef e digest del manifest. Lease/bearer non sono accettati nel journal. Sono riferimenti dichiarati del chiamante locale: la library non autentica una risposta server o attesta la corrispondenza di rootId al dispositivo. Verifica i byte degli artifact elencati, non tutta l'acquisizione/History esterna, l'autore o l'approvazione scientifica. File non elencati e archivi genitore restano dipendenze esplicite. Questo snapshot è di byte sotto controllo Owner: non è un ambiente isolato, un archivio autonomo completo o protezione contro processi locali ostili.

## Eventi e checkpoint

PREPARED → RUNNING → OPERATION_STARTED → CHECKPOINT, poi ulteriori operazioni/checkpoint oppure COMPLETED. Per ogni operazione il chiamante fornisce riferimenti a parametri e runtime, copiati prima della ricevuta OPERATION_STARTED. CHECKPOINT richiede stesso processRef e stessi byte dei parametri, oltre alle copie di risultato e History. processRef non può essere riusato nel tentativo. Il contenuto nativo dei file e la reale esecuzione non sono interpretati/attestati: i test usano receipt sintetici dichiarati tali, senza PixInsight. L'adapter dovrà integrare hook/receipt reali e validare versioni, target, processi, maschere e History prima di rivendicare un journal nativo operativo.

Eventi sequenziali esclusivi, schema chiuso e catena SHA256 dal manifest anchor, massimo 128 eventi (limite operativo). UTC host di registrazione non è l'epoca astronomica di acquisizione o la durata attestata di un processo. Ordine, schema e catena vengono riletti a ogni passaggio; corruzione e rimozione di eventi intermedi rifiutate. Non esiste firma/ancora esterna: riscrittura coordinata del journal o rimozione di un intero suffisso finale da un attore locale non sono escluse. Accesso quiescente e singolo coordinatore fidato sono prerequisiti; una collisione esclusiva non viene risolta con replay.

Riaprire un tentativo attivo non rilancia/continua un'operazione: consente soltanto il percorso esplicito RECOVERY_REQUIRED. Nessun processo, reset di lease o sblocco remoto automatico. FAILED/CANCELLED/RECOVERY_REQUIRED sono terminali immutabili e dichiarati dal chiamante; CANCELLED non prova da solo che PixInsight sia fermo. Il futuro adapter deve attendere il punto nativo sicuro, preservare checkpoint e riconciliare il server. Parziali prima dell'anchor e copie orfane restano disponibili per recovery manuale; non sono current head.

## Rapporto tecnico e bridge

COMPLETED richiede almeno un checkpoint e rivalida snapshot, parametri/runtime/checkpoint/History copiati. Il rapporto tecnico locale è creato esclusivamente e lega identità, head del journal e tre conteggi chiusi dichiarati dal chiamante. È `CALLER_REPORTED_NOT_ATTESTED` e `NOT_VALIDATED`: non è ancora il rapporto scientifico completo con misure individuali, limiti ed esportazione Owner. Ritoccare rapporto o artifact dopo sealing impedisce una receipt COMPLETED. Failure/recovery receipt senza risultato possono essere prodotte anche con artifact danneggiati; non li promuovono a validi.

`queue_receipt(sequence)` restituisce soltanto attempt, sequence, stage e, per COMPLETED, digest del rapporto, bindingRef e conteggi. Non manda rete e non include lease, path, immagini, coordinate o History. Il chiamante passa il lease vivo separatamente al transport già esistente. Bridge provato con la [coda MemoryStore](BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md): RUNNING, checkpoint/heartbeat, COMPLETED correlato; cancel rifiuta un nuovo RUNNING e ammette receipt CANCELLED. MemoryStore non è cloud/OAT. Sequence remota, outbox/ACK/risposta persa, lease expiry, autenticità claim, snapshot delle versioni native e recovery server restano responsabilità del futuro coordinatore/adapter. Un terminale computazionale locale non viene riscritto se il server rifiuta l'invio: futura riconciliazione deve conservare entrambi gli esiti, senza reinvio cieco.

## Correzione circoscritta del diniego HTTP

Ricorrenti errori Windows10053 si presentavano nelle richieste POST negate prima della lettura del corpo. Il comportamento è coerente con il reset TCP da chiusura con byte non letti descritto in [RFC 9112 §9.6](https://www.rfc-editor.org/rfc/rfc9112.html#section-9.6). Dopo il 403 il handler chiude la scrittura e scarta raw byte per massimo 64 KiB / 250 ms, senza parsing, dispatch, mutazioni, logging o nuova autenticazione. Diniego e separazione Owner/worker invariati; oltre i limiti la connessione viene comunque chiusa, senza promettere la consegna di qualsiasi payload ostile. È gestione del teardown, non consenso. Nessun deployment del servizio esistente da questo incremento.

## Validazione e residui

Sedici test journal con file/copie reali e receipt sintetici: snapshot, identità, parziali, ordine/catena, parametri, processRef, report/dati alterati, terminali, restart/recovery, envelope MemoryStore e cancel. Un nuovo controllo esegue 30 POST negati consecutivi e verifica 403/stato invariato. Suite Python transient: 43 locali, 42 PASS/un symlink fixture skipped per privilegio Windows, già dichiarato; 36 regressioni PIAI transport PASS. 55 test Node precedenti invariati. I nuovi workflow applicabili includono anche PixInsight local pilot e BKL-045 F3 perché cambia il handler condiviso. CI/review/post-merge esiti nella PR, mai anticipati.

Snapshot e journal sono candidati di library: non worker nativo, daemon, modulo Owner/UI o nuove analisi. Nessuna ripetizione di immagini, astrometria, detection, aperture o unit transfer. [Budget parziali](BKL-051-S4-LOCAL-EVIDENCE-REGISTRY-2026-10-08.md) e covarianze/Poisson/PSF/banda/rates restano aperti. Coda/invii disabilitati; nessun secret/IAM/account/servizio o gallery modificato. [Ricevuta minimizzata](evidence/BKL-051-S4-ATTEMPT-JOURNAL-2026-10-08.json).

Gate: exact-head CI → ARB → RQ → expected-head merge → post-merge/Pages. Rollback: revert code/docs e rigenerare projection, mantenendo journal/snapshot/receipt privati; non cancellare copie, rigenerare report sullo stesso attempt o riattivare vecchi binding. Seguono native producer e coordinatore HTTP/outbox, rapporto scientifico completo, UI e OAT, validation S2/S3 e reporting approvato. Acceptance finale e policy/soglie Owner ancora necessarie. P6/F4/F5/BKL-050/S10/Safety invariati; BKL-051 resta aperta.
