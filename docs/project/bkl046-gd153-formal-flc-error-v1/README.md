# BKL-046 · Incertezza formale ERR nel confronto GD153 con pose della stessa visita

Il programma propaga gli errori per pixel dell'estensione ERR dei prodotti WFC3/UVIS1 FLC. A ogni estrazione applica la stessa mappa PAM a segnale ed errore, calcola di nuovo il fondo mediano e ricalcola i tre stimatori. Usa 8.192 estrazioni gaussiane indipendenti per pixel, con centro, maschera DQ e calibrazione fissi. Verifica che la misura nominale coincida con il rapporto precedente e confronta la varianza Monte Carlo della somma con la propagazione analitica del modello diagonale. [Descrizione STScI delle estensioni SCI, ERR e DQ](https://hst-docs.stsci.edu/wfc3dhb/chapter-2-wfc3-data-structure/2-2-wfc3-file-structure)

| Posa | Banda | Differenza nominale, mediana per anello | Deviazione standard formale | Intervallo centrale delle estrazioni |
| --- | --- | ---: | ---: | ---: |
| iaah11daq | F606W | +2,01 mmag | 5,03 mmag | −9,59 a +10,04 mmag |
| iaah13ewq | F438W | +43,82 mmag | 7,16 mmag | +31,42 a +59,46 mmag |

In F438W, la differenza è 6,12 volte la deviazione standard formale per la mediana per anello. Anche la riscalatura per area dà una differenza di +33,15 mmag su 7,14 mmag di deviazione standard. Nei dieci confronti direzionali fra pose integre, corrispondenti a cinque coppie, le differenze assolute arrivano a 4,42 mmag. Ogni confronto usa una posa integra della stessa visita e banda.

L'incertezza per pixel trattata come indipendente non spiega la differenza F438W nel modello adottato. Gli intervalli descrivono perturbazioni attorno alle misure osservate. Il test non stima la covarianza spaziale, l'errore sistematico fra pose, l'incertezza dei campioni mancanti o la validità su altre stelle. Lo scarto espresso in unità di deviazione formale non è una significatività scientifica calibrata. Zero chiusure scientifiche e zero avvii PixInsight. [Correzione CTE e rumore nei prodotti WFC3](https://hst-docs.stsci.edu/wfc3dhb/chapter-6-wfc3-uvis-charge-transfer-efficiency-cte/6-4-the-pixel-based-model) · [Rapporto sulle misure nominali](../bkl046-gd153-natural-dq-sibling-flux-v1/README.md)

Per replicare, passare a `misura.py` il protocollo, la directory del kit FLC 11450, lo ZIP del confronto nella stessa visita, lo ZIP delle aperture integre, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato.