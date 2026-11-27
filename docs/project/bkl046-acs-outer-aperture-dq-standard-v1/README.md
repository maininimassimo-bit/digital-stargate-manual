# BKL-046 · Anelli ACS esterni con supporto DQ incompleto

Sono state rilette le dodici pose archiviate di GD71 e GD153. Il calcolo riproduce i tassi precedenti dove l'apertura era pienamente supportata. Per i pixel esclusi, usa il minimo e il massimo dei pixel ammessi a raggio simile. Mantiene centri, mappa d'area, fondo e stati DQ originali. Le 51 prove con maschere ruotate nelle due bande strette contengono tutte il valore noto dei pixel trattenuti. Sono controlli interni alle stesse pose.

| Sorgente | Intervallo F658N/F660N a 15 px | Intervallo a 20 px |
| --- | ---: | ---: |
| GD71 | 2,53695–2,54286 | 2,51659–2,52662 |
| GD153 | 2,56442–2,56978 | 2,54967–2,55576 |

I valori Gaia fissati sono 2,63839 e 2,64475. A 20 px superano il bordo superiore diagnostico rispettivamente del 4,42% e del 3,48%. Per entrambe le stelle la forchetta a 20 px scende rispetto a quella a 15 px. Allargare l'apertura nei limiti osservabili con questo metodo non avvicina il rapporto alla previsione Gaia.

Le forchette sono variazioni empiriche nel modello di riempimento. Le aperture originariamente escluse conservano il proprio stato. Rimangono aperti il fondo fuori dall'anello, la CTE, la correzione a infinito e una verifica di calibrazione indipendente. Nessuna chiusura scientifica.

Per riprodurre passare protocollo, manifest FITS GD71 e GD153, riscontri di crescita delle due stelle, confronto con Gaia, mappa d'area, directory delle dipendenze ACS e nuovo percorso di uscita. I FITS sono letti accanto ai rispettivi manifest.
