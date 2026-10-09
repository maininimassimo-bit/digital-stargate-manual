# BKL-051 — concorrenza della coda e backup su GCS

BKL-051 resta **OPEN**, scienza **NOT_VALIDATED**. PR #526 precedente rilasciata sul merge `78dad45ec4241b9b3b6de2f7a863a931cf80217b`: 15 workflow post-merge SUCCESS e sette endpoint Pages verificati. Questo incremento documentale è candidato ai gate del proprio commit; le ricevute precedenti non lo attestano.

## Prova reale del nucleo coda/storage

L'Owner ha autorizzato una sola esecuzione con massimo 20 minuti e 150 richieste HTTP GCS, poi una sola seconda esecuzione corretta. La prima si è fermata alla costruzione di una classe astratta di credenziale, dopo l'estrazione del token in memoria ma prima di qualsiasi richiesta allo storage. Errore, script e autorizzazione conservati. La correzione usa la classe concreta OAuth2, verificata localmente con token sintetico e senza rete; non cambia il codice di produzione o i criteri di PASS.

La seconda esecuzione è **PASS**, durata 4,672 secondi, **43 richieste HTTP**, inclusi **due HTTP 412 reali**. Due istanze locali del codice effettivo `TransientQueue`, `BackedUpStore` e `GCSStore` operano in un nuovo namespace diagnostico nei due bucket privati esistenti. Prima lettura sincronizzata in ciascuna fase; conflitti di generazione risolti tramite il retry della coda.

| Controllo | Evidenza osservata | Esito |
|---|---|---|
| Registrazione simultanea | Due scritture con generazione iniziale 0; una respinta, rilettura e nuova scrittura; entrambi i binding conservati | PASS |
| Creazione simultanea | Due scritture sulla stessa generazione; una respinta, rilettura e nuova scrittura; entrambi i job conservati | PASS |
| Idempotenza | Ripetizione delle due richieste create restituisce i medesimi job, senza ulteriori scritture primarie | PASS |
| Backup sotto conflitto | Sei payload distinti: quattro scritture confermate e due respinte; ogni copia nel bucket di backup verificata tramite SHA-256 | PASS |
| Head finale | Generazione e payload finale invariati dopo letture e verifica dei backup | PASS |

I due job diagnostici restano QUEUED, fuori dallo stato operativo e dal portale: nessuna prenotazione o esecuzione nativa. Nessuna lettura/scrittura del control object produttivo, attivazione Cloud Run, build, modifica IAM/traffico, fotografia o segnalazione esterna. Sessione HTTP chiusa e riferimento al token azzerato; nessun token o header persistito. Tutti gli oggetti diagnostici restano conservati; nessuna DELETE o pulizia distruttiva. Nessun rollback del servizio necessario perché non modificato.

## Limiti e provenienza

È una prova integrata del **nucleo coda/storage con GCS reale**, distinta dal precedente probe della sola primitiva CAS. Non collauda l'intero servizio distribuito: endpoint Cloud Run, autenticazione Google Owner, UI e runtime della specifica immagine cloud non sono eseguiti. Il costruttore GCSStore riceve tramite dependency injection un client SDK con token in memoria: discovery ADC della service identity non attestata. Non è una nuova accettazione operativa o scientifica.

SDK locale isolato: google-cloud-storage 3.17.0 e google-auth 2.61.0, entro i range dei requisiti del servizio; nessuna equivalenza dichiarata con l'immagine cloud. Impronte del codice, SDK, piano e approvazione fissate prima del live. [API ufficiale Blob](https://docs.cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob) e [retry SDK](https://docs.cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.retry) consultati; la pagina latest mostrava 3.16.0, distinta dalla versione locale verificata.

La prova di esaurimento degli **otto retry** è PASS soltanto su memoria con conflitto iniettato, senza cloud o credenziali: il primario resta invariato e il backup del candidato respinto conservato. Non equivale a esaurimento reale GCS. Le copie di scritture respinte sono candidati non confermati, **non head pubblicati**; non devono essere selezionate automaticamente per recovery.

## Residui obbligatori

Concorrenza/retry e backup del nucleo hanno ora evidenza reale. Rimangono le prove dell'intero servizio e le regressioni finali S4/S5. Restano rapporto scientifico completo, full variance/covarianze e calibrazione, timing/proper motion, pipeline multi-epoca, campione cieco con completezza/falsi positivi e policy quantitativa Owner. Reporting CBAT/TNS/VSX/MPC resta requisito: adattatori, tracklet, payload immutabile approvato, revoche/duplicati/ricevute e collaudo previsto; nessun invio autorizzato.

S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6 Accepted con limiti del dossier; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; S10/Safety e C→F invariati. Le due autorizzazioni per questo probe sono consumate, insieme alle cinque OAT e alle due build precedenti. Nessuna nuova estrazione/riattivazione implicitamente autorizzata. Rollback documentale tramite revert governato e rigenerazione delle proiezioni, preservando evidenze e oggetti diagnostici.
