# BKL-046 · Stabilità delle aperture di 47 Tucanae rispetto alla registrazione

Per ciascuna delle 23 sorgenti già ammesse in 47 Tucanae ho proiettato il picco F606W nelle altre due bande. Ho ricalcolato la previsione con una traslazione mediana e con un fit affine dei residui, separatamente per chip e banda. Ogni fit esclude la sorgente valutata. La tabella riporta lo scarto mediano dal picco archiviato, in pixel, prima della ricentratura locale.

| Chip e banda | WCS originale | Traslazione mediana | Fit affine |
| --- | ---: | ---: | ---: |
| UVIS1 F438W | 0,373 | 0,118 | 0,666 |
| UVIS1 F814W | 0,430 | 0,196 | 0,659 |
| UVIS2 F438W | 0,543 | 0,084 | 0,468 |
| UVIS2 F814W | 0,452 | 0,139 | 0,430 |

La traslazione riduce lo scarto mediano sotto 0,2 pixel in entrambe le bande e su entrambi i chip. Tutte e tre le soluzioni trovano gli stessi picchi, mantengono le 23 sorgenti e riproducono esattamente i termini cromatici da 5 a 10 pixel. L'errore attribuito alla correzione tabulata rimane quindi lo stesso con queste due varianti di registrazione. [Risultato sulle curve di 47 Tucanae](../bkl046-wfc3-external-field-ee-v1/README.md)

Il picco archiviato è il riferimento interno della verifica. Il test riguarda esclusivamente sorgenti già ammesse nelle stesse tre esposizioni. Rimangono aperti l'astrometria assoluta, la verifica delle sorgenti respinte e il contributo di vicini più deboli. Nessuna prova PixInsight e nessuna chiusura scientifica.

Per replicare, passare a `misura.py` il protocollo, lo ZIP dei due campi, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato.