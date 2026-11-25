# BKL-046 — Maschera su fotogrammi disgiunti per il segnale diffuso TV4

Il [controllo precedente](BKL-046-TV4-RIGA-CONSERVAZIONE-DIFFUSO.md) usava la posizione nota dell'iniezione per escludere i pixel occupati dalla sorgente. Qui la maschera deriva dalla media delle differenze di fotogrammi disgiunti da quelli usati per misurare il recupero. Il test scambia i due gruppi all'interno della stessa sequenza e si ripete nel dark e in CLEAR1 a comando zero. Il profilo sintetico è presente nei due gruppi, con rumore reale proveniente da fotogrammi separati. Le soglie e il sostegno minimo di 32 pixel per riga sono comuni a tutte le prove.

| Profilo | Picco | Flusso recuperato con la maschera ricavata dai fotogrammi |
| --- | --- | ---: |
| Gaussiana compatta, σ orizzontale 8 px | 0,5–4 DN | 99,97% |
| Gaussiana larga, σ orizzontale 21 px | 0,5 e 2 DN | 88,98% |
| Gaussiana larga, σ orizzontale 21 px | 4 DN | 89,30–89,76% |
| Fondo uniforme | 0,5–4 DN | 0% |
| Banda gaussiana che occupa tutta la riga | 0,5–4 DN | 0% |

Il rilevatore di maschera sottrae la mediana della riga prima di cercare il segnale. Un profilo costante lungo la riga scompare già in quel passaggio. Nessuna delle iniezioni uniformi o a banda intera innesca il veto. Il controllo del numero di pixel disponibili è quindi insufficiente per proteggere le componenti che il rilevatore stesso non rende osservabili. Per la gaussiana larga, la maschera ricavata dai fotogrammi resta sotto il 98,79% del controllo precedente con la forma nota. Risultati analoghi sui rischi di sottrazione eccessiva del fondo sono documentati in altri contesti di imaging a bassa brillanza superficiale. [Studio di Watkins et al.](https://academic.oup.com/mnras/article/528/3/4289/7603727)

I gruppi sono disgiunti all'interno di ciascuna verifica, provengono dalla stessa sessione di laboratorio e si scambiano nel secondo passaggio. Questo riscontro riguarda la sottrazione per riga e il rilevatore provati sui profili sintetici. Per le componenti estese a tutta la riga serve un riferimento osservativo che le distingua dall'offset. Restano aperti il trasferimento a immagini scientifiche e il confronto nativo.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro e replay identico | bf868823f671e3e176a21ad49400a333a8256dc4d63c9ba625289c05ba048784 |
| Archivio riletto su H: | 0c9c970c4322076b2739a09ed6e6c86ad5c598739f5438621072f2f0a8d8c665 |

Zero esecuzioni native e zero chiusure scientifiche in questo incremento.
