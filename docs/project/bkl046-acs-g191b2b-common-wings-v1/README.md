# BKL-046 · Ali F606W su pixel comuni

Ripetizione diagnostica dopo il riscontro sul nucleo saturo di G191B2B. Le sei pose ACS/WFC del programma 10054 usano gli stessi offset interi dal picco. La maschera comune esclude tutti i pixel scartati da almeno una posa e tutte le loro rotazioni e riflessioni. Nell'anello 4–8 px conserva 144 pixel su 152. In entrambe le pose di G191B2B viene scartato il pixel all'offset (4, −3), con DQ 16. Nell'anello 6–10 px restano 208 pixel su 208. [Flag di qualità CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

La statistica è la differenza fra le somme delle strisce lungo Y e lungo X, divisa per la somma dell'intero anello. Con strisce di semiampiezza 2 px e fondo stimato fra 15 e 22 px, si ottengono i seguenti intervalli sulle pose replicate.

| Sorgente | 4–8 px | 6–10 px |
| --- | ---: | ---: |
| GD153 | 7,23–7,95% | 2,13–2,37% |
| G191B2B | 9,18–9,34% | 4,40–4,74% |
| GD71 | 10,14–11,21% | 6,01–6,15% |

I valori di G191B2B rimangono compresi fra le due stelle di controllo in tutte le 12 combinazioni di anello, stima del fondo e ampiezza della striscia. La differenza fra le ali lungo i due assi è quindi osservabile anche nei controlli non saturi. Questo confronto descrittivo non separa l'effetto della fase subpixel, della PSF, dell'epoca e dell'eventuale carica ridistribuita. Il recupero del nucleo e il requisito scientifico restano aperti.

Per ripetere, eseguire `verifica.py` con il runtime Astropy, questo protocollo, la directory estratta dell'archivio dello studio precedente e un nuovo file di uscita. Il codice verifica gli hash del protocollo e del rapporto precedenti e quelli dei FITS e della mappa PAM. [Studio precedente e impronte dei prodotti MAST](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/c4ee655854ff22b6a4d7917e5341fe48f74dfc36/docs/project/bkl046-acs-g191b2b-saturation-diagnostic-v1)
