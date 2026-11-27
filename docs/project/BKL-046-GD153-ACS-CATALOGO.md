# GD153 · Copertura per amplificatore nei programmi ACS di monitoraggio

Per `FILTER_COLOR/2` è stata interrogata MAST senza filtro temporale per GD153, GD 153 e GD-153, ACS/WFC e filtri F435W, F606W e F814W. La risposta completa contiene 236 record, 140 HST e 96 HAP. I programmi rappresentati da record HST in tutti e tre i filtri sono 18. Questo conteggio riguarda il catalogo e include prodotti di associazione. [Archivio MAST HST](https://archive.stsci.edu/missions-and-data/hst) · [Piani di calibrazione ACS](https://www.stsci.edu/hst/instrumentation/acs/calibration/calibration-plans)

Sono state controllate per intero tre visite del monitoraggio ACS, su programmi distinti da 17661, il programma già studiato per i contrasti tra amplificatori. Per ciascuna delle nove associazioni è stata verificata la presenza di due membri RAW, due FLT con gli stessi identificativi, un CRJ e un prodotto ASN. Nei 18 header primari RAW sono stati confrontati identificativo, bersaglio, programma, filtro e `ASN_ID`.

| Programma | Visita | Associazioni per filtro | Header RAW verificati | Amplificatore e apertura |
| --- | --- | --- | ---: | --- |
| 16978 | jeuo02 | jeuo02010 · jeuo02050 · jeuo02020 | 6 | B · WFC1B-1K |
| 17341 | jf4i02 | jf4i02010 · jf4i02050 · jf4i02020 | 6 | B · WFC1B-1K |
| 17984 | jflp04 | jflp04010 · jflp04050 · jflp04020 | 6 | B · WFC1B-1K |

Queste visite sono candidate per un confronto temporale sullo stesso amplificatore. La selezione multiposizione deve comprendere dati ulteriori per verificare contrasti tra amplificatori. F435W ACS e F438W WFC3 sono passbande distinte e richiedono una previsione specifica per ogni risposta strumentale. L'audit riguarda catalogo, appartenenza e header primari. Non è stato qualificato alcun pixel per saturazione, DQ o supporto dell'apertura. Zero misure fotometriche ACS in questa verifica e zero chiusure scientifiche.

La copia su H: contiene la query, le risposte, gli estratti binari degli header primari e il verificatore. Il replay ha riprodotto il JSON byte per byte. Riscontro SHA-256 `3c8091954b1d0d1074f7a3141ffc5f4913bdb8c31ca215e5e2b00e3ebd6f21cc`. Archivio SHA-256 `38a5bd3b9a109a69346791cd008f8144593977480d7acea00a25c4a2c1c466d8`.
