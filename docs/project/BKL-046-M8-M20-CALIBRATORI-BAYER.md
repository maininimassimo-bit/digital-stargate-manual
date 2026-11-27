# BKL-046 · Ripetibilità dei calibratori Bayer di M8 e M20

Verificati 60 FITS della serie Colmic, 15 per ciascun gruppo. Tutti riportano ZWO ASI2600MC Pro, 6248 × 4176, binning 1 × 1, RGGB, gain 100 e offset 50. Luci e dark sono da 180 s. Flat e file etichettati `Bias` sono da 3 s, perciò questi ultimi sono trattati come dark-flat nel confronto. La massima differenza di temperatura riportata è 0,3 °C fra luci e dark e 0,5 °C fra flat e dark-flat, entro il limite diagnostico fissato. I gruppi sono stati acquisiti in date diverse. [Serie di Colmic e descrizione dei calibratori](https://siril.org/tutorials/tuto-scripts/index.html)

In ciascun gruppo di calibrazione, i primi 14 frame ordinati per data formano due gruppi alternati da sette. Su nove riquadri fissi di 128 × 128 pixel, si sottrae la mediana dei dark-flat alla mediana dei flat e si normalizza ogni parità Bayer sulla mediana del riquadro centrale. La differenza di risposta relativa confronta il rapporto fra le due stime con 1.

| Parità | Pixel campionati | P90 differenza assoluta del dark | P90 differenza relativa del flat | Riquadri con P90 del flat > 1% |
| --- | ---: | ---: | ---: | ---: |
| R | 36.864 | 4 ADU | 2,80% | 9/9 |
| G1 | 36.864 | 4 ADU | 1,59% | 9/9 |
| G2 | 36.864 | 4 ADU | 1,63% | 9/9 |
| B | 36.864 | 4 ADU | 1,65% | 9/9 |

La risposta flat non è replicata entro l'1% sul campione. Le differenze includono il rumore delle due stime, la normalizzazione e le variazioni fra frame. Il risultato non quantifica l'errore del flat calcolato con tutti i frame né quello sui flussi stellari finali. Da propagare separatamente l'effetto delle due calibrazioni sui flussi e sul rumore a pari scala. Zero master salvati, zero avvii PixInsight e zero chiusure scientifiche.

SHA-256 della ricevuta `65f914e2830af1c9152322c80970461c72bba7e9fdd9fe86f44b3069f9e8b5bc`.
