# BKL-046 · Saturazione del nucleo F606W di G191B2B

Due pose ACS/WFC F606W del programma 10054, entrambe WFC1-1K, chip 1 e amplificatore B, hanno un solo pixel con flag di saturazione del CCD (DQ 256). Il massimo RAW si allinea al massimo FLT con offset (0, 0) e correlazione superiore a 0,99996 sulla finestra priva del nucleo. I valori RAW sono 42.716 e 42.761 DN. Il FLT non contiene flag DQ 2048. Questi riscontri individuano la saturazione del CCD riportata da CALACS. La mappa SATUFILE indicata negli header non è stata ricalcolata né applicata in questo studio. [Passi di calibrazione e significato dei flag](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

Esclusione del solo pixel centrale, percentuale della somma registrata dopo correzione PAM e sottrazione del fondo, a parità di maschera sugli altri pixel.

| Sorgente | 3 px | 5 px | 10 px |
| --- | ---: | ---: | ---: |
| G191B2B, due pose | 17,05–17,13% | 15,40–15,48% | 14,61–14,71% |
| GD71, due controlli | 15,66–15,99% | 13,95–14,27% | 13,24–13,53% |
| GD153, due controlli | 18,62–20,07% | 16,95–18,27% | 16,11–17,39% |

L'annulus a 4–8 px di G191B2B include un altro pixel non ammesso dalla maschera in entrambe le pose, perciò il confronto simmetrico delle ali è escluso su G191B2B. I quattro controlli mostrano quanto pesa la rimozione del proprio picco anche con nucleo non saturo. La percentuale misura la differenza fra due somme registrate. La quantità di carica persa e il flusso vero del nucleo non sono determinati. La configurazione scelta non consente di trasferire un fattore correttivo fra le stelle. Il requisito scientifico rimane aperto.

Per ripetere eseguire `verifica.py` con, nell'ordine, il percorso del runtime Astropy, il protocollo, le directory dei RAW, dei FLT di G191B2B, dei FLT di GD71 e dei FLT di GD153, il file PAM e un nuovo file di uscita. I nomi e gli SHA-256 sono fissati nel protocollo, i prodotti HST sono scaricabili tramite i rispettivi identificativi MAST. La copia privata su H: contiene anche tutti gli input per la ripetizione. [Archivio MAST HST](https://mast.stsci.edu/)
