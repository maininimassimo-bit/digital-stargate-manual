# BKL-046 · Limite della soluzione astrometrica affine su NGC 6341

Sulle tre pose HST/ACS GO-9453, una trasformazione affine sul piano tangente è stata adattata a 81 punti per chip della WCS strumentale A. I 64 punti intermedi per chip sono rimasti fuori dall'adattamento. La proiezione indipendente è stata confrontata con la proiezione TAN di Astropy. Il controllo sintetico affine è rimasto sotto 10⁻⁸ pixel.

| Chip | P90 sui punti esclusi | Massimo sui punti esclusi |
| --- | --- | --- |
| 1 | 17,49 px | 30,76 px |
| 2 | 16,15 px | 26,29 px |

Le tre pose condividono il modello di distorsione strumentale. La loro concordanza verifica la ripetibilità del confronto su quel modello. Le distanze misurano la perdita geometrica dell'approssimazione affine nell'intero campo verificato. Una futura prova di BlindSolver dovrà distinguere la localizzazione iniziale del campo dalla precisione WCS dopo modellazione della distorsione. I valori non sono soglie di accettazione e non derivano da centroidi stellari.

Per riprodurre il calcolo, fornire a `verifica-affine.py` la directory dei tre FITS congelati, la directory dei pacchetti Astropy 7.2.0 e NumPy 2.3.5 e un percorso nuovo per il rapporto. Gli SHA-256 dei FITS sono nel codice e nel risultato.
