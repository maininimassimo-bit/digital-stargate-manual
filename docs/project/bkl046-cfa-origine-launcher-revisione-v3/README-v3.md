# BKL-046 · Preflight della candidata CFA v3

Il launcher v2 verificava il runtime del comparatore prima di richiedere la prenotazione. La verifica dei file PixInsight e dei dati della prova avveniva nel padre dopo l'ammissione. La v3 esegue un primo controllo di questi file prima di avviare l'adattatore R4. Il padre mantiene la verifica sotto custodia prevista dalla candidata v2.

Su DSG-Shared il preflight ha verificato 3 file PixInsight, 12 XDRZ, 6 FITS, il piano, il codice batch, 3 identità storage e 3824 file del comparatore. Quattro letture alterate in memoria sono state respinte separatamente per l'eseguibile, un XDRZ, un FITS e il batch. I file sorgente sono rimasti intatti.

Il nuovo soggetto è 8d4ba1c9268399de1ac98dccf17c622877cb25eca23118ecfb8388241a22849a. Il controllo con chiavi di prova attesta il comportamento del verificatore. Per l'attivazione servono le approvazioni autentiche ARB e RQ sul nuovo soggetto e la qualifica dell'installazione protetta. Nessuna ammissione richiesta e nessun avvio nativo.