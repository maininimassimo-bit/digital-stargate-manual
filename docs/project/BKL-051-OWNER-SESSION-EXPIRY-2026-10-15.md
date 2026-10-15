# BKL-051 — scadenza dell'accesso Owner

Stato: correzione locale candidata, non rilasciata. Milestone **OPEN /
NOT_VALIDATED**, stima indicativa 37%, zero controlli qualificati.

## Esito della prova precedente

PR596 ha introdotto il registro isolato ed è stata integrata e verificata fino
alla pubblicazione. La successiva prova autorizzata ha completato una esecuzione
diagnostica reale PixInsight, con ricevuta remota e collegamento al piano.
Il secondo comando dal portale ha ricevuto un rifiuto di accesso non autorizzato
o scaduto; la richiesta conservata resta da riconciliare, senza presumere che il
job sia stato creato o ripetere il comando. Gli altri due avvii nativi non sono
avvenuti. Nessuna diagnosi distingue retroattivamente scadenza e altri motivi
di rifiuto sulla base del solo messaggio HTTP.

Finestra interrotta: traffico precedente al 100%, dieci tag conservati,
configurazione e immagine originali ripristinate, quattro variabili transitorie
rimosse e sola aggiunta IAM temporanea rimossa. Il limite superiore registrato
è 47 richieste applicative sulle 384 autorizzate, incluse le riserve CORS.
Nuovo dossier locale verificato: un tentativo, copertura incompleta 1/3,
zero lacune archivistiche; il precedente dossier senza tentativi resta storico.
Il risultato RAW al centro geometrico è diagnostico, senza associazione sorgente,
varianza completa, significatività o accettazione scientifica.

## Correzione candidata

Il browser ricava soltanto la scadenza numerica `exp` dalla credenziale ricevuta
dal callback Google. Non la usa per attestare firma, identità o autorizzazione:
queste verifiche restano obbligatorie sul servizio. La decodifica è un controllo
preventivo locale, coerente con la [descrizione Google della credenziale e della
scadenza](https://developers.google.com/identity/gsi/web/reference/js-reference#CredentialResponse).

Prima di ogni richiesta HTTP e prima di conservare un nuovo intento, il portale
richiede oltre 30 secondi di validità residua, pari al timeout applicativo già
presente. In caso contrario termina l'accesso locale, elimina la vista privata
corrente e invita al nuovo accesso. Il margine non garantisce la validità lato
server: revoche, orologio locale errato e risposte tardive restano possibili.
HTTP401/403 continuano a disconnettere e a conservare gli intenti incerti.

Una credenziale malformata, senza scadenza intera positiva o con valore fuori
dall'intervallo numerico sicuro non avvia letture. Token e scadenza restano in
memoria e vengono eliminati su disconnessione o navigazione. Nessun refresh
automatico dell'identità, login automatizzato, polling o nuovo endpoint.
Un intento precedente non viene cancellato o reinviato dalla scadenza: occorrono
nuovo accesso, consultazione dello stato e comando manuale idempotente applicabile.

## Prove e residui

Quattro regressioni riproducono il comportamento precedente e verificano:
credenziale già scaduta, creazione vicina alla scadenza prima di scrivere
l'intento, conservazione della richiesta incerta alla scadenza e credenziali
malformate. Intera suite del portale: 49 test locali superati. Le credenziali dei
test sono sintetiche e senza firma; nessuna richiesta Google o cloud reale.

Restano gate del commit esatto, review indipendenti, rilascio e collaudo del
nuovo frontend. Una nuova finestra operativa richiede consenso specifico: quella
precedente è chiusa e non autorizza altre revisioni, permessi o avvii. Restano
inoltre capacità 32 binding/job e 1MiB, completamento della tripletta e tutti i
requisiti scientifici, di qualificazione indipendente e reporting della milestone.
Rollback frontend tramite revert; evidenze e richiesta pendente preservate.
