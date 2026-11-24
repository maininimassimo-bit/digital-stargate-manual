# BKL-046 · Fit WFC3/P330E con griglia di centratura a 1/32 di pixel

La prova ripete le stesse 1.536 immagini sintetiche con 24 maschere di P330E del [fit con fuoco interpolato](BKL-046-WFC3-P330E-INTERPOLAZIONE.md). Il passo della griglia di centratura passa da 1/8 a 1/32 di pixel su entrambi gli assi. Le fasi vere restano fuori dalla nuova griglia. Il fit usa gli stessi modelli di fuoco, la stessa apertura, i medesimi livelli di segnale e le stesse realizzazioni di rumore. Tutti i 3.072 record di controllo con forma e centro sintetici esatti coincidono con il precedente esperimento.

| Banda | Segnale, elettroni | P90 con maschera a 1/8 px | P90 con maschera a 1/32 px | P90 di centratura a 1/32 px |
| --- | ---: | ---: | ---: | ---: |
| F438W | 20.000 | 2,77% | 1,77% | 0,03165 px |
| F438W | 200.000 | 2,91% | 0,89% | 0,01724 px |
| F606W | 20.000 | 3,47% | 2,68% | 0,03457 px |
| F606W | 200.000 | 3,43% | 1,76% | 0,02388 px |
| F814W | 20.000 | 3,64% | 1,73% | 0,02971 px |
| F814W | 200.000 | 3,70% | 1,02% | 0,01061 px |

Il cambiamento riduce il P90 per tutte le combinazioni. A 200.000 elettroni solo F438W soddisfa la soglia sintetica dell’1%. F606W resta a 1,76%, in linea con il controllo precedente a centro esatto, pari a 1,76%. Il confronto usa le quattro fasi sintetiche già usate nella prova di interpolazione e non attesta la generalizzazione ad altre fasi o alle osservazioni P330E. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 755f87bcc904b6c49ddf30f2aa6d18bd89ac224ad04e89421670121189658096 |
| Programma | a1bf352440ffaf7e9e0b205504907d1bfc08723ad3b7cdc44ab450856be010fe |
| Verifica appaiata | 98c1daee19f7dee1f56af84d16c87810f0a02e7d3e149c950e4b1eaa66fcbe09 |
| Ricevuta con 9.216 esiti, riprodotta da H: | 1efe02abb6d00230235713608c0fbc0999217821489e34a956c953bb215ae23a |
