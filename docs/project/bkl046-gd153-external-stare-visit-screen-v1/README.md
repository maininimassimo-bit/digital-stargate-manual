# BKL-046 · Visite WFC3 di GD153 nei programmi 12334 e 14021

Ho verificato 12 associazioni MAST nelle bande F438W, F606W e F814W, due visite per programma. Nelle sei associazioni del programma 12334, la risposta archiviata di MAST non presenta prodotti FLC pubblici CALWF3. Il protocollo usa FLC e conserva i sei esiti a zero prodotti. Nel programma 14021, MAST presenta due FLC per associazione. Tutti e 12 sono stati acquisiti, riletti e identificati negli header. [Archivio MAST](https://hst-docs.stsci.edu/hstdhb/1-obtaining-hst-data/1-1-archive-overview) · [Piano di calibrazione WFC3](https://www.stsci.edu/hst/instrumentation/wfc3/calibration-plan)

| Visita | Chip | FLC | Veto DQ nel nucleo | Apertura o fondo rifiutati | Offset del centro |
| --- | ---: | ---: | ---: | ---: | ---: |
| icrw06 | UVIS1 | 6 | 3 | 2 | 1 |
| icrw07 | UVIS2 | 6 | 6 | 0 | 0 |

Le quattro terne di esposizioni hanno le stesse bande e lo stesso dither entro il limite di 0,05 giorni. Il filtro sul supporto esclude comunque tutte le pose. Nessuna visita aggiunge una terna fotometrica valida a 5 e 10 pixel. Il risultato si applica alle quattro visite esaminate. Restano disponibili altre associazioni pubbliche nel catalogo.

Il centro atteso usa il moto proprio Gaia e il WCS del prodotto. Il controllo conserva i veto DQ, usa PAM per il chip effettivo e misura il fondo con gli anelli 16–22 e 75–125 pixel. L'astrometria non include la parallasse dell'osservatore. Zero avvii PixInsight e zero chiusure scientifiche.

Per ripetere, passare a `misura.py` la directory del kit, quella con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo percorso di risultato. Il kit conserva risposte MAST, catalogo, FITS, PAM e Gaia. [Bilancio del trasferimento fra visite](../bkl046-gd153-visit-disjoint-aperture-color-v1/README.md)
