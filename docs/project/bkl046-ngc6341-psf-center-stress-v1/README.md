# BKL-046 · Sensibilità al centro di verifica in NGC 6341

Ho riprodotto i 1.472 confronti del test PSF NGC 6341. In ciascuna direzione, le forme restano quelle scelte dalla posa di stima. Ho spostato solo il centro del modello nella posa valutata di ±0,125 pixel lungo X o Y, mantenendo aperture, campioni, qualità e coordinate del fondo. I quattro spostamenti e il riferimento usano gli stessi 1.466 confronti misurabili. [Confronto di partenza](../bkl046-ngc6341-psf-zone-holdout-v1/README.md)

Il vantaggio mediano appaiato dell’angolo proprio rispetto a quello di zona rimane positivo per tutti gli spostamenti su entrambi i CCD e in entrambe le direzioni di stima. Nei 16 confronti con centro perturbato varia da **+0,58 a +3,16 punti percentuali**. Il modello con angolo proprio continua ad avere un guadagno mediano sul circolare soltanto sul CCD 1 quando la posa di stima è quella da 90 s.

I quattro spostamenti sono perturbazioni fissate. Il confronto quantifica la sensibilità su due pose e conserva tutti i sei casi non misurabili del rapporto precedente. Restano da verificare l’incertezza del centro con un riferimento indipendente, gli altri campi e l’operatore nativo.

Usare Python 3.12, NumPy 2.3.5 e Astropy 7.2.0 con `OPENBLAS_NUM_THREADS=1`. Passare a `misura.py` il protocollo, la directory estratta del kit NGC 6341 precedente, la directory delle dipendenze e una nuova directory di uscita.