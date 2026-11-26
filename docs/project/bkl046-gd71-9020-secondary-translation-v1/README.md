# BKL-046 · Traslazione astrometrica GD71 dal riferimento Gaia debole

La traslazione di ciascuna visita 9020 è stimata dai due centri del riferimento debole nelle sole pose F660N. GD71 resta fuori dal fit. Le due stime da pose separate differiscono di 0,0149 secondi d'arco in j8c103 e 0,0025 in j8c104. Le quattro predizioni GD71 nelle pose F658N tenute fuori dal fit hanno residui di 0,71–2,23 pixel, entro la soglia fissata di 3 pixel.

| Visita | Chip e amplificatore | F658N/F660N a 3 px | A 5 px | A 10 px |
| --- | --- | ---: | ---: | ---: |
| j8c103 | 1 / A | 2,613986 | 2,592099 | — |
| j8c104 | 2 / C | 2,570328 | 2,553704 | 2,531033 |

Ogni rapporto richiede due pose DQ ammesse per banda alla stessa apertura. Le visite restano separate. I rettangoli di ricerca del riferimento debole derivano dal controllo precedente, che aveva usato il candidato GD71. La traslazione ne esclude il centro e verifica la posizione fuori dal fit. Scala, rotazione e distorsione restano quelle del WCS di archivio. L'astrometria assoluta e la CTE richiedono ulteriori riscontri. Le misure sono diagnostiche e le esclusioni del protocollo originario conservano il loro esito.

Per ripetere passare protocollo, directory dei riscontri astrometrici, archivio FITS 9020, CSV Gaia, le due PAM, dipendenze ACS e un nuovo percorso di uscita. Nessuna chiusura scientifica o esecuzione PixInsight.
