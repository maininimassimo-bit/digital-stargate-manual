# BKL-046 · Launcher CFA v3 con inventario del runtime del comparatore

Il launcher v3 lega al pacchetto l'inventario di 3.824 file del runtime numerico e FITS, per 110.757.228 byte. Il controllo verifica nomi, dimensioni e impronte SHA-256 al preflight e prima dell'esecuzione del comparatore. Anche il codice del comparatore è letto, verificato ed eseguito dagli stessi byte. Un file sostituito con un altro della stessa dimensione, un elemento aggiuntivo e un'impronta estranea sono stati respinti in un albero di prova.

Il preflight effettivo ha verificato due volte percorsi, inventario R4 e file del runtime. Il comparatore ha riprodotto l'autotest e il dispatcher ha riprodotto i quattro risultati coerenti e i tre rifiuti sul registro di prova con la verifica del runtime attiva. I quattro casi coerenti hanno prodotto ricevute R4 di prova dopo la pubblicazione su H:.

Il soggetto per ARB è SHA-256 `d7da70e4fcbcc5ea92d54bb4390577d95cdba116447c350b9860b5f9d90c6727`. ARB e RQ indipendenti restano pendenti, così come l'ammissione. I dati sono sintetici. PixInsight è rimasto chiuso.
SHA-256 archivio H: 557dde6c82f2fb7b736a56633d2a7f0bc9edba8d5c0b19afa80fee98be62b245.
