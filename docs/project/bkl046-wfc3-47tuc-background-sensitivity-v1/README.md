# BKL-046 · Sensibilità dei colori di 47 Tucanae alla stima del fondo

Ho riletto le stesse tre esposizioni e le stesse 23 sorgenti ammesse di 47 Tucanae. Ho riprodotto il risultato con il fondo mediano fra 16 e 22 pixel, poi ho ricalcolato le aperture da 5 e 10 pixel mantenendo fissi i centri e le maschere. Le alternative sono due mediane in anelli esterni, 24–30 e 32–38 pixel, e un piano locale robusto stimato fra 16 e 30 pixel. Tutte le 23 sorgenti restano misurabili nelle quattro condizioni. [Fotometria di riferimento](../bkl046-wfc3-external-field-ee-v1/README.md)

| Fondo su UVIS2 | Variazione mediana assoluta rispetto al fondo originale | Errore mediano senza tabella EE | Errore mediano con tabella EE |
| --- | ---: | ---: | ---: |
| Mediana 16–22 pixel | 0,00 mmag | 4,93 mmag | 27,43 mmag |
| Mediana 24–30 pixel | 2,02 mmag | 4,45 mmag | 28,36 mmag |
| Mediana 32–38 pixel | 2,20 mmag | 4,51 mmag | 27,89 mmag |
| Piano robusto 16–30 pixel | 2,30 mmag | 3,57 mmag | 24,19 mmag |

La tabella riguarda il colore F606W − F814W. Cambiare la stima del fondo sposta la mediana, ma in tutte e quattro le condizioni la correzione tabulata aumenta l'errore mediano UVIS2. Con il piano robusto, una singola misura cambia di 39,31 mmag rispetto al fondo originale. Il rapporto conserva anche gli altri colori e UVIS1.

È una prova di sensibilità sullo stesso campo. I dati non separano il contributo dei vicini sotto soglia, il vero fondo e la variazione della PSF. Restano aperti la verifica su più campi, il confronto con riferimenti indipendenti e la prova nativa. Nessuna chiusura scientifica e nessun avvio PixInsight.

Per ripetere, passare a `misura.py` il protocollo, lo ZIP dei due campi, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo risultato.