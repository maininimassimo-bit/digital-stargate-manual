# BKL-046 · Riferimento di calibrazione per la contaminazione comune TV4

Il controllo aggiunge alla [regola di accordo fra strisce](BKL-046-TV4-ASTENSIONE-RIFERIMENTI.md) un riferimento temporale per il loro profilo comune. Per ogni regione, direzione e metodo media i profili centrati dei due contrasti di calibrazione. La soglia per direzione e metodo è il massimo scarto fra questi due contrasti nelle regioni di calibrazione. Il confronto riservato conserva gli stessi 640 casi, controlli e limiti dell’esperimento precedente. Le decisioni si applicano senza ottimizzare sulle iniezioni riservate.

| Operatore | Accettati oltre il 5% con entrambe le strisce contaminate su 64 pixel, solo accordo | Con riferimento di calibrazione | Correzioni accettate senza iniezione, prima → dopo |
| --- | ---: | ---: | ---: |
| Media | 56/80 | 12/80 | 7/10 → 6/10 |
| Media troncata | 56/80 | 28/80 | 7/10 → 7/10 |

Quando una sola striscia è contaminata su 64 pixel, rimangono 8/80 esiti accettati oltre il 5% per la media e 11/80 per la media troncata. Per la contaminazione comune estesa il passaggio alla regione grezza modifica l’uscita di oltre il 5% in 36/80 casi per la media e 28/80 per la media troncata, rispetto all’uscita dello stesso operatore senza iniezione. Questo scarto è registrato separatamente dall’errore provocato dalla correzione quando viene accettata.

La calibrazione è separata dai contrasti riservati, ma proviene dalla stessa acquisizione TV4. La prova usa iniezioni digitali. Restano da verificare il trasferimento a un’acquisizione indipendente e il comportamento su segnale diffuso reale. DIFFUSE_BACKGROUND/3 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 9deec5a5f5eda736d46b7ab7f041a7f49bc206eacb9098b384b27db9669a1938 |
| Programma | 22753fe4c87a5fa09b190ddfec4c45ccfd08ab1fdf32e5394d7938070e8da7ed |
| Verifica appaiata | 45160cf54687c2799297222be7ce1b199c4bb519eb9318ee7d2271589a7c7e11 |
| Riscontro replicato da H: | d50ac586a6ea38ae745c75417ca51a99544614a2bb7436ee658a729818fcd9a2 |
