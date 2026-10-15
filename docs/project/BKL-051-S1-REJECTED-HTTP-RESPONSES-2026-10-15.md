# BKL-051 — risposte HTTP rifiutate e chiusura della connessione

Stato: correzione candidata, non attivata sul servizio. BKL-051 **OPEN /
NOT_VALIDATED**, stima indicativa 37%, zero controlli scientifici qualificati.

## Errore postmerge conservato

La [PR601](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/601)
ha superato i 18 controlli premerge e le revisioni indipendenti ARB poi RQ.
Sul merge `2f336dc672ed2d9feb486b89fee499c6f7878fa3`, la suite scientifica
Windows è però terminata con un errore di connessione nel controllo del percorso
worker `close-recovery`, che deve rimanere inesistente. Il client non ha ricevuto
il 404 atteso; gli altri controlli e Pages sono riusciti. Il gate postmerge
precedente resta fallito e non è sanato retroattivamente dai risultati premerge.

Il gestore inviava il 404 e chiudeva immediatamente una connessione con dati
POST ancora non letti. Il medesimo rischio era già gestito per il 403. Una chiusura
TCP con dati in ingresso residui può impedire la consegna della risposta al
client; il codice numerico atteso non basta a dimostrare che il client lo riceva.

## Correzione del trasporto

La stessa chiusura controllata viene riutilizzata per tutte le risposte di errore
del gestore: 400, 403, 404, 409 e 503. Dopo aver inviato e svuotato la risposta,
il server chiude soltanto la direzione di uscita e scarta i dati residui entro i
limiti già esistenti di 64 KiB e 0,25 secondi. I dati scartati non vengono decodificati,
autenticati o eseguiti. Nessun reinvio automatico e nessuna nuova operazione di storage.

Autenticazione, separazione Owner/worker, percorsi, errori JSON, recupero e
idempotenza restano invariati. In particolare il worker non può chiudere la
recovery: quel percorso continua a rispondere 404. Il limite della coda resta
32 binding/job e 1 MiB; la capacità per le 177 esposizioni candidate è ancora
un requisito da completare, non uno scope eliminato.

## Prove e gate

Le regressioni includono richieste POST ripetute su percorsi inesistenti
transient Owner/worker e worker storico, senza mutazioni del registro. Una prova
deterministica controlla half-close, assenza di parsing e limiti di tempo/byte
per tutti gli errori. Il controllo del recupero Owner continua a verificare
l'accesso negato per le altre identità e il rifiuto del percorso worker.

Suite locali, CI e review indipendenti sul commit esatto precedono il merge;
il relativo successore richiede nuovi controlli postmerge. Nessuna prova sintetica
attesta il servizio cloud o l'esecuzione scientifica reale. Non ripetere job,
avvii PixInsight o richieste astronomiche per risolvere un errore di trasporto locale.

Questo codice non autorizza build cloud, deploy del servizio, IAM, nuove risorse,
spese, query IRSA o invii astronomici. Le precedenti prove autorizzate sono
concluse e ripristinate. Un'attivazione richiede il proprio perimetro operativo
approvato; i gate di questa correzione riguardano soltanto codice e prove offline.

Rollback: revert del package, conservando l'errore postmerge precedente, tutte
le ricevute, gli originali e i tentativi incerti. Nessuna cancellazione o replay.
