# BKL-046 · Stima del fuoco e del centro con le maschere P330E

Il test confronta una PSF standard e una scelta del fuoco a partire dai soli pixel validi. Usa le 24 maschere P330E e le [librerie PSF WFC3 già archiviate](BKL-046-WFC3-P330E-STRESS-PSF.md). Il fit varia il centro su una griglia a quarti di pixel, stima ampiezza e fondo e, nel secondo metodo, sceglie uno dei piani di fuoco di indice pari in base al residuo.

I profili di verifica interpolano piani adiacenti al 35% e usano fasi assenti dalla griglia di fit. Ogni caso ha rumore poissoniano e rumore di lettura sintetici. I fit con e senza maschera condividono la stessa realizzazione del rumore. Il confronto comprende due livelli di segnale, 20.000 e 200.000 elettroni nell'apertura, e conserva 6.656 esiti di fit.

| Banda | P90 del fit con maschera, PSF standard | P90 del fit con maschera, fuoco stimato |
| --- | ---: | ---: |
| F438W | 13,19–13,30% | 6,15–6,75% |
| F606W | 20,42–20,43% | 7,55–8,15% |
| F814W | 22,14–22,22% | 7,33–7,85% |

La scelta del piano di fuoco riduce l'errore in tutte le bande, ma supera il riferimento dell'1% per entrambi i livelli di flusso. Il P90 dell'errore di centratura è circa 0,177 pixel, coerente con la distanza minima nelle due coordinate fra le fasi sintetiche e i nodi di fit. Il test non separa l'errore di discretizzazione del fuoco da quello di centratura. Il controllo con profilo presente esattamente nella griglia recupera il flusso e il nodo di origine entro la tolleranza numerica.

I risultati caratterizzano profili e rumore simulati con maschere reali. I fit non ripristinano pixel o misurano il flusso delle visite di P330E. `FILTER_COLOR/2` e `FILTER_COLOR/3` restano aperti. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `453d14a19e43ed0401b66c927618641afd0133310a350a08a0bc36833ed363ce` |
| Programma | `0f23aea37c254ad991627882f40c667ef088feaab36c5a967ffef7a53c73bc3e` |
| Ricevuta per caso | `cdd74b9fc471de5678d89e5b9233791ce49bd85f8fe945b1bd04f4c50637c002` |
