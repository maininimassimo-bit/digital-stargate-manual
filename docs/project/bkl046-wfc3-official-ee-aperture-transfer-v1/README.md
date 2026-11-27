# BKL-046 · Curve di energia racchiusa WFC3 e correzione del colore

Ho verificato le due tabelle STScI `wfc3uvis[12]_aper_007_syn.csv` e usato le colonne nominali da 0,20 e 0,40 secondi d'arco per le misure a 5 e 10 pixel. Ho verificato dai FITS il chip e l'apertura nominale di ogni terna. Le nove visite comprendono due GD153 su UVIS1, due GRW+70°5824 su UVIS1 e cinque GRW+70°5824 su UVIS2. Le due terne in ciascuna visita GD153 sono aggregate con la mediana. [Tabelle e raccomandazioni STScI](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration/uvis-encircled-energy)

Ho confrontato la stima zero, la tabella del chip fisico e una lettura per raggio della raccomandazione STScI. Quest'ultima usa UVIS1 a 5 pixel nell'angolo specificato dell'amplificatore A e UVIS2 negli altri casi. Il rapporto quantifica anche la sensibilità all'uso della stessa tabella a entrambi i raggi. La documentazione STScI indica che per il passaggio da aperture piccole al raggio standard conviene misurare la correzione sui dati quando possibile.

| Stella e chip | F438W − F814W, errore assoluto mediano senza correzione | Tabella del chip fisico | Raccomandazione per raggio |
| --- | ---: | ---: | ---: |
| GD153 UVIS1 | 5,74 mmag | 4,50 mmag | 4,37 mmag |
| GRW+70°5824 UVIS1 | 4,77 mmag | 4,77 mmag | 16,57 mmag |
| GRW+70°5824 UVIS2 | 27,01 mmag | 5,35 mmag | 5,35 mmag |

La tabella di UVIS2 riduce nettamente l'errore F438W − F814W su UVIS2. Nelle stesse cinque visite, per F606W − F814W l'errore mediano passa da 12,83 a 13,49 mmag. Su UVIS1, il risultato dipende anche dalla posizione dell'apertura. Le visite GRW+70°5824 ammesse comprendono una posa per visita in ciascuna banda, con una visita nell'angolo dell'amplificatore A e l'altra in quello dell'amplificatore B.

Il confronto diagnostica l'applicazione delle curve ai casi osservati. Le tabelle derivano anche da osservazioni di stelle usate qui, con GRW+70°5824 nella calibrazione F814W. Rimangono aperte la verifica indipendente delle curve, l'incertezza alla scala di 5 pixel e la verifica nativa. Zero chiusure scientifiche e zero avvii PixInsight. [Censimento GRW+70°5824](../bkl046-grw70-11907-held-out-color-transfer-v1/README.md)

Per ripetere, passare a `misura.py` la directory estratta con le tabelle CSV, lo ZIP del centro GD153, la directory FLC GD153, gli ZIP del primo lotto GRW+70°5824 e del censimento, la directory con Astropy 7.2.0 e un nuovo percorso di risultato.