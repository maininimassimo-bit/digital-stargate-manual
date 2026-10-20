# BKL-051: conservazione dei prodotti nativi

`native_retention.py` implementa la copia di un prodotto opaco prevista dal
contratto W7. Non apre immagini, non legge campioni, non avvia PixInsight e non
accetta una ricevuta terminale. Il supervisore completo resta da integrare.

Il chiamante fidato fornisce due directory private già esistenti, separate e
quiescenti, un nome di file e l'impronta attesa con lunghezza. Sono rifiutati
attraversamenti, alias di percorso individuabili, reparse point e sorgenti con
hard link. Tutti gli antenati esistenti vengono controllati. Il limite per
prodotto è 192 MiB, con letture al massimo di 65536 byte; il supervisore dovrà
applicare anche il limite aggregato, i ruoli ammessi e il massimo di 20 prodotti.

La destinazione viene creata con esclusione del sistema operativo. Un file già
presente blocca la copia anche se vuoto o identico: non viene aperto per scrittura.
La copia verifica lunghezza, impronta, flush e fsync, quindi rilegge destinazione
e sorgente. Identità dei file e delle directory sono ricontrollate. Questi
controlli rilevano le modifiche provate; non costituiscono una protezione contro
un processo ostile che controlli contemporaneamente directory o filesystem.
Il protocollo richiede la proprietà esclusiva delle directory da parte del
supervisore e l'assenza di scritture native al prodotto dopo la sua chiusura.

Ogni eccezione conserva quanto è stato scritto. Non ci sono cancellazione,
recupero automatico o tentativi successivi. Il supervisore deve consumare il
tentativo prima della copia e registrare l'incertezza per qualsiasi eccezione,
compresi errori del proprio registro. Un riavvio del supervisore non può usare
questa funzione per dedurre che una prenotazione sia nuovamente disponibile.

Il risultato attesta soltanto `OPAQUE_BYTES_VERIFIED`, con
`scientificValidation:NOT_VALIDATED`. Non prova la semantica del terminale,
la completezza di History e checkpoint, la chiusura delle viste, il rispetto
del termine o l'accettazione scientifica. Flush, fsync e rilettura non promettono
durabilità assoluta dopo perdita di alimentazione. Questi obblighi restano nel
supervisore e nel successivo collaudo nativo autorizzato.

Le prove usano esclusivamente byte sintetici e verificano collisioni, errori
di impronta e dimensione, errori di fsync, mutazioni della sorgente, corruzione
della copia, limiti, hard link e letture limitate.
