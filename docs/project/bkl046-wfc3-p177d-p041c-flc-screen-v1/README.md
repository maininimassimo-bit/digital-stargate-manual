# BKL-046 · Verifica dei prodotti WFC3 per P041C e P177D

Il protocollo richiede esposizioni FLC di CALWF3 nelle bande F438W, F606W e F814W per verificare la fotometria su stelle esterne al campione precedente. Il controllo riguarda le tre visite e le nove associazioni selezionate nel catalogo congelato.

| Stella | Programma HST | Visita | Associazioni | FLT pubblici distinti | FLC elencati | Richieste FLC dirette con HTTP 404 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| P041C | 12334 | ibnx05 | 3 | 9 | 0 | 9 |
| P177D | 12334 | ibnx06 | 3 | 6 | 0 | 6 |
| P177D | 12699 | ibwi04 | 3 | 6 | 0 | 6 |

Le nove risposte MAST non elencavano prodotti FLC pubblici. Le 21 richieste dirette ai nomi FLC corrispondenti alle radici FLT hanno restituito tutte HTTP 404. Il risultato vale per le associazioni e gli endpoint interrogati durante questa acquisizione. Nessuna visita ha soddisfatto il requisito FLC. Non sono stati misurati flussi, colori o correzioni di apertura. Nessuna chiusura scientifica e nessun avvio di PixInsight.

Il rapporto [riscontro.json](riscontro.json) contiene la decisione per associazione. Il [riscontro degli endpoint](riscontro-endpoint.json) conserva nome, richiesta, codice HTTP e impronta del corpo di errore. Il pacchetto archiviato contiene anche le risposte del catalogo e le mappe PAM usate dal programma.

Per una riproduzione offline, estrarre il pacchetto e passare a `misura.py` la directory estratta, la directory che contiene NumPy 2.3.5 e Astropy 7.2.0, un nuovo percorso per il rapporto e lo SHA-256 dell’acquisizione `0febc35785b4c30dad737ddffe64faa1241c5fe7e05dbabe219b90fef3641d03`. Eseguire `verifica-registro.py` con la directory estratta per controllare la corrispondenza tra le risposte di catalogo e gli esiti HTTP registrati.