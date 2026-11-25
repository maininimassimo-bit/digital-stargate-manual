# BKL-046 — Fotometria ACS a tre bande di GD153

Il primo controllo, con una tolleranza WCS di cinque pixel, non ha identificato la sorgente. Una seconda ricerca limitata a 30 pixel dalla posizione Gaia propagata ha individuato un picco compatibile in tutte le pose, con centri entro due pixel per asse. I picchi distano 11,9–13,3 pixel dalla posizione Gaia proiettata. La corrispondenza è sostenuta dalla ripetizione e dal puntamento delle pose. La discrepanza astrometrica resta registrata. Le misure usano la mappa d’area WFC1 archiviata e il tempo EXPTIME di ciascun FITS. [Correzione dell’area dei pixel ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/pixel-area-maps)

Con raggio di tre pixel e DQ zero nell’intera apertura, tutte e sei le pose sono misurabili. I rapporti di elettroni al secondo sono F658N/F660N = 2,55113, F658N/F606W = 0,0235531 e F660N/F606W = 0,00923244. La differenza fra le due pose della stessa banda, divisa per la loro media, varia dallo 0,035% allo 0,450%. A raggio 5 passano solo le due pose F658N. A raggio 10, tutte le pose includono due pixel con DQ 64.

Due ripetizioni offline coincidono. Il rapporto riguarda un’apertura piccola e nessun prodotto ha una correzione CTE nei FITS utilizzati. Restano da verificare la dipendenza dal raggio, il confronto con CALSPEC e la risposta all’epoca 2003. Nessuna chiusura scientifica.
SHA-256 archivio H: 3ee3f35de8544ae5e8443b77c6c70022316f00e9fbeb0a4b36ea920922a5f27a.
