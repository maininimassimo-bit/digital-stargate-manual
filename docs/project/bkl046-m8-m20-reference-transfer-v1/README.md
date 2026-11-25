# BKL-046 · Replica del fondo differenziale su M8/M20

Il criterio già fissato per IC 1805 è stato trasferito a 12 pose Bayer distinte dal primo studio sul fondo M8/M20. Le tre pose di riferimento sono la prima, la mediana superiore e l'ultima del campione ammissibile. Le altre nove sono tutte confrontate con ciascuna. Il fit affine degli spostamenti usa i coefficienti stellari di Huber archiviati e i residui P90 verificati per posa. Tutte e 12 rispettano il limite diagnostico di un pixel nativo. Il confronto usa 192 celle, con il 99,88% di campioni comuni validi.

| Sequenza e riferimenti | Coppie favorevoli con ognuno dei riferimenti | Pose favorevoli con tutti i riferimenti |
| --- | --- | --- |
| IC 1805, 2 / 17 / 35 | 14/24, 11/24, 20/24 | 6/24 |
| M8/M20, 1 / 8 / 13 | 0/9, 6/9, 0/9 | 0/9 |

Un confronto è favorevole quando il piano migliora la mediana assoluta di almeno il 10% rispetto al solo offset, senza aumentare il P90, in entrambe le partizioni spaziali. La dipendenza dal riferimento si ripete su un altro campo e un'altra camera. I tre riferimenti di ogni campo condividono le pose bersaglio. Il confronto copre due sequenze con il proprio supporto geometrico, esposizione e scala ADU. Non stima il livello vero di fondo e non autorizza a selezionare il riferimento che ha ottenuto l'errore più basso sullo stesso test. Un criterio di selezione va fissato e verificato su nuove sequenze. [Test IC 1805](../bkl046-ic1805-reference-transfer-v1/README.md)

Replica con Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Argomenti: cartella con protocollo, cartella con Brutes_180s.zip e riscontro-con-celle.json, ricevuta stellare riscontro.json, directory dipendenze e file di uscita. Zero esecuzioni PixInsight e zero chiusure scientifiche. [Sorgente delle pose](https://siril.org/tutorials/tuto-scripts/index.html)