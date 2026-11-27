# Varianza temporale dei flat Bayer di M8–M20

Per BKL-046 sono state rilette 14 pose flat e 14 dark brevi della ZWO ASI2600MC Pro, tutte da 3 s. Il protocollo usa sette coppie cronologiche disgiunte, 35 riquadri e le quattro parità Bayer. Il fondo e la maschera dei pixel caldi derivano dalle coppie di stima. Per ogni coppia, il rapporto d’illuminazione è stimato sui riquadri di stima e applicato anche ai riquadri riservati. Il modello affine della varianza è stimato sulle quattro coppie e sui 18 riquadri di stima. La verifica usa le tre coppie rimanenti e gli altri 17 riquadri.

| Parità | P90 errore relativo, modello costante | P90 errore relativo, modello con segnale | Varianza mediana flat / dark breve (ADU²) |
| --- | ---: | ---: | ---: |
| R | 4,88% | 3,85% | 24.799 / 29,4 |
| G1 | 7,02% | 5,67% | 116.793 / 29,3 |
| G2 | 8,06% | 5,43% | 116.895 / 32,3 |
| B | 7,57% | 5,10% | 105.768 / 31,6 |

Il modello con il segnale migliora la previsione nelle quattro parità. Escludendo a turno una coppia di stima, la pendenza del G2 varia da 3,72 a 5,62 ADU. Le intercette del verde e del blu sono negative quando il modello è extrapolato a segnale zero. Il disegno confronta la varianza dominante nei flat con quella dei dark brevi e sfrutta la variazione spaziale del segnale a un solo tempo di posa. Per qualificare guadagno, regime misto e incertezza fisica serve una serie controllata su livelli d’illuminazione distinti.

Per replicare eseguire `misura.py <protocollo.json> <directory-calibratori> <pacchetti-Python> <nuovo-riscontro.json>`. Il calcolo verifica gli SHA-256 degli archivi e delle singole pose. L’elaborazione è offline.
