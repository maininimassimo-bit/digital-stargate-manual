# BKL-046 · Saturazione differenziale fra tre bande in G191B2B

La visita ACS 10054 ha due pose ciascuna in F606W, F658N e F660N sul chip 1, amplificatore B, apertura WFC1-1K. Entrambe le pose F606W hanno DQ 256 nel pixel di picco e nessun flag ADC entro 10 px. Le quattro pose a banda stretta hanno DQ nullo nel picco e nessun flag di saturazione entro 10 px. I centri sono massimi locali a distanza 0,63–0,69 arcsec dalla posizione mirata. [Flag CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

| Supporto di apertura a 10 px | F606W/F660N, rapporto registrato | F658N/F660N, rapporto registrato |
| --- | ---: | ---: |
| DQ ammessi per ciascuna posa | 1,4272 | 1,0087 |
| DQ ammessi più valore registrato del centro F606W | 1,6723 | 1,0087 |
| 304 offset comuni simmetrici su 317 | 1,6944 | 1,0037 |

I rapporti usano medie per banda di tassi PAM e fondo, convertiti con PHOTFLAM. L'apertura comune scarta il centro anche nelle pose non sature. Le somme quindi cambiano con il supporto in misura diversa secondo la banda. L'inclusione del valore registrato del nucleo F606W resta un confronto diagnostico. Non si ricostruisce il flusso vero del nucleo. Le pose sono sequenziali con filtri e tempi distinti. Il risultato riguarda queste bande ACS e non qualifica la risposta di un sensore CFA o la ricomposizione RGB.

Per ripetere, eseguire `verifica.py` con runtime Astropy, directory dei sei FITS e del loro manifest, mappa PAM, protocollo e un nuovo percorso di uscita. Il codice verifica le impronte delle immagini, del manifest e della PAM.
