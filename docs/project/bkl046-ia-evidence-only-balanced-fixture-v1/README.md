# BKL-046 · Formato di collaudo IA basato sulle evidenze

Il formato fornisce misure, conteggi di supporto, elenco delle unità, registri terminali e riferimenti delle ricevute. Quattro verifiche riguardano la soglia relativa, il supporto, la completezza dell'elenco assegnato e la coerenza dei legami tra le ricevute di prova. La richiesta esclude i campi contenenti il verdetto. Un archivio di confronto separato lega le risposte attese all'impronta di ciascuna richiesta.

Le 16 combinazioni delle quattro risposte attese sono rappresentate due volte. La seconda variante cambia segni, valori e meccanismo del legame errato. Il controllo deterministico ricava 128 risposte corrette su 128. La regola che risponde sempre NO ottiene 64 risposte corrette su 128 e due ticket interamente corretti su 32. Tre prove aggiuntive respingono un campo di verdetto, un campo estraneo in un endpoint e la ripetizione di un registro.

Le ricevute e le misure sono sintetiche. La coerenza referenziale della fixture non è un'ammissione R4. Le chiavi sono in file separati per costruzione, mentre la separazione effettiva degli accessi rimane da verificare. Le unità confermative vere restano zero e il campione bilanciato non rappresenta una prevalenza osservata.

Per ripetere usare Python 3.12 con il protocollo, il rapporto di ablazione Native64, il rapporto sulla quota fissata e una nuova directory di uscita. La pubblicazione contiene codice, protocollo e conteggi. Le due serie di file di prova sono conservate negli archivi H: e K:.
