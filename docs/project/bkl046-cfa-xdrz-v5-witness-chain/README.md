# Catena CFA v5 con testimone Windows e registro isolato

Il collaudo usa i moduli esatti del soggetto CFA v5. Il custode R4 installato agisce sul registro di prova e riceve un inventario simulato. Il processo padre usa il protocollo effettivo. Rilegge il marcatore nella cartella products, custodisce l’handle di un testimone Windows e passa i FITS simulati al comparatore della candidata.

Il caso conforme ha osservato la chiusura ordinaria e l’uscita a zero, verificato 17 file archiviati e rilasciato la prenotazione di prova. La finestra non reattiva e la maschera priva dell’effetto atteso hanno trattenuto la prenotazione. Anche la modifica del log dopo la chiusura e la collisione di archivio l’hanno trattenuta, pur con uscita a zero del parent.

L’archivio conserva i sorgenti e il rapporto del collaudo. Per replicare eseguire `node collaudo-catena.cjs <Python-fissato> <nuovo-rapporto.json> <directory-laboratorio>` su DSG-Shared. Le fonti della candidata, il kit congelato, il runtime del comparatore e il custode installato sono verificati nei rispettivi ingressi. È una prova dell’integrazione su registro isolato. La provenienza nativa dei FITS richiede ancora ARB, RQ, attivazione gestita e ammissione del coordinatore.
