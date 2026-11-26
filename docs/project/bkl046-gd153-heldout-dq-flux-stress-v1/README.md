# BKL-046 · Effetto delle lacune DQ sul flusso di apertura di GD153

Ho ricalcolato il flusso originale di 20 aperture WFC3/UVIS1 integre a raggio 10 pixel. Alle aperture ho applicato le maschere DQ di altre visite, proiettate da due pose nello stesso filtro. Il programma nasconde i valori originali nei punti senza supporto prima di stimarli. I valori nascosti servono soltanto a calcolare l'errore. Nessun FITS è modificato.

Per ciascuna regola di copertura si ottengono 140 confronti. Nei casi con lacune nel nucleo di raggio 3 pixel, il 90° percentile dell'errore assoluto relativo è il seguente.

| Regola di copertura | Casi con lacune nel nucleo | Somma dei campioni rimasti | Riscalatura per area | Mediana per anello |
| --- | ---: | ---: | ---: | ---: |
| Pixel più vicino | 18 | 3,35% | 2,99% | 1,94% |
| Quattro pixel circostanti | 53 | 8,70% | 6,70% | 3,52% |

Con la mediana per anello, 14 dei 18 casi con lacune nel nucleo rientrano nell'1% usando il pixel più vicino. Con quattro pixel di supporto, rientrano 23 dei 53. I sottoinsiemi sono diversi. Anche il metodo con l'errore minore supera l'1% al 90° percentile in entrambi i sottoinsiemi.

La mediana usa soltanto i valori conservati in anelli larghi un pixel. L'analisi trattiene il fondo della posa di riferimento e riusa la stessa stella in tutte le coppie. I confronti misurano la risposta di tre stime alla rimozione controllata di campioni reali. Restano aperti il recupero su esposizioni danneggiate, la propagazione dell'incertezza, la variazione fra stelle e la prova nativa. Zero avvii PixInsight e zero chiusure scientifiche.

Per ripetere, passare a `misura.py` la directory del kit, la directory delle pose di riferimento, lo ZIP della fotometria verificata, la directory del rapporto geometrico, i due kit delle maschere, NumPy 2.3.5/Astropy 7.2.0 e un nuovo risultato. [Copertura delle coppie di pose](../bkl046-gd153-dither-dq-union-v1/README.md) · [Fotometria di riferimento](../BKL-046-WFC3-GD153-APERTURE-INDIPENDENTI.md)
