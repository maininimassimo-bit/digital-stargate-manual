# BKL-046 · Provenienza di BlindSolver e Blind Solver 2000

La matrice v601 registra `src/scripts/BlindSolver2000.js` con la dichiarazione di Seti Astro e un digest congelato. Le due copie pubbliche dell'autore usano la stessa dichiarazione e contengono un riferimento all'API Astrometry.net. Entrambe hanno uno SHA-256 diverso dal digest della matrice, anche normalizzando terminatori di riga e BOM. I byte esatti della copia storica restano da recuperare. [Download Seti Astro](https://www.setiastro.com/pi-scripts) · [Sorgente Seti Astro a revisione fissa](https://github.com/setiastro/pixinsight-updates/blob/a357ba4ca7c7d27a3920d71abf9b372f50d5e57f/blindsolver2000.js)

L'installazione 1.9.6 sulla VM contiene `src/scripts/BlindSolver/BlindSolver.js`. Dichiara `Astrometry > BlindSolver` e include un motore che istanzia `BlindAstrometricSolver` con il percorso dell'indice locale. Il riscontro lega queste osservazioni ai digest del sorgente e alle righe di dichiarazione e chiamata.

Le evidenze supportano due voci distinte. L'identità della copia storica, l'equivalenza funzionale e le soglie scientifiche restano aperte. Il registro canonico conserva la voce storica. Il nuovo script resta una voce candidata al perimetro.

Per riprodurre il confronto, fornire al verificatore la matrice v601 congelata, la directory dell'installazione e una directory con i due sorgenti pubblici. Salvare il sorgente del commit come `setiastro-commit.js` e il download singolo come `setiastro-download.js`. I digest attesi sono nel riscontro. Il verificatore legge i file e produce un nuovo JSON.
