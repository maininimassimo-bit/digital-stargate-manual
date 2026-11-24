# BKL-046 · Rilettura GitHub dei documenti indicizzati

Al commit `44983614adfa47320735e00e72c8bb223e988645`, l’indice v1.171 registra 48 documenti pubblici con percorso, commit e SHA-256. Ogni documento è stato recuperato dall’API GitHub al commit indicato. Il controllo ha ricalcolato la dimensione, l’identificativo del blob Git e lo SHA-256 dei byte. Tutti i 48 blob corrispondono anche all’albero del commit dell’indice. I documenti totalizzano 97.332 byte. Due riletture GitHub hanno prodotto lo stesso archivio con indice, documenti e ricevuta.

L’API delle release del repository pubblico restituisce una release, v1.5.0, con zero allegati. La rilettura dei documenti Git copre le 48 schede con impronte registrate. La capsula integrale v1.171, gli allegati e le dipendenze richieste hanno ancora il solo riscontro di recupero locale indicato nell’indice. Per verificare il trasferimento servono il perimetro autorizzato di distribuzione, la destinazione GitHub scelta per il materiale completo e una rilettura degli oggetti effettivamente caricati. La baseline finale resta da accettare.

| Evidenza | SHA-256 |
| --- | --- |
| Programma di rilettura | b301a6b3fa17813613817723f6e935b79b9f23f58ffb0eef3296d916e74a4712 |
| Archivio locale replicato da H: | 676653e38b8980676de1bc9cc860154ef6141cf9422e425b90a7dbdccc5080ed |
