# BKL-046 · Riferimenti indipendenti DECam per M8/M20

La ricerca NOIRLab SIA ha restituito 7 righe per M8 e 23 per M20 nelle finestre da 0,05 gradi centrate sulle coordinate ICRS di SIMBAD. Il kit verifica sei ritagli FITS grezzi in banda r. In tutti il centro di catalogo ricade nel rettangolo del rispettivo ritaglio secondo il WCS del FITS. [Servizio SIA di NOIRLab](https://datalab.noirlab.edu/docs/manual/UsingAstroDataLab/DataAccessInterfaces/SimpleImageAccessSIA/SimpleImageAccessSIA.html) · [M8 in SIMBAD](https://simbad.cds.unistra.fr/simbad/sim-id?Ident=M+8) · [M20 in SIMBAD](https://simbad.cds.unistra.fr/simbad/sim-id?Ident=M20)

| Campo | Durata | CCD | Campioni non nulli sotto entrambi i livelli | Campioni a entrambi i livelli o sopra | Codici zero |
| --- | ---: | ---: | ---: | ---: | ---: |
| M8 | 30 s | 53 | 382.638 | 3.624 | 0 |
| M8 | 45 s | 28 | 35.397 | 164.563 | 0 |
| M8 | 100 s | 28 | 0 | 163.944 | 35.397 |
| M20 | 30 s | 73 | 372.710 | 0 | 0 |
| M20 | 180 s | 15 | 393.129 | 0 | 0 |
| M20 | 180 s | 15 | 393.129 | 0 | 0 |

Due campioni M8 da 45 s cadono fra i due livelli. Il conteggio usa il minore e il maggiore fra `SATURATA` e `SATURATB` dell'header. Queste soglie sono un controllo preliminare. La qualificazione richiede l'associazione per amplificatore e i livelli calibrati, oltre al controllo di linearità. I codici zero sono riportati a parte e la loro origine resta da verificare. [Guida DECam](https://www.ctio.noirlab.edu/noao/sites/default/files/DECam/DECamUG_v2.0.5-ARW.pdf)

Le pose M8 da 45 e 100 secondi condividono CCD, programma e notte. Il ritaglio da 100 s non ha campioni non nulli sotto entrambi i livelli. La posa da 30 s usa un altro CCD e un'altra data e supera le due soglie in 3.624 campioni. Le tre pose M20 della stessa notte offrono un controllo di trasferimento in banda r tra 30 e 180 secondi, ma nei ritagli verificati manca un caso sopra le soglie. I FITS DECam sono indipendenti dalla serie Colmic e differiscono per strumento, banda ed epoca. Il loro uso per la serie Colmic richiede co-registrazione, controllo delle PSF e verifica del trasferimento fotometrico.

Per ripetere, estrarre il kit di progetto, quindi passare a `verifica.py` la directory del kit, quella con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato. Gli URL individuali e le impronte sono nel rapporto. Lo ZIP di progetto contiene i FITS e i cataloghi SIA riletti. Zero avvii PixInsight e zero chiusure scientifiche.

I dati provengono dall'Astro Data Archive di NSF NOIRLab, gestito da AURA tramite accordo di cooperazione con la National Science Foundation. [Astro Data Archive](https://astroarchive.noirlab.edu/)
