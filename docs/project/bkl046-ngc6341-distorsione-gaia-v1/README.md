# BKL-046 · Effetto della distorsione sui centroidi NGC 6341

Il confronto riproduce il rapporto del pilot Gaia sulle pose HST/ACS da 5 e 90 s. Per ciascun chip mantiene le stesse coppie di calibrazione nelle tessere pari da 256 pixel e le stesse identità Gaia nelle tessere dispari. Rimuove i componenti di distorsione dalla WCS strumentale e adatta di nuovo un affine alle sole coppie di calibrazione originali.

| Posa | Chip | Coppie di verifica | P90 con distorsione | P90 senza distorsione |
| --- | --- | --- | --- | --- |
| 5 s | 1 | 44 | 0,536 px | 24,557 px |
| 5 s | 2 | 71 | 0,470 px | 19,010 px |
| 90 s | 1 | 44 | 0,536 px | 24,249 px |
| 90 s | 2 | 71 | 0,477 px | 17,780 px |

Nessuna delle coppie fissate resta entro un pixel dopo la rimozione della distorsione. Le identità provengono dal pilot originale, che richiedeva una corrispondenza univoca entro un pixel con la distorsione attiva. Il risultato è quindi condizionato alle corrispondenze selezionate e non misura completezza o falsi positivi su tutta la coorte. Le due pose condividono il modello strumentale. I risultati misurano l'effetto della rimozione della distorsione per questo campo e non definiscono soglie di accettazione di BlindSolver.

Per riprodurre il rapporto usare `confronto.py` con, nell'ordine, lo script e il rapporto congelati del pilot, la directory FITS e Gaia, il JSON congelato dei centroidi, la directory dei pacchetti Python e un nuovo percorso di uscita. Il confronto usa Astropy 7.2.0 e NumPy 2.3.5.
