# Candidata CFA v6 con log della console di PixInsight

Il batch apre il logging della console prima del primo caso e lo termina dopo il quinto. Conserva i byte UTF‑8 della console nella stessa directory dei prodotti. Il confronto verifica che il log riporti l’inizio e la fine della prenotazione e i cinque casi in ordine, ciascuno con l’identificativo della finestra dei pesi. Rilegge l’impronta del log prima della chiusura e prima dell’eventuale rilascio. Il log è incluso fra i 18 membri dell’archivio, oltre al marcatore.

Il formato è basato sui metodi di logging della documentazione PJSR installata e sull’uso di beginLog, flush ed endLog nel logger WBPP. La candidata non cambia gli script installati. Il log di prova viene generato dal testimone e i dieci FITS derivano dal modello. Il collaudo verifica che una riga di caso mancante o una modifica al log dopo la chiusura impediscano il rilascio nel registro isolato.

Il soggetto v6 richiede una nuova revisione indipendente. L’attivazione resta priva di configurazione gestita. Formato effettivo del log, provenienza dei FITS e interpretazione scientifica dovranno essere verificati nel processo PixInsight ammesso dal coordinatore.
