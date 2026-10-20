# BKL-051 — driver esplicito nel contesto originale

Stato: candidato tecnico non operativo. Non autorizza preparazione o esecuzione
reale. Milestone aperta, `NOT_VALIDATED`, zero controlli qualificati.

`native_linear_driver.main(session)` è un entry callable del bootstrap isolato
già definito. Non aggiunge argomenti al bootstrap, non legge credenziali e non
ricostruisce sessioni, processi, PID o grant da registri persistiti. Il bootstrap
operativo e il suo manifest esatto devono ancora essere confezionati e rivisti.

Il driver conserva sulla sessione originale un unico contesto vivo, anche dopo
errori del trasporto. Il primo `PREPARE` è consumato prima di costruire il
preparatore. Il preparatore conserva il budget originale e ritorna un supervisore
non avviato. Serve un successivo comando `START`, unico. Un secondo driver sulla
stessa sessione, una seconda preparazione e un secondo avvio sono rifiutati.

Il consenso umano fresco e circoscritto è una precondizione del chiamante fidato
prima di `PREPARE`. Né i comandi né il JSON di provenienza autenticano il consenso.
Non esiste un avvio automatico all'apertura o alla chiusura del trasporto.

Il canale binario accetta una riga JSON ASCII terminata da newline, al massimo
4096 byte. Il protocollo è `DSG_NATIVE_LINEAR_DRIVER_V1`, con campi chiusi:

| Comando | Campi oltre `protocol` e `command` | Effetto |
| --- | --- | --- |
| PREPARE | planPath, planSha256, approvalPath, approvalSha256 | Una preparazione dopo consenso fresco esterno |
| START | nessuno | Un avvio tramite il supervisore originale |
| TICK | nessuno | Un passo esplicito, potenzialmente conservazione e chiusura verificata |
| CANCEL | nessuno | Passo esplicito con richiesta cooperativa di arresto |
| OBSERVE | nessuno | Solo osservazione dell'handle originale, senza TICK o chiusura |
| STATUS | nessuno | Diagnostica memorizzata, senza prova fresca del processo |
| RELEASE_FILES | nessuno | Rilascio esplicito dei blocchi se mai avviato o uscito con identità fidata |
| EXIT | nessuno | Stesso gate di rilascio, poi termine del canale |

Non esistono daemon, polling pianificato o rinnovo del budget. Il chiamante deve
inviare i passi; una lettura bloccante non controlla autonomamente la scadenza del
parent. Il timeout nativo resta cooperativo, non una promessa di arresto forzato.
`TICK` mantiene integralmente i gate del supervisore: la presenza di un file o
l'uscita del processo da sole non autorizzano pubblicazione o chiusura.

EOF, righe eccessive/incomplete o errori del canale producono incertezza, tentativo
singolo di cancellazione e conservazione dei riferimenti disponibili. Non sono
una ricevuta di uscita. Una perdita del parent richiede riconciliazione distinta,
senza ricostruirne l'autorità. I messaggi di errore non restituiscono percorsi o
testo arbitrario delle eccezioni.

`EXIT` durante un processo attivo o un avvio ambiguo è rifiutato. Un processo
osservato uscito ma con identità incerta non permette il rilascio. Il rilascio
non attribuisce successo tecnico o scientifico e conserva i riferimenti Python;
non cancella prodotti o registri. Gli errori di rilascio restano visibili e i
blocchi non chiusi rimangono conservati per un esplicito tentativo di cleanup.

Le prove del canale usano preparatori, supervisori e handle simulati. Una prova
di composizione collega preparatore e supervisore reali su file sintetici opachi,
con rendering e blocchi nativi simulati: preparazione senza avvio e cancellazione
prima dell'avvio mantengono lo stesso budget e vietano il successivo `START`.
Non dimostrano compatibilità PJSR/Windows reale né validazione scientifica.
Rollback: rimuovere i tre file prima del collegamento operativo, conservando le
evidenze; nessuna esecuzione nativa è stata prodotta da questo incremento.
