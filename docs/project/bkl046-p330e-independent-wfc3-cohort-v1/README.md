# BKL-046 · Controllo di una seconda stella WFC3, P330E nei programmi 17682 e 17962

Ho selezionato tutte le 30 osservazioni pubbliche individuali P330E nelle bande F438W, F606W e F814W del catalogo fissato. Appartengono a sei visite dei programmi di sensibilità nel tempo 17682 e 17962. Per ognuna, la ricerca MAST ha restituito il prodotto FLC CALWF3 corrispondente al nome esatto dell'esposizione. Ho scaricato e verificato tutti i 30 FITS, confrontando nome, bersaglio, programma, filtro e tempo di inizio con il catalogo. [Piano di calibrazione WFC3](https://www.stsci.edu/hst/instrumentation/wfc3/calibration-plan) · [Accesso ai prodotti MAST](https://archive.stsci.edu/datadownloads.html)

| Programma | Visite | FLC verificati | Pose ammesse |
| --- | ---: | ---: | ---: |
| 17682 | 4 | 20 | 0 |
| 17962 | 2 | 10 | 0 |

Tutti gli header riportano `SCAN_TYP=C` e `EXPFLAG=TDF-DOWN AT EXPSTART`. Il protocollo richiede pose con puntamento fisso e metadati nominali. Il controllo termina quindi prima della ricerca del centro, dell'esame DQ e della stima del flusso. Per le scansioni WFC3, STScI descrive una procedura fotometrica specifica con apertura rettangolare. [Calibrazione fotometrica STScI, ISR 2023-02](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration)

Zero terne qualificate, zero prove PixInsight e zero chiusure scientifiche. Resta aperta la verifica su una seconda stella con pose a puntamento fisso che soddisfino i criteri di geometria, supporto e tempo. L'esclusione riguarda i due programmi e le bande esaminate.

L'archivio H/K contiene il catalogo, le risposte MAST, i 30 FITS, due mappe PAM, la ricevuta di acquisizione, il protocollo e il risultato. Per ripetere senza accedere a MAST, passare a `misura.py` la directory estratta, quella con NumPy 2.3.5 e Astropy 7.2.0, un nuovo file di risultato e lo SHA-256 del manifest di acquisizione `efb9882c8fe77ec14d6d4aa2ab9e93a5538b20ff80b7568e396f0b3cb6eba792`.