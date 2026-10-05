# P4 — Attivazione cloud e prove operative

| Campo | Valore |
|---|---|
| Versione | 1.1 |
| Data | 2026-10-05 |
| Stato | Owner-approved deployment; bounded live/native OAT; operational acceptance open |
| Modalità IA | SESSION_ASSISTED; zero nuove chiamate API IA |

## Autorizzazione e risorse

L’Owner ha approvato la proposta concreta e la credenziale dedicata dopo la consegna del candidato [PR #482](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/482). L’approvazione è soddisfatta e non deve essere richiesta nuovamente. La nuova infrastruttura può avere costi di esecuzione, storage, operazioni, build/registry ed egress; non esiste un limite di spesa rigido. Nessun polling continuo o provider IA a pagamento è attivato.

Creati soltanto servizio `dsg-pixinsight-pilot`, identità omonima, registry `pixinsight-pilot` e due bucket `dsg-piai-private-183451329061` / `dsg-piai-backup-183451329061`, progetto `digital-stargate-telemetry`, regione europe-west1. Cloud Run: 1 CPU, 512 MiB, min=0/max=1, concurrency=1, timeout 60 s, billing per richiesta. Bucket: prevenzione accesso pubblico enforced, accesso uniforme, versioning; nessuna regola di cancellazione automatica. La soft-delete predefinita del provider riguarda oggetti eventualmente eliminati, non introduce scadenza dei job o delle pubblicazioni.

Gli amministratori di progetto restano una boundary fidata. Runtime: creator/viewer sul primario e objectUser condizionato esclusivamente a `control/piai-state.json`; creator/viewer sul backup senza overwrite/delete. Nessun nuovo ruolo a livello progetto o accesso agli archivi fotografici. Servizio HTTP raggiungibile, tutte le route operative autenticate nell’applicazione; `/health` pubblico non contiene dati privati.

## Build e collegamento reale

Build `86d1d49e-0156-4263-8244-8206f688491f` SUCCESS: context allowlisted dal head revisionato `875cc375a130268b4be98b28ad11a7c8c11e4552`, senza foto/credenziali; build, push e test Python nel container riusciti. Digest distribuito `sha256:14a8ceb98989fe2e69b217b4ccf034cbfd63346401af506a3599cc44ffd65f66`, revisione iniziale `dsg-pixinsight-pilot-00001-bmw`; riavvio reale sulla stessa immagine in `dsg-pixinsight-pilot-p4-oat-restart-01`, 100% traffico verificato.

Credenziale casuale 256 bit generata privatamente. Copia PC cifrata con Windows User DPAPI e ACL Owner/SYSTEM; il server riceve solo SHA256. Un wrapper privato la decifra soltanto per la durata del processo e passa `DSG_PIAI_WORKER_TOKEN`; nessun token nei comandi, log, repository o pagina. Cartella worker dedicata, identità opaca persistente fissata dalla prima claim; la registry scientifica inizialmente vuota contiene ora solo due fixture private approvate con hash dei quattro master verificati. Non copiare identità/binding in una nuova cartella e non riutilizzare il vecchio root P3.

Dieci prove HTTPS sul servizio reale PASS: health/zero provider, anonimato Owner/worker negato, worker errato negato, worker con Origin browser negato, separazione route Owner/worker, Origin estraneo negato, worker corretto IDLE, root alternativo rifiutato e identità originale conservata. Queste prove non attestano login Google Owner o esecuzione scientifica.

## Storage OAT reale

Con identità runtime impersonata temporaneamente dall’Owner: backup dello stato effettivamente commesso letto e confrontato per SHA256, ripristinato in namespace separato e riletto identico. Overwrite del backup, cancellazione backup e overwrite fuori dal controllo primario rifiutati per IAM. Nessun rollback della coda attiva. Il permesso di impersonazione temporaneo è stato rimosso anche nei tentativi falliti; due tentativi iniziali hanno incontrato propagazione IAM, successivo tentativo PASS. La ricevuta pubblica è [minimizzata](evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json); log, hash di stato e percorsi PC rimangono privati.

CAS stale-create reale negato 412 senza mutazione; CAS concorrente GCS è ora verificato tramite CLI amministrativa; concorrenza delle route HTTP Owner soltanto sintetica. Restart e perdita deliberata della risposta dopo commit remoto sono ora provati nel cloud reale come descritto sotto. Il restore dimostra recupero bytes del preciso stato commesso; non garantisce un restore automatico o indipendente da amministratori fidati.

## Accesso Owner verificato e procedura diagnostica

La [pagina diagnostica P4](../pixinsight-pilot-check/index.md) è esclusa dalla navigazione principale e non è il comando di elaborazione P5. L’operatore inserisce il servizio approvato; prima di caricare Google GSI il digest dell’origine deve coincidere con quello fissato nel codice. Niente proxy, redirect o invio a una destinazione alternativa. Il token rimane nella memoria della pagina; non viene letto dalla chat né riutilizzato dall’archivio fotografico.

Accedere normalmente con l’account Owner e premere **Verifica accesso e annulla la prova**. La pagina crea una richiesta sintetica opaca, ripete identicamente la creazione, annulla e legge `CANCELLED`/`publication=NONE`. Non invocare il worker durante questa prova: il riferimento sintetico non è una sorgente scientifica registrata. Ripetere la stessa operazione nella stessa pagina dopo una perdita di risposta; nessuna credenziale o richiesta viene salvata nel browser. In caso di pagina chiusa dopo create, ispezionare la coda privata come amministratore prima di altre prove; non attivare il worker su un riferimento sconosciuto.

La pagina introduce solo il percorso necessario al login/OAT; nessun endpoint preimpostato pubblico o comando scientifico di produzione. Le credenziali Google e del worker restano distinte. L’autenticazione Owner è ora **PASS**: osservati Google callback e risultato reale della prova create/duplicate/cancel/status, terminata CANCELLED/NONE. Token non estratto dalla pagina. Login interattivo e autenticazione aggiuntiva restano all’utente.

## Gate residui e recupero

Login Owner e non-Owner valido negato, CAS stale-create, restart/lost-ack e OAT nativo circoscritto sono ora verificati. GCS concorrente reale verificato tramite CLI amministrativa con bytes invariati; restano concorrenza HTTP Owner soltanto sintetica e acceptance operativa più ampia. I riferimenti scientifici restano privati; il supervisore avvia `run.js` e conferma l’arresto prima di `--native-stopped`. Nessun retry del runtime già avviato o auto-replay. P5 sessioni/preview/provenance e P6 acceptance/recupero restano successivi. M27 pubblicata invariata.

Conservare root, binding, pending/ack, journal, originali e due bucket. Nessuna scadenza, riassegnazione offline, ripartenza o sblocco forzato. Ambiguità: interrompere nuove invocazioni e verificare la ricevuta; `RECOVERY_REQUIRED` conserva la prenotazione. Rollback: fermare il worker, revocare credenziale/digest e accesso invoker del servizio, conservare risorse/evidenza, revert codice tramite PR. Non eliminare archivi o ripristinare una precedente pubblicazione.

## Evidenza corrente — trasporto nativo circoscritto

Autenticazione Google Owner reale PASS sulla pagina diagnostica: creazione sintetica, ripetizione idempotente, annullamento e lettura CANCELLED/NONE. Google valido non-Owner negato e stale-create CAS reale negato senza mutazione. Riavvio del servizio sullo stesso digest e perdita deliberata dell’ack PREPARING dopo commit remoto: stessa richiesta recuperata, una preparazione; ciclo ripetuto con otto file identici.

Trasporto nativo sul PC verificato con due fixture amministrative isolate: pre-cancel con zero processi/output; M27 non lineare COMPLETED con 29 azioni, 15 checkpoint e 29 istanze workflow, originali invariati, finale Float32 RGB 4634×2808 e tutti i pixel finiti in [0,1]. Clipping misurato, non certificato assente. Raccolta dopo arresto PixInsight, prenotazioni chiuse e report remoto verificato. Questa prova usa Broker/BackedUpStore tramite CLI Owner amministrativa: non attesta ancora la creazione di un job scientifico dal comando HTTP/UI Owner. La prova HTTP Owner separata è sintetica; executionEvidence resta WORKER_REPORTED_NOT_ATTESTED, publication=NONE.

P4 ha ora una prova tecnica nativa circoscritta; CAS GCS concorrente reale PASS tramite CLI Owner amministrativa: due scritture degli stessi bytes di coda terminale, una accettata e una rifiutata per generazione obsoleta, backup verificato e stato logico invariato. Concorrenza sulle route Owner HTTP soltanto sintetica; acceptance operativa più ampia resta aperta. P5 comando scientifico/sessioni/preview/provenance, P6 e acceptance scientifica Owner sono successivi. SESSION_ASSISTED, zero nuove chiamate API IA; M27 pubblicata e autorità dispositivi/Safety invariate. Evidenza privata conservata; ricevuta pubblica minimizzata e runbook collegati sopra. CI/review/merge e Pages di questa riconciliazione sono da verificare sulla PR di consegna.

Osservazione reale dopo oltre 120 secondi senza contatto: OFFLINE diagnostico, stesso job/root ancora RUNNING, nessuna scadenza o riassegnazione osservata. Non è una prova di crash recovery del desktop.

Derivati locali TIFF RGB16/JPEG sRGB verificati; soluzione astrometrica conservata e checkpoint invariato dopo export. History disponibile: 13 viste, 47 passi, 82 istanze, 429679 byte; importer 1.2 PARSED_SUBSET. La History conservata non prova completezza a monte: executionEvidence=NOT_ESTABLISHED e workflowCompleteness=UNAVAILABLE del file importato restano invariati. Journal e correlazioni runtime delle 29 azioni conservati separatamente. Campo intero/dettaglio coerenti con la ricetta P3; nessuna superiorità scientifica o sostituzione pubblica dichiarata.

Il riavvio reale usa la stessa immagine distribuita: il client ha deliberatamente scartato una risposta PREPARING già commessa, senza creare copie prima dell’ack. Dopo il riavvio ha recuperato lo stesso job, confermato una sola PREPARING e preparato una sola volta. Una seconda invocazione conserva identici gli otto file preparati. Questo scenario controllato non attesta un’interruzione di rete casuale né un crash del PC/PixInsight durante un processo. Conservare root e binding: nessun job scade o viene riassegnato automaticamente.
