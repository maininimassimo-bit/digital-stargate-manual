# Classificazione della scala dei pesi XDRZ su mappa intera

Il classificatore BKL-046 confronta intensità, supporto e pesi su tutti i 48 × 48 pixel. Verifica tre ipotesi: pesi grezzi, massimo globale e massimo per canale. I denominatori provengono dall’oracolo offline. Un’unica ipotesi compatibile produce un riscontro numerico e rilegge le 14 impronte XDRZ della selezione. Zero o più ipotesi compatibili lasciano il caso irrisolto.

Il collaudo distingue le tre ipotesi in 96 confronti FITS sintetici. Restano irrisolte sette varianti alterate, comprese le normalizzazioni calcolate sul ritaglio, un peso modificato fuori dal ritaglio e il rigetto omesso. Il test della riga di comando esercita un caso compatibile e uno irrisolto. Entrambi riportano che la provenienza nativa resta da attestare.

Origine e coordinate di rigetto sono parametri della selezione. Il classificatore non le deduce dai FITS. Il significato dei pesi in PixInsight resta da verificare dopo revisione e ammissione.

Per l’autotest eseguire `classifica.py <protocollo.json> <comparatore-ritaglio> <codice-comparatore-precedente> <kit-XDRZ> <zip-calibrati> <pacchetti-Python> <oracolo-pieno.zip> <nuovo-riscontro.json>`. Il confronto di output forniti richiede anche `--request <richiesta.json> --request-sha256 <impronta>`.
