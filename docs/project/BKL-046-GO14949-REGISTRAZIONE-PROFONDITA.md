# BKL‑046 · Registrazione GO14949 con pose da 40 e 150 secondi

Il confronto applica lo stesso stimatore dei centroidi e gli stessi criteri DQ alle quattro esposizioni ACS/WFC F606W. Usa gli abbinamenti già archiviati e le stesse tessere distinte per fit e verifica. L’intersezione con centroidi validi in tutte le pose contiene 223 delle 677 stelle iniziali. Di queste, 105 sono nelle tessere di verifica, 43 sul chip 1 e 62 sul chip 2. [Confronto precedente a pari profondità](BKL-046-GO14949-REGISTRAZIONE-GUIDA.md)

| Sorgente della previsione per B da 40 s | P90 traslazione chip 1 | P90 affine chip 1 | P90 traslazione chip 2 | P90 affine chip 2 |
| --- | ---: | ---: | ---: | ---: |
| A da 40 s | 0,053 px | 0,052 px | 0,106 px | 0,106 px |
| C da 150 s | 0,090 px | 0,056 px | 0,081 px | 0,063 px |
| D da 150 s | 0,075 px | 0,059 px | 0,086 px | 0,082 px |
| Media delle due proiezioni da 150 s | 0,083 px | 0,065 px | 0,080 px | 0,072 px |

Tutti i P90 puntuali dei riferimenti da 150 s rientrano nel limite di 0,1 pixel nell’intersezione valida. Con la sola traslazione, alcuni intervalli descrittivi ricampionati superano la soglia. Per la media da 150 s con fit affine, gli intervalli sono 0,044–0,069 px sul chip 1 e 0,044–0,092 px sul chip 2. Sul chip 1, la posa A da 40 s resta più vicina alla posa B secondo questo indicatore.

I casi rifiutati per qualità restano nella ricevuta. Il confronto riguarda nuclei stellari validi e pose con geometrie diverse. Non attribuisce le differenze alla sola durata di esposizione. Resta aperta la verifica della ricomposizione su nuclei saturi e con elaborazione nativa. L’asse `SATURATION_BLEND/4` resta aperto.

SHA‑256 della ricevuta `f3b63a2933916551da70054a58d05364b49bd5833380fb68e51fa154a9ac1023`.
