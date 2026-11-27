# BKL-046 · Ordine dei controlli memoria Stream34 v11

Il collaudo carica dai sorgenti fissati il preflight e i metodi di avvio di Stream34 v11. Simula `GlobalMemoryStatusEx`, le scritture e la creazione del processo. I nove casi al confine confermano le soglie di 8 GiB di memoria fisica e 12 GiB di commit disponibile. L'uguaglianza con entrambe le soglie è ammessa. Un byte sotto una soglia produce il rispettivo rifiuto.

Nei sei scenari di avvio la riserva iniziale insufficiente impedisce di registrare l'intento. Se l'ultima lettura rileva una riserva insufficiente o fallisce, l'intento può essere già scritto e la creazione non viene invocata. Con entrambe le soglie rispettate, l'ultimo campione precede direttamente la chiamata di creazione simulata. La ricevuta del campione viene scritta dopo. Un errore in quella scrittura lascia conservato il custode del processo simulato.

La verifica riguarda l'ordine delle azioni nel codice fissato dopo il rilievo ARB. Non misura pressione o riserva continua della memoria, non accede al registro canonico e non richiede ammissione. Le approvazioni autentiche di v11 restano necessarie prima dell'esecuzione. Zero avvii PixInsight e zero chiusure scientifiche.

Per replicare, estrarre la candidata dal fascicolo con le impronte indicate nel protocollo. Passare a `collaudo.py` il protocollo, la directory della candidata estratta e il nuovo percorso del rapporto.
