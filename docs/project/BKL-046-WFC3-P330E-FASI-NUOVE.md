# BKL-046 · Verifica su nuove fasi della centratura WFC3/P330E

La prova riusa senza modifiche il [programma a 1/32 di pixel](BKL-046-WFC3-P330E-CENTRO-FINE.md). Cambia le quattro coppie di fase e il seme del rumore. Ogni coordinata nuova è esattamente a metà tra nodi della griglia di fit. I piani di fuoco, le 24 maschere reali, il profilo di rumore e i livelli di segnale restano quelli della prova precedente.

| Banda | P90 con maschera, 20.000 e⁻ | P90 con maschera, 200.000 e⁻ | P90 precedente a 200.000 e⁻ |
| --- | ---: | ---: | ---: |
| F438W | 1,88% | 1,09% | 0,89% |
| F606W | 2,38% | 1,70% | 1,76% |
| F814W | 1,97% | 1,19% | 1,02% |

Tutte le combinazioni restano sopra l’1%. Il P90 di centratura con maschera è circa 0,02210 px in tutte le combinazioni, la distanza radiale fra il punto a metà in entrambe le coordinate e il nodo più vicino. Il risultato ad alto segnale per F438W della prova precedente non si conferma in questo secondo insieme. Cambiano congiuntamente fase e rumore, quindi il confronto fra i due insiemi non stima separatamente quei due effetti. Le immagini sono sintetiche. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | e210dcc75cc6d4a88a9225ab73b46192627ee04f48f29364a9d3a89f25922c7c |
| Programma | a1bf352440ffaf7e9e0b205504907d1bfc08723ad3b7cdc44ab450856be010fe |
| Verifica di protocollo e copertura | 6b925c597281b839cae927978133e2140ceee1a3b5e3cf41068ac9b77430e200 |
| Ricevuta con 9.216 esiti, riprodotta da H: | 247afa329fb2a545278cb4786c2639ba8aaf3e7f19cd3137ad9f7c8d170dc698 |
