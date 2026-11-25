# BKL-046 · Fit affine stellare con e senza pesi di Huber

Dalle pose Bayer di M8 e M20 si ricavano 49 tracce complete nelle otto regioni pari per stimare, separatamente per posa, un campo affine dagli spostamenti dei centroidi. Si confrontano minimi quadrati ordinari e ripesatura di Huber, con soglia radiale fissata a 0,30 pixel nativi e 12 iterazioni. Le 54 stelle delle regioni dispari sono le stesse del confronto precedente. I residui individuali pubblicati per traslazione e affine regionale sono stati riprodotti alla precisione archiviata. Il controllo su un campo affine esatto verifica entrambi gli stimatori. Con una misura alterata deliberatamente, la stima robusta resta più vicina ai coefficienti noti.

| Modello | P90 su 756 residui (px nativi) | Pose con P90 ≤ 0,30 px |
| --- | ---: | ---: |
| Traslazione | 0,636 | 1/14 |
| Affine regionale | 0,437 | 1/14 |
| Affine stellare ordinario | 0,414 | 1/14 |
| Affine stellare con Huber | 0,394 | 3/14 |

Il fit con Huber riduce il P90 rispetto all'affine regionale in 10 pose su 14. Undici pose superano ancora la soglia. La stima usa una previsualizzazione a metà scala derivata dalle due parità verdi del RAW. I residui comprendono incertezza del centroide, errore di associazione ed errore del modello. Le stelle sono riutilizzate sulle stesse pose. Il risultato riguarda la registrazione di questo campo e lascia da verificare il contributo della misura del centroide e le prestazioni radiometriche di una ricostruzione CFA a scala comune. Zero esecuzioni native e zero chiusure scientifiche. [Dati di Colmic](https://siril.org/tutorials/tuto-scripts/index.html)

SHA-256 della ricevuta `aaadaabe9c31bd79f56b539c1c4d5301b017f87a75b9c193e753404742592e77`.
