# BKL-046 · Predizione di pixel reali nel nucleo WFC3/P330E

La prova usa i prodotti FLC del [campione DQ](BKL-046-WFC3-P330E-SUPPORTO-DQ.md). Su 24 esposizioni sono state elaborate le 23 respinte per DQ nel nucleo. L’esposizione esclusa per picco distante resta fuori dalla prova. Nelle 23 esposizioni, aperture circolari da 10 pixel forniscono solo campioni finiti e con DQ zero. In quattro turni, il fit usa tre gruppi definiti dalla parità delle coordinate del rivelatore e predice i pixel validi del gruppo restante nel nucleo 7 × 7. Ogni pixel del nucleo con DQ zero e valore finito entra in un solo gruppo di verifica.

Il fit stima ampiezza positiva e fondo costante con minimi quadrati non pesati e centro su griglia a 1/32 pixel. Il confronto usa gli stessi pixel e la stessa griglia per la selezione fra piani di indice pari e per la loro interpolazione. Per ogni esposizione si misura l’RMSE del nucleo sui pixel osservati e tenuti fuori dal fit, diviso per il picco osservato del nucleo. Il picco serve solo a normalizzare la metrica.

| Banda | Esposizioni | Pixel del nucleo predetti | RMSE mediana, discreto | RMSE mediana, interpolato | Migliorate / pari / peggiorate |
| --- | ---: | ---: | ---: | ---: | ---: |
| F438W | 8 | 367 | 10,88% | 10,38% | 3 / 3 / 2 |
| F606W | 7 | 322 | 13,32% | 13,26% | 3 / 3 / 1 |
| F814W | 8 | 368 | 9,08% | 9,12% | 2 / 4 / 2 |

In totale il modello interpolato migliora otto esposizioni, ne lascia dieci a pari esito e ne peggiora cinque. La metrica riguarda l’intensità dei pixel osservati, normalizzata al picco. È distinta dall’errore di flusso integrato delle prove sintetiche. La verifica separa i pixel entro ogni esposizione. Il trasferimento a visite indipendenti e il comportamento dove mancano i pixel restano da dimostrare. Nessun flusso di apertura o colore è stato stimato. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 5d4037cc6c273b0ca4a8a946fffe8c6a9a7f0d2d38e1ac207c2534099acc1742 |
| Programma | 2b38747e25e7560acb207a949d758b4c1b86b403e1aac5ef324f45c3ae2fd184 |
| Verifica | c87dbe1cffab9ebc5997dfeee21a5a8e74197f7fb45e97a04e81c6a0fad9f631 |
| Ricevuta, riprodotta da H: | 116a0dd52595ac7ffc6fd16ce725f90da3e8561359e56b032ab68d36f0b9fae6 |
