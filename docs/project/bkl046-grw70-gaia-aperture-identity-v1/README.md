# BKL-046 · Verifica astrometrica Gaia delle pose GRW+70°5824

La verifica ripete sulle stesse 12 pose il limite di quattro pixel, le aperture da 5 e 10 pixel e i controlli DQ del protocollo precedente. Cambia la sola posizione celeste iniziale. Ho incrociato la posizione CALSPEC con Gaia DR3, propagato il moto proprio al centro temporale di ciascuna esposizione e applicato la parallasse geocentrica. Il controllo conserva anche le soluzioni senza parallasse e con velocità radiale nulla. [Posizione e velocità radiale CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec) · [Gaia DR3 presso ARI](https://gaia.ari.uni-heidelberg.de/singlesource.html)

La sorgente Gaia DR3 `1686708050268594944` è l'unica delle due sorgenti della query compatibile con posizione ed intervallo di magnitudine fissati. La posizione propagata a J2000 dista 0,00087 secondi d'arco dalla posizione CALSPEC arrotondata. La correzione geocentrica sposta il centro previsto di 0,86–0,93 pixel rispetto alla sola propagazione baricentrica. Il termine legato alla velocità radiale incide per meno di 0,001 pixel nelle pose esaminate.

| Esito | Coordinate negli header | Gaia con parallasse geocentrica |
| --- | ---: | ---: |
| Scarto del picco sopra quattro pixel | 7 | 6 |
| DQ nel nucleo | 1 | 3 |
| Supporto insufficiente | 4 | 3 |
| Aperture complete a entrambi i raggi | 0 | 0 |

Cambiano i casi ammessi al controllo DQ. Sei pose che prima non superavano il limite sul picco ora passano. Cinque delle pose che lo superavano prima ora vengono respinte. In `ibbszj`, tutte e tre le bande permettono la misura a 5 pixel, mentre nessuna soddisfa il supporto a 10 pixel. I tre colori misurati a un solo raggio sono conservati nel JSON per diagnosi. Nessuna visita consente quindi il confronto cromatico fra aperture richiesto.

La previsione usa il centro della Terra e il WCS originale dei FLC. Rimangono fuori la posizione orbitale di HST, un fit astrometrico del campo e l'incertezza cromatica su più visite. L'alias `WD2309+105` nella ricerca precedente non identificava GRW+70°5824, il cui nome WD è `WD1337+705`. Tutti i 1.559 record restituiti per la ricerca precedente portavano comunque il nome `GRW+70D5824`. I conteggi e la coorte archiviati restano validi. [Verifica originale](../bkl046-three-independent-wfc3-calibrators-v1/README.md)

Per ripetere, passare a `misura.py` questo kit, il kit originale estratto, la directory con Astropy 7.2.0 e NumPy 2.3.5 e un nuovo file di risultato. Zero avvii PixInsight e zero chiusure scientifiche.