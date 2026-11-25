# BKL-046 · Verifica congiunta del batch sull'origine XDRZ

Il verificatore riceve la prenotazione attesa e controlla il marcatore, i nomi dei quattro casi e l'ordine delle otto righe di log. Per ogni caso verifica i tre XDRZ dichiarati, i parametri fissi, la presenza della sorgente PJSR esportata, la coerenza dei tre enumeratori e i percorsi delle due uscite. Il classificatore numerico opera sugli otto FITS riletti. La ricevuta lega le impronte del log, del marcatore e dei FITS all'esito numerico.

Tre scenari prodotti dal batch con API simulate sono accettati. In sette copie del caso valido i FITS restano intatti. Il verificatore respinge comunque una prenotazione diversa, un ingresso o una destinazione dichiarata errati, un deposito modificato, sorgente assente, enumeratore incoerente e log incompleto.

Il controllo riguarda coerenza dei file e parametri dichiarati. Gli enumeratori devono essere verificati con le API del runtime ammesso. Il verificatore non dimostra chi ha scritto le evidenze né che la prenotazione sia stata ammessa. Restano necessari il processo padre vincolato a R4, la custodia del processo originale e una revisione del pacchetto prima dell'ammissione. [Batch candidato](../bkl046-cfa-origin-batch-candidate-v1/README.md)

Argomenti del comando Python: ID atteso della prenotazione, directory con piano, manifest e classificatore, directory degli oracoli, file del comparatore v4, directory delle dipendenze, directory con marcatore, eventi e sottocartella outputs, nuovo percorso per la ricevuta. Il kit H/K conserva tutte le fixture usate per il replay.