# BKL-046 — Rumore delle ripetizioni e scala delle aperture in TV4

La misura usa gli stessi 40 FITS associati al [riallineamento della sfera](BKL-046-TV4-CLEAR1-RIALLINEAMENTO.md). In ogni gruppo di dieci fotogrammi, cinque coppie disgiunte sono formate prima con fotogrammi adiacenti, poi separando prima e seconda metà. Le due combinazioni riusano gli stessi fotogrammi. Le differenze divise per √2 misurano la varianza di una posa sotto l'ipotesi di rumori indipendenti tra le due pose. Sono state mantenute le cinque regioni interne e la sottrazione dell'overscan parallelo. Le pendenze fra due livelli sono state calcolate separatamente prima e dopo il riallineamento. La calibrazione TV4 pubblicata usa curve di trasferimento fotonico e riporta da 27,9 a 28,7 e⁻/DN per i quattro quadranti MRI. [Calibrazione strumentale Deep Impact](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/epoch-1/_documents/calibration_paper_draft.pdf)

| Accoppiamento e fase | 1 px | 2 × 2 px | 4 × 4 px | 16 × 16 px |
| --- | ---: | ---: | ---: | ---: |
| Adiacenti, prima | 30,50 | 29,37 | 28,64 | 25,18 |
| Adiacenti, dopo | 30,78 | 29,32 | 30,22 | 33,99 |
| Separati, prima | 30,66 | 29,64 | 29,13 | 34,44 |
| Separati, dopo | 30,85 | 29,74 | 29,54 | 24,94 |

I valori sono rapporti esplorativi in e⁻/DN tra la differenza di segnale e la differenza di varianza a due livelli, al centro del rivelatore. Su tutte le regioni il valore per singolo pixel varia da 30,08 a 31,66 e⁻/DN. Queste pendenze riguardano due sole durate e una sola sessione. Il confronto mostra quanto la stima dipenda dalla scala e dal campionamento.

A 16 × 16 px la varianza delle somme nella regione centrale è fra 1,13 e 1,35 volte quella attesa da pixel indipendenti, usando le mediane dei gruppi. Per il controllo, ho ricalcolato la prima coppia adiacente di ciascun gruppo e permutato 24 volte la posizione dei residui, conservandone i valori. Il rapporto mediano dopo permutazione è fra 0,98 e 1,01. Il controllo mostra che l'ordine spaziale contribuisce alla varianza nell'esempio. Il contributo fisico delle correlazioni e il guadagno assoluto richiedono più livelli, un controllo di lettura indipendente e repliche in altre condizioni.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro delle differenze appaiate e replay | 80a099a7a6f4db654496fad8ddb0b22a924d86282bcfa25d5fec84461d397256 |
| Riscontro delle aperture e replay | 15fd97a74c7ddda19e7311e45f2986f272fb8038fbdd7eddab5ee72bc8f02935 |
| Archivio riletto su H: | 7985666a775971a10e3b137bad35bc293d9d7f49ab40f8a36a5f40383a8888c9 |
| Archivio dipendente dei FITS | d6d5e0b68f7b5c4f896d8d30a9569ad9afc24020e4f34aeb44cf4a8d92ea9a7a |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
