# BKL-046 · Effetto del prodotto FLC sul nucleo saturo ACS17656

Ho confrontato i prodotti FLT e FLC dei due FLT da 150 s e dei due riferimenti da 40 s. Il confronto usa le stesse centrature e ha verificato l'identità di esposizione, geometria del rivelatore e stato PCTECORR. Il supporto comune dei soli FLT è di 303 pixel. Includendo le maschere FLC, il confronto appaiato usa gli stessi 300 pixel in tutti gli otto prodotti. [Correzione CTE di CALACS](https://www.stsci.edu/hst/instrumentation/acs/performance/pixel-based-cte-corrections)

| Confronto con la media delle pose brevi | FLT | FLC | Variazione |
| --- | ---: | ---: | ---: |
| Posa lunga jfdp02vfq | +3,01% | +2,09% | −0,92 punti percentuali |
| Posa lunga jfdp02vdq | +3,12% | +2,09% | −1,03 punti percentuali |

La tabella usa il fondo a 35–48 px. Gli altri due anelli danno lo stesso ordine di grandezza. Sul supporto comune l'aumento FLT→FLC è circa 1,0–1,1% nelle pose lunghe e 2,0–2,1% nelle brevi. La differenza fra i due prodotti è misurata sullo stesso insieme di pixel. Il confronto osserva l'effetto della pipeline e non determina la CTE fisica residua, il flusso vero dei pixel mancanti o la causa dello scarto residuo. Il supporto resta sotto il requisito originario del 97%. Nessuna chiusura scientifica. [Diagnostica FLT su supporto comune](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/76a51ef60b781c9117c83bd18c6a19675b1c57e2/docs/project/bkl046-acs-17656-saturated-core-shared-support-v1)

Per ripetere, eseguire `verifica.py` con runtime Astropy, runtime SciPy, directory dei FLC, directory estratta dello studio 17656 originario con riferimenti brevi e PAM, directory dello studio di sensibilità, directory dello studio FLT su supporto comune, protocollo e un nuovo file di uscita. Il codice legge i dati e i protocolli vincolati per SHA-256.
