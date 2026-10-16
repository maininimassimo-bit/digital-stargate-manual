# BKL-051: uscita posseduta dopo conservazione

Stato: sorgente candidata per il futuro supervisore, senza CLI o collegamento
operativo. Nessuna esecuzione o chiusura nativa autorizzata da questo documento.
Il consenso fresco sul pacchetto esatto resta un gate esterno del supervisore.
Milestone aperta, `NOT_VALIDATED`, zero nuovi controlli reali qualificati.

`OwnedNativeClosure` conserva il verificatore vivo originale e tutti i riferimenti
al tentativo. Una sola istanza è ammessa sui registri, con un solo tentativo di
chiusura. Costruirla non interroga né chiude processi e non crea una ricevuta.
Il futuro supervisore può invocarla soltanto nel proprio tentativo autorizzato,
dopo preparazione e avvio posseduto: un file, PID o booleano non ricostruisce
quel contesto. Il componente non avvia processi, cerca PID o rilascia blocchi.

Il percorso di chiusura verifica prima la composizione viva completa. Se l'handle
originale è già uscito, conserva il codice effettivo. Altrimenti attende fino a
un secondo sullo stesso handle Windows; se resta attivo, ripete la verifica
completa immediatamente prima dell'unico `TerminateProcess` del processo già
quiescente dopo il ritorno causale e la conservazione verificata. Attende poi
fino a 30 secondi sullo stesso handle e richiede l'uscita effettiva. Non usa
`Popen.terminate`, `Popen.wait`, PID persistiti o handle riaperti. Qualsiasi errore
precedente alla decisione impedisce la terminazione; dopo un errore non segue
un secondo tentativo. L'API Windows viene usata soltanto quando `close()` è
invocato dal futuro percorso operativo autorizzato, mai dai test con processi reali.

La ricevuta esclusiva `owned-closure.json` segue i sedici campi esatti di S7 del
contratto V5: binding originali, marker e ritorno, sessione e FILETIME, codice
effettivo, metodo, superamenti e accettazione tecnica condizionale. Il successo
tecnico richiede completamento condizionale, codice zero, nessun superamento
nativo, monotono o UTC e nessuna cancellazione. Un codice nonzero preesistente,
un fallimento nativo o una conservazione dopo scadenza restano soltanto cleanup.
`technicalComputationAccepted` non è accettazione scientifica né validazione del
modello fisico; tutti gli esiti restano `NOT_VALIDATED` con zero qualificati.

L'uscita viene conservata in memoria prima di ulteriori verifiche o scritture.
Solo dopo la nuova verifica completa si scrive la ricevuta con creazione
esclusiva, fsync e rilettura. Il controllo prechiusura vieta intenzionalmente
qualunque ricevuta di chiusura: non viene riabilitato. La fase terminale verifica
invece esattamente il nuovo file originale, tutti i pin S7 originali, i blocchi,
la pubblicazione viva, sessione, handle uscito, directory, cancellazione e segnali
prima e dopo l'ultima lettura. Non accetta una ricevuta sostituita con byte identici.
Un errore o una scadenza attraversata durante la ricevuta mantiene il file
storico ma produce `EXIT_VERIFIED_EVIDENCE_UNCERTAIN` in memoria, mai un successo.
Il supervisore dovrà conservare quel contesto e tentare una sola registrazione
di incertezza tramite i segnali esistenti. L'assenza del file non prova successo.

`observe_exit()` rimane disponibile per osservazioni limitate anche dopo errore.
Se l'handle originale mostra l'uscita, il componente conserva il fatto reale e
il codice, anche quando i controlli della ricevuta falliscono. Non finge che
il processo sia ancora vivo e non riabilita chiusura, nuovi avvii o ricostruzioni.
I blocchi e il Popen rimangono riferimenti forti: la loro gestione finale spetta
al supervisore dopo i propri gate, non a finalizzatori automatici.

Le prove usano esclusivamente processi e chiamate Windows simulati. Una prova di
composizione usa il controllo vivo reale su file sintetici opachi, bootstrap e
blocchi fittizi e osservazione del processo simulata; non è una prova nativa o
scientifica. Servono ancora composizione nel supervisore, preparatore/entry e
manifest esatti, consenso fresco e preflight PJSR reale prima di interpretazioni
osservative. Vale il confine privato e quiescente del contratto, non un sandbox
contro codice ostile dello stesso utente.

Rollback: revert dei tre file prima di ogni collegamento operativo; nessuna
risorsa o esecuzione reale è stata prodotta. Preservare tutte le prove e gli esiti
incerti: un rollback non autorizza ripetizioni o cancellazioni.
