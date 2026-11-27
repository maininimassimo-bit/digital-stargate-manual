# GD153 · Confronto temporale ACS/WFC sull'amplificatore B

Sono stati acquisiti tutti i 18 FLT CALACS individuati nell'audit MAST delle visite jeuo02, jf4i02 e jflp04. Le coppie per filtro conservano identificativi, tempi, associazioni e hash. Tutti i file hanno `PCTECORR=OMIT`. Il controllo FLT/RAW verifica intestazioni, amplificatore, tempi e associazione. Il picco è stato associato alla posizione Gaia DR3 a epoca e all'header FITS, con soglia di cinque pixel per entrambi. Per l'apertura si è usata la PAM ufficiale WFC1 e il fondo mediano in un anello 25–40 pixel con almeno il 70% di supporto. [STScI, ACS Pixel Area Maps](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/pixel-area-maps)

| Raggio | Pose valide / esaminate | Pixel per posa esclusi dall'apertura |
| --- | ---: | ---: |
| 3 px | 18/18 | 0 |
| 5 px | 0/18 | 2 |
| 10 px | 0/18 | 16–19 |

Le tre aperture non presentano bit di saturazione CCD o A/D secondo FITS DQ. I flag che impediscono l'uso delle aperture più ampie indicano, fra l'altro, pixel caldi e tiepidi, instabilità e trappole di carica. Tutti i rifiuti sono conservati nel riscontro. [STScI, ACS DQ](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/dq-flag-definitions)

A 3 pixel, i due rate di ciascuna coppia per visita e filtro differiscono dello 0,13–1,56% rispetto alla loro media. Le tre visite sono comparabili entro 0,01466 giorni tra prima e ultima posa di ciascuna visita. Con PHOTFLAM e la media delle due pose per filtro, l'escursione fra visite è 16,95 mmag in F435W−F606W, 13,48 in F435W−F814W e 15,62 in F606W−F814W. Sono colori dell'apertura, senza correzione dipendente dal filtro per encircled energy e con CTE non corretta. Le differenze comprendono la risposta dell'apertura e la dipendenza dalla posizione subpixel. Per attribuire una variazione alla risposta, servono una stima dell'apertura completa con supporto verificato, un trattamento della CTE e confronti su posizioni e amplificatori distinti. Nessun avvio nativo e nessuna chiusura scientifica.

La ripetizione dall'archivio su H: ha verificato il JSON per esposizione e riprodotto byte per byte la sintesi. SHA-256 del riscontro `618a3295451c1cebefd9de1b639da6c9d00dee2889f5f8e15b0a715f7c41155e`. SHA-256 della sintesi `be0234bf2b5e8b763fc8389b9316cd05f4d52d73dfaf3ad1a8d13ff7470808ba`. SHA-256 dell'archivio `342e3705a9e422459730beff4317a92b99e577da3d9e61f953eb5b49d4b885a5`.

[Selezione e provenienza delle visite](BKL-046-GD153-ACS-CATALOGO.md).
