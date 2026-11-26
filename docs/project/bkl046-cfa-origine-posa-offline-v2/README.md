# BKL-046 · Posa offline della candidata CFA v2

Il collaudo su DSG-Shared ha verificato 56 file dopo la posa in una directory di prova isolata. Di questi, 24 appartengono alla gerarchia di piano, oracoli e ingressi congelati. L'esecutore verifica l'impronta dello ZIP, il descrittore, i file e i due interpreti. Il collaudo respinge uno ZIP modificato, una destinazione esistente e un piano alterato dopo la posa.

Il controllo avvia Node con un ambiente esplicito e verifica che le impostazioni NODE_OPTIONS e NODE_PATH del chiamante siano escluse. L'entrypoint esatto termina con il rifiuto previsto mentre l'attivazione resta assente.

L'esito riguarda la posa in laboratorio. Restano da qualificare l'installazione protetta e il contesto di lancio effettivo, incluse le ACL della catena di avvio e la costruzione dell'ambiente dallo stesso launcher protetto. Restano richieste le ricevute indipendenti ARB e RQ sul soggetto esatto. Zero richieste di ammissione, avvii nativi o chiusure scientifiche.