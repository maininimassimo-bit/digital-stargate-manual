# BKL-046 · Registrazione M8–M20 con centroidi sui verdi originali

Il controllo confronta il fit affine robusto con centroidi a metà scala e con centroidi sul mosaico originale. Le due nuove stime usano le stesse 48 stelle di addestramento e 53 stelle di verifica per posa. Per ogni associazione del secondo metodo il centro è la media dei due centroidi stimati separatamente sulle parità verdi, a larghezza del profilo fissata dalle stelle di addestramento. L'esecuzione riproduce anche gli errori della geometria precedente e verifica che larghezze e associazioni coincidano con la prova sulle parità verdi.

| Metodo sulle stesse 742 associazioni di verifica | P90 complessivo (px nativi) | Pose con P90 fino a 0,30 px |
| --- | ---: | ---: |
| Centroidi a metà scala, fit archiviato con tutte le stelle di stima | 0,396267 | 3/14 |
| Centroidi a metà scala, fit ricalcolato con le stesse 48 stelle di stima | 0,400881 | 1/14 |
| Centroidi sul mosaico, fit ricalcolato con le stesse 48 stelle di stima | 0,298526 | 7/14 |

I centroidi sul mosaico riducono il P90 in 13 pose su 14 rispetto al fit appaiato, di circa il 26% sul totale. Il P90 per posa varia da 0,171 a 0,377 pixel. Restano sette pose sopra la soglia, quindi il risultato complessivo sotto 0,30 pixel non implica il superamento del criterio per posa. La convalida appaiata condivide stelle, associazioni e riferimento. La misura riguarda i residui di posizione. Gli effetti radiometrici e la validazione CFA in PixInsight alla stessa scala restano aperti.

Due esecuzioni hanno prodotto ricevute identiche con SHA-256 `8b8f89d0249f7fbe739bc3d283cd83be3af79207600714fb224c6934435f3180`. Zero esecuzioni native.
