# BKL-046 · Prova isolata della custodia R4 per i controlli XDRZ

Il collaudo esegue le funzioni installate di R4 per acquisizione esclusiva, identità del parent e osservazione del suo handle Windows. L'adattatore è riletto dall'installazione e il collaudo cambia, in memoria, solo il percorso di ingresso del custode per usare un registro temporaneo. Il parent è il testimone CFA. L'inventario PixInsight e l'esito della comparazione dei prodotti sono simulati.

| Caso | Esito |
| --- | --- |
| Parent originale legato, esito simulato presente e uscita zero | Il custode rilascia dopo l'uscita e scrive la ricevuta nel registro temporaneo |
| Parent originale legato con uscita non zero | La richiesta di rilascio è respinta e la prenotazione resta trattenuta |
| Uscita zero con evidenza del comparatore mancante | L'operatore del collaudo omette il rilascio e la prenotazione resta trattenuta |
| Prenotazione precedente già presente | Nessun parent viene creato e il record precedente è conservato |

Le due esecuzioni hanno prodotto la stessa ricevuta. I 30 file del registro canonico, letti prima e dopo, hanno conservato le impronte. Il collaudo non richiede un'ammissione sul registro canonico. Restano da integrare il comparatore reale e la custodia del processo e della finestra PixInsight. Il binding completo resta soggetto a revisione.

Ricevuta SHA-256 `cede53325e05b46824df7cf7fd7212901928a3373bee0102b869a72e0fd04859`. Zero esecuzioni native.
