# BKL-046 · Contabilità persistente delle risposte Native64

Il collaudo usa il valutatore già fissato in una banca SQLite temporanea su DSG-Shared. Una transazione lega lo stato del ticket all'impronta della risposta e al verdetto. La banca registra l'assegnazione anche quando la risposta manca. I controlli impediscono aggiornamenti o cancellazioni dei record terminali attraverso le operazioni provate.

- Due processi competono sullo stesso ticket. Il primo trattiene la transazione mentre il secondo raggiunge il tentativo di apertura. Un processo conclude la valutazione e l'altro riceve il rifiuto di riuso.
- Un processo di prova viene terminato dopo la scrittura e prima del commit. Dopo il rollback la nuova connessione vede il ticket assegnato senza impronta di risposta. Una nuova valutazione della stessa fixture locale conclude il ticket una sola volta.
- Le risposte mancanti e malformate rimangono terminali e irrisolte. I due verdetti valutati conservano insieme affermazione infondata e astensione. L'integrità della banca risulta corretta al termine.

Il collaudo riguarda un archivio locale con processi cooperanti. Lascia da verificare la custodia separata delle chiavi, il controllo degli accessi alla banca, il ripristino in caso di perdita del volume e il legame con un trasporto effettivo. La ripetizione dopo un rollback riguarda il valutatore di fixture. La prova non effettua chiamate a provider o richieste al coordinatore.

Per ripetere usare Python 3.12 con `verifica.py fixture <protocollo> <verifica.py storico> <nuovo rapporto>`.
