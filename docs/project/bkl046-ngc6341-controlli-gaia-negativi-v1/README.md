# BKL-046 · Corrispondenze accidentali nei controlli Gaia di NGC 6341

Il test riproduce il pilot sulle due pose ACS da 5 e 90 secondi. Riusa la calibrazione delle tessere pari e tutti i centroidi archiviati nelle tessere dispari. A calibrazione fissa trasla rigidamente la previsione del catalogo di 8, 16 o 32 pixel in otto direzioni e conta le coppie univoche entro un pixel.

| Posa | Chip | Centroidi | Coppie senza traslazione | Controlli con almeno una coppia |
| --- | --- | ---: | ---: | ---: |
| 5 s | 1 | 341 | 44 | 2 su 24 |
| 5 s | 2 | 395 | 71 | 0 su 24 |
| 90 s | 1 | 341 | 44 | 2 su 24 |
| 90 s | 2 | 395 | 71 | 0 su 24 |

Ciascuno dei quattro controlli non vuoti accetta una sola coppia. Allargando il raggio da 1 a 2 pixel si aggiunge una coppia per posa sul chip 1. Nessun centro accettato sia con il raggio di riferimento sia con un raggio alternativo cambia identità. I dettagli per gli altri raggi sono nel JSON.

I controlli condividono campo, strumento e catalogo. Misurano le associazioni accidentali per queste traslazioni fisse. La probabilità di falsi positivi per le corrispondenze reali e la completezza richiedono verità di riferimento indipendente. Nessun esito viene esteso alla validazione nativa di BlindSolver.

Eseguire `controlli.py` con lo script e il rapporto congelati del pilot, la directory FITS e Gaia, il JSON dei centroidi, la directory dei pacchetti Python e un nuovo percorso di uscita.
