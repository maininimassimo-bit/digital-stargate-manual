# GD153 · Confronto tra i colori WFC3 e CALSPEC

Il riferimento sintetico usa il composito GD153 `gd153_stiswfcnic_004.fits`, il modello `gd153_mod_012.fits` e le tabelle della risposta totale del chip WFC3/UVIS1. Le tabelle sono riferite al 26 giugno 2009. Il calcolo interpola spettro e throughput sulla griglia unione, integra il flusso con peso fotonico proporzionale a λ × throughput e ne ricava rate atteso e colori ST. Tutti e tre i passband risultano coperti dallo spettro. Nel composito tutta l'area fotonica integrata ricade, alla precisione del calcolo, su campioni con `TOTEXP > 0`. [CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec.html) · [Throughput WFC3](https://www.stsci.edu/hst/instrumentation/wfc3/performance/throughputs) · [Area di raccolta HST in SYNPHOT](https://ssb.stsci.edu/doc/stsci_python_x/pysynphot.doc/html/observation.html)

Sono confrontate tutte e quattro le terne che nel riscontro precedente passano il taglio di 0,05 giorni con raggio 10 pixel, anello 75–125 pixel, stima robusta della moda e correzione di encircled energy. Le terne appartengono a due visite.

| Colore ST | Atteso CALSPEC, mmag | Osservato meno atteso, mmag |
| --- | ---: | ---: |
| F438W−F606W | −1187,49 | +1,93 a +16,33 |
| F438W−F814W | −2489,00 | −11,34 a +5,06 |
| F606W−F814W | −1301,51 | −13,28 a −4,89 |

Lo spettro composito e il modello differiscono di meno di 1 mmag in ogni colore sintetico. I rate osservati corretti per encircled energy differiscono dal composito tra −1,355% e +0,203% sulle 12 misure. PHOTFLAM degli header moderni differisce dalla risposta a flusso piatto calcolata dalle curve di riferimento tra −0,089% e +0,227%. La procedura non applica una correzione aggiuntiva per la differenza di epoca tra curve e immagini. I residui non includono un bilancio d'incertezza con covarianze CALSPEC, throughput e apertura.

Il confronto aggiunge un riferimento spettrale per il bersaglio. La calibrazione UVIS usa standard CALSPEC tra cui GD153 e la correzione storica di encircled energy proviene dallo stesso programma osservativo. Per questo motivo il grado di indipendenza è limitato. L'asse `FILTER_COLOR/2` resta aperto. Zero avvii nativi e zero chiusure scientifiche. [Calibrazione fotometrica UVIS](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration/uvis-photometric-calibration.html)

Replay byte per byte dagli archivi su H:. Riscontro SHA-256 `9cd0ef27c3c0a400e026f5dadab16ec1aa3e9c4177fd1f4077cc8df4abe38efc`. Archivio SHA-256 `d776352e0d90198a97dabc9c97a741f4f5ece4c626e899f8b1b1a3f6099f325f`.

[Cohort e misura di apertura](BKL-046-WFC3-GD153-APERTURE-INDIPENDENTI.md).
