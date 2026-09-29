# Session Comparison — andamento SQM

Il grafico è collocato sotto la Hero e prima dei riepiloghi numerici. Usa esclusivamente includedSessions della projection BKL037-SQM-DYNAMIC-V1: mediana SQM in mag/arcsec², senza score, ranking o soglie. Ogni punto apre la sessione; una tabella accessibile espone valori e provenienza. Scala verticale adattiva esplicita, asse temporale reale, linee interrotte tra notti non consecutive. Dati mancanti non sono zero.

La pipeline di importazione rigenera già session-comparison-projection.json dal catalogo. Il consumer recupera il nuovo snapshot alla visita e ogni cinque minuti quando visibile. Snapshot invariato preserva il contenuto; errori rimuovono il grafico precedente. Nessun nuovo servizio, libreria o rendering continuo. Su mobile il grafico scorre internamente per mantenere leggibili le etichette.

Le misure rappresentano luminosità del cielo nel campionamento della sorgente, non certificano seeing, trasparenza, sicurezza o qualità complessiva delle immagini. Non vengono applicate nuove finestre notturne o correzioni fisiche.
