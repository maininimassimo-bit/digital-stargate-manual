# BKL-046 · Riferimenti spaziali sui dark reali di IC 1805

Si verificano 17 dark Canon a ISO 800 e 60 s. Da ogni posa si ricava l'offset di ciascuna parità RGGB usando le due strisce mascherate sinistre. Sei riquadri da 64 × 64 distribuiti sul sensore stimano la superficie quadratica. Sei riferimenti allineati hanno rango 3 e non definiscono il modello a sei coefficienti. Nel controllo sintetico, i sei riferimenti distribuiti recuperano una quadratica nota.

L'errore viene misurato sulle mediane di 36 riquadri separati per posa. Si confrontano il solo offset, la superficie stimata dai sei riquadri dello stesso dark e la superficie comune stimata esclusivamente dai dark del gruppo temporale alternato opposto. Il riferimento ricavato dallo stesso dark rappresenta una prova di disegno spaziale. La trasferibilità temporale è misurata solo col gruppo opposto.

| Parità | P90 errore assoluto, solo offset | P90, superficie per dark | P90, superficie dal gruppo opposto |
| --- | ---: | ---: | ---: |
| R | 2,00 ADU | 2,97 ADU | 1,79 ADU |
| G1 | 2,00 ADU | 2,85 ADU | 2,18 ADU |
| G2 | 2,00 ADU | 3,63 ADU | 2,63 ADU |
| B | 2,00 ADU | 3,46 ADU | 3,11 ADU |

La superficie per dark peggiora il P90 in tutte le parità. Quella trasferita riduce il bias mediano rispetto al solo offset, ma migliora il P90 soltanto nel rosso. Il rango completo dei sei riferimenti distribuiti non garantisce un miglioramento sui riquadri esclusi. Il test riguarda il contributo additivo del rivelatore in questa serie di dark. Restano aperti la separazione dal cielo illuminato, l'accoppiamento a ISO 100 dei flat e la replica con altre acquisizioni. Zero master salvati, zero chiusure scientifiche e zero avvii PixInsight.

SHA-256 della ricevuta `e967c80397d3ec42e2211114386646323021a7c8292f2fa84d44d2d539841b43`.
