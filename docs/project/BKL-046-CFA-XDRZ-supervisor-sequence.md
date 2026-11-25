# BKL-046 · Sequenza candidata del supervisore CFA

La sequenza riceve gli eventi dal canale originale del parent. Prima della cattura valida operazione, prenotazione, piano, soggetto e identità dichiarata del processo. Richiede una finestra associata al PID e all'istante di creazione attesi. Dopo la cattura verifica la rilettura dell'immagine e l'esito del comparatore legato al marcatore del batch. Per la chiusura ordinaria richiede un nuovo controllo della stessa finestra e lo stesso contesto.

Il rilascio richiede terminale coerente, uscita zero del parent originale, conferma dell'uscita del processo originale, finestra chiusa e rilettura dei risultati. Il simulatore ha verificato due percorsi conformi, uno con il flusso degli eventi frammentato, e 14 casi negativi. Fra questi rientrano cattura mancante, finestra diversa, perdita del canale di osservazione, ricevuta alterata, esiti incompleti e uscita non zero. Nessun caso negativo ha chiamato il rilascio. Le due ricevute coincidono.

Il modulo richiede componenti di osservazione, cattura, confronto e pubblicazione forniti dal launcher revisionato. Il test usa risposte simulate per tali componenti. Restano da verificare la cattura sulla finestra PixInsight, la provenienza delle esportazioni e il binding operativo completo dopo revisione. Nessuna ammissione o esecuzione nativa.

Ricevuta SHA-256 `bf982bc965edf353e32c58a3bcd52d028a357fa4d7353f70cc6c7829b571bd48`.
