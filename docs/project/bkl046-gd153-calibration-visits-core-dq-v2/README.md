# BKL-046 · Sei visite WFC3 di GD153, selezione e qualità del nucleo

I programmi HST 14384, 14883 e 14992 forniscono 18 associazioni pubbliche e 36 prodotti FLC CALWF3. Ho verificato tutte le esposizioni. Le 12 terne per visita, chip e dither rispettano il limite di 0,05 giorni fra le tre bande. Nessuna terna supera i controlli di fotometria a 5 e 10 pixel. [Piano di calibrazione WFC3](https://www.stsci.edu/hst/instrumentation/wfc3/calibration-plan)

| Visita | Chip | FLC | Flag di esposizione rifiutato | DQ nel nucleo | Apertura o fondo rifiutati |
| --- | ---: | ---: | ---: | ---: | ---: |
| id2406 | UVIS1 | 6 | 6 | 0 | 0 |
| id2407 | UVIS2 | 6 | 0 | 6 | 0 |
| iddn05 | UVIS1 | 6 | 0 | 6 | 0 |
| iddn06 | UVIS2 | 6 | 0 | 6 | 0 |
| idor02 | UVIS1 | 6 | 0 | 3 | 3 |
| idor03 | UVIS2 | 6 | 0 | 6 | 0 |

Le sei pose di id2406 sono puntate, ma l'header riporta `TDF-DOWN AT EXPSTART`. Fra i 27 rifiuti DQ nel nucleo, 24 presentano il bit 16 (pixel caldo), 17 il bit 1024 (trappola di carica) e 6 il bit 32 (pixel instabile). Una posa può contenere più flag. Nessun nucleo esaminato presenta i bit 256 o 2048 di saturazione. Il test mantiene tutti i veto, senza sostituire i pixel. [Tabella DQ ufficiale UVIS](https://hst-docs.stsci.edu/wfc3ihb/appendix-e-reduction-and-calibration-of-wfc3-data/e-2-the-stsci-reduction-and-calibration-pipeline)

Il controllo aggiunge due chip e sei visite alla ricerca di supporto empirico, ma non aggiunge una visita fotometrica qualificata alle due già ammesse. L'esito riguarda le sei visite selezionate. Restano aperti il trasferimento della correzione cromatica e la verifica indipendente della PSF. Zero avvii PixInsight e zero chiusure scientifiche.

Per replicare, passare a `misura.py` la directory estratta dal kit, quella con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato. I FITS, le risposte MAST, le mappe PAM e il riferimento Gaia sono fissati per impronta. [Studio precedente](../bkl046-gd153-external-stare-visit-screen-v1/README.md)
