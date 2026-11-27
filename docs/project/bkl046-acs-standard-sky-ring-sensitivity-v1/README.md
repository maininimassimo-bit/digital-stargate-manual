# BKL-046 · Sensibilità all'anello di fondo per GD71 e GD153

Il controllo riproduce il riscontro precedente per le otto pose delle due bande strette. Rilegge i FITS con gli stessi centri, PAM e criteri DQ. Per il fondo confronta la mediana originale con quella di tre anelli alternativi e con le quattro mediane ottenute omettendo a turno un quadrante. Il cambiamento della mediana trasla entrambi gli estremi di flusso della stessa quantità per pixel. Conserva quindi anche l'intervallo empirico per i pixel esclusi.

| Sorgente | Aumento ancora necessario a 10 px | A 15 px | A 20 px |
| --- | ---: | ---: | ---: |
| GD71 | 3,04% | 3,64% | 4,21% |
| GD153 | 2,29% | 2,71% | 3,12% |

Gli aumenti sono calcolati dal bordo superiore della forchetta più favorevole, che permette di scegliere una mediana diversa per ogni posa. Nessuno scenario include il rapporto Gaia. Il risultato misura la sensibilità alle mediane provate. Gradienti non modellati, sistematiche CTE e il riporto ad apertura infinita restano aperti. Le aperture escluse conservano il proprio stato e la forchetta non fornisce un'incertezza calibrata.

Per riprodurre passare protocollo, directory del precedente controllo degli anelli, i due manifest FITS, i due riscontri di crescita, il confronto delle aperture con Gaia, PAM, directory delle dipendenze e un nuovo file di risultato.
