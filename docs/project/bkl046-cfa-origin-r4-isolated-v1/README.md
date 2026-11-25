# BKL-046 · Controllo dell'origine in un registro R4 isolato

Il collaudo usa il custode R4 installato e l'adattatore del parent originale con le rispettive impronte. Reindirizza il comando del custode a un ingresso di prova che accetta solo directory isolate. Il processo padre è un testimone Python reale, identificato da PID e ora di creazione attraverso FD3. Il custode acquisisce e controlla l'handle del testimone. L'inventario PixInsight, i FITS e gli eventi del batch sono di prova. Gli eventi sono associati all'ID creato per ciascuna nuova prenotazione del registro isolato.

| Scenario | Uscita del padre | Verifica dei prodotti | R4 isolato |
| --- | ---: | --- | --- |
| Confronto valido | 0 | Ipotesi riconosciuta | Una richiesta di rilascio, ricevuta presente |
| Parametri trascritti difformi | 0 | Log respinto | Trattenuta |
| FITS leggibili, sequenza fuori modello | 0 | Nessuna ipotesi riconosciuta | Trattenuta |
| Padre fallito | 7 | Ipotesi riconosciuta | Trattenuta |

Le copie di acquisizione e identità del parent sono state rilette in tutti i casi. Nei tre rifiuti il test non ha inviato il comando di rilascio e ha verificato che il record attivo fosse ancora presente, senza ricevuta di rilascio. Il controllo dimostra la decisione del driver di prova con il custode reale su stato isolato. Mancano ancora la custodia della finestra e del processo PixInsight, la pubblicazione con blocco dei prodotti e la revisione dell'intero launcher. Nessun accesso al registro canonico e nessuna esecuzione PixInsight. [Verifica del batch](../bkl046-cfa-origin-bound-batch-evidence-v1/README.md)

Il collaudo Node richiede Python fissato dal soggetto v4, la directory del kit di verifica del batch con le sue fixture, parent_barrier.py v4, la directory delle dipendenze e due percorsi nuovi per stato di prova e rapporto. Il kit usa la stessa installazione R4 su DSG-Shared.