# BKL-046 — Copertura effettiva e flag di saturazione su Orione F658N

Il test proietta una griglia ICRS di 161 × 161 posizioni attorno a RA 83,7996° e Dec −5,4097°. Il passo è 0,05 arcsec e il campo misura 8 × 8 arcsec. Per ogni posizione il WCS del singolo chip seleziona il fotosito più vicino. La lettura verifica insieme SCI e DQ, escludendo pixel privi di un valore finito o con bit geometrici 1, 2, 4 e 8. Il conteggio mantiene i flag separati per saturazione di full well (256) e saturazione del convertitore A/D (2048). La colonna di confronto riporta le posizioni sature nella posa lunga e pulite in entrambe le pose da 150 s e nella posa esclusa da 340 s, sul totale delle posizioni valide comuni.

| Esposizione | Secondi | Posizioni valide | Full well | A/D | Sature con riferimenti puliti / valide comuni |
|---|---:|---:|---:|---:|---:|
| j8mf01esq | 150 | 22025 | 0 | 0 | Riferimento |
| j8mf01euq | 150 | 22023 | 0 | 0 | Riferimento |
| j93k0aofq | 340 | 25921 | 0 | 0 | Riferimento |
| j8oc01svq | 509 | 25921 | 0 | 0 | 0 / 20559 |
| j8oc01sxq | 509 | 25921 | 0 | 0 | 0 / 20559 |
| j8oc01szq | 509 | 25921 | 0 | 0 | 0 / 20559 |
| j8oc01t1q | 509 | 25921 | 0 | 0 | 0 / 20559 |
| jcaz07f5q | 774 | 25921 | 3 | 0 | 3 / 20559 |
| jcaz07ffq | 822 | 25921 | 1 | 0 | 1 / 20559 |

Le posizioni pulite in tutti e tre i riferimenti sono 20559 delle 25921 interrogate.

Le due pose da 774 e 822 s hanno 0 posizioni sature in comune sulla griglia, mantenendo puliti i tre riferimenti. Questo campo fornisce un controllo di copertura. Per la saturazione ripetibile occorre un campione con più posizioni sature concordanti.

Le posizioni sulla griglia possono ricadere sullo stesso fotosito. I risultati non sono misure indipendenti di flusso. Il confronto è una prova di copertura e flag sulle singole immagini, con WCS di archivio. Per un controllo fotometrico restano da verificare la registrazione effettiva sulle sorgenti, la stabilità tra epoche e le incertezze di flusso. Zero esecuzioni native e chiusure scientifiche.

Gli intervalli FITS letti sono fissati per ETag, lunghezza, SHA-256 e corrispondenza del prefisso con il dossier precedente. Il replay offline usa gli stessi blocchi archiviati, Astropy 7.2.0 e NumPy 2.3.5. Lo script accetta directory del dossier, directory delle dipendenze, directory del dossier delle esposizioni, percorso di output e modo replay. Il modo acquire preleva gli intervalli dalla fonte pubblica.

[Dossier delle esposizioni](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/9a5d19b5f6ae35b9dcd7ca6880295602343b73ab/docs/project/bkl046-orion-acs-f658n-exposure-members-v1) · [Flag DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps) · [Archivio pubblico FITS HST](https://registry.opendata.aws/mast-hst/)